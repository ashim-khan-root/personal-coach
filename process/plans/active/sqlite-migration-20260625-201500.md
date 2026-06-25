# SQLite Migration — Implementation Plan

**Goal:** Migrate the 6 highest-churn JSON/markdown data stores to SQLite for atomicity, queryability, and reliability.

**Architecture:** Single `coach/memory/coach.db` SQLite file. Each storage domain gets its own table. A new `coach/tools/db.py` module provides the connection manager and common helpers. Existing tools get a storage backend swap — no public API changes.

**Tech Stack:** `sqlite3` (stdlib, zero deps). Raw SQL (no ORM — keeps it simple, zero deps).

---

## Phase 1 — Foundation & Insight Ledger (~30 min)

### Task 1: Create `coach/tools/db.py` — Database module

File: `coach/tools/db.py` (new)

- `get_db()` — lazy singleton connection to `coach/memory/coach.db` with `PRAGMA journal_mode=WAL`, `PRAGMA foreign_keys=ON`
- `init_db()` — create tables on first run
- Tables:
  - `schema_version` (version INTEGER)
  - `insight_events` (id INTEGER PK, event TEXT, timestamp TEXT, payload TEXT as JSON)
  - `tasks` (id TEXT PK, title TEXT, priority TEXT, status TEXT, notes TEXT, created TEXT, due TEXT)
  - `sessions` (id TEXT PK, date TEXT, skill TEXT, duration_min INTEGER, rating INTEGER, notes TEXT)
  - `session_decisions` (id INTEGER PK, session_id TEXT REFERENCES sessions(id), decision TEXT)
  - `checkpoint` (key TEXT PK, value TEXT)

### Task 2: Migrate insight_ledger.py to use SQLite

Files: `coach/tools/insight_ledger.py`, `coach/tools/db.py`

- Add `log_insight()` → INSERT into `insight_events`
- Add `query_insights()` → SELECT with optional WHERE event/since/LIMIT
- Add `get_stats()` → SELECT COUNT, GROUP BY event
- Keep same function signatures (log_insight, query_insights, get_stats)
- Add `migrate_from_json()` one-shot importer for existing `insight_ledger.json`
- Remove `json.load`/`json.dump` from insight_ledger.py
- **Verify:** `py -3 -m pytest coach/tests/test_insight_ledger.py -v`

### Task 3: Migrate task_manager.py to use SQLite

Files: `coach/tools/task_manager.py`, `coach/tools/db.py`

- `_load_tasks()` → SELECT * FROM tasks
- `_save_tasks()` → no-op (SQLite is always current)
- `add_task()` → INSERT INTO tasks
- `done_task()` → UPDATE tasks SET status='done'
- `delete_task()` → DELETE FROM tasks
- Add `migrate_from_md()` for existing tasks.md
- Remove `json.load`/`json.dump` from task_manager.py
- **Verify:** manual add/list/done/delete cycle

---

## Phase 2 — Sessions (~45 min)

### Task 4: Migrate session storage to SQLite

Files: `coach/tools/db.py`, `coach/tools/store_session.py`, `coach/tools/session_hooks.py`

- Add `sessions` and `session_decisions` tables (already in Task 1)
- `store_session.py`: write to DB instead of markdown file
- `session_hooks.py`: `load_recent_sessions()` → SELECT from DB instead of glob + parse
- Add `migrate_from_md()` for existing session-*.md files
- **Verify:** `py -3 coach/tools/session_hooks.py pre`

### Task 5: Migrate recap.py to use SQLite

Files: `coach/tools/recap.py`

- `load_recent_sessions(days)` → query sessions table instead of parsing markdown
- `load_recent_conversations()` → keep as-is (conversations stay in markdown for now)
- `load_recent_decisions()` → query session_decisions table
- **Verify:** `py -3 -m pytest coach/tests/test_recap.py -v`

### Task 6: Migrate session-dependent readers

