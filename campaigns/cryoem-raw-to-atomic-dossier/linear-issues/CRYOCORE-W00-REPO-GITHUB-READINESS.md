## Summary

Prepare the CryoCore public checkout for a clean-history public repository, without launching RunPod or downloading data.

## Inputs

- `repo` - current `biosymphony-cryocore-public` checkout.
- `remote` - public repository remote to be added only after scrub and operator approval.

## Expected Artifacts

- `git remote -v` is empty or points only to the intended public repository.
- `main` is ready for a clean baseline commit after release checks pass.
- Repo-local validation commands pass.

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

- [ ] Public repository destination is selected, but no private remote is required.
- [ ] Clean-history `main` is ready with the CryoCore readiness files.
- [ ] No raw cryo-EM data, maps, private structures, model weights, secrets, or large biological data are committed.

## Validation Commands

```bash
git status --short --branch
git remote -v
make preflight
make registry-check
make runpod-check
make issue-check
make release-check
```

## Final Outcome Contract

- worker lane: `codex or trusted-after-run`
- closeout state: `issue-declared target state`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `declared artifacts, validation commands, and explicit partial/degraded/blocked closeout when evidence is incomplete`

## Touched Areas

- `README.md` - repo readiness instructions.
- `AGENTS.md` - agent guardrails.
- `.gitignore` - heavy-data exclusions.

## Dependencies

Blocked by: none

## Risk Notes

- Do not paste GitHub tokens, deploy keys, tracker API keys, or RunPod credentials into files or tracker comments.
- This issue does not authorize RunPod execution.

## Complexity

tier: medium

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W00
target_state: Todo
touched_areas:
  - README.md
  - AGENTS.md
  - .gitignore
complexity: medium
-->
