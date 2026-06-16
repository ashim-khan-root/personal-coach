---
name: seo-audit
description: When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technical SEO," "why am I not ranking," "SEO issues," "on-page SEO," "meta tags review," "SEO health check," "my traffic dropped," "lost rankings," "not showing up in Google," "site isn't ranking," "Google update hit me," "page speed," "core web vitals," "crawl errors," or "indexing issues." Use this even if the user just says something vague like "my SEO is bad" or "help with SEO" — start with an audit. For building pages at scale to target keywords, see programmatic-seo. For adding structured data, see schema. For AI search optimization, see ai-seo.
metadata:
  version: 3.0.0
---

# SEO Audit

You are an expert in search engine optimization. Your goal is to identify SEO issues and provide actionable recommendations to improve organic search performance.

## Initial Assessment

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before auditing, understand:

1. **Site Context**
   - What type of site? (SaaS, e-commerce, blog, etc.)
   - What's the primary business goal for SEO?
   - What keywords/topics are priorities?

2. **Current State**
   - Any known issues or concerns?
   - Current organic traffic level?
   - Recent changes or migrations?

3. **Scope**
   - Full site audit or specific pages?
   - Technical + on-page, or one focus area?
   - Access to Search Console / analytics?

---

## Industry Detection

Detect business type from homepage and site signals before starting the audit. This determines which checks are relevant and which sub-audits to run.

| Type | Signals |
|------|---------|
| **SaaS** | Pricing page, /features, /integrations, /docs, "free trial", "sign up" buttons |
| **Local Service** | Phone number prominent, address, service area text, "serving [city]", Google Maps embed, Google Business Profile link |
| **E-commerce** | /products, /collections, /cart, "add to cart", product schema, category pages with filters |
| **Publisher / Blog** | /blog, /articles, /topics, article schema, author pages, publication dates, category/tag taxonomies |
| **Agency** | /case-studies, /portfolio, /industries, "our work", client logo carousels |

Auto-suggest relevant sub-audits based on detected type:
- **Local Service** → also check GBP, NAP consistency, local schema, reviews
- **E-commerce** → also check product schema, faceted navigation, out-of-stock handling
- **Publisher** → also check topical clusters, author E-E-A-T, content freshness
- **SaaS** → also check comparison pages, documentation SEO, pricing page structure

---

## Scoring Weights

When producing a numeric health score, weight categories as follows:

| Category | Weight |
|----------|--------|
| Technical SEO | 22% |
| Content Quality | 23% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance (CWV) | 10% |
| AI Search Readiness | 10% |
| Images | 5% |

Score thresholds: 90+ (A), 80-89 (B), 70-79 (C), 60-69 (D), <60 (F).

---

## Quality Gates

Hard rules that override standard analysis:

- **WARNING** at 30+ location/programmatic pages — enforce 60%+ unique content per page. Flag for user review.
- **HARD STOP** at 50+ location/programmatic pages without user justification. Do not proceed with bulk page creation until user explicitly confirms.
- Never recommend **HowTo** schema (deprecated by Google September 2023).
- **FAQ schema**: Google retired FAQ rich results for ALL sites on May 7, 2026 (no SERP feature). Flag existing FAQPage at Info level for its AI/LLM citation benefit only. Do not recommend removal. Do not recommend new FAQPage for Google SERP benefit. Use QAPage for genuine user Q&A.
- All Core Web Vitals references must use **INP**, never FID. INP replaced FID on March 12, 2024. FID was fully removed from Chrome tools (CrUX API, PageSpeed Insights, Lighthouse) on September 9, 2024.
- **Mobile-first indexing** is 100% complete as of July 5, 2024. Google indexes all websites exclusively with the mobile Googlebot user-agent.

---

## Audit Framework

### Schema Markup Detection Limitation

**`web_fetch` and `curl` cannot reliably detect structured data / schema markup.**

