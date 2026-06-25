"""MCP server for coach memory.
Exposes vector search + context tools over stdio transport.

Usage:
  python tools/mcp_server.py                    # run stdio server
  python tools/mcp_server.py --interactive      # test via interactive REPL
"""
import sys, datetime, asyncio, io, contextlib
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"

sys.path.insert(0, str(MEM_DIR.parent))
from tools.index_memory import load_index

_IDX = None

def _get_idx():
    global _IDX
    if _IDX is None:
        _IDX = load_index()
    return _IDX

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
    return _read_file(fp)

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

# ── MCP tool handlers ────────────────────────────────────────────────────

def _tool_search_memory(query: str, limit: int = 10) -> str:
    idx = _get_idx()
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

def _tool_get_context() -> str:
    return _get_context_summary()

def _tool_get_checkpoint() -> str:
    return _get_checkpoint_text()

def _tool_get_goals() -> str:
    return _get_goals_text()

def _tool_get_recent_sessions(n: int = 5) -> str:
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

def _tool_get_habits() -> str:
    fp = MEM_DIR / "habits.md"
    if not fp.exists():
        return "No habits tracked."
    return _read_file(fp)

def _tool_web_search(query: str, max_results: int = 10) -> str:
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

def _tool_web_fetch(url: str) -> str:
    from tools.web_fetch import fetch_url
    result = fetch_url(url)
    if "error" in result:
        return f"Error: {result['error']}"
    lines = [f"=== {result.get('title', url)} ==="]
    lines.append(f"URL: {url}")
    lines.append("")
    lines.append(result.get("text", ""))
    return "\n".join(lines)

def _tool_seo_audit(url: str, crawl: bool = False, max_pages: int = 5, backlinks: bool = False, speed: bool = False) -> str:
    from tools.seo_audit import audit_url, format_report
    result = audit_url(url, with_crawl=crawl, max_pages=max_pages, with_backlinks=backlinks, with_speed=speed)
    if "error" in result:
        return f"Error: {result['error']}"
    return format_report(result)

def _tool_task_manager(action: str, title: str = "", priority: str = "medium", notes: str = "", task_id: str = "") -> str:
    from tools.task_manager import cmd_add, cmd_list, cmd_done, cmd_delete
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        if action == "add":
            cmd_add(title, priority, notes)
        elif action == "list":
            cmd_list("all")
        elif action == "done" and task_id:
            cmd_done(task_id)
        elif action == "delete" and task_id:
            cmd_delete(task_id)
    return buf.getvalue()

def _tool_deep_research(topic: str, max_per_query: int = 5, iterative: bool = False, no_llm: bool = False) -> str:
    if iterative:
        from tools.deep_research import agent_loop, DEFAULT_MAX_ITERATIONS
        report, state = asyncio.run(agent_loop(
            query=topic, provider=None, model=None,
            max_iterations=DEFAULT_MAX_ITERATIONS, verbose=False,
        ))
        summary = (
            f"## Deep Research: {topic}\n\n"
            f"**Topics covered:** {len(state.mind_map.findings)}\n"
            f"**Sources:** {state.mind_map.source_count()}\n"
            f"**Iterations:** {state.iteration}\n\n"
            f"---\n\n{report[:3000]}"
        )
        if len(report) > 3000:
            summary += f"\n\n*(truncated, full report saved to `coach/work/research/`)*"
        return summary
    else:
        from tools.deep_research import simple_research
        report = asyncio.run(simple_research(
            topic=topic, max_per_query=max_per_query, try_llm=not no_llm,
        ))
        return report[:3000] + ("\n\n*(truncated)*" if len(report) > 3000 else "")

def _tool_site_survey(action: str, client: str = "", location: str = "", contact: str = "", notes: str = "", survey_id: str = "", summary: str = "") -> str:
    from tools.site_survey import cmd_add, cmd_list, cmd_view, cmd_close
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        if action == "add":
            cmd_add(client, location, contact, notes)
        elif action == "list":
            cmd_list("open")
        elif action == "view" and survey_id:
            cmd_view(survey_id)
        elif action == "close" and survey_id:
            cmd_close(survey_id, summary)
    return buf.getvalue()

