"""Export saved sessions as Anki-importable JSON.
Usage: python export_anki.py [out_file]
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from db import init_db, get_db

def main():
    out_file = sys.argv[1] if len(sys.argv) > 1 else "anki_cards.json"
    init_db()
    rows = get_db().execute("SELECT skill, notes FROM sessions WHERE notes != '' AND notes != 'TODO' ORDER BY date DESC").fetchall()
    cards = []
    for r in rows:
        cards.append({
            "deck": "Coach::Sessions",
            "front": f"What did you learn from your {r['skill']} session?",
            "back": r["notes"],
            "tags": [r["skill"]]
        })
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(cards)} Anki cards to {out_file}")
    if len(cards) == 0:
        print("No sessions with notes found. Add notes to sessions to generate cards.")

if __name__ == "__main__":
    main()
