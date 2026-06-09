<?php
/**
 * Plugin Name: Secuview Product Schema
 * Description: Adds Product schema markup to WooCommerce product pages for rich results in Google.
 * Version: 1.0
 * 
 * INSTALLATION:
 * 1. Copy to wp-content/mu-plugins/ (auto-activates)
 *    OR
 * 2. Copy to wp-content/plugins/ and activate manually
 * 
 * NOTES:
 * - Requires WooCommerce to be installed
 * - Works with WP admin only (no FTP needed)
 * - Validate at: https://search.google.com/test/rich-results
 */

add_action('wp_head', function () {
    if (!is_product()) return;

    global $product;
    if (!$product) return;

    // Get product data
    $name = get_the_title();
    $description = wp_strip_all_tags($product->get_short_description());
    if (empty($description)) {
        $description = wp_strip_all_tags(get_the_excerpt());
    }
    $url = get_permalink();
    $image = get_the_post_thumbnail_url(get_the_ID(), 'large');
    if (!$image) {
        $image = wp_get_attachment_url(get_post_thumbnail_id());
    }

    // Price
    $price = $product->get_price();
    $regular_price = $product->get_regular_price();
    $sale_price = $product->get_sale_price();
    $currency = 'QAR'; // Qatar Riyal

    // Availability
    $stock_status = $product->get_stock_status();
    if ($stock_status === 'instock') {
        $availability = 'https://schema.org/InStock';
    } elseif ($stock_status === 'outofstock') {
        $availability = 'https://schema.org/OutOfStock';
    } else {
        $availability = 'https://schema.org/PreOrder';
    }

    // SKU
    $sku = $product->get_sku();

    // Brand (if set in product meta)
    $brand = get_post_meta(get_the_ID(), '_yoast_wpseo_primary_brand', true);

    // Category
    $categories = get_the_terms(get_the_ID(), 'product_cat');
    $category_name = '';
    if ($categories && !is_wp_error($categories)) {
        $category_name = $categories[0]->name;
    }

    // Rating
    $rating_count = $product->get_rating_count();
    $average_rating = $product->get_average_rating();

    // Build schema
    $schema = [
        '@context' => 'https://schema.org',
        '@type' => 'Product',
        'name' => $name,
        'description' => $description,
        'url' => $url,
    ];

    if ($image) {
        $schema['image'] = $image;
    }

    if ($sku) {
        $schema['sku'] = $sku;
    }

    if ($brand) {
        $schema['brand'] = [
            '@type' => 'Brand',
            'name' => $brand,
        ];
    } elseif ($category_name) {
        $schema['brand'] = [
            '@type' => 'Brand',
            'name' => 'Secuview',
        ];
    }

    // Offers
    $schema['offers'] = [
        '@type' => 'Offer',
        'url' => $url,
        'priceCurrency' => $currency,
        'price' => $price ?: $regular_price,
        'availability' => $availability,
        'itemCondition' => 'https://schema.org/NewCondition',
        'seller' => [
            '@type' => 'Organization',
            'name' => 'Secuview',
        ],
    ];

    if ($sale_price && $regular_price) {
        $schema['offers']['priceValidUntil'] = date('Y-m-d', strtotime('+1 year'));
    }

    // Aggregate Rating (if reviews exist)
    if ($rating_count > 0) {
        $schema['aggregateRating'] = [
            '@type' => 'AggregateRating',
            'ratingValue' => $average_rating,
            'reviewCount' => $rating_count,
            'bestRating' => '5',
            'worstRating' => '1',
        ];
    }

    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
});
