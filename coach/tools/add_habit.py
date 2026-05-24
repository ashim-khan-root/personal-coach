"""Add a new habit. Usage:
  python add_habit.py "<title>" "<cue>" "<action>" [reward]
"""
import sys, uuid
from pathlib import Path
MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
fp = MEM_DIR / "habits.md"

def main():
    if len(sys.argv) < 4:
        print("Usage: python add_habit.py '<title>' '<cue>' '<action>' [reward]")
        sys.exit(1)
    title = sys.argv[1]
    cue = sys.argv[2]
    action = sys.argv[3]
    reward = sys.argv[4] if len(sys.argv) > 4 else ""
    existing = fp.read_text(encoding="utf-8") if fp.exists() else ""
    import re
    existing_ids = re.findall(r"id: (habit-\d+)", existing)
    next_id = 1
    if existing_ids:
        next_id = max(int(e.split("-")[1]) for e in existing_ids) + 1
    new_entry = (
        f"\n- id: habit-{next_id}\n"
        f'  title: "{title}"\n'
        f'  cue: "{cue}"\n'
        f'  action: "{action}"\n'
        f'  reward: "{reward}"\n'
    )
    with open(fp, "a", encoding="utf-8") as f:
        f.write(new_entry)
    print(f"Habit added: {title}")

if __name__ == "__main__":
    main()
