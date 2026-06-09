---
name: writing-skills
description: "Use when creating new skills, editing existing skills, or verifying skills work before deployment. Also use when the user says 'create a skill for', 'write a skill', 'add a skill', or 'make a SKILL.md'."
---

# Writing Skills

## Overview

Writing skills is Test-Driven Development applied to process documentation. Write test cases (pressure scenarios), watch them fail (baseline behavior), write the skill, watch tests pass, and refactor.

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

## SKILL.md Structure

```yaml
---
name: skill-name-with-hyphens
description: "Use when [specific triggering conditions]"
---
```

- Two required fields: `name` and `description`
- `description` starts with "Use when..." — describes ONLY when to use, NOT what it does
- Keep under 500 characters

## Claude Search Optimization

- Description = When to Use, NOT What the Skill Does
- Use concrete triggers, symptoms, situations
- Write in third person
- NEVER summarize the skill's workflow in the description

## Key Rules

- No skill without a failing test first
- One excellent example beats many mediocre ones
- Use cross-references instead of repeating content
- Keep frequently-loaded skills under 200 words
