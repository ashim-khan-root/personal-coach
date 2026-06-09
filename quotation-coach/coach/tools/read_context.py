"""Read context: checkpoint, goals, habits, recent sessions. Usage: python read_context.py [N]"""
import sys
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"

def read_md(name):
    p = MEM_DIR / name
    return p.read_text(encoding="utf-8") if p.exists() else f"[{name} not found]"

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("="*60)
    print("  QUOTATION COACH — CONTEXT")
    print("="*60)
    print("\n--- CHECKPOINT ---")
    print(read_md("checkpoint.md")[:500])
    print("\n--- GOALS ---")
    print(read_md("goals.md")[:500])
    print("\n--- PROFILE ---")
    print(read_md("profile.md")[:300])
    print("\n--- RECENT SESSIONS ---")
    sessions = sorted(SESS_DIR.glob("session-*.md"), reverse=True)[:n] if (SESS_DIR := MEM_DIR / "sessions").exists() else []
    for s in sessions:
        txt = s.read_text(encoding="utf-8").splitlines()[:6]
        print("\n".join(txt))
        print()
    print("="*60)

if __name__ == "__main__":
    main()
