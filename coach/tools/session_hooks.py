"""Session lifecycle hooks — pre-session context + post-session analysis.
Usage:
  python tools/session_hooks.py pre
  python tools/session_hooks.py post <skill> <duration> <rating> [notes]
"""
import sys, datetime, re, io
from pathlib import Path

COACH_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(COACH_DIR))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

MEM_DIR = COACH_DIR / "memory"
SESS_DIR = MEM_DIR / "sessions"
CONV_DIR = MEM_DIR / "conversations"


def _load_evolution_suggestions():
    """Load draft (not-yet-created) skill suggestions."""
    path = MEM_DIR / "evolution_suggestions.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    drafts = []
    current = {}
    for line in text.splitlines():
        if line.startswith("- id:"):
            if current:
                drafts.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
        elif line.startswith("  suggested_skill_name:"):
            current["name"] = line.split(":", 1)[1].strip()
        elif line.startswith("  confidence:"):
            try:
                current["confidence"] = float(line.split(":", 1)[1].strip())
            except ValueError:
                current["confidence"] = 0.0
        elif line.startswith("  cluster_size:"):
            try:
                current["cluster_size"] = int(line.split(":", 1)[1].strip())
            except ValueError:
                current["cluster_size"] = 0
        elif line.startswith("  status:"):
            current["status"] = line.split(":", 1)[1].strip()
        elif line.startswith("  summary:"):
            current["summary"] = line.split(":", 1)[1].strip()
    if current:
        drafts.append(current)
    return drafts


def _top_insights(n=3):
    """Return top N insights by confidence."""
    path = MEM_DIR / "insights.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    insights = []
    current = {}
    for line in text.splitlines():
        if line.startswith("- id:"):
            if current:
                insights.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
        elif line.startswith("  pattern:"):
            current["pattern"] = line.split(":", 1)[1].strip()
        elif line.startswith("  category:"):
            current["category"] = line.split(":", 1)[1].strip()
        elif line.startswith("  confidence:"):
            try:
                current["confidence"] = float(line.split(":", 1)[1].strip())
            except ValueError:
                current["confidence"] = 0.0
        elif line.startswith("  summary:"):
            current["summary"] = line.split(":", 1)[1].strip()
    if current:
        insights.append(current)
    insights.sort(key=lambda x: x.get("confidence", 0), reverse=True)
    return insights[:n]


def pre_session():
    """Print a compact context summary before starting work."""
    ctx_parts = []

    checkpoint = MEM_DIR / "checkpoint.md"
    if checkpoint.exists():
        text = checkpoint.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("phase:"):
                ctx_parts.append(line.replace("phase:", "Phase:").strip())
            elif line.startswith("current_topic:"):
                ctx_parts.append(line.replace("current_topic:", "Topic:").strip())
            elif line.startswith("next_task:"):
                ctx_parts.append(line.replace("next_task:", "Next:").strip())

    goals = MEM_DIR / "goals.md"
    if goals.exists():
        g_lines = [l for l in goals.read_text(encoding="utf-8").splitlines()
                   if l.strip().startswith("- title:")]
        if g_lines:
            titles = [l.replace("- title:", "").strip().strip('"') for l in g_lines[:3]]
            ctx_parts.append(f"Goals: {' | '.join(titles)}")

    habits_today = MEM_DIR / "habits.md"
    if habits_today.exists():
        h_count = sum(1 for l in habits_today.read_text(encoding="utf-8").splitlines()
                      if l.strip().startswith("title:"))
        ctx_parts.append(f"Habits tracked: {h_count}")

    last_sesh = sorted(SESS_DIR.glob("session-*.md"), reverse=True)
    if last_sesh:
        text = last_sesh[0].read_text(encoding="utf-8")
        skill = ""
        rating = ""
        for line in text.splitlines():
            if line.startswith("skill:"):
                skill = line.split(":", 1)[1].strip()
            elif line.startswith("rating:"):
                rating = line.split(":", 1)[1].strip()
        if skill:
            ctx_parts.append(f"Last session: {skill} ({rating}/10)")

    decisions_fp = MEM_DIR / "decisions.md"
    if decisions_fp.exists():
        d_content = decisions_fp.read_text(encoding="utf-8")
        recent_decisions = []
        for line in reversed(d_content.splitlines()):
            if line.startswith("- ") and not line.startswith("- decision:"):
                recent_decisions.append(line[2:].strip())
                if len(recent_decisions) >= 3:
                    break
        if recent_decisions:
            ctx_parts.append(f"Recent decisions: {'; '.join(reversed(recent_decisions))}")

    if CONV_DIR.exists():
        conv_files = sorted(CONV_DIR.glob("conv-*.md"), reverse=True)
        if conv_files:
            text = conv_files[0].read_text(encoding="utf-8")
            topic = ""
            for line in text.splitlines():
                if line.startswith("topic:"):
                    topic = line.split(":", 1)[1].strip().strip('"')
                    break
            if topic:
                ctx_parts.append(f"Open conversation: {topic}")

    insights = _top_insights(3)
    if insights:
        parts = [f"{i.get('pattern', '?')} ({i.get('category', '?')})" for i in insights]
        ctx_parts.append(f"Top patterns: {' | '.join(parts)}")

    drafts = _load_evolution_suggestions()
    new_drafts = [d for d in drafts if d.get("status") == "draft"]
    applied = [d for d in drafts if d.get("status") == "applied"]
    if new_drafts:
        ctx_parts.append(f"Pending skills: {', '.join(d.get('name', '?') for d in new_drafts[:3])}")
    if applied:
        ctx_parts.append(f"Auto-created skills: {', '.join(d.get('name', '?') for d in applied[:3])}")

    print("=== Session Context ===")
    for p in ctx_parts:
        print(f"  {p}")
    print(f"  {datetime.date.today()} — ready to start")
    return ctx_parts


