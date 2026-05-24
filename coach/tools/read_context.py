"""Print current memory summary for the AI coach to read."""
import sys
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
SESS_DIR = MEM_DIR / "sessions"

def read_md(file):
    if not file.exists():
        return ""
    return file.read_text(encoding="utf-8")

def main(max_items=5):
    meta = read_md(MEM_DIR / "meta.md")
    goals = read_md(MEM_DIR / "goals.md")
    habits = read_md(MEM_DIR / "habits.md")
    resources = read_md(MEM_DIR / "resources.md")
    sessions = sorted(SESS_DIR.glob("session-*.md"), key=lambda p: p.stem, reverse=True)[:max_items]
    recent = []
    for s in sessions:
        txt = read_md(s).splitlines()[:10]
        recent.append("\n".join(txt) + f"\n  (file: {s.name})")
    parts = []
    if meta:
        parts.append("=== META ===")
        parts.append(meta)
    if goals:
        parts.append("=== GOALS ===")
        parts.append(goals)
    if habits:
        parts.append("=== HABITS ===")
        parts.append(habits)
    if resources:
        parts.append("=== RESOURCES ===")
        parts.append(resources)
    if recent:
        parts.append("=== RECENT SESSIONS ===")
        parts.append("\n---\n".join(recent))
    print("\n\n".join(parts))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
