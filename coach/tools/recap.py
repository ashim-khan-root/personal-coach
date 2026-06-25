"""Recap — summarize recent activity across sessions, decisions, and daily notes.
Usage:
  python tools/recap.py          # Last 7 days
  python tools/recap.py 14       # Last 14 days
"""
import sys, datetime, re
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
SESSIONS_DIR = MEM_DIR / "sessions"
CONV_DIR = MEM_DIR / "conversations"
DAILY_DIR = MEM_DIR / "daily"

_FIELD_PARSERS = {
    "date": ("date", str),
    "skill": ("skill", str),
    "rating": ("rating", str),
    "duration_min": ("duration", str),
    "notes": ("notes", str),
}

def _parse_session_file(text: str) -> dict:
    data = {}
    decisions = []
    for line in text.splitlines():
        for prefix, (key, _) in _FIELD_PARSERS.items():
            if line.startswith(f"{prefix}:"):
                data[key] = line.split(":", 1)[1].strip().strip('"')
                break
        else:
            if line.startswith("- decision:"):
                decisions.append(line.split(":", 1)[1].strip().strip('"'))
    data["decisions"] = decisions
    return data


def load_recent_sessions(days):
    cutoff = datetime.date.today() - datetime.timedelta(days=days)
    sessions = []
    if not SESSIONS_DIR.exists():
        return sessions
    for fp in sorted(SESSIONS_DIR.glob("session-*.md"), reverse=True):
        data = _parse_session_file(fp.read_text(encoding="utf-8"))
        try:
            d = datetime.date.fromisoformat(data.get("date", "").split("T")[0])
            if d >= cutoff:
                sessions.append(data)
        except (ValueError, IndexError):
            pass
    return sessions


def load_recent_conversations(days):
    cutoff = datetime.date.today() - datetime.timedelta(days=days)
    convos = []
    if not CONV_DIR.exists():
        return convos
    for fp in sorted(CONV_DIR.glob("*.md"), reverse=True):
        text = fp.read_text(encoding="utf-8")
        date = topic = ""
        key_points = []
        for line in text.splitlines():
            if line.startswith("date:"):
                date = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("topic:"):
                topic = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("- ") and "key_point" in line.lower():
                val = line.split(":", 1)[1].strip().strip('"') if ":" in line else line[2:].strip()
                key_points.append(val)
        try:
            d = datetime.date.fromisoformat(date)
            if d >= cutoff:
                convos.append({"date": date, "topic": topic, "key_points": key_points, "file": fp.name})
        except (ValueError, IndexError):
            pass
    return convos


def load_recent_decisions(days):
    cutoff = datetime.date.today() - datetime.timedelta(days=days)
    decisions = []
    fp = MEM_DIR / "decisions.md"
    if not fp.exists():
        return decisions
    current_date = ""
    topic = ""
    for line in fp.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            match = re.match(r"## (\d{4}-\d{2}-\d{2}) — (.+)", line)
            if match:
                current_date = match.group(1)
                topic = match.group(2)
        elif line.startswith("- ") and current_date:
            try:
                if datetime.date.fromisoformat(current_date) >= cutoff:
                    decisions.append({"date": current_date, "topic": topic, "decision": line[2:].strip()})
            except ValueError:
                pass
    return decisions


def generate_recap(days=7):
    sessions = load_recent_sessions(days)
    convos = load_recent_conversations(days)
    decisions = load_recent_decisions(days)

    report = []
    report.append(f"## Recap: Last {days} Days")
    report.append(f"**Period:** {(datetime.date.today() - datetime.timedelta(days=days)).isoformat()} to {datetime.date.today().isoformat()}\n")

    report.append(f"### Activity Summary")
    report.append(f"- Sessions: {len(sessions)}")
    report.append(f"- Conversations: {len(convos)}")
    report.append(f"- Decisions: {len(decisions)}")

    if sessions:
        report.append(f"\n### Sessions")
        by_skill = {}
        for s in sessions:
            by_skill.setdefault(s["skill"], []).append(s)
        for skill, skill_sessions in sorted(by_skill.items(), key=lambda x: -len(x[1])):
            ratings = [float(s["rating"]) for s in skill_sessions if s["rating"] and s["rating"].replace(".", "", 1).isdigit()]
            avg = sum(ratings) / len(ratings) if ratings else 0
            total = sum(int(s["duration"]) for s in skill_sessions if s["duration"] and s["duration"].isdigit())
            report.append(f"- **{skill}**: {len(skill_sessions)} sessions, avg {avg:.1f}/10, {total} min total")

    if convos:
        report.append(f"\n### Conversations")
        for c in convos:
            report.append(f"- **{c['date']}** — {c['topic']}")
            for kp in c["key_points"][:2]:
                report.append(f"  - {kp}")

    if decisions:
        report.append(f"\n### Decisions Made")
        for d in decisions:
            report.append(f"- **{d['date']}** — {d['decision']}")

    report.append(f"\n### What Happened")
    if sessions and convos:
        report.append(f"Active period with {len(sessions)} practice sessions and {len(convos)} deep-dive conversations.")
    elif sessions:
        report.append(f"Focused practice period — {len(sessions)} sessions logged.")
    elif convos:
        report.append(f"Thinking/planning period — {len(convos)} conversations recorded.")
    else:
        report.append(f"Quiet period — no activity recorded.")

    return "\n".join(report)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Recap recent activity")
    parser.add_argument("days", nargs="?", type=int, default=7, help="Number of days to look back")
    args = parser.parse_args()

    recap_text = generate_recap(args.days)
    print(recap_text)

    recap_path = MEM_DIR / f"recap-{datetime.date.today().isoformat()}.md"
    recap_path.write_text(recap_text, encoding="utf-8")
    print(f"\nSaved to: {recap_path}")


if __name__ == "__main__":
    main()
