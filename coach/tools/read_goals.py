"""Print current goals."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db import init_db, load_goals

def main():
    init_db()
    goals = load_goals()
    if not goals:
        print("No goals found.")
        return
    for g in goals:
        print(f"- id: {g['id']}")
        print(f'  title: "{g["title"]}"')
        print(f"  status: {g['status']}")
        print(f"  created: {g['created']}")

if __name__ == "__main__":
    main()
