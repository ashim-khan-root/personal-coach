export function validateListing(listing) {
  const errors = []
  if (!listing.name) {
    errors.push('name is required')
  }
  if (!listing.category) {
    errors.push('category is required')
  }
  return errors.length > 0
    ? { valid: false, errors }
    : { valid: true }
}
