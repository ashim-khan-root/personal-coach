"""Task manager: add, list, complete tasks. Usage:
  py -3 coach/tools/task_manager.py add "<title>" [priority] [notes]
  py -3 coach/tools/task_manager.py list [--all|--pending|--done|--overdue]
  py -3 coach/tools/task_manager.py done <id>
  py -3 coach/tools/task_manager.py delete <id>
"""
import sys, datetime, re, shlex
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
fp = MEM_DIR / "tasks.md"

TEMPLATE = """# Tasks

Tasks are stored as a YAML-like list. Use `task_manager.py` to manage.
"""


def _ensure_file():
    if not fp.exists():
        fp.write_text(TEMPLATE, encoding="utf-8")


def _load_tasks():
    _ensure_file()
    text = fp.read_text(encoding="utf-8")
    tasks = []
    buffer = []
    for line in text.split("\n"):
        if line.startswith("- id:"):
            if buffer:
                tasks.append(_parse_task(buffer))
            buffer = [line]
        elif line.startswith("  ") and buffer:
            buffer.append(line)
    if buffer:
        tasks.append(_parse_task(buffer))
    return tasks


def _parse_task(lines):
    task = {}
    for line in lines:
        if m := re.match(r"- id:\s*(.+)", line):
            task["id"] = m.group(1).strip()
        elif m := re.match(r"\s+title:\s*\"(.+)\"", line):
            task["title"] = m.group(1)
        elif m := re.match(r"\s+created:\s*(.+)", line):
            task["created"] = m.group(1).strip()
        elif m := re.match(r"\s+priority:\s*(.+)", line):
            task["priority"] = m.group(1).strip()
        elif m := re.match(r"\s+status:\s*(.+)", line):
            task["status"] = m.group(1).strip()
        elif m := re.match(r"\s+due:\s*(.+)", line):
            task["due"] = m.group(1).strip()
        elif m := re.match(r"\s+notes:\s*\"(.+)\"", line):
            task["notes"] = m.group(1)
    return task


def _save_tasks(tasks):
    _ensure_file()
    lines = [TEMPLATE.rstrip()]
    for t in tasks:
        lines.append(f"- id: {t.get('id', '?')}")
        lines.append(f'  title: "{t.get("title", "")}"')
        lines.append(f"  created: {t.get('created', '')}")
        lines.append(f"  priority: {t.get('priority', 'medium')}")
        lines.append(f"  status: {t.get('status', 'pending')}")
        if t.get("due"):
            lines.append(f"  due: {t['due']}")
        if t.get("notes"):
            lines.append(f'  notes: "{t["notes"]}"')
    fp.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _next_id(tasks):
    existing_ids = [t.get("id", "") for t in tasks]
    nums = []
    for eid in existing_ids:
        m = re.search(r"task-(\d+)", eid)
        if m:
            nums.append(int(m.group(1)))
    return f"task-{(max(nums) + 1) if nums else 1}"


def cmd_add(title, priority="medium", notes=""):
    tasks = _load_tasks()
    new_id = _next_id(tasks)
    task = {
        "id": new_id,
        "title": title,
        "created": datetime.date.today().isoformat(),
        "priority": priority if priority in ("low", "medium", "high") else "medium",
        "status": "pending",
        "notes": notes,
    }
    tasks.append(task)
    _save_tasks(tasks)
    print(f"Task added: [{new_id}] {title} (priority: {task['priority']})")


def cmd_list(filter_mode="pending"):
    tasks = _load_tasks()
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
    tasks = _load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "done"
            _save_tasks(tasks)
            print(f"Task completed: [{task_id}] {t['title']}")
            return
    print(f"Task not found: {task_id}")


def cmd_delete(task_id):
    tasks = _load_tasks()
    before = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) < before:
        _save_tasks(tasks)
        print(f"Task deleted: {task_id}")
    else:
        print(f"Task not found: {task_id}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    cmd = args[0]
    rest = args[1:]

    if cmd == "add":
        if not rest:
            print("Usage: task_manager.py add '<title>' [priority] [notes]")
            sys.exit(1)
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
            sys.exit(1)
        cmd_done(rest[0])
    elif cmd == "delete":
        if not rest:
            print("Usage: task_manager.py delete <id>")
            sys.exit(1)
        cmd_delete(rest[0])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
