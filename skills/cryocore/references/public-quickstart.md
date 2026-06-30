# Public Quickstart

This checkout gives you a fast local view of CryoCore before any provider
account, raw cryo-EM data, or license-gated package is involved. The first run
shows how an agent turns public structure data into an inspectable review page
with figures, methods, provenance, claim boundaries, and machine-readable
artifacts.

For agent-first usage, start with `docs/agent-quickstart.md`. For practical
workflows, use `docs/workflows.md` and `docs/use-cases.md`.

## Five-Minute First Run

From the repository root:

```bash
python3 -m venv .runtime/venv
. .runtime/venv/bin/activate
python3 -m pip install -r requirements-dev.txt
make demo-local
```

Inspect:

- `.runtime/t2r14-open-dossier/artifacts/report.html`
- `.runtime/t2r14-open-dossier/artifacts/claim_ledger.md`
- `.runtime/t2r14-open-dossier/artifacts/dossier_manifest.json`
- `.runtime/t2r14-open-dossier/artifacts/runpod-execution.tar.gz`

`runpod-execution` is the portable artifact-root convention used by provider
review. The first local demo writes it under `.runtime/` so users can inspect
the same shape without launching a provider.

This demo fetches public RCSB metadata and public mmCIF coordinates only, then
turns them into a small inspectable structure review. Raw movies, particle
stacks, maps, half-maps, model weights, private data, license files, and gated
tools stay outside the demo.

## Command Matrix

| Command | Use it for | Network | Provider mutation | Writes |
| --- | --- | --- | --- | --- |
| `make doctor` | public readiness report | no | no | no |
| `make readonly-check` | local structural validators | no | no | Python caches |
| `make release-check` | full public release gate | no | no | Python caches |
| `make demo-local` | tiny public-coordinate T2R14 demo | yes | no | `.runtime/` |
| `make public-metadata-check` | public accession metadata smoke | yes | no | no by default |
| `python3 scripts/cryocore/t2r14_open_dossier.py --out .runtime/t2r14-open-dossier --json` | tiny public-coordinate demo | yes | no | `.runtime/` |
| `make toolcheck` | no-download toolcheck fixture | no | no | `.runtime/` |
| `make runpod-scope-check` | public bridge manifest scope | no | no | no |

See `docs/validation-command-matrix.md` for the full map.

## Local Release Gate

Run the full local gate from the repository root:

```bash
make release-check
```

The gate is read-only except for normal Python cache files and ignored runtime
outputs. It validates manifests, schemas, issue templates, provider contracts,
public-snapshot hygiene, and the secret-scan path.

## Metadata-Only Demo

The public metadata path may query accession metadata and write only small
ledgers:

```bash
make public-metadata-check
```

The metadata path writes ledgers only. Raw movies, particle stacks, maps,
half-maps, masks, private structures, model weights, and license-gated content
stay outside git.

## Provider Prep

RunPod and other provider manifests in this repo are contracts and preparation
packets: provider profiles, stage contracts, artifact roots, budget gates, and
artifact-review requirements. A paid or mutating launch requires an
operator-owned launcher outside the public repo, explicit credentials, current
license review, a budget gate, and fetched artifact evidence.

Use:

```bash
make launch-preflight-prep
make runpod-scope-check
make provider-closeout-check
```

`make launch-preflight-real` is intentionally stricter and can fail while the
public repo is still healthy. Real launch readiness requires a digest-pinned
image or audited bootstrap route, a 40-character public commit SHA, operator
authorization, runtime credentials outside git, artifact fetch/hash, cost
reporting, and cleanup proof.

The public repo should remain useful even when those provider steps are never
run.

## After A Demo

Clean local caches and ignored runtime output with:

```bash
make clean
```
