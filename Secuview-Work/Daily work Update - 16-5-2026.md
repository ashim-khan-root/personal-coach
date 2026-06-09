
1- Researched for Secuview Branding on every Social media Platform.

2- wrote blog on Secuview about #### [Night Security for Your Villa: Tips & Solutions from Secuview](https://secuview.com/night-security-for-your-villa-tips-solutions-secuview/)


3- Fixed Robot.txt issues.. before many no important page indexing and this costs -Googlebot wastes crawl budget on junk pages

4- i will do this after migration - 
  You have two conflicting viewport tags in <head>:
<meta name="viewport" content="initial-scale=1.0" />    <!-- Line A -->
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />  <!-- Line B -->
	Line A comes from the Electron theme's header.php (hardcoded).  
	Line B is added by Elementor (or another plugin/theme customizer setting).
	The maximum-scale=1 on Line B disables pinch-zoom, which is an accessibility WCAG failure.

4-    Did this Best practice on Rank Math SEO Plugin - 
        General Setup (Dashboard → Rank Math)
	1. Module Configuration
	- 
	Enable modules you need: WooCommerce, Local SEO, SEO Analysis, 404 Monitor, Redirections, Link Module, Image SEO, Schema (Structured Data)
	- 
	Disable modules you don't need: BBPress, News Sitemap, Video Sitemap (unless you use these)
	1. General Settings → Links
	- 
	NoFollow External Links: Turn ON (preserve link equity)
	- 
	Open External Links in New Tab: Turn ON (better UX)
	- 
	NoFollow "Reply" links on comments: Turn ON
	1. General Settings → Breadcrumbs
	- 
	Enable breadcrumbs: Turn ON
	- 
	Separator: Use / (clean for SEO)
	- 
	Homepage label: "Home"
	- 
	Show prefix on archive pages: Disable
	- 
	Rich snippet type: BreadcrumbList (this adds Google-friendly breadcrumb schema)
	WooCommerce-Specific (Rank Math → Titles & Meta)
	1. Product Page Titles
	- 
	Go to Titles & Meta → Post Types → Products
	- 
	Single Product Title: %title% | %sitename%
	- 
	Single Product Description: %excerpt% (use the product short description)
	- 
	Add product schema: Enable "Add Product Schema" in WooCommerce settings
	1. Product Category Pages
	- 
	Archive Title: %category% | %sitename% (cleaner than default)
	- 
	Archive Description: Write 150-300 words of unique content per category page
	- 
	Add FAQ schema to category pages via Schema module for rich snippets
	1. NoIndex Low-Value Pages
	- 
	Go to Titles & Meta → WooCommerce
	- 
	Cart Page: No Index
	- 
	Checkout Page: No Index  
	- 
	My Account Page: No Index
	- 
	Order Received Page: No Index
	- 
	Product Tags Archive: No Index (thin content)
	- 
	Shop Page: Index (this is your main shop)
	Sitemap Configuration (Rank Math → Sitemap Settings)
	1. Sitemap Optimization
	- 
	Enable XML Sitemap: ON
	- 
	Exclude from sitemap: cart, checkout, my-account, register, login, order-received, order-tracking, add-to-card, wishlist, logout, password-reset, dashboard, payment, thank-you, user, members, affiliate-dashboard, browsing-history
	- 
	Remove Author sitemap: Go to Sitemap Settings → Authors → Disable sitemap
	- 
	Images in sitemap: Keep enabled (helps Google Discover)
	- 
	Links per sitemap: Default 200 is fine
	Schema (Structured Data) Setup
	1. Schema for Homepage
	- 
	Go to Edit Homepage → Rank Math Schema
	- 
	Set type to: Organization (not WebPage)
	- 
	Fill: Name, Logo, Description, ContactPoint (phone: 77888544), Opening Hours
	- 
	This powers the Knowledge Panel in Google
	1. Product Schema (Critical for Ecommerce)
	- 
	Rank Math automatically adds Product schema when WooCommerce module is enabled
	- 
	Verify: Google Rich Results Test → check for: name, image, price, availability, SKU
	- 
	Ensure AggregateRating schema is added for products with reviews
	1. FAQ Schema on Category Pages
	- 
	Add a FAQ section on each category page (e.g., "What's the best CCTV system in Qatar?")
	- 
	Use Rank Math's FAQ block or the Schema module to mark it up as FAQ schema
	- 
	This earns expandable rich snippets in search results
	Redirections (Rank Math → Redirections)
	1. Set Up 301 Redirects
	- 
	Redirect /categories/ → / (if still accessible)
	- 
	Redirect /add-to-card/ → /cart/ (fix the typo path)
	- 
	Redirect any old/deleted product URLs to relevant category or similar product
	- 
	Enable 404 Monitor to catch broken links automatically
	Advanced: Image & Local SEO
	1. Image SEO (Rank Math → Image SEO)
	- 
	Add missing alt text: Turn ON
	- 
	Alt text template: %title% %filename% 
	- 
	Title attribute: Keep blank (not needed for SEO)
	1. Local SEO (If you serve Qatar specifically)
	- 
	Go to Rank Math → Local SEO
	- 
	Set: Street Address, Phone (77888544), Map Coordinates
	- 
	Add Service Area: Qatar (Doha)
	- 
	This powers local search "near me" queries