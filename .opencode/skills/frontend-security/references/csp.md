# Content Security Policy Reference

## Strict CSP (Nonce-Based)

```http
Content-Security-Policy:
  default-src 'self';
  script-src 'nonce-{random}' 'strict-dynamic';
  object-src 'none';
  base-uri 'none';
  form-action 'self';
  frame-ancestors 'none';
```

## Directives Reference

| Directive | Purpose | Recommended |
|-----------|---------|-------------|
| `default-src` | Fallback for all directives | `'self'` |
| `script-src` | JavaScript sources | `'nonce-{r}' 'strict-dynamic'` |
| `style-src` | CSS sources | `'self' 'unsafe-inline'` |
| `img-src` | Images | `'self' data: https:` |
| `font-src` | Fonts | `'self'` |
| `connect-src` | Fetch, XHR, WS | `'self' https://api.example.com` |
| `frame-src` | iframes | `'none'` or specific origins |
| `frame-ancestors` | Who embeds this page | `'none'` |
| `object-src` | Plugins (Flash, etc.) | `'none'` |
| `base-uri` | Restrict `<base>` | `'none'` |
| `form-action` | Form submission targets | `'self'` |

## Report-Only Mode

```http
Content-Security-Policy-Report-Only:
  default-src 'self';
  report-uri /csp-report;
```

## Security Headers to Always Deploy

```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```
