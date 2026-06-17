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

    @mcp.tool()
    def seo_audit(url: str, crawl: bool = False, max_pages: int = 5, backlinks: bool = False, speed: bool = False) -> str:
        """Run an SEO audit on a URL. Optionally crawl sampled sitemap pages, check backlinks via Common Crawl (free), and check page speed (free).
        
        Args:
            url: The URL to audit
            crawl: If True, sample pages from the sitemap and check content depth, images, alt text, internal links
            max_pages: Number of pages to sample from the sitemap (used when crawl=True, default 5)
            backlinks: If True, check backlinks via Common Crawl CDX API (free, no API key)
            speed: If True, check page speed via Google PageSpeed Insights API (free, no API key)
        """
        from tools.seo_audit import audit_url, format_report
        result = audit_url(url, with_crawl=crawl, max_pages=max_pages, with_backlinks=backlinks, with_speed=speed)
        if "error" in result:
            return f"Error: {result['error']}"
        return format_report(result)

    @mcp.tool()
    def task_manager(action: str, title: str = "", priority: str = "medium", notes: str = "", task_id: str = "") -> str:
        """Manage tasks. Actions: add, list, done, delete.
        
        Args:
            action: add, list, done, or delete
            title: Task title (required for add)
            priority: low, medium, or high (default medium, used with add)
            notes: Optional notes (used with add)
            task_id: Task ID (required for done and delete)
        """
        from tools.task_manager import cmd_add, cmd_list, cmd_done, cmd_delete
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            if action == "add":
                cmd_add(title, priority, notes)
            elif action == "list":
                cmd_list("all")
            elif action == "done":
                if task_id:
                    cmd_done(task_id)
            elif action == "delete":
                if task_id:
                    cmd_delete(task_id)
        return buf.getvalue()

    @mcp.tool()
    def deep_research(topic: str, max_per_query: int = 5, iterative: bool = False, no_llm: bool = False) -> str:
        """Deep research on any topic using web search + optional LLM synthesis.
        
        Args:
            topic: The topic to research
            max_per_query: Max results per search query (default 5)
            iterative: Use iterative mode with follow-up queries (default False)
            no_llm: Skip LLM synthesis, use raw compilation (default False)
        """
        import asyncio
        from tools.deep_research import simple_research
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
            report = asyncio.run(simple_research(
                topic=topic, max_per_query=max_per_query, try_llm=not no_llm,
            ))
            return report[:3000] + ("\n\n*(truncated)*" if len(report) > 3000 else "")

    @mcp.tool()
    def site_survey(action: str, client: str = "", location: str = "", contact: str = "", notes: str = "", survey_id: str = "", summary: str = "") -> str:
        """Track MOI site survey visits. Actions: add, list, view, close.
        
        Args:
            action: add, list, view, or close
            client: Client name (required for add)
            location: Site location (required for add)
            contact: Contact person/phone (optional for add)
            notes: Survey notes (optional for add)
            survey_id: Survey ID (required for view and close)
            summary: Closing summary (optional for close)
        """
        from tools.site_survey import cmd_add, cmd_list, cmd_view, cmd_close
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            if action == "add":
                cmd_add(client, location, contact, notes)
            elif action == "list":
                cmd_list("open")
            elif action == "view":
                if survey_id:
                    cmd_view(survey_id)
            elif action == "close":
                if survey_id:
                    cmd_close(survey_id, summary)
        return buf.getvalue()

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
        elif cmd.startswith("deep"):
            import asyncio
            from tools.deep_research import simple_research
            topic = cmd[4:].strip()
            report = asyncio.run(simple_research(topic))
            print(report[:2000])
        elif cmd.startswith("seo"):
            from tools.seo_audit import audit_url, format_report
            parts = cmd.split(maxsplit=1)
            url = parts[1] if len(parts) > 1 else input("URL: ")
            result = audit_url(url)
            print(format_report(result))
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
