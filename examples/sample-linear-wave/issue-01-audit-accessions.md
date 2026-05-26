# Audit public accessions for Pol Theta map+model lane

## Summary

Confirm that EMDB `EMD-43816` and PDB `9ASJ` are fetchable from public APIs,
record their current metadata, and produce a structured input audit the next
issue can consume.

## Required Fields

- subgroup: `cryocore`
- campaign ID: `cryocore-poltheta-map-model-dossier-w1`
- routing label: `sym:cryocore`
- provider: `local`
- execution profile: `local-cpu-no-gpu`
- operator gate required: `no`
- exact inputs: EMDB `EMD-43816`, PDB `9ASJ`.
- expected artifacts: `.runtime/public-accession-metadata.json`, audit report appended to the issue.
- owned paths: `.runtime/public-accession-metadata.json`.
- dependencies: none.
- license and capability caveats: none. Public accession metadata only.
- risk notes: API throttling. Retry once before reporting blockers.

## Acceptance Criteria

- [ ] Declared inputs are audited before execution.
- [ ] Required artifacts are produced and hashed.
- [ ] Validation outputs join back to declared inputs.
- [ ] Claim level is stated explicitly.
- [ ] Any partial, degraded, blocked, or failed outcome is recorded honestly.

## Validation Commands

```bash
python3 scripts/cryocore/preflight.py --repo-root . --json
python3 scripts/cryocore/fetch_public_accession_metadata.py \
  --emdb EMD-43816 --pdb 9ASJ \
  --out .runtime/public-accession-metadata.json
python3 -m json.tool .runtime/public-accession-metadata.json
```

## Touched Areas

- `.runtime/public-accession-metadata.json` (gitignored)

## Dependencies

- None.

<!-- symphony:schema -->
```yaml
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
claim_level: candidate
```
