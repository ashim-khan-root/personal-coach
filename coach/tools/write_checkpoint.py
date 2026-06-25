"""Save a coaching checkpoint. Usage:
  python write_checkpoint.py "<phase>" "<current_topic>" "<next_task>" [notes]
"""
import sys, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db import init_db, set_checkpoint

def main():
    if len(sys.argv) < 4:
        print("Usage: python write_checkpoint.py '<phase>' '<current_topic>' '<next_task>' [notes]")
        sys.exit(1)
    phase = sys.argv[1]
    topic = sys.argv[2]
    next_task = sys.argv[3]
    notes = sys.argv[4] if len(sys.argv) > 4 else ""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    init_db()
    set_checkpoint("last_updated", now)
    set_checkpoint("phase", phase)
    set_checkpoint("current_topic", topic)
    set_checkpoint("next_task", next_task)
    set_checkpoint("notes", notes)
    print(f"Checkpoint saved: {topic} (phase: {phase})")

if __name__ == "__main__":
    main()
