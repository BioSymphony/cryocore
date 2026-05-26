## Summary

Implement provider-neutral RunPod launch-bundle tooling that packages a no-download smoke manifest and remote toolcheck runner without launching a Pod.

## Inputs

- `manifest` - `runpod/launch-manifests/no-download-smoke.json`
- `scripts` - CryoCore local scripts.

## Expected Artifacts

- `scripts/cryocore/runpod_launch_bundle.py`
- `scripts/cryocore/runpod_manifest_check.py`
- ignored dry-run output under `.runtime/cryocore-no-download-smoke/`

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

- [ ] Launch bundle generation succeeds without RunPod credentials.
- [ ] Bundle includes launch manifest, run-later instructions, remote runner, and bundle manifest.
- [ ] Bundle generation does not download data, launch RunPod, or require restricted licenses.

## Validation Commands

```bash
make runpod-check
make launch-bundle
python3 scripts/cryocore/runpod_manifest_check.py .runtime/cryocore-no-download-smoke/launch-manifest.json --json
```

## Final Outcome Contract

- worker lane: `codex or trusted-after-run`
- closeout state: `issue-declared target state`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `declared artifacts, validation commands, and explicit partial/degraded/blocked closeout when evidence is incomplete`

## Touched Areas

- `scripts/cryocore/runpod_launch_bundle.py` - launch bundle generator.
- `scripts/cryocore/runpod_manifest_check.py` - manifest validator.
- `runpod/launch-manifests/` - launch manifest inputs.

## Dependencies

Blocked by: CRYOCORE-W01, CRYOCORE-W02

## Risk Notes

- `.runtime/` output is ignored and should not be committed.
- This issue does not authorize RunPod execution.

## Complexity

tier: medium

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W03
target_state: Todo
touched_areas:
  - scripts/cryocore/runpod_launch_bundle.py
  - scripts/cryocore/runpod_manifest_check.py
  - runpod/launch-manifests/
complexity: medium
-->
