"""TF-IDF vector indexer for coach memory.
Usage:
  python tools/index_memory.py              # build/rebuild index
  python tools/index_memory.py --search "query"  # search without MCP
  python tools/index_memory.py --info       # show index stats
"""
import sys, re, json, math
from pathlib import Path
from collections import Counter
from datetime import datetime

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
INDEX_DIR = MEM_DIR / ".search_index"
INDEX_DIR.mkdir(parents=True, exist_ok=True)


# ── chunking ──────────────────────────────────────────────────────────────

def _read_file(path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _strip_yaml(text):
    return re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL).strip()


def _extract_date(text, filename):
    m = re.search(r'^date:\s*["\']?(\d{4}-\d{2}-\d{2})', text, re.MULTILINE)
    if m:
        return m.group(1)
    m = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if m:
        return m.group(1)
    return ""


def _chunk_sessions():
    entries = []
    sess_dir = MEM_DIR / "sessions"
    for fp in sorted(sess_dir.glob("session-*.md"), reverse=True):
        text = _read_file(fp)
        if not text.strip():
            continue
        date = _extract_date(text, fp.name)
        body = _strip_yaml(text)
        entries.append({
            "text": body or text,
            "meta": {"source": "sessions", "filename": fp.name, "date": date, "path": str(fp.relative_to(MEM_DIR))}
        })
    return entries


def _chunk_daily():
    entries = []
    daily_dir = MEM_DIR / "daily"
    for fp in sorted(daily_dir.glob("*.md"), reverse=True):
        text = _read_file(fp)
        if not text.strip():
            continue
        date = fp.stem if re.match(r'\d{4}-\d{2}-\d{2}', fp.stem) else ""
        body = _strip_yaml(text)
        sections = re.split(r'\n(?=##\s)', body) if body else [text]
        for sec in sections:
            sec = sec.strip()
            if len(sec) < 20:
                continue
            entries.append({
                "text": sec,
                "meta": {"source": "daily", "filename": fp.name, "date": date, "path": str(fp.relative_to(MEM_DIR))}
            })
    return entries


def _chunk_conversations():
    entries = []
    conv_dir = MEM_DIR / "conversations"
    if not conv_dir.exists():
        return entries
    for fp in sorted(conv_dir.glob("conv-*.md"), reverse=True):
        text = _read_file(fp)
        if not text.strip():
            continue
        date = _extract_date(text, fp.name)
        body = _strip_yaml(text)
        entries.append({
            "text": body or text,
            "meta": {"source": "conversations", "filename": fp.name, "date": date, "path": str(fp.relative_to(MEM_DIR))}
        })
    return entries


def _chunk_simple(source, filename):
    fp = MEM_DIR / filename
    if not fp.exists():
        return []
    text = _read_file(fp)
    if not text.strip():
        return []
    date = _extract_date(text, fp.name)
    body = _strip_yaml(text)

    entries = []
    if source in ("goals", "habits"):
        items = re.findall(r'^-?\s*title:\s*["\']?(.+?)["\']?$', body, re.MULTILINE)
        if items:
            for item in items:
                entries.append({
                    "text": item.strip(),
                    "meta": {"source": source, "filename": fp.name, "date": date, "path": str(fp.relative_to(MEM_DIR))}
                })
            return entries

    entries.append({
        "text": body or text,
        "meta": {"source": source, "filename": fp.name, "date": date, "path": str(fp.relative_to(MEM_DIR))}
    })
    return entries


def collect_entries():
    entries = []
    entries.extend(_chunk_sessions())
    entries.extend(_chunk_daily())
    entries.extend(_chunk_conversations())
    entries.extend(_chunk_simple("goals", "goals.md"))
    entries.extend(_chunk_simple("habits", "habits.md"))
    entries.extend(_chunk_simple("checkpoint", "checkpoint.md"))
    entries.extend(_chunk_simple("profile", "profile.md"))
    entries.extend(_chunk_simple("insights", "insights.md"))
    entries.extend(_chunk_simple("decisions", "decisions.md"))
    return entries


# ── TF-IDF (pure Python, no sklearn dependency at runtime) ───────────────

