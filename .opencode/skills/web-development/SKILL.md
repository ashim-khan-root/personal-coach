---
name: web-development
description: When the user wants to build, create, or code a website from scratch. Also use when the user mentions "build a website," "create a site," "HTML," "CSS," "JavaScript," "responsive design," "landing page code," "portfolio site," "business website," "frontend," "web page," "code my site," "write the HTML," "make a webpage," "static site," "single page app," "web app," or "website from scratch." Use this whenever someone needs actual code (HTML/CSS/JS) to build a website or web page. For site planning/structure, see site-architecture. For marketing copy, see copywriting. For WordPress, see wordpress. For Hugo, see hugo.
metadata:
  version: 1.0.0
---

# Web Development

You are an expert frontend web developer. Your goal is to write clean, modern, responsive HTML, CSS, and JavaScript that produces professional websites.

## Before Coding

Gather this context (ask if not provided):

### 1. Site Purpose
- What type of site? (business, portfolio, landing page, blog, documentation)
- What is the primary action visitors should take?
- Who is the target audience?

### 2. Design Requirements
- Any existing brand colors, fonts, or logo?
- Reference sites they like?
- Mobile-first or desktop-first?
- Dark mode or light mode?

### 3. Content
- How many pages?
- What content goes on each page? (text, images, videos)
- Any specific sections needed? (hero, features, testimonials, pricing, FAQ, contact)

### 4. Technical Requirements
- Static HTML or need a framework?
- Any integrations? (forms, analytics, payment)
- Hosting target? (GitHub Pages, Netlify, Vercel, traditional hosting)

---

## Development Principles

### HTML5 Standards
- Use semantic elements: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- Proper heading hierarchy (h1 → h2 → h3, never skip)
- Alt text on all images
- ARIA labels for accessibility
- Meta tags for SEO (title, description, Open Graph)

### CSS3 Best Practices
- Mobile-first responsive design with media queries
- CSS Grid and Flexbox for layouts
- CSS custom properties (variables) for theming
- Minimal CSS — avoid unnecessary selectors
- Use a consistent spacing scale (4px, 8px, 16px, 24px, 32px, 48px, 64px)

### JavaScript Standards
- Vanilla JS preferred unless framework specified
- Use `const` and `let`, never `var`
- Event delegation over individual event listeners
- Minimal DOM manipulation — prefer CSS for animations
- Progressive enhancement — site works without JS

### Performance
- Optimize images (WebP format, proper sizing)
- Minimize HTTP requests
- Lazy load below-the-fold content
- Inline critical CSS when possible
- Minify CSS and JS for production

---

## UI/UX Design Principles

### Visual Hierarchy
- **F-pattern** for text-heavy pages (headline → left-aligned content)
- **Z-pattern** for landing pages (logo → nav → CTA → bottom CTA)
- Most important element gets the most visual weight
- Use size, color, contrast, and spacing to guide the eye

### Typography
- **Headlines**: Bold, large, high contrast (48-72px desktop, 32-48px mobile)
- **Body**: 16-18px, line-height 1.5-1.7, max-width 65-75 characters
- **Limit font families**: 1-2 max (1 for headings, 1 for body)
- **Font pairing**: serif headings + sans-serif body, or vice versa

### Color System
- **60-30-10 rule**: 60% dominant (bg), 30% secondary (cards/sections), 10% accent (CTAs)
- **Contrast ratio**: 4.5:1 minimum for text, 3:1 for large text
- **Dark mode**: Use CSS custom properties to toggle themes
- **Accent color**: Reserved for CTAs and interactive elements only

### Spacing & Layout
- **Consistent spacing scale**: 4px base → 8, 12, 16, 24, 32, 48, 64, 96
- **Whitespace is active**: It groups elements and creates breathing room
- **Grid alignment**: Align everything to an 8px grid
- **Max content width**: 1200px for pages, 700-800px for articles

### Buttons & CTAs
- **Primary CTA**: High contrast, one per section, clear action verb
- **Size**: Min 44px touch target (mobile), 40px height minimum
- **Padding**: 12px 24px (small), 16px 32px (medium), 20px 40px (large)
- **Border radius**: Match design language (4px subtle, 8px modern, 9999px pill)

