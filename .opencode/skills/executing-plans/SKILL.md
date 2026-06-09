---
name: executing-plans
description: "Use when you have a written implementation plan to execute. Also use when the user says 'execute the plan', 'implement the plan', 'follow the plan', or when a plan file exists in process/plans/active/."
---

# Executing Plans

## Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically — identify concerns
3. If concerns: raise with user before starting
4. If OK: create TodoWrite and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete

After all tasks pass verification, report results.

## When to Stop and Ask for Help

Stop when blocked by a missing dependency, test failure, unclear instruction, or repeated verification failure.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Stop when blocked, don't guess
- Never start implementation on main/master without explicit consent
