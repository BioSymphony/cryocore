# Prep RunPod manifest for Pol Theta dossier

## Summary

Validate `runpod/bridge-manifests/poltheta-map-model-dossier.json` against the
RunPod scope and reference checks. Confirm the manifest is publishable and
covers the bridge entrypoint that the Pol Theta demo expects.

## Required Fields

- subgroup: `cryocore`
- campaign ID: `cryocore-poltheta-map-model-dossier-w1`
- routing label: `sym:cryocore`
- provider: `provider-neutral`
- execution profile: `local-cpu-no-gpu`
- operator gate required: `no`
- exact inputs: `runpod/bridge-manifests/poltheta-map-model-dossier.json`.
- expected artifacts: updated bridge manifest if the scope or reference checks flag drift, otherwise a no-change confirmation appended to the issue.
- owned paths: `runpod/bridge-manifests/poltheta-map-model-dossier.json`.
- dependencies: issue `CRYOCORE-W1-01` (the audit names the accessions this manifest references).
- license and capability caveats: prep mode only. A paid RunPod launch is operator-owned and belongs in a later wave.
- risk notes: a scope drift would block the prep check until the manifest is corrected.

## Acceptance Criteria

- [ ] Declared inputs are audited before execution.
- [ ] Required artifacts are produced, fetched when remote, and hashed.
- [ ] Validation outputs join back to declared inputs.
- [ ] Claim level is stated explicitly.
- [ ] Any partial, degraded, blocked, or failed outcome is recorded honestly.

## Validation Commands

```bash
python3 scripts/cryocore/preflight.py --repo-root . --json
make runpod-scope-check
make runpod-reference-check
make bridge-manifest-check
```

## Touched Areas

- `runpod/bridge-manifests/poltheta-map-model-dossier.json` (only if drift is found)

## Dependencies

- `CRYOCORE-W1-01`

<!-- symphony:schema -->
```yaml
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
claim_level: candidate
```
