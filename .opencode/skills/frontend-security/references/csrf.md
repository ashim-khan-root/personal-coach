# CSRF Protection Reference

## Cookie-Based (SameSite)

The simplest defense — set `SameSite=Strict` or `SameSite=Lax` on session cookies.

```javascript
res.setHeader('Set-Cookie', `session=${token}; HttpOnly; Secure; SameSite=Strict`);
```

- `Strict` — cookie not sent on any cross-site request
- `Lax` — cookie sent on top-level navigations with safe methods (GET)

## Token-Based

Include a non-guessable token in state-changing requests.

```javascript
// Server embeds CSRF token in page or response header
const csrfToken = document.querySelector('meta[name=csrf-token]').content;

// Include in fetch
fetch('/api/delete', {
  method: 'POST',
  headers: { 'X-CSRF-Token': csrfToken }
});

// Include in form
<form method="POST" action="/delete">
  <input type="hidden" name="_csrf" value="{{csrfToken}}">
</form>
```

## Framework Integrations

- **Angular**: Built-in `HttpClientXsrfModule` intercepts X-XSRF-TOKEN
- **Next.js**: Server Actions include CSRF protection by default (Origin/Referer check)
- **Express**: `csurf` or `csrf-csrf` middleware
- **Django**: `{% csrf_token %}` in templates by default
- **Rails**: `authenticity_token` in forms by default