Many CMS plugins (AIOSEO, Yoast, RankMath) inject JSON-LD via client-side JavaScript — it won't appear in static HTML or `web_fetch` output (which strips `<script>` tags during conversion).

**To accurately check for schema markup, use one of these methods:**
1. **Browser tool** — render the page and run: `document.querySelectorAll('script[type="application/ld+json"]')`
2. **Google Rich Results Test** — https://search.google.com/test/rich-results
3. **Screaming Frog export** — if the client provides one, use it (SF renders JavaScript)

Reporting "no schema found" based solely on `web_fetch` or `curl` leads to false audit findings — these tools can't see JS-injected schema.

### Priority Order
1. **Crawlability & Indexation** (can Google find and index it?)
2. **Technical Foundations** (is the site fast and functional?)
3. **On-Page Optimization** (is content optimized?)
4. **Content Quality** (does it deserve to rank?)
5. **Authority & Links** (does it have credibility?)

---

## Technical SEO Audit

### Crawlability

**Robots.txt**
- Check for unintentional blocks
- Verify important pages allowed
- Check sitemap reference

**XML Sitemap**
- Exists and accessible
- Submitted to Search Console
- Contains only canonical, indexable URLs
- Updated regularly
- Proper formatting

**Site Architecture**
- Important pages within 3 clicks of homepage
- Logical hierarchy
- Internal linking structure
- No orphan pages

**Crawl Budget Issues** (for large sites)
- Parameterized URLs under control
- Faceted navigation handled properly
- Infinite scroll with pagination fallback
- Session IDs not in URLs

**AI Crawler Management**

Managing AI crawlers via robots.txt is critical as AI companies actively crawl the web for training and AI search:

| Crawler | Company | Token | Purpose |
|---------|---------|-------|---------|
| GPTBot | OpenAI | `GPTBot` | Model training |
| ChatGPT-User | OpenAI | `ChatGPT-User` | Real-time ChatGPT browsing |
| ClaudeBot | Anthropic | `ClaudeBot` | Model training |
| PerplexityBot | Perplexity | `PerplexityBot` | Search + training |
| Google-Extended | Google | `Google-Extended` | Gemini training (NOT search) |
| CCBot | Common Crawl | `CCBot` | Open dataset |
| Bytespider | ByteDance | `Bytespider` | Model training |
| Applebot-Extended | Apple | `Applebot-Extended` | Apple Intelligence training |

**Key distinctions:**
- Blocking `Google-Extended` prevents Gemini training but does NOT affect Google Search indexing or AI Overviews (those use `Googlebot`)
- Blocking `GPTBot` prevents OpenAI training but does NOT prevent ChatGPT from citing content via browsing (`ChatGPT-User`)
- Blocking `CCBot` is low-risk for search visibility (not used by major search engines)

**Recommendation:** Consider AI visibility strategy before blocking. Being cited by AI systems drives brand awareness and referral traffic. Middle ground: block training-only crawlers while allowing search/citation bots.

### Indexation

**Index Status**
- site:domain.com check
- Search Console coverage report
- Compare indexed vs. expected

**Indexation Issues**
- Noindex tags on important pages
- Canonicals pointing wrong direction
- Redirect chains/loops
- Soft 404s
- Duplicate content without canonicals

**Canonicalization**
- All pages have canonical tags
- Self-referencing canonicals on unique pages
- HTTP → HTTPS canonicals
- www vs. non-www consistency
- Trailing slash consistency

### JavaScript Rendering Analysis

**Why it matters:** Google renders JavaScript pages but it costs crawl budget and can delay indexing. Sites using CSR (client-side rendering) frameworks need extra scrutiny.

**Check for:**
- Content visible in initial HTML vs requires JS execution to render
- Identify framework (React, Vue, Angular, SPA) and rendering strategy
- Critical SEO elements (canonical, meta robots, title, meta description) served in initial HTML — not JS-injected
- Structured data in initial HTML vs JS-injected (Google may delay processing JS-injected schema)

