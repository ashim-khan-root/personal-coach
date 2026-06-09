"""MCP server for quotation-coach memory access.
Exposes: get_context, get_checkpoint, get_goals, get_recent_sessions, get_rates
"""
import json, sys
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"

def read_file(name):
    p = MEM_DIR / name
    return p.read_text(encoding="utf-8") if p.exists() else ""

def get_context():
    parts = []
    for f in ["checkpoint.md", "goals.md", "profile.md"]:
        c = read_file(f)
        if c:
            parts.append(f"=== {f} ===\n{c[:500]}")
    sessions_dir = MEM_DIR / "sessions"
    if sessions_dir.exists():
        sessions = sorted(sessions_dir.glob("session-*.md"), reverse=True)[:3]
        if sessions:
            parts.append("=== RECENT SESSIONS ===")
            for s in sessions:
                parts.append(s.read_text(encoding="utf-8")[:300])
    return "\n\n".join(parts)

def get_recent_sessions(n=5):
    sessions_dir = MEM_DIR / "sessions"
    if not sessions_dir.exists():
        return "No sessions found."
    sessions = sorted(sessions_dir.glob("session-*.md"), reverse=True)[:n]
    lines = []
    for s in sessions:
        meta = {}
        for line in s.read_text(encoding="utf-8").splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip('"')
        lines.append(f"- {meta.get('skill','?')} — {meta.get('rating','?')}/10 — {meta.get('date','?')}")
    return "\n".join(lines)

def get_checkpoint():
    return read_file("checkpoint.md") or "No checkpoint set."

def get_goals():
    return read_file("goals.md") or "No goals set."

def get_rates():
    return read_file("rates.json") or "No rates found."

def run_stdio():
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("quotation-memory")

    @mcp.tool()
    def get_context_tool() -> str:
        return get_context()

    @mcp.tool()
    def get_checkpoint_tool() -> str:
        return get_checkpoint()

    @mcp.tool()
    def get_goals_tool() -> str:
        return get_goals()

    @mcp.tool()
    def get_recent_sessions_tool(n: int = 5) -> str:
        return get_recent_sessions(n)

    @mcp.tool()
    def get_rates_tool() -> str:
        return get_rates()

    @mcp.resource("memory://checkpoint")
    def resource_checkpoint() -> str:
        return get_checkpoint()

    @mcp.resource("memory://goals")
    def resource_goals() -> str:
        return get_goals()

    @mcp.resource("memory://context")
    def resource_context() -> str:
        return get_context()

    mcp.run(transport="stdio")

def run_interactive():
    print("=== Quotation Memory MCP (interactive) ===\n")
    while True:
        try:
            cmd = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not cmd or cmd in ("exit", "quit"):
            break
        if cmd == "context":
            print(get_context())
        elif cmd == "checkpoint":
            print(get_checkpoint())
        elif cmd == "goals":
            print(get_goals())
        elif cmd == "rates":
            print(get_rates()[:1000])
        elif cmd.startswith("sessions"):
            parts = cmd.split()
            n = int(parts[1]) if len(parts) > 1 else 5
            print(get_recent_sessions(n))
        else:
            print(f"Unknown command: {cmd}")

def main():
    if "--interactive" in sys.argv:
        run_interactive()
    else:
        run_stdio()

if __name__ == "__main__":
    main()
