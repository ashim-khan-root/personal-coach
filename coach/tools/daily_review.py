"""Daily review — end-of-day reflection, task migration, summary generation.
Usage:
  python tools/daily_review.py                    # Run review on today's note
  python tools/daily_review.py "extra notes..."   # Add notes then run review
"""
import sys, datetime, re
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
DAILY_DIR = MEM_DIR / "daily"
INBOX_DIR = MEM_DIR / "inbox" / "captures"
INBOX_ARCHIVE = MEM_DIR / "inbox" / "processed"


def today_str():
    return datetime.date.today().isoformat()


def tomorrow_str():
    return (datetime.date.today() + datetime.timedelta(days=1)).isoformat()


def daily_path(date_str=None):
    return DAILY_DIR / f"{date_str or today_str()}.md"


def parse_tasks(content):
    """Extract tasks and their completion status."""
    tasks = []
    for line in content.splitlines():
        m = re.match(r'^(\s*)- \[([ x>])\]\s*(.*)', line)
        if m:
            indent, status, text = m.groups()
            tasks.append({
                "indent": indent,
                "status": status,
                "text": text.strip(),
                "line": line
            })
    return tasks


def parse_sessions(content):
    """Extract session log entries."""
    sessions = []
    in_table = False
    for line in content.splitlines():
        if line.strip().startswith("| Skill"):
            in_table = True
            continue
        if in_table:
            if line.strip().startswith("|---"):
                continue
            if line.strip().startswith("|"):
                cells = [c.strip() for c in line.strip().split("|")[1:-1]]
                if len(cells) >= 2 and cells[0]:
                    sessions.append(cells)
            else:
                in_table = False
    return sessions


def scan_inbox():
    """List unprocessed inbox items."""
    if not INBOX_DIR.exists():
        return []
    return sorted(INBOX_DIR.glob("*"))


def archive_old_dails():
    """Move daily notes older than 7 days to processed."""
    if not DAILY_DIR.exists():
        return 0
    cutoff = datetime.date.today() - datetime.timedelta(days=7)
    moved = 0
    for fp in DAILY_DIR.glob("*.md"):
        try:
            d = datetime.date.fromisoformat(fp.stem)
            if d < cutoff:
                INBOX_ARCHIVE.mkdir(parents=True, exist_ok=True)
                dest = INBOX_ARCHIVE / fp.name
                fp.rename(dest)
                moved += 1
        except ValueError:
            pass
    return moved


def run_review(extra_notes=""):
    today = today_str()
    path = daily_path()
    tomorrow = tomorrow_str()
    report = []

    if not path.exists():
        print(f"No daily note for {today}. Nothing to review.")
        return

    content = path.read_text(encoding="utf-8")

    if extra_notes:
        if "## Notes\n" in content:
            content = content.replace("## Notes\n", f"## Notes\n- {extra_notes}\n")
        report.append(f"Added notes: {extra_notes}")

    tasks = parse_tasks(content)
    completed = [t for t in tasks if t["status"] == "x"]
    incomplete = [t for t in tasks if t["status"] == " "]
    migrated = [t for t in tasks if t["status"] == ">"]

    if completed:
        report.append(f"\nCompleted ({len(completed)}):")
        for t in completed:
            report.append(f"  [x] {t['text']}")

    if incomplete:
        report.append(f"\nIncomplete ({len(incomplete)}):")
        for t in incomplete:
            report.append(f"  [ ] {t['text']}")

    if incomplete:
        tomorrow_path = daily_path(tomorrow)
        if tomorrow_path.exists():
            t_content = tomorrow_path.read_text(encoding="utf-8")
        else:
            t_content = f"---\ndate: {tomorrow}\n---\n\n# {tomorrow}\n\n## Tasks\n\n### Migrated from {today}\n\n"

        migration_block = ""
        for t in incomplete:
            migration_block += f"- [ ] {t['text']}\n"
            content = content.replace(t["line"], t["line"].replace("- [ ]", "- [>]"))

        if "### Migrated from" in t_content:
            t_content = t_content.replace(
                f"### Migrated from {today}\n",
                f"### Migrated from {today}\n{migration_block}"
            )
        else:
            t_content += f"\n### Migrated from {today}\n{migration_block}"

        tomorrow_path.write_text(t_content, encoding="utf-8")
        report.append(f"\nMigrated {len(incomplete)} tasks to {tomorrow}")

    sessions = parse_sessions(content)
    if sessions:
        report.append(f"\nSessions today: {len(sessions)}")
        for s in sessions:
            report.append(f"  {s[0]} — {s[1]} min — {s[2]}/10")

    inbox_items = scan_inbox()
    if inbox_items:
        report.append(f"\nInbox: {len(inbox_items)} items to process")
        for item in inbox_items[:5]:
            report.append(f"  - {item.name}")

    summary_parts = []
    if completed:
        summary_parts.append(f"completed {len(completed)} tasks")
    if sessions:
        summary_parts.append(f"logged {len(sessions)} sessions")
    if incomplete:
        summary_parts.append(f"migrated {len(incomplete)} tasks to tomorrow")

    summary = f"Today I {', '.join(summary_parts)}." if summary_parts else "Light day — no tasks or sessions logged."
    report.append(f"\n--- Daily Summary ---\n{summary}")

    if "## Daily Summary\n" in content:
        content = content.replace(
            "## Daily Summary\n",
            f"## Daily Summary\n{summary}\n"
        )

    moved = archive_old_dails()
    if moved:
        report.append(f"\nArchived {moved} old daily notes")

    path.write_text(content, encoding="utf-8")

    print(f"=== Daily Review: {today} ===\n")
    for line in report:
        print(line)
    print(f"\nFile updated: {path}")


def main():
    extra = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    run_review(extra)


if __name__ == "__main__":
    main()
