## Summary

Define and validate the no-download smoke-run contract for RunPod readiness, including GPU visibility, repo clone manifest, network-volume write/read, and artifact manifest output.

## Inputs

- `manifest` - `runpod/launch-manifests/no-download-smoke.json`
- `runner` - `scripts/cryocore/toolcheck_runner.py`

## Expected Artifacts

- ignored local dry-run output under `.runtime/cryocore-toolcheck/`
- `run-manifest.json`
- `validation/toolcheck.json`
- `validation/gpu.json`
- `validation/storage.json`
- `provenance.md`

## Stage / Progress Contract

- stage contract: `n/a`
- artifact granularity: `per-issue`
- progress ledger: `n/a`
- resume command: `see Validation Commands`
- partial success policy: `blocked, partial, or degraded closeout only; no provider or scientific success claim without the declared artifacts and validation evidence`

## Provider / Execution Profile

- provider: `runpod`
- execution profile: `no-download-smoke`
- operator gate required: `no`

## Tooling / License Posture

- tools: `repo validators, public metadata tooling, provider dry-run scaffolds as declared by the issue`
- posture: `mixed`
- current primary source checked: `no; repo-local contract posture only`
- intended use context: `unknown until operator gate`
- image/runtime action: `scaffold or dry-run only unless the issue explicitly authorizes execution`
- operator action required: `none for local mock prep; explicit approval is deferred to CRYOCORE-W04A before paid provider mutation, gated tool installation, raw data download, or private-data handling`

## Acceptance Criteria

- [ ] Toolcheck runner can execute locally in mock-GPU mode.
- [ ] Toolcheck runner writes all expected no-download artifacts.
- [ ] The contract records missing optional tools without treating them as fatal during prep.

## Validation Commands

```bash
make toolcheck
test -f .runtime/cryocore-toolcheck/run-manifest.json
test -f .runtime/cryocore-toolcheck/validation/toolcheck.json
test -f .runtime/cryocore-toolcheck/validation/storage.json
```

## Final Outcome Contract

- worker lane: `codex or trusted-after-run`
- closeout state: `issue-declared target state`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `declared artifacts, validation commands, and explicit partial/degraded/blocked closeout when evidence is incomplete`

## Touched Areas

- `scripts/cryocore/toolcheck_runner.py` - smoke runner.
- `references/artifact-contract.md` - smoke dossier contract.
- `references/validation-gates.md` - environment/storage gates.

## Dependencies

Blocked by: CRYOCORE-W03

## Risk Notes

- Use `--mock-gpu` only for local prep; real RunPod smoke should require actual GPU visibility.
- Do not download EMPIAR, EMDB, PDB, model weights, or private data in this issue.

## Complexity

tier: medium

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W04
target_state: Todo
touched_areas:
  - scripts/cryocore/toolcheck_runner.py
  - references/artifact-contract.md
  - references/validation-gates.md
complexity: medium
-->
