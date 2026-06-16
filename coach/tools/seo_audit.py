"""Full on-page + technical SEO audit for any URL.
Checks meta, headings, schema, robots, sitemap, social tags, AI crawlers,
content depth, images, internal links, sampled pages from sitemap.

Usage:
  py -3 coach/tools/seo_audit.py <url>
  py -3 coach/tools/seo_audit.py <url> --json
  py -3 coach/tools/seo_audit.py <url> --crawl
  py -3 coach/tools/seo_audit.py <url> --crawl --max-pages 10
  py -3 coach/tools/seo_audit.py <url> --backlinks
  py -3 coach/tools/seo_audit.py <url> --speed
  py -3 coach/tools/seo_audit.py <url> --crawl --backlinks --speed
"""
import sys, json, re, time
from urllib.parse import urlparse, urljoin
from collections import Counter, defaultdict
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
TIMEOUT = 15
CRAWL_DELAY = 0.5

AI_CRAWLERS = {
    "GPTBot": "OpenAI (training)",
    "ChatGPT-User": "OpenAI (browsing/citation)",
    "ClaudeBot": "Anthropic (training)",
    "PerplexityBot": "Perplexity (search+training)",
    "Google-Extended": "Google (Gemini training)",
    "CCBot": "Common Crawl (dataset)",
    "Bytespider": "ByteDance (training)",
    "Applebot-Extended": "Apple (Apple Intelligence training)",
}


def fetch_soup(url):
    resp = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml"), resp


