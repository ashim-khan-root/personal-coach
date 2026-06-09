# Redesign Starfox Secu Website — Enterprise B2B Brand

## Objective
Redesign starfoxsecu.com as the B2B/enterprise face of Starfox Security System (est. 2005), covering gaps that Secuview (B2C consumer brand) cannot fill.

## Two-Brand Strategy

| Brand | Role | Platform | Focus |
|---|---|---|---|
| **Secuview** | B2C Consumer | WordPress/WooCommerce | E-commerce, smart home, blog content |
| **Starfox Secu** | B2B Enterprise | Hugo (static site) | MOI approval, projects, tenders, services |

Together they cover the full Qatar security market — no competitor has both.

## Current State of starfoxsecu.com

- Static HTML site (index.html, some PHP)
- **0** schema blocks, **0** meta description, **0** H1 tags
- 6 sections: About, Solutions, Partners, Services, Clients, Contact
- No blog, no e-commerce, no Arabic, no MOI badge
- 226 bytes returned without proper headers (server restrictions)
- Single page with anchor navigation
- Empty meta description and keywords

## Target Architecture

### Pages

| Page | Purpose |
|---|---|
| **Home** | Hero, stats (est. 2005, X projects, X clients), CTA, partner logos |
| **About** | Company history, mission, team, ISO certifications |
| **Services** | Service categories (CCTV, Access Control, PA, ELV, Cabling, Maintenance) |
| **Projects** | Portfolio/case studies with client logos and project descriptions |
| **Solutions** | By sector (Education, Healthcare, Government, Commercial, Residential) |
| **Blog** | Industry insights, MOI compliance guides, tech explainers |
| **Contact** | Contact form, map, RFQ form for enterprise inquiries |
| **Careers** | Optional — job openings |

### Key Features Missing That Must Be Added

1. **MOI-Approved Contractor badge** — prominently on homepage and footer
2. **ISO certifications** (9001, 14001, 45001 if applicable)
3. **Schema markup** — LocalBusiness, Organization, Service, Article, BreadcrumbList
4. **Meta descriptions** on every page (150-160 chars)
5. **H1 tags** with primary keywords on every page
6. **Client portfolio** with logos and project descriptions
7. **Partner badges** (Hikvision, Dahua, Bosch, Cisco, etc.)
8. **Arabic language support** (at minimum: homepage + contact)
9. **Request for Quotation / Tender form**
10. **Blog with Article schema**

## Technical Approach

**Hugo Static Site**
- Use your existing Hugo skills (aslielectronics.com experience)
- No CMS, no database — faster hosting, cheaper, more secure
- Manual SEO with Hugo templates (meta tags, schema, OG)
- Blog as Markdown files with Article schema in template
- Deploy to current starfoxsecu.com hosting or GitHub Pages
- Estimated build time: 2-3 days

## Design Direction

- **Professional / Corporate** — not consumer-friendly like Secuview
- **Dark blue + white** color scheme (trust, security, corporate)
- **Hero section**: Large image of a security installation + "Qatar's Trusted Security Partner Since 2005"
- **Trust signals row**: MOI badge, ISO badges, years in business, projects completed
- **Solutions grid**: Icons + service name + short description
- **Project showcase**: Before/after or project cards with client names
- **Partner carousel**: Scrolling logo bar of brand partners

## Content Needed

| Item | Source |
|---|---|
| Company history (2005-present) | You / Rashid |
| List of completed projects | You |
| Client testimonials | Collect from existing clients |
| Partner/vendor list | You (Hikvision, Dahua, etc.) |
| Service descriptions | Adapt from Secuview content |
| Team photos and bios | Optional |

## SEO Strategy

- Primary keywords: "security company Qatar", "MOI approved CCTV Qatar", "security system installer Doha"
- Each service page targets: "[service] Qatar", "[service] Doha"
- Blog: MOI compliance guides, technology comparisons, Qatar security regulations
- Internal linking between starfoxsecu.com and secuview.com (cross-domain)

## Success Criteria

- [ ] starfoxsecu.com has 5+ pages with unique content
- [ ] Schema markup on all pages (LocalBusiness, Organization, Service, Article)
- [ ] MOI approval badge displayed
- [ ] Meta descriptions on all pages
- [ ] Blog with minimum 5 posts
- [ ] Arabic version for homepage + contact
- [ ] Lighthouse score 80+ for performance

## Estimated Timeline

| Phase | Time |
|---|---|
| Hugo project setup + theme | 1 day |
| Page templates + content | 1 day |
| Schema + SEO + Arabic | 1 day |
| **Total** | **~3 days** |
