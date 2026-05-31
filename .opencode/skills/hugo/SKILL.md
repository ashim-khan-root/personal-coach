---
name: hugo
description: When the user wants to build, customize, or deploy a Hugo static site. Also use when the user mentions "Hugo," "Hugo site," "Hugo theme," "Hugo templates," "Hugo layouts," "Hugo shortcodes," "Hugo config," "hugo.toml," "hugo.yaml," "config.toml," "content directory," "archetypes," "static site generator," "Hugo deployment," "GitHub Pages Hugo," "Netlify Hugo," "Hugo modules," "Hugo pipes," "Hugo data," "Hugo menus," "Hugo taxonomies," or "Hugo blog." Use this whenever someone is working with the Hugo static site generator. For WordPress, see wordpress. For plain HTML/CSS/JS, see web-development.
metadata:
  version: 1.0.0
---

# Hugo Development

You are an expert Hugo static site developer. Your goal is to build, customize, and deploy Hugo sites with clean templates, proper content structure, and optimized performance.

## Before Starting

Gather this context (ask if not provided):

### 1. Site Purpose
- What type of site? (blog, business, portfolio, documentation, landing page)
- How many content sections?
- Any existing content to migrate?

### 2. Current State
- New Hugo site or existing project?
- Hugo version installed?
- Which theme? (if any)
- Deployment target? (GitHub Pages, Netlify, Vercel, Cloudflare Pages)

### 3. Requirements
- Custom layouts needed?
- Menu structure?
- Taxonomies? (tags, categories)
- Multi-language?
- Forms or interactive elements?

---

## Hugo Project Structure

```
site/
├── archetypes/
│   └── default.md          # Front matter template
├── content/
│   ├── _index.md           # Homepage content
│   ├── blog/
│   │   ├── _index.md       # Blog section page
│   │   └── post-1.md       # Individual post
│   └── products/
│       ├── _index.md
│       └── product-1.md
├── data/                    # Data files (YAML, JSON, TOML)
├── i18n/                    # Translations
├── layouts/
│   ├── _default/
│   │   ├── baseof.html      # Base template
│   │   ├── list.html        # Section/list pages
│   │   └── single.html      # Single content pages
│   ├── partials/
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── head.html
│   ├── shortcodes/          # Custom shortcodes
│   └── index.html           # Homepage template
├── static/
│   ├── images/
│   ├── css/
│   └── js/
├── themes/                  # Installed themes
├── config.toml              # Site configuration
└── hugo.toml                # Alternative config filename
```

---

## Configuration

### config.toml Template
```toml
baseURL = "https://yoursite.com/"
languageCode = "en-us"
title = "Your Site Title"
theme = "your-theme"

[params]
  description = "Site description for SEO"
  author = "Your Name"
  dateFormat = "Jan 2, 2006"
  showReadingTime = true

[menu]
  [[menu.main]]
    name = "Home"
    url = "/"
    weight = 1
  [[menu.main]]
    name = "Blog"
    url = "/blog/"
    weight = 2
  [[menu.main]]
    name = "About"
    url = "/about/"
    weight = 3
  [[menu.main]]
    name = "Contact"
    url = "/contact/"
    weight = 4

[taxonomies]
  tag = "tags"
  category = "categories"

[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true  # Allow HTML in markdown

[outputs]
  home = ["HTML", "RSS", "JSON"]
```

---

## Content Format

### Front Matter (YAML)
```yaml
---
title: "Post Title"
date: 2026-05-31
draft: false
description: "Meta description for SEO"
categories: ["SEO"]
tags: ["wordpress", "optimization"]
slug: "custom-url-slug"
image: "/images/featured-image.jpg"
---
```

### Front Matter (TOML)
```toml
+++
title = "Post Title"
date = 2026-05-31
draft = false
description = "Meta description for SEO"
categories = ["SEO"]
tags = ["wordpress", "optimization"]
+++
```

---

## Templates

### baseof.html
```html
<!DOCTYPE html>
<html lang="{{ .Site.LanguageCode }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ if .IsHome }}{{ .Site.Title }}{{ else }}{{ .Title }} | {{ .Site.Title }}{{ end }}</title>
    <meta name="description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Site.Params.description }}{{ end }}">
    <link rel="stylesheet" href="{{ "css/style.css" | absURL }}">
</head>
<body>
    {{ partial "header.html" . }}
    <main>
        {{ block "main" . }}{{ end }}
    </main>
    {{ partial "footer.html" . }}
    <script src="{{ "js/main.js" | absURL }}"></script>
</body>
</html>
```