def check_robots(base_url):
    robots_url = base_url.rstrip("/") + "/robots.txt"
    try:
        resp = requests.get(robots_url, timeout=TIMEOUT, headers=HEADERS)
        if resp.status_code != 200:
            return {"status": "missing", "code": resp.status_code}
        text = resp.text
        blocked_ai = []
        for bot, desc in AI_CRAWLERS.items():
            needle = f"Disallow: /"
            if needle in text and bot in text:
                blocked_ai.append({"bot": bot, "purpose": desc})
        return {
            "status": "ok",
            "has_sitemap": "sitemap:" in text.lower(),
            "ai_bots_blocked": blocked_ai,
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def check_sitemap(base_url):
    for path in ["/sitemap.xml", "/sitemap_index.xml"]:
        try:
            resp = requests.get(base_url.rstrip("/") + path, timeout=TIMEOUT, headers=HEADERS)
            if resp.status_code == 200 and "<?xml" in resp.text[:200]:
                urls = re.findall(r"<loc>(.*?)</loc>", resp.text)
                return {"status": "ok", "url_count": len(urls), "path": path, "urls": urls}
        except Exception:
            pass
    return {"status": "missing", "urls": []}


def categorize_url(url, base_domain):
    path = urlparse(url).path.lower()
    if "/blog/" in path or "/article" in path:
        return "blog"
    if "/product" in path or "/products/" in path or "/shop/" in path:
        return "product"
    if "/category" in path or "/categories/" in path:
        return "category"
    if "/tag" in path or "/tags/" in path:
        return "tag"
    if path in ("/", ""):
        return "home"
    return "page"


CC_INDEXES = [
    "CC-MAIN-2025-22",
    "CC-MAIN-2025-18",
    "CC-MAIN-2025-13",
    "CC-MAIN-2025-09",
    "CC-MAIN-2025-04",
]


def check_backlinks(domain):
    """Query Common Crawl CDX API for backlinks (free, no API key)."""
    backlinks = []
    total_pages = 0
    for idx in CC_INDEXES:
        try:
            url = f"http://index.commoncrawl.org/{idx}-index?url={domain}&output=json&limit=100"
            resp = requests.get(url, timeout=30, headers=HEADERS)
            if resp.status_code != 200:
                continue
            for line in resp.text.strip().split("\n"):
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    src = record.get("source", record.get("url", ""))
                    if src:
                        backlinks.append({
                            "source": src,
                            "timestamp": record.get("timestamp", ""),
                            "status": record.get("status", ""),
                        })
                except (json.JSONDecodeError, KeyError):
                    pass
        except Exception:
            pass
        time.sleep(0.3)

    referring_domains = set()
    for bl in backlinks:
        try:
            referring_domains.add(urlparse(bl["source"]).netloc)
        except Exception:
            pass

    return {
        "total_backlinks": len(backlinks),
        "referring_domains": len(referring_domains),
        "sample_sources": [bl["source"] for bl in backlinks[:10]],
    }


def check_backlinks_fast(domain):
    """Quick check using only the most recent CC index."""
    try:
        url = f"http://index.commoncrawl.org/{CC_INDEXES[0]}-index?url={domain}&output=json&limit=20"
        resp = requests.get(url, timeout=15, headers=HEADERS)
        if resp.status_code != 200:
            return {"total_backlinks": 0, "referring_domains": 0, "note": "CC index unavailable"}
        count = len(resp.text.strip().split("\n")) if resp.text.strip() else 0
        domains = set()
        for line in resp.text.strip().split("\n"):
            if not line:
                continue
            try:
                record = json.loads(line)
                src = record.get("source", record.get("url", ""))
                if src:
                    domains.add(urlparse(src).netloc)
            except Exception:
                pass
        return {"total_backlinks": count, "referring_domains": len(domains)}
    except Exception as e:
        return {"total_backlinks": 0, "referring_domains": 0, "error": str(e)}


def check_pagespeed(url):
    """Check page speed via Google PageSpeed Insights API (free, no key).
    Falls back to simple load time measurement if API rate-limited."""
    api = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    try:
        resp = requests.get(api, params={"url": url, "strategy": "mobile"}, timeout=20, headers=HEADERS)
        if resp.status_code == 429:
            # Rate limited -- do simple timing instead
            start = time.time()
            r = requests.get(url, timeout=15, headers=HEADERS)
            elapsed = round(time.time() - start, 2)
            return {
                "performance_score": None,
                "load_time_sec": elapsed,
                "note": "Google API rate-limited, used basic load time instead",
            }
        if resp.status_code != 200:
            return {"error": f"API returned {resp.status_code}"}
        data = resp.json()
        lh = data.get("lighthouseResult", {})
        audits = lh.get("audits", {})

        performance = lh.get("categories", {}).get("performance", {}).get("score")
        if performance is not None:
            performance = round(performance * 100)

        lcp = audits.get("largest-contentful-paint", {}).get("displayValue")
        inp = audits.get("interaction-to-next-paint", {}).get("displayValue")
        cls = audits.get("cumulative-layout-shift", {}).get("displayValue")
        tbt = audits.get("total-blocking-time", {}).get("displayValue")

        return {
            "performance_score": performance,
            "lcp": lcp,
            "inp": inp or audits.get("max-potential-fid", {}).get("displayValue"),
            "cls": cls,
            "tbt": tbt,
        }
    except Exception as e:
        return {"error": str(e)}


def check_meta(soup):
    findings = {}
    title = soup.find("title")
    findings["title"] = title.get_text(strip=True) if title else None
    if findings["title"]:
        findings["title_length"] = len(findings["title"])
    desc = soup.find("meta", attrs={"name": "description"})
    findings["description"] = desc.get("content", "").strip() if desc else None
    if findings["description"]:
        findings["description_length"] = len(findings["description"])
    viewport = soup.find("meta", attrs={"name": "viewport"})
    findings["viewport"] = bool(viewport)
    canonical = soup.find("link", attrs={"rel": "canonical"})
    findings["canonical"] = canonical.get("href") if canonical else None
    robots_meta = soup.find("meta", attrs={"name": "robots"})
    findings["robots_meta"] = robots_meta.get("content") if robots_meta else "index, follow (implied)"
    lang = soup.find("html").get("lang") if soup.find("html") else None
    findings["html_lang"] = lang
    return findings


def check_headings(soup):
    h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
    h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]
    h3s = [h.get_text(strip=True) for h in soup.find_all("h3")]
    return {
        "h1_count": len(h1s),
        "h1_tags": h1s[:3],
        "h2_count": len(h2s),
        "h2_tags": h2s[:5],
        "h3_count": len(h3s),
        "h3_tags": h3s[:5],
    }


