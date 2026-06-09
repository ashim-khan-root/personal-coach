"""Add a new goal. Usage:
  python add_goal.py "<title>" <target_date> <metric> [notes]
"""
import sys, datetime
from pathlib import Path
MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
fp = MEM_DIR / "goals.md"

def main():
    if len(sys.argv) < 4:
        print("Usage: python add_goal.py '<title>' <target_date> <metric> [notes]")
        sys.exit(1)
    title = sys.argv[1]
    target_date = sys.argv[2]
    metric = sys.argv[3]
    notes = sys.argv[4] if len(sys.argv) > 4 else ""
    existing = fp.read_text(encoding="utf-8") if fp.exists() else ""
    import re, uuid
    existing_ids = re.findall(r"id: (goal-\d+)", existing)
    next_id = 1
    if existing_ids:
        next_id = max(int(e.split("-")[1]) for e in existing_ids) + 1
    new_entry = (
        f"\n- id: goal-{next_id}\n"
        f'  title: "{title}"\n'
        f"  created: {datetime.date.today().isoformat()}\n"
        f"  target_date: {target_date}\n"
        f'  metric: "{metric}"\n'
        f'  notes: "{notes}"\n'
    )
    with open(fp, "a", encoding="utf-8") as f:
        f.write(new_entry)
    print(f"Goal added: {title}")

if __name__ == "__main__":
    main()
