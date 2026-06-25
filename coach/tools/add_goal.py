"""Add a new goal. Usage:
  python add_goal.py "<title>" <target_date> <metric> [notes]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db import init_db, add_goal, load_goals

def _next_goal_id():
    goals = load_goals()
    nums = [int(g["id"].split("-")[1]) for g in goals if g["id"].startswith("goal-")]
    return f"goal-{(max(nums) + 1) if nums else 1}"

def main():
    if len(sys.argv) < 4:
        print("Usage: python add_goal.py '<title>' <target_date> <metric> [notes]")
        sys.exit(1)
    title = sys.argv[1]
    init_db()
    add_goal(_next_goal_id(), title)
    print(f"Goal added: {title}")

if __name__ == "__main__":
    main()
