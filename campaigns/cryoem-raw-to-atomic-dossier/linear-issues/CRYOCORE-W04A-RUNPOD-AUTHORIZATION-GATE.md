## Summary

Hold the line between no-download prep and any cost-bearing RunPod, large-download, or license-gated execution. This is a human/operator gate, not a worker implementation issue.

## Inputs

- `smoke contract` - CRYOCORE-W04 outcome and ignored `.runtime/` dry-run artifacts.
- `RunPod account` - external operator-controlled account and network volume.
- `license posture` - explicit runtime access decisions for gated tools.

## Expected Artifacts

- Operator decision comment in the selected tracker.
- Confirmed RunPod network volume plan or explicit decision to defer.
- Confirmed no secrets, license IDs, model weights, raw maps, or raw movies are in git or tracker comments.

## Stage / Progress Contract

- stage contract: `n/a`
- artifact granularity: `per-campaign`
- progress ledger: `n/a`
- resume command: `make runpod-scope-check && make launch-preflight-prep`
- partial success policy: `operator may close blocked/deferred; no paid execution is successful until artifacts are fetched, hashed, and cleanup is verified`

## Provider / Execution Profile

- provider: `runpod`
- execution profile: `no-download-smoke`
- setup posture: `operator-selected: public image, private image, runtime bootstrap, or CryoCore Network Volume bootstrap`
- writable volume/env: `CRYOCORE_RUNPOD_NETWORK_VOLUME_ID if a writable RunPod volume is authorized`
- operator gate required: `yes`

## Tooling / License Posture

- tools: `RunPod Pods, optional private registry, optional Network Volume bootstrap, optional license-gated tools after separate approval`
- posture: `mixed`
- current primary source checked: `yes; docs/runpod-stack.md and docs/tooling-and-licensing.md`
- intended use context: `operator-declared before launch`
- image/runtime action: `scaffold`
- operator action required: `explicit GO, setup posture, spend cap, cleanup policy, and owned resource confirmation`

## Acceptance Criteria

- [ ] Operator confirms whether a real no-download RunPod smoke launch is authorized.
- [ ] Operator confirms GPU budget/class and network volume path if launch is authorized.
- [ ] Operator confirms the setup posture; GHCR/private image is optional, and the default non-GHCR path is CryoCore Network Volume bootstrap.
- [ ] Operator confirms any writable RunPod volume is CryoCore-owned and not a sibling campaign volume.
- [ ] Operator confirms large data downloads remain blocked until a later explicit data-intake gate.

## Validation Commands

```bash
make preflight
make runpod-check
make runpod-scope-check
python3 scripts/cryocore/public_release_report.py --repo-root . --json
```

## Final Outcome Contract

- worker lane: `trusted-after-run`
- closeout state: `In Review`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `explicit operator decision; paid launch remains blocked unless the trusted launcher validates scope, artifacts, hashes, and cleanup`

## Touched Areas

- `campaigns/cryoem-raw-to-atomic-dossier/linear-issues/` - authorization gate contract.
- `docs/linear-orchestration.md` - gate/state policy if changed.

## Dependencies

Blocked by: CRYOCORE-W04

## Risk Notes

- Keep this issue non-terminal until a human/operator intentionally approves or rejects execution.
- Do not move downstream cost-bearing work to `Todo` while this issue is unresolved.
- This issue does not itself launch RunPod.
- Do not create, stop, delete, or modify any pod/volume/template that is not declared by CryoCore manifests or the CryoCore pod ledger.

## Complexity

tier: small

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W04A
target_state: In Review
touched_areas:
  - campaigns/cryoem-raw-to-atomic-dossier/linear-issues/
  - docs/linear-orchestration.md
complexity: small
-->
