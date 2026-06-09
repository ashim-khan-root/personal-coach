# Personal Coach — Agent Instructions

## Run context

- **Always run commands from the project root (`personal-coach/`)** — all tools use absolute path resolution internally.
- **Python**: `py -3` on Windows (full path: `C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe`)
- Deps: `pip install -r coach/requirements.txt` (requests, pyyaml, genanki, scikit-learn, mcp, lightrag-hku, joblib, duckduckgo-search, beautifulsoup4).

## Tool commands (run from `personal-coach/` root)

| Command | Purpose |
|---|---|
| `py -3 coach/tools/read_context.py [N]` | Full memory summary (last N sessions, default 5) |
| `py -3 coach/tools/read_goals.py` | Print goals.md |
| `py -3 coach/tools/read_habits.py` | Print habits.md |
| `py -3 coach/tools/read_checkpoint.py` | Print current coaching checkpoint |
| `py -3 coach/tools/store_session.py <skill> <duration> <rating> [notes]` | Save a session entry |
| `py -3 coach/tools/export_anki.py [out_file]` | Export sessions with notes as Anki JSON |
| `py -3 coach/tools/add_goal.py "<title>" <target_date> <metric> [notes]` | Add goal |
| `py -3 coach/tools/add_habit.py "<title>" "<cue>" "<action>" [reward]` | Add habit |
| `py -3 coach/tools/write_checkpoint.py "<phase>" "<topic>" "<next_task>" [notes]` | Save checkpoint |
| `py -3 coach/tools/new_plan.py "<title>"` | Create a new plan file from template in `process/plans/active/` |
| `py -3 coach/tools/extract_insights.py [--min-confidence 0.5]` | Extract patterns from sessions into scored insights |
| `py -3 coach/tools/evolve_skill.py [--min-cluster 3] [--min-confidence 0.7]` | Cluster high-confidence insights into new skill suggestions |
| `py -3 coach/tools/session_hooks.py pre` | Print pre-session context summary (checkpoint + goals + habits + last session) |
| `py -3 coach/tools/session_hooks.py post <skill> <duration> <rating> [notes]` | Run post-session insight extraction (auto-triggered by store_session.py) |
| `py -3 coach/tools/morning_plan.py` | Show today's daily note or create from template |
| `py -3 coach/tools/morning_plan.py "brain dump..."` | Create/update today's daily note with categorized tasks |
| `py -3 coach/tools/daily_review.py` | End-of-day review: task migration, summary, inbox scan |
| `py -3 coach/tools/daily_review.py "extra notes..."` | Add notes then run daily review |
| `py -3 coach/tools/weekly_synthesis.py` | 7-day pattern analysis: wins, stalls, skill breakdown |
| `py -3 coach/tools/thinking_partner.py "problem"` | Socratic questioning mode for stuck problems |
| `py -3 coach/tools/inbox_processor.py` | Show inbox items with auto-categorization |
| `py -3 coach/tools/inbox_processor.py --auto` | Auto-organize inbox captures into sessions/tasks/goals/habits |
| `py -3 coach/tools/memory_search.py "query"` | Search across all memory files (vector search first, fallback to keyword) |
| `py -3 coach/tools/memory_search.py "query" --keyword` | Force keyword-only search |
| `py -3 coach/tools/index_memory.py` | Build/rebuild TF-IDF vector search index (auto-runs on session store) |
| `py -3 coach/tools/index_memory.py --search "query"` | Direct vector search without MCP |
| `py -3 coach/tools/index_memory.py --info` | Show index stats |
| `py -3 coach/tools/ask_memory.py "question"` | Semantic search + display relevant chunks |
| `py -3 coach/tools/ask_memory.py "question" --ask` | Same + try Ollama summarization (if available) |
| `py -3 coach/tools/mcp_server.py` | Start stdio MCP server (exposes search_memory, get_context, get_checkpoint, get_goals, get_recent_sessions, get_habits, web_search, web_fetch) |
| `py -3 coach/tools/mcp_server.py --interactive` | Interactive test mode |
| `py -3 coach/tools/recap.py [N]` | Summarize last N days (default 7) across sessions, decisions, conversations |
| `py -3 coach/tools/serve.py` | Start dev server to preview sites in browser |
| `py -3 coach/tools/serve.py --open` | Start server + auto-open browser |
| `py -3 coach/tools/serve.py /path/to/site` | Serve a specific directory |
| `py -3 coach/tools/backup_memory.py` | Git commit+push + ZIP archive of all memory |
| `py -3 coach/tools/make_quotation.py "<input>"` | AI quotation maker: "8 cameras 2MP", "3 cameras 4MP KPOI", etc. |
| `py -3 coach/tools/make_quotation.py --interactive` | Interactive chat mode for quotations |
| `py -3 coach/tools/make_quotation.py --list-rates` | Show current rate card |
| `py -3 coach/tools/make_quotation.py --update-rates <file.xlsx>` | Import new prices from Excel to rate card |
| `py -3 coach/tools/backup_memory.py --git-only` | Git commit+push only |
| `py -3 coach/tools/backup_memory.py --zip-only` | ZIP archive only |
| `py -3 coach/tools/restore_memory.py` | Restore from git (pull + rebuild index) |
| `py -3 coach/tools/restore_memory.py --from-zip` | Restore from latest ZIP backup |
| `py -3 coach/tools/restore_memory.py --from-zip <path>` | Restore from specific ZIP |
| `py -3 coach/tools/restore_memory.py --list` | List available ZIP backups |
| `py -3 coach/tools/index_memory_lightrag.py` | Build LightRAG index (falls back to TF-IDF) |
| `py -3 coach/tools/index_memory_lightrag.py --search "query"` | Search via LightRAG/TF-IDF |
| `py -3 coach/tools/index_memory_lightrag.py --info` | Show index stats |
| `py -3 coach/tools/web_search.py "query"` | Web search via DuckDuckGo (free, no API key) |
| `py -3 coach/tools/web_search.py "query" --max 20` | Web search with custom result count |
| `py -3 coach/tools/web_search.py "query" --site secuview.com` | Search within a specific domain |
| `py -3 coach/tools/web_fetch.py <url>` | Fetch and extract readable text from a URL |
| `py -3 coach/tools/web_fetch.py <url> --selector "div.content"` | Fetch only a specific CSS selector |
| `py -3 coach/tools/deep_research.py "<topic>"` | Search, fetch, compile into research brief (tries Ollama synthesis, falls back to raw) |
| `py -3 coach/tools/deep_research.py "<topic>" --max 4` | Control how many results per search variation |
| `py -3 coach/tools/deep_research.py "<topic>" --no-llm` | Skip LLM synthesis, always use raw compilation |