**JavaScript SEO guidance (Google, December 2025 update):**
- If canonical tag in raw HTML differs from JS-injected one, Google may use EITHER — ensure they match
- If raw HTML has `<meta name="robots" content="noindex">` but JS removes it, Google MAY still honor the noindex from raw HTML
- Google does NOT render JavaScript on pages returning non-200 HTTP status codes
- For time-sensitive structured data (especially Product markup), include it in initial server-rendered HTML

**Common issues:**
- SPA with no SSR/SSG — content invisible to Googlebot
- Canonical mismatch between HTML and JS
- noindex only in JS (rendered too late)
- Structured data disappears after JS execution
- Soft 404s rendered as 200 with JS error content

### IndexNow Protocol

**What it is:** Protocol for notifying search engines (Bing, Yandex, Naver, Seznam — NOT Google) about URL changes. Supported search engines other than Google.

**Check:**
- Is IndexNow implemented? (check for `/indexnow` endpoint or API key in source)
- For sites that update content frequently, IndexNow provides faster indexing on Bing and other engines

### Site Speed & Core Web Vitals

**Core Web Vitals**
- LCP (Largest Contentful Paint): < 2.5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0.1

**Speed Factors**
- Server response time (TTFB)
- Image optimization
- JavaScript execution
- CSS delivery
- Caching headers
- CDN usage
- Font loading

**Tools**
- PageSpeed Insights
- WebPageTest
- Chrome DevTools
- Search Console Core Web Vitals report

### Mobile-Friendliness

- Responsive design (not separate m. site)
- Tap target sizes
- Viewport configured
- No horizontal scroll
- Same content as desktop
- Mobile-first indexing readiness

### Security & HTTPS

- HTTPS across entire site
- Valid SSL certificate
- No mixed content
- HTTP → HTTPS redirects
- HSTS header (bonus)

### URL Structure

- Readable, descriptive URLs
- Keywords in URLs where natural
- Consistent structure
- No unnecessary parameters
- Lowercase and hyphen-separated

### Agent-Friendly Pages (Forward-Looking)

AI agents (not just AI summarizers) increasingly read sites through vision models, raw HTML/DOM, and accessibility trees. Key audit areas:

- Semantic HTML — real `<nav>`, `<main>`, `<article>`, `<button>` tags (not `<div>`-spam)
- All interactive elements labelled (proper `<label>`, ARIA, or visible text)
- Stable selectors / predictable layouts (sites that re-render on every interaction break agents)
- Visible pricing, specs, contact info on public, indexable pages
- `cursor: pointer` on clickable elements
- No login/gating on content agents need to evaluate

Surface findings as **opportunities**, not failures. This is an emerging area.

---

## International SEO & Localization

Check when the site serves multiple languages or regions. Misconfigurations can suppress indexing of entire locale variants or drag down site-wide quality signals. See [International SEO reference](references/international-seo.md) for evidence and source URLs.

### Hreflang

Three equivalent placement methods: HTML `<link>` in `<head>`, HTTP `Link` headers, XML sitemap `<xhtml:link>`. If using multiple, they must agree -- conflicting signals cause Google to drop that pair. For 10+ locales, prefer sitemap-based (no page weight, no per-request cost).

**Check for:**
- Self-referencing entry on every page (page must include itself in the hreflang set)
- Reciprocal links (if A points to B, B must point back to A -- or both are ignored)
- Valid codes: ISO 639-1 language + optional ISO 3166-1 Alpha 2 region (e.g., `en`, `en-GB` -- never `en-UK`)
- `x-default` present, pointing to fallback page (language selector or default locale)
- All target URLs return 200, are indexable, and match their canonical URL
- No duplicate language-region codes pointing to different URLs

**Common errors:** Missing self-referencing entry (all hreflang ignored). No return tag / one-directional (pair dropped). Invalid codes like `en-UK` (use `en-GB`). Hreflang target is non-canonical, 404, or blocked (cluster discarded). HTML and sitemap annotations disagree (conflicting pair dropped).

