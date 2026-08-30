# BioSymphony CryoCore

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Release check](https://img.shields.io/badge/release%20check-make%20release--check-informational.svg)](#five-minute-start)
[![Status: pre-alpha](https://img.shields.io/badge/status-pre--alpha-orange.svg)](#status)

**A cryo-EM skill pack for agents that plan, validate, and review structural workflows.**

![BioSymphony CryoCore banner](docs/assets/cryocore-banner.jpg)

CryoCore gives coding agents a control layer for cryo-EM work. An
agent can choose a workflow, organize declared inputs and outputs, prepare
figures, compare structures, and assemble local or operator-gated provider
packets.

The repository supplies skill instructions, prompt fixtures, JSON Schema
contracts, tool-posture records, provider templates, and local validators.
Public checks validate contracts. They do not launch providers or package
gated tools. Keep raw data, maps, private structures, model weights, license
files, credentials, and heavy outputs outside this repository.

![CryoCore at a glance: inputs become contracts, pass execution gates, and end as bounded review outputs](docs/assets/cryocore-overview.svg)

## How It Works

Point your agent at this repository and give it a cryo-EM goal. The agent reads
[AGENTS.md](AGENTS.md), the relevant skill under [skills/](skills/), and the
schemas under [modules/schemas/](modules/schemas/). It can fetch
public-accession metadata when the workflow calls for it, inspect map/model
inputs, draft figure plans, compare states, prepare provider packets, and return
a review package with methods, provenance, artifacts, caveats, and next steps.

You remain responsible for the goal, approvals, and output review. Human
authorization is required for paid GPU time, license acceptance, raw-data
access, and claim escalation. Provider execution remains operator-owned.

## Capabilities

| Capability | Output |
| --- | --- |
| Map/model and density review | Give an agent public accession IDs or operator-declared artifacts and receive summaries of the available maps, models, fit metrics, caveats, and follow-up work. Missing artifacts remain explicit in the claim ledger. |
| Figure and state workflows | Prepare reproducible structural figures, renderer routes, comparison axes, and heterogeneity or conformational-state review plans. |
| Cryo-EM tool routing | RELION, MotionCor3, Warp/M, Topaz, cryoDRGN, ModelAngelo, Coot, Phenix, ChimeraX, Mol*, PyMOL, and related tools stay mapped to lanes, licenses, and runtime boundaries. |
| Provider-neutral preparation | RunPod, AWS Batch, SSH/HPC, neocloud, generic cloud VM, and local workstation profiles use the same stage contracts, launch preparation, and budget and cleanup gates. |
| Works with different agent harnesses | Single-agent terminals, tracker-driven workers, and custom orchestration can use the same skills, schemas, and validators. |
| Handoff layer for agent work | Artifacts, hashes, checker outputs, cost records, cleanup proof, provenance, and claim boundaries are recorded before a result is treated as complete. |

Lane modules describe stages from raw movies through figures and state review.
Schemas, ledgers, and validators preserve inputs, artifacts, hashes,
provenance, cost records, cleanup proof, and claim boundaries for handoff.
Every tool routes through one of three license lanes:

![Tool lane routing: open, watch, and runtime-gated lanes by license posture](docs/assets/tool-lane-routing.svg)

See [Workflow Blueprints](docs/workflows.md) for how to choose a path,
[Goal Orchestration](docs/goal-orchestration.md) for `/goal`-style agent setup,
and [Use Cases](docs/use-cases.md) for copyable prompts.

## Choose Your Path

| I am... | Start here | First command |
| --- | --- | --- |
| New to CryoCore | [Public Quickstart](docs/public-quickstart.md) | `make demo-local` |
| Want a guided walk-through | [Tour](docs/tour.md) | `make demo-local` |
| Pointing an agent at the repo | [Agent Quickstart](docs/agent-quickstart.md) | `make skill-check` |
| Turning a broad goal into work | [Goal Orchestration](docs/goal-orchestration.md) | `make goal-brief-check` |
| Choosing a workflow | [Workflow Blueprints](docs/workflows.md) | `make docs-link-check` |
| Reusing patterns elsewhere | [Adoption Guide](docs/adoption-guide.md) | `make docs-link-check` |
| Preparing cloud resources | [Compute Backends](docs/compute-backends.md) | `make provider-check` |
| Planning Linear issue waves | [Tracker Orchestration](docs/linear-orchestration.md) | `make issue-check` |
| Checking a provider run | [Provider Run Review](docs/use-cases.md#2-provider-run-review) | `make provider-closeout-check` |
| Preparing a public switch | [Public Release](PUBLIC_RELEASE.md) | `make release-check` |

## Workflow Chooser

The `Claim ceiling` column uses CryoCore's claim ladder. See
[Claim Levels](docs/claim-levels.md) for what `candidate`, `processed`,
`validated`, and `publishable` mean.

| Starting point | Goal | First command | Side effects | Expected output | Claim ceiling |
| --- | --- | --- | --- | --- | --- |
| New checkout | See the repo work | `make demo-local` | public RCSB/mmCIF fetch, writes `.runtime/` | HTML report, figures, manifest, claim boundaries | `processed` demo evidence |
| EMDB/PDB IDs | Plan or build a map/model review | [Map/Model Dossier](docs/recipes/map-model-dossier.md) | public metadata/artifact fetch only when commanded | input audit, summaries, figures, provenance, caveats | `processed` or `candidate` |
| Cloud/HPC idea | Prepare provider work | `make provider-check` | no provider mutation | provider profile, gates, launch-request plan | `candidate` until artifacts are joined |
| Linear campaign | Split work for agents | `make issue-check` | no network or provider mutation | issue DAG, dependencies, labels | `candidate` |
| Fetched run artifacts | Decide if a run is complete | `make provider-closeout-check` | local fixture check only | blockers, hashes, cost, cleanup, claim level | artifact-dependent |
| Public switch | Check publishability | `make release-check` | local checks and secret scan | release report and blockers | repo readiness only |

## Five-Minute Start

Install the development requirements, then run the local demo:

```bash
python3 -m pip install -r requirements-dev.txt
make demo-local
```

This fetches public RCSB/mmCIF data and writes the output under ignored
`.runtime/`. Raw movies, maps, half-maps, model weights, private data, license
files, and gated tools stay outside the demo.

Then inspect:

- `.runtime/t2r14-open-dossier/artifacts/report.html`
- `.runtime/t2r14-open-dossier/artifacts/claim_ledger.md`
- `.runtime/t2r14-open-dossier/artifacts/dossier_manifest.json`

What the first run gives you:

| Artifact | Why it matters |
| --- | --- |
| `report.html` | A human-readable review page with public inputs, figures, and methods. |
| `claim_ledger.md` | Claim boundaries and caveats, so an agent cannot turn a summary into unsupported mechanism claims. |
| `dossier_manifest.json` | Machine-readable inputs, artifacts, provenance, and review state. |
| `runpod-execution.tar.gz` | Portable artifact bundle shape used later by provider review. |

To inspect an example without running the demo, open
[T2R14 Open Dossier Preview](examples/t2r14-open-dossier-preview/).

![T2R14 dossier shape: input audit, then dossier artifacts, then claim boundary](docs/assets/demo-gallery/t2r14-preview.svg)

Expected success looks like:

```json
{
  "ok": true,
  "run_id": "cryocore-demo-t2r14-open-dossier"
}
```

Run the local public release gate:

```bash
make release-check
```

Prefer explicit commands?

```bash
python3 scripts/cryocore/t2r14_open_dossier.py --out .runtime/t2r14-open-dossier --json
python3 -m json.tool .runtime/t2r14-open-dossier/status.json
```

## Agent Prompt

Paste this into your coding agent from the repository root. This is the
canonical prompt. [docs/agent-quickstart.md](docs/agent-quickstart.md) uses the
same prompt.

```text
Use the CryoCore skill pack in this repo. Stay local. Read AGENTS.md,
README.md, docs/goal-orchestration.md, docs/workflows.md, docs/use-cases.md,
and the relevant skill under skills/. Build a claim-bounded cryo-EM map/model review,
figure workflow, state comparison, provider plan, or artifact package. Keep
private data, secrets, raw or heavy artifacts, provider logs, model weights,
and license files out of git and public outputs. Run the smallest relevant
checks first, then `make release-check` for release-readiness tasks.
Report exact artifacts, claim levels, check results, and remaining issues.
```

More agent patterns are in [Agent Quickstart](docs/agent-quickstart.md) and
[Agent Task Prompts](examples/agent-tasks/).

Copying this into another repo? Start with [Adoption Guide](docs/adoption-guide.md).

## Using CryoCore With Your Agents

![Harness compatibility](docs/assets/harness-patterns.svg)

CryoCore is designed so different agent stacks can drive the same public
contracts. Example integration patterns:

| Pattern | How it runs | Where to start |
| --- | --- | --- |
| Symphony with agent workers | Symphony dispatches bounded workers against tracker issues. Each worker reads the relevant CryoCore skill and reports an outcome block. | [templates/symphony-cryocore.WORKFLOW.md](templates/symphony-cryocore.WORKFLOW.md), [docs/linear-orchestration.md](docs/linear-orchestration.md) |
| Tracker-managed workers | A tracker holds the campaign graph and labels while compatible workers read the skill pack and produce review-ready artifacts. | [templates/linear-issue.md](templates/linear-issue.md), [docs/agent-quickstart.md](docs/agent-quickstart.md) |
| Terminal agent | One agent reads `AGENTS.md`, the chosen skill, and the relevant validators, then drives a bounded mission. | [Agent Prompt](#agent-prompt), [skills/](skills/) |
| Your own orchestration | Every contract is plain JSON Schema or Markdown. Wire CryoCore into the orchestration you already run. | [docs/agent-skill-guide.md](docs/agent-skill-guide.md), [modules/schemas/](modules/schemas/) |

The skill pack supports a bounded local task, a staged multi-issue
campaign, and operator-gated cloud or HPC work with provider-neutral contracts
and artifact evidence.

Local and remote workflows use the same contracts:

![Local or cloud, same shape](docs/assets/local-or-cloud-topology.svg)

- Laptop or workstation: public-accession demos, CPU-only checks, claim-boundary drafts.
- RunPod, AWS Batch, SSH/HPC, neocloud VMs: launch manifests, stage contracts, fetched-artifact reports, cost and cleanup proof.
- Mixed: plan and validate locally, then hand the same campaign to cloud workers when GPU time is ready.

## Install Model

Use CryoCore as a source checkout. Clone or copy it, install
`requirements-dev.txt`, and run `make` targets or `python3
scripts/cryocore/*.py` commands from the repository root. A pip-installable
package is on the roadmap.

## Core Workflow

Each mission follows these steps. The agent performs the work, and the operator
approves gated actions.

![Mission arc: user goal, goal brief, wave plan, execution, review output, with the human and agent roles at each step](docs/assets/mission-arc.svg)

In detail, each mission:

1. Declares public accessions or operator-provided inputs.
2. Audits inputs and data boundaries before work starts.
3. Inspects maps, models, density support, states, or figure needs.
4. Routes tools through open, watch, or runtime-gated lanes.
5. Tracks stage progress, artifacts, hashes, cost, cleanup, and claim level.
6. Emits a review output with figures, methods, provenance, caveats, and next steps.

The same shape works at three scales:

- local: small public demos and validators only
- cloud: operator-gated RunPod, AWS, SSH/HPC, or compatible provider contracts
- tracker: Linear-style issue waves with explicit dependencies and review gates

Use [Workflow Blueprints](docs/workflows.md) to pick the right scale before
dispatching work.

CryoCore separates experimental cryo-EM processing from AI design runtimes. The
design side can consume CryoCore outputs while RELION, Warp/M, MotionCor,
ModelAngelo, ChimeraX, Coot, and validation tooling keep their own images and
dependency surfaces apart from RFdiffusion, Boltz, Chai, ProteinMPNN, and
screening stacks.

## Handoff Layer

CryoCore records the following information for multi-day work and human review:

- the public accession, operator dataset, or derived artifact used as input
- the tool lane that was planned, gated, or executed
- the completed stage
- the artifacts that were produced and hashed
- the licenses or use-context approvals required
- the claims or next steps supported by the artifacts

A stage becomes trustworthy when the artifacts are joined to the declared
inputs and the check outputs, checksums, cost records, cleanup proof, and
claim boundaries are all in place.

The shape of one mission, at a glance:

```text
   public accessions               operator data
        |                                |
        +----------------+---------------+
                         |
                         v
   +-------------------------------------------+
   |  input audit and resource mode            |
   +---------------------+---------------------+
                         |
                         v
   +-------------------------------------------+
   |  tool lane: open, watch, runtime-gated    |
   +---------------------+---------------------+
                         |
                         v
   +-------------------------------------------+
   |  stage: prep mode or real mode            |
   +---------------------+---------------------+
                         |
                         v
   +-------------------------------------------+
   |  artifacts + hashes + cost records        |
   +---------------------+---------------------+
                         |
                         v
   +-------------------------------------------+
   |  checks: schemas, contract self-check,    |
   |  wwPDB rollup                             |
   +---------------------+---------------------+
                         |
                         v
   +-------------------------------------------+
   |  review output: figures, caveats,         |
   |  claim boundaries, next steps             |
   +-------------------------------------------+
```

## Repository Layout

![Repo layout](docs/assets/repo-layout-tree.svg)

<details>
<summary>Full file listing</summary>

```text
campaigns/        CryoCore campaign contracts
containers/       Public image posture and runtime separation notes
demos/            Public cryo demos and review readouts
docs/             Durable architecture, split, licensing, and data-policy docs
examples/         Tiny example manifests
modules/          Image, lane, and provider contracts
references/       Machine-readable tool registry
scripts/cryocore/ Validators and local utilities
skills/cryocore/  Repo-local skill instructions
templates/        Tracker issue and operator-gate templates
tests/            Lightweight validator tests
```

</details>

## Key Assets

- `modules/lane-modules/raw-to-map.v1.json`, `map-to-model.v1.json`, and `figure-dossier.v1.json`: scientific lane shapes for processing, model review, and figures.
- `scripts/cryocore/t2r14_open_dossier.py`, `poltheta_map_model_dossier.py`, and `structure_jury_dossier.py`: runnable public-accession review demos.
- `modules/schemas/`: provider-run, workflow-run, claim-ledger, figure-manifest, map-model-fit, artifact-index, cost, cleanup, and accession metadata schemas.
- `modules/artifact-contracts/structure-dossier.v1.json`: claim-level ladder and required artifacts.
- `runpod/stage-contracts/`: stage contracts with progress-ledger requirements that close only when each stage is confirmed.
- `scripts/cryocore/provider_closeout_check.py`: confirms artifacts, hashes, cost records, and cleanup proof are all in place before a provider run is treated as complete.
- `scripts/cryocore/contract_self_check.py`: checks that real provider results are backed by real artifacts rather than mocks, fixtures, planned-only entries, or fallbacks.
- `scripts/cryocore/public_snapshot_check.py`: scans a public snapshot for secrets, heavy cryo-EM artifacts, local paths, and private execution markers.
- `scripts/cryocore/runpod_scope_check.py`: scans public bridge manifests, inline source bundles, public service scope, and prep-only gates.
- `scripts/cryocore/runpod_reference_check.py`: confirms that public entrypoints exist and resume commands match the checked-in files.
- `docs/agent-skill-guide.md` and `docs/prompt-library.md`: agent workflows and reusable prompt patterns.
- `docs/workflows.md`: workflow selector for public accessions, agents, cloud resources, Linear issue waves, and provider review.
- `skills/cryocore-public-safety/SKILL.md`: public-release review for privacy, secrets, provider risk, and claims.
- `docs/recipes/README.md`: copyable workflows for release checks, metadata ledgers, demo runs, provider prep, and provider run review.
- `docs/validation-command-matrix.md` and `docs/failure-modes.md`: command selection and post-run review of stage outcomes.
- `references/software-registry.yaml`: machine-readable tool posture across open, watch, and runtime-gated cryo-EM tools.

## Boundary With Structure Factory

![CryoCore and Structure Factory boundary](docs/assets/cryocore-sf-boundary.svg)

CryoCore owns experimental cryo-EM processing and structural review. Structure Factory owns cross-lane orchestration, prediction/design, screening, and campaign synthesis.

The two repos intentionally duplicate a small set of shared posture records. ChimeraX is the clearest example: it belongs in CryoCore for map/model inspection and figure rendering, and it belongs in Structure Factory for design and atlas reports. Duplicating these records lets each repo keep a focused scientific runtime.

See [Split Evaluation](docs/split-evaluation.md) and
[Move/Duplicate Map](docs/move-duplicate-map.md).

## Related Projects

- [Proteus](https://github.com/jvogan/proteus): structural-biology skills for AI coding agents, including PyMOL and ChimeraX automation plus AlphaFold DB, RCSB PDB, UniProt, and Rosetta workflows. Pairs well with CryoCore when a mission needs hands-on molecular visualization or sequence/structure lookups alongside cryo-EM map/model review.

## Public Demos

- [T2R14 Open Dossier](demos/t2r14-open-dossier/): CPU-only public PDB/EMDB metadata and coordinate review.
- [Pol Theta Map/Model Dossier](demos/poltheta-map-model-dossier/): public EMDB/PDB/wwPDB validation review shape for a map/model lane.
- [Dual Structure Comparison](demos/structure-jury-dual-dossier/): joins two public deposited-structure lanes into one review package.

Demo launch manifests are public scaffolds for the prep stage. An operator must
initiate paid provider execution and keep credentials outside the repository.
Review provider results against fetched and hashed artifacts.

## Quickstart

The fastest path is [Public Quickstart](docs/public-quickstart.md). The
agent-first path is [Agent Quickstart](docs/agent-quickstart.md).

## Current Toolwatch

See [Toolwatch 2026-08-30](docs/toolwatch-2026-08-30.md) for the latest
source-backed tool and repository audit. The [July](docs/toolwatch-2026-07-05.md),
[June](docs/toolwatch-2026-06-21.md), and [May](docs/toolwatch-2026-05-27.md)
notes remain as historical context. See
[Workflow Orchestration Provenance](docs/workflow-orchestration-provenance.md)
and [Public Accession APIs](docs/public-accession-apis.md) for the recommended
provenance and metadata-helper direction.

## Local Commands

The menu your agent has available. Each command is read-only on local files
unless noted in the linked docs. You can run any of them directly to verify
what the agent is doing.

```bash
python3 scripts/cryocore/preflight.py --repo-root . --json
python3 scripts/cryocore/software_registry_check.py references/software-registry.yaml --json
python3 scripts/cryocore/fetch_public_accession_metadata.py --emdb EMD-43816 --pdb 9ASJ --out .runtime/public-accession-metadata.json
make module-check
make runpod-check
make runpod-scope-check
make issue-check
make contract-self-check
make release-check
```

All commands above run locally. They validate contracts, query public accession
APIs when invoked, and write any output to ignored `.runtime/`. Provider
dispatch, raw-data downloads, gated software installs, and GPU workloads are
operator-initiated steps documented separately. See
[Data Policy](docs/data-policy.md).

Run the public release gate:

```bash
make release-check
```

## Status

Pre-alpha public release. CryoCore supports agent-guided map/model
review on public accessions, figure and state workflow planning, provider
preflight, contract validation, provider-run review templates and fixtures,
Linear-style campaign planning, tool and license posture tracking, and
claim-bounded structural evidence packets. The CPU-only T2R14 demo runs end to
end on a laptop. Paid provider lanes ship as prep-mode contracts that an
operator executes outside the public repository. The contracts preserve the
approvals and evidence required for workflows that use paid GPU compute, gated
scientific tools, or heavy artifacts.

## Documentation Map

- [Tour](docs/tour.md): fifteen-minute guided walk through the repo, with a paste-into-agent prompt at the end.
- [Public Quickstart](docs/public-quickstart.md): first commands and demo outputs.
- [Demos](demos/README.md): one local public demo plus two operator-owned workflow preparations.
- [Mission Catalog](docs/mission-catalog.md): menu of seed missions an agent can take on, sorted from smallest to largest.
- [Pol Theta Walkthrough](docs/missions/pol-theta-walkthrough.md): narrative end-to-end mission from broad goal to map/model review.
- [Agent Quickstart](docs/agent-quickstart.md): copy-paste agent prompt and routing.
- [Workflow Blueprints](docs/workflows.md): choose public-accession, agent, cloud, Linear, or run-review paths.
- [Use Cases](docs/use-cases.md): common workflows and copyable prompts.
- [Adoption Guide](docs/adoption-guide.md): how to reuse CryoCore patterns elsewhere.
- [Local Installation](docs/local-installation.md): source-checkout install model.
- [Agent Skill Guide](docs/agent-skill-guide.md): using this repo as a public skill pack.
- [Skill Installation](docs/skill-installation.md): using or copying the skill pack locally.
- [Recipes](docs/recipes/README.md): copyable workflow recipes.
- [Validation Command Matrix](docs/validation-command-matrix.md): validator selection and command side effects.
- [Failure Modes](docs/failure-modes.md): triage guide for stage outcomes, privacy issues, and provider-risk situations.
- [Prompt Library](docs/prompt-library.md): prompt patterns for agents and reviewers.
- [Demo Gallery](docs/demo-gallery.md): demo scope, artifacts, and claim boundaries.
- [Data Policy](docs/data-policy.md): data tiers and git boundaries.
- [Provider Execution Model](docs/provider-execution-model.md): provider launch, evidence, and artifact-review model.
- [Compute Backends](docs/compute-backends.md), [Provider Readiness](docs/provider-readiness.md), and [Tracker Orchestration](docs/linear-orchestration.md): cloud-resource and Linear-style campaign workflow.
- [Claim Levels](docs/claim-levels.md): claim ladder and downgrade triggers.
- [Schema Catalog](docs/schema-catalog.md) and [Module Catalog](docs/module-catalog.md): contract inventory.
- [Privacy Threat Model](docs/privacy-threat-model.md): privacy and release-risk controls.
- [Troubleshooting](docs/troubleshooting.md): common validation failures.
- [Public Switch Checklist](docs/public-switch-checklist.md): local-to-public publishing checklist.
- [Glossary](docs/glossary.md): cryo-EM and CryoCore terminology.
- [FAQ](FAQ.md) and [Roadmap](ROADMAP.md): community orientation and next milestones.
- [Governance](GOVERNANCE.md) and [Maintainers](MAINTAINERS.md): review and release ownership.
- [Agent Task Prompts](examples/agent-tasks/README.md): prompt fixtures for agents.
