import json

def export_cards(cards, out_file="anki_cards.json"):
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    print("Exported", len(cards), "cards to", out_file)

def export_cards_to_apkg(cards, out_file="anki_cards.apkg"):
    try:
        from genanki import Deck, Note, Model, Package
    except ImportError:
        print("Install genanki: pip install genanki")
        return
    model = Model(
        1607392319,
        "Coach Model",
        fields=[{"name": "Front"}, {"name": "Back"}],
        templates=[{
            "name": "Card 1",
            "qfmt": "{{Front}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Back}}',
        }],
    )
    deck = Deck(2059400110, "Coach::Arabic")
    for c in cards:
        note = Note(model=model, fields=[c["front"], c["back"]])
        deck.add_note(note)
    Package(deck).write_to_file(out_file)
    print("Exported", len(cards), "cards to", out_file)

if __name__ == "__main__":
    import sys
    cards_file = sys.argv[1] if len(sys.argv) > 1 else "anki_cards.json"
    with open(cards_file, encoding="utf-8") as f:
        cards = json.load(f)
    export_cards_to_apkg(cards)
