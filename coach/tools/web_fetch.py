"""Fetch and extract readable content from a URL.

Usage:
  py -3 coach/tools/web_fetch.py <url>
  py -3 coach/tools/web_fetch.py <url> --selector "div.content"
"""
import sys, json, re
import requests
from bs4 import BeautifulSoup


def fetch_url(url: str, selector: str | None = None, max_chars: int = 8000) -> dict:
    try:
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        if selector:
            elements = soup.select(selector)
            text = "\n".join(e.get_text(strip=True) for e in elements)
        else:
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)

        text = re.sub(r"\n{3,}", "\n\n", text)

        return {
            "url": url,
            "title": soup.title.string.strip() if soup.title and soup.title.string else "",
            "text": text[:max_chars],
            "truncated": len(text) > max_chars,
        }
    except Exception as e:
        return {"url": url, "error": str(e)}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    selector = None
    for i, a in enumerate(sys.argv[1:]):
        if a == "--selector" and i + 2 < len(sys.argv):
            selector = sys.argv[i + 2]

    if not args:
        print("Usage: py -3 coach/tools/web_fetch.py <url> [--selector css]")
        sys.exit(1)

    result = fetch_url(args[0], selector)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(result, indent=2, ensure_ascii=False))
