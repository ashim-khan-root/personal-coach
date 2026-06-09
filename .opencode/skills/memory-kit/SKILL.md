---
name: memory-kit
description: "Use when you need persistent memory across sessions, multi-project context handoff, or knowledge that accumulates over time. Also use when the user starts a new session and needs to recall what was done before."
---

# Memory Kit

Persistent memory for AI agents. Four-layer architecture, agent-driven promotion, zero manual editing.

## Core invariant

**User only talks. Agent captures, proposes, writes.**

## Memory Layers

| Layer | Answers | Written by |
|---|---|---|
| `daily/YYYY-MM-DD.md` | "what happened today" | End-of-day synthesis |
| `MEMORY.md` | "what patterns repeat across sessions" | Agent during conversation |
| `knowledge/concepts/*.md` | "facts and rationale by topic" | After promotion approval |
| `rules/*.md` | "what must always/never happen" | After 6+ months stable pattern |

## Daily Workflow

1. **Open a session** — auto-load context, recent state, knowledge base
2. **Work normally** — agent captures patterns silently
3. **Close day** — agent synthesizes, audits for promotions, proposes, writes on approval

## Adaptation Notes for personal-coach

- Our `coach/memory/sessions/` map to `daily/` layer
- Our `coach/memory/checkpoint.md` maps to `MEMORY.md` hot cache
- Our `coach/tools/extract_insights.py` maps to the promotion pipeline
- Our `coach/process/plans/` map to project task tracking
