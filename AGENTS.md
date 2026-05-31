# Personal Coach — Agent Instructions

## Run context

- **Always run commands from `coach/`** — all scripts use relative paths (`coach/tools/*.py`, `coach/memory/`, etc.).
- The user talks to me (opencode) directly. `agent.py` is deprecated.
- Install deps: `pip install -r requirements.txt` (requests, pyyaml, genanki).

## Tool commands (run from `coach/`)

| Command | Purpose |
|---|---|
| `python3 tools/read_context.py [N]` | Full memory summary (last N sessions, default 5) |
| `python3 tools/read_goals.py` | Print goals.md |
| `python3 tools/read_habits.py` | Print habits.md |
| `python3 tools/read_checkpoint.py` | Print current coaching checkpoint |
| `python3 tools/store_session.py <skill> <duration> <rating> [notes]` | Save a session entry |
| `python3 tools/export_anki.py [out_file]` | Export sessions with notes as Anki JSON |
| `python3 tools/add_goal.py "<title>" <target_date> <metric> [notes]` | Add goal |
| `python3 tools/add_habit.py "<title>" "<cue>" "<action>" [reward]` | Add habit |
| `python3 tools/write_checkpoint.py "<phase>" "<topic>" "<next_task>" [notes]` | Save checkpoint |
| `python3 tools/new_plan.py "<title>"` | Create a new plan file from template in `process/plans/active/` |
| `python3 tools/extract_insights.py [--min-confidence 0.5]` | Extract patterns from sessions into scored insights |
| `python3 tools/evolve_skill.py [--min-cluster 3] [--min-confidence 0.7]` | Cluster high-confidence insights into new skill suggestions |
| `python3 tools/session_hooks.py pre` | Print pre-session context summary (checkpoint + goals + habits + last session) |
| `python3 tools/session_hooks.py post <skill> <duration> <rating> [notes]` | Run post-session insight extraction (auto-triggered by store_session.py) |
| `python3 tools/morning_plan.py` | Show today's daily note or create from template |
| `python3 tools/morning_plan.py "brain dump..."` | Create/update today's daily note with categorized tasks |
| `python3 tools/daily_review.py` | End-of-day review: task migration, summary, inbox scan |
| `python3 tools/daily_review.py "extra notes..."` | Add notes then run daily review |
| `python3 tools/weekly_synthesis.py` | 7-day pattern analysis: wins, stalls, skill breakdown |
| `python3 tools/thinking_partner.py "problem"` | Socratic questioning mode for stuck problems |
| `python3 tools/inbox_processor.py` | Show inbox items with auto-categorization |
| `python3 tools/inbox_processor.py --auto` | Auto-organize inbox captures into sessions/tasks/goals/habits |
| `python3 tools/memory_search.py "query"` | Search across all memory files for context |
| `python3 tools/recap.py [N]` | Summarize last N days (default 7) across sessions, decisions, conversations |
| `python3 tools/decisions.md` | Decisions log (read/write manually or via store_session.py --decision) |
| `python3 tools/serve.py` | Start dev server to preview sites in browser |
| `python3 tools/serve.py --open` | Start server + auto-open browser |
| `python3 tools/serve.py /path/to/site` | Serve a specific directory |

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
| `weekly-YYYY-MM-DD.md` | Weekly synthesis report |

Session files are sorted reverse-chronologically by stem.

## Skills (`.opencode/skills/`)

Skills live in `.opencode/skills/<name>/SKILL.md`. Opencode auto-loads them when
the `description` field matches the task. **63 skills installed** from:

| Source | Skills | Coverage |
|---|---|---|
| `coreyhaines31/marketingskills` | 43 | SEO, CRO, copywriting, analytics, ads, email, social, schema, pricing, referrals, onboarding, product marketing, etc. |
| `obra/superpowers` | 3 | writing-plans, executing-plans, writing-skills |
| `NVIDIA/skills` | 1 | skill-evolution (detect generalizable learnings → propose updates) |
| Adapted from `awrshift/claude-memory-kit` | 1 | memory-kit (multi-layer persistent memory architecture) |
| **Custom (local)** | **3** | **web-development, wordpress, hugo** |

The keyword table below is a quick reference; opencode now handles routing
via SKILL.md `description` fields automatically.

## Output directory (`coach/work/`)

Artifacts are organized into subdirectories by type:

| Directory | Content |
|---|---|
| `content/` | Blog posts, articles, marketing copy |
| `reports/` | Daily and project work reports |
| `research/` | Audits, competitor analysis, keyword research |
| `n8n/` | n8n workflow JSON exports |
| `scripts/` | Standalone scripts and tests |

## Workflow

1. Start session → run `session_hooks.py pre` to recall context → propose next task.
2. User completes task → `store_session.py` saves entry + auto-triggers `post_session` to refresh insights.
3. Periodically run `extract_insights.py` (or let it auto-run after every session) to surface patterns.
4. Run `evolve_skill.py` when multiple insights cluster → generates skill suggestions.
5. Remember everything — never let the user repeat context.

## Daily Workflow (Morning → Evening)

### Morning: Brain Dump → Plan
```
python tools/morning_plan.py "email Sarah, finish report, check analytics"
```
- Creates today's daily note from template
- Auto-categorizes tasks vs notes
- Shows context: checkpoint, goals, last session

### During Day: Capture to Inbox
Drop loose thoughts into `memory/inbox/captures/` as simple text files.
```
python tools/inbox_processor.py          # see what's there
python tools/inbox_processor.py --auto   # organize everything
```

### Evening: Review & Migrate
```
python tools/daily_review.py
```
- Marks completed tasks
- Migrates incomplete tasks to tomorrow's note
- Generates daily summary
- Shows inbox items to process

### Weekly: Pattern Check
```
python tools/weekly_synthesis.py
```
- Analyzes last 7 days of notes + sessions
- Shows wins, stalls, neglected areas
- Skill breakdown with session counts

### Stuck? Thinking Partner
```
python tools/thinking_partner.py "I don't know what to focus on"
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
| 🧠 **REVIEW** | Archive plan to `process/plans/completed/`. Run `session_hooks.py post` to capture learnings. | Read, Write |

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

**To create a plan:** run `python tools/new_plan.py "<title>"` from `coach/`.
**Naming convention:** `plan-title-YYYYMMDD-HHMMSS.md`
**Context router:** `process/context/all-context.md` — read first at session start.

## No tests, no CI, no linting

Pure Python CLI app. No test framework detected. No build/typecheck step.
