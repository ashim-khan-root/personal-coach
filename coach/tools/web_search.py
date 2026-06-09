"""Web search via DuckDuckGo. Returns structured results.

Usage:
  py -3 coach/tools/web_search.py "query" [--max 10]
  py -3 coach/tools/web_search.py "query" --site secuview.com
"""
import sys, json
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS


def search_web(query: str, max_results: int = 10, site: str | None = None) -> list[dict]:
    full_query = f"site:{site} {query}" if site else query
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(full_query, max_results=max_results))
        return [
            {
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
            }
            for r in results
        ]
    except Exception as e:
        return [{"error": str(e)}]


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--max")]
    max_r = 10
    site = None
    for i, a in enumerate(sys.argv[1:]):
        if a == "--max" and i + 2 < len(sys.argv):
            max_r = int(sys.argv[i + 2])
        if a.startswith("--site"):
            site = sys.argv[i + 1] if "=" not in a else a.split("=", 1)[1]

    query = " ".join(a for a in args if not a.startswith("--"))
    if not query:
        print("Usage: py -3 coach/tools/web_search.py <query> [--max N] [--site domain]")
        sys.exit(1)

    results = search_web(query, max_r, site)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(results, indent=2, ensure_ascii=False))
