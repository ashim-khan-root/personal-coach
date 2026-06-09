"""Weekly synthesis — review past 7 days for patterns, wins, stalls, neglect.
Usage:
  python tools/weekly_synthesis.py
"""
import sys, datetime, re
from pathlib import Path
from collections import Counter

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
DAILY_DIR = MEM_DIR / "daily"
SESSIONS_DIR = MEM_DIR / "sessions"


def last_7_days():
    today = datetime.date.today()
    return [(today - datetime.timedelta(days=i)).isoformat() for i in range(7)]


def load_daily_notes(days):
    notes = {}
    for d in days:
        path = DAILY_DIR / f"{d}.md"
        if path.exists():
            notes[d] = path.read_text(encoding="utf-8")
    return notes


def load_sessions(days):
    sessions = []
    if not SESSIONS_DIR.exists():
        return sessions
    for fp in sorted(SESSIONS_DIR.glob("session-*.md"), reverse=True):
        text = fp.read_text(encoding="utf-8")
        date = skill = rating = duration = notes = ""
        for line in text.splitlines():
            if line.startswith("date:"):
                date = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("skill:"):
                skill = line.split(":", 1)[1].strip()
            elif line.startswith("rating:"):
                rating = line.split(":", 1)[1].strip()
            elif line.startswith("duration_min:"):
                duration = line.split(":", 1)[1].strip()
            elif line.startswith("notes:"):
                notes = line.split(":", 1)[1].strip().strip('"')
        if date in days and skill:
            sessions.append({
                "date": date, "skill": skill,
                "rating": rating, "duration": duration, "notes": notes
            })
    return sessions


def analyze(daily_notes, sessions):
    report = []
    days_with_notes = list(daily_notes.keys())

    total_tasks_done = 0
    total_tasks_migrated = 0
    all_skills = Counter()

    for date, content in daily_notes.items():
        for line in content.splitlines():
            if re.match(r'^\s*- \[x\]', line):
                total_tasks_done += 1
            elif re.match(r'^\s*- \[>\]', line):
                total_tasks_migrated += 1

    for s in sessions:
        all_skills[s["skill"]] += 1

    report.append(f"## Weekly Synthesis")
    report.append(f"**Period:** {(datetime.date.today() - datetime.timedelta(days=6)).isoformat()} to {datetime.date.today().isoformat()}")
    report.append(f"**Days with notes:** {len(days_with_notes)}/7")
    report.append(f"**Sessions logged:** {len(sessions)}")

    report.append(f"\n### Wins")
    report.append(f"- Tasks completed: {total_tasks_done}")
    if sessions:
        avg_rating = sum(float(s["rating"]) for s in sessions if s["rating"]) / len(sessions)
        total_mins = sum(int(s["duration"]) for s in sessions if s["duration"].isdigit())
        report.append(f"- Average session rating: {avg_rating:.1f}/10")
        report.append(f"- Total practice time: {total_mins} min")

    report.append(f"\n### Skill Breakdown")
    if all_skills:
        for skill, count in all_skills.most_common():
            report.append(f"- {skill}: {count} sessions")
    else:
        report.append("- No sessions logged this week")

    report.append(f"\n### Stalls")
    if total_tasks_migrated > 0:
        report.append(f"- {total_tasks_migrated} tasks migrated (incomplete)")
    empty_days = [d for d in last_7_days() if d not in daily_notes]
    if empty_days:
        report.append(f"- No notes on {len(empty_days)} days: {', '.join(empty_days[:3])}")

    report.append(f"\n### Recommendations")
    if not sessions:
        report.append("- Start logging sessions to track progress")
    if len(days_with_notes) < 3:
        report.append("- Try to use daily notes more consistently")
    if total_tasks_migrated > total_tasks_done:
        report.append("- Too many tasks migrating — break them into smaller pieces")

    return "\n".join(report)


def main():
    days = last_7_days()
    daily_notes = load_daily_notes(days)
    sessions = load_sessions(days)

    if not daily_notes and not sessions:
        print("No data found for the past 7 days.")
        print("Start using daily notes and logging sessions to get weekly insights.")
        return

    report = analyze(daily_notes, sessions)
    print(report)

    report_path = MEM_DIR / f"weekly-{datetime.date.today().isoformat()}.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nSaved to: {report_path}")


if __name__ == "__main__":
    main()
