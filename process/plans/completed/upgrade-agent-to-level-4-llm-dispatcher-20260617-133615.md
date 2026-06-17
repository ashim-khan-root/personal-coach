---
title: "Upgrade agent to Level 4 LLM Dispatcher"
created: "2026-06-17T13:36:15.392648+00:00"
status: completed  # active | completed | backlog
phase: review  # research | plan | execute | review
---

## Objective

Move the tool execution system in [agent.py](file:///C:/Users/Lenovo/Desktop/MOI%20Site%20survey/personal-coach/coach/agent.py) from keyword matching to a Level 4 LLM-based dispatcher. Instead of scanning for substring matches, the agent will query the LLM to classify user intent, determine if a local tool needs to be executed, and construct the correct command-line arguments dynamically.

## Approach

1. **Dispatcher Prompt**: Define a `DISPATCHER_PROMPT` in [prompts.py](file:///C:/Users/Lenovo/Desktop/MOI%20Site%20survey/personal-coach/coach/prompts.py) detailing all coach memory/workflow tools, their inputs, flag syntax, and examples. The LLM must output clean JSON:
   * `{"tool": "<tool_name>", "args": ["arg1", "arg2", ...], "reason": "<rationale>"}`
   * Or `{"tool": null}` if no tool is required.
2. **LLM Dispatcher Call**: Add a `dispatch_tool` method to `CoachAgent` that calls the model with the dispatcher prompt.
3. **Execution Harness**: If a tool is identified:
   * Log the selected tool and arguments.
   * Run the tool script using `subprocess.run` (resolving the Python executable as `py -3` on Windows).
   * Capture `stdout` and `stderr`.
4. **Context Injection**: Feed the tool output (if any) directly into the main prompt context so the coach can formulate a coherent, context-rich final response.
5. **Robustness & Fallbacks**: 
   * Gracefully handle invalid JSON or syntax exceptions from local LLMs.
   * If a tool fails, report the error or fall back to standard chat without crashing.

## Deliverables

- **[prompts.py](file:///C:/Users/Lenovo/Desktop/MOI%20Site%20survey/personal-coach/coach/prompts.py)**: Define `DISPATCHER_PROMPT` containing instructions and formatting rules for tools.
- **[agent.py](file:///C:/Users/Lenovo/Desktop/MOI%20Site%20survey/personal-coach/coach/agent.py)**: Update `CoachAgent` to implement `dispatch_tool`, execute selected scripts, and integrate execution outputs.
- **Verification**: Run interactive checks with tools like `task_manager.py`, `read_goals.py`, and general chat queries to verify routing logic.

## Success Criteria

- [ ] Standard conversational queries (e.g. "hi", "how are you?") do not trigger tools.
- [ ] Intent queries (e.g. "show goals", "list pending tasks") correctly invoke `read_goals.py` or `task_manager.py list`.
- [ ] Command queries with arguments (e.g. "add high priority task Build a website") correctly execute `task_manager.py add "Build a website" high`.
- [ ] Tool results are successfully captured and reflected in the final agent reply to the user.
- [ ] Any script errors or parsing issues are caught and do not crash the interactive main loop.

## Resources

- Relevant skills: [web-development](file:///C:/Users/Lenovo/Desktop/MOI%20Site%20survey/personal-coach/.opencode/skills/web-development/SKILL.md), [agent-browser](file:///C:/Users/Lenovo/Desktop/MOI%20Site%20survey/personal-coach/.opencode/skills/agent-browser/SKILL.md)
- Memory references: [AGENTS.md](file:///C:/Users/Lenovo/Desktop/MOI%20Site%20survey/personal-coach/AGENTS.md)

## Notes
- All commands on Windows must run via `py -3` in the root working directory.
- Avoid using libraries that might not be in the requirements; stick to `subprocess`, `json`, and the standard library.

