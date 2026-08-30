# Demos

Three public workflow examples. T2R14 runs locally without credentials. The Pol
Theta and Dual Structure examples provide local preparation checks and optional
operator-owned execution.

Select an example by its output and execution requirements.

| Demo | Runtime | Complexity | What it shows you |
| --- | --- | --- | --- |
| [T2R14 Open Dossier](t2r14-open-dossier/) | ~1 minute, CPU-only | Beginner | Declared inputs, chain and ligand summaries, SVG figures, provenance, claim boundaries, and a manifest. |
| [Pol Theta Map/Model Dossier](poltheta-map-model-dossier/) | Prep check ~1 minute. Execution is operator-owned. | Intermediate | EMDB map headers, a deposited PDB model, an AMP-PNP ligand neighborhood, wwPDB report intake, and density-support checks. |
| [Dual Structure Comparison](structure-jury-dual-dossier/) | Prep check ~1 minute. Execution is operator-owned. | Intermediate | Two public deposited-structure lanes joined into one review package for consistent comparison. |

## How to start

From a fresh checkout, run:

```bash
make demo-local
```

This command runs the T2R14 demo. It writes output to the ignored
`.runtime/t2r14-open-dossier/` directory. The primary artifacts are:

- `artifacts/report.html`: human-readable review with inputs, figures, and methods
- `artifacts/claim_ledger.md`: claim boundaries and caveats
- `artifacts/dossier_manifest.json`: machine-readable inputs, artifacts, and provenance

After T2R14, run the other two prep checks to see the full-lane and dual-lane
shapes:

```bash
make demo-poltheta-prep-check
make demo-structure-jury-prep-check
```

These two targets validate the bridge manifests with the operator-owned
provider bridge CLI, defaulting to `symphony-neocloud-bridge`. If you do not
have that CLI installed, the targets will print a clear message and exit. The
bridge-manifest JSON files are in
[runpod/bridge-manifests/](../runpod/bridge-manifests/). You can inspect them
directly.

## Pointing your agent at the demos

Each demo README is short and agent-readable. To have your agent run a demo
itself, paste the [Agent Prompt](../README.md#agent-prompt) from the repo
README and ask the agent to start with one of the demos by name. The agent
will read the relevant README, run the prep check, and report what it found.

## How the examples scale

The examples are the smallest end-to-end exercises of CryoCore's contracts.
The contract pattern also applies to:

- [Campaign contracts](../campaigns/) for multi-stage missions
- [Provider profiles](../modules/provider-profiles/) for RunPod, AWS Batch, SSH/HPC, and other lanes
- [Linear-style issue waves](../docs/linear-orchestration.md) for tracker-driven campaigns

See [Demo Gallery](../docs/demo-gallery.md) for the descriptive companion to
this index, and [Workflow Blueprints](../docs/workflows.md) when you are ready
to pick the next workflow scale.
