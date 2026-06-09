<?php
/**
 * Plugin Name: Secuview Organization Schema
 * Description: Adds Organization schema to homepage for knowledge panel in Google.
 * Version: 1.0
 * 
 * INSTALLATION:
 * 1. Copy to wp-content/mu-plugins/ (auto-activates)
 *    OR
 * 2. Copy to wp-content/plugins/ and activate manually
 * 
 * NOTES:
 * - Shows company info in Google knowledge panel
 * - Validate at: https://search.google.com/test/rich-results
 * - Update social URLs and contact info as needed
 */

add_action('wp_head', function () {
    if (!is_front_page()) return;

    $schema = [
        '@context' => 'https://schema.org',
        '@type' => 'Organization',
        'name' => 'Secuview',
        'alternateName' => 'Starfox Security System',
        'url' => 'https://secuview.com',
        'logo' => 'https://secuview.com/wp-content/uploads/secuview-logo.png',
        'description' => 'Secuview is a division of Starfox Security System (est. 2005), providing smart home security, CCTV, access control, PA systems, and networking products in Qatar.',
        'foundingDate' => '2005',
        'address' => [
            '@type' => 'PostalAddress',
            'streetAddress' => 'Salwa Road',
            'addressLocality' => 'Doha',
            'addressRegion' => 'Doha',
            'addressCountry' => 'QA',
        ],
        'contactPoint' => [
            '@type' => 'ContactPoint',
            'telephone' => '+974-4412-XXXX',  // UPDATE
            'contactType' => 'sales',
            'areaServed' => 'QA',
            'availableLanguage' => ['English', 'Arabic'],
        ],
        'sameAs' => [
            'https://www.facebook.com/secuview',
            'https://www.instagram.com/secuview',
            'https://www.linkedin.com/company/secuview',
        ],
        'knowsAbout' => [
            'Smart Home Security',
            'CCTV Systems',
            'Access Control',
            'PA Systems',
            'PoE Switches',
            'Network Equipment',
            'Smart Locks',
            'Video Doorbells',
        ],
        'areaServed' => [
            '@type' => 'Country',
            'name' => 'Qatar',
        ],
        'parentOrganization' => [
            '@type' => 'Organization',
            'name' => 'Starfox Security System',
            'url' => 'https://starfoxsecu.com',
        ],
    ];

    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
});
