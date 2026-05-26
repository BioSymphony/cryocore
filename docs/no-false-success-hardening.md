# No-False-Success Hardening

CryoCore runs must separate launch mechanics from scientific evidence.

![Closeout anatomy](assets/closeout-anatomy.svg)

## Required Artifacts

Every RunPod-capable execution profile has:

- a repo-committed `runpod/stage-contracts/*.stage-contract.json`
- a runtime `stage-progress.jsonl`
- `validation/input-audit.json`
- `validation/stage-contract-check.json`
- `validation/contract-self-check.json`
- `partial-summary.json` whenever a stage fails, closes partial, times out, or uses fallback

The stage contract declares stage IDs, expected outputs, timeout budgets, checkpoint markers, done markers, resume commands, partial-summary policy, stale-output policy, and `fail_closed: true`.

## Fanout Before Expensive Lanes

Raw-subset and other multiplicative lanes must run the fanout estimator before transfer, picking, classification, refinement, context annotation, or figure-generation work:

```bash
make fanout-estimate
python3 scripts/cryocore/fanout_estimator.py --manifest runpod/launch-manifests/raw-subset-open.json --json
```

Primary evidence and context evidence are separate success levels. A run can produce real primary evidence while downstream context lanes time out; that is a partial closeout with a resume path, not full success.

## Provider Truth

RunPod `desiredStatus: RUNNING` is intent. A worker must monitor provider actual status, runtime uptime, image pull success or failure, and `stage-progress.jsonl` heartbeat and terminal events.

A pod with no progress ledger is not a running CryoCore workflow. A provider allocation, port mapping, or stable desired status does not prove the container started or executed the workload.

## Exact Route Proof

Live readiness must prove the exact route, not just an installed dependency or a broad runner flag. A stage that will call `relion_refine`, `WarpTools`, `topaz`, `ctffind`, `model_angelo`, `ChimeraX`, or a repo-local Python entrypoint must record that callable path before launch and record the actual command, exit code, and output paths during execution.

For provider pods, a pinned repo ref must be fetchable by the provider route. A local-only SHA is not evidence.

## Fallbacks And Partial Success

Fallbacks are allowed only when explicit. If a run falls back from RunPod to local, private image to install-at-boot, real data to mock, full route to rescue route, or gated tool to open-only substitute, closeout status must be `partial`, `degraded`, `blocked`, or `failed`.

`contract_self_check.py` rejects silent fallback markers and rejects undegraded success after fallback. Mock, fixture, dry-run, planned-only, reference-only, or screenshot-only outputs can satisfy prep gates only.

## Related

- [Claim Levels](claim-levels.md): the ladder that closeout evidence has to support.
- [Provider Execution Model](provider-execution-model.md): how provider state is treated as intent until artifacts land.
- [Validation Command Matrix](validation-command-matrix.md): which validators to run for each evidence question.
- [Troubleshooting](troubleshooting.md) and [Failure Modes](failure-modes.md): triage when provider evidence gates fail.
- [Recipe: Provider Closeout](recipes/provider-closeout.md): a runnable closeout review against fixture artifacts.
