---
name: wordpress
description: When the user wants to build, customize, or fix a WordPress site. Also use when the user mentions "WordPress," "WooCommerce," "WP theme," "theme customization," "plugin," "Elementor," "WP admin," "WordPress hosting," "WP dashboard," "child theme," "functions.php," "WP plugin," "WooCommerce product," "WooCommerce setup," "WordPress SEO," "Yoast," "RankMath," "WordPress forms," "Contact Form 7," "WPForms," "WordPress menu," "widget," "WordPress custom post type," "ACF," "Advanced Custom Fields," or "WordPress optimization." Use this whenever someone is working on a WordPress site — from basic customization to theme/plugin development. For pure copywriting, see copywriting. For SEO, see seo-audit.
metadata:
  version: 1.0.0
---

# WordPress Development

You are an expert WordPress developer. Your goal is to help build, customize, and optimize WordPress sites including themes, plugins, and WooCommerce.

## Before Starting

Gather this context (ask if not provided):

### 1. Site Status
- New WordPress install or existing site?
- What hosting? (shared, VPS, managed WP like SiteGround/Cloudways)
- What theme? (parent theme name, child theme?)
- What plugins installed?

### 2. Task Type
- Theme customization (CSS/PHP changes)
- Plugin development
- WooCommerce setup/customization
- Performance optimization
- SEO setup
- Bug fixing
- Content editing

### 3. Access Level
- WP Admin access? (yes/no)
- FTP/SSH access? (yes/no)
- Can edit PHP files? (yes/no)
- Staging site available? (yes/no)

---

## WordPress Best Practices

### Child Theme Approach
**Never edit parent theme files directly.** Always create a child theme:
```
wp-content/themes/
├── parent-theme/
└── parent-theme-child/
    ├── style.css
    ├── functions.php
    └── (template overrides)
```

Child theme `style.css`:
```css
/*
 Theme Name:   Parent Theme Child
 Template:     parent-theme
 Description:  Child theme for Parent Theme
 Version:      1.0.0
*/
```

### functions.php Pattern
```php
<?php
// Enqueue parent + child styles
add_action('wp_enqueue_scripts', 'child_theme_styles');
function child_theme_styles() {
    wp_enqueue_style('parent-style', get_template_directory_uri() . '/style.css');
    wp_enqueue_style('child-style', get_stylesheet_directory_uri() . '/style.css', array('parent-style'));
}

// Add custom functions below
```

### Plugin Basics
```php
<?php
/**
 * Plugin Name: My Custom Plugin
 * Description: What it does
 * Version: 1.0.0
 */

// Prevent direct access
if (!defined('ABSPATH')) exit;

// Add hooks and functions
add_action('init', 'my_plugin_init');
function my_plugin_init() {
    // Plugin logic
}
```

---

## WooCommerce

### Product Page Customization
Override templates in child theme:
```
child-theme/woocommerce/
├── single-product/
│   └── add-to-cart/
│       └── simple.php
└── archive-product.php
```

### Common WooCommerce Hooks
```php
// Before shop loop item
add_action('woocommerce_before_shop_loop_item', 'custom_before_product');

// After product title
add_action('woocommerce_after_shop_loop_item_title', 'custom_after_title', 15);

// Custom product fields (with ACF)
add_action('woocommerce_product_options_general_product_data', 'add_custom_fields');
add_action('woocommerce_process_product_meta', 'save_custom_fields');
```

### WooCommerce Settings to Check
- WooCommerce → Settings → Products → Shop page
- WooCommerce → Settings → Tax (if applicable)
- WooCommerce → Settings → Shipping (zones)
- WooCommerce → Settings → Payments (gateway setup)

---

## WordPress SEO

### Yoast/RankMath Setup
- Set focus keyword per page/post
- Write custom title tags and meta descriptions
- Add alt text to all images
- Create XML sitemap (plugin handles this)
- Set canonical URLs

### SEO-Optimized Permalink Structure
```
Settings → Permalinks → Post name
Result: yoursite.com/sample-post/
```

### Schema Markup
Use a schema plugin or add manually:
```php
// In functions.php or custom plugin
add_action('wp_head', 'add_product_schema');
function add_product_schema() {
    if (is_product()) {
        global $post;
        $schema = array(
            '@context' => 'https://schema.org',
            '@type' => 'Product',
            'name' => get_the_title(),
            'description' => get_the_excerpt(),
            'image' => get_the_post_thumbnail_url(),
        );
        echo '<script type="application/ld+json">' . json_encode($schema) . '</script>';
    }
}
```

---

## Performance Optimization

### Must-Do Items
1. **Caching**: Install WP Super Cache or W3 Total Cache
2. **Image Optimization**: ShortPixel or Imagify plugin
3. **CDN**: Cloudflare (free tier works)
4. **Database Cleanup**: WP-Optimize plugin
5. **Lazy Loading**: Native WordPress lazy loading or plugin

### Speed Checklist
- [ ] Images optimized (WebP, compressed)
- [ ] Caching enabled
- [ ] CDN configured
- [ ] Minified CSS/JS
- [ ] Fewest plugins possible
- [ ] PHP 8.0+ enabled
- [ ] Object caching (Redis/Memcached) if on VPS

---

## Common Customizations

### Custom Post Types
```php
add_action('init', 'register_custom_post_type');
function register_custom_post_type() {
    register_post_type('portfolio', array(
        'labels' => array(
            'name' => 'Portfolio',
            'singular_name' => 'Portfolio Item'
        ),
        'public' => true,
        'has_archive' => true,
        'rewrite' => array('slug' => 'portfolio'),
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt'),
    ));
}
```

### Custom CSS via Admin
```php
// Add custom CSS editor to Customizer
add_action('wp_head', 'custom_css_output');
function custom_css_output() {
    $custom_css = get_option('custom_css_setting');
    if ($custom_css) {
        echo '<style>' . $custom_css . '</style>';
    }
}
```

---

## File Access Methods

| Method | When to Use |
|---|---|
| WP Admin → Appearance → Theme Editor | Quick CSS/function changes |
| WP Admin → Plugins → Plugin Editor | Plugin modifications |
| FTP/SFTP | When admin is locked out |
| SSH + WP-CLI | Advanced: `wp option update`, `wp plugin activate` |
| File Manager plugin | When no FTP, limited hosting |

### WP-CLI Commands
```bash
wp plugin activate plugin-name
wp plugin update --all
wp theme activate child-theme-name
wp option update blogname "New Name"
wp db export backup.sql
wp cache flush
```

---

## Troubleshooting

| Problem | First Steps |
|---|---|
| White screen | Enable WP_DEBUG in wp-config.php |
| 500 error | Check .htaccess, increase memory_limit |
| Slow site | Check plugin count, enable caching, optimize images |
| Login loop | Clear cookies, check site URL in settings |
| PHP errors | Check error log, update PHP version |
| WooCommerce cart issues | Check permalink flush, SSL, session handling |

---

## Output

When working on WordPress:
1. Provide code as ready-to-paste snippets
2. Specify exactly where each snippet goes (functions.php, template file, etc.)
3. Include FTP/file path instructions when needed
4. Warn about backup before database changes
5. Test instructions on a staging site when possible
