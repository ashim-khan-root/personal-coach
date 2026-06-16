# Doubt-Driven Development

Adversarial in-flight review for non-trivial decisions. Use before committing risky code, architectural choices, or irreversible operations.

## Trigger

A decision is **non-trivial** when it:
- Introduces branching logic or crosses a module boundary
- Asserts properties the type system can't verify (thread safety, idempotence, ordering)
- Has irreversible blast radius (production deploy, data migration, public API change)
- Depends on context a future reader won't see

## Protocol: CLAIM → EXTRACT → DOUBT → RECONCILE → STOP

### 1. CLAIM
Name the decision in 2-3 lines:
```
CLAIM: "The caching layer is thread-safe under read-heavy load."
WHY IT MATTERS: A race corrupts user data and is hard to detect in QA.
```

### 2. EXTRACT
Isolate the smallest reviewable unit — the diff, function, or proposal. Strip your reasoning. Hand the reviewer data, not conclusions.

### 3. DOUBT
Spawn a fresh-context reviewer with this adversarial prompt:
```
Adversarial review. Find what is wrong with this artifact.
Assume the author is overconfident. Look for:
- Unstated assumptions
- Edge cases not handled
- Hidden coupling or shared state
- Ways the contract could be violated
- Existing conventions this might break
- Failure modes under unexpected input

Do NOT validate or summarize. Find issues or state none found.

ARTIFACT:
CONTRACT:
```
Pass ARTIFACT + CONTRACT only. Never pass the CLAIM — it biases the reviewer.

**Cross-model escalation (interactive only):** After single-model review, ask: "Want a cross-model second opinion?" Options: Gemini CLI, Codex CLI, manual review, or skip.

### 4. RECONCILE
Classify every finding against the actual artifact text. Accept valid issues, reject false positives with evidence.

### 5. STOP
Stop when: findings become trivial/duplicative, 3 cycles completed, or user overrides.

## When NOT to use
- Renaming, formatting, file moves
- Following a clear unambiguous instruction
- One-line changes with obvious correctness
- User explicitly wants speed over verification
