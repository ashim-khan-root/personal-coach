"""Analyze quotation history for patterns and insights. Usage: python analyze_patterns.py"""
import json, datetime
from pathlib import Path
from collections import Counter, defaultdict

BASE = Path(__file__).resolve().parent.parent
MEM_DIR = BASE / "memory"
SESS_DIR = MEM_DIR / "sessions"
QUOTES_DIR = MEM_DIR / "quotations"

def analyze():
    sessions = sorted(SESS_DIR.glob("session-*.md")) if SESS_DIR.exists() else []
    if not sessions:
        print("No sessions found. Run some quotations first.")
        return

    cam_types = Counter()
    total_qar = 0
    moi_count = 0
    daily_counts = defaultdict(int)
    monthly_revenue = defaultdict(float)

    for s in sessions:
        txt = s.read_text(encoding="utf-8")
        lines = txt.splitlines()
        meta = {}
        for line in lines:
            if line.startswith("---"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()

        ct = meta.get("cam_type", "unknown")
        cam_types[ct] += int(meta.get("cam_count", 0))
        total_qar += float(meta.get("total_qar", 0))

        if meta.get("moi_compliant") == "yes":
            moi_count += 1

        date_str = meta.get("date", "")[:10]
        if date_str:
            month_key = date_str[:7]
            monthly_revenue[month_key] += float(meta.get("total_qar", 0))
            daily_counts[date_str] += 1

    print("="*60)
    print("  QUOTATION PATTERN ANALYSIS")
    print("="*60)
    print(f"\nTotal sessions: {len(sessions)}")
    print(f"Total cameras quoted: {sum(cam_types.values())}")
    print(f"Total revenue quoted: {total_qar:,.0f} QAR")
    print(f"MOI-compliant quotes: {moi_count} ({moi_count/len(sessions)*100:.0f}%)")
    print(f"Average quote value: {total_qar/len(sessions):,.0f} QAR")

    print(f"\n--- Camera Type Breakdown ---")
    for ct, count in cam_types.most_common():
        print(f"  {ct:20s} {count:>4} cameras")

    print(f"\n--- Monthly Revenue ---")
    for month, rev in sorted(monthly_revenue.items()):
        print(f"  {month}: {rev:>10,.0f} QAR")

    print(f"\n--- Busiest Days ---")
    for day, count in sorted(daily_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {day}: {count} quotes")

    print()

if __name__ == "__main__":
    analyze()
