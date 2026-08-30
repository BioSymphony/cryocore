# Tour

A guided walk through the repo. About fifteen minutes if you run every step.
About three minutes if you read along. You can do this yourself, or paste the
prompt at the bottom into your agent and have it walk you through.

## Step 1. Review the core files

Start with three files at the repository root:

- [README.md](../README.md): overview, capability table, agent prompt, and harness patterns.
- [AGENTS.md](../AGENTS.md): operating rules, required validators, and repository exclusions.
- [docs/glossary.md](glossary.md): cryo-EM vocabulary, tools, and CryoCore orchestration terms.

If you are new to cryo-EM, start with the glossary sections "Cryo-EM
Vocabulary" and "Cryo-EM Tools At A Glance."

## Step 2. Run the smallest demo

From the repo root:

```bash
python3 -m pip install -r requirements-dev.txt
make demo-local
```

That fetches public RCSB metadata and the PDB mmCIF coordinate file for the
T2R14 receptor complex (PDB `9W0Q`, EMDB `EMD-65512`). It does not download
the EMDB map. The demo computes chain and ligand summaries, renders SVG
figures, and writes a review package under ignored `.runtime/`.

The demo runs in about a minute on a laptop CPU.

## Step 3. Inspect the output

Open the headline artifacts:

```bash
ls .runtime/t2r14-open-dossier/artifacts/
```

Inspect these files first:

- `report.html`: the human-readable review. Open it in a browser to see inputs, figures, and methods together.
- `claim_ledger.md`: what the evidence supports and where claims have to stop.
- `dossier_manifest.json`: machine-readable inputs, artifacts, provenance, and review state.

A static sample is committed at
[examples/t2r14-open-dossier-preview/](../examples/t2r14-open-dossier-preview/)
if you want to see the shape before running anything.

## Step 4. See the release gate

```bash
make release-check
```

This runs the tests, public-release report, secret scan, and contract
validators. A green result means the local content gates passed. Complete the
[Public Switch Checklist](public-switch-checklist.md) and the
`--publish-ready` check before publishing.

The individual checks are listed in
[docs/validation-command-matrix.md](validation-command-matrix.md) when you
want a smaller, faster iteration loop.

## Step 5. Read one skill

An agent loads the skill pack when it works in this repository.

```bash
ls skills/
cat skills/cryocore/SKILL.md
```

Each skill has a `SKILL.md` (the human and agent-readable spec) and an `agents/`
directory with harness-specific configuration. [skills/README.md](../skills/README.md)
has a "Use When" table mapping each skill to the trigger that pulls it in.

## Step 6. Point your agent at the repo

Copy the block in the README's [Agent Prompt](../README.md#agent-prompt)
section. Then give the agent a goal in plain English. For example:

- "Build a public-accession map/model review for EMDB `EMD-43816` and PDB `9ASJ`."
- "Review the artifact evidence for a hypothetical Pol Theta run on RunPod."
- "Draft a Linear-style issue wave for a four-stage map-to-model campaign."

The agent reads `AGENTS.md`, picks the relevant skill, runs the validators, and
returns a review output or wave plan you can inspect.

## Where to go next

| Track | Start here |
| --- | --- |
| Run the other two demos | [Pol Theta](../demos/poltheta-map-model-dossier/), [Structure Jury](../demos/structure-jury-dual-dossier/) |
| Choose a workflow scale | [Workflow Blueprints](workflows.md) |
| Set up an agent harness | [Agent Quickstart](agent-quickstart.md) |
| Plan a Linear-style wave | [Tracker Orchestration](linear-orchestration.md) |
| Prepare a cloud or HPC lane | [Compute Backends](compute-backends.md), [Provider Readiness](provider-readiness.md) |
| Reuse the skill pack in another repo | [Adoption Guide](adoption-guide.md), [Skill Installation](skill-installation.md) |
| Browse copyable workflows | [Recipes](recipes/README.md) |

## Tour prompt for your agent

Paste this into your coding agent to have it walk you through the tour:

```text
Use the CryoCore tour. Read docs/tour.md and follow each step in order. Run the
commands locally where the tour calls for them, summarize the result of each
step, and stop at any gate that asks for operator authorization. Report which
artifacts appeared, which validators passed, and which next track from the
table is the smallest applicable next step.
```
