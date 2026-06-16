# Moving Personal Coach to a New PC

## Prerequisites

- Git installed
- Python 3.10+ installed
- Access to the GitHub repo

## Step-by-Step

### 1. Clone the repository

```bash
git clone https://github.com/ashim-khan-root/personal-coach.git
cd personal-coach
```

### 2. Install dependencies

```bash
pip install -r coach/requirements.txt
```

### 3. Restore memory data

```bash
python3 coach/tools/restore_memory.py
```

This pulls the latest session history, decisions, goals, habits, and daily notes from GitHub, then rebuilds the TF-IDF vector search index.

If git is unavailable, restore from the latest ZIP backup:

```bash
python3 coach/tools/restore_memory.py --from-zip
```

To list available backups:

```bash
python3 coach/tools/restore_memory.py --list
```

### 4. Start using the coach

```bash
# Load pre-session context
python3 coach/tools/session_hooks.py pre

# Or start the MCP server
python3 coach/tools/mcp_server.py
```

The `opencode.json` in the project root auto-registers the coach-memory MCP server with opencode — no manual config needed.

### 5. Verify everything works

```bash
# Check checkpoint
python3 coach/tools/read_checkpoint.py

# Check goals
python3 coach/tools/read_goals.py

# View recent sessions
python3 coach/tools/read_context.py 5

# Test memory search
python3 coach/tools/memory_search.py "solar 4G camera" --keyword
```

---

## How Backup Works

| Mechanism | Frequency | What's Saved |
|-----------|-----------|-------------|
| Git commit + push | Every session store (auto) | All files in `coach/memory/` |
| ZIP archive | Manual (`backup_memory.py`) | Full memory dir including search index |
| Git pull | Manual (`restore_memory.py`) | Latest from GitHub |

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python3 coach/tools/restore_memory.py` | Pull from git + rebuild index |
| `python3 coach/tools/restore_memory.py --from-zip` | Restore from latest ZIP |
| `python3 coach/tools/restore_memory.py --list` | Show available backups |
| `python3 coach/tools/backup_memory.py` | Git push + create ZIP |
| `python3 coach/tools/session_hooks.py pre` | Print session context |