## LightRAG

LightRAG v1.5.1 (`pip install lightrag-hku`) provides graph-based RAG indexing.
- **Auto-fallback**: If Ollama is not running, gracefully falls back to TF-IDF.
- **Storage**: `coach/memory/.lightrag/` — vector DB + knowledge graph
- **Prerequisite**: Ollama running with `nomic-embed-text` and `llama3.2:3b` models

### Replace TF-IDF with LightRAG (when Ollama is running):
To switch `memory_search.py` to prefer LightRAG, the module provides `search_index()` with modes: `hybrid` (default), `local`, `global`, `tfidf`.

## MCP Servers (opencode.json)

The project config at `opencode.json` registers these MCP servers:

| Server | Command | Purpose |
|---|---|---|
| `n8n-mcp` | `n8n-mcp` | n8n workflow automation |
| `coach` | `py -3 coach/tools/mcp_server.py` | Personal coach memory, goals, habits, sessions |

## ECC — Everything Claude Code

ECC (`.opencode/ecc-temp/`) provides 240+ development skills, 35 commands, and specialized agents.
Skills path: `".opencode/ecc-temp/skills"` — loaded via `opencode.json`.

### Commands (via `/`)
| Command | Purpose |
|---|---|
| `/plan` | Create implementation plan |
| `/code-review` | Review code quality |
| `/security` | Security vulnerability scan |
| `/verify` | Run verification loop |
| `/learn` | Extract patterns from session |
| `/eval` | Run evaluation against criteria |
| `/checkpoint` | Save progress state |
| `/orchestrate` | Orchestrate multiple agents |
| `/evolve` | Cluster instincts into skills |

### Agents (subagent mode)
| Agent | Purpose |
|---|---|
| `planner` | Implementation planning |
| `code-reviewer` | Code quality review |
| `python-reviewer` | Python-specific review |
| `security-reviewer` | Vulnerability detection |
| `doc-updater` | Documentation updates |
| `harness-optimizer` | Config tuning |

