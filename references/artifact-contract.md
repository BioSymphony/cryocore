# CryoCore Artifact Contract

CryoCore runs must produce a reviewable dossier without relying on chat history, provider dashboards, or transient pod state.

## Required Files

```text
structure-dossier/
  dossier_manifest.json
  run_manifest.json
  data-intake-ledger.json
  provenance.md
  claim_ledger.md
  methods.md
  validation/input-audit.json
  validation/stage-contract-check.json
  validation/contract-self-check.json
  figures/README.md
```

No-download smoke runs may emit a smaller prep dossier:

```text
structure-dossier/
  run_manifest.json
  validation/input-audit.json
  validation/toolcheck.json
  validation/gpu.json
  validation/storage.json
  stage-progress.jsonl
  validation/stage-contract-check.json
  validation/contract-self-check.json
  provenance.md
```

## Manifest Requirements

Each dossier manifest records:

- campaign ID and run ID
- source accessions or secure local references
- declared execution profile and provider
- software versions and license posture
- GPU type and image digest for remote execution
- input artifact references and hashes where practical
- output artifact paths and hashes
- validation commands and status
- claim level and caveats

## Claim Ledger Requirements

Every density, model, ligand, state, resolution, map/model-fit, or biological-mechanism claim must include:

- claim text
- evidence artifact
- confidence level
- caveat
- reviewer or auditor status

Screenshots, provider status, and runner flags are not scientific evidence by themselves.
