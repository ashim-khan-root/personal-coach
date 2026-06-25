"""Store a practice session. Usage:
  python store_session.py <skill> <duration_min> <rating> [notes] [--no-hooks] [--decision "what you decided"]
"""
import sys, uuid, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db import init_db, store_session as db_store_session
from insight_ledger import log_insight


def extract_decisions_from_notes(notes):
    decisions = []
    for line in notes.split("\n"):
        low = line.lower().strip()
        if any(kw in low for kw in ["decided to", "i'll ", "i will ", "going to", "chose to", "plan is to"]):
            decisions.append(line.strip().lstrip("- "))
    return decisions


def main():
    init_db()

    no_hooks = "--no-hooks" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--no-hooks"]

    explicit_decisions = []
    if "--decision" in sys.argv:
        d_idx = args.index("--decision")
        if d_idx + 1 < len(args):
            explicit_decisions = [args[d_idx + 1]]
            args = args[:d_idx] + args[d_idx + 2:]

    if len(args) < 3:
        print("Usage: python store_session.py <skill> <duration_min> <rating> [notes] [--no-hooks] [--decision \"what\"]")
        sys.exit(1)
    skill = args[0]
    duration_min = int(args[1])
    rating = int(args[2])
    notes = args[3] if len(args) > 3 else ""

    now = datetime.datetime.now(datetime.timezone.utc)
    session_id = str(uuid.uuid4())
    auto_decisions = extract_decisions_from_notes(notes) if notes else []
    all_decisions = explicit_decisions + auto_decisions

    session_data = {
        "id": session_id,
        "date": now.isoformat(),
        "skill": skill,
        "duration_min": duration_min,
        "rating": rating,
        "notes": notes,
        "decisions": all_decisions,
    }
    db_store_session(session_data)
    print(f"Session stored: {skill} | {duration_min}min | {rating}/10")

    if all_decisions:
        log_insight("session_decisions", {"count": len(all_decisions), "skill": skill})

    meta_path = Path(__file__).resolve().parent.parent / "memory" / "meta.md"
    if meta_path.exists():
        meta = meta_path.read_text(encoding="utf-8")
        lines = meta.splitlines()
        new_lines = []
        updated = False
        for line in lines:
            if line.startswith("updated_at:"):
                new_lines.append(f"updated_at: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
                updated = True
            else:
                new_lines.append(line)
        if not updated:
            new_lines.append(f"updated_at: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
        meta_path.write_text("\n".join(new_lines), encoding="utf-8")

    if not no_hooks:
        try:
            import sys as _sys
            _sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
            from tools.session_hooks import post_session
            post_session(skill, str(duration_min), str(rating), notes)
        except Exception as e:
            print(f"[hooks] post-session analysis skipped: {e}")

    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from tools.backup_memory import git_commit_and_push
        git_commit_and_push(quiet=True)
        if not no_hooks:
            print("[backup] Memory backed up to git")
    except Exception:
        pass


if __name__ == "__main__":
    main()