def check_schema(soup):
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    types = []
    errors = 0
    for s in scripts:
        try:
            data = json.loads(s.string)
            if isinstance(data, dict):
                types.append(data.get("@type", "unknown"))
            elif isinstance(data, list):
                for item in data:
                    types.append(item.get("@type", "unknown"))
        except Exception:
            errors += 1
    return {"present": len(scripts) > 0, "count": len(scripts), "types": types, "parse_errors": errors}


def check_social_tags(soup):
    og = {}
    for meta in soup.find_all("meta", attrs={"property": re.compile(r"^og:")}):
        og[meta.get("property")] = meta.get("content")
    twitter = {}
    for meta in soup.find_all("meta", attrs={"name": re.compile(r"^twitter:")}):
        twitter[meta.get("name")] = meta.get("content")
    return {"og": og, "twitter": twitter}


def check_images(soup, base_url):
    imgs = soup.find_all("img")
    total = len(imgs)
    missing_alt = 0
    empty_alt = 0
    no_src = 0
    for img in imgs:
        alt = img.get("alt", "")
        if alt is None:
            missing_alt += 1
        elif alt.strip() == "":
            empty_alt += 1
        if not img.get("src"):
            no_src += 1
    return {
        "total": total,
        "missing_alt": missing_alt,
        "empty_alt": empty_alt,
        "with_alt": total - missing_alt - empty_alt,
        "no_src": no_src,
    }


def check_internal_links(soup, base_domain, base_url):
    links = soup.find_all("a", href=True)
    internal = 0
    external = 0
    nofollow = 0
    broken = 0
    linked_pages = set()
    for a in links:
        href = a.get("href", "")
        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue
        if href.startswith("/") or base_domain in href:
            internal += 1
            full_url = urljoin(base_url, href)
            linked_pages.add(full_url.rstrip("/"))
            rel = a.get("rel", [])
            if isinstance(rel, list) and "nofollow" in rel:
                nofollow += 1
        elif href.startswith("http"):
            external += 1
    return {
        "internal": internal,
        "external": external,
        "nofollow": nofollow,
        "unique_linked_pages": len(linked_pages),
    }


def check_content(soup):
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    words = text.split()
    word_count = len(words)
    paragraphs = len(soup.find_all("p"))
    return {"word_count": word_count, "paragraph_count": paragraphs}


def check_page_quality(soup):
    text = soup.get_text(separator=" ", strip=True).lower()
    signals = {
        "no_products": "no products" in text or "no items" in text or "nothing here" in text,
        "coming_soon": any(t in text for t in ["coming soon", "check back later", "under construction"]),
        "placeholder_lorem": "lorem ipsum" in text or "placeholder" in text,
    }
    return signals