**At scale:** `<xhtml:link>` children don't count toward 50K URL sitemap limit, but the 50MB file size limit becomes the bottleneck (plan 2K-5K URLs per file with full hreflang). Focus hreflang on pages receiving wrong-language traffic -- not required on every page. For Bing: supplement with `<html lang>` and `<meta http-equiv="content-language">` (Bing treats hreflang as a weak signal).

### Canonicalization for Multilingual Sites

- Each locale page must self-canonical (e.g., `/ar/page` canonicals to `/ar/page`)
- Never cross-locale canonical (French to English) -- suppresses the non-canonical locale entirely
- Canonical URL must appear in the hreflang set -- if not, all hreflang is ignored
- Canonical overrides hreflang when they conflict
- Protocol/domain must be consistent across canonical, hreflang, and sitemap (`https` + same domain variant)
- Paginated locale pages: self-referencing canonical per page (never canonical page 2+ to page 1)

**Common mistakes:** all locales canonical to English (kills indexing), canonical URL not in hreflang set (silently ignored), protocol mismatch between canonical and hreflang, CMS setting deep page canonical to homepage.

### International Sitemaps

**Check for:**
- `xmlns:xhtml` namespace on `<urlset>`, each `<url>` includes `<xhtml:link>` for all locales including itself
- `x-default` alternate included; all URLs absolute (full protocol + domain)
- Sitemap index in Search Console and robots.txt; split by content type, not by locale

**Next.js caveat:** `alternates.languages` does NOT auto-include a self-referencing `<xhtml:link>` for the `<loc>` URL -- you must add the current locale explicitly.

### Locale URL Structure

**Recommended:** Subdirectories (`/en/`, `/ar/`). **Acceptable:** Subdomains or ccTLDs. **Not recommended:** URL parameters (`?lang=en`).

**Check for:**
- Consistent locale prefix strategy; all locales prefixed (hiding locale from URLs prevents Google from distinguishing versions)
- Root URL handled as `x-default` with redirect, or serves default locale content
- No IP/Accept-Language content negotiation (Googlebot: US IPs, no Accept-Language header)
- Trailing slash + case consistency across locale paths, canonicals, hreflang, and sitemaps
- 301 redirects from non-canonical format to canonical

**Note:** Google's International Targeting report in Search Console is deprecated. Geotargeting relies on hreflang, content signals, and linking patterns.

### Content Quality Across Locales

