"""Thinking partner — Socratic questioning with conversation memory.
Usage:
  python tools/thinking_partner.py "I want to start X but don't know how"
"""
import sys, datetime, re, uuid
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
CONV_DIR = MEM_DIR / "conversations"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db import init_db, load_recent_sessions


def load_context():
    parts = []
    cp = MEM_DIR / "checkpoint.md"
    if cp.exists():
        for line in cp.read_text(encoding="utf-8").splitlines():
            if line.startswith("phase:"):
                parts.append(("checkpoint", line.split(":", 1)[1].strip()))
            elif line.startswith("current_topic:"):
                parts.append(("topic", line.split(":", 1)[1].strip()))

    goals = MEM_DIR / "goals.md"
    if goals.exists():
        lines = [l.strip() for l in goals.read_text(encoding="utf-8").splitlines()
                 if l.strip().startswith("- title:")]
        for l in lines[:3]:
            parts.append(("goal", l.replace("- title:", "").strip().strip('"')))
    return parts


def load_recent_decisions(limit=5):
    decisions = []
    fp = MEM_DIR / "decisions.md"
    if not fp.exists():
        return decisions
    content = fp.read_text(encoding="utf-8")
    for line in reversed(content.splitlines()):
        if line.startswith("- ") and not line.startswith("- decision:"):
            decisions.append(line[2:].strip())
            if len(decisions) >= limit:
                break
        elif line.startswith("## "):
            match = re.match(r"## (\d{4}-\d{2}-\d{2}) — (.+)", line)
            if match and decisions:
                decisions[-1] = f"[{match.group(1)}] {decisions[-1]}"
    return list(reversed(decisions))


def load_related_sessions(topic, limit=3):
    init_db()
    sessions = load_recent_sessions(days=7)
    topic_lower = topic.lower()
    result = []
    for s in sessions:
        skill = s.get("skill", "")
        notes = s.get("notes", "")
        if topic_lower in skill.lower() or topic_lower in notes.lower():
            result.append({"date": s.get("date", ""), "skill": skill, "notes": notes})
            if len(result) >= limit:
                break
    return result


def load_past_conversations(topic, limit=2):
    convos = []
    if not CONV_DIR.exists():
        return convos
    topic_lower = topic.lower()
    for fp in sorted(CONV_DIR.glob("*.md"), reverse=True):
        text = fp.read_text(encoding="utf-8")
        t = p = d = ""
        key_points = []
        for line in text.splitlines():
            if line.startswith("topic:"):
                t = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("problem:"):
                p = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("date:"):
                d = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("- key_point:"):
                key_points.append(line.split(":", 1)[1].strip().strip('"'))
        if topic_lower in t.lower() or topic_lower in p.lower():
            convos.append({"date": d, "topic": t, "problem": p, "key_points": key_points})
            if len(convos) >= limit:
                break
    return convos


def save_conversation(statement, questions, topic_guess):
    CONV_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    cid = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = CONV_DIR / f"conv-{cid}.md"

    content = f"""---
id: "conv-{cid}"
date: "{today}"
topic: "{topic_guess}"
problem: "{statement[:200]}"
status: open
---

# Conversation: {topic_guess}

## Problem
{statement}

## Questions Asked
"""
    for i, q in enumerate(questions, 1):
        content += f"{i}. {q}\n"

    content += """
## Key Points
- (to be filled after discussion)

## Decision
- (to be filled when decided)

## Outcome
- (to be filled after implementation)
"""
    path.write_text(content, encoding="utf-8")
    return path


def log_decision(topic, decision):
    fp = MEM_DIR / "decisions.md"
    today = datetime.date.today().isoformat()
    entry = f"\n## {today} — {topic}\n- {decision}\n"
    if fp.exists():
        content = fp.read_text(encoding="utf-8")
        content += entry
        fp.write_text(content, encoding="utf-8")
    else:
        fp.write_text(f"# Decisions Log\n{entry}", encoding="utf-8")


def thinking_partner(statement):
    ctx = load_context()
    decisions = load_recent_decisions()
    related_sessions = load_related_sessions(statement)
    past_convos = load_past_conversations(statement)

    print("=== Thinking Partner Mode ===\n")
    print(f'You said: "{statement}"\n')

    if past_convos:
        print("--- Past Related Conversations ---")
        for c in past_convos:
            print(f"  [{c['date']}] {c['topic']}")
            for kp in c["key_points"][:2]:
                print(f"    - {kp}")
        print()

    if related_sessions:
        print("--- Related Sessions ---")
        for s in related_sessions:
            print(f"  [{s['date']}] {s['skill']}: {s['notes'][:80]}")
        print()

    if decisions:
        print("--- Recent Decisions ---")
        for d in decisions[-3:]:
            print(f"  - {d}")
        print()

    lower = statement.lower()
    if any(w in lower for w in ["don't know how", "stuck", "confused", "overwhelmed"]):
        questions = [
            "What's the ONE thing that would make the biggest difference right now?",
            "What have you already tried? What happened?",
            "If you had to explain this to a 10-year-old, what would you say?",
        ]
    elif any(w in lower for w in ["should i", "which", "choose", "decide"]):
        questions = [
            "What does your gut say before you overthink it?",
            "What's the worst that happens if you pick the wrong one?",
            "Which option excites you more, even slightly?",
        ]
    elif any(w in lower for w in ["want to", "plan", "goal", "start", "build"]):
        questions = [
            "What does done look like? Be specific.",
            "What's the smallest version of this you could do today?",
            "Who else has done this? What can you learn from them?",
        ]
    elif any(w in lower for w in ["problem", "issue", "broken", "fix"]):
        questions = [
            "What exactly is failing? What do you see vs what you expect?",
            "When did this last work? What changed?",
            "If you had to debug this step by step, where would you start?",
        ]
    else:
        questions = [
            "Can you say more about what's really driving this?",
            "What would success look like here?",
            "What's the first concrete step you could take?",
        ]

    print("Let me ask you some questions to clarify:\n")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")

    if ctx:
        print(f"\nContext from your coach:")
        for label, val in ctx:
            print(f"  - [{label}] {val}")

    topic_guess = statement[:50].strip()
    conv_path = save_conversation(statement, questions, topic_guess)

    print(f"\n---")
    print("Answer these questions, then I'll help you structure a plan.")
    print(f"Conversation saved: {conv_path.name}")
    print("When you reach a decision, tell me and I'll log it.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/thinking_partner.py \"your thought/problem here\"")
        print("\nExamples:")
        print('  python tools/thinking_partner.py "I want to learn SEO but feel overwhelmed"')
        print('  python tools/thinking_partner.py "Should I focus on content or technical SEO?"')
        print('  python tools/thinking_partner.py "My website traffic dropped"')
        sys.exit(1)

    statement = " ".join(sys.argv[1:])
    thinking_partner(statement)


if __name__ == "__main__":
    main()
