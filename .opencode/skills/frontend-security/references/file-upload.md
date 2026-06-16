# File Upload Security Reference

## Client-Side Validation

```javascript
function validateFile(file) {
  const errors = [];

  // Size
  const maxSize = 5 * 1024 * 1024;
  if (file.size > maxSize) errors.push('File exceeds 5MB limit');

  // MIME type
  const allowed = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'];
  if (!allowed.includes(file.type)) errors.push('File type not allowed');

  // Extension matches MIME
  const ext = file.name.split('.').pop().toLowerCase();
  const mimeMap = {
    jpg: 'image/jpeg', jpeg: 'image/jpeg',
    png: 'image/png', webp: 'image/webp', pdf: 'application/pdf'
  };
  if (mimeMap[ext] !== file.type) errors.push('Extension does not match file type');

  return { valid: errors.length === 0, errors };
}
```

## Server Validation (Required)

Client validation is UX only. Always re-validate server-side:

- Check MIME via `file --mime-type` or magic bytes
- Validate file extension against allowlist (not blocklist)
- Scan for malware if possible
- Store outside webroot or use hash-based filenames
- Serve with `Content-Disposition: attachment` to prevent script execution

## Security Rules

- Never trust `Content-Type` header from client
- Rename files on server (UUID/hash, not user-supplied name)
- Limit max file size at reverse proxy level
- Serve uploaded files from a separate domain/CDN
