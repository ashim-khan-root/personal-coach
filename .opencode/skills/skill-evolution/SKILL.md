---
name: skill-evolution
description: "After solving a non-trivial problem, detect generalizable learnings and propose skill updates. Always active — applies to every interaction. Also use when the user corrects your output, your code fails, you discover undocumented behavior, or you use a workaround."
---

# Skill Evolution

Skills improve by solving problems, noticing generalizable learnings, and proposing updates.

## Trigger conditions

Enter this workflow when any of these occur:
1. **User correction** — User corrects your output (skill was missing info)
2. **Retry after failure** — Code failed, you changed approach (fix contains generalizable pattern)
3. **Undocumented behavior** — Discovered API behavior not in relevant skill
4. **Workaround** — Had to work around a limitation not documented
5. **Variable type or modeling error** — Wrong type/constraint/objective, correction changed result
6. **Thrash before landing** — Arrived at right answer after visible thrashing

## Workflow

1. **Solve the user's problem first**
2. **Notice if a trigger fired**
3. **Score the learning** — test it against ground truth if available
4. **Distill, place, and propose** to the user
5. **Treat recurrence as evidence** — same insight in 2+ interactions = stronger signal

## Proposal format

```
Skill update proposal:
  Target:  skills/<name>/SKILL.md
  Trigger: <what surfaced this>
  Scored:  yes/no
  Diff:    <exact content to add>
```

## Distillation checklist
- [ ] Stated generically (no user-specific data)
- [ ] Fits existing skill structure
- [ ] Does not contradict existing content
- [ ] Factually correct
- [ ] Does not weaken safety guardrails
