# Input Validation Reference

## Client-Side Validation Patterns

```javascript
// Email
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// URL
function validateURL(url) {
  try {
    const u = new URL(url);
    return ['http:', 'https:'].includes(u.protocol);
  } catch { return false; }
}

// Phone (international flexible)
function validatePhone(phone) {
  return /^\+?[\d\s\-()]{7,20}$/.test(phone);
}

// Alphanumeric
function validateAlphaNumeric(input) {
  return /^[a-zA-Z0-9 _-]+$/.test(input);
}

// Integer within range
function validateInt(input, min, max) {
  const n = parseInt(input, 10);
  return !isNaN(n) && n >= min && n <= max;
}
```

## Whitelist Over Blacklist

Always validate against what's **allowed** (whitelist), not what's blocked.

```javascript
// GOOD: whitelist
const allowed = ['image/jpeg', 'image/png', 'image/webp'];
if (!allowed.includes(file.type)) reject();

// BAD: blacklist (can be bypassed)
const blocked = ['text/html', 'application/x-javascript'];
if (blocked.includes(file.type)) reject(); // new dangerous MIME type not in list
```

## Important

Client-side validation is for **user experience only**. All validation must be replicated server-side where the real security boundary lives.
