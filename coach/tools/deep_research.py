"""Deep research agent -- iterative, multi-source, citation-backed.

Enhancements adopted from KResearch (github.com/KuekHaoYang/KResearch):
- Iterative agent loop (LLM decides what to search next)
- MindMap epistemic state (findings, confidence, contradictions)
- Trafilatura content extraction with httpx/bs4 fallback
- Inline citation tracking [1], [2], ...
- Ollama provider (local or cloud)
- Structured report with Executive Summary, thematic sections, contradictions

Usage:
  py -3 coach/tools/deep_research.py "best cctv cameras qatar 2026"
  py -3 coach/tools/deep_research.py "competitor analysis aman qa" --max 4
  py -3 coach/tools/deep_research.py "latest AI SEO trends" --no-llm
  py -3 coach/tools/deep_research.py "quantum computing breakthroughs" --iterative

"""
from __future__ import annotations

import asyncio
import io
import sys

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
import datetime
import json
import logging
import os
import re
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

COACH_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(COACH_DIR))

from tools.insight_ledger import log_insight
WORK_DIR = COACH_DIR / "work" / "research"
WORK_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.WARNING, format="%(levelname)s:%(name)s:%(message)s")
log = logging.getLogger("deep_research")

DEFAULT_MAX_ITERATIONS = 30
DEFAULT_MAX_FETCH = 12
MAX_CONTENT_LEN = 12_000

# ── MindMap — Epistemic State ──────────────────────────────────────────────

@dataclass
class Source:
    url: str
    title: str = ""
    snippet: str = ""

@dataclass
class Contradiction:
    topic: str
    claim_a: str
    claim_b: str
    source_a: Source
    source_b: Source

@dataclass
class Finding:
    topic: str
    content: str
    sources: list[Source] = field(default_factory=list)
    confidence: float = 0.0
    contradictions: list[Contradiction] = field(default_factory=list)

@dataclass
class MindMap:
    query: str
    findings: list[Finding] = field(default_factory=list)
    all_sources: list[Source] = field(default_factory=list)

    def add_finding(self, topic: str, content: str, sources: list[Source], confidence: float) -> Finding:
        for f in self.findings:
            if f.topic.lower() == topic.lower():
                f.content = f"{f.content}\n\n{content}".strip()
                existing_urls = {s.url for s in f.sources}
                for s in sources:
                    if s.url not in existing_urls:
                        f.sources.append(s)
                        existing_urls.add(s.url)
                f.confidence = max(f.confidence, confidence)
                return f
        finding = Finding(topic=topic, content=content, sources=sources, confidence=confidence)
        self.findings.append(finding)
        return finding

    def log_contradiction(self, topic: str, claim_a: str, claim_b: str, source_a: Source, source_b: Source):
        for f in self.findings:
            if f.topic.lower() == topic.lower():
                f.contradictions.append(Contradiction(topic, claim_a, claim_b, source_a, source_b))
                return
        f = Finding(topic=topic, content="", confidence=0.0)
        f.contradictions.append(Contradiction(topic, claim_a, claim_b, source_a, source_b))
        self.findings.append(f)

    def get_summary(self) -> str:
        if not self.findings:
            return "(no findings yet)"
        lines = []
        for f in self.findings:
            conf = f"{f.confidence:.0%}" if f.confidence else "none"
            lines.append(f"- {f.topic}  ({len(f.sources)} sources, confidence: {conf})")
            for c in f.contradictions:
                lines.append(f"  [!] Contradiction: {c.claim_a[:80]} vs {c.claim_b[:80]}")
        return "\n".join(lines)

    def get_gaps(self) -> list[str]:
        return [f.topic for f in self.findings if f.confidence < 0.3]

    def source_count(self) -> int:
        return len(self.all_sources)

    def get_citation(self, url: str) -> int:
        for i, s in enumerate(self.all_sources, 1):
            if s.url == url:
                return i
        return 0

    def record_source(self, url: str, title: str = "", snippet: str = "") -> int:
        for i, s in enumerate(self.all_sources, 1):
            if s.url == url:
                return i
        self.all_sources.append(Source(url=url, title=title, snippet=snippet))
        return len(self.all_sources)

    def to_markdown(self) -> str:
        return self.get_summary()

