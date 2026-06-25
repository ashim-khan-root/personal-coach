"""Add a new habit. Usage:
  python add_habit.py "<title>" "<cue>" "<action>" [reward]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db import init_db, add_habit, load_habits

def _next_habit_id():
    habits = load_habits()
    nums = [int(h["id"].split("-")[1]) for h in habits if h["id"].startswith("habit-")]
    return f"habit-{(max(nums) + 1) if nums else 1}"

def main():
    if len(sys.argv) < 4:
        print("Usage: python add_habit.py '<title>' '<cue>' '<action>' [reward]")
        sys.exit(1)
    title = sys.argv[1]
    init_db()
    add_habit(_next_habit_id(), title)
    print(f"Habit added: {title}")

if __name__ == "__main__":
    main()
