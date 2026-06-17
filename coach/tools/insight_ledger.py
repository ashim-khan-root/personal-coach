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
    """Log a single event. Thread-safe for CLI use (no concurrency)."""
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
    """Query the insight ledger.

    Args:
        event: Filter by event name (exact match).
        since: ISO date string, e.g. "2026-06-01" — only entries after this.
        limit: Max results. Default 50, use 0 for all.
    """
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
    """Return aggregate stats: total events, unique event types, date range."""
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
    """CLI entry point."""
    args = sys.argv[1:]
    if not args or args[0] == "--help":
        print("Usage:")
        print("  py -3 insight_ledger.py log <event> [--payload '{\"key\":\"val\"}']")
        print("  py -3 insight_ledger.py query [--event <name>] [--since <date>] [--limit N]")
        print("  py -3 insight_ledger.py stats")
        return

    cmd = args[0]
    if cmd == "log" and len(args) >= 2:
        event = args[1]
        payload = {}
        if "--payload" in args:
            idx = args.index("--payload")
            if idx + 1 < len(args):
                try:
                    payload = json.loads(args[idx + 1])
                except json.JSONDecodeError:
                    print(f"Invalid payload JSON: {args[idx + 1]}")
                    sys.exit(1)
        log_insight(event, payload)
        print(f"[OK] Logged '{event}'")

    elif cmd == "query":
        event = None
        since = None
        limit = 50
        if "--event" in args:
            idx = args.index("--event")
            if idx + 1 < len(args):
                event = args[idx + 1]
        if "--since" in args:
            idx = args.index("--since")
            if idx + 1 < len(args):
                since = args[idx + 1]
        if "--limit" in args:
            idx = args.index("--limit")
            if idx + 1 < len(args):
                limit = int(args[idx + 1])
        results = query_insights(event=event, since=since, limit=limit)
        print(f"[OK] {len(results)} entries:")
        for r in results:
            ts = r.get("timestamp", "?")[11:19]
            ev = r["event"]
            pl = json.dumps(r.get("payload", {}), ensure_ascii=False)
            print(f"  {ts}  {ev}  {pl[:120]}")

    elif cmd == "stats":
        stats = get_stats()
        print(json.dumps(stats, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
