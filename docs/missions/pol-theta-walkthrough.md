# Pol Theta Walkthrough

A narrative end-to-end mission, written so a newcomer can see how a CryoCore
mission actually unfolds from a broad goal to a reviewable dossier. The
walkthrough uses the Pol Theta helicase deposit (EMDB `EMD-43816`, PDB `9ASJ`)
and a single coding agent driving the work.

![Mission arc](../assets/mission-arc.svg)

The matching artifacts are committed in:

- [examples/sample-goal-brief/](../../examples/sample-goal-brief/) (filled-out goal brief)
- [examples/sample-linear-wave/](../../examples/sample-linear-wave/) (first wave of issues)
- [demos/poltheta-map-model-dossier/](../../demos/poltheta-map-model-dossier/) (the demo itself)

## The starting goal

The user opens the agent and types:

> Produce a publishable dossier for the human Pol Theta helicase domain using
> the public EMDB and PDB deposits. Stay in prep mode for now.

That sentence is the whole input. No accessions, no commands, no schema.

## Step 1. Orient

The agent reads the repo entry points before anything else: [AGENTS.md](../../AGENTS.md),
[README.md](../../README.md), and the [Glossary](../glossary.md). It learns
two things: CryoCore expects evidence work to bundle into a dossier, and the
domain vocabulary names what a deposit actually contains (map, model,
half-maps, validation report, FSC, B-factor).

Because the goal is broad, the agent reaches for [Goal Orchestration](../goal-orchestration.md)
and the [goal brief template](../../templates/goal-brief.md).

## Step 2. Fill the goal brief

The agent identifies the accessions from the user's wording and produces a
goal brief. The committed example is at
[examples/sample-goal-brief/goal-brief.md](../../examples/sample-goal-brief/goal-brief.md).
Highlights:

- Public accessions are named: EMDB `EMD-43816`, PDB `9ASJ`.
- Resource mode is `public_metadata_network`.
- Claim ceiling is `processed`. Mechanism, ligand-action, and therapeutic claims stay out.
- The first artifact is the prep-check log.
- Operator gates are listed for the future paid run.

The brief is small. A capable agent can produce it in one pass after reading
the template.

## Step 3. Decide on single-agent or wave

The brief sits at a fork. The agent could run the prep check itself in a
single session, or split the work into a tracker-driven wave.

The agent chooses to split. Reasons:

- Each step has a clear artifact (audit, manifest, prep check).
- The wave shape teaches the user the contract style for future missions.
- A bounded wave makes it easy to hand later issues to another worker.

## Step 4. Draft the first wave

Using the [Linear Wave Planning prompt](../../examples/agent-tasks/linear-wave-planning.prompt.md),
the agent produces three issues. The committed examples are under
[examples/sample-linear-wave/](../../examples/sample-linear-wave/):

| Issue | What it does |
| --- | --- |
| [CRYOCORE-W1-01](../../examples/sample-linear-wave/issue-01-audit-accessions.md) | Audit public accessions; produce `.runtime/public-accession-metadata.json`. |
| [CRYOCORE-W1-02](../../examples/sample-linear-wave/issue-02-prep-runpod-manifest.md) | Validate the RunPod bridge manifest against scope and reference checks. |
| [CRYOCORE-W1-03](../../examples/sample-linear-wave/issue-03-run-prep-check.md) | Run `make demo-poltheta-prep-check`, then `make contract-self-check`. |

Future paid execution stays in Backlog. The wave makes that explicit.

## Step 5. Run the wave

The agent (or three parallel workers in a multi-agent harness) executes the
issues in dependency order. After each issue, the worker appends a final
outcome block to the issue body, names the artifacts produced, and reports
the validation command output.

The wave passes when issue three closes with a green contract-self-check.

## Step 6. Inspect the dossier

The dossier lives under `.runtime/poltheta-map-model-remote/` after a full run.
A static sample of the shape is in
[examples/t2r14-open-dossier-preview/](../../examples/t2r14-open-dossier-preview/)
for the T2R14 variant; the Pol Theta dossier follows the same contract under
[modules/artifact-contracts/structure-dossier.v1.json](../../modules/artifact-contracts/structure-dossier.v1.json).

What the human reviewer reads:

- `report.html` for the narrative summary, figures, and methods.
- `claim_ledger.md` for the claim ceiling and caveats.
- `validation-summary.json` for the wwPDB validation rollup.
- `dossier_manifest.json` for the machine-readable inputs, artifacts, and provenance.

## Step 7. Close the mission

The mission closes one of two ways:

- **Stays in prep mode.** The wave's third issue ships a green contract-self-check, the dossier shape is committed, and the operator opens or declines the paid-launch gate at their own pace.
- **Escalates to a real run.** The operator authorizes paid GPU time, real-mode artifacts are required, and a second wave runs the actual RunPod launch and the [provider run review](../use-cases.md#2-provider-run-review).

In both cases, the agent appends a final outcome block to the calling issue
or thread so the human reviewer has one place to read what happened.

## What the user actually did

Count the moments the user typed something:

1. The starting goal sentence at Step 1.
2. A review pass on the goal brief at Step 2.
3. An approval or correction on the wave plan at Step 4.
4. A review of the dossier at Step 6.
5. A decision at Step 7 about whether to authorize a paid run.

Five touches. The agent did the rest, leaning on the skill pack, the schemas,
and the validators that ship in this repo.

## Adapting this walkthrough

Swap the accessions and most of the brief still applies. The skill pack is
target-agnostic. To run a different mission, pick one of the entries in the
[Mission Catalog](../mission-catalog.md) and follow the same six steps.
