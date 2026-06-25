"""Inbox processor — organize loose captures into the right place.
Usage:
  python tools/inbox_processor.py          # Show inbox items
  python tools/inbox_processor.py --auto   # Auto-categorize and move items
"""
import sys, datetime, re, shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db import init_db, add_goal, add_habit, load_goals, load_habits

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
INBOX_DIR = MEM_DIR / "inbox" / "captures"
INBOX_ARCHIVE = MEM_DIR / "inbox" / "processed"
SESSIONS_DIR = MEM_DIR / "sessions"


def categorize_item(filepath):
    """Heuristic categorization based on content keywords."""
    text = filepath.read_text(encoding="utf-8").lower() if filepath.suffix == ".md" else filepath.name.lower()

    task_kw = ["todo", "task", "do ", "finish", "complete", "send", "email",
               "call", "meeting", "create", "build", "fix", "update", "write",
               "review", "check", "buy", "set up", "setup", "install"]
    session_kw = ["practice", "studied", "learned", "session", "trained", "worked on"]
    habit_kw = ["habit", "daily", "every day", "routine", "morning", "evening"]
    goal_kw = ["goal", "target", "deadline", "objective", "milestone"]

    if any(kw in text for kw in session_kw):
        return "session"
    if any(kw in text for kw in task_kw):
        return "task"
    if any(kw in text for kw in habit_kw):
        return "habit"
    if any(kw in text for kw in goal_kw):
        return "goal"
    return "note"


def show_inbox():
    if not INBOX_DIR.exists():
        print("Inbox is empty (directory doesn't exist yet).")
        return

    items = sorted(INBOX_DIR.glob("*"))
    if not items:
        print("Inbox is empty!")
        return

    print(f"=== Inbox: {len(items)} items ===\n")
    for item in items:
        cat = categorize_item(item)
        print(f"  [{cat:8s}] {item.name}")
        if item.suffix == ".md":
            text = item.read_text(encoding="utf-8")
            preview = text[:100].replace("\n", " ").strip()
            if preview:
                print(f"            {preview}...")
    print(f"\nRun: python tools/inbox_processor.py --auto  to organize")


def auto_process():
    if not INBOX_DIR.exists():
        print("Inbox is empty.")
        return

    items = sorted(INBOX_DIR.glob("*"))
    if not items:
        print("Inbox is empty!")
        return

    INBOX_ARCHIVE.mkdir(parents=True, exist_ok=True)
    processed = 0

    for item in items:
        cat = categorize_item(item)
        content = item.read_text(encoding="utf-8") if item.suffix == ".md" else ""

        if cat == "session":
            _create_session_from_capture(item, content)
        elif cat == "task":
            _add_to_daily_task(item, content)
        elif cat == "habit":
            _add_to_habits(item, content)
        elif cat == "goal":
            _add_to_goals(item, content)

        dest = INBOX_ARCHIVE / f"{datetime.date.today().isoformat()}-{item.name}"
        shutil.move(str(item), str(dest))
        processed += 1
        print(f"  [{cat:8s}] {item.name} -> organized")

    print(f"\nProcessed {processed} items from inbox")


def _create_session_from_capture(filepath, content):
    """Create a session entry from inbox capture."""
    today = datetime.date.today().strftime("%Y%m%d")
    now = datetime.datetime.now().strftime("%H%M%S")
    session_path = SESSIONS_DIR / f"session-{today}-{now}.md"

    title = content.split("\n")[0].strip() if content else filepath.stem
    session_path.write_text(
        f'---\nid: "session-{today}-{now}"\n'
        f'date: "{datetime.date.today().isoformat()}"\n'
        f'skill: "{title}"\n'
        f'duration_min: 0\n'
        f'rating: 0\n'
        f'notes: "Imported from inbox"\n'
        f'tags: [inbox-import]\n---\n\n'
        f'{content}',
        encoding="utf-8"
    )


def _add_to_daily_task(filepath, content):
    """Add item to today's daily note as a task."""
    daily = MEM_DIR / "daily" / f"{datetime.date.today().isoformat()}.md"
    if daily.exists():
        text = daily.read_text(encoding="utf-8")
        title = content.split("\n")[0].strip() if content else filepath.stem
        if "## Tasks" in text:
            text = text.replace("## Tasks\n", f"## Tasks\n- [ ] {title}\n")
            daily.write_text(text, encoding="utf-8")


def _add_to_habits(filepath, content):
    """Add item to habits via DB."""
    init_db()
    existing = load_habits()
    nums = [int(h["id"].split("-")[1]) for h in existing if h["id"].startswith("habit-")]
    next_id = f"habit-{(max(nums) + 1) if nums else 1}"
    title = content.split("\n")[0].strip() if content else filepath.stem
    add_habit(next_id, title)


def _add_to_goals(filepath, content):
    """Add item to goals via DB."""
    init_db()
    existing = load_goals()
    nums = [int(g["id"].split("-")[1]) for g in existing if g["id"].startswith("goal-")]
    next_id = f"goal-{(max(nums) + 1) if nums else 1}"
    title = content.split("\n")[0].strip() if content else filepath.stem
    add_goal(next_id, title)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        auto_process()
    else:
        show_inbox()


if __name__ == "__main__":
    main()
