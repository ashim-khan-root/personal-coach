# Context Router

This file is the entrypoint for loading project context. Read this first, then load only what's relevant.

## Quick Reference

| Domain | File | When to Read |
|---|---|---|
| Coach memory | `coach/memory/` (goals, habits, sessions, checkpoint, profile) | Every session start |
| Active plans | `process/plans/active/` | Before executing any task |
| Completed plans | `process/plans/completed/` | When reviewing past work |
| Skills | `.opencode/skills/<name>/SKILL.md` | When task matches keyword (see AGENTS.md skill registry) |
| DDD adversarial review | `process/context/doubt-driven-development.md` | Before risky code, migrations, or irreversible operations |
| Coaching checkpoint | `python3 coach/tools/read_checkpoint.py` | At session start |
| Session history | `python3 coach/tools/read_context.py [N]` | At session start |
| Work artifacts | `coach/work/` (content, reports, research, n8n, scripts) | When creating or reviewing deliverables |

## Context Discovery Protocol

1. **Session start**: run `python3 coach/tools/session_hooks.py pre` → checkpoint + goals + habits + last session
2. **Before any task**: check `process/plans/active/` for existing plans
3. **During task**: load the relevant skill from `.opencode/skills/` if keywords match
4. **After task**: archive plan to `process/plans/completed/` + run `python3 coach/tools/session_hooks.py post`

## Plan Lifecycle

```
User request → RESEARCH context → PLAN in process/plans/active/
→ EXECUTE → REVIEW → Archive to process/plans/completed/
```

Plans live in `process/plans/active/` while being worked on, move to `completed/` when done. Use `_template.md` for new plans.
