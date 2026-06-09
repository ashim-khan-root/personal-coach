<?php
/**
 * Plugin Name: Secuview Breadcrumb Schema
 * Description: Adds BreadcrumbList schema for navigation breadcrumbs in search results.
 * Version: 1.0
 * 
 * INSTALLATION:
 * 1. Copy to wp-content/mu-plugins/ (auto-activates)
 *    OR
 * 2. Copy to wp-content/plugins/ and activate manually
 * 
 * NOTES:
 * - Shows breadcrumb trail in Google search results
 * - Requires a breadcrumb function or Yoast/RankMath breadcrumbs
 * - Validate at: https://search.google.com/test/rich-results
 */

add_action('wp_head', function () {
    if (is_front_page()) return;

    $breadcrumbs = [];
    $position = 1;

    // Home
    $breadcrumbs[] = [
        '@type' => 'ListItem',
        'position' => $position++,
        'name' => 'Home',
        'item' => home_url('/'),
    ];

    // WooCommerce category
    if (is_product()) {
        global $product;
        if ($product) {
            $categories = get_the_terms(get_the_ID(), 'product_cat');
            if ($categories && !is_wp_error($categories)) {
                $cat = $categories[0];
                // Parent category
                if ($cat->parent) {
                    $parent = get_term($cat->parent);
                    if ($parent && !is_wp_error($parent)) {
                        $breadcrumbs[] = [
                            '@type' => 'ListItem',
                            'position' => $position++,
                            'name' => $parent->name,
                            'item' => get_term_link($parent),
                        ];
                    }
                }
                $breadcrumbs[] = [
                    '@type' => 'ListItem',
                    'position' => $position++,
                    'name' => $cat->name,
                    'item' => get_term_link($cat),
                ];
            }
            // Product
            $breadcrumbs[] = [
                '@type' => 'ListItem',
                'position' => $position++,
                'name' => get_the_title(),
                'item' => get_permalink(),
            ];
        }
    }

    // Product category page
    elseif (is_product_category()) {
        $category = get_queried_object();
        if ($category && isset($category->term_id)) {
            if ($category->parent) {
                $parent = get_term($category->parent);
                if ($parent && !is_wp_error($parent)) {
                    $breadcrumbs[] = [
                        '@type' => 'ListItem',
                        'position' => $position++,
                        'name' => $parent->name,
                        'item' => get_term_link($parent),
                    ];
                }
            }
            $breadcrumbs[] = [
                '@type' => 'ListItem',
                'position' => $position++,
                'name' => $category->name,
                'item' => get_term_link($category),
            ];
        }
    }

    // Blog post
    elseif (is_single()) {
        $breadcrumbs[] = [
            '@type' => 'ListItem',
            'position' => $position++,
            'name' => 'Blog',
            'item' => get_post_type_archive_link('post'),
        ];
        $breadcrumbs[] = [
            '@type' => 'ListItem',
            'position' => $position++,
            'name' => get_the_title(),
            'item' => get_permalink(),
        ];
    }

    // Page
    elseif (is_page()) {
        $breadcrumbs[] = [
            '@type' => 'ListItem',
            'position' => $position++,
            'name' => get_the_title(),
            'item' => get_permalink(),
        ];
    }

    // Shop page
    elseif (is_shop()) {
        $breadcrumbs[] = [
            '@type' => 'ListItem',
            'position' => $position++,
            'name' => 'Shop',
            'item' => wc_get_page_permalink('shop'),
        ];
    }

    // Cart / Checkout
    elseif (is_cart() || is_checkout()) {
        $breadcrumbs[] = [
            '@type' => 'ListItem',
            'position' => $position++,
            'name' => 'Shop',
            'item' => wc_get_page_permalink('shop'),
        ];
        $name = is_cart() ? 'Cart' : 'Checkout';
        $breadcrumbs[] = [
            '@type' => 'ListItem',
            'position' => $position++,
            'name' => $name,
            'item' => get_permalink(),
        ];
    }

    if (count($breadcrumbs) < 2) return; // Need at least 2 items

    $schema = [
        '@context' => 'https://schema.org',
        '@type' => 'BreadcrumbList',
        'itemListElement' => $breadcrumbs,
    ];

    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
});
