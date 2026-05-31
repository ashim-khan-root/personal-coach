# Secuview — Facebook/Instagram Shop Setup Guide

## Prerequisites

- [ ] Personal Facebook account
- [ ] Secuview business email
- [ ] Secuview Facebook Page created
- [ ] Instagram handle for Secuview (Business or Creator account)
- [ ] Product images (600x600px min, 1+ per item)
- [ ] Product info: name, price, description, SKU, website link

---

## Step 1: Create Facebook Business Manager

1. Go to `business.facebook.com/overview`
2. Click **Create Account**
3. Enter:
   - Business name: `Secuview`
   - Your name
   - Business email
4. Verify email
5. Inside Business Manager → **Business Assets > Pages**
6. Click **Add > Add existing Page** → add Secuview's Facebook Page

---

## Step 2: Set Up Commerce Manager Catalog

1. From Business Manager → **All Tools > Commerce Manager**
2. Click **Create Catalog**
3. Choose **E-commerce** as catalog type
4. Name: `Secuview Products`
5. Select your Business Manager account
6. **Add Products** → choose **Manual** (no Shopify/Magento integration)
7. Upload method:
   - **Add items manually** — add products one by one
   - **CSV upload** — download template, fill, upload (better for 10+ items)

---

## Step 3: Add Products

### Manual method:
1. Click **Add Item** → **Add Item Manually**
2. Fill: name, description, price, link, image, category, brand, GTIN
3. Submit → wait for **Approved** status

### CSV method (preferred — 187 products pre-scraped):
1. Click **Add Item** → **Add Items via Data Feed**
2. A pre-built CSV is ready: `work/content/secuview-facebook-catalog.csv` 
3. It contains all 187 Secuview products with: `id`, `title`, `price`, `link`, `brand`, `availability`, `category`
4. **Missing:** `description` and `image_link` — these can be filled manually in Commerce Manager after upload or added later
5. Upload CSV → map columns → submit
6. Check **Diagnostics** tab for errors

> **CSV regeneration:** run `python3 work/scripts/scrape_secuview.py` from `coach/` to re-scrape when products change.

> **Fields with special characters** (Arabic text, currency symbols) may cause CSV errors. Stick to plain English.

---

## Step 4: Link Instagram Account

1. In Commerce Manager → **Settings > Data Sources > Instagram**
2. Click **Connect Instagram**
3. Log in with Secuview's Instagram credentials

### Prerequisites for Instagram — verify all:

| Check | How |
|-------|-----|
| Instagram is Business/Creator account | App → Settings → Account → Switch to Professional → Business |
| Instagram linked to Facebook Page | App → Settings → Account → Linked Accounts → Facebook → select Secuview page |
| Instagram in a Shopping-supported country | Qatar is supported since 2021 |
| Catalog has at least 1 approved product | Complete Step 3 first |

### Troubleshooting link issues:
- **"Instagram account not eligible"** — re-check account type (must be Business/Creator)
- **"Account already connected to another catalog"** — disconnect from old catalog first
- **"Page not linked"** — verify Facebook Page is linked in Instagram settings before connecting

---

## Step 5: Submit for Instagram Shopping Approval

1. In Commerce Manager → **Settings > Instagram Shopping**
2. Click **Submit for Review**
3. Instagram reviews against [Commerce Eligibility](https://www.facebook.com/business/help/634452705528148)

### Requirements (confirm before submitting):
- [ ] Account follows Community Guidelines
- [ ] Sells **physical goods** (Secuview ✓)
- [ ] Has a website clearly showing products & pricing (`secuview.com`)
- [ ] No prohibited content (weapons, drugs, surveillance laws — security cameras are OK)
- [ ] Facebook Page info matches website (name, address, phone are consistent)

### Timeline:
- **Typical:** 24–72 hours
- **Max:** Up to 2 weeks
- **If rejected:** Check Business Support email for reason → fix → resubmit

---

## Post-Approval Checklist

- [ ] Add product tags in Instagram posts (tag icon in composer)
- [ ] Add product tags in Stories
- [ ] Enable **Shop tab** on Instagram profile
- [ ] Pin a tagged product post to profile
- [ ] Add product links in bio as fallback

---

## Qatar-Specific Notes

- Instagram Shopping is **available in Qatar** (since 2021)
- Security/camera equipment is not on the prohibited list — should pass review
- Your store domain must be a **public `.com` domain** — `secuview.com` works
- If you serve Arabic-speaking customers, consider dual-language product descriptions
- Facebook Pay is not available in Qatar; all purchases redirect to `secuview.com` checkout

---

## Key Links

| Resource | URL |
|----------|-----|
| Facebook Business Manager | `business.facebook.com/overview` |
| Commerce Manager | `business.facebook.com/commerce` |
| Commerce Eligibility Policy | `www.facebook.com/business/help/634452705528148` |
| Instagram Shopping Docs | `www.facebook.com/business/help/1849961763127830` |

---

*Last updated: 2026-05-31*
