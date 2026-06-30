---
name: cryocore-map-model-dossier
description: Use when building or reviewing public-safe EMDB/PDB map-model dossiers and CryoCore evidence bundles.
---

# CryoCore Map Model Dossier

Use this skill for public accession dossiers, map/model validation summaries,
claim ledgers, and Structure Factory handoff bundles.

## Read First

- `references/structure-dossier.v1.json`
- `references/artifact-contract.md`
- `references/validation-gates.md`
- `references/data-policy.md`

## Rules

- Inputs must be public accessions or secure local references.
- Do not commit maps, half-maps, masks, models, FASTA files, or private data.
- Record chain assignment assumptions, entity mapping, biological assembly
  assumptions, and unresolved density caveats.
- Distinguish deposited experimental evidence from prediction/design hypotheses.
- Every claim must point to evidence artifacts and a claim level.

## Outputs

Expected dossier outputs include manifest, methods, validation summary, figure
manifest, reproducible scene/script/session files, provenance, and claim ledger.
