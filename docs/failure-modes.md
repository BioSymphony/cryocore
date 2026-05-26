# Failure Modes

These are the common ways CryoCore can look successful while still being unsafe
or scientifically incomplete.

| Failure mode | Symptom | Required response |
| --- | --- | --- |
| Provider status treated as evidence | Pod is `RUNNING` or `COMPLETED`, but artifacts are missing. | Run closeout checks. Do not claim success without fetched artifacts, hashes, validation, and cleanup proof. |
| Public service exposes the workspace | A bridge manifest starts `http.server` on `0.0.0.0` from the repo root. | Fail the manifest. Serve only `runpod-execution/artifacts` and require authenticated access. |
| Inline source bundle hides private code | A bridge manifest embeds a base64 tarball. | Decode, list, path-check, and scan the bundle before release. |
| Stage contract points to stale scripts | `resume_command` references a missing local entrypoint. | Fix the reference or add a public fail-closed stub before release. |
| Raw or deposited source data leaks into archives | Export tarballs include `data/`, `.map`, `.mrc`, `.cif`, or raw movie files. | Archive only reports, ledgers, validation summaries, and figures unless an operator explicitly approves a data export. |
| License-gated tool runs without a gate | CryoSPARC, Phenix, ChimeraX, MotionCor2, or similar tools run from public defaults. | Fail closed until current license, user context, credential, and budget gates are recorded outside git. |
| Fallback output is promoted | A mock or fixture artifact satisfies a real run. | `contract_self_check.py` must reject real closeout. Downgrade the claim. |
| Tool license review is stale | Toolwatch and registry posture are older than the allowed review age. | Refresh primary-source review and update `docs/tooling-and-licensing.md`. |

## Local Triage

Run:

```bash
make runpod-check
make runpod-scope-check
make public-snapshot-check
make provider-closeout-check
```

Then inspect the failing JSON report. Prefer fixing the contract or lowering the
claim over adding exceptions.

## Related

- [Troubleshooting](troubleshooting.md): per-validator triage when a specific check fails.
- [No-False-Success Hardening](no-false-success-hardening.md): the closeout rules these failure modes violate.
- [Claim Levels](claim-levels.md): the ladder to downgrade against when a failure mode lands.
- [Validation Command Matrix](validation-command-matrix.md): which validator to run for each evidence question.
