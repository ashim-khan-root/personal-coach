import os, yaml, json, uuid, datetime, re, subprocess
from pathlib import Path
from prompts import SYSTEM_PROMPT, START_PROMPT
from memory_manager import MemoryManager

BASE = Path(__file__).parent
CONFIG_PATH = BASE / "config.yaml"

class CoachAgent:
    def __init__(self):
        self.config = self._load_config()
        self.memory = MemoryManager()
        self.model_type = self.config.get("model_type", "local")
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.api_url = self.config.get("api_url", "http://localhost:11434/v1/chat/completions")
        self.model_name = self.config.get("model_name", "llama3")
        self.temp = self.config.get("temperature", 0.7)
        self.max_tokens = self.config.get("max_tokens", 2048)

    def _load_config(self):
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    def call_model(self, system, user):
        import requests
        headers = {"Content-Type": "application/json"}
        if self.model_type != "local" and self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "temperature": self.temp,
            "max_tokens": self.max_tokens
        }
        resp = requests.post(self.api_url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def discover_tools(self, query):
        """Speculative tool discovery based on query intent."""
        tools_dir = BASE / "tools"
        available_tools = [f.stem for f in tools_dir.glob("*.py")]
        
        # Simple keyword matching for now (Coach 2.0 Step 2 will use LLM for this)
        matches = []
        for tool in available_tools:
            if tool.replace('_', ' ') in query.lower():
                matches.append(tool)
        return matches

    def process_input(self, user_input):
        # 1. Update Memory Context (Deep RAG)
        context = self.memory.get_context_for_query(user_input)
        
        # 2. Check for Tool Intent
        potential_tools = self.discover_tools(user_input)
        if potential_tools:
            print(f"DEBUG: Potential tools detected: {potential_tools}")

        # 3. Generate Response with Deep Context
        full_system = f"{SYSTEM_PROMPT}\n\nCURRENT CONTEXT:\n{context}"
        try:
            return self.call_model(full_system, user_input)
        except Exception as e:
            return f"Error connecting to brain: {e}"

def main_loop():
    agent = CoachAgent()
    print("\n=== Coach 2.0 (Deep Memory Active) ===")
    
    # Initial Greeting
    initial_context = agent.memory.get_context_for_query("morning")
    greeting = agent.call_model(SYSTEM_PROMPT, START_PROMPT.format(memory=initial_context))
    print(f"\n{greeting}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
            
        if user_input.lower() in ("exit", "quit", "bye"):
            break
        
        # Parse Structured Commands first
        cmd_name, groups = parse_command(user_input)
        if cmd_name:
            if cmd_name == "session_complete":
                skill, duration, rating, notes = groups
                agent.memory.store_session(skill, duration, rating, notes)
                print(f"Session stored.")
            continue

        response = agent.process_input(user_input)
        print(f"\n=== Coach ===\n{response}\n=============\n")

# --- Command Parsing (kept for compatibility) ---
PATTERNS = {
    "plan": re.compile(r"^[Pp]lan:\s*[Tt]rain\s+(.+?)\s+to\s+(.+?)(?:\s+in\s+(.+))?$"),
    "session_complete": re.compile(
        r"^[Ss]ession\s+complete:\s*(.+?),\s*duration\s+(\d+),\s*self-rating\s+(\d+)(?:,\s*notes:\s*(.+))?$"
    ),
    "anki": re.compile(r"^[Cc]reate\s+[Aa]nki\s+cards?:\s*(.+)$"),
    "reflect": re.compile(r"^[Rr]eflect:\s*(.+)$"),
}

def parse_command(text):
    for cmd_name, pattern in PATTERNS.items():
        m = pattern.match(text)
        if m: return cmd_name, m.groups()
    return None, None

if __name__ == '__main__':
    main_loop()

