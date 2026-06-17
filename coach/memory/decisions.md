# Decisions Log

All decisions made during sessions, thinking partner conversations, and planning.
Format: `## [date] — [topic]`

---


## 2026-05-31 — coach-system-upgrade (session)
- Upgraded coach from 8.5/10 to 10/10

## 2026-05-31 — skill-development (session)
- Expanded from 48 to 63 skills covering marketing, coding, design, research

## 2026-05-31 — automation-setup (session)
- Daily auto-push to GitHub at 4:50 PM

## 2026-06-09 — prompt-enhance-protocol (session)
- `--prompt enhance` suffix on any command means: rephrase/enhance user's intent first, show it, then proceed.
- Without `--prompt enhance`, take input literally (current behavior).

## 2026-05-31 — secuview-schema-markup (session)
- All 4 schema types ready for upload

## 2026-06-02 — coach-vector-memory (session)
- Added TF-IDF vector search index (zero ML models, pure math)
- Built MCP server exposing coach memory over stdio protocol
- Built ask_memory.py CLI for semantic search + optional Ollama QA
- memory_search.py now tries vector search first, falls back to keyword
- Auto-indexing on every session store

## 2026-06-02 — coach-improvement (session)
- Proactively prompt user for 15-min prompt engineering drills during lulls
---\ndate: 2026-06-05T22:13:00+03:00\ndecision: Start building a business/classified listing website for Qatar\ncontext: User wants financial freedom, a full side business alongside current job\napproach: Build website first, then promote via WhatsApp and Facebook\ncompetitor_strategy: Find gaps in existing classified sites (mzadqatar, qatarliving, qatarclassifieds) and outperform\ntags: [business, qatar, classifieds, entrepreneurship]\n---

## 2026-06-16 — research (session)
- Evaluated addyosmani/agent-skills repo (60k stars). Reviewed DDD, Context Engineering, Source-Driven Development skills. Decided to distill only Doubt-Driven Development — cherry-picked CLAIM→EXTRACT→DOUBT→RECONCILE→STOP protocol into process/context/doubt-driven-development.md. Skipped the other two (redundant or too narrow). Added reference to context router.

## 2026-06-16 — skill-evolution (session)
- Created insight_ledger.py as foundation for all tool instrumentation. Every new tool should call log_insight() after its main flow.

## 2026-06-17 — coach-2.0-powersuite (session)
- Decided to implement "Power Suite" (repo_map, autofix, lead_gen, content_factory, debate) to move towards Level 3/4 autonomy.
- Switched to AST-based Repo-Maps for context efficiency.
- Adopted "Self-Healing" pattern (autofix) for faster development loops.