### Cards & Containers
- **Subtle shadows** over borders for depth
- **Border radius**: Consistent across all cards (8px or 12px)
- **Padding**: 24-32px internal spacing
- **Hover state**: Slight shadow increase or subtle lift

---

## Animations & Micro-Interactions

### CSS Transitions (Always Use First)
```css
/* Base transition — apply to interactive elements */
.btn, .card, .nav-link, .input {
  transition: all 0.2s ease;
}

/* Specific properties */
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-primary {
  transition: background-color 0.15s ease, transform 0.1s ease;
}

.nav-link {
  transition: color 0.2s ease, border-color 0.2s ease;
}
```

### Hover Effects
```css
/* Card lift */
.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

/* Button press */
.btn:active {
  transform: scale(0.98);
}

/* Image zoom on card hover */
.card:hover .card-image {
  transform: scale(1.05);
}
.card-image {
  transition: transform 0.3s ease;
  overflow: hidden;
}

/* Underline slide-in */
.link-underline {
  position: relative;
}
.link-underline::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--primary);
  transition: width 0.3s ease;
}
.link-underline:hover::after {
  width: 100%;
}

/* Glow effect */
.btn-glow:hover {
  box-shadow: 0 0 20px rgba(37, 99, 235, 0.4);
}
```

### Scroll-Triggered Animations
```css
/* Fade in from bottom */
.fade-in-up {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.fade-in-up.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Fade in from left/right */
.fade-in-left {
  opacity: 0;
  transform: translateX(-30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.fade-in-left.visible {
  opacity: 1;
  transform: translateX(0);
}

/* Scale in */
.scale-in {
  opacity: 0;
  transform: scale(0.9);
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.scale-in.visible {
  opacity: 1;
  transform: scale(1);
}

/* Staggered children */
.stagger-children > * {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.stagger-children.visible > *:nth-child(1) { transition-delay: 0.1s; }
.stagger-children.visible > *:nth-child(2) { transition-delay: 0.2s; }
.stagger-children.visible > *:nth-child(3) { transition-delay: 0.3s; }
.stagger-children.visible > *:nth-child(4) { transition-delay: 0.4s; }
.stagger-children.visible > *:nth-child(5) { transition-delay: 0.5s; }
.stagger-children.visible > * {
  opacity: 1;
  transform: translateY(0);
}
```

### Intersection Observer (Trigger Animations)
```javascript
// Add to main.js
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target); // Animate once
    }
  });
}, observerOptions);

// Observe all animated elements
document.querySelectorAll('.fade-in-up, .fade-in-left, .scale-in, .stagger-children')
  .forEach(el => observer.observe(el));
```

### CSS Keyframe Animations
```css
/* Pulse — for attention */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
.animate-pulse {
  animation: pulse 2s ease-in-out infinite;
}

/* Shake — for errors */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

/* Spin — for loaders */
@keyframes spin {
  to { transform: rotate(360deg); }
}
.loader {
  animation: spin 1s linear infinite;
}

/* Bounce — for CTAs */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* Gradient shift — for hero backgrounds */
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.hero-gradient {
  background: linear-gradient(135deg, var(--primary), var(--accent), var(--primary));
  background-size: 200% 200%;
  animation: gradientShift 8s ease infinite;
}
```

### Parallax Effect
```css
/* Simple CSS parallax */
.parallax-container {
  perspective: 1px;
  height: 100vh;
  overflow-x: hidden;
  overflow-y: auto;
}
.parallax-bg {
  transform: translateZ(-2px) scale(3);
}
.parallax-content {
  transform: translateZ(0);
}
```

### Loading States
```css
/* Skeleton loading */
.skeleton {
  background: linear-gradient(90deg, var(--bg-alt) 25%, var(--border) 50%, var(--bg-alt) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-md);
}
@keyframes shimmer {
  to { background-position: -200% 0; }
}

/* Button loading state */
.btn.loading {
  position: relative;
  color: transparent;
}
.btn.loading::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  top: 50%;
  left: 50%;
  margin: -10px 0 0 -10px;
  border: 2px solid #fff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
```

### Page Transitions
```css
/* Fade between pages */
.page-enter {
  opacity: 0;
  transform: translateY(10px);
}
.page-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

/* Slide-in from side for modals */
.modal-enter {
  transform: translateX(100%);
}
.modal-enter-active {
  transform: translateX(0);
  transition: transform 0.3s ease;
}
```

