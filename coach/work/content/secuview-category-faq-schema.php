<?php
/**
 * Plugin Name: Secuview Category FAQ Schema
 * Description: Adds FAQ schema to WooCommerce category pages via MU plugin. No visible text on page.
 * Version: 1.0
 */

add_action('wp_head', function () {
    if (!is_product_category()) return;

    $category = get_queried_object();
    if (!$category || !isset($category->slug)) return;

    $schema = get_faq_schema_for_category($category->slug);
    if (!$schema) return;

    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
});

function get_faq_schema_for_category($slug) {
    $faqs = [
        'smart-lock' => [
            ['name' => 'What types of smart locks do you sell in Qatar?', 'text' => 'Secuview offers fingerprint smart locks, app-controlled locks, keyless entry locks, glass door locks, and WiFi-enabled door locks in Doha.'],
            ['name' => 'How much do smart locks cost in Qatar?', 'text' => 'Secuview smart locks range from 480 QAR for basic mobile control locks to 1,300 QAR for waterproof courtyard gate locks. Most fingerprint models are 550-750 QAR.'],
            ['name' => 'Can I control my smart lock from my phone?', 'text' => 'Yes. Most Secuview smart locks are Tuya app-compatible, allowing you to lock/unlock remotely, share temporary passwords, and check access logs.'],
            ['name' => 'Do you install smart locks in Doha?', 'text' => 'Yes. Secuview provides professional installation for all smart locks across Doha and Qatar with warranty support.'],
        ],
        'poe-switch' => [
            ['name' => 'What is a PoE switch?', 'text' => 'A PoE (Power over Ethernet) switch delivers both data and electrical power to devices like CCTV cameras and access points through a single Ethernet cable. No separate power outlet needed.'],
            ['name' => 'How many ports do I need for my CCTV system?', 'text' => 'For home use, an 8-port PoE switch is usually enough. For offices or large installations, 16-port or 24-port models are recommended.'],
            ['name' => 'What is PoE budget and why does it matter?', 'text' => 'PoE budget is the total power the switch can deliver to all connected devices. A 300W PoE switch can power more cameras than a 120W model. Always check total wattage of your devices before buying.'],
            ['name' => 'Do you deliver PoE switches in Qatar?', 'text' => 'Yes. Secuview delivers PoE switches across Doha and all of Qatar with warranty and support.'],
        ],
        'smart-switch' => [
            ['name' => 'What are WiFi smart switches?', 'text' => 'WiFi smart switches replace your regular wall switches. They let you control lights and fans from your phone via the Tuya app, set schedules, and use voice control with Google Home or Alexa.'],
            ['name' => 'Do smart switches work without internet?', 'text' => 'Smart switches need WiFi for remote control and voice commands. However, they still work as regular switches manually even if the internet is down.'],
            ['name' => 'Are Secuview smart switches compatible with Tuya?', 'text' => 'Yes. All Secuview WiFi smart switches and sockets are Tuya-compatible, so you can control them from one app alongside other smart home devices.'],
            ['name' => 'Can I install smart switches myself?', 'text' => 'We recommend professional installation for safety, especially for replacing existing wall switches. Secuview offers installation services in Doha.'],
        ],
        'access-point-router' => [
            ['name' => 'What is the difference between a router and an access point?', 'text' => 'A router connects your home to the internet and assigns IP addresses. An access point extends WiFi coverage to areas your router cannot reach, like a second floor or garden.'],
            ['name' => 'Which router is best for a large villa in Qatar?', 'text' => 'For large villas, a dual-band WiFi 6 router or mesh system is recommended. Secuview carries high-power routers suitable for Qatar homes.'],
            ['name' => 'Do you offer 4G LTE routers in Qatar?', 'text' => 'Yes. Secuview sells outdoor 4G LTE routers with SIM card support, ideal for backup internet or areas without fiber connectivity.'],
        ],
        'cctv-system' => [
            ['name' => 'What CCTV camera is best for home in Qatar?', 'text' => 'For homes, 4K IP cameras with night vision and weatherproof rating are recommended. Secuview offers a range suitable for Qatar climate.'],
            ['name' => 'How much does a CCTV system cost in Qatar?', 'text' => 'CCTV system prices vary based on camera count and features. Entry-level systems start around 500 QAR while professional 4K systems range higher. Contact Secuview for a quote.'],
            ['name' => 'Do you install CCTV cameras in Doha?', 'text' => 'Yes. Secuview provides professional CCTV installation services across Doha and Qatar with warranty coverage.'],
        ],
        'pa-system' => [
            ['name' => 'What PA system do I need for a mosque in Qatar?', 'text' => 'For mosques, a 150W to 480W amplifier with ceiling speakers is recommended. The exact setup depends on prayer hall size and whether you need separate zones for men and women.'],
            ['name' => 'What PA system is best for a school?', 'text' => 'Schools need a 100W to 380W amplifier with ceiling speakers in classrooms and wall-mounted speakers in corridors. Multiple zones allow separate control per floor.'],
            ['name' => 'Can I play recorded audio through a PA system?', 'text' => 'Yes. Most Secuview amplifiers include AUX input, USB, or Bluetooth for playing recorded audio from a phone or computer.'],
        ],
        'time-attendance-access-control' => [
            ['name' => 'What is a biometric attendance system?', 'text' => 'A biometric attendance system uses fingerprints or face recognition to record when employees clock in and out. It prevents buddy punching and creates accurate payroll data.'],
            ['name' => 'How much does a fingerprint attendance machine cost in Qatar?', 'text' => 'Secuview offers fingerprint attendance systems from 500 QAR and face recognition systems from 600 QAR — affordable options for Qatari businesses.'],
            ['name' => 'Can I export attendance data to Excel?', 'text' => 'Yes. Secuview attendance systems support USB export and cloud-based reporting. Data can be exported as CSV or Excel files for payroll processing.'],
        ],
        'cable' => [
            ['name' => 'What type of network cable is best for home in Qatar?', 'text' => 'CAT6 cable is recommended for most homes. It supports faster speeds up to 10 Gbps and is suitable for CCTV cameras, internet, and smart home devices.'],
            ['name' => 'What is the difference between CAT5e and CAT6?', 'text' => 'CAT6 supports higher speeds (up to 10 Gbps) and has better interference protection than CAT5e (up to 1 Gbps). For new installations in Qatar, CAT6 is the better choice.'],
            ['name' => 'Do you sell network cables by length in Qatar?', 'text' => 'Yes. Secuview sells CAT6 and coaxial cables in various lengths. Visit our showroom on Salwa Road or order online.'],
        ],
        'rack' => [
            ['name' => 'What size server rack do I need?', 'text' => 'The rack size depends on your equipment. A 9U to 12U rack works for small setups. Larger installations need 22U to 27U racks. All sizes available at Secuview in Doha.'],
            ['name' => 'Do you deliver server racks in Qatar?', 'text' => 'Yes. Secuview delivers server racks and network cabinets across Doha and Qatar.'],
        ],
        'ir-converter' => [
            ['name' => 'What is an IR converter?', 'text' => 'An IR converter lets you control AC units, TVs, and other IR devices from your phone via the Tuya app. It learns your remote signals and sends them over WiFi.'],
            ['name' => 'Does the IR converter work with all AC brands in Qatar?', 'text' => 'Most brands are supported. The IR converter learns from your existing remote, so it works with any brand that uses infrared.'],
        ],
        'smart-doorphone' => [
            ['name' => 'What is a video doorphone?', 'text' => 'A video doorphone lets you see and talk to visitors at your gate or door from inside your home or via your phone app. It includes a camera, microphone, speaker, and unlock function.'],
            ['name' => 'Can I unlock the door from my phone?', 'text' => 'Yes. Secuview smart doorphones with Tuya app support let you see who is at the door and unlock it remotely from anywhere.'],
        ],
    ];

    if (!isset($faqs[$slug])) return null;

    $mainEntity = [];
    foreach ($faqs[$slug] as $faq) {
        $mainEntity[] = [
            '@type' => 'Question',
            'name' => $faq['name'],
            'acceptedAnswer' => [
                '@type' => 'Answer',
                'text' => $faq['text'],
            ],
        ];
    }

    return [
        '@context' => 'https://schema.org',
        '@type' => 'FAQPage',
        'mainEntity' => $mainEntity,
    ];
}
