"""Print the current coaching checkpoint for AI to read."""
from pathlib import Path
MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
fp = MEM_DIR / "checkpoint.md"
if fp.exists():
    print(fp.read_text(encoding="utf-8"))
else:
    print("No checkpoint found. Start fresh.")
