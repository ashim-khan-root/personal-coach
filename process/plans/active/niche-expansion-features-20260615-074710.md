---
title: "Niche Expansion & Features"
created: "2026-06-15T07:47:10"
status: active
phase: plan
---

## Objective

Scale the site from 15 general tools into 5+ niche categories, each capable of ranking independently and cross-linking for compound SEO growth. All on ONE domain with subdirectories (not subdomains).

## Site Architecture

```
example.com/
├── /                          ← Homepage (hub, links to all categories)
├── /tools/                    ← General utilities (existing 15 tools)
├── /calculators/              ← Health, finance, everyday calculators
├── /construction/             ← Construction calculators (concrete, steel, etc.)
├── /devtools/                 ← Developer utilities (formatting, checking)
├── /seo-tools/                ← SEO/webmaster utilities
├── /blog/                     ← Content that drives tool discovery
└── /text-tools/               ← Writing utilities
```

## Niche Categories

### 1. Construction Calculators ← suggested by you earlier
| Tool | Est. searches/mo | Build time |
|------|:-:|:-:|
| Concrete Calculator | 200K | 20 min |
| Rebar Calculator | 50K | 15 min |
| Roofing Calculator | 80K | 25 min |
| Paint Calculator | 60K | 15 min |
| Flooring Calculator | 40K | 15 min |
| Brick/Block Calculator | 30K | 15 min |
| Stair Calculator | 20K | 20 min |
| **Total** | **~480K** | **~2 hr** |

**Why:** High intent, construction pros search these daily, easy to rank.

### 2. SEO / Webmaster Tools
| Tool | Searches |
|------|:-:|
| Meta Tag Checker | 30K |
| SSL Checker | 40K |
| HTTP Header Checker | 15K |
| Sitemap Generator | 25K |
| Robots.txt Tester | 10K |
| Page Speed Test | 60K+ |

**Why:** Audience overlaps with tools site, developers/seo pros are high-value ad traffic.

### 3. Developer Tools
| Tool | Searches |
|------|:-:|
| HTML Minifier | 20K |
| CSS Minifier | 20K |
| JS Minifier | 30K |
| YAML to JSON | 15K |
| Diff Tool (already exists) | — |
| SQL Formatter | 15K |

**Why:** Already have dev-adjacent tools (JSON formatter, Base64), easy expansion.

### 4. Health & Fitness Calculators
| Tool | Searches |
|------|:-:|
| BMI Calculator | 200K+ |
| BMR Calculator | 80K |
| Body Fat Calculator | 50K |
| Calorie Calculator | 60K |
| Pregnancy Due Date | 100K+ |
| Water Intake Calculator | 40K |

**Why:** Massive search volume, evergreen content.

## Feature Additions

### 1. Blog Section
- Posts like "How Much Concrete Do I Need?" → links to concrete calculator
- "What is a Good BMI?" → links to BMI calculator
- 1 blog post per major tool = perpetual SEO growth
- Hugo blog section is trivial to add

### 2. Category Landing Pages
- `/construction/` page with all construction calculators + description
- Internal link hub: category page → tool pages → blog → category page
- Creates topical authority clusters

### 3. Tool Search / Filter
- Once we hit 25+ tools, add a search bar to `/tools/` page
- Filter by category tabs (All / Text / Image / Dev / Calculators)

### 4. Widget Embed
- Let users embed the tool on their own site via `<iframe>` or `<script>`
- Free backlinks from every embed

### 5. Print-Friendly Results
- "Print" or "PDF" button on calculators (construction, health)
- High utility for construction pros on site

## Phasing

| Phase | What | Tools count |
|-------|------|:-:|
| **1** | Construction calculators (batch of 7) | 15 → 22 |
| **2** | Health calculators (batch of 6) | 22 → 28 |
| **3** | Dev/SEO tools (batch of 7) | 28 → 35 |
| **4** | Blog section + 1 post per category | 35 + blog |
| **5** | Category pages + search + embed | — |

## Success Criteria

- [ ] 35+ tools live across 5 niches
- [ ] Blog section running with 3+ posts
- [ ] Category landing pages for each niche
- [ ] Search/filter on /tools/
- [ ] All tools cross-linked within their category

## Resources

- Skills: web-development, hugo, seo-audit
- All tools follow existing pattern: `content/<category>/<tool>/index.md` + `static/js/<tool>.js`