@dataclass
class ResearchState:
    query: str
    mind_map: MindMap
    iteration: int = 0
    max_iterations: int = DEFAULT_MAX_ITERATIONS
    draft_requested: bool = False
    token_usage: int = 0

    @classmethod
    def create(cls, query: str, max_iterations: int = DEFAULT_MAX_ITERATIONS):
        return cls(query=query, mind_map=MindMap(query=query), max_iterations=max_iterations)

    def increment(self):
        self.iteration += 1

    def is_over_budget(self) -> bool:
        return self.max_iterations > 0 and self.iteration >= self.max_iterations

# ── Tools ───────────────────────────────────────────────────────────────────

async def tool_web_search(query: str, max_results: int = 10) -> dict:
    from tools.web_search import search_web
    results = await asyncio.to_thread(search_web, query, max_results)
    return {"results": results, "count": len(results), "query": query}

async def tool_read_webpage(url: str, max_chars: int = MAX_CONTENT_LEN) -> dict:
    result = await _extract_trafilatura(url)
    if not result:
        result = await _extract_httpx(url)
    if not result:
        return {"error": f"Could not extract content from {url}", "url": url}
    content = result["content"]
    truncated = False
    if len(content) > max_chars:
        content = content[:max_chars] + "\n\n[Content truncated...]"
        truncated = True
    return {
        "content": content,
        "title": result.get("title", ""),
        "url": url,
        "char_count": len(result["content"]),
        "truncated": truncated,
    }

async def _extract_trafilatura(url: str) -> dict | None:
    try:
        import trafilatura
        def _do():
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                return None
            text = trafilatura.extract(downloaded, output_format="markdown", include_links=True, with_metadata=True)
            meta = trafilatura.extract_metadata(downloaded)
            title = meta.title if meta else ""
            if not text:
                return None
            return {"content": text, "title": title, "url": url}
        return await asyncio.to_thread(_do)
    except Exception as e:
        log.debug("trafilatura failed for %s: %s", url, e)
        return None

async def _extract_httpx(url: str) -> dict | None:
    try:
        import httpx
        from bs4 import BeautifulSoup
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()
            title = soup.title.string if soup.title else ""
            content = soup.get_text(separator="\n", strip=True)
            if not content or len(content) < 50:
                return None
            return {"content": content, "title": title, "url": url}
    except Exception as e:
        log.debug("httpx fallback failed for %s: %s", url, e)
        return None

async def tool_update_findings(state: ResearchState, topic: str, content: str, sources: list[dict], confidence: float) -> dict:
    src_objects = [Source(url=s.get("url", ""), title=s.get("title", ""), snippet=s.get("snippet", "")) for s in sources]
    for s in src_objects:
        state.mind_map.record_source(s.url, s.title, s.snippet)
    state.mind_map.add_finding(topic, content, src_objects, confidence)
    return {"status": "ok", "summary": state.mind_map.get_summary()}

async def tool_log_contradiction(state: ResearchState, topic: str, claim_a: str, claim_b: str, source_a: dict, source_b: dict) -> dict:
    state.mind_map.log_contradiction(
        topic, claim_a, claim_b,
        Source(url=source_a.get("url", ""), title=source_a.get("title", "")),
        Source(url=source_b.get("url", ""), title=source_b.get("title", "")),
    )
    return {"status": "ok", "contradictions": len(state.mind_map.findings)}

async def tool_draft_report(state: ResearchState) -> dict:
    src_count = state.mind_map.source_count()
    topic_count = len(state.mind_map.findings)
    if src_count < 6 or topic_count < 2:
        return {
            "status": "rejected",
            "reason": f"Only {src_count} sources across {topic_count} topics. Need at least 6 sources across 2+ topics. Keep researching.",
        }
    state.draft_requested = True
    return {"status": "ready", "sources": src_count, "topics": topic_count}

# ── LLM Providers ───────────────────────────────────────────────────────────

def call_ollama(prompt: str, model: str | None = None, max_tokens: int = 2000) -> str | None:
    try:
        import yaml
    except ImportError:
        yaml = None
    config = {}
    config_path = COACH_DIR / "config.yaml"
    if yaml and config_path.exists():
        try:
            config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    api_url = config.get("api_url", "http://localhost:11434/v1/chat/completions")
    model_name = model or config.get("model_name", "llama3.2:3b")
    try:
        import httpx
        with httpx.Client(timeout=120) as client:
            resp = client.post(api_url, json={
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": max_tokens,
                "stream": False,
            })
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        log.debug("Ollama call failed: %s", e)
    return None

