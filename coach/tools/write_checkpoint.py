"""Save a coaching checkpoint. Usage:
  python write_checkpoint.py "<phase>" "<current_topic>" "<next_task>" [notes]
"""
import sys, datetime
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
fp = MEM_DIR / "checkpoint.md"

def main():
    if len(sys.argv) < 4:
        print("Usage: python write_checkpoint.py '<phase>' '<current_topic>' '<next_task>' [notes]")
        sys.exit(1)
    phase = sys.argv[1]
    topic = sys.argv[2]
    next_task = sys.argv[3]
    notes = sys.argv[4] if len(sys.argv) > 4 else ""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    content = (
        f"---\n"
        f"last_updated: {now}\n"
        f"phase: \"{phase}\"\n"
        f"current_topic: \"{topic}\"\n"
        f"next_task: \"{next_task}\"\n"
        f"notes: \"{notes}\"\n"
        f"---\n"
    )
    fp.write_text(content, encoding="utf-8")
    print(f"Checkpoint saved: {topic} (phase: {phase})")

if __name__ == "__main__":
    main()
