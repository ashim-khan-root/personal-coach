# npm / Dependency Security Reference

## Audit Commands

```bash
# Full audit
npm audit

# JSON output for CI
npm audit --json

# Fix auto-fixable
npm audit fix

# Force fix (may break SemVer)
npm audit fix --force

# Check for outdated
npm outdated
```

## Supply Chain Risks

| Risk | Mitigation |
|------|------------|
| Malicious package | Check downloads, last publish date, maintainer reputation |
| Typosquatting | Double-check package names, use `npm owner ls <pkg>` |
| Compromised maintainer | Pin exact versions, use lockfiles, audit diffs |
| Unmaintained dep | Use `npm view <pkg> time` to check freshness |

## Best Practices

- Commit `package-lock.json` / `yarn.lock`
- Enable Dependabot or Renovate for automated updates
- Run `npm audit` in CI pipeline
- Use `--ignore-scripts` for installs in CI (`npm ci --ignore-scripts`)
- Review major version bumps for breaking security changes
- Use `npm dedupe` to flatten duplicate deps
- Consider `socket.dev` or `snyk` for deeper vulnerability scanning
