# Hugo Site Audit: safehome (ashim-khan-root.github.io/safehome)
**Date:** 2026-05-21
**Framework:** Hugo + Tailwind CSS
**Status:** GitHub Pages (pre-production)

---

## ✅ What's Working Well

| Feature | Status |
|---------|--------|
| Clean Hugo + Tailwind setup | ✅ |
| Full product catalog (178+ products) | ✅ |
| Category navigation (6 main categories) | ✅ |
| Blog section (3 posts) | ✅ |
| About page with company story | ✅ |
| Contact page | ✅ |
| Prices in QAR (local currency) | ✅ |
| Cart functionality | ✅ |
| Mobile-responsive design | ✅ |
| Free shipping banner | ✅ |
| Deal of the day timer | ✅ |
| Newsletter signup | ✅ |
| Fast load times (Hugo static site) | ✅ |

---

## 🚨 Issues to Fix Before Production

### 1. Price Display Bug (HIGH)
Some products show `QAR %!f(int=00)` — this is a Hugo template formatting issue where the price value isn't being parsed correctly.

**Products affected:**
- Secuview 4G LTE Wi-Fi Router with SIM
- Secuview 200W 16-Port Gigabit PoE Switch
- Secuview Outdoor Wireless 4G Router
- Secuview 16-Port Gigabit PoE Switch | 300W

**Fix:** Check the Hugo template that renders `{{ .Params.price }}` — ensure it's a float, not an integer. Use `printf "%.2f"` or convert the frontmatter to float.

### 2. Custom Domain (HIGH)
Currently on `ashim-khan-root.github.io/safehome` — cannot rank on Google properly.

**Recommended domains:**
- `safehome.qa` (best — local Qatar TLD)
- `secuview.shop` (alternative)
- `safehomeqatar.com` (generic)

**Setup:** Use Cloudflare for DNS + free SSL + CDN.

### 3. SEO Meta Tags (HIGH)
**Missing across all pages:**
- Meta descriptions
- Open Graph tags (Facebook, LinkedIn)
- Twitter Card tags
- Canonical URLs
- Hreflang tags (if bilingual)

**Fix:** Add Hugo partial `layouts/partials/head.html` with dynamic meta tags pulled from frontmatter.

### 4. No Sitemap or robots.txt (HIGH)
**Missing:**
- `sitemap.xml` — essential for Google indexing
- `robots.txt` — control crawler access

**Fix:** Hugo has built-in sitemap support — enable in `config.toml`:
```toml
[params]
  enableRobotsTXT = true
[mediaTypes]
  [mediaTypes."text/sitemap"]
    suffixes = ["xml"]
```

### 5. No Structured Data (HIGH)
**Missing schemas:**
- Product schema (for rich snippets in search results)
- Organization schema
- BreadcrumbList schema
- FAQ schema (for blog posts)

**Fix:** Add JSON-LD partial and include on product pages.

### 6. Product Image Alt Text (MEDIUM)
Some alt text is keyword-stuffed and unnatural:
- `"Trusted Tangle-Free Doha | Secuview"`
- `"Certified Heat-Free Doha | Secuview"`

**Fix:** Write natural, descriptive alt text like `"Secuview 1U rack shelf with ventilated steel design"`

### 7. Blog Content Misalignment (MEDIUM)
Current blog posts:
- "Getting Started with Hugo and Tailwind CSS"
- "5 Hugo Tips for Faster Development"
- "Mastering Tailwind CSS: A Complete Guide"

These are **developer tutorials**, not e-commerce content. They won't attract customers looking for security products.

**Fix:** Replace with product buying guides and SEO-optimized content (like the Home WiFi Starter Kit blog we wrote).

### 8. No Analytics (MEDIUM)
No Google Analytics, Meta Pixel, or any tracking. You can't measure traffic or conversions.

**Fix:** Add Google Analytics 4 + Google Search Console before launch.

### 9. Contact Form Not Functional (MEDIUM)
Static site has no backend. Form submissions will 404 or do nothing.

**Fix options:**
- Netlify Forms (if deploying on Netlify)
- Formspree (free tier)
- Cloudflare Workers (advanced)

### 10. Category URL Structure (LOW)
Double-dash in URLs: `/categories/network--communications/`

This works but looks messy. Consider slug aliases in Hugo frontmatter.

### 11. No Product Search (LOW)
No search bar for users to find products.

**Fix:** Add Lunr.js (client-side search, works with Hugo).

---

## 📋 Production-Ready Checklist

### Week 1: Critical Fixes
- [ ] Fix price `%!f(int=00)` display bug in Hugo template
- [ ] Register custom domain (recommend `safehome.qa`)
- [ ] Set up Cloudflare DNS + SSL
- [ ] Add proper `<head>` meta partial (description, OG, Twitter)
- [ ] Enable Hugo sitemap + create robots.txt

### Week 2: Content + Structure
- [ ] Add Product schema JSON-LD to all product pages
- [ ] Add Organization schema to homepage
- [ ] Fix product image alt texts (natural, not keyword-stuffed)
- [ ] Replace developer blog posts with e-commerce buying guides
- [ ] Add the Home WiFi Starter Kit blog post we wrote

### Week 3: Launch Prep
- [ ] Set up Google Analytics 4 + Search Console
- [ ] Implement functional contact form (Formspree)
- [ ] Add breadcrumb navigation
- [ ] Optimize images (compress + WebP)
- [ ] Test on mobile + desktop + all browsers
- [ ] Set up 404 page

### Week 4: Launch + Promote
- [ ] Point custom domain to Cloudflare
- [ ] Submit sitemap to Google Search Console
- [ ] Set up social media profiles (if not already)
- [ ] Create Google Business Profile for SafeHOME
- [ ] Start link building (directory listings, local Qatar directories)

---

## 💰 Cost Estimate for Production

| Item | Cost |
|------|------|
| Domain (safehome.qa) | ~80-120 QAR/year |
| Cloudflare (free tier) | Free |
| Hosting (GitHub Pages) | Free |
| Formspree (free tier) | Free |
| Google Analytics | Free |
| Search Console | Free |
| **Total** | **~100 QAR/year** |

---

## 🔄 Deployment Options

### Option A: Keep GitHub Pages + Custom Domain (Recommended)
- Free hosting
- Cloudflare for DNS + SSL
- Hugo builds on push via GitHub Actions

### Option B: Move to Netlify
- Better form handling (Netlify Forms built-in)
- Automatic deploy from GitHub
- Free tier generous
- Split testing built-in

### Option C: VPS (DigitalOcean / Linode)
- Full control
- ~$6/month
- Overkill for Hugo static site

**Recommendation:** Option A (GitHub Pages + Cloudflare) for now. Move to Netlify later if you need forms.

---

## 📊 SEO Baseline (Current State)

| Metric | Status |
|--------|--------|
| Pages indexed in Google | 0 (not on custom domain) |
| Page speed | Fast (static Hugo) |
| Mobile-friendly | ✅ |
| SSL | ✅ (GitHub Pages) |
| Structured data | ❌ |
| Meta tags | ❌ |
| Sitemap | ❌ |
| Analytics | ❌ |
| Blog content aligned | ❌ (tutorials, not products) |

---

*Generated by Personal Growth Coach — AI-powered site audit*
