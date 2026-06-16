---
name: frontend-security
description: Audit frontend codebases for web security vulnerabilities — XSS, CSP, CSRF, DOM injection, file upload, input validation, dependency security, and framework-specific risks (React, Vue, Angular, Astro, vanilla JS). Based on OWASP guidelines. Use when reviewing frontend code, adding security headers, handling user input in the browser, or auditing client-side security posture.
---

# Frontend Security

You are a frontend security expert. Your goal is to identify, explain, and fix client-side security vulnerabilities.

## Audit Methodology

1. **Grep for dangerous patterns** — innerHTML, eval, dangerouslySetInnerHTML, document.write, raw filters
2. **Review headers** — CSP, X-Frame-Options, X-Content-Type-Options, Permissions-Policy
3. **Check input handling** — validation, sanitization, output encoding context
4. **Audit dependencies** — npm audit, known CVEs, supply chain risk
5. **Verify framework patterns** — React escaping bypasses, Vue v-html, Angular bypassSecurityTrust, Astro {untrusted}

---

## 1. Cross-Site Scripting (XSS)

### Unsafe Sinks — NEVER use with untrusted data

```javascript
element.innerHTML = userInput;
document.write(userInput);
eval(userInput);
new Function(userInput);
location.href = userInput;
```

### Safe Alternatives

```javascript
element.textContent = userInput;
element.setAttribute('title', userInput);
```

### Output Encoding by Context

| Context | Encoding | Example |
|---------|----------|---------|
| HTML body | HTML entities | `&lt;script&gt;` |
| HTML attribute | Attribute encode | `&quot;` |
| JavaScript string | Unicode escape | `\x3cscript\x3e` |
| URL param | URL encode | `%3Cscript%3E` |

### HTML Sanitization (when HTML is required)

```javascript
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
  ALLOWED_ATTR: ['href']
});
```

---

## 2. Content Security Policy (CSP)

### Strict CSP (Recommended)

```http
Content-Security-Policy:
  default-src 'self';
  script-src 'nonce-{random}' 'strict-dynamic';
  object-src 'none';
  base-uri 'none';
  form-action 'self';
  frame-ancestors 'none';
```

### Nonce Generation

```javascript
const nonce = crypto.randomBytes(16).toString('base64');
res.setHeader('Content-Security-Policy',
  `script-src 'nonce-${nonce}' 'strict-dynamic'; object-src 'none'; base-uri 'none'`
);
```

### Report-Only Mode for Testing

```http
Content-Security-Policy-Report-Only:
  default-src 'self';
  report-uri /csp-report;
```

### Security Headers Companion

```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

---

## 3. DOM Security

### DOM Clobbering

```html
<!-- DANGEROUS: attacker injects element with id="config" -->
<form id="config"></form>
<script>
  if (config.apiKey)  // DOM clobbered — returns form element
</script>
```

**Mitigation**: Use `typeof` checks, `hasOwnProperty`, or isolate trusted globals in a separate namespace.

### Prototype Pollution

```javascript
// DANGEROUS: merging user-controlled objects recursively
function merge(target, source) {
  for (let key in source) {
    if (key === '__proto__' || key === 'constructor') continue;
    target[key] = source[key];
  }
}
```

**Mitigation**: Use `Object.create(null)` for maps, freeze prototypes with `Object.freeze(Object.prototype)`.

### PostMessage Security

```javascript
// SAFE: validate origin and data
window.addEventListener('message', (event) => {
  if (event.origin !== 'https://trusted-site.com') return;
  if (typeof event.data !== 'string') return;
  // process
});
```

---

## 4. CSRF Protection

### Cookie-Based (SameSite)

```javascript
// Set cookies with SameSite=Strict or SameSite=Lax
res.setHeader('Set-Cookie', `session=${token}; HttpOnly; Secure; SameSite=Strict`);
```

### Token-Based (API)

```javascript
// Include anti-CSRF token in state-changing requests
fetch('/api/delete', {
  method: 'POST',
  headers: { 'X-CSRF-Token': csrfToken }
});
```

### Framework-Provided

- React/Next.js: CSRF tokens for form actions via server actions
- Angular: HttpClientXsrfModule built-in
- Django/Express: csurf or similar middleware

---

## 5. Input Validation

### Client-Side Validation (UX + First Line)

```javascript
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function sanitizeFilename(name) {
  return name.replace(/[^a-zA-Z0-9._-]/g, '');
}
```

**Important**: Client validation is UX only. Server must re-validate everything.

### URL Validation

```javascript
function isValidHref(input) {
  try {
    const url = new URL(input, window.location.origin);
    return ['http:', 'https:'].includes(url.protocol);
  } catch {
    return false;
  }
}
```

---

## 6. File Upload Security

```javascript
function validateFileUpload(file) {
  const maxSize = 5 * 1024 * 1024;
  if (file.size > maxSize) throw new Error('File too large');

  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (!allowedTypes.includes(file.type)) throw new Error('Invalid type');

  // Validate extension matches MIME
  const ext = file.name.split('.').pop().toLowerCase();
  const mimeMap = { jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', webp: 'image/webp' };
  if (mimeMap[ext] !== file.type) throw new Error('Extension/MIME mismatch');

  return true;
}
```

---

## 7. Framework-Specific Risks

### React / Next.js

```jsx
// DANGEROUS: bypasses React's auto-escaping
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// SAFE: React escapes by default
<div>{userInput}</div>

// DANGEROUS: javascript: in href
<a href={userInput}>Link</a>
```

### Vue

```vue
<!-- DANGEROUS: bypasses Vue escaping -->
<div v-html="userInput"></div>

<!-- SAFE: Vue auto-escapes -->
<div>{{ userInput }}</div>
```

### Angular

```typescript
// DANGEROUS: bypasses Angular sanitization
this.sanitizer.bypassSecurityTrustHtml(userInput)

// SAFE: Angular sanitizes by default
<div>{{ userInput }}</div>
```

### Astro

```astro
<!-- DANGEROUS: raw HTML interpolation -->
{userInput}

<!-- SAFE: auto-escaped by default -->
{userInput}
```

---

## 8. Dependency Security

```bash
# Audit current project
npm audit

# Fix auto-fixable issues
npm audit fix

# Check for outdated packages
npm outdated

# View specific advisory
npm audit --json | jq '.advisories'
```

### Best Practices

- Commit `package-lock.json` / `yarn.lock`
- Enable Dependabot or Renovate
- Run `npm audit` in CI
- Avoid packages with no maintenance (check last publish date, open issues)
- Pin exact versions for build reproducibility

---

## 9. Pre-Deployment Checklist

- [ ] No `innerHTML`, `document.write`, `eval`, `dangerouslySetInnerHTML`, `v-html` on untrusted data
- [ ] CSP headers configured (strict mode preferred)
- [ ] `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY` set
- [ ] All user inputs validated (client + server)
- [ ] File uploads restricted by size, type, extension
- [ ] PostMessage origin validated
- [ ] CSRF protection on state-changing requests
- [ ] `npm audit` shows no high/critical vulnerabilities
- [ ] No secrets in client-side code or `.env` exposed to browser
- [ ] Third-party scripts loaded with `integrity` attribute (SRI)

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP XSS Prevention Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP CSP Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [MDN Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [DOM Clobbering (OWASP)](https://owasp.org/www-community/attacks/DOM_Clobbering)
