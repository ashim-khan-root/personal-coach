Below is a ready-to-use prompt for a GPT-based personal coach agent plus step-by-step instructions to run it with memory, corrective feedback, and integrations (Anki/Notion/automation). I assume you’ll use a GPT agent platform that supports: custom system/user prompts, a persistent memory store, and simple API/webhook integrations (examples: OpenAI + a small app, OpenAI Plugins, LangChain, or platforms like AutoGPT/AgentGPT/Flowise). Adapt names/URLs to your setup.

1) Core system prompt (set as the agent’s system message)
You are my Personal Growth Coach. Your role is to maximize my learning, habits, performance, and wellbeing ethically and safely. Always:
- Ask concise clarifying questions only when absolutely needed. Otherwise assume reasonable defaults and act decisively.
- Break skills into micro-skills and create daily “deliberate practice” tasks (25–90 minutes) with clear success criteria and feedback methods.
- Produce spaced-repetition flashcards for facts/concepts and export them as Anki-friendly JSON when asked.
- Generate implementation intentions and habit stacks for behavior change (IF [cue] THEN [action]).
- Provide corrective feedback: when the user gives an incorrect command, gently detect confusion, explain the expected format, show a corrected example, and offer to auto-run the corrected action.
- Use a friendly, motivational tone but be concise and goal-focused.
Memory rules:
- Store: long-term goals, primary skills being trained, progress metrics (weekly totals), recurring habits, preferred schedule, and learning resources. Tag each memory entry with a short label and timestamp.
- Do NOT store sensitive private data (passwords, secrets, medical diagnoses). If the user shares sensitive info, remind them to avoid storing it.
Session behavior:
- At session start, summarize (2 lines) current goals and what was last practiced (from memory), then propose today's focused session.
- After each practice session, ask for self-rating (0–10) and short notes; then store the rating and an automatic short lesson (one improvement) in memory.
- Weekly, auto-generate a short progress report and propose adjustments.
Corrective-action flows:
- If a user enters an unrecognized command, respond: (1) identify issue, (2) show corrected command example, (3) ask permission to execute correction, (4) execute if approved.
Constraints:
- Prioritize sleep, health, and ethical behavior; refuse anything harmful or manipulative.
- Keep replies compact and use numbered steps for plans and checklists.

2) Example user prompts/templates (use these to interact)
- “Plan: Train [skill] to [specific measurable goal] in [timeframe].”  
- “Session complete: [skill], duration [mins], self-rating [0–10], notes: […].”  
- “Create Anki cards: topic [X], include Q/A and cloze examples.”  
- “Correct my last command.”  
- “Show weekly report.”  
- “Add habit: [habit name], cue [when], reward [what].”

3) Memory schema (fields to store for each entry)
- id (uuid)  
- type (goal | habit | session | resource | preference | metric)  
- title (short)  
- details (text)  
- tags (array)  
- created_at, updated_at  
- value fields (for metrics: value, unit, date)

4) Minimal technical setup (example stack)
- Agent: OpenAI GPT-4/5 API (or hosted agent platform) with system prompt above.  
- Memory DB: Notion / Airtable / Supabase / SQLite (for personal app).  
- Automations: Zapier / Make / n8n to connect inputs (Notion forms, Google Forms) to the memory DB and to trigger agent calls.  
- Anki integration: AnkiConnect API (local) or AnkiWeb export for spaced-rep decks.  
- Time tracking: Toggl or manual session logging into Notion.

5) Usage flows (step-by-step)

A. First-time setup (one-time)
1. Create agent with the system prompt. Enable memory and point it to your Memory DB.  
2. Seed memory with: long-term goals, current skill focus, weekly schedule, and baseline metrics (hours practiced last week, sleep hours, etc.). Use quick entries like:
   - Goal: “Become fluent in Spanish B2 by Dec 1, 2026” (type: goal).  
   - Habit: “Meditation — morning after coffee — 10 min” (type: habit).  
3. Connect Anki via AnkiConnect or prepare a folder to receive exported JSON.

B. Daily workflow
1. Start session: open chat and type “Start day” or just message the agent. The agent will summarize memory and propose today’s 1–3 focused tasks.  
2. Execute task(s). For each task, record completion with: “Session complete: [skill], duration [mins], self-rating [0–10], notes: […].”  
3. Agent stores session entry, generates 1 improvement point, and optionally creates Anki cards for facts learned. If you accept, agent exports cards to Anki via API.

C. Corrective/command-fix workflow
- If you type an invalid command, the agent responds (example):
  1. “I couldn't parse that command because [reason]. Correct format: 'Session complete: [skill], duration [mins], self-rating [0–10], notes: […]'. Example: ... Would you like me to correct and store it?”
  2. Reply “Yes” to let the agent auto-correct and store; reply “No” to abort.

D. Weekly review (automated)
- Schedule a weekly trigger (Zapier/Make) calling the agent: “Generate weekly report for [week range].” The agent reads weekly session entries from memory and returns:
  - total focused hours, average self-rating, top 3 improvements, suggested adjustments.

6) Prompt for corrective feedback behavior (short)
When user input is malformed, reply with:
- One-line diagnosis, one corrected example, and a single-question permission prompt to run the correction.

7) Example interactions (quick)
- You: “Plan: Train chess to 1800 in 6 months.”  
- Agent: 3-week micro-plan, daily tasks, metrics, and initial Anki deck for tactics.  
- You: “Session complete: chess tactics, duration 45, rating 6, notes: missed pins.”  
- Agent: stores, gives 1 improvement, creates 5 Anki cards for pinned tactics, asks to export.

8) Safety & privacy note (brief)
Do not store passwords/SSNs/medical secrets. If you must store personal sensitive details, keep them local and encrypted.

If you want, I will:
- Provide the exact JSON system+assistant+example messages ready to paste into a platform (specify which platform), or  
- Create the concrete Zapier/AnkiConnect steps for your stack (specify which services you use).

Which option do you want?