"""Print current habits."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db import init_db, load_habits

def main():
    init_db()
    habits = load_habits()
    if not habits:
        print("No habits found.")
        return
    for h in habits:
        print(f"- id: {h['id']}")
        print(f'  title: "{h["title"]}"')
        print(f"  status: {h['status']}")
        print(f"  streak: {h['streak']}")
        print(f"  created: {h['created']}")

if __name__ == "__main__":
    main()
