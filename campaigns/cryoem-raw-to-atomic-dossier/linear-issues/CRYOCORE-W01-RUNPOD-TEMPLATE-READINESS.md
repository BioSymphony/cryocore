## Summary

Define no-download RunPod Pod templates, environment schema, and network-volume layout for CryoCore smoke testing.

## Inputs

- `runpod docs` - official RunPod Pod/template/environment documentation.
- `structure factory repo` - local RunPod launch kit.

## Expected Artifacts

- `runpod/pod-env.schema.json`
- `runpod/network-volume-layout.md`
- `runpod/templates/*.template.json`
- `runpod/launch-manifests/no-download-smoke.json`
- `scripts/cryocore/runpod_scope_check.py`

## Stage / Progress Contract

- stage contract: `runpod/stage-contracts/no-download-smoke.stage-contract.json`
- artifact granularity: `per-campaign`
- progress ledger: `/workspace/cryocore/runs/<run-id>/stage-progress.jsonl`
- resume command: `make runpod-check && make runpod-scope-check`
- partial success policy: `prep-only; failed scope or manifest checks block launch readiness`

## Provider / Execution Profile

- provider: `runpod`
- execution profile: `no-download-smoke`
- setup posture: `public image or CryoCore Network Volume bootstrap; private image optional`
- writable volume/env: `CRYOCORE_RUNPOD_NETWORK_VOLUME_ID`
- operator gate required: `no`

## Tooling / License Posture

- tools: `RunPod Pods, public Docker Hub bases, optional GHCR/private registry, optional Network Volume bootstrap`
- posture: `mixed`
- current primary source checked: `yes; docs/runpod-stack.md and docs/public-repo-and-private-image-policy.md`
- intended use context: `personal/non-commercial prep unless operator changes posture`
- image/runtime action: `scaffold`
- operator action required: `none for prep; explicit approval before paid launch`

## Acceptance Criteria

- [ ] Templates use RunPod Pods, not Serverless.
- [ ] Persistent storage is mounted at `/workspace` and durable CryoCore output paths live under `/workspace/cryocore/`.
- [ ] Network Volume guidance names CryoCore-owned writable state and does not reuse sibling campaign volumes.
- [ ] GHCR/private-image setup is documented as optional, with public image/runtime bootstrap/Network Volume bootstrap alternatives.
- [ ] No template or manifest contains secrets, license IDs, tokens, private installer URLs, or large data download instructions.

## Validation Commands

```bash
make runpod-check
make runpod-scope-check
python3 -m json.tool runpod/pod-env.schema.json >/dev/null
python3 -m json.tool runpod/launch-manifests/no-download-smoke.json >/dev/null
```

## Final Outcome Contract

- worker lane: `codex`
- closeout state: `In Review`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `runpod-check, runpod-scope-check, and no committed secrets/data`

## Touched Areas

- `runpod/` - RunPod launch kit.
- `docs/runpod-stack.md` - RunPod execution policy.

## Dependencies

Blocked by: CRYOCORE-W00

## Risk Notes

- Do not run `runpodctl pod create` in this issue.
- License-gated tools remain gated and runtime-provided.

## Complexity

tier: medium

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W01
target_state: Todo
touched_areas:
  - runpod/
  - docs/runpod-stack.md
complexity: medium
-->
