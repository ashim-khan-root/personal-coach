import sys
import subprocess
import os
from pathlib import Path

# Add coach root to path for imports
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from agent import CoachAgent
from prompts import SYSTEM_PROMPT

def run_with_autofix(command, max_retries=3):
    agent = CoachAgent()
    
    for attempt in range(max_retries):
        print(f"--- Attempt {attempt + 1}: Running '{command}' ---")
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if process.returncode == 0:
            print("✅ Command succeeded!")
            print(process.stdout)
            return True
            
        print("❌ Command failed. Triggering autofix...")
        error_msg = process.stderr or process.stdout
        print(f"Error detected:\n{error_msg}")
        
        # Identify the file causing the error (simple heuristic)
        # Often the last .py file mentioned in a traceback
        python_files = re.findall(r'File "(.+?\.py)"', error_msg)
        if not python_files:
            print("Could not identify the failing file. Aborting.")
            return False
            
        target_file = python_files[-1]
        print(f"Targeting file for fix: {target_file}")
        
        file_content = Path(target_file).read_text(encoding="utf-8")
        
        prompt = (
            f"The following command failed: {command}\n\n"
            f"Error message:\n{error_msg}\n\n"
            f"Content of {target_file}:\n\n{file_content}\n\n"
            f"Please provide the FULL corrected content of {target_file} to fix the error. "
            f"Return ONLY the file content, no explanations."
        )
        
        fix_system_prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            "You are a self-healing engineering agent. Your only job is to fix the provided code to resolve the specific error. "
            "Output the full file content directly."
        )
        
        try:
            new_content = agent.call_model(fix_system_prompt, prompt)
            # Basic sanitization if the LLM adds markdown blocks
            new_content = re.sub(r'^```python\n|```$', '', new_content, flags=re.MULTILINE).strip()
            
            Path(target_file).write_text(new_content, encoding="utf-8")
            print(f"Applied fix to {target_file}. Retrying...")
        except Exception as e:
            print(f"Failed to generate fix: {e}")
            return False
            
    print("Reached max retries. Autofix failed.")
    return False

if __name__ == "__main__":
    import re
    if len(sys.argv) < 2:
        print("Usage: python autofix.py \"command to run\"")
        sys.exit(1)
        
    cmd = sys.argv[1]
    run_with_autofix(cmd)