## claude-mem

Installed at `~/.claude/plugins/marketplaces/thedotmack/plugin/`.
- Search: `npx claude-mem search <query>`
- Requires Bun runtime; start with `npx claude-mem start`

## n8n-mcp

Installed globally (`n8n-mcp@2.57.2`). Runs as stdio MCP server.
- Start: `npx n8n-mcp` (auto-managed via `opencode.json`)

## Memory layout (`coach/memory/`)

| File | Format |
|---|---|
| `meta.md` | YAML frontmatter: agent metadata, updated_at |
| `goals.md` | YAML list with id, title, created, target_date, metric, notes |
| `habits.md` | YAML list with id, title, cue, action, reward |
| `resources.md` | YAML list of resource groups |
| `profile.md` | User profile (YAML frontmatter + Markdown body) |
| `checkpoint.md` | Coaching checkpoint with phase, topic, next_task |
| `sessions/session-YYYYMMDD-HHMMSS.md` | Per-session YAML frontmatter (id, date, skill, duration_min, rating, notes, tags) + body |
| `daily/YYYY-MM-DD.md` | Daily note with brain dump, tasks, notes, session log, summary |
| `inbox/captures/` | Loose items waiting to be organized |
| `inbox/processed/` | Archived processed inbox items |
| `templates/daily-note.md` | Template for new daily notes |
| `conversations/conv-YYYYMMDD-HHMMSS.md` | Thinking partner conversation logs with key points and decisions |
| `decisions.md` | Master log of all decisions made across sessions and conversations |
| `rates.json` | Rate card data for quotation maker (camera, NVR, HDD prices) |
| `quotations/` | Generated quotation XLSX files |
| `backups/memory-backup-YYYYMMDD-HHMMSS.zip` | Timestamped ZIP backup of entire memory directory |
| `weekly-YYYY-MM-DD.md` | Weekly synthesis report |

Session files are sorted reverse-chronologically by stem.

## Skills (`.opencode/skills/`)

Skills live in `.opencode/skills/<name>/SKILL.md`. Opencode auto-loads them when
the `description` field matches the task. **64 skills installed** from:

| Source | Skills | Coverage |
|---|---|---|
| `coreyhaines31/marketingskills` | 43 | SEO, CRO, copywriting, analytics, ads, email, social, schema, pricing, referrals, onboarding, product marketing, etc. |
| `obra/superpowers` | 3 | writing-plans, executing-plans, writing-skills |
| `NVIDIA/skills` | 1 | skill-evolution (detect generalizable learnings → propose updates) |
| Adapted from `awrshift/claude-memory-kit` | 1 | memory-kit (multi-layer persistent memory architecture) |
| `ui-ux-pro-max-skill` | 1 | UI/UX design direction and creative direction |
| **Custom (local)** | **3** | **web-development, wordpress, hugo** |

ECC adds **240+ additional skills** at `.opencode/ecc-temp/skills/` covering development, testing, security, DevOps, and domain-specific workflows (Python, Rust, Go, Kotlin, C++, Java, Django, Laravel, Spring Boot, etc.).

The keyword table below is a quick reference; opencode now handles routing
via SKILL.md `description` fields automatically.

## Output directory (`coach/work/`)

Artifacts are organized into subdirectories by type:

| Directory | Content |
|---|---|
| `content/blogs/` | Published blog posts and guides |
| `content/schemas/` | PHP schema markup MU plugins |
| `content/fixes/` | On-page SEO fix copy files |
| `content/social/` | Reddit posts and social content |
| `content/facebook/` | Facebook catalog, shop guides |
| `content/drafts/` | Drafts, notes, reference files |
| `reports/` | Daily and project work reports |
| `research/` | Audits, competitor analysis, keyword research |
| `n8n/` | n8n workflow JSON exports |
| `scripts/` | Standalone scripts and tests |

## Workflow

1. Start session → run `coach/tools/session_hooks.py pre` to recall context → propose next task.
2. User completes task → `coach/tools/store_session.py` saves entry + auto-triggers `post_session` to refresh insights + auto-git-commit-and-push to GitHub.
3. Periodically run `coach/tools/extract_insights.py` (or let it auto-run after every session) to surface patterns.
4. Run `coach/tools/evolve_skill.py` when multiple insights cluster → generates skill suggestions.
5. Remember everything — never let the user repeat context.

