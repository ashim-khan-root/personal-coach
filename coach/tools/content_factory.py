import sys
import datetime
from pathlib import Path

# Add coach root to path for imports
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from tools.web_search import search_web
from tools.web_fetch import fetch_url
from agent import CoachAgent

def generate_article(keyword):
    agent = CoachAgent()
    print(f"Researching keyword: {keyword}...")
    
    # 1. Research Top 3 competitors
    search_results = search_web(keyword, max_results=3)
    research_context = ""
    
    for res in search_results:
        url = res.get("url")
        print(f"  Reading: {url}")
        content = fetch_url(url).get("text", "")[:1500]
        research_context += f"\n--- Source: {url} ---\n{content}\n"
        
    # 2. Generate optimized content
    prompt = (
        f"You are a programmatic SEO expert. Write a high-value, 1000-word article targeting the keyword: '{keyword}'.\n\n"
        f"Use the following research context for facts and structure:\n{research_context}\n\n"
        "Requirements:\n"
        "1. Catchy H1 with keyword.\n"
        "2. At least 5 sections with H2/H3 tags.\n"
        "3. Include a 'How to' guide.\n"
        "4. Include a 'Technical FAQ' section.\n"
        "5. Maintain a professional yet helpful tone.\n"
        "Return the content in Markdown format."
    )
    
    try:
        content = agent.call_model("You are a high-performance SEO content writer.", prompt)
        return content
    except Exception as e:
        print(f"Failed to generate content: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python content_factory.py \"keyword\"")
        sys.exit(1)
        
    kw = sys.argv[1]
    article = generate_article(kw)
    
    if article:
        output_dir = BASE / "work" / "content"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = kw.lower().replace(' ', '-') + ".md"
        output_file = output_dir / filename
        
        output_file.write_text(article, encoding="utf-8")
        print(f"✅ Article generated: {output_file}")
