# Framework-Specific Security Patterns

## React / Next.js

```jsx
// SAFE — auto-escaped by React
<div>{userInput}</div>

// DANGEROUS — bypasses React escaping
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// SAFE — URL validation for href
const url = userInput.startsWith('https://') ? userInput : '#';
<a href={url}>Link</a>

// SAFE — server action with CSRF (Next.js)
async function deleteUser(formData) {
  'use server';
  // Next.js validates Origin/Referer automatically
}
```

## Vue

```vue
<!-- SAFE — auto-escaped -->
<div>{{ userInput }}</div>

<!-- DANGEROUS — bypasses escaping -->
<div v-html="userInput"></div>

<!-- SAFE — URL validation -->
<a :href="sanitizeUrl(userInput)">Link</a>
```

## Angular

```typescript
// SAFE — auto-sanitized by DomSanitizer
<div>{{ userInput }}</div>

// DANGEROUS — bypasses sanitization
<div [innerHTML]="sanitizer.bypassSecurityTrustHtml(userInput)"></div>

// SAFE — DomSanitizer methods
sanitizer.sanitize(SecurityContext.HTML, userInput);
sanitizer.sanitize(SecurityContext.URL, userInput);
```

## Astro

```astro
<!-- SAFE — auto-escaped in templates -->
<div>{userInput}</div>

<!-- DANGEROUS — set:html bypasses escaping -->
<div set:html={userInput} />
```

## Key Rule

Never use `dangerouslySetInnerHTML`, `v-html`, `bypassSecurityTrust*`, or `set:html` with any value that contains user-controlled data.
