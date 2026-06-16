# DOM Security Reference

## DOM Clobbering

Attackers inject elements with `id` or `name` attributes that shadow global JS variables.

```html
<form id="config"></form>
<script>
  if (config.apiKey) { /* config is the form element, not an object */ }
</script>
```

### Mitigation

```javascript
// Check actual type
if (typeof config !== 'object' || !config || config instanceof HTMLElement) return;

// Use namespace isolation
const trusted = Object.freeze({ apiKey: process.env.API_KEY });
```

## Prototype Pollution

When merging untrusted objects recursively, `__proto__` can be polluted.

```javascript
// DANGEROUS merge
function merge(target, source) {
  for (let key in source) {
    if (typeof source[key] === 'object') {
      target[key] = merge(target[key] || {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}
```

### Mitigation

```javascript
// Safe: reject dangerous keys
function safeMerge(target, source) {
  for (let key in source) {
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') continue;
    target[key] = source[key];
  }
  return target;
}

// Or use Object.create(null) for map-like objects
const map = Object.create(null);
```

## PostMessage

```javascript
window.addEventListener('message', (event) => {
  if (event.origin !== 'https://trusted.com') return;
  if (typeof event.data !== 'object' || !event.data) return;
  process(event.data);
});
```

## Clickjacking

```http
X-Frame-Options: DENY
# or in CSP:
Content-Security-Policy: frame-ancestors 'none';
```
