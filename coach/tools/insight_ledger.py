"""Insight Ledger — lightweight event logging for every tool.
Each tool can log runtime, quality, and outcome data. The ledger
accumulates into a SQLite database that weekly_synthesis, session_analytics,
and other reflective tools can query.

Usage:
  from insight_ledger import log_insight, query_insights

  log_insight("tool_run", {"tool": "uuid_generator", "runtime_ms": 12})
  recent = query_insights(event="tool_run", limit=10)
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db import log_insight, query_insights, get_insight_stats as get_stats


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
    from db import init_db
    init_db()
    main()
