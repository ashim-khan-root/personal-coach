"""Print current habits."""
from pathlib import Path
MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
fp = MEM_DIR / "habits.md"
if fp.exists():
    print(fp.read_text(encoding="utf-8"))
else:
    print("No habits file found.")