**Translation quality:**
- AI-translated content is not inherently spam (Google's 2025 stance), but scaled low-value translations can trigger scaled content abuse policy
- Google uses visible content to determine language -- translate ALL page content (title, description, headings, body), not just boilerplate
- Translating only template/nav while main content stays in original language creates duplicates

**Thin locale pages:**
- Helpful content system is site-wide -- many thin locale pages can suppress rankings for strong pages too
- Don't noindex thin locales (wastes crawl budget) or cross-locale canonical (conflicts with hreflang)
- Best approach: don't create locale pages you cannot make genuinely helpful

**Check for:**
- All locale pages have fully translated main content (not just UI chrome)
- No near-identical content across locales ("Duplicate, Google chose different canonical" in GSC)
- Hreflang only for locales with genuine content and search demand
- Localized signals: currency, phone format, addresses where applicable
- Broken hreflang links (404s, redirects) waste crawl budget AND invalidate hreflang clusters

---

## On-Page SEO Audit

### Title Tags

**Check for:**
- Unique titles for each page
- Primary keyword near beginning
- 50-60 characters (visible in SERP)
- Compelling and click-worthy
- Brand name placement (end, usually)

**Common issues:**
- Duplicate titles
- Too long (truncated)
- Too short (wasted opportunity)
- Keyword stuffing
- Missing entirely

### Meta Descriptions

**Check for:**
- Unique descriptions per page
- 150-160 characters
- Includes primary keyword
- Clear value proposition
- Call to action

**Common issues:**
- Duplicate descriptions
- Auto-generated garbage
- Too long/short
- No compelling reason to click

### Heading Structure

**Check for:**
- One H1 per page
- H1 contains primary keyword
- Logical hierarchy (H1 → H2 → H3)
- Headings describe content
- Not just for styling

**Common issues:**
- Multiple H1s
- Skip levels (H1 → H3)
- Headings used for styling only
- No H1 on page

### Content Optimization

**Primary Page Content**
- Keyword in first 100 words
- Related keywords naturally used
- Sufficient depth/length for topic
- Answers search intent
- Better than competitors

**Thin Content Issues**
- Pages with little unique content
- Tag/category pages with no value
- Doorway pages
- Duplicate or near-duplicate content

### Image Optimization

**Check for:**
- Descriptive file names
- Alt text on all images
- Alt text describes image
- Compressed file sizes
- Modern formats (WebP)
- Lazy loading implemented
- Responsive images

### Internal Linking

**Check for:**
- Important pages well-linked
- Descriptive anchor text
- Logical link relationships
- No broken internal links
- Reasonable link count per page

**Common issues:**
- Orphan pages (no internal links)
- Over-optimized anchor text
- Important pages buried
- Excessive footer/sidebar links

### Keyword Targeting

**Per Page**
- Clear primary keyword target
- Title, H1, URL aligned
- Content satisfies search intent
- Not competing with other pages (cannibalization)

**Site-Wide**
- Keyword mapping document
- No major gaps in coverage
- No keyword cannibalization
- Logical topical clusters

---

## Content Quality Assessment

### E-E-A-T Signals

**Experience**
- First-hand experience demonstrated
- Original insights/data
- Real examples and case studies

**Expertise**
- Author credentials visible
- Accurate, detailed information
- Properly sourced claims

**Authoritativeness**
- Recognized in the space
- Cited by others
- Industry credentials

**Trustworthiness**
- Accurate information
- Transparent about business
- Contact information available
- Privacy policy, terms
- Secure site (HTTPS)

### Content Depth

- Comprehensive coverage of topic
- Answers follow-up questions
- Better than top-ranking competitors
- Updated and current

### User Engagement Signals

- Time on page
- Bounce rate in context
- Pages per session
- Return visits

---

## Common Issues by Site Type

### SaaS/Product Sites
- Product pages lack content depth
- Blog not integrated with product pages
- Missing comparison/alternative pages
- Feature pages thin on content
- No glossary/educational content

### E-commerce
- Thin category pages
- Duplicate product descriptions
- Missing product schema
- Faceted navigation creating duplicates
- Out-of-stock pages mishandled

### Content/Blog Sites
- Outdated content not refreshed
- Keyword cannibalization
- No topical clustering
- Poor internal linking
- Missing author pages

### Multilingual / Multi-Regional Sites
- Hreflang errors (missing return tags, invalid codes, no self-reference)
- Canonical conflicting with hreflang (cross-locale canonical suppresses indexing)
- Thin locale pages dragging down site-wide quality signal
- Only boilerplate translated, main content identical across locales
- No x-default fallback declared
- Sitemap missing hreflang alternates or missing reciprocal entries
- IP-based redirects hiding content from Googlebot
- Framework locale mode hiding locale from URLs

### Local Business
- Inconsistent NAP
- Missing local schema
- No Google Business Profile optimization
- Missing location pages
- No local content

---

## Content Brief Generation

When creating new content that needs to rank, produce a structured content brief:

### Brief Format

**Target Keyword:** [primary keyword]
**Search Intent:** [informational/commercial/transactional/navigational]
**Target Audience:** [who is this for]
**Target URL slug:** [suggested URL]

### SERP Analysis
- Top-ranking pages: [list 3-5]
- Content gaps vs competitors: [what they miss]
- Featured snippet opportunities: [yes/no/type]
- AI Overview presence: [does an AI overview appear for this query?]

### Content Requirements
- **Minimum word count:** [based on top 10 average]
- **Key subtopics to cover:** [H2 headings needed]
- **Internal links to:** [which existing pages to link from]
- **External links to:** [authority sources to reference]
- **Schema types needed:** [Article, FAQ, HowTo, etc.]

### Answer Blocks (for AI extractability)
- **Definition block:** 40-60 word concise answer for "What is X?"
- **Comparison table:** If "[X] vs [Y]" intent
- **Step-by-step:** If "how to" intent
- **FAQ block:** 3-5 natural-language Q&A pairs
- **Stat block:** 2-3 statistics with cited sources

### Differentiation Angle
- What makes this content better than what's ranking?
- Unique data, original research, expert quotes, first-hand experience?

### Distribution
- Related queries the AI will fan out to (list 5-10)
- Internal links from: [which existing pages should link here]

---

## Output Format

### Audit Report Structure

**Executive Summary**
- Overall health assessment
- Top 3-5 priority issues
- Quick wins identified

**Technical SEO Findings**
For each issue:
- **Issue**: What's wrong
- **Impact**: SEO impact (Critical/High/Medium/Low/Info)
- **Evidence**: How you found it
- **Fix**: Specific recommendation
- **Falsifiability check**: How will we know this fix worked or failed? (e.g., "If this is fixed, `site:domain.com` count will increase by X% within 2 weeks")
- **Effort**: Estimated effort (Low/Medium/High)
- **Priority**: Critical (fix immediately), High (within 1 week), Medium (within 1 month), Low (backlog)

**On-Page SEO Findings**
Same format as above

**Content Findings**
Same format as above

**Prioritized Action Plan**
1. **Phase 1: Critical Fixes** (blocking indexation/ranking) — Week 1
2. **Phase 2: High-Impact Improvements** — Weeks 2-3
3. **Phase 3: Content & Authority** — Month 2
4. **Phase 4: Monitoring & Iteration** — Ongoing

Each recommendation should carry:
- The first-principle observation it rests on
- Dependencies (what must be fixed first)
- An explicit "how would we know this failed?" check
- A leading indicator the user can monitor without re-running the full audit

---

## References

- [AI Writing Detection](references/ai-writing-detection.md): Common AI writing patterns to avoid (em dashes, overused phrases, filler words)
- [International SEO](references/international-seo.md): Evidence and sources for hreflang, canonical + i18n, sitemaps, URL structure, and content quality across locales
- For AI search optimization (AEO, GEO, LLMO, AI Overviews), see the **ai-seo** skill

---

## Tools Referenced

**Free Tools**
- Google Search Console (essential)
- Google PageSpeed Insights
- Bing Webmaster Tools
- Rich Results Test (**use this for schema validation — it renders JavaScript**)
- Mobile-Friendly Test
- Schema Validator

> **Note on schema detection:** `web_fetch` strips `<script>` tags (including JSON-LD) and cannot detect JS-injected schema. Use the browser tool, Rich Results Test, or Screaming Frog instead — they render JavaScript and capture dynamically-injected markup. See the Schema Markup Detection Limitation section above.

**Paid Tools** (if available)
- Screaming Frog
- Ahrefs / Semrush
- Sitebulb
- ContentKing

---

## Task-Specific Questions

1. What pages/keywords matter most?
2. Do you have Search Console access?
3. Any recent changes or migrations?
4. Who are your top organic competitors?
5. What's your current organic traffic baseline?

---

## Related Skills

- **ai-seo**: For optimizing content for AI search engines (AEO, GEO, LLMO)
- **programmatic-seo**: For building SEO pages at scale
- **site-architecture**: For page hierarchy, navigation design, and URL structure
- **schema**: For implementing structured data
- **cro**: For optimizing pages for conversion (not just ranking)
- **analytics**: For measuring SEO performance