### Smooth Scrolling
```css
/* Global smooth scroll */
html {
  scroll-behavior: smooth;
}

/* Section offset for fixed nav */
section[id] {
  scroll-margin-top: 80px;
}
```

### Cursor & Interaction Feedback
```css
/* Custom cursor for interactive areas */
.clickable {
  cursor: pointer;
}

/* Focus styles (accessibility + UX) */
.btn:focus-visible, .link:focus-visible, .input:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

/* Disabled state */
.btn:disabled, .btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}
```

### Advanced: GSAP (When CSS Isn't Enough)
```html
<!-- Add before closing body -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
<script>
gsap.registerPlugin(ScrollTrigger);

// Text reveal
gsap.from('.hero-title', {
  y: 50,
  opacity: 0,
  duration: 1,
  ease: 'power3.out'
});

// Staggered cards
gsap.from('.feature-card', {
  scrollTrigger: {
    trigger: '.features-grid',
    start: 'top 80%'
  },
  y: 60,
  opacity: 0,
  duration: 0.6,
  stagger: 0.15,
  ease: 'power2.out'
});

// Counter animation
gsap.to('.counter', {
  scrollTrigger: { trigger: '.stats', start: 'top 80%' },
  textContent: 1000,
  duration: 2,
  snap: { textContent: 1 },
  ease: 'power1.inOut'
});
</script>
```

### Animation Best Practices
- **Less is more**: Animate to guide attention, not to impress
- **Respect prefers-reduced-motion**: Some users get motion sickness
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
- **Performance**: Only animate `transform` and `opacity` (GPU-accelerated)
- **Duration**: 150-300ms for interactions, 500-800ms for page transitions
- **Easing**: `ease` or `ease-out` for entrances, `ease-in` for exits
- **No animation on load**: Let content appear first, then animate on scroll

### SEO
- Unique title tags (50-60 chars)
- Meta descriptions (150-160 chars)
- Proper heading structure
- Schema.org structured data where relevant
- Clean URL structure
- Sitemap.xml and robots.txt

---

## File Structure

Standard project structure:
```
project/
├── index.html
├── css/
│   ├── style.css
│   └── responsive.css
├── js/
│   └── main.js
├── images/
│   └── (optimized images)
├── robots.txt
└── sitemap.xml
```

For single-page sites, keep everything in one folder with inline or embedded CSS/JS.

---

## Common Patterns

### Navigation
```html
<nav class="navbar">
  <div class="container">
    <a href="/" class="logo">Brand</a>
    <button class="menu-toggle" aria-label="Toggle menu">☰</button>
    <ul class="nav-links">
      <li><a href="#features">Features</a></li>
      <li><a href="#pricing">Pricing</a></li>
      <li><a href="#contact">Contact</a></li>
    </ul>
  </div>
</nav>
```

### Hero Section
```html
<section class="hero">
  <div class="container">
    <h1>Clear headline with value proposition</h1>
    <p>Supporting text that explains the benefit</p>
    <a href="#cta" class="btn btn-primary">Primary Action</a>
  </div>
</section>
```

### Footer
```html
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">Brand info</div>
      <div class="footer-links">Navigation</div>
      <div class="footer-contact">Contact info</div>
    </div>
    <div class="footer-bottom">© 2026 Brand. All rights reserved.</div>
  </div>
</footer>
```

---

## CSS Variables Template

```css
:root {
  /* Colors */
  --primary: #2563eb;
  --primary-dark: #1d4ed8;
  --secondary: #64748b;
  --accent: #f59e0b;
  --text: #1e293b;
  --text-light: #64748b;
  --bg: #ffffff;
  --bg-alt: #f8fafc;
  --border: #e2e8f0;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;

  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Borders */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
}
```

---

## Responsive Breakpoints

```css
/* Mobile first — base styles are mobile */
/* Tablet */
@media (min-width: 768px) { ... }
/* Desktop */
@media (min-width: 1024px) { ... }
/* Large desktop */
@media (min-width: 1280px) { ... }
```

---

## Output

When building a site:
1. Create all files with complete, working code
2. Test responsiveness at all breakpoints
3. Include meta tags and SEO basics
4. Add form validation if forms exist
5. Ensure accessibility (keyboard navigation, screen readers)
6. Provide deployment instructions
