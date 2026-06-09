"""Memory search — find relevant context across all memory files.
Supports vector search (TF-IDF) first, falls back to keyword.

Usage:
  python tools/memory_search.py "facebook shop"
  python tools/memory_search.py "SEO" --limit 5
  python tools/memory_search.py "SEO" --keyword   # force keyword mode
"""
import sys, re
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"

COACH_DIR = MEM_DIR.parent


def _vector_search(query, limit):
    """Try LightRAG vector search first, fall back to TF-IDF."""
    sys.path.insert(0, str(COACH_DIR))

    try:
        from tools.index_memory_lightrag import search_index
        results = search_index(query, limit)
        if results:
            return [
                (r["score"], MEM_DIR / r["meta"]["path"], r["meta"]["source"])
                for r in results
                if r["meta"].get("path")
            ]
    except Exception:
        pass

    try:
        from tools.index_memory import load_index
        idx = load_index()
        if idx is None:
            return None
        results = idx.search(query, limit)
        if not results:
            return None
        return [
            (r["score"], MEM_DIR / r["meta"]["path"], r["meta"]["source"])
            for r in results
        ]
    except Exception:
        return None


def search_files(query, limit=10, use_vector=True):
    """Search across all memory files for query matches.
    Uses TF-IDF vector search first, falls back to keyword matching.
    """
    if use_vector:
        vec_results = _vector_search(query, limit)
        if vec_results is not None:
            return vec_results

    query_lower = query.lower()
    results = []

    search_targets = [
        MEM_DIR / "sessions",
        MEM_DIR / "conversations",
        MEM_DIR / "daily",
        MEM_DIR / "inbox" / "processed",
        MEM_DIR / "decisions.md",
        MEM_DIR / "goals.md",
        MEM_DIR / "habits.md",
        MEM_DIR / "profile.md",
        MEM_DIR / "checkpoint.md",
        MEM_DIR / "insights.md",
    ]

    for target in search_targets:
        if target.is_dir():
            for fp in sorted(target.glob("*.md"), reverse=True):
                score = _score_file(fp, query_lower)
                if score > 0:
                    results.append((score, fp, "directory"))
        elif target.exists() and target.suffix == ".md":
            score = _score_file(target, query_lower)
            if score > 0:
                results.append((score, target, "file"))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:limit]


def _score_file(filepath, query_lower):
    """Score a file based on query matches."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return 0

    content_lower = content.lower()
    score = 0

    exact_count = content_lower.count(query_lower)
    score += exact_count * 10

    words = query_lower.split()
    for word in words:
        if len(word) > 2:
            score += content_lower.count(word) * 3

    if filepath.name.startswith("session-"):
        score += 2
    elif filepath.name.startswith("20"):
        score += 1

    return score


def _extract_context(filepath, query_lower, context_lines=3):
    """Extract matching lines with context."""
    try:
        lines = filepath.read_text(encoding="utf-8").splitlines()
    except Exception:
        return ""

    matches = []
    for i, line in enumerate(lines):
        if query_lower in line.lower():
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            context = "\n".join(f"  {'>' if j == i else ' '} {lines[j]}" for j in range(start, end))
            matches.append(context)

    return "\n\n".join(matches[:3])


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/memory_search.py \"query\" [--limit N] [--keyword]")
        sys.exit(1)

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    query = args[0] if args else ""
    limit = 10
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        if idx + 1 < len(sys.argv):
            limit = int(sys.argv[idx + 1])
    use_vector = "--keyword" not in sys.argv

    results = search_files(query, limit, use_vector)

    if not results:
        print(f'No results for "{query}"')
        return

    print(f'=== Memory Search: "{query}" ===\n')
    for score, fp, rtype in results:
        rel = fp.relative_to(MEM_DIR)
        print(f"  [{score:6.3f}] {rel}")

        content = fp.read_text(encoding="utf-8")
        content_lower = content.lower()
        idx = content_lower.find(query.lower())
        if idx >= 0:
            start = max(0, idx - 50)
            end = min(len(content), idx + len(query) + 100)
            snippet = content[start:end].replace("\n", " ").strip()
            if start > 0:
                snippet = "..." + snippet
            if end < len(content):
                snippet = snippet + "..."
            print(f"        {snippet}")
        print()


if __name__ == "__main__":
    main()
