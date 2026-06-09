"""Store a quotation session. Usage:
  python store_session.py <cam_count> <cam_type> <total_qar> [notes] [--moi]
"""
import sys, uuid, datetime as dt
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
SESS_DIR = MEM_DIR / "sessions"
SESS_DIR.mkdir(parents=True, exist_ok=True)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    moi = "--moi" in sys.argv
    if len(args) < 3:
        print("Usage: python store_session.py <cam_count> <cam_type> <total_qar> [notes] [--moi]")
        sys.exit(1)
    sid = str(uuid.uuid4())
    now = dt.datetime.now(dt.timezone.utc)
    ts = now.isoformat()
    fn = now.strftime("session-%Y%m%d-%H%M%S") + ".md"
    content = f"""---
id: {sid}
date: {ts}
cam_count: {args[0]}
cam_type: {args[1]}
total_qar: {args[2]}
moi_compliant: {'yes' if moi else 'no'}
notes: {" ".join(args[3:]) if len(args) > 3 else ""}
tags: [quotation, {args[1]}]
---
"""
    fpath = SESS_DIR / fn
    fpath.write_text(content, encoding="utf-8")
    print(f"Session stored: {fpath.name}")
    print(f"{args[0]} x {args[1]} = {args[2]} QAR {'(MOI)' if moi else ''}")

if __name__ == "__main__":
    main()
