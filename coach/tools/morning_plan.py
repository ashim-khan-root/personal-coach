"""Morning plan — create today's daily note from brain dump.
Usage:
  python tools/morning_plan.py                  # Show today's note or create from template
  python tools/morning_plan.py "brain dump..."  # Create/update today's note with tasks
"""
import sys, datetime, re
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
TEMPLATE = MEM_DIR / "templates" / "daily-note.md"
INBOX_DIR = MEM_DIR / "inbox" / "captures"
DAILY_DIR = MEM_DIR / "daily"


def today_str():
    return datetime.date.today().isoformat()


def daily_path(date_str=None):
    d = date_str or today_str()
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    return DAILY_DIR / f"{d}.md"


def load_context():
    """Load goals, habits, checkpoint for context."""
    parts = []
    for name, marker in [("goals.md", "- title:"), ("habits.md", "- title:")]:
        fp = MEM_DIR / name
        if fp.exists():
            lines = [l.strip() for l in fp.read_text(encoding="utf-8").splitlines()
                     if l.strip().startswith(marker)]
            if lines:
                items = [l.replace(marker, "").strip().strip('"') for l in lines[:5]]
                parts.append(f"{name.replace('.md','')}: {', '.join(items)}")

    cp = MEM_DIR / "checkpoint.md"
    if cp.exists():
        for line in cp.read_text(encoding="utf-8").splitlines():
            if line.startswith("phase:"):
                parts.append(line.replace("phase:", "Checkpoint:").strip())

    last_sesh = sorted((MEM_DIR / "sessions").glob("session-*.md"), reverse=True)
    if last_sesh:
        text = last_sesh[0].read_text(encoding="utf-8")
        skill = rating = ""
        for line in text.splitlines():
            if line.startswith("skill:"):
                skill = line.split(":", 1)[1].strip()
            elif line.startswith("rating:"):
                rating = line.split(":", 1)[1].strip()
        if skill:
            parts.append(f"Last session: {skill} ({rating}/10)")
    return parts


def show_today():
    path = daily_path()
    if path.exists():
        print(f"=== Today's Note ({today_str()}) ===")
        print(path.read_text(encoding="utf-8"))
    else:
        print(f"No daily note for {today_str()} yet.")
        print("Run: python tools/morning_plan.py \"<brain dump>\"")
    ctx = load_context()
    if ctx:
        print("\n--- Context ---")
        for c in ctx:
            print(f"  {c}")


def create_or_update(brain_dump):
    path = daily_path()
    ctx = load_context()

    if path.exists():
        content = path.read_text(encoding="utf-8")
    else:
        if TEMPLATE.exists():
            content = TEMPLATE.read_text(encoding="utf-8")
            content = content.replace("{{date}}", today_str())
        else:
            content = f"---\ndate: {today_str()}\n---\n\n# {today_str()}\n\n## Brain Dump\n\n## Tasks\n\n### Active Projects\n- [ ]\n\n### Areas\n- [ ]\n\n### Quick Wins\n- [ ]\n\n## Notes\n\n## Session Log\n| Skill | Duration | Rating | Notes |\n|-------|----------|--------|-------|\n\n## Daily Summary\n"

    lines = brain_dump.strip().split("\n")
    tasks = []
    notes = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        low = stripped.lower()
        is_task = any(kw in low for kw in [
            "todo", "task", "do ", "finish", "complete", "send", "email",
            "call", "meeting", "create", "build", "fix", "update", "write",
            "review", "check", "buy", "set up", "setup", "install", "configure"
        ])
        if is_task:
            tasks.append(stripped)
        else:
            notes.append(stripped)

    if tasks:
        task_block = "\n".join(f"- [ ] {t}" for t in tasks)
        if "### Active Projects" in content:
            content = content.replace(
                "### Active Projects\n- [ ]",
                f"### Active Projects\n{task_block}"
            )
        elif "## Tasks" in content:
            content = content.replace("## Tasks\n- [ ]", f"## Tasks\n{task_block}")

    if notes:
        note_block = "\n".join(f"- {n}" for n in notes)
        if "## Notes\n" in content:
            content = content.replace("## Notes\n", f"## Notes\n{note_block}\n")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    print(f"=== Daily Note Updated: {today_str()} ===")
    if tasks:
        print(f"\nTasks added ({len(tasks)}):")
        for t in tasks:
            print(f"  - [ ] {t}")
    if notes:
        print(f"\nNotes added ({len(notes)}):")
        for n in notes:
            print(f"  - {n}")
    print(f"\nFile: {path}")
    if ctx:
        print("\nContext:")
        for c in ctx:
            print(f"  {c}")


def main():
    if len(sys.argv) < 2:
        show_today()
    else:
        create_or_update(" ".join(sys.argv[1:]))


if __name__ == "__main__":
    main()
