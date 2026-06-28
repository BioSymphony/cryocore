# Recipes

These recipes are agent-ready starting points. Paid compute, raw data
transfers, license-gated software, and private data handling stay behind
operator gates.

| Goal | Recipe |
| --- | --- |
| Check the repo | `make release-check` |
| Fetch metadata only | [Public Accession Example](public-accession-example.md) |
| Build a map/model review plan | [Map/Model Dossier](map-model-dossier.md) |
| Choose public-accession, cloud, Linear, or run-review path | [Workflow Blueprints](../workflows.md) |
| Review a provider run | [Provider Run Review](provider-closeout.md) |
| Audit a tool or license posture | [Toolwatch Audit](toolwatch-audit.md) |
| Review structural figures | [Figure Dossier](figure-dossier.md) |
| Render snapshots, movies, or FSC panels | [Figure Rendering](rendering.md) |
| Plan heterogeneity/state analysis | [Heterogeneity Jury](heterogeneity-jury.md) |

## Fast Local Check

```bash
python3 -m pip install -r requirements-dev.txt
make release-check
```

Use [Validation Command Matrix](../validation-command-matrix.md) to pick
narrower commands.
