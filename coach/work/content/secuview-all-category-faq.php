<?php
/**
 * Plugin Name: Secuview Category FAQ Schema (All Categories)
 * Description: Adds FAQ schema JSON-LD to all main product category pages
 * Version: 1.0
 */

add_action('wp_head', function () {
    $uri = $_SERVER['REQUEST_URI'] ?? '';

    // === Smart Home ===
    if (strpos($uri, '/product-category/smart-home/') !== false) {
        ?>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Best smart locks in Qatar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview offers fingerprint, mobile-controlled, and keyless smart locks in Doha with free delivery and local support."
      }
    },
    {
      "@type": "Question",
      "name": "Which smart switches work with Tuya in Qatar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview WiFi smart switches and sockets are Tuya-compatible, allowing remote control via app from anywhere in Doha."
      }
    },
    {
      "@type": "Question",
      "name": "Do you offer installation for smart home devices in Doha?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview provides professional installation services for smart locks, doorphones, and home automation across Qatar."
      }
    },
    {
      "@type": "Question",
      "name": "What smart home products do you sell in Qatar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview stocks smart locks, WiFi switches, video doorphones, IR converters, central control panels, and smart lights — all available in Doha."
      }
    }
  ]
}
</script>
        <?php
    }

    // === Security Surveillance ===
    if (strpos($uri, '/product-category/security-surveillance/') !== false) {
        ?>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Best CCTV cameras in Qatar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview offers a wide range of CCTV surveillance cameras in Qatar including dome, bullet, and PTZ cameras for home and business security."
      }
    },
    {
      "@type": "Question",
      "name": "Which security cameras are MOI compliant in Doha?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview supplies MOI-compliant CCTV systems approved for use across Qatar. Contact us for certified solutions tailored to your requirements."
      }
    },
    {
      "@type": "Question",
      "name": "Do you install surveillance cameras in Qatar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, Secuview provides professional installation services for CCTV cameras, security systems, and surveillance setups across Doha and all of Qatar."
      }
    },
    {
      "@type": "Question",
      "name": "What is the difference between WiFi and 4G cameras?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "WiFi cameras connect to your home network, while 4G cameras use a mobile data connection — ideal for remote sites in Qatar without internet access."
      }
    }
  ]
}
</script>
        <?php
    }

    // === Network & Communications ===
    if (strpos($uri, '/product-category/network-communications/') !== false) {
        ?>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Best POE switches in Qatar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview supplies POE switches in Qatar for CCTV and network setups, with options from 4 to 24 ports for homes and businesses in Doha."
      }
    },
    {
      "@type": "Question",
      "name": "Which access points are best for offices in Doha?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview offers high-performance access points and routers suitable for offices in Qatar, with MOI-compliant options and professional support."
      }
    },
    {
      "@type": "Question",
      "name": "Do you install network infrastructure in Qatar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, Secuview provides end-to-end network installation including switches, routers, cabling, and rack setup for businesses across Doha and Qatar."
      }
    },
    {
      "@type": "Question",
      "name": "What network equipment does Secuview supply in Doha?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview stocks POE switches, ethernet switches, access points, routers, PABX systems, telephone equipment, racks, and network accessories in Qatar."
      }
    }
  ]
}
</script>
        <?php
    }

    // === Audio Products ===
    if (strpos($uri, '/product-category/audio-products/') !== false) {
        ?>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Best PA system for schools in Qatar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview offers PA systems ideal for schools, offices, and events in Qatar with ceiling speakers, hanging speakers, amplifiers, and full audio solutions."
      }
    },
    {
      "@type": "Question",
      "name": "What is the difference between ceiling and hanging speakers?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ceiling speakers are recessed-mounted for clean looks in offices, while hanging speakers project sound over larger areas like warehouses and halls in Qatar."
      }
    },
    {
      "@type": "Question",
      "name": "Do you install audio systems in Doha?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, Secuview provides professional installation for PA systems, background music, and audio setups across schools, offices, and commercial spaces in Qatar."
      }
    },
    {
      "@type": "Question",
      "name": "Do you offer home cinema setup in Qatar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview supplies KTV and home cinema audio equipment in Qatar including active speakers and amplifiers for immersive entertainment setups in Doha."
      }
    }
  ]
}
</script>
        <?php
    }

    // === Cable ===
    if (strpos($uri, '/product-category/cable/') !== false) {
        ?>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Best CCTV cable in Qatar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview supplies high-quality coaxial cables for CCTV systems in Qatar, ensuring clear signal transmission for surveillance setups in Doha."
      }
    },
    {
      "@type": "Question",
      "name": "What network cable do I need for my office in Doha?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Secuview offers Cat5e, Cat6, and network cables suitable for office and security installations in Qatar, with professional guidance on the right type."
      }
    },
    {
      "@type": "Question",
      "name": "What is the difference between coaxial and network cable?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Coaxial cable is used for CCTV video transmission, while network cable (Ethernet) is used for data networks. Secuview stocks both in Doha."
      }
    },
    {
      "@type": "Question",
      "name": "Do you offer cable installation services in Qatar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, Secuview provides certified cable installation services for CCTV, network, audio, and power cabling across residential and commercial projects in Qatar."
      }
    }
  ]
}
</script>
        <?php
    }
});
