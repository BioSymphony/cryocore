# Demo Gallery

The public demos are intentionally small and claim-bounded.

![T2R14 demo preview](assets/demo-gallery/t2r14-preview.svg)

## T2R14 Open Dossier

- Maturity: local runnable.
- Input class: public PDB/RCSB coordinate metadata.
- Raw data: none.
- License-gated tools: none.
- Claim ceiling: processed, with mechanism claims downgraded unless separate
  evidence is added.
- Preview asset: `docs/assets/demo-gallery/t2r14-preview.svg`.
- Claim excerpt: `docs/assets/demo-gallery/t2r14-claim-excerpt.md`.

Local run:

```bash
python3 scripts/cryocore/t2r14_open_dossier.py --out .runtime/t2r14-open-dossier --json
```

Expected small outputs include `report.html`, `coordinate-summary.json`,
`ligand-neighborhoods.json`, `figures/*.svg`, `claim_ledger.md`, and an export
tarball that excludes the downloaded `data/` cache.

Static sample output shape: `examples/t2r14-open-dossier-preview/`.

## Pol Theta Map/Model Dossier

- Maturity: provider-gated demo shape with local prep checks.
- Input class: deposited public map/model accessions.
- Raw movies: none.
- License-gated tools: none for the default parser path.
- Claim ceiling: processed or candidate unless expert map/model review and
  validation artifacts are attached.

Prep check:

```bash
make demo-poltheta-prep-check
```

Expected remote artifacts include `report.html`, `report.md`,
`dossier_manifest.json`, `claim_ledger.md`, `validation/map_model_fit.json`,
`figures/*.svg`, and `runpod-execution.tar.gz`.

## Structure Jury Dual Dossier

- Maturity: provider-gated demo shape with local prep checks.
- Input class: two deposited public structures.
- Raw movies: none.
- License-gated tools: none for the default public route.
- Claim ceiling: comparative observation across the two deposits.

Prep check:

```bash
make demo-structure-jury-prep-check
```

Expected remote artifacts include target-level dossiers, a campaign summary,
combined `claim_ledger.md`, validation outputs, figures, and
`runpod-execution.tar.gz`.

Provider launch examples are preparation artifacts only. Real paid execution is
an operator-owned activity outside this public checkout.
