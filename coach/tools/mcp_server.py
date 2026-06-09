"""MCP server for coach memory.
Exposes vector search + context tools over stdio transport.

Usage:
  python tools/mcp_server.py                    # run stdio server
  python tools/mcp_server.py --interactive      # test via interactive REPL
"""
import sys, datetime
from pathlib import Path
from collections import Counter

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"

sys.path.insert(0, str(MEM_DIR.parent))
from tools.index_memory import load_index


# ── helpers ───────────────────────────────────────────────────────────────

def _read_file(path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _get_checkpoint_text():
    fp = MEM_DIR / "checkpoint.md"
    if not fp.exists():
        return "No checkpoint set."
    text = _read_file(fp)
    return text


def _get_goals_text():
    fp = MEM_DIR / "goals.md"
    if not fp.exists():
        return "No goals set."
    text = _read_file(fp)
    goals = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- title:"):
            title = line.split(":", 1)[1].strip().strip('"')
            goals.append(f"- {title}")
    return "\n".join(goals) if goals else text[:500]


def _get_recent_sessions(n=5):
    sess_dir = MEM_DIR / "sessions"
    files = sorted(sess_dir.glob("session-*.md"), reverse=True)[:n]
    results = []
    for fp in files:
        text = _read_file(fp)
        meta = {}
        for line in text.splitlines():
            if line.startswith("skill:"):
                meta["skill"] = line.split(":", 1)[1].strip()
            elif line.startswith("rating:"):
                meta["rating"] = line.split(":", 1)[1].strip()
            elif line.startswith("duration_min:"):
                meta["duration"] = line.split(":", 1)[1].strip()
            elif line.startswith("date:"):
                meta["date"] = line.split(":", 1)[1].strip().strip('"')
        meta["filename"] = fp.name
        results.append(meta)
    return results


def _get_context_summary():
    parts = []
    today = datetime.date.today().isoformat()

    checkpoint = _get_checkpoint_text()
    for line in checkpoint.splitlines():
        if line.startswith("phase:"):
            parts.append(f"Phase: {line.split(':', 1)[1].strip()}")
        elif line.startswith("current_topic:"):
            parts.append(f"Topic: {line.split(':', 1)[1].strip()}")
        elif line.startswith("next_task:"):
            parts.append(f"Next: {line.split(':', 1)[1].strip()}")

    goals = _get_goals_text()
    if goals:
        glines = [l for l in goals.splitlines() if l.startswith("- ")]
        parts.append(f"Goals ({len(glines)}):")
        for g in glines[:3]:
            parts.append(f"  {g}")

    recent = _get_recent_sessions(1)
    if recent:
        s = recent[0]
        parts.append(f"Last session: {s.get('skill', '?')} ({s.get('rating', '?')}/10)")

    parts.append(f"Date: {today}")
    return "\n".join(parts)


# ── MCP server ────────────────────────────────────────────────────────────

def run_stdio():
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("coach-memory")

    idx = load_index()

    @mcp.tool()
    def search_memory(query: str, limit: int = 10) -> str:
        if idx is None:
            return "Error: memory index not built. Run `python tools/index_memory.py` first."
        results = idx.search(query, limit)
        if not results:
            return f'No results for "{query}"'
        lines = [f"=== Results for: {query} ==="]
        for r in results:
            src = r["meta"]["source"]
            fn = r["meta"]["filename"]
            snippet = r["text"][:300].replace("\n", " ").strip()
            lines.append(f"\n[{r['score']:.3f}] ({src}) {fn}")
            lines.append(f"  {snippet}")
        return "\n".join(lines)

    @mcp.tool()
    def get_context() -> str:
        return _get_context_summary()

    @mcp.tool()
    def get_checkpoint() -> str:
        return _get_checkpoint_text()

    @mcp.tool()
    def get_goals() -> str:
        return _get_goals_text()

    @mcp.tool()
    def get_recent_sessions(n: int = 5) -> str:
        sessions = _get_recent_sessions(n)
        if not sessions:
            return "No sessions found."
        lines = ["=== Recent Sessions ==="]
        for s in sessions:
            lines.append(f"\n{s.get('filename', '?')}")
            lines.append(f"  Skill: {s.get('skill', '?')}")
            lines.append(f"  Rating: {s.get('rating', '?')}/10")
            lines.append(f"  Duration: {s.get('duration', '?')}min")
            if s.get('date'):
                lines.append(f"  Date: {s['date']}")
        return "\n".join(lines)

    @mcp.tool()
    def get_habits() -> str:
        fp = MEM_DIR / "habits.md"
        if not fp.exists():
            return "No habits tracked."
        return _read_file(fp)

    @mcp.tool()
    def web_search(query: str, max_results: int = 10) -> str:
        from tools.web_search import search_web
        results = search_web(query, max_results)
        if not results:
            return f'No results for "{query}"'
        lines = [f"=== Web Search: {query} ==="]
        for r in results[:max_results]:
            lines.append(f"\n{r.get('title', '?')}")
            lines.append(f"  URL: {r.get('url', '?')}")
            lines.append(f"  {r.get('snippet', '')[:300]}")
        return "\n".join(lines)

    @mcp.tool()
    def web_fetch(url: str) -> str:
        from tools.web_fetch import fetch_url
        result = fetch_url(url)
        if "error" in result:
            return f"Error: {result['error']}"
        lines = [f"=== {result.get('title', url)} ==="]
        lines.append(f"URL: {url}")
        lines.append("")
        lines.append(result.get("text", ""))
        return "\n".join(lines)

    @mcp.resource("memory://checkpoint")
    def resource_checkpoint() -> str:
        return _get_checkpoint_text()

    @mcp.resource("memory://goals")
    def resource_goals() -> str:
        return _get_goals_text()

    @mcp.resource("memory://sessions/recent")
    def resource_recent_sessions() -> str:
        sessions = _get_recent_sessions(5)
        lines = ["# Recent Sessions"]
        for s in sessions:
            lines.append(f"- {s.get('skill', '?')} — {s.get('rating', '?')}/10 ({s.get('date', '?')})")
        return "\n".join(lines)

    mcp.run(transport="stdio")


# ── interactive test mode ────────────────────────────────────────────────

def run_interactive():
    print("=== Coach Memory MCP (interactive) ===\n")
    idx = load_index()
    if idx:
        print(f"Index loaded: {len(idx.entries)} chunks, {len(idx.vocab)} terms")
    else:
        print("No index found. Run `python tools/index_memory.py` first.")

    while True:
        try:
            cmd = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not cmd:
            continue
        if cmd in ("exit", "quit"):
            break
        if cmd == "context":
            print(_get_context_summary())
        elif cmd == "checkpoint":
            print(_get_checkpoint_text())
        elif cmd == "goals":
            print(_get_goals_text())
        elif cmd.startswith("sessions"):
            parts = cmd.split()
            n = int(parts[1]) if len(parts) > 1 else 5
            sessions = _get_recent_sessions(n)
            for s in sessions:
                print(f"  {s.get('skill','?')} — {s.get('rating','?')}/10 — {s.get('date','?')}")
        else:
            if idx:
                results = idx.search(cmd, 5)
                for r in results:
                    fn = r["meta"]["filename"]
                    snippet = r["text"][:150].replace("\n", " ").strip()
                    print(f"  [{r['score']:.3f}] {fn}")
                    print(f"    {snippet}")
            else:
                print("No index available.")


def main():
    if "--interactive" in sys.argv:
        run_interactive()
    else:
        run_stdio()


if __name__ == "__main__":
    main()
