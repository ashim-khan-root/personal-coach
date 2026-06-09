"""Ask questions about your coach memory.
Uses TF-IDF vector search to find relevant context, then optionally
summarizes via Ollama (if available).

Usage:
  python tools/ask_memory.py "What did I learn about SEO?"
  python tools/ask_memory.py "Facebook shop progress" --ask   # try Ollama
  python tools/ask_memory.py "SEO" --limit 5
"""
import sys, json, os
from pathlib import Path

COACH_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(COACH_DIR))

def load_index():
    try:
        from tools.index_memory_lightrag import load_index as _lr_load
        idx = _lr_load()
        if idx is not None:
            return idx
    except Exception:
        pass
    try:
        from tools.index_memory import load_index as _tfidf_load
        return _tfidf_load()
    except Exception:
        return None


def load_config():
    fp = COACH_DIR / "config.yaml"
    if not fp.exists():
        return {"api_url": "http://localhost:11434/v1/chat/completions", "model_name": "llama3.2:3b"}
    try:
        import yaml
        return yaml.safe_load(fp.read_text(encoding="utf-8"))
    except Exception:
        return {"api_url": "http://localhost:11434/v1/chat/completions", "model_name": "llama3.2:3b"}


def ask_ollama(query, context_chunks, config, timeout=8):
    """Try to get an LLM summary. Returns None if unavailable/timed out."""
    try:
        import httpx
    except ImportError:
        return None

    context_text = "\n\n".join(
        f"[{r['meta']['source']}] {r['meta']['filename']}:\n{r['text'][:600]}"
        for r in context_chunks
    )

    prompt = (
        "You are a coaching assistant reviewing session notes and memory files.\n"
        "Answer the question based ONLY on the provided context.\n"
        "If the context doesn't contain enough information, say so.\n"
        "Cite specific sources (filename) when possible.\n\n"
        f"Context:\n{context_text}\n\n"
        f"Question: {query}\n\n"
        "Answer:"
    )

    payload = {
        "model": config.get("model_name", "llama3.2:3b"),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 500,
        "stream": False,
    }

    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.post(
                config.get("api_url", "http://localhost:11434/v1/chat/completions"),
                json=payload,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
    except Exception:
        pass
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    use_llm = "--ask" in sys.argv
    limit = 10
    if "--limit" in sys.argv:
        li = sys.argv.index("--limit")
        limit = int(sys.argv[li + 1])

    query = " ".join(args) if args else ""
    if not query:
        print("Usage: python tools/ask_memory.py \"your question\"")
        sys.exit(1)

    idx = load_index()
    if not idx:
        print("No index found. Run `python tools/index_memory.py` first.")
        sys.exit(1)

    results = idx.search(query, limit)
    if not results:
        print(f'No relevant context found for "{query}"')
        return

    if use_llm:
        print(f"Searching memory and generating answer...\n")
        config = load_config()
        answer = ask_ollama(query, results, config)
        if answer:
            print("─" * 50)
            print(answer)
            print("─" * 50)
        else:
            print("(Ollama unavailable or timed out — showing raw results below)\n")

    print(f'\n=== "{query}" — Top {len(results)} results ===\n')
    for r in results:
        src = r["meta"]["source"]
        fn = r["meta"]["filename"]
        snippet = r["text"][:250].replace("\n", " ").strip()
        print(f"  [{r['score']:.3f}] ({src}) {fn}")
        print(f"    {snippet}")
        print()


if __name__ == "__main__":
    main()
