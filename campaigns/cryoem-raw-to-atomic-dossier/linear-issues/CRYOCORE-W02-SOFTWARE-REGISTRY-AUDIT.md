## Summary

Harden the CryoCore software registry so every tool-jury lane has install method, license posture, smoke command, image family, GPU class, artifacts, and citation notes.

## Inputs

- `registry` - `references/software-registry.yaml`
- `container plans` - `containers/*/README.md`

## Expected Artifacts

- Expanded `references/software-registry.yaml`
- Container family plans under `containers/`
- Registry check output from `make registry-check`

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

- [ ] Every registry entry includes image family, install method, license class, license gate, RunPod fit, GPU class, smoke command, runtime artifacts, citation notes, status, and notes.
- [ ] Restricted tools are marked gated rather than ready.
- [ ] Registry contains cryo-EM, model-building, heterogeneity, visualization, validation, and provider-adjacent lanes.

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

- `references/software-registry.yaml` - software registry.
- `containers/` - image family plans.
- `scripts/cryocore/software_registry_check.py` - registry validation.

## Dependencies

Blocked by: CRYOCORE-W00

## Risk Notes

- Do not claim a tool is installed or ready until an actual image smoke test proves it.
- Do not commit license files, private installers, or model weights.

## Complexity

tier: medium

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W02
target_state: Todo
touched_areas:
  - references/software-registry.yaml
  - containers/
  - scripts/cryocore/software_registry_check.py
complexity: medium
-->
