"""Store a practice session. Usage:
  python store_session.py <skill> <duration_min> <rating> [notes]
"""
import sys, uuid, datetime
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
SESS_DIR = MEM_DIR / "sessions"
SESS_DIR.mkdir(parents=True, exist_ok=True)

def main():
    if len(sys.argv) < 4:
        print("Usage: python store_session.py <skill> <duration_min> <rating> [notes]")
        sys.exit(1)
    skill = sys.argv[1]
    duration_min = sys.argv[2]
    rating = sys.argv[3]
    notes = sys.argv[4] if len(sys.argv) > 4 else ""
    sid = str(uuid.uuid4())
    now = datetime.datetime.now(datetime.timezone.utc)
    timestamp = now.isoformat()
    filename = now.strftime("session-%Y%m%d-%H%M%S") + ".md"
    content = (
        f"---\n"
        f"id: {sid}\n"
        f"date: {timestamp}\n"
        f"skill: {skill}\n"
        f"duration_min: {duration_min}\n"
        f"rating: {rating}\n"
        f"notes: |\n"
        f"  {notes}\n"
        f"tags: []\n"
        f"---\n"
    )
    fpath = SESS_DIR / filename
    fpath.write_text(content, encoding="utf-8")
    print(f"Session stored: {fpath.name}")
    print(f"skill: {skill} | duration: {duration_min}min | rating: {rating}/10")

    meta_path = MEM_DIR / "meta.md"
    if meta_path.exists():
        meta = meta_path.read_text(encoding="utf-8")
        lines = meta.splitlines()
        new_lines = []
        updated = False
        for line in lines:
            if line.startswith("updated_at:"):
                new_lines.append(f"updated_at: {datetime.datetime.utcnow().isoformat()}")
                updated = True
            else:
                new_lines.append(line)
        if not updated:
            new_lines.append(f"updated_at: {datetime.datetime.utcnow().isoformat()}")
        meta_path.write_text("\n".join(new_lines), encoding="utf-8")

if __name__ == "__main__":
    main()