## Daily Workflow (Morning → Evening)

### Morning: Brain Dump → Plan
```
py -3 coach/tools/morning_plan.py "email Sarah, finish report, check analytics"
```
- Creates today's daily note from template
- Auto-categorizes tasks vs notes
- Shows context: checkpoint, goals, last session

### During Day: Capture to Inbox
Drop loose thoughts into `coach/memory/inbox/captures/` as simple text files.
```
py -3 coach/tools/inbox_processor.py          # see what's there
py -3 coach/tools/inbox_processor.py --auto   # organize everything
```

### Evening: Review & Migrate
```
py -3 coach/tools/daily_review.py
```
- Marks completed tasks
- Migrates incomplete tasks to tomorrow's note
- Generates daily summary
- Shows inbox items to process

### Weekly: Pattern Check
```
py -3 coach/tools/weekly_synthesis.py
```
- Analyzes last 7 days of notes + sessions
- Shows wins, stalls, neglected areas
- Skill breakdown with session counts

### Stuck? Thinking Partner
```
py -3 coach/tools/thinking_partner.py "I don't know what to focus on"
```
- Socratic questioning mode
- Asks clarifying questions before giving answers

## Coaching Workflow Protocol (RIPER-5)

Follow this phase-locked workflow for non-trivial tasks. Each phase has strict boundaries.

| Phase | What happens | Tools allowed |
|---|---|---|
| 🔍 **RESEARCH** | Read context, checkpoint, goals, habits. Load relevant SKILL.md. Gather facts. | Read only |
| 📋 **PLAN** | Write a plan in `process/plans/active/`. Define objective, approach, deliverables, success criteria. | Read, Write (plans only) |
| ⚡ **EXECUTE** | Implement the plan. Produce deliverables. | Full access |
| 🧠 **REVIEW** | Archive plan to `process/plans/completed/`. Run `coach/tools/session_hooks.py post` to capture learnings. | Read, Write |

**Rules:**
- RESEARCH is read-only — no writing files.
- PLAN must complete before EXECUTE — ask user to review the plan first.
- After EXECUTE, always offer to archive the plan and run post-session hooks.
- **Trivial tasks** (quick answer, single command, < 5 min) skip straight to EXECUTE.
- **Fast mode**: user says "FAST MODE: <task>" → compressed RESEARCH+PLAN in one pass, still pause before EXECUTE.

## Intent Detection & Routing

When a user makes a request, detect intent and route accordingly:

| Intent | Keywords | Action |
|---|---|---|
| **Session** | "session", "practice", "study", "train", "worked on" | Load context → propose next task |
| **Feature request** | "build", "add", "create", "implement", "make" | RESEARCH → PLAN → EXECUTE → REVIEW |
| **Question** | "what", "how", "why", "where", "when" | RESEARCH (direct answer if trivial) |
| **Bug/debug** | "fix", "bug", "broken", "error", "wrong" | RESEARCH → PLAN → EXECUTE |
| **Quick task** | small change, single file, < 15 lines | EXECUTE directly |
| **Review** | "review", "audit", "check", "look at" | RESEARCH → REVIEW report |
| **Plan** | "plan", "plan for", "i want to" | Create plan in `process/plans/active/` |

**Precedence:** explicit mode command > bug/debug > feature request > question.

## Skill Registry (Quick Reference)

This table is a quick reference for available skills. Opencode now auto-loads
skills when user intent matches the SKILL.md `description` field.

