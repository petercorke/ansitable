# Publishing ansitable

## Automated Publishing via GitHub Actions (OIDC)

This project uses GitHub Actions with OIDC for secure, automated publishing to PyPI.

### Setup (One-time)

1. **On PyPI**: Configure Trusted Publishers
   - Go to PyPI → Account settings → Publishing
   - Add a new Trusted Publisher:
     - PyPI Project Name: `ansitable`
     - GitHub Repository Owner: `petercorke`
     - Repository Name: `ansitable`
     - Workflow Name: `release.yml`
     - Environment Name: `pypi`

2. **GitHub Actions**: Create environment (if not present)
   - Settings → Environments → Create environment `pypi`
   - (OIDC trust is configured above; no secrets needed)

### Publishing a Release

Once OIDC is configured, publishing is automatic:

```bash
# 1. Ensure all changes are committed and tests pass
git status
pytest

# 2. Update version in pyproject.toml (already at 1.0.0)
# Update CHANGELOG.md with release notes

# 3. Commit version bump
git add pyproject.toml CHANGELOG.md
git commit -m "chore: version X.Y.Z"

# 4. Create and push tag
git tag vX.Y.Z
git push
git push --tags
```

The `release.yml` workflow will:
- Trigger automatically on tag push
- Build sdist and wheel
- Publish to PyPI using OIDC (no API tokens)
- (Docs already auto-deploy via `master.yml`)

### Local Testing (Optional)

For local builds (e.g., emergency publishes):

```bash
# Build
make dist

# Upload (requires `~/.pypirc` with token or credentials)
make upload
```

### Troubleshooting

- **Workflow fails with "untrusted"**: Verify Trusted Publisher config on PyPI
- **Build errors**: Run `pytest` locally first
- **Check workflow status**: GitHub → Actions → `publish` workflow

### Security Notes

- No PyPI API tokens stored in GitHub secrets
- OIDC token is temporary and automatically rotated
- Only tags matching `v*` trigger publishing
- Environment `pypi` prevents accidental publishes
