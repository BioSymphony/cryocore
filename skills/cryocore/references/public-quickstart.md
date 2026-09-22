# Public Quickstart

Run the CPU-only demo to turn public structure coordinates and metadata into
an HTML review report. The report includes figures, methods, input provenance,
and evidence limits. No provider account or GPU is needed.

For agent tasks, start with the [agent quickstart](agent-quickstart.md). For
processing plans, see [workflows](workflows.md) and [use cases](use-cases.md).

## Run The Local Demo

From the repository root, with Python 3.10 or later:

```bash
python3 -m venv .runtime/venv
. .runtime/venv/bin/activate
python3 -m pip install -r requirements-dev.txt
make demo-local
```

The demo fetches public RCSB metadata and mmCIF coordinates. It writes these
outputs under `.runtime/t2r14-open-dossier/artifacts/`:

| File | Contents |
| --- | --- |
| `report.html` | Review page with figures and methods |
| `claim_ledger.md` | Supported conclusions and evidence limits |
| `dossier_manifest.json` | Input and output records |
| `runpod-execution.tar.gz` | Portable artifact bundle for run review |

The bundle uses the same directory layout as provider output. Creating it
locally does not launch a provider or process experimental maps.

## Command Matrix

| Command | Use it for | Network | Provider mutation | Writes |
| --- | --- | --- | --- | --- |
| `make doctor` | public readiness report | no | no | no |
| `make readonly-check` | local structural validators | no | no | Python caches |
| `make release-check` | full public release gate | no | no | Python caches |
| `make demo-local` | tiny public-coordinate T2R14 demo | yes | no | `.runtime/` |
| `make public-metadata-check` | metadata fixture and accession links | no | no | no |
| `python3 scripts/cryocore/t2r14_open_dossier.py --out .runtime/t2r14-open-dossier --json` | tiny public-coordinate demo | yes | no | `.runtime/` |
| `make toolcheck` | no-download toolcheck fixture | no | no | `.runtime/` |
| `make runpod-scope-check` | public bridge manifest scope | no | no | no |

See `docs/validation-command-matrix.md` for the full map.

## Local Release Gate

Run the full local gate from the repository root:

```bash
make release-check
```

The gate validates manifests, schemas, issue templates, provider contracts,
skill bundles, and public content, then runs the tests. Secret scanning runs
when Gitleaks is installed; use `make release-check REQUIRE_GITLEAKS=1` to
require it. The checks may create Python caches but do not launch providers.

## Metadata-Only Demo

Check the metadata fixture and prepare accession references locally:

```bash
make public-metadata-check
```

This command checks a JSON fixture and builds EMPIAR, EMDB, and PDB metadata
URLs without fetching them. It discards the generated ledger and creates no
output files. The underlying script fetches metadata only with `--fetch`.

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
public repo is still healthy. Real launch readiness requires a digest-pinned image or audited bootstrap route, a 40-character
public commit SHA, operator
authorization, runtime credentials outside git, artifact fetch/hash, cost
reporting, and cleanup proof.

## After A Demo

Remove Python caches and the entire `.runtime/` directory, including demo
reports and the virtual environment, with:

```bash
make clean
```
