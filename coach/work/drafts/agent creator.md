Below is a compact, model-agnostic implementation plan with open-source code examples you can run locally. It uses a simple agent loop, a local "memory" stored as Markdown files, and is compatible with any LLM (local or remote) that exposes a chat/completion API. I include:

- file structure
- system prompt (agent behavior)
- Python code (agent loop, memory read/write in MD, Anki export stub)
- how memory is organized so agent quickly loads context on start
- how to handle corrective-feedback and command parsing
- run instructions

You can copy-paste and adapt for your LLM (OpenAI, local Llama.cpp/ggml endpoints, etc.).

File structure (local project)
- coach/
  - agent.py
  - prompts.py
  - memory/
    - meta.md
    - goals.md
    - habits.md
    - sessions/ (folder of session-YYYYMMDD-HHMM.md)
    - resources.md
  - anki_export.py
  - config.yaml
  - requirements.txt
  - README.md

System prompt (short, put in prompts.py)
- Role: Personal Growth Coach. Maximize learning, habits, performance ethically. Ask clarifying questions only when needed. Break skills into micro-skills, produce daily deliberate-practice tasks with success criteria, generate spaced-rep cards, store and use memory from local MD files (see schema). On unrecognized commands: identify issue, show corrected command example, ask permission to execute correction. At session start: summarize goals & last practice (2 lines) and propose today’s tasks. After sessions: ask self-rating (0–10) and notes, store session, produce one improvement. Weekly: auto-generate short report and suggested changes. Refuse harmful requests. Keep replies concise, numbered steps.

Memory format (local Markdown)
- meta.md (agent metadata, updated_at)
- goals.md (YAML frontmatter or bullet list). Example:
  - id: goal-1
    title: "Spanish B2 by 2026-12-01"
    created: 2026-05-20
    target_date: 2026-12-01
    metric: "CEFR B2"
    notes: "Study 5h/week"
- habits.md (list with cue/action/reward)
- sessions/ session files named session-20260520-0900.md with frontmatter:
  ---
  id: session-uuid
  date: 2026-05-20T09:00
  skill: chess tactics
  duration_min: 45
  rating: 6
  notes: "missed pins"
  tags: [tactics, chess]
  ---
  (agent_summary and one improvement lines after)

Agent loads memory by reading these MD files and building a short context summary (max tokens) to send to the model each run.

agent.py (minimal, replace MODEL_CALL with your LLM call)
```python
# agent.py
import os, yaml, json, uuid, datetime
from prompts import SYSTEM_PROMPT, START_PROMPT
from pathlib import Path

MEM_DIR = Path("memory")
SESS_DIR = MEM_DIR/"sessions"
SESS_DIR.mkdir(parents=True, exist_ok=True)

def read_md(file):
    if not file.exists(): return ""
    return file.read_text(encoding="utf-8")

def load_memory_summary(max_items=10):
    # load goals, habits, recent sessions summarised
    goals = read_md(MEM_DIR/"goals.md")
    habits = read_md(MEM_DIR/"habits.md")
    sessions = sorted(SESS_DIR.glob("session-*.md"), reverse=True)[:max_items]
    recent = []
    for s in sessions:
        txt = read_md(s).splitlines()[:8]
        recent.append("\n".join(txt))
    summary = f"GOALS:\n{goals}\n\nHABITS:\n{habits}\n\nRECENT SESSIONS:\n" + "\n\n".join(recent)
    # truncate if needed
    return summary[:3000]

def call_model(system, user, model="gpt-5-mini"):
    # Replace this function with your model API call
    # Should return model's text reply
    raise NotImplementedError("Implement MODEL_CALL for your LLM here")

def start_session():
    mem_summary = load_memory_summary()
    user_msg = START_PROMPT.format(memory=mem_summary)
    reply = call_model(SYSTEM_PROMPT, user_msg)
    print("Agent:", reply)
    return reply

def store_session(skill, duration_min, rating, notes):
    sid = str(uuid.uuid4())
    now = datetime.datetime.utcnow().isoformat()
    content = (
f"---\nid: {sid}\ndate: {now}\nskill: {skill}\nduration_min: {duration_min}\nrating: {rating}\nnotes: |\n  {notes}\n---\n\nagent_one_improvement: TODO\n")
    fname = SESS_DIR/f"session-{now.replace(':','').replace('.','')}.md"
    fname.write_text(content, encoding="utf-8")
    return fname

if __name__ == '__main__':
    start_session()
```

