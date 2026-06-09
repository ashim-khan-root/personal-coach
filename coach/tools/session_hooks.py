"""Session lifecycle hooks — pre-session context + post-session analysis.
Usage:
  python tools/session_hooks.py pre
  python tools/session_hooks.py post <skill> <duration> <rating> [notes]
"""
import sys, datetime, re
from pathlib import Path

COACH_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(COACH_DIR))

MEM_DIR = COACH_DIR / "memory"
SESS_DIR = MEM_DIR / "sessions"
CONV_DIR = MEM_DIR / "conversations"


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

    print("=== Session Context ===")
    for p in ctx_parts:
        print(f"  {p}")
    print(f"  {datetime.date.today()} — ready to start")
    return ctx_parts


def post_session(skill, duration, rating, notes=""):
    """Run after storing a session — triggers insight extraction + vector index."""
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

    try:
        from tools.index_memory_lightrag import build_index as _lr_build
        _lr_build()
        print("[hooks] LightRAG index refreshed")
    except Exception:
        pass

    try:
        from tools.index_memory import build_index
        build_index()
        print("[hooks] TF-IDF index refreshed")
    except Exception as e:
        print(f"[hooks] Vector index refresh skipped: {e}")

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
