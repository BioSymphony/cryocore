# Demos

Three runnable public demos. Each one shows a different cryo-EM workflow your
agent can run with public-accession inputs and no credentials.

Pick a demo by what you want your agent (or you) to see first.

| Demo | Runtime | Complexity | What it shows you |
| --- | --- | --- | --- |
| [T2R14 Open Dossier](t2r14-open-dossier/) | ~1 minute, CPU-only | Beginner | The review shape end to end: declared inputs, chain and ligand summaries, SVG figures, provenance, claim boundaries, and a manifest. Best first run. |
| [Pol Theta Map/Model Dossier](poltheta-map-model-dossier/) | Prep check ~1 minute; real run is operator-owned | Intermediate | A full map and model lane with EMDB map headers, deposited PDB model, AMP-PNP ligand neighborhood, wwPDB report intake, and density-support checks. |
| [Dual Structure Comparison](structure-jury-dual-dossier/) | Prep check ~1 minute; real run is operator-owned | Intermediate | Two public deposited-structure lanes joined into one review. Useful for comparing two structural interpretations with the same workflow shape. |

## How to start

The fastest first command from a fresh checkout:

```bash
make demo-local
```

That runs the T2R14 demo. Output lands under `.runtime/t2r14-open-dossier/`,
which is gitignored. The headline artifacts are:

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
bridge-manifest JSON files themselves are in
[runpod/bridge-manifests/](../runpod/bridge-manifests/) and can be inspected
directly.

## Pointing your agent at the demos

Each demo README is short and agent-readable. To have your agent run a demo
itself, paste the [Agent Prompt](../README.md#agent-prompt) from the repo
README and ask the agent to start with one of the demos by name. The agent
will read the relevant README, run the prep check, and report what it found.

## Where the demos live in the bigger picture

The demos are the smallest end-to-end exercises of CryoCore's contracts. The
same shape scales to:

- [Campaign contracts](../campaigns/) for multi-stage missions
- [Provider profiles](../modules/provider-profiles/) for RunPod, AWS Batch, SSH/HPC, and other lanes
- [Linear-style issue waves](../docs/linear-orchestration.md) for tracker-driven campaigns

See [Demo Gallery](../docs/demo-gallery.md) for the descriptive companion to
this index, and [Workflow Blueprints](../docs/workflows.md) when you are ready
to pick the next workflow scale.