# ── Prompt Templates ────────────────────────────────────────────────────────

AGENT_SYSTEM_PROMPT = """You are a deep research agent. Your goal: produce a thoroughly researched,
citation-backed report on the user's query.

## Research Methodology

### Phase 1 — Decompose
Break the query into 3-7 sub-questions (what, why, how, who, when, debates, implications).

### Phase 2 — Search + Read (repeat)
For EACH sub-question:
1. web_search with a specific targeted query
2. read_webpage on the 2-3 best results
3. update_findings immediately after each read
Continue until ALL sub-questions have real source data.

### Phase 3 — Verify
- Find second sources for claims with 1 source
- Log contradictions with log_contradiction
- Verify numerical claims

### Phase 4 — Synthesize
Only when you have 10+ sources and findings for all sub-questions, call draft_report().
Then write the COMPLETE report as your final message.

## Tools
- web_search(query, max_results=10): Search DuckDuckGo
- read_webpage(url): Extract text from a URL
- update_findings(topic, content, sources, confidence): Record findings
- log_contradiction(topic, claim_a, claim_b, source_a, source_b): Log conflicts
- draft_report(): Signal readiness. Then write the report.

## Citation Rules
Every factual claim MUST have an inline citation [N]. Sequential numbers.
If you CANNOT cite a claim, do NOT include it.

## Report Format
- # Research Report: {{Title}}
- ## Executive Summary (4-6 sentences)
- ## {{Thematic Sections}} (5+ sections with inline citations)
- ## Contradictions & Debates
- ## Limitations
- ## Sources ([1] Title - URL)

## Current State
Query: {query}
Findings:
{mind_map_summary}
Sources: {source_count} | Iteration: {iteration}/{max_iterations}
"""

REPORT_PROMPT = """Write the final research report based on the mind map below.

Mind Map:
{mind_map_summary}

Sources:
{sources}

Requirements:
- Inline citations [1], [2] for every factual claim
- Executive Summary
- 5+ thematic sections with specific data
- Contradictions & Debates section
- Limitations section
- Numbered Sources list
- Minimum 2000 words
"""

TOOL_DESCRIPTIONS = {
    "web_search": {
        "description": "Search the web. Returns title, url, snippet for each result.",
        "params": {
            "query": "The search query (be specific, include year for time-sensitive topics)",
            "max_results": "Maximum results (default 10, max 20)",
        },
    },
    "read_webpage": {
        "description": "Extract clean text content from a URL.",
        "params": {"url": "The full URL to fetch"},
    },
    "update_findings": {
        "description": "Record a finding in the mind map. Do this AFTER every read_webpage.",
        "params": {
            "topic": "Category/topic name",
            "content": "The finding details with numbers and quotes",
            "sources": 'List of {{"url": "...", "title": "...", "snippet": "..."}}',
            "confidence": "Number 0.0-1.0",
        },
    },
    "log_contradiction": {
        "description": "Record a conflict between two sources.",
        "params": {
            "topic": "Topic",
            "claim_a": "First claim",
            "claim_b": "Second claim",
            "source_a": '{{"url": "...", "title": "..."}}',
            "source_b": '{{"url": "...", "title": "..."}}',
        },
    },
    "draft_report": {
        "description": "Signal readiness to write the final report.",
        "params": {},
    },
}

# ── Shared helpers ─────────────────────────────────────────────────────────

