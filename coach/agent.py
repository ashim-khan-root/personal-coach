import os, yaml, json, uuid, datetime, re, subprocess
from pathlib import Path
from prompts import SYSTEM_PROMPT, START_PROMPT, DISPATCHER_PROMPT
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

    def discover_tools_fallback(self, query):
        """Fallback keyword-based discovery."""
        tools_dir = BASE / "tools"
        available_tools = [f.stem for f in tools_dir.glob("*.py")]
        for tool in available_tools:
            if tool.replace('_', ' ') in query.lower():
                return tool
        return None

    def dispatch_tool(self, user_input):
        """Use the LLM to classify intent and return tool info (tool_name, args, reason)."""
        prompt = DISPATCHER_PROMPT.format(query=user_input)
        try:
            raw_response = self.call_model("You are a strict text classification router.", prompt)
            
            tool_name = None
            args = []
            reason = ""
            
            for line in raw_response.splitlines():
                line = line.strip()
                if line.startswith("TOOL:"):
                    val = line.split(":", 1)[1].strip()
                    if val.lower() not in ("none", "null", ""):
                        tool_name = val
                elif line.startswith("ARG:"):
                    val = line.split(":", 1)[1].strip()
                    # Strip surrounding quotes if the LLM generated them
                    if val.startswith('"') and val.endswith('"'):
                        val = val[1:-1]
                    elif val.startswith("'") and val.endswith("'"):
                        val = val[1:-1]
                    args.append(val)
                elif line.startswith("REASON:"):
                    reason = line.split(":", 1)[1].strip()
                    
            return tool_name, args, reason
        except Exception as e:
            print(f"DEBUG: LLM dispatch failed ({e}). Falling back to keyword matching.")
            fallback = self.discover_tools_fallback(user_input)
            return fallback, [], f"Fallback due to error: {e}"

    def execute_tool(self, tool_name, args):
        """Execute the python script corresponding to the tool name via subprocess."""
        tool_script = BASE / "tools" / f"{tool_name}.py"
        if not tool_script.exists():
            return f"Error: Tool script '{tool_name}.py' not found at {tool_script}"
            
        cmd = ["py", "-3", str(tool_script)] + [str(arg) for arg in args]
        print(f"DEBUG: Executing tool command: {' '.join(cmd)}")
        try:
            # Run in the project root directory
            project_root = BASE.parent
            res = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True, timeout=120)
            
            output = ""
            if res.stdout:
                output += f"Output:\n{res.stdout}\n"
            if res.stderr:
                output += f"Errors/Warnings:\n{res.stderr}\n"
            if res.returncode != 0:
                output += f"Exit Code: {res.returncode}\n"
            
            return output if output else "Tool executed successfully (no output)."
        except Exception as e:
            return f"Error executing tool {tool_name}: {e}"

    def process_input(self, user_input):
        # 1. Update Memory Context (Deep RAG) first, so we don't have to reload memory post-tool
        # (Though we might want context to contain tool output, we gather context and append tool output)
        tool_name, args, reason = self.dispatch_tool(user_input)
        
        tool_output = ""
        if tool_name:
            print(f"DEBUG: LLM dispatched tool: '{tool_name}' with args: {args}. Reason: {reason}")
            tool_output = self.execute_tool(tool_name, args)
            print(f"DEBUG: Tool output:\n{tool_output}\n")
            
        # 2. Update Memory Context (Deep RAG)
        context = self.memory.get_context_for_query(user_input)
        
        # 3. Generate Response with Deep Context and Tool Output (if any)
        context_block = f"CURRENT CONTEXT:\n{context}"
        if tool_output:
            context_block += f"\n\nEXECUTED TOOL OUTPUT ({tool_name} {' '.join(args)}):\n{tool_output}"
            
        full_system = f"{SYSTEM_PROMPT}\n\n{context_block}"
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

