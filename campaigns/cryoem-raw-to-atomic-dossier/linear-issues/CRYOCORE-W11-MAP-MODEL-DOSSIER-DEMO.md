## Summary

Run the practical map/model-only CryoCore demo using EMDB-43816 and PDB 9ASJ. This lane proves validation, figures, captions, provenance, and claim audit without raw movie downloads.

## Inputs

- `launch manifest` - `runpod/launch-manifests/map-model-dossier.json`
- `data module` - `modules/data-modules/emdb-43816-pdb-9asj.map-model.v1.json`
- `accessions` - EMDB `EMD-43816`, PDB `9ASJ`

## Expected Artifacts

- `/workspace/cryocore/runs/<run-id>/dossier_manifest.json` - map/model dossier inventory.
- `/workspace/cryocore/runs/<run-id>/validation/map_model_fit.json` - validation summary.
- `/workspace/cryocore/runs/<run-id>/figures/` - reproducible figure panels.
- `/workspace/cryocore/runs/<run-id>/methods.md` - methods draft.
- `/workspace/cryocore/runs/<run-id>/claim_ledger.md` - claim/evidence/caveat ledger.

## Stage / Progress Contract

- stage contract: `n/a`
- artifact granularity: `per-issue`
- progress ledger: `n/a`
- resume command: `see Validation Commands`
- partial success policy: `blocked, partial, or degraded closeout only; no provider or scientific success claim without the declared artifacts and validation evidence`

## Provider / Execution Profile

- provider: `runpod`
- execution profile: `map-model-dossier`
- operator gate required: `yes`

## Tooling / License Posture

- tools: `repo validators, public metadata tooling, provider dry-run scaffolds as declared by the issue`
- posture: `mixed`
- current primary source checked: `no; repo-local contract posture only`
- intended use context: `unknown until operator gate`
- image/runtime action: `scaffold or dry-run only unless the issue explicitly authorizes execution`
- operator action required: `explicit approval before paid provider mutation, gated tool installation, raw data download, or private-data handling`

## Acceptance Criteria

- [ ] Run downloads only EMDB/PDB map/model artifacts, never raw EMPIAR movies.
- [ ] Figures are generated from reproducible scripts or sessions.
- [ ] Claim ledger distinguishes structure-supported claims from interpretation.
- [ ] Phenix and ChimeraX are optional gated lanes until runtime access exists.

## Validation Commands

```bash
python3 scripts/cryocore/runpod_manifest_check.py runpod/launch-manifests/map-model-dossier.json --json
python3 scripts/cryocore/license_gate_check.py --manifest runpod/launch-manifests/map-model-dossier.json --json
make test
```

## Final Outcome Contract

- worker lane: `codex or trusted-after-run`
- closeout state: `issue-declared target state`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `declared artifacts, validation commands, and explicit partial/degraded/blocked closeout when evidence is incomplete`

## Touched Areas

- `modules/data-modules/` - EMDB/PDB map-model contract.
- `runpod/launch-manifests/` - map/model dossier launch profile.
- `modules/artifact-contracts/` - dossier artifact requirements.

## Dependencies

Blocked by: CRYOCORE-W08 and explicit operator approval for map/model RunPod execution.

## Risk Notes

- Do not overclaim raw-data reproducibility from a map/model-only lane.
- Record contour levels, software versions, accessions, and caveats in every figure artifact.

## Complexity

tier: medium

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W11
target_state: Backlog
touched_areas:
  - modules/data-modules/
  - runpod/launch-manifests/
  - modules/artifact-contracts/
complexity: medium
-->