def audit_url(url: str, with_crawl: bool = False, max_pages: int = 5, with_backlinks: bool = False, with_speed: bool = False) -> dict:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    base_domain = parsed.netloc

    results = {"url": url, "base_url": base_url}

    try:
        soup, resp = fetch_soup(url)
        results["status_code"] = resp.status_code
        results["page_size_kb"] = round(len(resp.content) / 1024, 1)
        results["meta"] = check_meta(soup)
        results["headings"] = check_headings(soup)
        results["schema"] = check_schema(soup)
        results["social"] = check_social_tags(soup)
        results["ssl"] = {"https": parsed.scheme == "https"}
        results["images"] = check_images(soup, base_url)
        results["internal_links"] = check_internal_links(soup, base_domain, base_url)
        results["content"] = check_content(soup)
        results["quality_signals"] = check_page_quality(soup)
    except Exception as e:
        return {"url": url, "error": f"Page fetch failed: {e}"}

    results["robots"] = check_robots(base_url)
    results["sitemap"] = check_sitemap(base_url)

    issues = []
    meta = results.get("meta", {})

    if meta.get("title_length", 0) < 30:
        issues.append({"severity": "high", "issue": "Title too short", "detail": f"{meta.get('title_length', 0)} chars (min 30)"})
    elif meta.get("title_length", 0) > 60:
        issues.append({"severity": "medium", "issue": "Title may truncate in SERP", "detail": f"{meta.get('title_length', 0)} chars (max 60)"})
    if not meta.get("title"):
        issues.append({"severity": "high", "issue": "Missing <title> tag"})

    if meta.get("description_length", 0) < 120 and meta.get("description_length", 0) > 0:
        issues.append({"severity": "medium", "issue": "Meta description too short", "detail": f"{meta.get('description_length', 0)} chars (target 150-160)"})
    elif meta.get("description_length", 0) > 160:
        issues.append({"severity": "low", "issue": "Meta description may truncate", "detail": f"{meta.get('description_length', 0)} chars"})
    if not meta.get("description"):
        issues.append({"severity": "high", "issue": "Missing meta description"})
    if not meta.get("viewport"):
        issues.append({"severity": "high", "issue": "Missing viewport meta tag"})
    if not meta.get("canonical"):
        issues.append({"severity": "medium", "issue": "Missing canonical URL"})
    if not meta.get("html_lang"):
        issues.append({"severity": "low", "issue": "Missing lang attribute on <html>"})

    headings = results.get("headings", {})
    if headings.get("h1_count", 0) == 0:
        issues.append({"severity": "high", "issue": "No H1 tag on page"})
    elif headings.get("h1_count", 0) > 1:
        issues.append({"severity": "low", "issue": f"Multiple H1s ({headings['h1_count']})"})
    if headings.get("h2_count", 0) == 0:
        issues.append({"severity": "medium", "issue": "No H2 headings (poor structure)"})

    imgs = results.get("images", {})
    if imgs.get("total", 0) > 0:
        pct_missing = round((imgs.get("missing_alt", 0) / imgs["total"]) * 100) if imgs["total"] > 0 else 0
        if imgs.get("missing_alt", 0) > 0:
            issues.append({"severity": "medium", "issue": f"Images missing alt text", "detail": f"{imgs['missing_alt']}/{imgs['total']} ({pct_missing}%)"})
        if imgs.get("no_src", 0) > 0:
            issues.append({"severity": "medium", "issue": f"Images with no src attribute", "detail": f"{imgs['no_src']}"})

    content = results.get("content", {})
    wc = content.get("word_count", 0)
    if wc < 300:
        issues.append({"severity": "medium", "issue": "Thin content", "detail": f"{wc} words (min 300 for non-trivial pages)"})
    elif wc < 600:
        issues.append({"severity": "low", "issue": "Below average content depth", "detail": f"{wc} words"})

    quality = results.get("quality_signals", {})
    if quality.get("no_products"):
        issues.append({"severity": "high", "issue": "Category/page shows no products", "detail": "Page displays 'no products' or 'no items' message"})
    if quality.get("coming_soon"):
        issues.append({"severity": "medium", "issue": "Page shows placeholder/coming soon content"})
    if quality.get("placeholder_lorem"):
        issues.append({"severity": "high", "issue": "Page contains lorem ipsum placeholder text"})

    robots = results.get("robots", {})
    if robots.get("status") == "missing":
        issues.append({"severity": "medium", "issue": "No robots.txt found"})
    if robots.get("ai_bots_blocked"):
        issues.append({"severity": "info", "issue": f"AI training crawlers blocked in robots.txt", "detail": f"{len(robots['ai_bots_blocked'])} crawlers restricted"})

    smap = results.get("sitemap", {})
    if smap.get("status") == "missing":
        issues.append({"severity": "medium", "issue": "No XML sitemap found"})

    schema = results.get("schema", {})
    if not schema.get("present"):
        issues.append({"severity": "medium", "issue": "No JSON-LD schema detected"})

    if not results.get("ssl", {}).get("https"):
        issues.append({"severity": "critical", "issue": "Page not served over HTTPS"})

    # ── multi-page crawl ─────────────────────────────────
    if with_crawl:
        smap_urls = smap.get("urls", [])
        if smap_urls:
            categories = Counter()
            sampled = []
            for u in smap_urls[:max_pages * 3]:
                cat = categorize_url(u, base_domain)
                categories[cat] += 1
            for cat in ("category", "tag", "product", "blog", "page"):
                for u in smap_urls:
                    if categorize_url(u, base_domain) == cat and len(sampled) < max_pages:
                        sampled.append(u)
                        break
            while len(sampled) < min(max_pages, len(smap_urls)):
                for u in smap_urls:
                    if u not in sampled:
                        sampled.append(u)
                        break
            results["sitemap_breakdown"] = dict(categories)

            page_results = []
            for pu in sampled[:max_pages]:
                try:
                    time.sleep(CRAWL_DELAY)
                    psoup, presp = fetch_soup(pu)
                    pmeta = check_meta(psoup)
                    pcontent = check_content(psoup)
                    pimgs = check_images(psoup, base_url)
                    pquality = check_page_quality(psoup)
                    plinks = check_internal_links(psoup, base_domain, base_url)
                    page_results.append({
                        "url": pu,
                        "type": categorize_url(pu, base_domain),
                        "status": presp.status_code,
                        "title": pmeta.get("title"),
                        "word_count": pcontent["word_count"],
                        "paragraphs": pcontent["paragraph_count"],
                        "images": pimgs["total"],
                        "images_missing_alt": pimgs["missing_alt"],
                        "quality_signals": pquality,
                        "internal_links": plinks["internal"],
                        "external_links": plinks["external"],
                    })
                    if pquality.get("no_products"):
                        issues.append({"severity": "high", "issue": f"Empty page: {pu}", "detail": "Shows 'no products' / empty state"})
                    if pcontent["word_count"] < 100:
                        issues.append({"severity": "medium", "issue": f"Very thin page: {pu}", "detail": f"Only {pcontent['word_count']} words"})
                    if not pmeta.get("title"):
                        issues.append({"severity": "high", "issue": f"Missing title on: {pu}"})
                    if pimgs["missing_alt"] > 0:
                        issues.append({"severity": "medium", "issue": f"Missing alt text on page: {pu}", "detail": f"{pimgs['missing_alt']} images"})
                except Exception:
                    page_results.append({"url": pu, "error": "fetch failed"})
            results["sampled_pages"] = page_results

    # ── backlinks ──────────────────────────────────────────
    if with_backlinks:
        bl = check_backlinks_fast(base_domain)
        results["backlinks"] = bl
        if bl.get("total_backlinks", 0) == 0:
            issues.append({"severity": "info", "issue": "No backlinks found in Common Crawl index", "detail": "Site may be too new or lack external links"})
        elif bl.get("total_backlinks", 0) < 10:
            issues.append({"severity": "low", "issue": "Very few backlinks", "detail": f"{bl['total_backlinks']} backlinks from {bl.get('referring_domains', '?')} domains"})
    else:
        results["backlinks"] = None

    # ── page speed ─────────────────────────────────────────
    if with_speed:
        ps = check_pagespeed(url)
        results["pagespeed"] = ps
        if "error" in ps:
            issues.append({"severity": "info", "issue": "Page speed check failed", "detail": ps["error"]})
        elif ps.get("load_time_sec"):
            lt = ps["load_time_sec"]
            if lt > 5:
                issues.append({"severity": "medium", "issue": "Slow page load time", "detail": f"{lt}s (basic measurement)"})
            elif lt > 3:
                issues.append({"severity": "low", "issue": "Moderate page load time", "detail": f"{lt}s (basic measurement)"})
        else:
            score = ps.get("performance_score")
            if score is not None:
                if score < 50:
                    issues.append({"severity": "high", "issue": "Poor page speed", "detail": f"Performance score: {score}/100"})
                elif score < 70:
                    issues.append({"severity": "medium", "issue": "Below average page speed", "detail": f"Performance score: {score}/100"})
                elif score < 90:
                    issues.append({"severity": "low", "issue": "Room for page speed improvement", "detail": f"Performance score: {score}/100"})
            elif "error" not in ps:
                issues.append({"severity": "info", "issue": "Page speed data incomplete"})
    else:
        results["pagespeed"] = None

    results["issues"] = issues
    results["issue_count"] = len(issues)
    results["critical"] = sum(1 for i in issues if i["severity"] == "critical")
    results["high"] = sum(1 for i in issues if i["severity"] == "high")
    results["medium"] = sum(1 for i in issues if i["severity"] == "medium")
    results["low"] = sum(1 for i in issues if i["severity"] == "low")
    results["info"] = sum(1 for i in issues if i["severity"] == "info")

    return results