Files: `coach/tools/extract_insights.py`, `coach/tools/weekly_synthesis.py`, `coach/tools/session_analytics.py`, `coach/tools/thinking_partner.py`, `coach/tools/mcp_server.py`, `coach/tools/read_context.py`, `coach/tools/inbox_processor.py`, `coach/tools/index_memory.py`

- Each file: replace `Path(SESSIONS_DIR).glob("session-*.md")` + parse with `db.query("SELECT ... FROM sessions")`
- Most are just replacing `load_session_files()` → `SELECT * FROM sessions WHERE date >= ?`
- **Verify:** `py -3 -m pytest coach/tests/ -v`

---

## Phase 3 — Goals, Habits, Decisions, Checkpoint (~30 min)

### Task 7: Migrate goals.md to SQLite

Files: `coach/tools/db.py`, `coach/tools/add_goal.py`, `coach/tools/read_goals.py`

- Add `goals` table (id TEXT PK, title TEXT, status TEXT, created TEXT)
- `add_goal.py`: INSERT INTO goals
- `read_goals.py`: SELECT * FROM goals
- **Verify:** `py -3 coach/tools/read_goals.py`

### Task 8: Migrate habits.md to SQLite

Files: `coach/tools/db.py`, `coach/tools/add_habit.py`, `coach/tools/read_habits.py`

- Add `habits` table (id TEXT PK, title TEXT, status TEXT, streak INTEGER, created TEXT)
- `add_habit.py`: INSERT INTO habits
- `read_habits.py`: SELECT * FROM habits
- **Verify:** `py -3 coach/tools/read_habits.py`

### Task 9: Migrate checkpoint.md to SQLite

Files: `coach/tools/db.py`, `coach/tools/write_checkpoint.py`, `coach/tools/read_checkpoint.py`

- Use existing `checkpoint` table (key-value)
- `write_checkpoint.py`: INSERT OR REPLACE INTO checkpoint
- `read_checkpoint.py`: SELECT * FROM checkpoint
- **Verify:** `py -3 coach/tools/read_checkpoint.py`

### Task 10: Migrate decisions.md to SQLite

Files: `coach/tools/db.py`, `coach/tools/store_session.py`, `coach/tools/thinking_partner.py`

- Decisions already captured in `session_decisions` table
- Standalone decisions (store_session.py appends to decisions.md): add a `decisions` table or just use new entries — align with session context
- **Verify:** store a session with decisions, confirm they're queryable

---

## Phase 4 — Cleanup (~15 min)

### Task 11: Add init_db() call to entry points

Files: `coach/tools/db.py`, `coach/memory_manager.py`, `coach/agent.py`

- `init_db()` called once at app startup
- Add migration runner that checks `schema_version` and runs incremental migrations

### Task 12: Update .gitignore and remove migrated files

- Add `coach/memory/coach.db` to `.gitignore`
- Remove archived markdown files that are fully migrated (optional, can keep as read-only legacy)

### Task 13: Verify the full test suite

```bash
py -3 -m pytest coach/tests/ -v --tb=short
```

---

## Not Migrating (staying as markdown/files)

- **Daily notes** — human-readable, edited by hand, templates matter
- **Conversations** — human-readable narrative format
- **Snapshots** — human-readable, git-like history
- **Insights / evolution suggestions** — human-reviewed, editorial workflow
- **Profile / meta / resources** — static config, rarely changed
- **Site surveys** — separate concern, markdown is fine
- **Reports (recap, weekly, analytics)** — generated output, not source of truth
- **Backups / ZIP archives** — operational, outside migration scope
- **LightRAG indices** — managed by library, format is opaque
- **Quotation system** — separate project now

---

## Rollout Strategy

1. Phases 1-4 executed in order
2. After each phase: run tests, commit
3. Keep backward compat: old markdown files aren't deleted, just ignored by readers
4. If something breaks: `db.py` can fall back to file I/O for any domain

## Migration Functions

Each domain gets a `migrate_*()` function in `db.py` that:
1. Reads all existing files
2. Inserts into SQLite
3. Returns count of migrated records

These are one-shot and can be deleted once confirmed working.
