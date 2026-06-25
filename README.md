# Personal Coach

An AI-powered personal coaching system that runs locally via OpenCode. Tracks sessions, decisions, goals, habits, and insights — no cloud dependency, all data stays on your machine.

## Features

- **Session tracking** — Log what you worked on, for how long, and how it went
- **Persistence** — Every session, decision, goal, and insight is stored in markdown files
- **Vector memory search** — Semantic search across all past sessions and notes
- **Insight extraction** — Auto-detects patterns, strengths, and areas for improvement
- **Skill evolution** — Clusters insights into reusable skill suggestions
- **RIPER workflow** — Research → Plan → Execute → Review for non-trivial tasks
- **Plans & goals** — Structured goal tracking with checkpoint system
- **Context window management** — Snapshot/restore for long-running sessions

## Quick Start

```bash
pip install -r coach/requirements.txt
python coach/tools/session_hooks.py pre
```

See full setup in [`coach/user-manual.md`](coach/user-manual.md).

## Tools

All tools live in [`coach/tools/`](coach/tools/):

| Tool | Purpose |
|------|---------|
| `session_hooks.py` | Pre/post session lifecycle |
| `store_session.py` | Log a completed session |
| `memory_search.py` | Vector + keyword memory search |
| `deep_research.py` | Multi-source research agent |
| `seo_audit.py` | On-page + technical SEO audit |
| `insight_ledger.py` | Event logging across tools |
| `evolve_skill.py` | Cluster insights into skill suggestions |
| `task_manager.py` | Add/list/done/delete tasks |
| `thinking_partner.py` | Socratic questioning mode |
| `daily_review.py` | End-of-day review |
| `weekly_synthesis.py` | Weekly pattern analysis |
| `site_survey.py` | Track site survey visits |
| `mcp_server.py` | MCP server for OpenCode integration |

## Project Structure

```
personal-coach/
  coach/
    tools/          # CLI tools
    memory/         # Sessions, decisions, goals, insights
    skills/         # Reusable skill definitions
    work/           # Content, reports, research
  process/
    plans/          # Active & completed implementation plans
  opencode.json     # OpenCode MCP configuration
  AGENTS.md         # Agent reference (for OpenCode)
```

## Requirements

- Python 3.11+
- Ollama (optional, for LLM-powered features like insight extraction)
- OpenCode (for interactive coaching sessions)

## License

MIT
