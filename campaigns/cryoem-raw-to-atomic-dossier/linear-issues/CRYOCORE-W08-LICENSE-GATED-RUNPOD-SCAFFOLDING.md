## Summary

Add prep-only RunPod scaffolding for open and license-gated CryoCore lanes. This issue does not launch RunPod, download EMPIAR data, or install restricted software.

## Inputs

- `repo` - `path/to/biosymphony-cryocore-public`
- `license posture` - CryoSPARC, Phenix, and ChimeraX remain runtime-gated; MotionCor3 is open-source but still needs exact build/version verification.

## Expected Artifacts

- `scripts/cryocore/license_gate_check.py` - open/gated lane readiness checker.
- `runpod/entrypoints/` - bootstrap and export scripts.
- `runpod/launch-manifests/` - no-download, raw-subset, gated, and map/model launch profiles.

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
- operator action required: `explicit approval before paid provider mutation, gated tool installation, raw data download, or private-data handling`

## Acceptance Criteria

- [ ] Missing optional license gates report `skipped`, not failure.
- [ ] Enabled or required gated lanes without usable runtime access report `blocked`.
- [ ] No license IDs, private installer URLs, raw data, maps, or model weights are committed.
- [ ] All local no-download validators pass.

## Validation Commands

```bash
make preflight
make module-check
make runpod-check
make license-gate-check
make test
```

## Final Outcome Contract

- worker lane: `codex or trusted-after-run`
- closeout state: `issue-declared target state`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `declared artifacts, validation commands, and explicit partial/degraded/blocked closeout when evidence is incomplete`

## Touched Areas

- `scripts/cryocore/` - validators and gated-lane checks.
- `runpod/` - execution profiles and entrypoints.
- `modules/` - reusable sidecar contracts.

## Dependencies

Blocked by: CRYOCORE-W04A

## Risk Notes

- This is prep-only. Do not launch RunPod or download raw EMPIAR data.
- Runtime secrets must live in RunPod secret/env configuration, not git or Linear.

## Complexity

tier: medium

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W08
target_state: Backlog
touched_areas:
  - scripts/cryocore/
  - runpod/
  - modules/
complexity: medium
-->
