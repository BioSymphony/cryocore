# Maintainers

BioSymphony CryoCore is maintained by the BioSymphony maintainers.

## Review Expectations

Security-sensitive changes require maintainer review:

- public release gates and secret/privacy scanners
- RunPod or provider-facing manifests and bridge manifests
- schemas and provider closeout contracts
- license/tool posture records
- CI, release, and GitHub workflow files
- public examples that mention accessions, claims, or generated artifacts

## Maintainer Checklist

Before public release or tag:

```bash
make clean
make release-check
python3 scripts/cryocore/public_release_report.py --repo-root . --json
python3 scripts/cryocore/public_release_report.py --repo-root . --publish-ready --expected-remote https://github.com/BioSymphony/biosymphony-cryocore-public.git --json
```

The `--publish-ready` check is expected to fail while this repo is still local
with no public remote, no initial commit, or no release tag.
