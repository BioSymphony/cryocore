## Summary

Backlog the real cryo-EM tool-jury lanes for RELION, CryoSPARC, Warp/M, MotionCor, CTF estimation, Topaz, crYOLO, cryoDRGN, and RECOVAR after no-download RunPod readiness passes.

## Inputs

- `smoke outcome` - CRYOCORE-W04 artifacts.
- `public dataset` - EMPIAR accession references only, no committed raw data.

## Expected Artifacts

- tool-jury run plan
- per-lane manifests
- license gates for restricted tools
- data intake ledger

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

- [ ] No real raw data download starts until storage, budget, and dataset scope are approved.
- [ ] Each tool lane has an explicit install/status gate.
- [ ] Disagreements become review artifacts rather than hidden failures.

## Validation Commands

```bash
make preflight
make registry-check
make runpod-check
```

## Final Outcome Contract

- worker lane: `codex or trusted-after-run`
- closeout state: `issue-declared target state`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `declared artifacts, validation commands, and explicit partial/degraded/blocked closeout when evidence is incomplete`

## Touched Areas

- `campaigns/cryoem-raw-to-atomic-dossier/` - campaign plan.
- `references/software-registry.yaml` - lane readiness.
- `runpod/` - future execution manifests.

## Dependencies

Blocked by: CRYOCORE-W04 and CRYOCORE-W04A

## Risk Notes

- Keep this issue in Backlog until the no-download smoke path has passed on RunPod.

## Complexity

tier: large

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W05
target_state: Backlog
touched_areas:
  - campaigns/cryoem-raw-to-atomic-dossier/
  - references/software-registry.yaml
  - runpod/
complexity: large
-->
