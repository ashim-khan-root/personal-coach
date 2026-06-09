# Secuview Schema Markup — Installation Guide

## Files Created

| File | Schema Type | Where It Shows |
|------|-------------|----------------|
| `secuview-product-schema.php` | Product | Product pages — price, availability, ratings in Google |
| `secuview-localbusiness-schema.php` | LocalBusiness | Homepage — address, phone, hours in Google Maps |
| `secuview-organization-schema.php` | Organization | Homepage — company info, knowledge panel |
| `secuview-breadcrumb-schema.php` | BreadcrumbList | All pages — breadcrumb trail in search results |

## Installation (WP Admin Only)

### Step 1: Access File Manager
1. Login to WP Admin
2. Go to **Plugins → File Manager** (or install "File Manager" plugin if not installed)

### Step 2: Upload Files
1. Navigate to `wp-content/mu-plugins/` (create folder if it doesn't exist)
2. Upload all 4 PHP files:
   - `secuview-product-schema.php`
   - `secuview-localbusiness-schema.php`
   - `secuview-organization-schema.php`
   - `secuview-breadcrumb-schema.php`

**Note:** MU plugins auto-activate. No need to go to Plugins page.

If `mu-plugins` folder doesn't exist:
1. Create folder: `wp-content/mu-plugins/`
2. Upload files there

**Alternative:** Upload to `wp-content/plugins/` and activate each manually.

### Step 3: Update Placeholder Values
Search each file for `XXXX` or `UPDATE` and replace with real data:

**LocalBusiness & Organization:**
- Phone: `+974-4412-XXXX` → your real phone
- Address: `Salwa Road` → full address if needed
- Coordinates: Update latitude/longitude
- Showroom photo URL
- Social media URLs

### Step 4: Validate
Test each schema type:
- https://search.google.com/test/rich-results
- Paste your page URL
- Check for errors

### Step 5: Monitor
- Google Search Console → Enhancements
- Check for rich result errors
- Monitor impressions/clicks for product rich results

## What You'll See in Google

| Schema | Rich Result |
|--------|-------------|
| Product | Price, availability, star ratings next to your listing |
| LocalBusiness | Map pin, address, hours, phone in local search |
| Organization | Knowledge panel on right side when searching "secuview" |
| Breadcrumb | `Home > Smart Locks > Fingerprint Lock` instead of URL |

## Expected Impact

- **Product schema**: Products show with price and "In Stock" in Google — higher click-through
- **LocalBusiness**: Appears in "security store doha" map results
- **Organization**: Knowledge panel when people search your brand
- **Breadcrumb**: Cleaner search appearance, better click-through
