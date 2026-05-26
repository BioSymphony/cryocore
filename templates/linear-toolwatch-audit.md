# Toolwatch Audit

## Summary

- Tool IDs:
- Lane:
- Current registry status:
- Proposed status:

## Primary Sources Checked

- Upstream repo:
- Docs:
- Release/version page:
- Paper or preprint:
- License or terms:

## Findings

- Current version or commit:
- Release date:
- License delta:
- Runtime gate:
- Image family:
- Smoke command:
- Expected artifacts:
- Affected lane modules:

## Acceptance

- `references/software-registry.yaml` updated or explicitly left unchanged.
- `docs/tooling-and-licensing.md` updated when durable policy changed.
- No secrets, license files, gated installers, model weights, raw maps, or raw movies committed.
- Stale or ambiguous entries marked `planned`, `gated`, `watch`, or `blocked` honestly.

## Validation

```bash
make preflight
make registry-check
make module-check
```
