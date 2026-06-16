# Session Summary — Coach System Expansion

## Goal
Expand the coach's capabilities: SEO audit tool with multi-page crawl + backlinks + page speed, task manager, site survey tracker, and MCP server integration.

## Progress
### Done
- **Created `seo_audit.py` v1**: single-page audit for meta, headings, schema, social, robots, sitemap, AI crawlers, SSL.
- **Added MCP tool**: `seo_audit(url)` tool in `mcp_server.py` for both stdio MCP and interactive modes.
- **Updated skills**: seo-audit SKILL.md -> v3.0 (scoring, AI crawler table, falsifiability), ai-seo -> v2.1, schema -> v2.1 (FAQ/HowTo deprecation May 7 2026).
- **Expanded `seo_audit.py` to v2** with all new flags:
  - `--crawl`: samples N sitemap pages (category/tag/product/blog/page), checks content depth, images/alt text, internal links, thin page detection, quality signals.
  - `--backlinks`: checks backlinks via Common Crawl CDX API (free, no API key).
  - `--speed`: checks page speed via Google PageSpeed Insights API with fallback to basic load time timing.
  - `--max-pages N`: control crawl sample size (default 5).
  - Fixed arg parsing for both `--max-pages=N` and `--max-pages N` forms.
- **Tested all modes on aslielectronics.com**:
  - Basic: 5 issues (3M, 1L, 1I) -- title 61 chars, desc 91 chars, 1 image no src, 381w content, 6 AI crawlers blocked.
  - Crawl: +2 medium (categories 57w thin, tags/4g-camera/ 90w thin).
  - Backlinks: 0 backlinks (expected for 3-week-old site).
  - Speed: 0.41s load time fallback (Google API rate-limited).
- **Created `task_manager.py`**: add/list/done/delete tasks with priority, stored in `coach/memory/tasks.md`. MCP tool registered.
- **Created `site_survey.py`**: add/list/view/close MOI site survey visits with client, location, contact, notes. MCP tool registered.
- **Updated AGENTS.md**: added all new tool commands and flags.
- **Updated MCP server**: added `task_manager`, `site_survey` tools; updated `seo_audit` tool signature with crawl/backlinks/speed params.

## Key Decisions
- All new tools follow existing pattern: single Python file in `coach/tools/`, YAML-like list in `coach/memory/`.
- Common Crawl CDX for free backlinks (no API key); fast mode uses only latest index.
- Page speed fallback: if Google API rate-limited, measure basic load time via requests.
- Task manager stores in `tasks.md`, site surveys in `site_surveys.md`.

## Relevant Files
- `coach/tools/seo_audit.py` -- Expanded to v2 with --crawl, --backlinks, --speed
- `coach/tools/task_manager.py` -- New task management tool
- `coach/tools/site_survey.py` -- New MOI site survey tool
- `coach/tools/mcp_server.py` -- All 3 tools registered as MCP tools
- `AGENTS.md` -- Updated with all new tool commands
- `.opencode/skills/seo-audit/SKILL.md` -- Updated to v3.0
- `.opencode/skills/ai-seo/SKILL.md` -- Updated to v2.1
- `.opencode/skills/schema/SKILL.md` -- Updated to v2.1