# ── MCP server ────────────────────────────────────────────────────────────

def run_stdio():
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("coach-memory")

    mcp.tool(name="search_memory")(_tool_search_memory)
    mcp.tool(name="get_context")(_tool_get_context)
    mcp.tool(name="get_checkpoint")(_tool_get_checkpoint)
    mcp.tool(name="get_goals")(_tool_get_goals)
    mcp.tool(name="get_recent_sessions")(_tool_get_recent_sessions)
    mcp.tool(name="get_habits")(_tool_get_habits)
    mcp.tool(name="web_search")(_tool_web_search)
    mcp.tool(name="web_fetch")(_tool_web_fetch)
    mcp.tool(name="seo_audit")(_tool_seo_audit)
    mcp.tool(name="task_manager")(_tool_task_manager)
    mcp.tool(name="deep_research")(_tool_deep_research)
    mcp.tool(name="site_survey")(_tool_site_survey)

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

_INTERACTIVE_DISPATCH = {}

def _register_interactive(name, fn, needs_idx=False):
    _INTERACTIVE_DISPATCH[name] = (fn, needs_idx)

def _icmd_context():
    print(_get_context_summary())

def _icmd_checkpoint():
    print(_get_checkpoint_text())

def _icmd_goals():
    print(_get_goals_text())

def _icmd_sessions(cmd):
    parts = cmd.split()
    n = int(parts[1]) if len(parts) > 1 else 5
    sessions = _get_recent_sessions(n)
    for s in sessions:
        print(f"  {s.get('skill','?')} — {s.get('rating','?')}/10 — {s.get('date','?')}")

def _icmd_search(cmd):
    idx = _get_idx()
    if not idx:
        print("No index available.")
        return
    query = cmd
    results = idx.search(query, 5)
    for r in results:
        fn = r["meta"]["filename"]
        snippet = r["text"][:150].replace("\n", " ").strip()
        print(f"  [{r['score']:.3f}] {fn}")
        print(f"    {snippet}")

def _icmd_deep(cmd):
    topic = cmd[4:].strip()
    from tools.deep_research import simple_research
    report = asyncio.run(simple_research(topic))
    print(report[:2000])

def _icmd_seo(cmd):
    from tools.seo_audit import audit_url, format_report
    parts = cmd.split(maxsplit=1)
    url = parts[1] if len(parts) > 1 else input("URL: ")
    result = audit_url(url)
    print(format_report(result))

_register_interactive("context", _icmd_context)
_register_interactive("checkpoint", _icmd_checkpoint)
_register_interactive("goals", _icmd_goals)


def _handle_interactive_cmd(cmd):
    if cmd in ("exit", "quit"):
        return False
    if not cmd:
        return True

    if cmd == "context":
        _icmd_context()
    elif cmd == "checkpoint":
        _icmd_checkpoint()
    elif cmd == "goals":
        _icmd_goals()
    elif cmd.startswith("sessions"):
        _icmd_sessions(cmd)
    elif cmd.startswith("deep"):
        _icmd_deep(cmd)
    elif cmd.startswith("seo"):
        _icmd_seo(cmd)
    else:
        _icmd_search(cmd)
    return True


def run_interactive():
    print("=== Coach Memory MCP (interactive) ===\n")
    idx = _get_idx()
    if idx:
        print(f"Index loaded: {len(idx.entries)} chunks, {len(idx.vocab)} terms")
    else:
        print("No index found. Run `python tools/index_memory.py` first.")

    while True:
        try:
            cmd = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not _handle_interactive_cmd(cmd):
            break


def main():
    if "--interactive" in sys.argv:
        run_interactive()
    else:
        run_stdio()


if __name__ == "__main__":
    main()
