## Summary

Backlog atomic model building, refinement, and validation lanes for ModelAngelo, Phenix, Coot, ChimeraX, ISOLDE, MolProbity-style checks, and map-model evidence.

## Inputs

- `map outputs` - future W05 reconstruction artifacts.
- `sequence/model references` - public accessions or secure local references only.

## Expected Artifacts

- atomic model build manifest
- validation summaries
- model/map fit evidence
- chain assignment notes

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

- [ ] Model-building lane records tool versions, input map, sequence source, and confidence caveats.
- [ ] Validation includes geometry and map-model agreement checks.
- [ ] Restricted tools remain gated until license/runtime access is explicit.

## Validation Commands

```bash
make registry-check
make preflight
```

## Final Outcome Contract

- worker lane: `codex or trusted-after-run`
- closeout state: `issue-declared target state`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `declared artifacts, validation commands, and explicit partial/degraded/blocked closeout when evidence is incomplete`

## Touched Areas

- `campaigns/cryoem-raw-to-atomic-dossier/` - model-build wave plan.
- `containers/model-build/` - image plan.
- `references/artifact-contract.md` - model/validation dossier requirements.

## Dependencies

Blocked by: CRYOCORE-W05

## Risk Notes

- Do not overclaim ligand, interface, or mechanism evidence without density-backed validation.

## Complexity

tier: large

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W06
target_state: Backlog
touched_areas:
  - campaigns/cryoem-raw-to-atomic-dossier/
  - containers/model-build/
  - references/artifact-contract.md
complexity: large
-->
