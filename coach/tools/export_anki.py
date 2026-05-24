"""Export saved sessions as Anki-importable JSON.
Usage: python export_anki.py [out_file]
"""
import json, sys
from pathlib import Path
MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
SESS_DIR = MEM_DIR / "sessions"

def main():
    out_file = sys.argv[1] if len(sys.argv) > 1 else "anki_cards.json"
    cards = []
    for sf in sorted(SESS_DIR.glob("session-*.md"), key=lambda p: p.stem, reverse=True):
        txt = sf.read_text(encoding="utf-8")
        import re
        m = re.search(r"skill: (.+)", txt)
        n = re.search(r"notes: \|\s*\n\s+(.+)", txt)
        skill = m.group(1).strip() if m else "unknown"
        notes = n.group(1).strip() if n else ""
        if notes and notes != "TODO":
            cards.append({
                "deck": "Coach::Sessions",
                "front": f"What did you learn from your {skill} session?",
                "back": notes,
                "tags": [skill]
            })
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(cards)} Anki cards to {out_file}")
    if len(cards) == 0:
        print("No sessions with notes found. Add notes to sessions to generate cards.")

if __name__ == "__main__":
    main()
