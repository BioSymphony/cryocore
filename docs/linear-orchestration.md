# Tracker Orchestration

CryoCore issue contracts add cryo-EM provider, profile, stage, and evidence
gates on top of a portable external-agent issue schema. Operators may map these
drafts into Linear, GitHub Issues, or another tracker while keeping credentials,
provider logs, billing details, private data, and license files outside public
repo files and public issue bodies.

Use [Workflow Blueprints](workflows.md#5-linear-issue-wave) for the end-to-end
workflow.

## Skill Composition

- Orchestrator setup, workflow metadata, monitoring, and wave review: `portable orchestration skill or runbook`
- Codex worker tracker operations: `portable tracker integration skill or runbook`
- CryoCore domain gates: `skills/cryocore/SKILL.md`

Use the base issue sections plus the CryoCore additions in `templates/linear-issue.md`.

Specialized templates are available for common work types:

- `templates/linear-toolwatch-audit.md`
- `templates/linear-no-download-lane-scaffold.md`
- `templates/linear-paid-provider-run.md`
- `templates/linear-map-model-dossier.md`
- `templates/linear-heterogeneity-jury.md`
- `templates/linear-figure-dossier.md`

## Cross-Inventory Gate

Before dispatching a generated issue wave, run file-reference mode so referenced repo-controlled paths are checked against the actual checkout:

```bash
make issue-check
python3 scripts/cryocore/issue_check.py campaigns/cryoem-raw-to-atomic-dossier/linear-issues --check-file-references --json
```

This catches issue templates that name a non-existent script, launch manifest, bridge manifest, stage contract, or source-controlled reference. Runtime artifacts under `.runtime/`, `runpod-execution/`, `artifacts/`, and `outputs/` are validated by stage contracts and contract self-checks after execution.

## Routing

Every CryoCore external-agent issue should use:

```text
sym:cryocore
```

## Wave Labels

```text
wave:00-control
wave:01-provider-prep
wave:02-smoke
wave:03-data
wave:04-processing
wave:05-model-build
wave:06-dossier
```

## Gate Labels

```text
gate:contract
gate:environment
gate:data-intake
gate:processing
gate:model-build
gate:figure
gate:claim-audit
```

## Risk Labels

```text
risk:license-gated
risk:large-download
risk:gpu-cost
risk:secret-required
risk:gui-required
risk:human-authorization
```

## Provider Labels

```text
provider:runpod
provider:local
provider:aws-batch
provider:ssh-hpc
provider:generic-cloud
provider:neocloud
```

RunPod is the reference paid-pod provider for the first CryoCore demos. AWS Batch is the cloud scale path after adapter parity. Local, SSH/HPC, generic cloud, and neocloud labels are adapter planning or prep unless an issue explicitly authorizes provider-specific execution.

## State Policy

- `Backlog`: default for future or cost-bearing work.
- `Todo`: only the current active wave.
- `In Progress`: active external-agent worker.
- `In Review`: gate check, snapshot/manual integration, or human/operator review.
- `Blocked`: license, secret, provider, data, cost, or authorization blocker.
- `Done`, `Canceled`, `Duplicate`: terminal states.

Start CryoCore with `max_concurrent_agents: 1` until Wave 0 passes.

## Operator Workflow Adaptation

The public workflow template in `templates/symphony-cryocore.WORKFLOW.md` is
pseudocode. Use it as a checklist for a private operator workflow. The private
copy supplies tracker credentials, clean checkout or snapshot provisioning,
worker environment allowlists, and host-side provider closeout.

For paid provider work, public issues should stop at an operator-gated launch
request. Provider mutation, artifact fetch, hash verification, cost reporting,
cleanup proof, and final tracker state belong to the private operator closeout
lane.

## Linear Workflow

1. Start from `campaigns/cryoem-raw-to-atomic-dossier/issue-dag.md`.
2. Copy the relevant template from `templates/`.
3. Keep future, paid, raw-data, or license-gated work in `Backlog`.
4. Move only the first local/prep wave to `Todo`.
5. Skip any `Todo` issue with an unresolved `Blocked by:` dependency.
6. Assign one worker until `make issue-check` and the local validators pass.
7. Require every issue to state provider, execution profile, input boundary,
   expected artifacts, operator gate, validation commands, risk notes, and claim
   ceiling.
8. For cloud work, workers stop at prep-mode launch requests unless an operator
   explicitly approves provider mutation outside the public repo.
9. Move provider issues to `In Review` after artifacts are fetched and closeout
   evidence is available.
10. Move to `Done` only after the final outcome block lists artifacts,
   validation, claim level, and residual risks.

## Issue Body Must Include

- summary and scope
- declared inputs and data tier
- provider and execution profile
- stage contract or workflow contract
- expected artifacts and artifact root
- operator-gate requirement
- validation commands
- touched repo areas
- dependencies and blockers
- tracker labels or mapping to wave/provider/gate/risk labels
- risk notes
- final outcome block requirement

Do not include secret values, raw logs, credential screenshots, private data,
license files, billing exports, or heavy scientific outputs.

## Outcome Convention

Every final worker comment must include a parseable outcome block with
`outcome_version: 1`. Use [Final Outcome Block](../templates/final-outcome-block.md).

Trusted-after-run RunPod closeout moves an issue to `Done` when the declared artifacts are fetched, validated, hashed, scanned, and the cleanup has been verified. Provider success records sit alongside that evidence rather than substituting for it.
