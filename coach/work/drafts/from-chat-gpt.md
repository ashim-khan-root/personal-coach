## Modular serialized-agent implementation checklist

### 1. Core architecture (modules)
- Agent registry (discovery + metadata)
- Router/selector (intent classifier → agent mapping)
- Shared services: auth, storage, logging, rate-limit, telemetry
- Memory manager (short-term & long-term)
- Prompt manager (templates, versions, prompt chains)
- RAG layer (vector DB, retriever, document indexer)
- Action executor (connectors, sandboxed side-effects)
- Safety & validation layer (policy checks, veto, human escalation)
- Config & feature-flag service
- CI/CD, monitoring, and rollback

### 2. Serialization format & versioning
- Use JSON Lines or protocol buffers for serialized agent packages.
- Package fields:
  - id, version, created_at, compatible_model_versions
  - intent_signatures (list of example utterances, intents)
  - capabilities (actions, integrations)
  - prompt_templates (named templates with version)
  - memory_schema (fields, retention_policy)
  - permissions_required (scopes)
  - connector_manifests (endpoints, auth types)
  - safety_policies (blocklist, allowed_content_flags)
  - metrics_spec (events to emit)
  - ui_hints (tone, persona, suggested_responses)
- Semantic versioning and migration scripts for schema changes.

### 3. Agent registry & discovery
- Store packages in DB + object store for binaries.
- Index by intent_signatures, capabilities, tags, and metadata.
- Provide API: register, update, deactivate, fetch-by-intent, fetch-by-id.
- On registration validate schema and run safety/static checks.

### 4. Router / auto-picker
- Intent classifier (fine-tuned model or ensemble) → returns top-N agents with confidence.
- Rules engine fallback (priority rules, frequency, user prefs).
- Selection policy:
  - If confidence > high_threshold → pick top agent.
  - If confidence in mid_range → combine agents or ask short clarifying question.
  - If multi-capability needed → compose agents using orchestrator.
- Cache selection results per session.

### 5. Memory manager
- Short-term session context (token-limited, ephemeral).
- Long-term memory with typed entries per agent (user_profile, preferences, projects, contacts).
- Memory operations: read, write, summarize, redact, expire, export.
- User controls UI: list memories, delete, correct, export.
- Encryption at rest + access-scoped keys per agent.

### 6. Prompt & chain manager
- Store named prompt templates with placeholders and constraints.
- Support prompt chaining, verifiers, and grounding steps.
- Template parameters bound from memory + retrieval results.
- Prompt caching & A/B variant testing metadata.
- Versioned prompt rollback.

### 7. Retrieval-Augmented Generation (RAG)
- Ingest pipelines: parsers for docs, code, emails, website content.
- Vector DB with per-agent namespaces + periodic reindex job.
- Retriever config per agent: k, rerankers, chunking strategy.
- Include provenance metadata and snippet citations in responses.

### 8. Action executor & connectors
- Connector manifest pattern with OAuth/JWT support and fine-grained scopes.
- Execute actions in sandboxed worker with quotas and dry-run mode.
- Preflight checks and confirmation requirements for destructive or sensitive actions.
- Transaction logs and reversible operations where possible.

### 9. Safety, compliance & validation
- Static policy checks on prompts and agent package (blocklist, allowed intents).
- Runtime content filters and hallucination detectors.
- Confidence thresholds and human-in-loop escalation channels.
- Audit logs for decisions, actions, and data accesses.
- Compliance hooks for consent, data deletion, and regional regulation flags.

### 10. Testing & QA
- Unit tests for prompt templates, serializers, and connectors.
- Integration tests: intent→agent flow, memory ops, RAG retrieval.
- Adversarial tests for prompt injection, data exfiltration, escape sequences.
- CI checks for package publishing with safety gates.

### 11. Deployment & lifecycle
- Feature flags and canary rollouts for new agent versions.
- Migration scripts for memory_schema changes.
- Backwards compatibility policy and deprecation window.
- Health checks, metrics (latency, error, hallucination rate), and alerting.

### 12. Observability & metrics
- Telemetry events: intent_detected, agent_selected, prompt_sent, action_executed, safety_blocked, user_feedback.
- Per-agent dashboards: usage, success rate, average response time, cost.
- Periodic audits for bias, failure modes, and privacy leaks.

### 13. UX & user controls
- Minimal onboarding for agent permissions and capabilities.
- Inline persona & capability card when an agent is auto-picked.
- Easy undo, confirm dialogs for side-effects.
- Memory management UI and privacy controls.

### 14. Data model examples (concise)
- Agent package (JSON): id, version, intents[], capabilities[], prompt_templates{}, memory_schema{}, connectors[]
- Memory entry: id, agent_id, user_id, type, content, summary, created_at, expires_at, source
- Intent detection record: utterance, detected_intent, confidence, top_agents[]

### 15. Prompt templates (examples)
- System: agent role, constraints, allowed_actions
- User: user message + explicit expected output schema (JSON)
- Verifier: checklist to validate critical facts and required fields

### 16. Security & keys
- Per-connector scoped credentials with rotation.
- KMS-backed encryption keys for long-term memory.
- Least-privilege IAM roles for workers and services.

### 17. Cost & performance optimizations
- Mixed-model routing (small model for intent, medium for RAG, large for complex reasoning).
- Response caching, prompt token trimming, and async background tasks for heavy ops.
- Batched retrievals and connector calls.

### 18. Example workflows (high-level)
- Personal coach: detect goal intent → fetch goals+habits memory → plan using planning template → schedule tasks via calendar connector (confirm before write).
- Coding buddy: detect code intent → RAG on codebase namespace → generate patch + run static checks → present diff + run test suggestion.
- Website builder: detect feature request → retrieve site schema + assets → scaffold code via template → dry-run deploy to staging connector.
- Mental-health coach: prioritize safety flow → restrict to supportive content, surface crisis resources, escalate to human if risk detected, store only anonymized session flags.

### 19. Documentation & onboarding
- Developer docs: package spec, connector guide, prompt authoring rules.
- Internal runbook: incident response, rollback, and escalation.
- User-facing docs: agent capabilities, memory controls, and data handling.

### 20. Prioritized rollout checklist
1. Define agent package schema and registry.
2. Implement intent classifier + basic router.
3. Build prompt manager + simple memory store.
4. Add RAG with vector DB and retriever.
5. Implement connector sandbox and confirm flows.
6. Add safety validation and CI gates.
7. Launch alpha with telemetry + feature flags.
8. Iterate with user feedback and expand agents.
