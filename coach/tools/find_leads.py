import sys
import json
import datetime
from pathlib import Path

# Add coach root to path for imports
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from tools.web_search import search_web
from tools.web_fetch import fetch_url
from agent import CoachAgent

def find_leads(niche, location, max_leads=10):
    agent = CoachAgent()
    query = f"companies in {location} needing {niche} or automation services"
    print(f"Searching for leads: {query}...")
    
    search_results = search_web(query, max_results=max_leads)
    leads = []
    
    for res in search_results:
        url = res.get("url")
        if not url or "linkedin.com" in url or "yellowpages" in url:
            continue
            
        print(f"Analyzing company: {url}")
        site_data = fetch_url(url)
        content = site_data.get("text", "")[:2000]
        
        prompt = (
            f"Analyze this website content for a company named '{res.get('title')}' at {url}.\n\n"
            f"Content:\n{content}\n\n"
            "Identify:\n"
            "1. What do they do?\n"
            "2. Potential pain points where AI/Automation could help.\n"
            "3. Contact info if available.\n\n"
            "Return a JSON object with keys: name, website, services, pain_points, contact_info."
        )
        
        try:
            lead_json = agent.call_model("You are a business analyst finding lead opportunities.", prompt)
            # Clean JSON
            lead_json = re.sub(r'```json\n|```', '', lead_json, flags=re.MULTILINE).strip()
            lead_data = json.loads(lead_json)
            leads.append(lead_data)
            print(f"✅ Found Lead: {lead_data['name']}")
        except Exception as e:
            print(f"Failed to analyze {url}: {e}")
            
    return leads

if __name__ == "__main__":
    import re
    niche = sys.argv[1] if len(sys.argv) > 1 else "AI automation"
    loc = sys.argv[2] if len(sys.argv) > 2 else "Qatar"
    
    leads = find_leads(niche, loc)
    
    output_dir = BASE / "work" / "leads"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = output_dir / f"leads-{timestamp}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2)
        
    print(f"\nCaptured {len(leads)} leads to {output_file}")