class TfidfIndex:
    def __init__(self):
        self.entries = []
        self.idf = {}
        self.doc_norms = []
        self.vocab = {}

    def _tokenize(self, text):
        return re.findall(r'[a-zA-Z0-9_]{2,}', text.lower())

    def _term_freq(self, tokens):
        return Counter(tokens)

    def build(self, entries):
        self.entries = entries
        n_docs = len(entries)

        doc_tfs = []
        df = Counter()
        for e in entries:
            tokens = self._tokenize(e["text"])
            tf = self._term_freq(tokens)
            doc_tfs.append(tf)
            df.update(set(tokens))

        self.vocab = {term: idx for idx, (term, _) in enumerate(df.most_common())}
        vocab_size = len(self.vocab)

        self.idf = {}
        for term, freq in df.items():
            self.idf[term] = math.log((n_docs + 1) / (freq + 1)) + 1

        import numpy as np
        self.matrix = np.zeros((n_docs, vocab_size), dtype=np.float32)
        for i, tf in enumerate(doc_tfs):
            for term, freq in tf.items():
                if term in self.vocab:
                    tfidf = freq * self.idf.get(term, 0)
                    self.matrix[i, self.vocab[term]] = tfidf

        self.doc_norms = np.linalg.norm(self.matrix, axis=1)
        self.doc_norms = np.where(self.doc_norms == 0, 1, self.doc_norms)

    def search(self, query, k=10):
        query_tokens = self._tokenize(query)
        q_tf = self._term_freq(query_tokens)

        import numpy as np
        q_vec = np.zeros(len(self.vocab), dtype=np.float32)
        for term, freq in q_tf.items():
            if term in self.vocab:
                q_vec[self.vocab[term]] = freq * self.idf.get(term, 0)

        q_norm = np.linalg.norm(q_vec)
        if q_norm == 0:
            return []

        q_vec = q_vec / q_norm
        scores = self.matrix / self.doc_norms[:, np.newaxis]
        scores = scores @ q_vec

        top_indices = np.argsort(scores)[::-1][:k]
        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                results.append({
                    "score": float(scores[idx]),
                    "text": self.entries[idx]["text"][:500],
                    "meta": self.entries[idx]["meta"]
                })
        return results

    def save(self, path):
        import joblib
        joblib.dump({
            "entries": self.entries,
            "idf": self.idf,
            "vocab": self.vocab,
            "matrix": self.matrix,
            "doc_norms": self.doc_norms,
        }, path)

    @classmethod
    def load(cls, path):
        import joblib
        data = joblib.load(path)
        idx = cls()
        idx.entries = data["entries"]
        idx.idf = data["idf"]
        idx.vocab = data["vocab"]
        idx.matrix = data["matrix"]
        idx.doc_norms = data["doc_norms"]
        return idx


# ── public API ───────────────────────────────────────────────────────────

INDEX_PATH = INDEX_DIR / "index.joblib"


def build_index():
    entries = collect_entries()
    if not entries:
        print("[index] No entries found to index.")
        return None
    idx = TfidfIndex()
    idx.build(entries)
    idx.save(INDEX_PATH)
    print(f"[index] Indexed {len(entries)} chunks from memory")
    return idx


def load_index():
    if INDEX_PATH.exists():
        return TfidfIndex.load(INDEX_PATH)
    return None


def get_index_info():
    idx = load_index()
    if not idx:
        return {"status": "no_index", "entries": 0}
    sources = Counter(e["meta"]["source"] for e in idx.entries)
    return {
        "status": "ready",
        "entries": len(idx.entries),
        "vocab_size": len(idx.vocab),
        "sources": dict(sources),
    }


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    if "--search" in sys.argv:
        q_idx = sys.argv.index("--search")
        if q_idx + 1 < len(sys.argv):
            query = sys.argv[q_idx + 1]
            limit = 10
            if "--limit" in sys.argv:
                li = sys.argv.index("--limit")
                limit = int(sys.argv[li + 1])
            idx = load_index()
            if not idx:
                print("[index] No index found. Run without --search first.")
                return
            results = idx.search(query, limit)
            if not results:
                print(f'No results for "{query}"')
                return
            print(f'=== Vector Search: "{query}" ===\n')
            for r in results:
                src = r["meta"]["source"]
                fn = r["meta"]["filename"]
                print(f"  [{r['score']:.3f}] ({src}) {fn}")
                print(f"        {r['text'][:200].replace(chr(10), ' ')}")
                print()
        return

    if "--info" in sys.argv:
        info = get_index_info()
        if info["status"] == "no_index":
            print("[index] No index built yet. Run without flags to build.")
        else:
            print(f"Entries: {info['entries']}")
            print(f"Vocab size: {info['vocab_size']}")
            print("Sources:")
            for src, count in info["sources"].items():
                print(f"  {src}: {count}")
        return

    build_index()


if __name__ == "__main__":
    main()