prompts.py
```python
SYSTEM_PROMPT = """You are Personal Growth Coach. Use local memory passed in user messages. At start, summarize goals and last practice (2 lines) and propose today's 1-3 focused tasks. When parsing user commands detect malformed ones and follow corrective flow. Keep concise numbered steps."""
START_PROMPT = "Memory snapshot:\n{memory}\n\nStart the session: summarize goals+last practice in 2 lines and propose today's tasks."
```

Command parsing & corrective feedback (pattern)
- Agent should expect structured commands:
  - "Plan: Train [skill] to [goal] in [timeframe]."
  - "Session complete: [skill], duration [mins], self-rating [0–10], notes: [...]"
  - "Create Anki cards: topic [X]"
- If user input doesn't match regex patterns, agent returns:
  1) one-line diagnosis,
  2) corrected example,
  3) "Execute corrected command? (yes/no)"
- Implement parser in agent.py to apply corrections automatically when user confirms.

Anki export stub (anki_export.py)
```python
# anki_export.py
import json, os
def export_cards(cards, out_file="anki_cards.json"):
    # cards: list of {"deck":"Default","front":"Q","back":"A","tags":["t"]}
    with open(out_file,"w",encoding="utf-8") as f:
        json.dump(cards,f,ensure_ascii=False,indent=2)
    print("Exported", len(cards), "cards to", out_file)
```
Hook this to AnkiConnect or import JSON to create a deck.

How memory is loaded fast on start
- Keep memory files small and structured.
- Agent loads only:
  - goals.md (full)
  - habits.md (full)
  - last 5 session files (sessions folder)
- Build a one-paragraph summary string (max ~3000 chars) and send as part of the START_PROMPT. This gives the model immediate context.

Making the memory MD files human+agent friendly
- Use YAML frontmatter at top of each file for metadata; keep body short (2–5 lines).
- Example session file shown earlier.
- Example goals.md:
  ---
  - id: goal-1
    title: "Spanish B2"
    target_date: 2026-12-01
    metric: "CEFR B2"
    notes: "5h/week; vocab 30/day"
  ---

Corrective-flow example (pseudo)
1. User: "session chess 45 notes missed pins"
2. Parser fails regex → Agent reply:
   - "I couldn't parse — expected 'Session complete: [skill], duration [mins], self-rating [0–10], notes: [...].' Correct example: 'Session complete: chess tactics, duration 45, self-rating 6, notes: missed pins. Would you like me to correct and store it? (yes/no)'"
3. If user says yes, agent reformats, asks for missing rating (if absent) or assigns default prompt "Please provide rating 0–10" then stores.

Model-agnostic integration
- call_model() in agent.py is the only LLM-specific part. Implement it for:
  - OpenAI: use openai.ChatCompletion.create with system+user messages.
  - Local LLMs: use HTTP to llama.cpp/llama.cpp-webui, or run via text-generation-webui, or use LangChain connectors.
- Keep messages short: system prompt + START_PROMPT with memory summary + user's immediate command.

Running locally (quick start)
1. Install Python dependencies (requests, pyyaml): pip install -r requirements.txt
2. Implement call_model() for your LLM and set API keys in config.yaml or environment variables.
3. Seed memory files in memory/ (create goals.md, habits.md).
4. Run: python agent.py — it will print agent's start reply.
5. Interact by calling functions or extending agent.py to accept CLI input in a loop and process commands via parser.

Persistence and speed tips
- Use small, recent-session slices — avoid sending entire history to the model.
- Keep memory MD files < 1–2 KB each.
- Cache parsed memory summary and only refresh when files change (watch file mtime).
- For very fast local LLMs, reduce system prompt length and rely on concise memory summary.

Security & privacy
- Keep MD memory local and encrypted if needed (use OS file encryption or gpg).
- Do not store secrets in memory files.

Next steps I can provide (pick one):
- Full ready-to-run repo with OpenAI & llama.cpp call_model implementations.
- A complete CLI loop (interactive) that parses commands and writes session files.
- A JSON system+example messages bundle tailored to a specific platform (specify which).

Which next step do you want?