## Summary

Activate the gated CryoSPARC raw-subset lane after runtime license access exists. The lane uses the same EMPIAR-13124 subset as the open demo and records exact CryoSPARC plus open-tool versions.

## Inputs

- `launch manifest` - `runpod/launch-manifests/raw-subset-gated.json`
- `runtime secrets` - RunPod-provided CryoSPARC access only.
- `prior artifacts` - CRYOCORE-W09 open-lane raw-subset ledger and QC outputs.

## Expected Artifacts

- `/workspace/cryocore/runs/<run-id>/validation/license-gates.json` - ready/blocked/skipped gate report.
- `/workspace/cryocore/runs/<run-id>/validation/fanout-estimate.json` - same-subset fanout estimate before gated transfer or processing.
- `/workspace/cryocore/runs/<run-id>/validation/versions.json` - gated and open tool versions.
- `/workspace/cryocore/runs/<run-id>/cryosparc_project_manifest.json` - CryoSPARC job/export ledger if enabled.
- `/workspace/cryocore/runs/<run-id>/provenance.md` - runtime secret and license caveats without secret values.

## Stage / Progress Contract

- stage contract: `n/a`
- artifact granularity: `per-issue`
- progress ledger: `n/a`
- resume command: `see Validation Commands`
- partial success policy: `blocked, partial, or degraded closeout only; no provider or scientific success claim without the declared artifacts and validation evidence`

## Provider / Execution Profile

- provider: `runpod`
- execution profile: `raw-subset-gated`
- operator gate required: `yes`

## Tooling / License Posture

- tools: `repo validators, public metadata tooling, provider dry-run scaffolds as declared by the issue`
- posture: `mixed`
- current primary source checked: `no; repo-local contract posture only`
- intended use context: `unknown until operator gate`
- image/runtime action: `scaffold or dry-run only unless the issue explicitly authorizes execution`
- operator action required: `explicit approval before paid provider mutation, gated tool installation, raw data download, or private-data handling`

## Acceptance Criteria

- [ ] CryoSPARC gate reports `ready` before processing begins; MotionCor3/open-tool executable readiness is recorded separately.
- [ ] Fanout estimate matches the declared subset and stays within the operator-approved budget.
- [ ] No license ID, installer URL, token, or proprietary package is written to git or Linear.
- [ ] Gated outputs are compared against the open-lane run using the same subset profile.
- [ ] Any blocked license gate fails the gated run clearly before large downloads.

## Validation Commands

```bash
python3 scripts/cryocore/license_gate_check.py --manifest runpod/launch-manifests/raw-subset-gated.json --json
python3 scripts/cryocore/runpod_manifest_check.py runpod/launch-manifests/raw-subset-gated.json --json
python3 scripts/cryocore/fanout_estimator.py --manifest runpod/launch-manifests/raw-subset-gated.json --json
make test
```

## Final Outcome Contract

- worker lane: `codex or trusted-after-run`
- closeout state: `issue-declared target state`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `declared artifacts, validation commands, and explicit partial/degraded/blocked closeout when evidence is incomplete`

## Touched Areas

- `runpod/entrypoints/` - gated bootstrap scripts.
- `runpod/launch-manifests/` - gated raw-subset launch profile.
- `scripts/cryocore/` - license gate and toolcheck validation.

## Dependencies

Blocked by: CRYOCORE-W09 and confirmed CryoSPARC runtime access.

## Risk Notes

- Academic/non-commercial licenses must not be used for commercial service work.
- CryoSPARC UI ports must not be exposed directly to the public internet.

## Complexity

tier: large

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W10
target_state: Blocked
touched_areas:
  - runpod/entrypoints/
  - runpod/launch-manifests/
  - scripts/cryocore/
complexity: large
-->
