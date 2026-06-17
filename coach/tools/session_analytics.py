"""Session analytics — aggregate insight ledger + session data into stats.
Generates CLI reports and optional HTML charts.

Usage:
  py -3 coach/tools/session_analytics.py
  py -3 coach/tools/session_analytics.py --days 14
  py -3 coach/tools/session_analytics.py --chart        # HTML bar chart
  py -3 coach/tools/session_analytics.py --event deep_research_complete
"""
import datetime
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
SESS_DIR = MEM_DIR / "sessions"
WORK_DIR = Path(__file__).resolve().parent.parent / "work"
WORK_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from insight_ledger import _load as load_ledger


def load_sessions(days: int) -> list[dict]:
    """Load session files from the last N days."""
    cutoff = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    sessions = []
    if not SESS_DIR.exists():
        return sessions
    for fp in sorted(SESS_DIR.glob("session-*.md"), reverse=True):
        text = fp.read_text(encoding="utf-8")
        entry = {}
        body = []
        in_front, in_body = False, False
        for line in text.splitlines():
            if line.strip() == "---":
                if not in_front:
                    in_front = True
                elif in_front:
                    in_front, in_body = False, True
                continue
            if in_front and ":" in line:
                k, _, v = line.partition(":")
                entry[k.strip()] = v.strip().strip('"').strip("'")
            elif in_body:
                body.append(line)
        date_str = entry.get("date", "")[:10]
        if date_str >= cutoff:
            entry["_body"] = "\n".join(body)
            sessions.append(entry)
    return sessions


def compute_skill_breakdown(sessions: list[dict]) -> list[dict]:
    """Aggregate sessions by skill."""
    by_skill = defaultdict(lambda: {"count": 0, "total_min": 0, "ratings": [], "dates": []})
    for s in sessions:
        skill = s.get("skill", "unknown")
        by_skill[skill]["count"] += 1
        try:
            by_skill[skill]["total_min"] += int(s.get("duration_min", 0))
        except (ValueError, TypeError):
            pass
        try:
            by_skill[skill]["ratings"].append(int(s.get("rating", 0)))
        except (ValueError, TypeError):
            pass
        by_skill[skill]["dates"].append(s.get("date", "")[:10])
    result = []
    for skill, data in sorted(by_skill.items(), key=lambda x: -x[1]["total_min"]):
        avg_r = round(sum(data["ratings"]) / len(data["ratings"]), 1) if data["ratings"] else 0
        result.append({
            "skill": skill,
            "sessions": data["count"],
            "total_min": data["total_min"],
            "avg_rating": avg_r,
            "last_date": max(data["dates"]),
        })
    return result


def compute_ledger_events(ledger: list[dict], days: int) -> dict:
    """Aggregate insight ledger events."""
    cutoff = (datetime.datetime.now(datetime.timezone.utc) -
              datetime.timedelta(days=days)).isoformat()
    recent = [e for e in ledger if e.get("timestamp", "") >= cutoff]
    by_event = Counter()
    by_day = Counter()
    for e in recent:
        by_event[e["event"]] += 1
        day = e.get("timestamp", "")[:10]
        by_day[day] += 1
    return {
        "total_events": len(recent),
        "by_event": dict(by_event.most_common()),
        "by_day": dict(sorted(by_day.items())),
    }


def generate_chart_html(analytics: dict) -> str:
    """Generate a self-contained HTML bar chart."""
    skill_rows = analytics["skill_breakdown"]
    top_skills = skill_rows[:10]
    labels = json.dumps([s["skill"][:18] for s in top_skills])
    sessions_data = json.dumps([s["sessions"] for s in top_skills])
    hours_data = json.dumps([round(s["total_min"] / 60, 1) for s in top_skills])
    ratings_data = json.dumps([s["avg_rating"] for s in top_skills])

    event_items = json.dumps(list(analytics["ledger"]["by_event"].items()))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Coach Analytics — {datetime.date.today()}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 1000px; margin: 2rem auto; padding: 0 1rem; }}
