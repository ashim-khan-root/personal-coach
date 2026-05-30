import { describe, it } from 'node:test'
import assert from 'node:assert'
import { validateListing } from './validate-listing.js'

describe('validateListing', () => {
  it('returns error if name is missing', () => {
    const result = validateListing({ category: 'Security' })
    assert.equal(result.valid, false)
    assert.ok(result.errors.some(e => e.includes('name')))
  })

  it('returns error if category is missing', () => {
    const result = validateListing({ name: 'Test Co' })
    assert.equal(result.valid, false)
    assert.ok(result.errors.some(e => e.includes('category')))
  })
})
