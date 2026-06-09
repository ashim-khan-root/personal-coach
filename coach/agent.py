import os, yaml, json, uuid, datetime, re
from pathlib import Path
from prompts import SYSTEM_PROMPT, START_PROMPT

BASE = Path(__file__).parent
MEM_DIR = BASE / "memory"
SESS_DIR = MEM_DIR / "sessions"
SESS_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_PATH = BASE / "config.yaml"

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

config = load_config()
MODEL_TYPE = config.get("model_type", "local")
API_KEY = os.environ.get("OPENAI_API_KEY", "")
API_URL = config.get("api_url", "http://localhost:11434/v1/chat/completions")
MODEL_NAME = config.get("model_name", "llama3")
TEMPERATURE = config.get("temperature", 0.7)
MAX_TOKENS = config.get("max_tokens", 2048)

def read_md(file):
    if not file.exists():
        return ""
    return file.read_text(encoding="utf-8")

def write_md(file, content):
    file.write_text(content, encoding="utf-8")

def load_memory_summary(max_items=5):
    goals = read_md(MEM_DIR / "goals.md")
    habits = read_md(MEM_DIR / "habits.md")
    meta = read_md(MEM_DIR / "meta.md")
    sessions = sorted(SESS_DIR.glob("session-*.md"), key=lambda p: p.stem, reverse=True)[:max_items]
    recent = []
    for s in sessions:
        txt = read_md(s).splitlines()[:10]
        recent.append("\n".join(txt))
    summary_parts = []
    if meta:
        summary_parts.append(f"META:\n{meta}")
    if goals:
        summary_parts.append(f"GOALS:\n{goals}")
    if habits:
        summary_parts.append(f"HABITS:\n{habits}")
    if recent:
        summary_parts.append("RECENT SESSIONS:\n" + "\n---\n".join(recent))
    summary = "\n\n".join(summary_parts)
    return summary[:4000]

