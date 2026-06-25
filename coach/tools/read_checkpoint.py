"""Print the current coaching checkpoint for AI to read."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db import init_db, get_checkpoint

def main():
    init_db()
    cp = get_checkpoint()
    if not cp:
        print("No checkpoint found. Start fresh.")
        return
    print("---")
    for k, v in cp.items():
        print(f'{k}: "{v}"')
    print("---")

if __name__ == "__main__":
    main()