### single.html
```html
{{ define "main" }}
<article class="post">
    <header>
        <h1>{{ .Title }}</h1>
        <time>{{ .Date.Format .Site.Params.dateFormat }}</time>
    </header>
    <div class="content">
        {{ .Content }}
    </div>
    {{ if .Params.tags }}
    <footer class="tags">
        {{ range .Params.tags }}
        <a href="{{ "tags/" | absURL }}{{ . | urlize }}">#{{ . }}</a>
        {{ end }}
    </footer>
    {{ end }}
</article>
{{ end }}
```

### list.html
```html
{{ define "main" }}
<section class="post-list">
    <h1>{{ .Title }}</h1>
    {{ range .Pages }}
    <article>
        <h2><a href="{{ .RelPermalink }}">{{ .Title }}</a></h2>
        <time>{{ .Date.Format .Site.Params.dateFormat }}</time>
        <p>{{ .Description }}</p>
    </article>
    {{ end }}
</section>
{{ end }}
```

---

## Shortcodes

### Image with Caption
```html
<!-- layouts/shortcodes/figure.html -->
<figure>
    <img src="{{ .Get "src" }}" alt="{{ .Get "alt" }}" loading="lazy">
    {{ with .Get "caption" }}<figcaption>{{ . }}</figcaption>{{ end }}
</figure>
```
Usage: `{{</* figure src="/images/photo.jpg" alt="Description" caption="Photo caption" */>}}`

### YouTube Embed
```html
<!-- layouts/shortcodes/youtube.html -->
<div class="video-wrapper">
    <iframe src="https://www.youtube.com/embed/{{ .Get "id" }}" 
            frameborder="0" 
            allowfullscreen
            loading="lazy"></iframe>
</div>
```

### Callout Box
```html
<!-- layouts/shortcodes/callout.html -->
<div class="callout callout-{{ .Get "type" | default "info" }}">
    {{ .Inner }}
</div>
```

---

## Menu System

### In config.toml
```toml
[menu]
  [[menu.main]]
    name = "Products"
    url = "/products/"
    weight = 1
  [[menu.main]]
    name = "Services"
    url = "/services/"
    weight = 2
    [[menu.main]]
      name = "SEO"
      parent = "Services"
      url = "/services/seo/"
      weight = 1
```

### In Template
```html
<nav>
    <ul>
        {{ range .Site.Menus.main }}
        <li>
            <a href="{{ .URL }}">{{ .Name }}</a>
            {{ if .HasChildren }}
            <ul>
                {{ range .Children }}
                <li><a href="{{ .URL }}">{{ .Name }}</a></li>
                {{ end }}
            </ul>
            {{ end }}
        </li>
        {{ end }}
    </ul>
</nav>
```

---

## Deployment

### GitHub Pages
```yaml
# .github/workflows/hugo.yml
name: Deploy Hugo
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
      - run: hugo --minify
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

### Netlify
```toml
# netlify.toml
[build]
  command = "hugo --minify"
  publish = "public"

[build.environment]
  HUGO_VERSION = "0.128.0"
```

### Cloudflare Pages
```bash
# Build command
hugo --minify
# Output directory
public
```

---

## Hugo Commands

```bash
# Create new site
hugo new site mysite

# Create new content
hugo new content/blog/my-post.md

# Create new page
hugo new content/about.md

# Start dev server
hugo server -D          # Include drafts
hugo server --bind 0.0.0.0  # Access from network

# Build for production
hugo --minify

# Update theme
git submodule update --remote
```

---

## Common Patterns

### Recent Posts on Homepage
```html
{{ range first 5 (where .Site.RegularPages "Section" "blog") }}
<article>
    <h3><a href="{{ .RelPermalink }}">{{ .Title }}</a></h3>
    <time>{{ .Date.Format "Jan 2, 2006" }}</time>
</article>
{{ end }}
```

### Section Pages
```html
{{ range .Site.Sections }}
<a href="{{ .RelPermalink }}">{{ .Title }}</a>
{{ end }}
```

### Breadcrumbs
```html
<nav class="breadcrumb">
    <a href="/">Home</a>
    {{ range .Ancestors.Reverse }}
    <a href="{{ .RelPermalink }}">{{ .Title }}</a>
    {{ end }}
    <span>{{ .Title }}</span>
</nav>
```

---

## Output

When working on Hugo:
1. Provide complete file contents (not snippets)
2. Specify exact file paths
3. Include config changes
4. Test with `hugo server -D` before deployment
5. Minify for production: `hugo --minify`
