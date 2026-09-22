# Tool Use And Chaining

Use CryoCore's tool records and skills to build a sequence of calls for your
task. Your agent runs those calls through its terminal or API tools. The
repository supplies helpers and workflow contracts; scientific applications
run in the environment you provide.

## Choose A Tool

Search the [software registry](../references/software-registry.yaml) by role.
Read the source and version, install requirements, license gate, status, smoke
command, and expected outputs for each candidate. Check the review date before
relying on a record. The [source review](toolwatch-2026-09-22.md) explains the
latest additions.

Use the matching [skill](../skills/) for task instructions. A `--help` or
`--version` smoke command checks availability. Build the processing call from
the selected version's documentation and the task's inputs.

## Callable Tools

| Need | Entry point | Behavior |
| --- | --- | --- |
| Public accession metadata | [Metadata helper](../scripts/cryocore/fetch_public_accession_metadata.py) | Builds accession links; `--fetch` requests metadata and records response status and hashes |
| Coordinate analysis | [T2R14 demo](../scripts/cryocore/t2r14_open_dossier.py) | Fetches public coordinates, computes chain contacts and ligand neighborhoods, and writes SVG figures |
| Structure or density images | [PyMOL helper](../scripts/cryocore/render/pymol_render.py) | Run through installed PyMOL for map/model views, cartoons, density selections, or turntables |
| ChimeraX scenes | [ChimeraX helper](../scripts/cryocore/render/chimerax_render.py) | Prepares a command script; `--execute` runs it through an available, authorized ChimeraX installation |
| FSC curves | [FSC plotter](../scripts/cryocore/render/fsc_plot.py) | Plots supplied curve files with matplotlib; `--demo` produces an illustrative curve |
| Output checks | [Schema checker](../scripts/cryocore/schema_check.py), [figure checker](../scripts/cryocore/figure_manifest_check.py) | Check declared fields, files, and figure records before handoff |

The [scripts index](../scripts/README.md) lists the remaining helpers. Use each
helper's `--help` for its arguments. Dependencies belong in the selected
runtime; the registry is a knowledge base, not an installer or an executable
dispatch table.

## A Small Runnable Chain

From the repository root, build a metadata record and pass it to the schema
checker. These calls stay offline and write only under `.runtime/`:

```bash
python3 scripts/cryocore/fetch_public_accession_metadata.py \
  --emdb EMD-43816 --pdb 9ASJ \
  --out .runtime/tool-chain/metadata.json

python3 scripts/cryocore/schema_check.py \
  --schema modules/schemas/public-accession-metadata.v1.schema.json \
  --instance .runtime/tool-chain/metadata.json --json
```

The first call's output path is the second call's input. To fetch public
metadata, add `--fetch` to the first call. Check `fetch_performed`, each response
status, and errors before a dependent call: schema validity alone does not
establish that a request succeeded.

For a chain that performs coordinate analysis and creates figures, run
`make demo-local`. The [demo implementation](../scripts/cryocore/t2r14_open_dossier.py)
connects RCSB requests, mmCIF parsing, contact calculations, and SVG rendering.
It uses deposited coordinates; map-fit validation requires experimental maps.

## Connect Scientific Tools

The [processing module](../modules/lane-modules/raw-to-map.v1.json) declares
motion correction, CTF estimation, picking, classification, refinement, and
map postprocessing. The [model-building module](../modules/lane-modules/map-to-model.v1.json)
consumes map references, entity information, and processing records. The
[figure module](../modules/lane-modules/figure-dossier.v1.json) consumes reviewed
maps or models and a figure specification.

These are composition contracts. Configure the actual commands and any format
conversion for the installed software. For each handoff, record:

| Record | What it establishes |
| --- | --- |
| Tool version, command, and parameters | Which invocation produced the result |
| Input IDs, paths, and hashes | Which data the tool used |
| Output paths and required fields | What the next call can consume |
| Format, units, coordinate frame, and entity mapping | Whether the next tool can interpret the result |
| Exit status, file checks, and scientific validation | Whether the result is ready for the intended next step |

When a required check fails, retain the failure and correct the call or choose
a suitable alternative. Continue independent steps when their inputs are
ready. Keep original experimental evidence for validating AI-derived outputs.
See the [validation requirements](../references/validation-gates.md).

## Agent Integrations

Use the skills from a source checkout or through your agent's
[skill installation mechanism](skill-installation.md). The agent supplies
command and API access. MCP integrations documented in individual tool records
need their own setup. Trackers and task schedulers are optional coordination
layers; they are not required for a local tool chain.
