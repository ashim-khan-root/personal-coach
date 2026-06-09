"""Session hooks for pre/post quotation generation."""
import sys, json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MEM_DIR = BASE / "memory"

def pre_session():
    """Print pre-session context"""
    files = ["checkpoint.md", "goals.md"]
    for f in files:
        p = MEM_DIR / f
        if p.exists():
            print(f"=== {f} ===")
            print(p.read_text(encoding="utf-8")[:400])
            print()

def post_session(cam_count, cam_type, total_qar, notes=""):
    """Auto-store session and update meta"""
    import store_session
    store_session.main()

def main():
    if len(sys.argv) < 2:
        print("Usage: python session_hooks.py pre")
        print("       python session_hooks.py post <cam_count> <cam_type> <total_qar> [notes]")
        sys.exit(1)
    mode = sys.argv[1]
    if mode == "pre":
        pre_session()
    elif mode == "post":
        if len(sys.argv) >= 5:
            post_session(sys.argv[2], sys.argv[3], sys.argv[4], " ".join(sys.argv[5:]))
        else:
            print("post requires: cam_count cam_type total_qar [notes]")

if __name__ == "__main__":
    main()
