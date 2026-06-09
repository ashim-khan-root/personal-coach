# Google Shopping + Merchant Center — Setup Guide for secuview.com

**Goal:** Show Secuview products with prices in Google Search results (free traffic, no ad spend required)

**Time needed:** 1 hour initial setup + 3-7 days for Google review

**Access needed:** WordPress admin access (no FTP/SSH required)

---

## Step 1: Install the Plugin

1. Log in to WordPress admin (`secuview.com/wp-admin`)
2. Go to **Plugins > Add New**
3. Search: **"Google Listings & Ads"** by WooCommerce
4. Click **Install Now** → **Activate**

## Step 2: Connect to Google

1. After activation, a setup wizard will appear
2. Click **"Set up guided setup"**
3. Sign in with the **same Google account** used for the Business Profile
4. Grant permissions (the plugin needs access to Google Merchant Center)
5. A Merchant Center account will be created automatically

## Step 3: Set Up the Product Feed

1. Select which products to include:
   - Smart Home (Smart Locks, Doorbells, Smart Switches, IR Controller)
   - Network & Communications (Routers, PoE Switches, Access Points, Racks)
   - Audio Products (PA Systems, Speakers)
   - Cable (Network Cable, Coaxial Cable)
   - ✅ Include all categories except CCTV (that's the other team's section)
2. Set **Target Country** → **Qatar**
3. Set **Target Language** → **English**
4. Set **Currency** → **QAR (Qatari Riyal)**

## Step 4: Configure Shipping & Taxes

In the plugin settings:

1. **Shipping rates:**
   - Option A: Flat rate 30 QAR
   - Option B: Free shipping over 500 QAR (encourages larger orders)
   - Choose whichever works for your current shipping setup
2. **Tax settings:** Set to 0% (no sales tax on electronics in Qatar)

## Step 5: Verify Your Website

Google needs to confirm you own secuview.com:

1. During setup, the plugin offers **automatic verification** — select this
2. If automatic fails, use **HTML meta tag** method:
   - Copy the meta tag provided by Google
   - In WP admin, go to **Tools > File Manager**
   - Navigate to `wp-content/themes/` and find your active theme
   - Alternatively, use a plugin like **Insert Headers and Footers** to paste the meta tag
3. Click **Verify** in the Google Merchant Center dashboard

## Step 6: Submit for Review

1. In the plugin dashboard, click **"Submit for Review"**
2. The feed will be reviewed by Google (takes 3-7 days)
3. Check back in Merchant Center for any "disapproved products"
4. Common disapproval reasons and fixes:
   - **Missing GTIN** → Use the product SKU in the GTIN field
   - **Price mismatch** → Ensure WooCommerce prices match the feed
   - **Image issues** → Ensure product images are clear, on white background if possible
   - **Description too short** → Expand product descriptions to 50+ words

## Step 7: Enable Free Listings

Once approved:

1. Go to **Google Merchant Center** → **Growth** → **Manage Programs**
2. Click **Get Started** on **Free Listings**
3. Your products will now appear in Google Shopping tab for free

## Step 8 (Optional) — Paid Shopping Ads

If budget allows later:

1. Link Merchant Center to **Google Ads** account
2. Create a **Smart Shopping Campaign**
3. Suggested starting budget: **50-100 QAR/day**
4. Target keywords: "buy smart lock qatar", "4g router doha", "poe switch qatar"

---

## Expected Results

| Metric | Estimate |
|--------|----------|
| Setup time | 1 hour |
| Free listings review | 3-7 days |
| Monthly impressions (est.) | 500-2,000 from Shopping tab |
| Cost | Free (unless running paid ads) |

---

## Troubleshooting

**"Products not showing in Shopping tab"**
- Check Merchant Center > Diagnostics for feed errors
- Ensure product prices are in QAR
- Ensure product images are at least 100x100px

**"Website verification failed"**
- Try the HTML meta tag method via Insert Headers and Footers plugin
- Make sure the meta tag is in the `<head>` section of every page

**"Disapproved due to missing GTIN"**
- In WooCommerce, edit the product and enter the SKU in the "GTIN" field
- You can bulk-edit via **Products > All Products > Bulk Edit**

---

## Full Order of Operations

```
Day 1: Install plugin → Connect Google → Configure feed → Submit review
Day 3-7: Google reviews the feed
Day 7: Approve free listings → Products appear in Google Shopping
```
