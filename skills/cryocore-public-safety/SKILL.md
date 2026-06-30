---
name: cryocore-public-safety
description: Use when reviewing CryoCore changes for public release safety, privacy, secret leakage, provider-cost risk, heavy biological data, license posture, or unsupported scientific claims.
---

# CryoCore Public Safety

Use this skill before publishing, accepting PRs, or sharing generated outputs.

## Read First

- `PUBLIC_RELEASE.md`
- `SECURITY.md`
- `docs/data-policy.md`
- `docs/privacy-threat-model.md`
- `docs/public-repo-and-private-image-policy.md`
- `docs/claim-levels.md`

## Review Checklist

- No credentials, tokens, signed URLs, SSH keys, registry auth, or license files.
- No private paths, private clone instructions, private image namespaces, provider
  IDs, billing records, or raw provider logs.
- No raw movies, maps, half-maps, masks, particle stacks, private structures,
  unpublished sequences, model weights, or generated heavy outputs.
- No paid provider mutation or raw download is enabled by default.
- No `remote_launch_allowed: true` in public bridge manifests.
- Raw download contracts require explicit operator authorization at runtime.
- Claim ledgers downgrade unsupported mechanism, ligand, state, and biological
  claims.
- Public docs describe tool/license posture without redistributing gated tools.

## Commands

```bash
make public-release-report
make release-check
```

For targeted scans:

```bash
python3 scripts/cryocore/public_snapshot_check.py --repo-root <cryocore-repo> --profile public --json
python3 scripts/cryocore/public_release_report.py --repo-root <cryocore-repo> --json
```

When this skill is installed outside the CryoCore repo, resolve the bundled
`scripts/cryocore/*.py` paths relative to this skill folder and keep
`--repo-root` pointed at the CryoCore checkout being reviewed.

## Output

Return findings first, ordered by severity, with file paths and line numbers.
If there are no findings, say that and list residual risks such as unpinned
provider images or operator-owned launch gates.
