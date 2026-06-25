"""Insight Ledger — lightweight event logging for every tool.
Each tool can log runtime, quality, and outcome data. The ledger
accumulates into a JSON file that weekly_synthesis, session_analytics,
and other reflective tools can query.

Usage:
  from insight_ledger import log_insight, query_insights

  log_insight("tool_run", {"tool": "uuid_generator", "runtime_ms": 12})
  recent = query_insights(event="tool_run", limit=10)
"""
import datetime
import json
import sys
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
LEDGER_FILE = MEM_DIR / "insight_ledger.json"


def _load() -> list[dict]:
    if not LEDGER_FILE.exists():
        return []
    try:
        raw = LEDGER_FILE.read_text(encoding="utf-8")
        return json.loads(raw) if raw else []
    except (json.JSONDecodeError, OSError):
        return []


def _save(entries: list[dict]):
    LEDGER_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def log_insight(event: str, payload: dict | None = None):
    entries = _load()
    entries.append({
        "event": event,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "payload": payload or {},
    })
    _save(entries)


def query_insights(event: str | None = None,
                   since: str | None = None,
                   limit: int = 50) -> list[dict]:
    entries = _load()
    if event:
        entries = [e for e in entries if e["event"] == event]
    if since:
        entries = [e for e in entries if e.get("timestamp", "") >= since]
    entries.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
    if limit > 0:
        entries = entries[:limit]
    return entries


def get_stats() -> dict:
    entries = _load()
    if not entries:
        return {"total": 0, "event_types": [], "earliest": None, "latest": None}
    types = list({e["event"] for e in entries})
    timestamps = [e["timestamp"] for e in entries if e.get("timestamp")]
    return {
        "total": len(entries),
        "event_types": sorted(types),
        "earliest": min(timestamps) if timestamps else None,
        "latest": max(timestamps) if timestamps else None,
    }



def main():
    import argparse
    parser = argparse.ArgumentParser(description="Insight Ledger — event logging")
    sub = parser.add_subparsers(dest="command", required=True)

    p_log = sub.add_parser("log", help="Log an event")
    p_log.add_argument("event", help="Event name")
    p_log.add_argument("--payload", help="JSON payload string")

    p_query = sub.add_parser("query", help="Query events")
    p_query.add_argument("--event", help="Filter by event name")
    p_query.add_argument("--since", help="ISO date filter")
    p_query.add_argument("--limit", type=int, default=50, help="Max results")

    sub.add_parser("stats", help="Show aggregate stats")

    args = parser.parse_args()

    if args.command == "log":
        payload = json.loads(args.payload) if args.payload else {}
        log_insight(args.event, payload)
        print(f"[OK] Logged '{args.event}'")
    elif args.command == "query":
        results = query_insights(event=args.event, since=args.since, limit=args.limit)
        print(f"[OK] {len(results)} entries:")
        for r in results:
            ts = r.get("timestamp", "?")[11:19]
            ev = r["event"]
            pl = json.dumps(r.get("payload", {}), ensure_ascii=False)
            print(f"  {ts}  {ev}  {pl[:120]}")
    elif args.command == "stats":
        print(json.dumps(get_stats(), indent=2))


if __name__ == "__main__":
    main()
