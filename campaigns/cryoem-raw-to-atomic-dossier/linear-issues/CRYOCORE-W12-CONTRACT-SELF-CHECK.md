## Summary

Add the CryoCore no-false-success gate: an input audit before execution and a contract self-check before any cryo-EM RunPod or dossier issue can close as successful.

## Inputs

- `GeneCluster learning` - every BioSymphony workflow needs explicit input-audit and joined contract-self-check scripts.
- `CryoCore manifests` - `runpod/launch-manifests/` and `modules/artifact-contracts/structure-dossier.v1.json`.
- `prior run artifacts` - no-download, raw-subset, or map/model artifact roots under `/workspace/cryocore/runs/<run-id>/`.

## Expected Artifacts

- `scripts/cryocore/input_audit.py` - summarizes known manifest inputs and missing operator items before execution.
- `scripts/cryocore/contract_self_check.py` - joins declared inputs, materialized ledgers, run artifacts, mock labels, validation outputs, and claim levels.
- `validation/input-audit.json` - run-local input audit report.
- `validation/contract-self-check.json` - run-local final evidence join report.

## Stage / Progress Contract

- stage contract: `n/a`
- artifact granularity: `per-issue`
- progress ledger: `n/a`
- resume command: `see Validation Commands`
- partial success policy: `blocked, partial, or degraded closeout only; no provider or scientific success claim without the declared artifacts and validation evidence`

## Provider / Execution Profile

- provider: `provider-neutral`
- execution profile: `no-download-smoke`
- operator gate required: `no`

## Tooling / License Posture

- tools: `repo validators, public metadata tooling, provider dry-run scaffolds as declared by the issue`
- posture: `mixed`
- current primary source checked: `no; repo-local contract posture only`
- intended use context: `unknown until operator gate`
- image/runtime action: `scaffold or dry-run only unless the issue explicitly authorizes execution`
- operator action required: `explicit approval before paid provider mutation, gated tool installation, raw data download, or private-data handling`

## Acceptance Criteria

- [ ] Input audit reads manifests/ledgers first and emits only explicit `missing_operator_items`.
- [ ] Contract self-check fails real runs when `mock_gpu`, `mock_tools`, or `dry_run` evidence is required.
- [ ] Raw-subset success requires data-intake ledger values to join to the declared EMPIAR subset profile and deterministic rule.
- [ ] Map/model dossier success requires claim levels and map/model validation evidence rather than screenshots or command flags.
- [ ] All local no-download validators pass.

## Validation Commands

```bash
make input-audit
make contract-self-check
make test
```

## Final Outcome Contract

- worker lane: `codex or trusted-after-run`
- closeout state: `issue-declared target state`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `declared artifacts, validation commands, and explicit partial/degraded/blocked closeout when evidence is incomplete`

## Touched Areas

- `scripts/cryocore/` - audit and final self-check scripts.
- `modules/artifact-contracts/` - dossier closeout and evidence requirements.
- `references/validation-gates.md` - maturity ladder and no-false-success rule.
- `campaigns/cryoem-raw-to-atomic-dossier/` - Linear DAG and issue contract.

## Dependencies

Blocked by: CRYOCORE-W08

## Risk Notes

- This is a validation-hardening issue only. Do not launch RunPod or download raw EMPIAR data.
- A passing schema check is not enough; the final self-check must prove artifact joins.
- Do not claim final resolution, handedness, ligand fit, or publishability from screenshots or single-map evidence.

## Complexity

tier: medium

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W12
target_state: Backlog
touched_areas:
  - scripts/cryocore/
  - modules/artifact-contracts/
  - references/validation-gates.md
  - campaigns/cryoem-raw-to-atomic-dossier/
complexity: medium
-->
