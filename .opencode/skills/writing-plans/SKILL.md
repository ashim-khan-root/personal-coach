---
name: writing-plans
description: "Use when you have a spec or requirements for a multi-step task, before touching code. Also use when the user asks for a plan, implementation plan, task breakdown, or step-by-step approach for a non-trivial feature or change."
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

**Save plans to:** `process/plans/active/<plan-name-YYYYMMDD-HHMMSS.md>`

## Bite-Sized Task Granularity

Each step is one action (2-5 minutes).

## Plan Document Header

```
# [Feature Name] Implementation Plan

**Goal:** [One sentence]

**Architecture:** [2-3 sentences]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

- Each task has create/modify file list
- Steps use checkbox syntax
- Every step must contain actual code/content — no placeholders

## No Placeholders

Never write: "TBD", "TODO", "implement later", "fill in details", "add error handling" (without showing how).

## Self-Review

After writing the plan, check spec coverage, scan for placeholders, verify type consistency across tasks.

## Execution Handoff

After saving, offer: Subagent-driven (recommended) vs inline execution.