def call_model_openai(system, user):
    if not API_KEY:
        return "API key not set. Set OPENAI_API_KEY env var or use model_type: local."
    import requests
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def call_model_local(system, user):
    import requests
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS
    }
    resp = requests.post(API_URL, headers={"Content-Type": "application/json"}, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def call_model(system, user):
    if MODEL_TYPE == "local":
        return call_model_local(system, user)
    return call_model_openai(system, user)

PATTERNS = {
    "plan": re.compile(r"^[Pp]lan:\s*[Tt]rain\s+(.+?)\s+to\s+(.+?)(?:\s+in\s+(.+))?$"),
    "session_complete": re.compile(
        r"^[Ss]ession\s+complete:\s*(.+?),\s*duration\s+(\d+),\s*self-rating\s+(\d+)(?:,\s*notes:\s*(.+))?$"
    ),
    "anki": re.compile(r"^[Cc]reate\s+[Aa]nki\s+cards?:\s*(.+)$"),
    "reflect": re.compile(r"^[Rr]eflect:\s*(.+)$"),
}

def parse_command(text):
    trimmed = text.strip()
    for cmd_name, pattern in PATTERNS.items():
        m = pattern.match(trimmed)
        if m:
            return cmd_name, m.groups()
    return None, None

def generate_improvement_tip(skill, rating, notes):
    prompt = (
        f"Based on this practice session:\n"
        f"Skill: {skill}\n"
        f"Self-rating: {rating}/10\n"
        f"Notes: {notes}\n\n"
        f"Generate ONE specific, actionable improvement tip for next time "
        f"(1-2 sentences). Be direct and practical."
    )
    try:
        return call_model(
            "You are a concise improvement coach. Give one actionable tip based on session data.",
            prompt
        )[:500]
    except Exception:
        return None

def generate_correction(text):
    return (
        f"I couldn't parse your command.\n"
        f"Expected format: 'Session complete: <skill>, duration <mins>, self-rating <0-10>, notes: <...>'\n"
        f"Example: 'Session complete: chess tactics, duration 45, self-rating 6, notes: missed pins'\n"
        f"Would you like me to correct and store it? (yes/no)"
    )

def store_session(skill, duration_min, rating, notes="", improvement=""):
    sid = str(uuid.uuid4())
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    content = (
        f"---\n"
        f"id: {sid}\n"
        f"date: {timestamp}\n"
        f"skill: {skill}\n"
        f"duration_min: {duration_min}\n"
        f"rating: {rating}\n"
        f"notes: |\n"
        f"  {notes}\n"
        f"tags: []\n"
        f"---\n\n"
        f"agent_one_improvement: {improvement or 'TODO'}\n"
    )
    fname = SESS_DIR / f"session-{now}.md"
    write_md(fname, content)
    return fname

def handle_session_complete(groups, raw_text):
    skill, duration, rating, notes = groups
    try:
        rating = int(rating)
    except ValueError:
        rating = input("Invalid rating. Please provide a number 0-10: ")
        try:
            rating = int(rating)
        except ValueError:
            rating = 0
    if not notes:
        notes = input("Notes (optional): ") or ""
    fname = store_session(skill, int(duration), int(rating), notes)
    print(f"Session stored: {fname}")
    tip = generate_improvement_tip(skill, rating, notes)
    if tip:
        content = read_md(fname)
        content = content.replace("agent_one_improvement: TODO", f"agent_one_improvement: {tip}")
        write_md(fname, content)
        print(f"\n💡 One improvement for next time:\n{tip}\n")
    return True

def handle_plan(groups):
    print(f"Plan recognized — training '{groups[0]}' towards '{groups[1]}'.")
    return True

def handle_anki(groups):
    topic = groups[0]
    print(f"Anki card creation requested for topic: {topic}")
    return True

def handle_reflect(groups):
    topic = groups[0]
    sessions = sorted(SESS_DIR.glob("session-*.md"), key=lambda p: p.stem, reverse=True)
    relevant = []
    for s in sessions:
        txt = s.read_text(encoding="utf-8")
        if topic.lower() in txt.lower():
            relevant.append(txt[:500])
    context = "\n---\n".join(relevant[:10]) if relevant else "No past sessions found on this topic."
    try:
        reply = call_model(
            SYSTEM_PROMPT + "\n\nYou are now reflecting on past sessions. Give a meta-perspective: patterns, growth, blind spots, and recommendations.",
            f"Reflect on these sessions about '{topic}':\n\n{context}"
        )
    except Exception:
        reply = f"Found {len(relevant)} session(s) about '{topic}'. Couldn't generate reflection — connectivity issue."
    print(f"\n=== Reflection on: {topic} ===\n{reply}\n=============================\n")
    return True

COMMAND_HANDLERS = {
    "session_complete": handle_session_complete,
    "plan": handle_plan,
    "anki": handle_anki,
    "reflect": handle_reflect,
}

def start_session():
    mem_summary = load_memory_summary()
    user_msg = START_PROMPT.format(memory=mem_summary)
    try:
        reply = call_model(SYSTEM_PROMPT, user_msg)
    except Exception as e:
        print(f"\n⚠️  Couldn't reach the LLM ({e}). Starting in offline mode.")
        reply = "I'm here! Tell me what you're working on and I'll help."
    print("\n=== Coach ===")
    print(reply)
    print("=============\n")
    return reply

def update_meta():
    meta_path = MEM_DIR / "meta.md"
    meta = read_md(meta_path)
    lines = meta.splitlines() if meta else []
    new_lines = []
    updated = False
    for line in lines:
        if line.startswith("updated_at:"):
            new_lines.append(f"updated_at: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        new_lines.insert(0, f"updated_at: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
    write_md(meta_path, "\n".join(new_lines))

def main_loop():
    start_session()
    update_meta()
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "bye"):
            print("Coach: Goodbye! Keep growing.")
            break
        cmd_name, groups = parse_command(user_input)
        if cmd_name:
            handler = COMMAND_HANDLERS.get(cmd_name)
            if handler:
                if cmd_name == "session_complete":
                    handler(groups, user_input)
                else:
                    handler(groups)
                update_meta()
            continue
        try:
            reply = call_model(
                SYSTEM_PROMPT + "\n\nWhen the user sends unstructured input, respond helpfully as a coach.",
                user_input
            )
        except Exception:
            reply = "I'm having trouble connecting right now. Could you try again or use a structured command?"
        print(f"\n=== Coach ===\n{reply}\n=============\n")
        update_meta()

if __name__ == '__main__':
    main_loop()