def _dedup_urls(results: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for r in results:
        url = r.get("url", "")
        if url and url not in seen:
            seen.add(url)
            unique.append(r)
    return unique

def _extract_next_query(text: str | None) -> str | None:
    if not text:
        return None
    text = text.strip()
    for prefix in ["NEXT_QUERY:", "Next Query:", "next query:"]:
        if prefix in text:
            for line in text.split("\n"):
                if prefix in line:
                    val = line.split(prefix, 1)[1].strip().strip('"').strip("'")
                    if val:
                        val = _clean_query(val)
                        if val:
                            return val
    first_line = text.split("\n")[0].strip()
    first_line = _clean_query(first_line)
    if first_line and len(first_line) > 10 and first_line.lower() != "done":
        return first_line
    return None

def _clean_query(q: str) -> str:
    q = re.sub(r'[\*\#\_\~\`]', '', q)
    q = q.strip().strip('"').strip("'").strip('»').strip('«').strip()
    q = re.sub(r'\s+', ' ', q)
    return q

def _extract_topic(query: str) -> str:
    stop_words = {"what", "is", "are", "the", "best", "top", "how", "to",
                  "does", "do", "in", "for", "of", "and", "a", "an", "2026",
                  "guide", "review", "comparison", "explained", "overview"}
    words = query.lower().split()[:6]
    significant = [w for w in words if w not in stop_words]
    return " ".join(significant[:4]) if significant else query[:40]

def _parse_action(text: str) -> dict | None:
    if not text:
        return None
    try:
        data = json.loads(text)
        if "tool" in data:
            result = {"name": data["tool"], "args": {}}
            for k, v in data.items():
                if k != "tool":
                    result["args"][k] = v
            return result
    except (json.JSONDecodeError, TypeError):
        pass
    lines = text.strip().split("\n")
    action_name = None
    args = {}
    for line in lines:
        line = line.strip()
        if line.upper().startswith("TOOL:"):
            action_name = line[5:].strip().lower()
        elif line.upper().startswith("ARG_") and ":" in line:
            colon_idx = line.index(":")
            key = line[4:colon_idx].strip()
            value = line[colon_idx + 1:].strip()
            args[key] = _coerce_value(value)
    if action_name and action_name in TOOL_DESCRIPTIONS:
        return {"name": action_name, "args": args}
    text_lower = text.lower()
    for tool_name in TOOL_DESCRIPTIONS:
        if tool_name in text_lower:
            return {"name": tool_name, "args": {}}
    return None

def _coerce_value(v: str) -> Any:
    v = v.strip()
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    if v.isdigit():
        return int(v)
    try:
        return json.loads(v)
    except (json.JSONDecodeError, TypeError):
        pass
    return v

def _short_args(a: dict) -> str:
    if not a:
        return ""
    parts = []
    for k, v in a.items():
        s = str(v)
        if len(s) > 60:
            s = s[:57] + "..."
        parts.append(f"{k}='{s}'")
    return ", ".join(parts)

def slugify(text: str) -> str:
    text = re.sub(r"[^a-z0-9\s-]", "", text.lower().strip())
    return re.sub(r"[\s-]+", "-", text)[:60]

def _generate_variations(query: str) -> list[str]:
    base = query.strip().rstrip(".")
    return [base, f"{base} 2026 guide", f"{base} review comparison"]

def _save_report(topic: str, brief: str) -> Path:
    date_str = datetime.date.today().isoformat()
    filename = f"research-{slugify(topic)}-{date_str}.md"
    filepath = WORK_DIR / filename
    filepath.write_text(brief, encoding="utf-8")
    return filepath

# ── LLM Provider Auto-Detect ───────────────────────────────────────────────

_LLM_CACHE: dict[str, str | None] = {"provider": None}

def _ollama_available() -> bool:
    try:
        import httpx
        r = httpx.get("http://localhost:11434/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

def _detect_provider(override: str | None = None) -> str:
    if override and override != "auto":
        return override
    if _LLM_CACHE["provider"]:
        return _LLM_CACHE["provider"]
    if _ollama_available():
        _LLM_CACHE["provider"] = "ollama"
        print("  [LLM] Ollama detected")
        return "ollama"
    print("  [LLM] No LLM provider available — using raw compilation")
    return "none"

def _llm_call_factory(provider: str | None, model: str | None):
    actual = _detect_provider(provider)
    if actual == "ollama":
        def call(prompt: str, max_tokens: int = 2000) -> str | None:
            return call_ollama(prompt, model=model, max_tokens=max_tokens)
        return call
    else:
        def call(prompt: str, max_tokens: int = 2000) -> str | None:
            return None
        return call

# ── Fetch helpers ──────────────────────────────────────────────────────────

async def _fetch_urls(urls: list[dict], pages_data: list, state: ResearchState, label: str = ""):
    for i, r in enumerate(urls, 1):
        url = r.get("url", "")
        title = r.get("title", "") or url[:50]
        prefix = f"    [{i}/{len(urls)}]" + (f" {label}" if label else "")
        print(f"  {prefix} {title[:60]}...")
        page = await tool_read_webpage(url)
        if not page.get("error"):
            page["title"] = title
            pages_data.append(page)
            state.mind_map.record_source(url, title, r.get("snippet", ""))

async def _initial_search(query: str) -> tuple[list[dict], list[dict], list[dict]]:
    queries = list(set([query, f"{query} overview guide", f"{query} 2026", f"{query} explained"]))
    all_results = []
    for q in queries:
        results = await tool_web_search(q, 8)
        all_results.extend(results.get("results", []))
        print(f"    Searched '{q[:50]}' -> {results.get('count', 0)} results")
    unique = _dedup_urls(all_results)
    print(f"  Total unique results: {len(unique)}")
    return unique[:DEFAULT_MAX_FETCH], unique, all_results

# ── Report Generation ───────────────────────────────────────────────────────

def _build_llm_report(query: str, synthesis: str, sources: list[Source]) -> str:
    sources_md = "\n".join(f"[{i}] {s.title} - {s.url}" for i, s in enumerate(sources, 1))
    return (
        f"# Research Report: {query}\n"
        f"**Generated:** {datetime.date.today().isoformat()}\n"
        f"**Method:** LLM-synthesized\n\n"
        f"---\n\n"
        f"{synthesis}\n\n"
        f"---\n\n"
        f"## Sources\n"
        f"{sources_md}\n"
    )

def _build_raw_report(state: ResearchState, pages_data: list | None = None) -> str:
    mm = state.mind_map
    pages = pages_data or []
    lines = [
        f"# Research Report: {state.query}",
        f"**Generated:** {datetime.date.today().isoformat()}",
        f"**Method:** Raw compilation\n",
        "## Executive Summary",
        f"Researched {len(mm.findings)} topics from {mm.source_count()} sources, {len(pages)} pages fetched.\n",
    ]
    if mm.findings:
        for f in mm.findings:
            lines.extend([
                f"\n## {f.topic}",
                f"**Confidence:** {f.confidence:.0%}" if f.confidence else "",
                f"**Sources:** {len(f.sources)}",
                "",
                f.content[:3000] if len(f.content) > 3000 else f.content,
            ])
            if f.contradictions:
                lines.append("\n### Contradictions")
                for c in f.contradictions:
                    lines.append(f"- {c.claim_a[:100]} vs {c.claim_b[:100]}")
    elif pages:
        for p in pages:
            title = p.get("title", "Untitled")
            url = p.get("url", "")
            text = p.get("content", p.get("text", ""))
            lines.append(f"\n## {title}")
            lines.append(f"**URL:** {url}")
            lines.append(text[:3000])
            if len(text) > 3000:
                lines.append("*(truncated)*")
    lines.extend([
        "\n## Sources",
        *[f"[{i}] {s.title} - {s.url}" for i, s in enumerate(mm.all_sources, 1)],
    ])
    return "\n".join(lines)

def _generate_report(state: ResearchState, provider: str | None = None, model: str | None = None, pages_data: list | None = None) -> str:
    mm = state.mind_map
    sources_md = "\n".join(f"[{i}] {s.title} - {s.url}" for i, s in enumerate(mm.all_sources, 1))
    llm = _llm_call_factory(provider, model)
    prompt = REPORT_PROMPT.format(mind_map_summary=mm.to_markdown(), sources=sources_md)
    try:
        synthesis = llm(prompt, max_tokens=3000)
        if synthesis:
            return _build_llm_report(query=state.query, synthesis=synthesis, sources=mm.all_sources)
    except Exception:
        pass
    return _build_raw_report(state, pages_data)

def _build_simple_raw(topic: str, pages: list[dict]) -> str:
    lines = [
        f"# Research: {topic}",
        f"**Generated:** {datetime.date.today().isoformat()}\n",
        "## Sources Found",
    ]
    for p in pages:
        title = p.get("title", "Untitled")
        url = p.get("url", "")
        text = p.get("content", p.get("text", ""))
        lines.append(f"\n### {title}")
        lines.append(f"**URL:** {url}")
        lines.append(f"**Content ({len(text)} chars):**")
        lines.append(text[:3000])
        if len(text) > 3000:
            lines.append("*(truncated)*")
    return "\n".join(lines)

# ── Agent Loop ──────────────────────────────────────────────────────────────

async def _phase2_iterative(state: ResearchState, pages_data: list, llm_think, query: str, max_iterations: int):
    print(f"\n  [Phase 2] Iterative deep-dive (max {max_iterations} iterations)...\n")
    while not state.is_over_budget():
        state.increment()
        remaining = max_iterations - state.iteration + 1

        if state.mind_map.source_count() >= 10 and state.iteration >= 3:
            break
        if state.iteration >= max_iterations:
            break

        prev_findings = "\n".join(
            f"- {p.get('title', '?')[:60]}: {p.get('content', '')[:200]}"
            for p in pages_data[-3:]
        )

        research_prompt = (
            f"Research query: {query}\n\n"
            f"We have found {state.mind_map.source_count()} sources so far across these topics:\n"
            f"{state.mind_map.get_summary() or '(initial search complete)'}\n\n"
            f"Recent content found:\n{prev_findings[:1000]}\n\n"
            f"What specific sub-topic or angle should we search for next "
            f"to deepen this research? ({remaining} iterations remaining)\n\n"
            f"Respond with:\n"
            f"NEXT_QUERY: <your search query suggestion>\n"
            f"REASON: <why this helps>\n\n"
            f"If you think we have enough information for a solid report, respond with:\n"
            f"NEXT_QUERY: done"
        )

        response = llm_think(research_prompt, max_tokens=500)
        if not response:
            print("  [Phase 2] LLM unresponsive, stopping")
            break

        next_query = _extract_next_query(response)
        if not next_query or next_query.lower() in ("done", "stop", "quit"):
            print("  [Phase 2] LLM indicated research is sufficient")
            break

        print(f"  Iteration {state.iteration}: Searching '{next_query[:70]}...'")
        results = await tool_web_search(next_query, 8)
        new_results = results.get("results", [])
        if not new_results:
            print("    No results found, trying next iteration")
            continue

        new_urls = _dedup_urls(new_results)[:4]
        fetched_pages_this_round = []
        for r in new_urls:
            url = r.get("url", "")
            title = r.get("title", "") or url[:50]
            print(f"    Fetching: {title[:60]}...")
            page = await tool_read_webpage(url)
            if not page.get("error"):
                page["title"] = title
                pages_data.append(page)
                fetched_pages_this_round.append(page)
                state.mind_map.record_source(url, title, r.get("snippet", ""))

        topic = _extract_topic(next_query)
        if fetched_pages_this_round:
            combined = "\n\n".join(p.get("content", "")[:500] for p in fetched_pages_this_round)
            await tool_update_findings(
                state, topic, combined[:2000],
                [{"url": p.get("url", ""), "title": p.get("title", "")} for p in fetched_pages_this_round],
                0.7,
            )


async def agent_loop(
    query: str,
    provider: str | None = None,
    model: str | None = None,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
    verbose: bool = False,
) -> tuple[str, ResearchState]:
    state = ResearchState.create(query, max_iterations)
    print(f"\n{'='*60}")
    print(f"  Deep Research: {query}")
    print(f"  Max iterations: {max_iterations}")
    print(f"{'='*60}\n")

    llm_think = _llm_call_factory(provider, model)

    print("  [Phase 1] Initial broad search...")
    top_urls, all_unique, _ = await _initial_search(query)
    print(f"  Fetching top {len(top_urls)} pages...")
    pages_data = []
    await _fetch_urls(top_urls, pages_data, state)

    await _phase2_iterative(state, pages_data, llm_think, query, max_iterations)

    return _generate_report(state, provider, model, pages_data), state


# ── Simple Mode (original behavior) ─────────────────────────────────────────

async def _fetch_and_compile(topic: str, max_per_query: int, try_llm: bool) -> tuple[str, list, str, int]:
    from tools.web_search import search_web
    queries = _generate_variations(topic)
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
    unique = _dedup_urls(all_results)
    print(f"Unique URLs: {len(unique)}")

    top_urls = unique[:8]
    print(f"\nFetching top {len(top_urls)} pages...")
    pages = []
    for i, r in enumerate(top_urls, 1):
        url = r.get("url", "")
        title = r.get("title", "?")
        print(f"  [{i}/{len(top_urls)}] {title[:50]}...")
        page = await tool_read_webpage(url)
        page["title"] = title
        pages.append(page)

    print(f"\nCompiling research brief...")
    return topic, pages, unique, try_llm


async def simple_research(topic: str, max_per_query: int = 5, try_llm: bool = True) -> str:
    print(f"=== Deep Research (Simple Mode): {topic} ===\n")

    topic, pages, unique, try_flag = await _fetch_and_compile(topic, max_per_query, try_llm)
    brief, method, llm_time = _synthesize_or_raw(topic, pages, try_flag)

    filepath = _save_report(topic, brief)
    log_insight("deep_research_complete", {
        "mode": "simple", "query": topic[:60], "pages": len(pages),
        "method": method, "llm_time_ms": llm_time, "sources": len(unique),
    })
    print(f"\n=== Done ===")
    print(f"Method: {'LLM synthesis' if method == 'llm' else 'Raw compilation'}")
    print(f"Pages fetched: {len(pages)}")
    print(f"Saved: {filepath}")
    print(f"\nPreview (first 500 chars):\n")
    print(brief[:500])
    return brief


def _synthesize_or_raw(topic: str, pages: list[dict], try_llm: bool) -> tuple[str, str, int]:
    if not try_llm:
        return _build_simple_raw(topic, pages), "raw", 0
    llm = _llm_call_factory(None, None)
    start_t = time.time()
    synthesis = llm(f"Synthesize research on: {topic}")
    llm_time = int((time.time() - start_t) * 1000)
    if synthesis:
        return _build_llm_report(topic, synthesis, [Source(url=p.get("url", ""), title=p.get("title", "?")) for p in pages]), "llm", llm_time
    print("  No LLM available — using raw compilation")
    return _build_simple_raw(topic, pages), "raw", llm_time


# ── Main ────────────────────────────────────────────────────────────────────

def _run_iterative(topic, provider, model, max_iter, verbose):
    start_time = time.time()
    report, state = asyncio.run(agent_loop(
        query=topic, provider=provider, model=model,
        max_iterations=max_iter, verbose=verbose,
    ))
    filepath = _save_report(topic, report)
    runtime_s = int(time.time() - start_time)
    log_insight("deep_research_complete", {
        "mode": "iterative", "query": topic[:60],
        "sources": state.mind_map.source_count(),
        "topics": len(state.mind_map.findings),
        "iterations": state.iteration, "runtime_s": runtime_s,
    })
    print(f"\n{'='*60}")
    print(f"  [OK] Research complete!")
    print(f"  Topics covered: {len(state.mind_map.findings)}")
    print(f"  Sources: {state.mind_map.source_count()}")
    print(f"  Iterations: {state.iteration}")
    print(f"  Runtime: {runtime_s}s")
    print(f"  Saved: {filepath}")
    print(f"{'='*60}\n")
    print(report[:800])


def _run_simple(topic, max_per, try_llm):
    asyncio.run(simple_research(topic=topic, max_per_query=max_per, try_llm=try_llm))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Deep research agent — multi-source, citation-backed.")
    parser.add_argument("topic", nargs="+", help="Research topic")
    parser.add_argument("--max", type=int, default=5, help="Max results per search query")
    parser.add_argument("--no-llm", action="store_true", help="Skip LLM synthesis, use raw compilation")
    parser.add_argument("--iterative", action="store_true", help="Use iterative agent loop")
    parser.add_argument("--provider", help="LLM provider override")
    parser.add_argument("--model", help="Model name override")
    parser.add_argument("--max-iter", type=int, default=DEFAULT_MAX_ITERATIONS, help="Max iterative iterations")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    topic = " ".join(args.topic)
    if args.max > 0:
        print(f"Max results per query: {args.max}")
    if args.iterative:
        _run_iterative(topic, args.provider, args.model, args.max_iter, args.verbose)
    else:
        _run_simple(topic, args.max, not args.no_llm)


if __name__ == "__main__":
    main()
