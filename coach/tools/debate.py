import sys
from pathlib import Path

# Add coach root to path for imports
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from agent import CoachAgent

def run_debate(proposal, topic="Software Architecture"):
    agent = CoachAgent()
    
    print(f"=== Starting Agent Debate on: {topic} ===")
    print(f"Proposal: {proposal}\n")
    
    # Agent 1: The Visionary / Developer
    dev_prompt = (
        "You are an ambitious Software Architect. Your goal is to build powerful, scalable, and feature-rich systems. "
        "Review the proposal and suggest how to make it bigger and better."
    )
    
    # Agent 2: The Pragmatist / Security Auditor
    auditor_prompt = (
        "You are a cautious Security Auditor and SRE. Your goal is to find risks, technical debt, and security holes. "
        "Review the proposal and find everything that could go wrong."
    )
    
    print("Agent 1 (Architect) is thinking...")
    dev_view = agent.call_model(dev_prompt, proposal)
    
    print("Agent 2 (Auditor) is thinking...")
    auditor_view = agent.call_model(auditor_prompt, proposal)
    
    print("\n--- Architect's Vision ---")
    print(dev_view)
    
    print("\n--- Auditor's Concerns ---")
    print(auditor_view)
    
    # Final Synthesis
    synthesis_prompt = (
        "You are a Senior Technical Project Manager. You have heard two views on a proposal: "
        "one from an Architect and one from an Auditor. Provide a final, balanced recommendation "
        "that captures the best of both while mitigating the risks."
    )
    
    debate_summary = f"Architect: {dev_view}\n\nAuditor: {auditor_view}"
    
    print("\nSynthesizing final recommendation...")
    final_plan = agent.call_model(synthesis_prompt, debate_summary)
    
    print("\n=== Final Balanced Recommendation ===")
    print(final_plan)
    
    return final_plan

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debate.py \"proposal text\"")
        sys.exit(1)
        
    proposal = sys.argv[1]
    run_debate(proposal)
