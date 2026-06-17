import sys, re, datetime
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent
MEM_DIR = BASE / "memory"
SESS_DIR = MEM_DIR / "sessions"

sys.path.insert(0, str(BASE))
from tools.index_memory import load_index as load_tfidf_index

class MemoryManager:
    """Unified memory manager for Personal Coach 2.0.
    Handles RAG, session history, and context assembly.
    """
    def __init__(self, max_items=5):
        self.max_items = max_items
        self.tfidf_idx = load_tfidf_index()
        self.lightrag_idx = self._load_lightrag()

    def _load_lightrag(self):
        """Attempts to load LightRAG if available and Ollama is running."""
        try:
            from tools.index_memory_lightrag import load_index as load_lr
            return load_lr()
        except Exception:
            return None

    def read_md(self, file_path):
        if not file_path.exists():
            return ""
        return file_path.read_text(encoding="utf-8")

    def get_context_for_query(self, query):
        """Assembles a weighted context based on the current user query."""
        context_parts = []
        
        # 1. RAG Results (Semantic Search)
        rag_results = self.search(query, limit=5)
        if rag_results:
            context_parts.append("RELEVANT MEMORY (RAG):")
            for r in rag_results:
                snippet = r["text"][:300].replace("\n", " ").strip()
                context_parts.append(f"- [{r['meta'].get('source', 'unknown')}] {snippet}")

        # 2. Hard-coded critical context
        goals = self.read_md(MEM_DIR / "goals.md")
        profile = self.read_md(MEM_DIR / "profile.md")
        checkpoint = self.read_md(MEM_DIR / "checkpoint.md")

        if goals: context_parts.append(f"\nACTIVE GOALS:\n{goals}")
        if profile: context_parts.append(f"\nUSER PROFILE:\n{profile}")
        if checkpoint: context_parts.append(f"\nCURRENT CHECKPOINT:\n{checkpoint}")

        # 3. Recent Sessions (Temporal Context)
        sessions = sorted(SESS_DIR.glob("session-*.md"), key=lambda p: p.stem, reverse=True)[:self.max_items]
        if sessions:
            context_parts.append("\nRECENT SESSIONS:")
            for s in sessions:
                txt = self.read_md(s).splitlines()[:10]
                context_parts.append("\n".join(txt))

        return "\n\n".join(context_parts)[:6000]

    def search(self, query, limit=5):
        """Hybrid search across LightRAG and TF-IDF."""
        results = []
        
        # Try LightRAG first
        if self.lightrag_idx and hasattr(self.lightrag_idx, 'query'):
            try:
                from lightrag.base import QueryParam
                res_text = self.lightrag_idx.query(query, param=QueryParam(mode="hybrid", top_k=limit))
                results.append({
                    "score": 1.0,
                    "text": str(res_text),
                    "meta": {"source": "lightrag"}
                })
            except Exception:
                pass

        # Fallback/Augment with TF-IDF
        if self.tfidf_idx:
            try:
                tfidf_res = self.tfidf_idx.search(query, limit)
                results.extend(tfidf_res)
            except Exception:
                pass

        # Deduplicate and sort could go here, but for now we just return
        return results[:limit]

    def store_session(self, skill, duration_min, rating, notes="", decisions=None):
        """Stores a new session and triggers index refresh via tools."""
        import uuid
        sid = str(uuid.uuid4())
        now = datetime.datetime.now(datetime.timezone.utc)
        timestamp = now.isoformat()
        filename = now.strftime("session-%Y%m%d-%H%M%S") + ".md"
        
        decision_block = ""
        if decisions:
            decision_block = "decisions:\n" + "".join(f'  - "{d}"\n' for d in decisions)

        content = (
            f"---\n"
            f"id: {sid}\n"
            f"date: {timestamp}\n"
            f"skill: {skill}\n"
            f"duration_min: {duration_min}\n"
            f"rating: {rating}\n"
            f"notes: |\n"
            f"  {notes}\n"
            f"{decision_block}"
            f"tags: []\n"
            f"---\n"
        )
        fpath = SESS_DIR / filename
        fpath.write_text(content, encoding="utf-8")
        
        # Refresh indices (LightRAG/TF-IDF)
        try:
            from tools.index_memory_lightrag import build_index
            build_index()
        except Exception:
            pass
            
        return fpath
