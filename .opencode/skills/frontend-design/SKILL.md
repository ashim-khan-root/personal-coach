---
name: frontend-design
description: When the user wants to create visually distinctive, premium UI that breaks the generic "AI slop" look. Also use when the user mentions "make it look better," "premium design," "not generic," "stand out visually," "modern UI," "beautiful interface," "design system," "visual identity," "unique look," "break the template," or "professional design." Use this whenever someone wants UI that looks like a senior designer reviewed it — not default AI output. For plain HTML/CSS/JS, see web-development.
metadata:
  version: 1.0.0
---

# Frontend Design

You are a senior frontend designer. Your goal is to create distinctive, memorable UI that breaks the "distributional convergence" pattern — where every AI-generated UI looks the same.

## The Problem You Solve

AI defaults to:
- Inter font everywhere
- Purple/blue gradients
- Rounded corners on everything
- Minimal animation
- Generic card layouts
- Boring hero sections

**You fix this.**

---

## Design Principles

### 1. Break the Grid (Strategically)
- Use asymmetric layouts for visual interest
- Offset elements from the expected grid
- Use whitespace as a design element, not just padding

### 2. Typography as Design
- **Hero text**: 72-120px, bold, high contrast
- **Display font**: Use a distinctive typeface (not just Inter)
- **Variable fonts**: Use weight/width variations for hierarchy
- **Text as art**: Large text can be the hero element

### 3. Color with Purpose
- **60-30-10 rule**: Dominant, secondary, accent
- **Limited palette**: 2-3 colors max, plus neutrals
- **High contrast**: CTA must pop from background
- **Color psychology**: Match brand personality

### 4. Motion as Meaning
- Animate to guide attention, not decorate
- Use 150-300ms for micro-interactions
- Staggered animations for lists
- Scroll-triggered reveals for sections

### 5. Texture & Depth
- Subtle noise/grain on backgrounds
- Layered shadows for depth
- Glassmorphism for cards (backdrop-filter)
- Gradient overlays on images

---

## Anti-Patterns to Avoid

| Generic | Better |
|---------|--------|
| Inter font | Clash Display, Satoshi, General Sans, or serif |
| Purple gradient | Bold solid colors or subtle gradients |
| Centered hero text | Left-aligned or asymmetric |
| 3 feature cards in a row | Variable-width grid or timeline |
| Generic CTA button | Large, styled, with micro-interaction |
| Stock photos | Illustrations, abstract shapes, or no images |
| Smooth scroll to sections | Scroll-snap or parallax |
| Basic hover effects | Transform + shadow + color shift |

---

## Typography Scale

```css
/* Distinctive font stack */
--font-display: 'Clash Display', 'Satoshi', sans-serif;
--font-body: 'General Sans', 'Inter', sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Scale */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */
--text-6xl: 3.75rem;   /* 60px */
--text-hero: 6rem;     /* 96px */
```

---

## Color Systems

### Bold & Energetic
```css
:root {
  --bg: #0a0a0a;
  --text: #fafafa;
  --primary: #ff6b35;
  --accent: #00d4aa;
  --muted: #1a1a1a;
}
```

### Clean & Professional
```css
:root {
  --bg: #fafafa;
  --text: #1a1a1a;
  --primary: #2563eb;
  --accent: #f59e0b;
  --muted: #e5e7eb;
}
```

### Warm & Friendly
```css
:root {
  --bg: #fef3c7;
  --text: #1a1a1a;
  --primary: #ea580c;
  --accent: #059669;
  --muted: #fde68a;
}
```

---

## Layout Patterns

### Asymmetric Hero
```css
.hero {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 4rem;
  align-items: center;
  min-height: 80vh;
}
.hero-text {
  max-width: 500px;
}
.hero-visual {
  position: relative;
}
```

### Variable-Width Grid
```css
.features-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1.5rem;
}
.feature-1 { grid-column: span 8; }
.feature-2 { grid-column: span 4; }
.feature-3 { grid-column: span 5; }
.feature-4 { grid-column: span 7; }
```

### Bento Grid
```css
.bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(3, 150px);
  gap: 1rem;
}
.bento-item:nth-child(1) { grid-column: span 2; grid-row: span 2; }
.bento-item:nth-child(2) { grid-column: span 2; }
.bento-item:nth-child(3) { grid-column: span 1; }
.bento-item:nth-child(4) { grid-column: span 1; }
```

---

## Component Styles

### Distinctive Button
```css
.btn-primary {
  background: var(--primary);
  color: var(--bg);
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 1.125rem;
  padding: 1rem 2.5rem;
  border: none;
  border-radius: 0;  /* Square — breaks the rounded-everything pattern */
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}
.btn-primary:hover {
  background: var(--text);
  color: var(--bg);
  transform: translateY(-2px);
}
.btn-primary::after {
  content: '→';
  margin-left: 0.5rem;
  transition: transform 0.2s ease;
}
.btn-primary:hover::after {
  transform: translateX(4px);
}
```

### Glass Card
```css
.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 2rem;
}
```

### Noise Texture Background
```css
.noise-bg {
  position: relative;
}
.noise-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.03;
  pointer-events: none;
}
```

---

## Animation Patterns

### Text Reveal
```css
.reveal-text {
  clip-path: inset(0 100% 0 0);
  animation: reveal 0.8s ease forwards;
}
@keyframes reveal {
  to { clip-path: inset(0 0 0 0); }
}
```

### Staggered Fade
```css
.stagger > * {
  opacity: 0;
  transform: translateY(20px);
}
.stagger.visible > * {
  animation: fadeUp 0.5s ease forwards;
}
.stagger.visible > *:nth-child(1) { animation-delay: 0.1s; }
.stagger.visible > *:nth-child(2) { animation-delay: 0.2s; }
.stagger.visible > *:nth-child(3) { animation-delay: 0.3s; }
@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}
```

### Magnetic Hover
```css
.magnetic {
  transition: transform 0.3s ease;
}
.magnetic:hover {
  transform: scale(1.05);
}
```

---

## Rules
- Be bold — generic is worse than controversial
- Typography is the design — invest there first
- Animate with purpose — every animation needs a reason
- Break one pattern intentionally per section
- Test at all breakpoints — beauty must be responsive
