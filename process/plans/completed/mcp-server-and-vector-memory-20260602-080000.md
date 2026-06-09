---
title: "MCP Server + Vector Memory Search"
created: "2026-06-02"
status: active
phase: plan
---

## Objective

Add semantic search, MCP server integration, and LLM-powered QA to the coach, modeled after second-brain-agent's approach. This lets opencode (and any MCP client) query coach memory natively with vector embeddings instead of keyword matching.

## Approach

Four deliverables, built bottom-up. **Embeddings use TF-IDF (pure math, zero ML models)** — no neural networks, ONNX, or model downloads. Runs instantly on any CPU without stressing the system.

1. **Vector indexer** (`tools/index_memory.py`) — scans all memory files (sessions, daily notes, conversations, goals, habits, profile, insights, decisions), chunks content by file/section, builds a TF-IDF vector index via `sklearn.feature_extraction.text.TfidfVectorizer`, persists to `memory/.search_index/` (compressed pickle). Idempotent — skips unchanged files by comparing mtime. Indexes 63+ sessions in <1s.

2. **MCP server** (`tools/mcp_server.py`) — stdio-based MCP server. Exposes tools:
   - `search_memory(query, limit, filter_domain)` — TF-IDF semantic search across all memory
   - `get_recent_sessions(n)` — last N sessions with metadata
   - `get_context()` — pre-session context summary (like `session_hooks.py pre`)
   - `get_checkpoint()` — current checkpoint
   - `get_goals()` — current goals
   - Resources: `memory://sessions/recent`, `memory://checkpoint`, `memory://goals`

3. **LLM QA CLI** (`tools/ask_memory.py`) — "What did I learn about SEO last week?" → retrieves top-k chunks via TF-IDF search → displays them with source citations → optionally feeds to Ollama chat if available (graceful fallback if Ollama is busy/hanging).

4. **Auto-indexing hooks** — wire `index_memory.py` into `session_hooks.py post()` so every session store auto-refreshes the vector index.

5. **Upgrade `memory_search.py`** — try vector search first, fall back to keyword.

### Dependencies added
- `scikit-learn>=1.3.0` — TF-IDF vectorization (pure math, no GPU)
- `mcp>=1.0.0` — MCP server framework (stdio transport)
- `joblib>=1.3.0` — persist/load the TF-IDF index (comes with sklearn)

### Chunking strategy
- **Sessions**: 1 chunk per file (they're short — <50 lines)
- **Daily notes**: split by `##` sections
- **Conversations**: entire file
- **Goals/Habits/Checkpoint/Profile/Insights/Decisions**: 1 chunk per file
- Metadata per chunk: `{source: "sessions|daily|goals|...", filename: "session-...", date: "2026-06-01"}`

## Deliverables

1. `coach/tools/index_memory.py` — TF-IDF vector indexer
2. `coach/tools/mcp_server.py` — MCP server
3. `coach/tools/ask_memory.py` — LLM QA CLI (with Ollama fallback)
4. `coach/tools/memory_search.py` — upgraded to try vector first
5. `coach/requirements.txt` — updated
6. `session_hooks.py` — auto-indexing on post session

## Success Criteria

- `python tools/index_memory.py` indexes all memory in <2s
- `python tools/mcp_server.py` responds to MCP tool calls via stdio
- `python tools/ask_memory.py "SEO learnings"` returns relevant chunks
- `python tools/memory_search.py "facebook"` returns vector results first
- After `store_session.py`, vector index auto-refreshes

## Resources

- Memory references: `memory_search.py`, `session_hooks.py`, `store_session.py`
- Reference implementation: `flepied/second-brain-agent` (concept, not deps)
- TF-IDF: `sklearn.feature_extraction.text.TfidfVectorizer`
- MCP protocol: stdio JSON-RPC transport

## Notes

- Index directory: `memory/.search_index/` (gitignored)
- `.gitignore` updated to exclude `memory/.search_index/`
- Don't break existing keyword `memory_search.py` — augment it
- MCP server uses stdio transport (standard for tool integration)
