# Callable Scripts

Use these helpers through your agent's terminal. The
[tool-use guide](../docs/tool-use-and-chaining.md) explains how to connect calls
and check their outputs. Most helpers use Python's standard library; renderers
and plotting tools have the dependencies listed below.

## Data, Analysis, And Rendering

| Helper | What it does | Runtime |
| --- | --- | --- |
| [Public metadata](cryocore/fetch_public_accession_metadata.py) | Prepare accession links or fetch metadata with `--fetch` | Python; network access for fetching |
| [Coordinate analysis](cryocore/t2r14_open_dossier.py) | Compute chain contacts and ligand neighborhoods; create SVG figures | Python and public RCSB access |
| [PyMOL rendering](cryocore/render/pymol_render.py) | Render maps, models, selections, and turntables | PyMOL; ffmpeg for movies |
| [ChimeraX rendering](cryocore/render/chimerax_render.py) | Prepare scene commands; run with `--execute` when authorized | Python for preparation; ChimeraX and a supported graphics context for execution |
| [FSC plotting](cryocore/render/fsc_plot.py) | Plot supplied FSC curves | Python and matplotlib |

## Checks And Execution Preparation

| Need | Helpers |
| --- | --- |
| Validate tool outputs | [Schemas](cryocore/schema_check.py), [figures](cryocore/figure_manifest_check.py), [input/output joins](cryocore/contract_self_check.py) |
| Check runtime availability | [Tool checks](cryocore/toolcheck_runner.py), [tool-record freshness](cryocore/tooling_freshness_check.py) |
| Compose workflow modules | [Module checks](cryocore/module_manifest_check.py), [provider profiles](cryocore/provider_profile_check.py) |
| Prepare provider work | [Launch preflight](cryocore/runpod_launch_preflight.py), [local preparation runner](cryocore/provider_runner.py) |
| Review a completed run | [Run checks](cryocore/provider_closeout_check.py) |
| Maintain the public toolkit | [Public content](cryocore/public_snapshot_check.py), [documentation links](cryocore/docs_link_check.py), [skill index](cryocore/skill_pack_check.py) |

Use [the validation command matrix](../docs/validation-command-matrix.md) to
choose a check and review its side effects.
