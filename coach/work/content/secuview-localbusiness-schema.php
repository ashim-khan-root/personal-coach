<?php
/**
 * Plugin Name: Secuview LocalBusiness Schema
 * Description: Adds LocalBusiness schema to homepage for local search visibility in Qatar.
 * Version: 1.0
 * 
 * INSTALLATION:
 * 1. Copy to wp-content/mu-plugins/ (auto-activates)
 *    OR
 * 2. Copy to wp-content/plugins/ and activate manually
 * 
 * NOTES:
 * - Shows business info in Google Maps and local search
 * - Validate at: https://search.google.com/test/rich-results
 * - Update phone/address/hours as needed
 */

add_action('wp_head', function () {
    if (!is_front_page()) return;

    $schema = [
        '@context' => 'https://schema.org',
        '@type' => 'LocalBusiness',
        'name' => 'Secuview - Starfox Security System',
        'alternateName' => 'Starfox Security System',
        'description' => 'Smart home security, CCTV, access control, PA systems, and networking products in Qatar. Professional installation and support.',
        'url' => 'https://secuview.com',
        'telephone' => '+974-4412-XXXX',  // UPDATE with actual phone
        'email' => 'info@secuview.com',
        'address' => [
            '@type' => 'PostalAddress',
            'streetAddress' => 'Salwa Road',  // UPDATE with full address
            'addressLocality' => 'Doha',
            'addressRegion' => 'Doha',
            'postalCode' => '',
            'addressCountry' => 'QA',
        ],
        'geo' => [
            '@type' => 'GeoCoordinates',
            'latitude' => 25.2854,  // UPDATE with exact coordinates
            'longitude' => 51.5310,
        ],
        'openingHoursSpecification' => [
            [
                '@type' => 'OpeningHoursSpecification',
                'dayOfWeek' => ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday'],
                'opens' => '09:00',
                'closes' => '21:00',
            ],
            [
                '@type' => 'OpeningHoursSpecification',
                'dayOfWeek' => 'Friday',
                'opens' => '16:00',
                'closes' => '21:00',
            ],
        ],
        'image' => 'https://secuview.com/wp-content/uploads/secuview-showroom.jpg',  // UPDATE with showroom photo
        'logo' => 'https://secuview.com/wp-content/uploads/secuview-logo.png',
        'priceRange' => '$$',
        'paymentAccepted' => 'Cash, Credit Card, Bank Transfer',
        'currenciesAccepted' => 'QAR',
        'areaServed' => [
            '@type' => 'Country',
            'name' => 'Qatar',
        ],
        'hasOfferCatalog' => [
            '@type' => 'OfferCatalog',
            'name' => 'Secuview Products',
            'itemListElement' => [
                [
                    '@type' => 'OfferCatalog',
                    'name' => 'Smart Home',
                    'itemListElement' => [
                        ['@type' => 'Offer', 'itemOffered' => ['@type' => 'Product', 'name' => 'Smart Locks']],
                        ['@type' => 'Offer', 'itemOffered' => ['@type' => 'Product', 'name' => 'Smart Switches']],
                        ['@type' => 'Offer', 'itemOffered' => ['@type' => 'Product', 'name' => 'Video Doorbells']],
                    ],
                ],
                [
                    '@type' => 'OfferCatalog',
                    'name' => 'Security',
                    'itemListElement' => [
                        ['@type' => 'Offer', 'itemOffered' => ['@type' => 'Product', 'name' => 'CCTV Systems']],
                        ['@type' => 'Offer', 'itemOffered' => ['@type' => 'Product', 'name' => 'Access Control']],
                        ['@type' => 'Offer', 'itemOffered' => ['@type' => 'Product', 'name' => 'Time Attendance']],
                    ],
                ],
                [
                    '@type' => 'OfferCatalog',
                    'name' => 'Networking',
                    'itemListElement' => [
                        ['@type' => 'Offer', 'itemOffered' => ['@type' => 'Product', 'name' => 'PoE Switches']],
                        ['@type' => 'Offer', 'itemOffered' => ['@type' => 'Product', 'name' => 'Routers']],
                        ['@type' => 'Offer', 'itemOffered' => ['@type' => 'Product', 'name' => 'Access Points']],
                        ['@type' => 'Offer', 'itemOffered' => ['@type' => 'Product', 'name' => 'Network Cables']],
                    ],
                ],
            ],
        ],
        'sameAs' => [
            'https://www.facebook.com/secuview',
            'https://www.instagram.com/secuview',
            'https://www.linkedin.com/company/secuview',
        ],
    ];

    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
});
