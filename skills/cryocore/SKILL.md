---
name: cryocore
description: Use when planning or executing BioSymphony CryoCore campaigns for cryo-EM raw processing, map/model validation, heterogeneity review, structural rendering, and provider-neutral cryo workflows.
---

# CryoCore

Use this skill for CryoCore work. In a full CryoCore checkout, run repository
commands from the repo root. In a standalone skill install, read the bundled
files under `references/`.

## Local Memory

Read every Markdown note under `.cryocore-memory/` if the folder exists, before
the always-read docs below. These are durable lessons captured by past agents
on this user's machine: install gotchas, validator quirks, provider edge
cases, doctrine corrections the user already confirmed. Treat them as
agent-process guidance, not as biology evidence or claim closeout.

The folder is gitignored. It must never travel upstream. Memory is for
cross-campaign behavior change; the claim ledger and closeout artifacts remain
the audit trail for any specific run.

When you encounter something the next agent should know, append a note at
`.cryocore-memory/YYYY-MM-DD-<slug>.md` using the shape in
`references/memory-note-template.md`. Never put secrets,
private paths, campaign-specific data, raw sequences, provider identifiers,
signed URLs, or large outputs into a memory note.

## Always Read

- `references/AGENTS.md`
- `references/README.md`
- `references/public-quickstart.md`
- `references/goal-orchestration.md`
- `references/claim-levels.md`
- `references/split-evaluation.md`
- `references/tooling-and-licensing.md`

## Freshness Check

Before relying on `references/tooling-and-licensing.md`, `references/software-registry.yaml`,
or any other posture record, check the dates. Policy docs carry `Last reviewed:`
lines; the bundled source-backed audit is `references/toolwatch-2026-06-21.md`.
In a full CryoCore checkout, run `make tooling-freshness-check` to confirm both
are within the configured window (default 120 days). If either is stale, refresh through the
`cryocore-toolwatch` skill before treating posture as current. Posture records
age silently; tool versions, license terms, and upstream APIs do not.

## Mode Routing

- `docs_or_planning`: docs, manifests, modules, issue plans. No paid compute.
- `local_prep`: validators, examples, launch packets, no remote execution.
- `paid_provider_run`: RunPod, cloud, SSH/HPC, raw download, or gated runtime execution. Requires explicit operator gate, budget, artifact fetch/hash, and cleanup.
- `scientific_closeout`: final claims. Requires provenance, validation, artifact hashes, and claim downgrade when evidence is incomplete.

## Specialized Repo Skills

- `cryocore-toolwatch`: tool, preprint, API, workflow, and license audits.
- `cryocore-public-safety`: public release, privacy, and security review.
- `cryocore-run-closeout`: provider/run closeout and no-false-success checks.
- `cryocore-map-model-dossier`: public-safe EMDB/PDB map-model dossiers.
- `cryocore-heterogeneity-jury`: state/ensemble/heterogeneity planning and review.
- `cryocore-figure-dossier`: reproducible figure and renderer dossiers.

## Request Routing

| User asks for | Read next |
| --- | --- |
| Public release readiness, privacy, secrets, or security | `cryocore-public-safety` |
| RunPod closeout, provider artifacts, cost, cleanup, or false success | `cryocore-run-closeout` |
| EMDB/PDB map-model evidence, validation, or dossier planning | `cryocore-map-model-dossier` |
| Tool, license, version, or literature watch | `cryocore-toolwatch` |
| Figure manifest, visual evidence, or renderer route | `cryocore-figure-dossier` |
| Heterogeneity, state assignment, ensembles, or conformational jury | `cryocore-heterogeneity-jury` |

## Hard Rules

- No raw movies, maps, half-maps, model weights, private data, secrets, or license files in git.
- ChimeraX is runtime-gated and duplicated with Structure Factory by design.
- Experimental evidence outranks prediction/design output.
- Scientific success requires fetched artifacts, hashes, validation outputs, cost records, cleanup proof, and a claim ledger joined to the declared inputs.
- Missing optional renderers should block only renderer lanes.

## Local Checks

In a full CryoCore checkout:

```bash
make preflight
make goal-brief-check
make registry-check
make module-check
make runpod-check
make issue-check
make contract-self-check
make release-check
```
