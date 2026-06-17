"""Save a context snapshot to prevent data loss when context window fills.
Usage:
  py -3 coach/tools/save_context_snapshot.py "<task>" "<files>" "<decisions>" "<next_goal>"

Example:
  py -3 coach/tools/save_context_snapshot.py "Fixing timestamp converter bug" "timestamp-converter.js, main.css" "Added widget HTML, fixed CSS" "Build and deploy"
"""
import sys, datetime, json
from pathlib import Path

SNAP_DIR = Path(__file__).resolve().parent.parent / "memory" / "snapshots"

def main():
    if len(sys.argv) < 2:
        print("Usage: py -3 coach/tools/save_context_snapshot.py '<task>' '<files>' '<decisions>' '<next_goal>'")
        sys.exit(1)

    task = sys.argv[1] if len(sys.argv) > 1 else ""
    files = sys.argv[2] if len(sys.argv) > 2 else ""
    decisions = sys.argv[3] if len(sys.argv) > 3 else ""
    next_goal = sys.argv[4] if len(sys.argv) > 4 else ""

    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc)
    ts = now.strftime("%Y%m%d-%H%M%S")
    fp = SNAP_DIR / f"snapshot-{ts}.md"

    content = (
        f"---\n"
        f"created: {now.isoformat()}\n"
        f"task: \"{task}\"\n"
        f"files: \"{files}\"\n"
        f"decisions: \"{decisions}\"\n"
        f"next_goal: \"{next_goal}\"\n"
        f"---\n"
    )
    fp.write_text(content, encoding="utf-8")
    print(f"Snapshot saved: {fp.name}")

    # Clean old snapshots (keep last 20)
    snaps = sorted(SNAP_DIR.glob("snapshot-*.md"), reverse=True)
    for old in snaps[20:]:
        old.unlink()

if __name__ == "__main__":
    main()
