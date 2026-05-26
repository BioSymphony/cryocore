# Troubleshooting

For false-success and public-release risk patterns, also read
[Failure Modes](failure-modes.md).

## `make release-check` Fails On `public_snapshot_check`

Common causes:

- A heavy data suffix was added, such as `.mrc`, `.map`, `.star`, `.cs`, `.pt`,
  `.safetensors`, `.zip`, or `.tar.gz`.
- A local path, private marker, token-like string, or provider credential was
  added.
- A runtime directory such as `.runtime/`, `artifacts/`, `outputs/`, or
  `scratch/` is being considered for commit.

Move runtime outputs to ignored storage, replace private values with public-safe
descriptions, then rerun:

```bash
make public-release-report
```

## Provider Closeout Is Blocked

Real closeout needs the following alongside provider status, command exit, and pod ID:

- `stage-progress.jsonl`
- `validation/stage-contract-check.json`
- `validation/input-audit.json`
- `validation/contract-self-check.json`
- `artifact_hashes.json`
- cost report for paid compute
- cleanup proof for temporary provider resources
- claim ledger with evidence artifacts

## Schema Check Fails

Use `modules/schemas/` as the source of truth. The local checker implements the
small JSON Schema subset used by this repo and intentionally fails closed on
required fields, enums, types, `const`, arrays, and `anyOf` branches.

## Tool Or License Is Unclear

Record the tool as `watch` or `gated`. Do not add binaries, installers, license
files, model weights, private image layers, or execution claims until current
terms and use context are reviewed.

## CI Fails On Gitleaks

Treat it as a release blocker. Remove the secret-like text or split test strings
so the scanner can distinguish detectors from real credentials. Do not suppress
without a clear public-safe reason.

## RunPod Scope Check Fails

Common blockers:

- `remote_launch_allowed` is true in a public bridge manifest.
- An inline base64 source bundle cannot be decoded and scanned.
- A public `http.server` binds to `0.0.0.0` without authenticated access.
- A public artifact server serves the repo workspace instead of
  `runpod-execution/artifacts`.

Regenerate the bridge manifest after fixing the source generator:

```bash
python3 scripts/cryocore/build_t2r14_bridge_manifest.py
python3 scripts/cryocore/build_poltheta_bridge_manifest.py
python3 scripts/cryocore/build_structure_jury_bridge_manifest.py
make runpod-scope-check
```

## RunPod Reference Check Fails

`resume_command` or an entrypoint references a missing local script. Add a
public-safe implementation, add a fail-closed stub, or update the stage contract
to point at an existing public entrypoint.

```bash
make runpod-reference-check
```

## Related

- [Failure Modes](failure-modes.md): the false-success patterns these checks defend against.
- [Validation Command Matrix](validation-command-matrix.md): full validator list with side-effect and network notes.
- [No-False-Success Hardening](no-false-success-hardening.md): the closeout rules and required artifacts.
- [Public Switch Checklist](public-switch-checklist.md): the readiness list these checks support.
