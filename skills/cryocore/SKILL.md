---
name: cryocore
description: Use when planning or executing BioSymphony CryoCore campaigns for cryo-EM raw processing, map/model validation, heterogeneity review, structural rendering, and provider-neutral cryo workflows.
---

# CryoCore

Use this repo-local skill for CryoCore work in the current
`biosymphony-cryocore-public` checkout.

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
`skills/cryocore/references/memory-note-template.md`. Never put secrets,
private paths, campaign-specific data, raw sequences, provider identifiers,
signed URLs, or large outputs into a memory note.

## Always Read

- `AGENTS.md`
- `README.md`
- `docs/public-quickstart.md`
- `docs/goal-orchestration.md`
- `docs/claim-levels.md`
- `docs/split-evaluation.md`
- `docs/tooling-and-licensing.md`

## Freshness Check

Before relying on `docs/tooling-and-licensing.md`, `references/software-registry.yaml`,
or any other posture record, check the dates. Policy docs carry `Last reviewed:`
lines; the current source-backed audit lives at `docs/toolwatch-YYYY-MM-DD.md`.
Run `make tooling-freshness-check` to confirm both are within the configured
window (default 120 days). If either is stale, refresh through the
`cryocore-toolwatch` skill before treating posture as current. Posture records
age silently; tool versions, license terms, and upstream APIs do not.

## Mode Routing

- `docs_or_planning`: docs, manifests, modules, issue plans. No paid compute.
- `local_prep`: validators, examples, launch packets, no remote execution.
- `paid_provider_run`: RunPod, cloud, SSH/HPC, raw download, or gated runtime execution. Requires explicit operator gate, budget, artifact fetch/hash, and cleanup.
- `scientific_closeout`: final claims. Requires provenance, validation, artifact hashes, and claim downgrade when evidence is incomplete.

## Specialized Repo Skills

- `skills/cryocore-toolwatch/SKILL.md`: tool, preprint, API, workflow, and license audits.
- `skills/cryocore-public-safety/SKILL.md`: public release, privacy, and security review.
- `skills/cryocore-run-closeout/SKILL.md`: provider/run closeout and no-false-success checks.
- `skills/cryocore-map-model-dossier/SKILL.md`: public-safe EMDB/PDB map-model dossiers.
- `skills/cryocore-heterogeneity-jury/SKILL.md`: state/ensemble/heterogeneity planning and review.
- `skills/cryocore-figure-dossier/SKILL.md`: reproducible figure and renderer dossiers.

## Request Routing

| User asks for | Read next |
| --- | --- |
| Public release readiness, privacy, secrets, or security | `skills/cryocore-public-safety/SKILL.md` |
| RunPod closeout, provider artifacts, cost, cleanup, or false success | `skills/cryocore-run-closeout/SKILL.md` |
| EMDB/PDB map-model evidence, validation, or dossier planning | `skills/cryocore-map-model-dossier/SKILL.md` |
| Tool, license, version, or literature watch | `skills/cryocore-toolwatch/SKILL.md` |
| Figure manifest, visual evidence, or renderer route | `skills/cryocore-figure-dossier/SKILL.md` |
| Heterogeneity, state assignment, ensembles, or conformational jury | `skills/cryocore-heterogeneity-jury/SKILL.md` |

## Hard Rules

- No raw movies, maps, half-maps, model weights, private data, secrets, or license files in git.
- ChimeraX is runtime-gated and duplicated with Structure Factory by design.
- Experimental evidence outranks prediction/design output.
- Scientific success requires fetched artifacts, hashes, validation outputs, cost records, cleanup proof, and a claim ledger joined to the declared inputs.
- Missing optional renderers should block only renderer lanes.

## Local Checks

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