def format_report(r):
    lines = []
    lines.append(f"=== SEO Audit: {r['url']} ===")
    lines.append(f"Status: {r.get('status_code', '?')} | Size: {r.get('page_size_kb', '?')}KB")
    lines.append("")

    if "error" in r:
        lines.append(f"ERROR: {r['error']}")
        return "\n".join(lines)

    meta = r.get("meta", {})
    lines.append("-- Meta Tags --")
    lines.append(f"  Title:       {meta.get('title', 'MISSING')} ({meta.get('title_length', 0)} chars)")
    lines.append(f"  Description: {meta.get('description', 'MISSING')[:80] or 'MISSING'} ({meta.get('description_length', 0)} chars)")
    lines.append(f"  Viewport:    {'YES' if meta.get('viewport') else 'NO'}")
    lines.append(f"  Canonical:   {meta.get('canonical', 'MISSING')}")
    lines.append(f"  Robots:      {meta.get('robots_meta', '?')}")
    lines.append(f"  HTML lang:   {meta.get('html_lang', 'MISSING')}")

    headings = r.get("headings", {})
    lines.append("")
    lines.append("-- Headings --")
    lines.append(f"  H1: {headings.get('h1_count', 0)} -- {'; '.join(headings.get('h1_tags', []) or ['(none)'])}")
    lines.append(f"  H2: {headings.get('h2_count', 0)} -- {'; '.join(headings.get('h2_tags', []) or ['(none)'])}")
    lines.append(f"  H3: {headings.get('h3_count', 0)}")

    content = r.get("content", {})
    lines.append("")
    lines.append("-- Content --")
    lines.append(f"  Words:       {content.get('word_count', 0)}")
    lines.append(f"  Paragraphs:  {content.get('paragraph_count', 0)}")

    imgs = r.get("images", {})
    lines.append("")
    lines.append("-- Images --")
    lines.append(f"  Total:       {imgs.get('total', 0)}")
    lines.append(f"  With alt:    {imgs.get('with_alt', 0)}")
    lines.append(f"  Missing alt: {imgs.get('missing_alt', 0)}")
    lines.append(f"  Empty alt:   {imgs.get('empty_alt', 0)}")

    links = r.get("internal_links", {})
    lines.append("")
    lines.append("-- Internal Links --")
    lines.append(f"  Internal:    {links.get('internal', 0)}")
    lines.append(f"  External:    {links.get('external', 0)}")
    lines.append(f"  Nofollow:    {links.get('nofollow', 0)}")
    lines.append(f"  Unique URLs: {links.get('unique_linked_pages', 0)}")

    schema = r.get("schema", {})
    lines.append("")
    lines.append("-- Schema --")
    lines.append(f"  Blocks:      {schema.get('count', 0)} -- Types: {', '.join(schema.get('types', []) or ['none'])}")

    social = r.get("social", {})
    lines.append("")
    lines.append("-- Social Tags --")
    lines.append(f"  OG tags:     {len(social.get('og', {}))}")
    lines.append(f"  Twitter tags: {len(social.get('twitter', {}))}")

    robots = r.get("robots", {})
    smap = r.get("sitemap", {})
    lines.append("")
    lines.append("-- Infrastructure --")
    lines.append(f"  robots.txt:     {robots.get('status', '?')}")
    if robots.get("has_sitemap"):
        lines.append("  Sitemap ref:    YES in robots.txt")
    if robots.get("ai_bots_blocked"):
        for b in robots["ai_bots_blocked"]:
            lines.append(f"  AI blocked:     {b['bot']} ({b['purpose']})")
    lines.append(f"  XML sitemap:    {smap.get('status', '?')}" + (f" ({smap.get('url_count', 0)} URLs)" if smap.get('url_count') else ""))
    lines.append(f"  HTTPS:          {'YES' if r.get('ssl', {}).get('https') else 'NO'}")

    bl = r.get("backlinks")
    if bl:
        lines.append("")
        lines.append("-- Backlinks (Common Crawl) --")
        lines.append(f"  Total:          {bl.get('total_backlinks', 0)}")
        lines.append(f"  Referring domains: {bl.get('referring_domains', 0)}")
        err = bl.get("error")
        if err:
            lines.append(f"  Error:          {err}")
        sample = bl.get("sample_sources")
        if sample:
            lines.append(f"  Sample sources: ")
            for s in sample[:5]:
                lines.append(f"    {s[:90]}")

    ps = r.get("pagespeed")
    if ps and "error" not in ps:
        lines.append("")
        if ps.get("load_time_sec"):
            lines.append("-- Page Speed (Basic) --")
            lines.append(f"  Load time:   {ps['load_time_sec']}s")
        else:
            lines.append("-- Page Speed (Google) --")
            lines.append(f"  Performance: {ps.get('performance_score', '?')}/100")
            lcp = ps.get("lcp")
            if lcp:
                lines.append(f"  LCP:         {lcp}")
            inp = ps.get("inp")
            if inp:
                lines.append(f"  INP:         {inp}")
            cls = ps.get("cls")
            if cls:
                lines.append(f"  CLS:         {cls}")

    sitemap_breakdown = r.get("sitemap_breakdown", {})
    if sitemap_breakdown:
        lines.append("")
        lines.append("-- Sitemap Breakdown --")
        for cat, count in sorted(sitemap_breakdown.items(), key=lambda x: -x[1]):
            lines.append(f"  {cat}: {count}")

    sampled = r.get("sampled_pages", [])
    if sampled:
        lines.append("")
        lines.append("-- Sampled Pages --")
        for p in sampled:
            err = p.get("error", "")
            if err:
                lines.append(f"  [ERR] {p['url']} -- {err}")
            else:
                qs = p.get("quality_signals", {})
                flags = []
                if qs.get("no_products"):
                    flags.append("EMPTY")
                if qs.get("coming_soon"):
                    flags.append("PLACEHOLDER")
                flag_str = f" <{','.join(flags)}>" if flags else ""
                alt_missing = p.get("images_missing_alt", 0)
                alt_str = f" alt-miss:{alt_missing}" if alt_missing else ""
                lines.append(f"  [{p.get('type','?')}] {p.get('word_count', 0)}w{alt_str}{flag_str}")
                lines.append(f"        {p.get('title', 'NO TITLE')[:60]}")
                lines.append(f"        {p['url']}")

    issues = r.get("issues", [])
    if issues:
        lines.append("")
        lines.append(f"-- Issues Found ({r.get('issue_count', 0)}) --")
        for sev in ("critical", "high", "medium", "low", "info"):
            for i in issues:
                if i["severity"] == sev:
                    label = sev.upper()
                    detail = f" -- {i['detail']}" if "detail" in i else ""
                    lines.append(f"  [{label}] {i['issue']}{detail}")

    lines.append("")
    lines.append(f"Summary: {r.get('critical', 0)} critical, {r.get('high', 0)} high, {r.get('medium', 0)} medium, {r.get('low', 0)} low, {r.get('info', 0)} info")
    if sampled:
        lines.append(f"Pages sampled: {len(sampled)} (use --crawl to adjust)")
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    json_output = "--json" in args
    with_crawl = "--crawl" in args
    with_backlinks = "--backlinks" in args
    with_speed = "--speed" in args
    max_pages = 5
    skip_indices = set()
    for i, a in enumerate(args):
        if a == "--max-pages" and i + 1 < len(args):
            try:
                max_pages = int(args[i + 1])
                skip_indices.add(i + 1)
            except (ValueError, IndexError):
                pass
        elif a.startswith("--max-pages="):
            try:
                max_pages = int(a.split("=")[1])
            except (ValueError, IndexError):
                pass

    urls = [a for idx, a in enumerate(args) if not a.startswith("--") and idx not in skip_indices]

    for url in urls:
        result = audit_url(url, with_crawl=with_crawl, max_pages=max_pages, with_backlinks=with_backlinks, with_speed=with_speed)
        if json_output:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(format_report(result))
            print()


if __name__ == "__main__":
    main()
