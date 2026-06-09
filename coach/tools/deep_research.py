"""Deep research agent — search, fetch, synthesize.

Usage:
  py -3 coach/tools/deep_research.py "best cctv cameras qatar 2026"
  py -3 coach/tools/deep_research.py "competitor analysis aman qa" --max 4
  py -3 coach/tools/deep_research.py "latest AI SEO trends" --no-llm
"""
import sys, json, datetime, re
from pathlib import Path

COACH_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(COACH_DIR))

WORK_DIR = COACH_DIR / "work" / "research"
WORK_DIR.mkdir(parents=True, exist_ok=True)

from tools.web_search import search_web
from tools.web_fetch import fetch_url


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text[:60]


def generate_variations(query):
    base = query.strip().rstrip(".")
    return [
        base,
        f"{base} 2026 guide",
        f"{base} review comparison",
    ]


def dedup_urls(results):
    seen = set()
    unique = []
    for r in results:
        url = r.get("url", "")
        if url and url not in seen:
            seen.add(url)
            unique.append(r)
    return unique


def call_ollama(topic, pages_text):
    try:
        import httpx, yaml
    except ImportError:
        return None
    config_path = COACH_DIR / "config.yaml"
    if config_path.exists():
        try:
            config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        except Exception:
            config = {}
    else:
        config = {}
    api_url = config.get("api_url", "http://localhost:11434/v1/chat/completions")
    model = config.get("model_name", "llama3.2:3b")

    context = "\n\n---\n\n".join(
        f"Source: {p.get('url', '?')}\nTitle: {p.get('title', '?')}\n{p.get('text', '')[:2000]}"
        for p in pages_text
    )

    prompt = (
        "You are a research analyst. Synthesize the following web research into a structured brief.\n\n"
        f"Research Topic: {topic}\n\n"
        f"Source Material:\n{context}\n\n"
        "Provide:\n"
        "1. Executive Summary (2-3 sentences)\n"
        "2. Key Findings (bullet points with source citations)\n"
        "3. Statistics & Data Points (if any)\n"
        "4. Notable Quotes (if any)\n"
        "5. Gaps & Missing Information\n"
        "6. Sources Used (URLs)\n\n"
        "Be concise. Cite sources by title."
    )

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(api_url, json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 1000,
                "stream": False,
            })
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        pass
    return None


def build_raw_summary(topic, pages):
    lines = [
        f"# Research: {topic}",
        f"**Generated:** {datetime.date.today().isoformat()}\n",
        "## Sources Found",
    ]
    for p in pages:
        title = p.get("title", "Untitled")
        url = p.get("url", "")
        lines.append(f"\n### {title}")
        lines.append(f"**URL:** {url}")
        text = p.get("text", "")
        lines.append(f"**Content ({len(text)} chars):**")
        lines.append(text[:3000])
        if len(text) > 3000:
            lines.append("*(truncated)*")
    return "\n".join(lines)


def build_llm_summary(topic, pages, synthesis):
    sources = "\n".join(f"- [{p.get('title', '?')}]({p.get('url', '?')})" for p in pages)
    return (
        f"# Research: {topic}\n"
        f"**Generated:** {datetime.date.today().isoformat()}\n"
        f"**Method:** LLM-synthesized (Ollama)\n\n"
        f"---\n\n"
        f"{synthesis}\n\n"
        f"---\n\n"
        f"## Sources\n"
        f"{sources}\n"
    )


def deep_research(topic, max_per_query=5, try_llm=True):
    print(f"=== Deep Research: {topic} ===\n")

    queries = generate_variations(topic)
    print(f"Search variations ({len(queries)}):")
    for q in queries:
        print(f"  - {q}")
    print()

    all_results = []
    for q in queries:
        print(f"  Searching: {q[:60]}...")
        results = search_web(q, max_results=max_per_query)
        all_results.extend(results)
        print(f"    -> {len(results)} results")

    print(f"\nTotal raw results: {len(all_results)}")
    unique = dedup_urls(all_results)
    print(f"Unique URLs: {len(unique)}")

    top_urls = unique[:8]
    print(f"\nFetching top {len(top_urls)} pages...")
    pages = []
    for i, r in enumerate(top_urls, 1):
        url = r.get("url", "")
        title = r.get("title", "?")
        print(f"  [{i}/{len(top_urls)}] {title[:50]}...")
        page = fetch_url(url, max_chars=8000)
        page["title"] = title
        pages.append(page)

    print(f"\nCompiling research brief...")

    if try_llm:
        synthesis = call_ollama(topic, pages)
        if synthesis:
            brief = build_llm_summary(topic, pages, synthesis)
            method = "llm"
        else:
            print("  Ollama unavailable — falling back to raw compilation")
            brief = build_raw_summary(topic, pages)
            method = "raw"
    else:
        brief = build_raw_summary(topic, pages)
        method = "raw"

    date_str = datetime.date.today().isoformat()
    filename = f"research-{slugify(topic)}-{date_str}.md"
    filepath = WORK_DIR / filename
    filepath.write_text(brief, encoding="utf-8")

    print(f"\n=== Done ===")
    print(f"Method: {'LLM synthesis' if method == 'llm' else 'Raw compilation'}")
    print(f"Pages fetched: {len(pages)}")
    print(f"Saved: {filepath}")
    print(f"\nPreview (first 500 chars):\n")
    print(brief[:500])

    return str(filepath)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    max_per = 5
    try_llm = True
    for i, a in enumerate(sys.argv[1:]):
        if a == "--max" and i + 2 < len(sys.argv):
            max_per = int(sys.argv[i + 2])
        if a == "--no-llm":
            try_llm = False

    topic = " ".join(args)
    if not topic:
        print(__doc__)
        sys.exit(1)

    deep_research(topic, max_per, try_llm)


if __name__ == "__main__":
    main()
