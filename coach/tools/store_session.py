"""Store a practice session. Usage:
  python store_session.py <skill> <duration_min> <rating> [notes] [--no-hooks] [--decision "what you decided"]
"""
import sys, uuid, datetime, re
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
SESS_DIR = MEM_DIR / "sessions"
SESS_DIR.mkdir(parents=True, exist_ok=True)

def extract_decisions_from_notes(notes):
    """Auto-detect decisions in session notes."""
    decisions = []
    for line in notes.split("\n"):
        low = line.lower().strip()
        if any(kw in low for kw in ["decided to", "i'll ", "i will ", "going to", "chose to", "plan is to"]):
            decisions.append(line.strip().lstrip("- "))
    return decisions

def log_decision_to_file(skill, decisions):
    """Append decisions to decisions.md."""
    fp = MEM_DIR / "decisions.md"
    today = datetime.date.today().isoformat()
    entry = f"\n## {today} — {skill} (session)\n"
    for d in decisions:
        entry += f"- {d}\n"
    if fp.exists():
        content = fp.read_text(encoding="utf-8")
        content += entry
        fp.write_text(content, encoding="utf-8")
    else:
        fp.write_text(f"# Decisions Log\n{entry}", encoding="utf-8")

def main():
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
    duration_min = args[1]
    rating = args[2]
    notes = args[3] if len(args) > 3 else ""
    sid = str(uuid.uuid4())
    now = datetime.datetime.now(datetime.timezone.utc)
    timestamp = now.isoformat()
    filename = now.strftime("session-%Y%m%d-%H%M%S") + ".md"

    auto_decisions = extract_decisions_from_notes(notes) if notes else []
    all_decisions = explicit_decisions + auto_decisions
    decision_block = ""
    if all_decisions:
        decision_block = "decisions:\n" + "".join(f'  - "{d}"\n' for d in all_decisions)

    content = (
        f"---\n"
        f"id: {sid}\n"
        f"date: {timestamp}\n"
        f"skill: {skill}\n"
        f"duration_min: {duration_min}\n"
        f"rating: {rating}\n"
        f"notes: |\n"
        f"  {notes}\n"
        f"{decision_block}"
        f"tags: []\n"
        f"---\n"
    )
    fpath = SESS_DIR / filename
    fpath.write_text(content, encoding="utf-8")
    print(f"Session stored: {fpath.name}")
    print(f"skill: {skill} | duration: {duration_min}min | rating: {rating}/10")

    if all_decisions:
        log_decision_to_file(skill, all_decisions)
        print(f"Decisions logged: {len(all_decisions)}")

    meta_path = MEM_DIR / "meta.md"
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
            post_session(skill, duration_min, rating, notes)
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
