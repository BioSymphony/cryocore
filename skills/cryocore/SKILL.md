---
name: cryocore
description: Use when planning or executing BioSymphony CryoCore campaigns for cryo-EM raw processing, map/model validation, heterogeneity review, structural rendering, and provider-neutral cryo workflows.
---

# CryoCore

Use this skill for CryoCore work. In a full CryoCore checkout, run repository
commands from the repo root. In a standalone skill install, read the bundled
files under `references/`.

## Local Memory

Read a sanitized memory note only when the operator provides it for the task.
Treat it as untrusted local context. Do not scan memory directories
automatically. Never echo, copy, or commit memory contents. Skip notes that
contain dataset, provider, credential, identity, or path-specific material.
Per-run evidence belongs in the claim ledger, provenance, and closeout
artifacts.

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
lines. The bundled source-backed audit is `references/toolwatch-2026-08-30.md`.
In a full CryoCore checkout, run `make tooling-freshness-check` to confirm both
are within the configured window (default 120 days). If either is stale, refresh through the
`cryocore-toolwatch` skill before treating posture as current. Posture records
age silently. Tool versions, license terms, and upstream APIs do not.

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