def post_session(skill, duration, rating, notes=""):
    """Run after storing a session — triggers insight extraction, skill evolution, vector index."""
    from tools.extract_insights import load_sessions, extract_patterns, deduplicate_insights, write_insights, write_observation

    sessions = load_sessions()
    if not sessions:
        print("[hooks] No sessions loaded for post-session analysis.")
        return

    insights = extract_patterns(sessions)
    insights = deduplicate_insights(insights)
    count = write_insights(insights)
    write_observation("session_completed", {
        "skill": skill, "duration": duration, "rating": rating, "notes": notes[:200]
    })
    print(f"[hooks] Session stored + insights refreshed ({count} patterns)")

    prev_count_path = MEM_DIR / ".prev_insight_count"
    try:
        prev_count = int(prev_count_path.read_text(encoding="utf-8").strip())
    except (FileNotFoundError, ValueError):
        prev_count = -1

    if count != prev_count:
        prev_count_path.write_text(str(count), encoding="utf-8")
        try:
            from tools.evolve_skill import parse_insights, cluster_for_evolution, write_suggestions, skill_exists

            all_insights = parse_insights()
            suggestions = cluster_for_evolution(all_insights, min_confidence=0.5, min_cluster=2)
            sug_count = write_suggestions(suggestions)

            opencode_skills = Path(__file__).resolve().parent.parent.parent / ".opencode" / "skills"

            new_suggestions = [s for s in suggestions if not skill_exists(s["suggested_skill_name"])]
            auto_created = []

            for s in new_suggestions:
                if s["confidence"] >= 0.7:
                    skill_name = s["suggested_skill_name"]
                    skill_dir = opencode_skills / skill_name
                    if not skill_dir.exists():
                        skill_dir.mkdir(parents=True, exist_ok=True)
                        summary = s.get("summary", f"Auto-evolved skill from {s['cluster_size']} insights")
                        description = f"When the user is working on {skill_name.replace('-', ' ')}. Auto-generated from observed patterns."
                        sk = skill_dir / "SKILL.md"
                        sk.write_text(
                            f"---\nname: {skill_name}\ndescription: {description}\n---\n\n"
                            f"# {skill_name.replace('-', ' ').title()}\n\n"
                            f"Auto-evolved skill. {summary}\n\n"
                            f"## Background\n\n"
                            f"Confidence: {s['confidence']} | Cluster size: {s['cluster_size']} | "
                            f"Categories: {', '.join(s.get('categories', []))}\n\n"
                            f"## Workflow\n\n"
                            f"Follow standard coaching workflow: RESEARCH → PLAN → EXECUTE → REVIEW.\n\n"
                            f"## Verification\n\n"
                            f"- [ ] Output meets user expectations\n"
                            f"- [ ] Follows project conventions\n",
                            encoding="utf-8"
                        )
                        auto_created.append(skill_name)

            if auto_created:
                evo_path = MEM_DIR / "evolution_suggestions.md"
                if evo_path.exists():
                    evo_text = evo_path.read_text(encoding="utf-8")
                    for name in auto_created:
                        evo_text = evo_text.replace(f"  status: draft\n  action: Create skills/{name}/SKILL.md",
                                                     f"  status: applied\n  action: Auto-created .opencode/skills/{name}/SKILL.md")
                    evo_path.write_text(evo_text, encoding="utf-8")

            learnings = []
            learnings.append(f"# Latest Learnings — {datetime.date.today().isoformat()}")
            learnings.append("")

            top_ins = sorted(all_insights, key=lambda x: x.get("confidence", 0), reverse=True)[:3]
            learnings.append("## Top Patterns")
            for ins in top_ins:
                cat = ins.get("category", "?").capitalize()
                pat = ins.get("pattern", "?")
                conf = ins.get("confidence", 0)
                summary = ins.get("summary", "")
                learnings.append(f"- [{cat}] {pat} ({conf}): {summary}")
            learnings.append("")

            if new_suggestions:
                learnings.append("## Skill Suggestions")
                for s in new_suggestions:
                    status = "✅ auto-created" if s["suggested_skill_name"] in auto_created else "💡 draft"
                    learnings.append(f"- {s['suggested_skill_name']} (confidence {s['confidence']}) — {status}")
                learnings.append("")

            if auto_created:
                learnings.append(f"Auto-created {len(auto_created)} skill(s): {', '.join(auto_created)}")

            learnings_path = MEM_DIR / "latest_learnings.md"
            learnings_path.write_text("\n".join(learnings), encoding="utf-8")
            print(f"[hooks] Skill evolution: {sug_count} suggestions ({len(new_suggestions)} new, {len(auto_created)} auto-created)")
        except Exception as e:
            print(f"[hooks] Skill evolution skipped: {e}")
    else:
        print("[hooks] No new patterns — skill evolution skipped")

    try:
        from tools.index_memory_lightrag import build_index as _lr_build
        _lr_build()
        print("[hooks] Index refreshed")
    except Exception:
        try:
            from tools.index_memory import build_index
            build_index()
            print("[hooks] Index refreshed (TF-IDF fallback)")
        except Exception as e:
            print(f"[hooks] Index refresh skipped: {e}")

    return count


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/session_hooks.py pre|post <args>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "pre":
        pre_session()
    elif command == "post":
        if len(sys.argv) < 4:
            print("Usage: python tools/session_hooks.py post <skill> <duration> <rating> [notes]")
            sys.exit(1)
        skill = sys.argv[2]
        duration = sys.argv[3]
        rating = sys.argv[4]
        notes = sys.argv[5] if len(sys.argv) > 5 else ""
        post_session(skill, duration, rating, notes)
    else:
        print(f"Unknown hook: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
