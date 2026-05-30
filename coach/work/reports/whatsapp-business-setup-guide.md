# WhatsApp Business Catalog — Setup Guide for Secuview

**Goal:** Let customers browse and inquire about products directly via WhatsApp — Qatar's #1 messaging app

**Time needed:** 30 min initial setup + ongoing product uploads

**Cost:** Free

---

## Step 1: Download WhatsApp Business

1. On your phone, go to **Play Store** (Android) or **App Store** (iPhone)
2. Search: **"WhatsApp Business"** (green icon with "Business" badge)
3. Download and install
4. **Do NOT uninstall your personal WhatsApp** — WhatsApp Business runs alongside it

> Note: You need a **second phone number** to register WhatsApp Business. Options:
> - A secondary SIM (if your phone supports dual SIM)
> - A landline number that can receive SMS/call
> - A virtual number (like Skype number)

## Step 2: Set Up Your Business Profile

1. Open WhatsApp Business → Agree to Terms
2. Enter your business phone number (e.g., 40012384 or a dedicated sales line)
3. Verify via SMS or phone call
4. Restore backup (skip if no previous backup exists)
5. Complete your profile:

   | Field | What to enter |
   |-------|---------------|
   | **Business name** | Starfox Security System |
   | **Category** | Electronics / Security |
   | **Description** | Qatar's trusted security & networking partner since 2005. Smart locks, CCTV, routers, and smart home products. Visit our showroom on Salwa Road. |
   | **Address** | 57, Street 406, Al-Maamourah, Salwa Road, Doha |
   | **Hours** | Sat-Thu 7:30-1:00 / 4:00-9:00 |
   | **Website** | https://secuview.com |
   | **Email** | info@starfoxsecu.com |

## Step 3: Create Your Product Catalog

1. In WhatsApp Business, tap the **three dots menu** (⋮) → **Business tools** → **Catalog**
2. Tap **Add item** or the **+** button
3. Add products one by one:

   **Example entries:**

   | Product Name | Price | Description | Link |
   |--------------|-------|-------------|------|
   | Secuview Fingerprint Smart Lock | 600 QAR | Fingerprint + PIN + key. App control. Fits wooden doors. | secuview.com/product/secuview-fingerprint-smart-lock-with-remote-control/ |
   | 4G LTE WiFi Router with SIM | (enter price) | 600Mbps, 4 antennas, battery backup. Works with Ooredoo/Vodafone. | secuview.com/product/secuview-4g-lte-wifi-router-sim-600mbps/ |
   | WiFi Video Doorbell | 388 QAR | 1080p HD, two-way audio, IP65 weatherproof. | secuview.com/product/secuview-smart-wi-fi-waterproof-video-doorbell/ |
   | 3-Gang WiFi Smart Switch | 145 QAR | Control lights + fan from phone. TUYA app. | secuview.com/product/secuview-three-gang-wi-fi-remote-control-smart-switch-with-metal-border/ |
   | PoE Switch 8-Port Gigabit | (enter price) | For CCTV cameras. Plug and play. | secuview.com/product-category/network-communications/poe-switch/ |

4. **Image tips:**
   - Use clear product photos from your website
   - Square or 1:1 ratio works best
   - White or light background preferred

5. Add at least **10-15 products** to start (locks, routers, switches, doorbells, cables)

## Step 4: Set Up Quick Replies (Time Saver)

1. Go to **Business tools** → **Quick replies**
2. Add templates for common questions:

   | Shortcut | Message |
   |----------|---------|
   | `/hours` | Our showroom is open Saturday-Thursday: 7:30 AM - 1:00 PM and 4:00 PM - 9:00 PM. Closed Friday. |
   | `/location` | We're on Salwa Road, Al-Maamourah. Here's our Google Maps link: [your GBP link] |
   | `/catalog` | Browse our products here: [catalog link from Step 6] |
   | `/install` | Yes, we offer professional installation. Call us to schedule. |
   | `/price` | Prices vary by product. Check our catalog or visit the showroom. |

## Step 5: Add WhatsApp Button to secuview.com

Option A — **Plugin method** (easiest):
1. In WP admin, go to **Plugins > Add New**
2. Install **"WhatsApp Button"** or **"Click to Chat"** plugin
3. Set the number to your WhatsApp Business number (with country code, e.g., 97440012384)
4. Choose position (bottom-right corner recommended)
5. Set greeting message: "Hi! How can we help you today?"

Option B — **Manual method** (if no plugin access):
1. In WP admin, go to **Appearance > Theme File Editor** or use File Manager
2. Add this HTML before the closing `</body>` tag in `footer.php`:

```html
<a href="https://wa.me/97440012384" target="_blank" style="position:fixed;bottom:20px;right:20px;background:#25D366;color:white;padding:12px 20px;border-radius:50px;z-index:9999;text-decoration:none;font-weight:bold;box-shadow:0 2px 10px rgba(0,0,0,0.2);">
  Chat on WhatsApp
</a>
```

## Step 6: Share Your Catalog

1. In WhatsApp Business, go to **Business tools** → **Catalog**
2. Tap the **three dots** → **Share** → Copy the catalog link
3. Your catalog link will look like: `https://wa.me/c/97440012384`
4. Share this link everywhere:
   - Website header/navigation
   - Facebook page bio
   - Instagram bio
   - Email signatures
   - Business cards
   - Google Business Profile (add to GBP description)

## Step 7 (Optional) — Click-to-WhatsApp Ads

Once the catalog is live:

1. Go to **Facebook Ads Manager** or **Meta Business Suite**
2. Create a campaign → Objective: **Messages**
3. Select **WhatsApp** as the destination
4. Target: Qatar, adults 25-55, interests: home security, electronics
5. Budget: Start with **20-50 QAR/day**
6. The ad sends users directly to your WhatsApp with a predefined message

---

## Expected Results

| Metric | Estimate |
|--------|----------|
| Setup time | 30-45 min |
| Product upload time | 10 min per 5 products |
| WhatsApp inquiries | High — Qatar has 90%+ WhatsApp penetration |
| Cost | Free (catalog) / optional paid ads |

---

## Maintenance

- **Weekly:** Check WhatsApp messages and respond within 1-2 hours
- **Monthly:** Update catalog (new products, price changes, remove out of stock)
- **Assign:** Designate one person to handle WhatsApp inquiries during business hours

---

## Quick Start Checklist

```
Day 1:
□ Download WhatsApp Business
□ Set up profile with business info
□ Add 10-15 products to catalog

Day 2:
□ Add Quick Replies (hours, location, catalog)
□ Share catalog link on website + social media
□ Install WhatsApp button plugin on secuview.com

Ongoing:
□ Respond to messages within 2 hours
□ Add new products as they arrive
```
