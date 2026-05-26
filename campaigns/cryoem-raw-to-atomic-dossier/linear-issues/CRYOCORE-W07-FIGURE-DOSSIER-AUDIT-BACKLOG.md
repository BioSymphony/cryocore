## Summary

Backlog the publishable figure dossier, methods draft, claim ledger, reviewer skepticism pass, and next-experiment recommendations for the raw-to-atomic campaign.

## Inputs

- `model validation` - future W06 outputs.
- `figure contract` - CryoCore artifact and validation references.

## Expected Artifacts

- structure dossier
- figure dossier
- methods draft
- claim ledger
- reviewer-grade caveat audit
- next-experiment plan

## Stage / Progress Contract

- stage contract: `n/a`
- artifact granularity: `per-issue`
- progress ledger: `n/a`
- resume command: `see Validation Commands`
- partial success policy: `blocked, partial, or degraded closeout only; no provider or scientific success claim without the declared artifacts and validation evidence`

## Provider / Execution Profile

- provider: `provider-neutral`
- execution profile: `map-model-dossier`
- operator gate required: `yes`

## Tooling / License Posture

- tools: `repo validators, public metadata tooling, provider dry-run scaffolds as declared by the issue`
- posture: `mixed`
- current primary source checked: `no; repo-local contract posture only`
- intended use context: `unknown until operator gate`
- image/runtime action: `scaffold or dry-run only unless the issue explicitly authorizes execution`
- operator action required: `explicit approval before paid provider mutation, gated tool installation, raw data download, or private-data handling`

## Acceptance Criteria

- [ ] Every figure is reproducible from scripts or saved sessions.
- [ ] Every structural claim maps to an evidence artifact and confidence level.
- [ ] Dossier includes unresolved limitations and next experiments.

## Validation Commands

```bash
make preflight
make issue-check
```

## Final Outcome Contract

- worker lane: `codex or trusted-after-run`
- closeout state: `issue-declared target state`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `declared artifacts, validation commands, and explicit partial/degraded/blocked closeout when evidence is incomplete`

## Touched Areas

- `campaigns/publishable-figure-dossier/` - figure campaign integration.
- `references/artifact-contract.md` - final dossier shape.
- `references/validation-gates.md` - claim audit gate.

## Dependencies

Blocked by: CRYOCORE-W06

## Risk Notes

- Publication-grade figures must include accessions, contour levels, software versions, and caveats.

## Complexity

tier: large

<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
campaign_id: cryoem-raw-to-atomic-dossier
wave: W07
target_state: Backlog
touched_areas:
  - campaigns/publishable-figure-dossier/
  - references/artifact-contract.md
  - references/validation-gates.md
complexity: large
-->
