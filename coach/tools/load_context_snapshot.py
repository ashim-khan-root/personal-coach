"""Load the latest context snapshot.
Usage:
  py -3 coach/tools/load_context_snapshot.py

Returns the most recent snapshot content or 'No snapshots found'.
"""
import sys
from pathlib import Path

SNAP_DIR = Path(__file__).resolve().parent.parent / "memory" / "snapshots"

def main():
    if not SNAP_DIR.exists():
        print("No snapshots found.")
        sys.exit(0)

    snaps = sorted(SNAP_DIR.glob("snapshot-*.md"), reverse=True)
    if not snaps:
        print("No snapshots found.")
        sys.exit(0)

    content = snaps[0].read_text(encoding="utf-8")
    print(content.strip())

if __name__ == "__main__":
    main()
