# Personal Coach — User Manual

## How This Works

You talk to me (opencode), I track everything in `coach/memory/`. Every session, decision, goal, and habit is persisted. I never make you repeat context.

```
You: "good morning"
  Me: checks checkpoint + goals + last session → proposes next task
You: works for 2 hours
  Me: logs session, extracts insights, refreshes search index
```

---

## Your Daily Rhythm

### Morning (30s)
```bash
python3 coach/tools/morning_plan.py "brain dump here"
# or just say "morning" — I'll run it
```
I show checkpoint, goals, last session. You dump tasks.

### During Day
- Say what you're working on — I'll suggest next steps
- Stuck? Say `"thinking partner: <problem>"` — Socratic mode
- Quick memory: `"what did I learn about SEO?"` — I search automatically

### Evening (1 min)
```bash
python3 coach/tools/daily_review.py
```
I migrate unfinished tasks, generate summary, check inbox.

### Weekly (5 min)
```bash
python3 coach/tools/weekly_synthesis.py
```
Pattern analysis: wins, stalls, neglected areas, skill breakdown.

---

## How to Talk to Me

| Say this | I do |
|---|---|
| `"morning"` / `"start session"` | Pre-session context + propose next task |
| `"worked on X for 2 hours"` | Ask for rating + notes → store session |
| `"thinking partner: I'm stuck on X"` | Socratic questioning |
| `"what did I learn about X?"` | Vector search memory → show relevant results |
| `"plan: <task>"` | Research → write plan → ask approval → execute |
| `"review my week"` | Weekly synthesis |
| `"what's on my plate?"` | Show checkpoint + active plans |
| `"capture: <note>"` | Add to inbox for later processing |

### For Sessions — Say This Format
```
"worked on seo-optimization for 45 minutes, rating 8"
"practiced content-writing 2 hours, rating 9, wrote 3 blog posts"
"session: python 30min 7 finished the scraper script"
```

If you just say `"session: X"` I'll ask for the rest.

---

## The RIPER Workflow (for Non-Trivial Tasks)

For anything bigger than a quick answer:

1. **Research** — I read context, goals, plans (read-only)
2. **Plan** — I write a plan, you approve
3. **Execute** — I build it
4. **Review** — I archive plan, log decisions, capture learnings

Just say `"plan: <what you want>"` to start. For small things, I skip straight to execute.

---

## Context You Never Need to Repeat

| Stored in | Examples |
|---|---|
| `checkpoint.md` | Current phase, topic, next task |
| `goals.md` | 4 goals with targets and metrics |
| `profile.md` | Your role, skills, projects, training roadmap |
| `decision.md` | Every decision ever made |
| `sessions/` | 63+ sessions with ratings and notes |
| `insights.md` | Auto-extracted patterns and strengths |

I read these automatically at every session start.

---

## Tools Quick Reference

```bash
# Start/end
python3 coach/tools/session_hooks.py pre          # start context
python3 coach/tools/store_session.py <skill> <min> <rating> [notes]

# Memory search
python3 coach/tools/memory_search.py "query"       # vector + keyword
python3 coach/tools/ask_memory.py "question"        # search with context
python3 coach/tools/index_memory.py --info          # show index stats

# Daily workflow
python3 coach/tools/morning_plan.py "brain dump"
python3 coach/tools/daily_review.py
python3 coach/tools/weekly_synthesis.py
python3 coach/tools/inbox_processor.py --auto

# Coaching
python3 coach/tools/thinking_partner.py "problem"
python3 coach/tools/recap.py 7
```

---

## Tips for Best Results

1. **Rate honestly** — 10/10 every time hides what's actually hard. A 6/10 with honest notes is more valuable.
2. **Notes matter** — "SEO work on product pages" is ok. "Added alt text to 20+ images, fixed meta descriptions on 15 product pages, saw 12% CTR improvement" is gold.
3. **Capture decisions** — When you decide something, say "decided to X" in your session notes. I auto-log it.
4. **Checkpoint is your compass** — If you're not sure what to work on, just say "what should I do next?" and I'll read it.
5. **No overthinking** — Just start working. I track the rest.

---

## File Locations

```
personal-coach/                    # workspace root
  coach/
    tools/                         # 21 CLI tools
    memory/                        # all your data
      sessions/                    # practice logs
      daily/                       # daily notes
      .search_index/               # vector search (auto-built)
    work/
      content/blogs/               # published content
      reports/                     # work reports
      research/                    # audits, keyword research
  process/
    plans/active/                  # plans in progress
    plans/completed/               # finished plans
  opencode.json                    # MCP config
  AGENTS.md                        # full reference
```
