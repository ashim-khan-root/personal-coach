# XSS Prevention Reference

## Output Encoding Rules

Apply context-appropriate encoding for all untrusted data:

| Context | Encoding Method | Example |
|---------|----------------|---------|
| HTML Body | HTML Entity Encoding | `&lt;script&gt;` |
| HTML Attribute | Attribute Encoding | `&quot;` |
| JavaScript String | Unicode Escape | `\x3cscript\x3e` |
| CSS | CSS Encoding | `\3c script\3e` |
| URL Parameter | URL Encoding | `%3Cscript%3E` |

## Unsafe vs Safe Sinks

### Unsafe — NEVER with untrusted data

```javascript
element.innerHTML = userInput;
element.outerHTML = userInput;
document.write(userInput);
elem.insertAdjacentHTML('beforeend', userInput);
eval(userInput);
new Function(userInput);
setTimeout(userInput, 100);  // string form
location.href = userInput;
location.assign(userInput);
window.open(userInput);
```

### Safe alternatives

```javascript
element.textContent = userInput;
element.setAttribute('title', userInput); // non-event attributes only
element.classList.add(userInput);          // sanitized by browser
```

## HTML Sanitization (when HTML is necessary)

```javascript
import DOMPurify from 'dompurify';

// Basic
element.innerHTML = DOMPurify.sanitize(dirty);

// With config
const clean = DOMPurify.sanitize(dirty, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
  ALLOWED_ATTR: ['href', 'title']
});

// Sanitizer API (modern browsers)
const sanitizer = new Sanitizer({
  allowElements: ['b', 'i', 'a'],
  allowAttributes: { 'href': ['a'] }
});
element.setHTML(userInput, { sanitizer });
```

## URL Validation

```javascript
function isValidUrl(input) {
  try {
    const url = new URL(input);
    return ['http:', 'https:'].includes(url.protocol);
  } catch {
    return false;
  }
}

function sanitizeHref(input) {
  if (!input) return '#';
  const trimmed = input.trim().toLowerCase();
  if (trimmed.startsWith('javascript:') || trimmed.startsWith('data:') || trimmed.startsWith('vbscript:')) return '#';
  return input;
}
```
