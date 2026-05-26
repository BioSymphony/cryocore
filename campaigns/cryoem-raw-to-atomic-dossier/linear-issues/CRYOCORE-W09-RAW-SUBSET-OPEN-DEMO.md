## Summary

Run the first honest raw-data demo using a deterministic EMPIAR-13124 raw EER subset and open tools only. Success is motion/CTF QC and a credible path to 2D classes, not a guaranteed publication-grade full reconstruction.

## Inputs

- `launch manifest` - `runpod/launch-manifests/raw-subset-open.json`
- `data module` - `modules/data-modules/empiar-13124.raw-subset.v1.json`
- `subset profile` - `raw_movies_100`

## Expected Artifacts

- `/workspace/cryocore/runs/<run-id>/data-intake-ledger.json` - subset intake ledger.
- `/workspace/cryocore/runs/<run-id>/validation/fanout-estimate.json` - bounded work estimate before transfer or context lanes.
- `/workspace/cryocore/runs/<run-id>/validation/` - tool, GPU, storage, and version checks.
- `/workspace/cryocore/runs/<run-id>/motion_correction_qc/` - motion correction outputs if tools are available.
- `/workspace/cryocore/runs/<run-id>/ctf_qc/` - CTF outputs if tools are available.
- `/workspace/cryocore/runs/<run-id>/provenance.md` - no-cheating provenance.

## Stage / Progress Contract

- stage contract: `n/a`
- artifact granularity: `per-issue`
- progress ledger: `n/a`
- resume command: `see Validation Commands`
- partial success policy: `blocked, partial, or degraded closeout only; no provider or scientific success claim without the declared artifacts and validation evidence`

## Provider / Execution Profile

- provider: `runpod`
- execution profile: `raw-subset-open`
- operator gate required: `yes`

## Tooling / License Posture

- tools: `repo validators, public metadata tooling, provider dry-run scaffolds as declared by the issue`
- posture: `mixed`
- current primary source checked: `no; repo-local contract posture only`
- intended use context: `unknown until operator gate`
- image/runtime action: `scaffold or dry-run only unless the issue explicitly authorizes execution`
- operator action required: `explicit approval before paid provider mutation, gated tool installation, raw data download, or private-data handling`

## Acceptance Criteria

- [ ] Public scaffold records only the declared raw-subset plan; real downloader work is operator-owned.
- [ ] If an operator authorizes real raw-download execution, the run downloads only the declared raw subset to provider scratch and closes with hashes, cost, and cleanup proof.
- [ ] Fanout estimate passes before download and separates primary evidence lanes from context lanes.
- [ ] No processed particles, deposited maps, deposited models, or author-aligned micrographs are used during processing.
- [ ] Run exports only small artifacts and excludes raw movies from exported outputs.
- [ ] Failures are recorded as artifacts with tool/version context and `partial-summary.json` if later context lanes fail.

## Validation Commands

```bash
make runpod-check
make fanout-estimate
python3 scripts/cryocore/runpod_manifest_check.py runpod/launch-manifests/raw-subset-open.json --json
python3 scripts/cryocore/fanout_estimator.py --manifest runpod/launch-manifests/raw-subset-open.json --json
python3 scripts/cryocore/toolcheck_runner.py --manifest runpod/launch-manifests/raw-subset-open.json --out .runtime/raw-subset-open-toolcheck --mock-gpu
```

## Final Outcome Contract

- worker lane: `codex or trusted-after-run`
- closeout state: `issue-declared target state`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `declared artifacts, validation commands, and explicit partial/degraded/blocked closeout when evidence is incomplete`

## Touched Areas

- `runpod/launch-manifests/` - raw-subset execution profile.
- `modules/data-modules/` - EMPIAR-13124 raw-subset contract.
- `runpod/entrypoints/` - RunPod runtime scaffolding.

## Dependencies

Blocked by: CRYOCORE-W08 and explicit operator approval for raw-data RunPod spend.

## Risk Notes

- Do not run this locally; raw subset data must land only on RunPod scratch.
- Stop after the bounded subset. Full EMPIAR-13124 processing requires a separate issue.

## Complexity

tier: large

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W09
target_state: Backlog
touched_areas:
  - runpod/launch-manifests/
  - modules/data-modules/
  - runpod/entrypoints/
complexity: large
-->