h1 {{ color: #1a1a2e; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
canvas {{ max-height: 300px; }}
table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
th, td {{ padding: 0.5rem; text-align: left; border-bottom: 1px solid #ddd; }}
th {{ background: #1a1a2e; color: white; }}
tr:hover {{ background: #f5f5f5; }}
</style>
</head>
<body>
<h1>Coach Analytics</h1>
<p>Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}</p>

<div class="grid">
  <div>
    <h3>Sessions by Skill</h3>
    <canvas id="chartSessions"></canvas>
  </div>
  <div>
    <h3>Hours by Skill</h3>
    <canvas id="chartHours"></canvas>
  </div>
</div>

<div class="grid">
  <div>
    <h3>Average Rating by Skill</h3>
    <canvas id="chartRatings"></canvas>
  </div>
  <div>
    <h3>Ledger Events (total: {analytics["ledger"]["total_events"]})</h3>
    <canvas id="chartEvents"></canvas>
  </div>
</div>

<h2>Skill Breakdown</h2>
<table>
  <tr><th>Skill</th><th>Sessions</th><th>Hours</th><th>Avg Rating</th><th>Last</th></tr>
{"".join(f"<tr><td>{s['skill']}</td><td>{s['sessions']}</td><td>{round(s['total_min']/60,1)}</td><td>{s['avg_rating']}</td><td>{s['last_date']}</td></tr>" for s in skill_rows)}
</table>

<script>
new Chart(document.getElementById('chartSessions'), {{
  type: 'bar',
  data: {{
    labels: {labels},
    datasets: [{{ label: 'Sessions', data: {sessions_data}, backgroundColor: '#4a6cf7' }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }} }}
}});
new Chart(document.getElementById('chartHours'), {{
  type: 'bar',
  data: {{
    labels: {labels},
    datasets: [{{ label: 'Hours', data: {hours_data}, backgroundColor: '#6c63ff' }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }} }}
}});
new Chart(document.getElementById('chartRatings'), {{
  type: 'line',
  data: {{
    labels: {labels},
    datasets: [{{ label: 'Avg Rating', data: {ratings_data}, borderColor: '#f7b731', tension: 0.3 }}]
  }},
  options: {{ responsive: true, scales: {{ y: {{ min: 0, max: 5 }} }} }}
}});
const events = {event_items};
new Chart(document.getElementById('chartEvents'), {{
  type: 'doughnut',
  data: {{
    labels: events.map(e => e[0]),
    datasets: [{{ data: events.map(e => e[1]), backgroundColor: ['#4a6cf7','#6c63ff','#f7b731','#20c997','#e83e8c','#fd7e14'] }}]
  }}
}});
</script>
</body>
</html>"""
    return html


def main():
    args = sys.argv[1:]
    days = 7
    show_chart = False
    event_filter = None

    i = 0
    while i < len(args):
        if args[i] == "--days" and i + 1 < len(args):
            days = int(args[i + 1])
            i += 2
            continue
        if args[i] == "--chart":
            show_chart = True
            i += 1
            continue
        if args[i] == "--event" and i + 1 < len(args):
            event_filter = args[i + 1]
            i += 2
            continue
        i += 1

    print(f"=== Session Analytics (last {days} days) ===\n")

    sessions = load_sessions(days)
    ledger = load_ledger()

    if event_filter:
        ledger = [e for e in ledger if e["event"] == event_filter]

    skill_breakdown = compute_skill_breakdown(sessions)
    ledger_stats = compute_ledger_events(ledger, days)

    total_min = sum(s["total_min"] for s in skill_breakdown)
    total_sessions = sum(s["sessions"] for s in skill_breakdown)

    print(f"Sessions found: {total_sessions} ({total_min} min = {round(total_min/60,1)}h)")
    print(f"Skills active: {len(skill_breakdown)}")
    print(f"Ledger events: {ledger_stats['total_events']}\n")

    print(f"{'Skill':<25} {'Sessions':<10} {'Hours':<8} {'Rating':<8} {'Last'}")
    print("-" * 65)
    for s in skill_breakdown:
        print(f"{s['skill']:<25} {s['sessions']:<10} {round(s['total_min']/60,1):<8} {s['avg_rating']:<8} {s['last_date']}")

    if ledger_stats["by_event"]:
        print(f"\n--- Ledger Event Breakdown ---")
        for event, count in ledger_stats["by_event"].items():
            print(f"  {event}: {count}")

    if ledger_stats["by_day"]:
        print(f"\n--- Daily Event Activity ---")
        for day, count in ledger_stats["by_day"].items():
            print(f"  {day}: {count} events")

    analytics = {
        "skill_breakdown": skill_breakdown,
        "ledger": ledger_stats,
        "total_min": total_min,
        "total_sessions": total_sessions,
        "period_days": days,
    }

    if show_chart:
        html = generate_chart_html(analytics)
        path = WORK_DIR / f"analytics-{datetime.date.today().isoformat()}.html"
        path.write_text(html, encoding="utf-8")
        print(f"\nHTML chart saved: {path}")

    print(f"\n=== Done ===")


if __name__ == "__main__":
    main()
