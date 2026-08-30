# Recipe: Map/Model Review

Build a claim-bounded map/model review for a public EMDB and PDB pair. This
recipe uses the script from the
[Pol Theta demo](../../demos/poltheta-map-model-dossier/) and produces the same
artifact set.

## When to use it

- Your agent needs to review a deposited cryo-EM map+model pair.
- A reviewer wants the inputs, methods, figures, density support, validation summary, and claim boundaries in one bundle.
- A campaign needs a review-shape reference before scaling to a paid provider run.

## Inputs

- A public EMDB ID, for example `EMD-43816`.
- A public PDB ID, for example `9ASJ`.
- Optional deposited map and model artifacts fetched into ignored runtime storage.

## Commands

The command below downloads a deposited EMDB map, PDB coordinates, and
validation reports into ignored runtime storage. Run it only under an
explicitly authorized issue scope. Use the preparation check when you need
only the contract shape.

```bash
python3 scripts/cryocore/poltheta_map_model_dossier.py \
  --out .runtime/poltheta-map-model-local/runpod-execution \
  --json
```

For a different deposit, use the applicable map-and-model review builder. The
artifact contract in
[modules/artifact-contracts/structure-dossier.v1.json](../../modules/artifact-contracts/structure-dossier.v1.json)
applies.

## Files Produced

- `artifacts/report.md`: human-readable review.
- `artifacts/report.html`: HTML review with embedded figures.
- `artifacts/claim_ledger.md`: claim boundaries and caveats.
- `artifacts/provenance.md`: input audit, methods, and pointers to source accessions.
- `artifacts/figures/*.svg`: SVG figures rendered from the map and model.
- `artifacts/validation/map_model_fit.json`: machine-readable map and model fit metrics.

## Claim Ceiling

Start at `processed` or `candidate`. Increase the ceiling only when expert
review and stronger validation artifacts support a higher level. These
artifacts can include wwPDB validation outputs, density-support checks, and
cross-correlation results.

## Validation

```bash
make schema-check
make figure-manifest-check
make contract-self-check
make release-check
```

## Failure Handling

When a deposited artifact fetch fails, close as `blocked` or `partial` and
record which inputs were missing. The claim ledger stays at the lowest level
the available evidence supports.

## Related

- [Pol Theta Walkthrough](../missions/pol-theta-walkthrough.md): narrative end-to-end mission using this recipe.
- [Figure Dossier](figure-dossier.md): companion recipe for figure-only review outputs.
- [Map and Model Review skill](../../skills/cryocore-map-model-dossier/SKILL.md): the skill an agent loads to run this recipe.
