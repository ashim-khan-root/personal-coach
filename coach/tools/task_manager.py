"""Task manager: add, list, complete tasks. Usage:
  py -3 coach/tools/task_manager.py add "<title>" [priority] [notes]
  py -3 coach/tools/task_manager.py list [--all|--pending|--done|--overdue]
  py -3 coach/tools/task_manager.py done <id>
  py -3 coach/tools/task_manager.py delete <id>
"""
import datetime, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db import load_tasks, add_task as db_add_task, update_task_status, delete_task as db_delete_task
from db import init_db, migrate_tasks_from_md
from insight_ledger import log_insight


def _next_id(tasks):
    existing_ids = [t.get("id", "") for t in tasks]
    nums = []
    for eid in existing_ids:
        m = re.search(r"task-(\d+)", eid)
        if m:
            nums.append(int(m.group(1)))
    return f"task-{(max(nums) + 1) if nums else 1}"


def cmd_add(title, priority="medium", notes=""):
    tasks = load_tasks()
    new_id = _next_id(tasks)
    task = db_add_task(new_id, title, priority, notes)
    print(f"Task added: [{new_id}] {title} (priority: {task['priority']})")
    log_insight("task_added", {"task_id": new_id, "title": title[:60], "priority": task["priority"]})


def cmd_list(filter_mode="pending"):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    if filter_mode == "pending":
        tasks = [t for t in tasks if t.get("status") != "done"]
    elif filter_mode == "done":
        tasks = [t for t in tasks if t.get("status") == "done"]
    elif filter_mode == "overdue":
        today = datetime.date.today().isoformat()
        tasks = [t for t in tasks if t.get("due", "") and t["due"] < today and t.get("status") != "done"]

    if not tasks:
        print(f"No {filter_mode} tasks.")
        return

    for t in sorted(tasks, key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "medium"), 3)):
        due = f" (due: {t['due']})" if t.get("due") else ""
        notes = f" -- {t['notes'][:40]}" if t.get("notes") else ""
        print(f"  [{t['id']}] [{t.get('priority','?')}] {t.get('title','?')}{due}{notes}")


def cmd_done(task_id):
    update_task_status(task_id, "done")
    print(f"Task completed: {task_id}")
    log_insight("task_completed", {"task_id": task_id})


def cmd_delete(task_id):
    if db_delete_task(task_id):
        print(f"Task deleted: {task_id}")
        log_insight("task_deleted", {"task_id": task_id})
    else:
        log_insight("task_not_found", {"task_id": task_id})
        print(f"Task not found: {task_id}")


def main():
    init_db()
    migrate_tasks_from_md()

    import sys as _sys
    args = _sys.argv[1:]
    if not args:
        print(__doc__)
        _sys.exit(1)

    cmd = args[0]
    rest = args[1:]

    if cmd == "add":
        if not rest:
            print("Usage: task_manager.py add '<title>' [priority] [notes]")
            _sys.exit(1)
        title = rest[0]
        priority = rest[1] if len(rest) > 1 else "medium"
        notes = rest[2] if len(rest) > 2 else ""
        cmd_add(title, priority, notes)
    elif cmd == "list":
        mode = rest[0] if rest else "pending"
        mode = mode.lstrip("-")
        cmd_list(mode)
    elif cmd == "done":
        if not rest:
            print("Usage: task_manager.py done <id>")
            _sys.exit(1)
        cmd_done(rest[0])
    elif cmd == "delete":
        if not rest:
            print("Usage: task_manager.py delete <id>")
            _sys.exit(1)
        cmd_delete(rest[0])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
