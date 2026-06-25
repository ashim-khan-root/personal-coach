"""LightRAG vector indexer for coach memory.
Reuses chunking and TF-IDF fallback from index_memory.py.
Adds graph-based RAG on top when LightRAG + Ollama are available.

Usage:
  python tools/index_memory_lightrag.py              # build/rebuild index
  python tools/index_memory_lightrag.py --search "query"  # search without MCP
  python tools/index_memory_lightrag.py --info       # show index stats
"""
import sys, json
from pathlib import Path
from collections import Counter

import index_memory
from index_memory import collect_entries, TfidfIndex, INDEX_PATH

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
LIGHT_DIR = MEM_DIR / ".lightrag"
LIGHT_DIR.mkdir(parents=True, exist_ok=True)

try:
    from lightrag import LightRAG as _LightRAG
    from lightrag.base import QueryParam
    from lightrag.llm.ollama import ollama_model_complete, ollama_embed
    import numpy as np
    HAS_LIGHTRAG = True
except ImportError:
    HAS_LIGHTRAG = False


# ── Public API ──────────────────────────────────────────────────────────

LIGHTRAG_PATH = LIGHT_DIR / "lightrag_data"
LIGHTRAG_CONFIG_PATH = LIGHT_DIR / "config.json"


def _ollama_running():
    try:
        import urllib.request
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2)
        return True
    except Exception:
        return False


def _build_lightrag():
    if not _ollama_running():
        print("[lightrag] Ollama not running. Use TF-IDF fallback.")
        return None
    try:
        import asyncio
        config_path = Path(__file__).resolve().parent.parent / "config.yaml"
        model_name = "llama3.2:3b"
        if config_path.exists():
            try:
                import yaml
                cfg = yaml.safe_load(config_path.read_text())
                model_name = cfg.get("model_name", model_name)
            except Exception:
                pass

        rag = _LightRAG(
            working_dir=str(LIGHT_DIR),
            llm_model_func=ollama_model_complete,
            embedding_func=ollama_embed,
            llm_model_name=model_name,
            llm_model_max_async=2,
            embedding_batch_num=10,
            enable_llm_cache=True,
        )
        asyncio.run(rag.initialize_storages())
        return rag
    except (ConnectionError, Exception) as e:
        print(f"[lightrag] Failed to initialize: {e}")
        return None


def build_index():
    entries = collect_entries()
    if not entries:
        print("[index] No entries found to index.")
        return None

    if HAS_LIGHTRAG and _ollama_running():
        rag = _build_lightrag()
        if rag:
            try:
                import asyncio
                async def do_insert():
                    for i, entry in enumerate(entries):
                        text = entry["text"]
                        meta = entry["meta"]
                        doc_id = f"{meta['source']}::{meta['filename']}::{i}"
                        await rag.ainsert(text, ids=doc_id)
                        if (i + 1) % 10 == 0 or i == len(entries) - 1:
                            print(f"[lightrag] Indexed {i + 1}/{len(entries)} chunks")

                asyncio.run(do_insert())
                print(f"[lightrag] Built LightRAG index with {len(entries)} chunks")
                return rag
            except Exception as e:
                print(f"[lightrag] Build failed: {e}, falling back to TF-IDF")

    idx = TfidfIndex()
    idx.build(entries)
    idx.save(INDEX_PATH)
    print(f"[index] Indexed {len(entries)} chunks from memory (TF-IDF fallback)")
    return idx


def load_index():
    if HAS_LIGHTRAG and _ollama_running():
        try:
            rag = _build_lightrag()
            if rag and any(f.suffix != ".graphml" for f in LIGHT_DIR.iterdir()):
                return rag
        except Exception:
            pass

    if INDEX_PATH.exists():
        return TfidfIndex.load(INDEX_PATH)
    return None


def search_index(query, k=10, mode="hybrid"):
    try:
        from lightrag.base import QueryParam
    except ImportError:
        mode = "tfidf"

    idx = load_index()
    if idx is None:
        return []

    if mode != "tfidf" and hasattr(idx, "query"):
        try:
            param = QueryParam(mode=mode, top_k=k)
            result_text = idx.query(query, param=param)
            return [{
                "score": 1.0,
                "text": str(result_text)[:500],
                "meta": {"source": "lightrag", "filename": "", "date": "", "path": ""}
            }]
        except Exception:
            pass

    if hasattr(idx, "search"):
        return idx.search(query, k)

    return []


def get_index_info():
    idx = load_index()
    if idx is None:
        return {"status": "no_index", "entries": 0}

    if hasattr(idx, "entries"):
        sources = Counter(e["meta"]["source"] for e in idx.entries)
        return {
            "status": "ready",
            "entries": len(idx.entries),
            "source": "lightrag" if HAS_LIGHTRAG and LIGHT_DIR.exists() and any(LIGHT_DIR.iterdir()) else "tfidf",
            "sources": dict(sources),
        }

    return {
        "status": "ready",
        "entries": "lightrag",
        "source": "lightrag",
    }


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    if "--search" in sys.argv:
        q_idx = sys.argv.index("--search")
        if q_idx + 1 < len(sys.argv):
            query = sys.argv[q_idx + 1]
            limit = 10
            mode = "hybrid"
            if "--limit" in sys.argv:
                li = sys.argv.index("--limit")
                limit = int(sys.argv[li + 1])
            if "--mode" in sys.argv:
                mi = sys.argv.index("--mode")
                if mi + 1 < len(sys.argv):
                    mode = sys.argv[mi + 1]
            results = search_index(query, limit, mode)
            if not results:
                print(f'No results for "{query}"')
                return
            print(f'=== LightRAG Search: "{query}" (mode={mode}) ===\n')
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
            print(f"Source: {info.get('source', 'unknown')}")
            print(f"Entries: {info['entries']}")
            if "sources" in info and isinstance(info["sources"], dict):
                print("Sources:")
                for src, count in info["sources"].items():
                    print(f"  {src}: {count}")
        return

    build_index()


if __name__ == "__main__":
    main()