| Skill | Trigger Keywords |
|---|---|
| `seo-audit` | seo, search engine, ranking, organic, google |
| `programmatic-seo` | programmatic seo, seo at scale, large site seo |
| `schema` | schema, structured data, json-ld, rich results |
| `ai-seo` | ai seo, llm, chatgpt, ai overviews, gemini |
| `content-strategy` | content strategy, editorial, content plan, blog strategy |
| `copywriting` | copy, writing, headlines, persuasive, conversion copy |
| `analytics` | analytics, ga4, tracking, metrics, data |
| `supabase` | supabase, postgres, realtime, auth, edge functions |
| `shadcn` | shadcn, ui components, radix, tailwind |
| `agent-browser` | browser automation, headless, scrape, puppeteer |
| `just-scrape` | scraping, crawl, extract data |
| `tdd` | tdd, test-first, red-green-refactor, testing |
| `diagnose` | diagnose, debug, root cause, troubleshoot |
| `triage` | triage, prioritize, what to work on, backlog |
| `handoff` | handoff, context switch, resume, status |
| `prototype` | prototype, poc, proof of concept, mvp |
| `caveman` | caveman, dumb it down, simple explanation |
| `to-prd` | prd, product spec, requirements doc |
| `to-issues` | issues, tickets, github issues, tasks |
| `improve-codebase-architecture` | architecture, refactor, restructure, tech debt |
| `competitor-profiling` | competitor, competitive analysis, market research |
| `pricing` | pricing, pricing strategy, monetization, tiers |
| `launch` | launch, go-to-market, gtm, distribution, ship |
| `cro` | conversion, cro, a/b test, optimize, funnel |
| `site-architecture` | site architecture, sitemap, information architecture, navigation |
| `referrals` | referral, viral, word of mouth, share |
| `marketing-psychology` | psychology, persuasion, triggers, behavioral |
| `directory-submissions` | directory, citations, local seo, listings |
| `web-development` | html, css, javascript, build website, create site, landing page code, frontend, responsive, web page, static site, single page app |
| `wordpress` | wordpress, woocommerce, wp theme, plugin, elementor, wp admin, functions.php, yoast, rankmath, custom post type, acf |
| `hugo` | hugo, hugo theme, hugo templates, hugo layouts, hugo shortcodes, hugo config, hugo.toml, static site generator, hugo deployment, github pages hugo |
| `deep-research` | research, deep dive, investigate, competitive research, market research, literature review, fact check |
| `n8n-workflows` | n8n, n8n workflow, automation, workflow automation, zapier, make, webhook, api integration |
| `kaizen` | kaizen, continuous improvement, process optimization, eliminate waste, lean, streamline |
| `ship-learn-next` | what to work on next, prioritize tasks, decide next step, what did i learn, feedback loop |
| `domain-brainstormer` | domain name, find a domain, check domain availability, website name, brand name |
| `lead-research` | find leads, prospect research, lead generation, identify prospects, b2b leads |
| `frontend-design` | premium design, not generic, stand out visually, modern ui, beautiful interface, design system |
| `d3-visualization` | d3, chart, graph, data visualization, interactive chart, dashboard, visualize data |
| `excalidraw-diagrams` | diagram, architecture diagram, system design, flowchart, wireframe, excalidraw |
| `competitive-ads` | competitor ads, ad spy, facebook ads library, google ads transparency, ad creative research |
| `brand-voice` | brand voice, tone of voice, writing style, brand personality, consistent tone |
| `xlsx-master` | excel, spreadsheet, csv, xlsx, data analysis, pivot table, financial model, product catalog |

## Plan Lifecycle

Plans are stored in `process/plans/` with three subdirectories:

| Directory | Purpose |
|---|---|
| `active/` | Plans currently being worked on |
| `completed/` | Archived after REVIEW phase |
| `backlog/` | Deferred or future plans |

**To create a plan:** run `py -3 coach/tools/new_plan.py "<title>"` from `personal-coach/`.
**Naming convention:** `plan-title-YYYYMMDD-HHMMSS.md`
**Context router:** `process/context/all-context.md` — read first at session start.

## Blog Writing Convention (Secuview)

Whenever writing a blog post, ALWAYS include this RankMath-optimized block at the top of the file:

```yaml
---
# RankMath SEO
rankmath_title: "Primary Keyword | Secondary Keyword - Secuview Qatar"
rankmath_description: "160-char meta description with primary keyword, CTA, and location. Ends with period."
rankmath_permalink: /blog/keyword-rich-slug/
rankmath_focus_keyword: "primary keyword"
rankmath_related_keywords: [keyword1, keyword2, keyword3]
---
```

Rules:
- **Title**: 50-60 chars, front-load primary keyword, include "Qatar" and/or "Secuview"
- **Description**: 150-160 chars, include keyword + CTA + location, end with period
- **Permalink**: lowercase, hyphens, target keyword only (no stop words)
- **Content**: H2/H3 structure, FAQ section at bottom, internal links to product categories, Qatar-specific (pricing, climate, vendors)

## No tests, no CI, no linting

Pure Python CLI app. No test framework detected. No build/typecheck step.
