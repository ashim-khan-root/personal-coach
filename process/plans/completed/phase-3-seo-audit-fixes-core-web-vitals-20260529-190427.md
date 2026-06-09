---
title: "Phase 3 - SEO Audit Fixes & Core Web Vitals"
created: "2026-05-29T19:04:27.172120+00:00"
status: active
phase: plan
---

## Objective

Fix all Critical and High priority issues from the AsliElectronics SEO audit to improve rankings, CTR, and Core Web Vitals.

## Approach

Work through issues in priority order — Critical → High → Medium (quick wins first). Each change pushed to GitHub, verified on live site after deploy.

## Deliverables

1. [Critical] Catchy title tag: `AsliElectronics | Premium Security & Smart Solutions in Qatar`
2. [High] 150-160 char meta description on every page
3. [High] `loading="lazy"` on all product/category images
4. [High] Explicit `width`/`height` attributes on all `<img>` tags (fix CLS)
5. [Medium] Self-host Google Fonts or add `&display=swap`
6. [Medium] BreadcrumbList schema structured data
7. [Medium] Product schema on product pages
8. [Medium] hreflang tags for en + ar
9. [Low] Fix newsletter form action
10. [Low] Consolidate inline SVGs into sprite

## Success Criteria

- Lighthouse score ≥ 90 on mobile + desktop
- CLS < 0.1 (Core Web Vitals pass)
- Meta description and title visible in view-source on all pages
- Breadcrumb + Product schema validatable via Schema.org tester
- All pushed to GitHub and live on Cloudflare

## Resources

- SEO audit: `coach/work/research/aslielectronics-seo-audit-2026-05-29.md`

## Notes

Start with Hugo layout files: layouts/index.html, layouts/_default/baseof.html, layouts/partials/head.html
