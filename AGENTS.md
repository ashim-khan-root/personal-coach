# Personal Coach — Agent Instructions

## Entrypoint & run context

- **Always run commands from `coach/`** — all scripts use relative paths (`coach/agent.py`, `coach/tools/*.py`, `coach/memory/`, etc.).
- Start interactive session: `python agent.py` (from `coach/`).
- Install deps: `pip install -r requirements.txt` (requests, pyyaml, genanki).

## Tool commands (run from `coach/`)

| Command | Purpose |
|---|---|
| `python tools/read_context.py [N]` | Full memory summary (last N sessions, default 5) |
| `python tools/read_goals.py` | Print goals.md |
| `python tools/read_habits.py` | Print habits.md |
| `python tools/read_checkpoint.py` | Print current coaching checkpoint |
| `python tools/store_session.py <skill> <duration> <rating> [notes]` | Save a session entry |
| `python tools/export_anki.py [out_file]` | Export sessions with notes as Anki JSON |
| `python tools/add_goal.py "<title>" <target_date> <metric> [notes]` | Add goal |
| `python tools/add_habit.py "<title>" "<cue>" "<action>" [reward]` | Add habit |
| `python tools/write_checkpoint.py "<phase>" "<topic>" "<next_task>" [notes]` | Save checkpoint |

## Structured commands (for `agent.py` interactive mode)

- `Plan: Train <skill> to <goal> in <timeframe>.`
- `Session complete: <skill>, duration <mins>, self-rating <0-10>, notes: <...>`
- `Create Anki cards: topic <X>`
- Unstructured input falls through to free-form LLM chat.

## Config

`coach/config.yaml` — `model_type` is `local` (Ollama) or `openai`; `api_url` defaults to `http://localhost:11434/v1/chat/completions`; `model_name` defaults to `llama3`. Override with `OPENAI_API_KEY` env var.

## Memory layout (`coach/memory/`)

| File | Format |
|---|---|
| `meta.md` | YAML frontmatter: agent metadata, updated_at |
| `goals.md` | YAML list with id, title, created, target_date, metric, notes |
| `habits.md` | YAML list with id, title, cue, action, reward |
| `resources.md` | YAML list of resource groups |
| `profile.md` | User profile (YAML frontmatter + Markdown body) |
| `checkpoint.md` | Coaching checkpoint with phase, topic, next_task |
| `sessions/session-YYYYMMDD-HHMMSS.md` | Per-session YAML frontmatter (id, date, skill, duration_min, rating, notes, tags) + body |

Session files are sorted reverse-chronologically by stem.

## Skills

`coach/skills/<name>/SKILL.md` contains domain expertise. **When the user's task matches a skill domain, read the relevant SKILL.md.** Key categories: SEO/marketing (seo-audit, programmatic-seo, schema, ai-seo, content-strategy, copywriting, analytics, etc.), dev (supabase, shadcn, agent-browser, just-scrape), workflow (tdd, diagnose, triage, handoff, prototype, caveman, to-prd, to-issues, improve-codebase-architecture).

## Output directory

`coach/work/` — store generated artifacts (audits, blog posts, analyses) here.

## Workflow

1. Start session → recall what we last worked on → propose next task.
2. User completes task → store session with rating + notes.
3. After session → generate one improvement point or note for next time.
4. Remember everything — never let the user repeat context.

## No tests, no CI, no linting

Pure Python CLI app. No test framework detected. No build/typecheck step.
