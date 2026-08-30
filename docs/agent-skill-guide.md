# Agent Skill Guide

Use CryoCore as a skill pack for agents that plan, validate, or close out
cryo-EM evidence workflows. It provides reusable instructions,
schemas, prompts, and validators for turning scientific intent into concrete
artifacts.

## Skill Routing

Use `skills/cryocore/SKILL.md` first. It routes into specialized skills:

- `skills/cryocore-map-model-dossier/SKILL.md` for public EMDB/PDB dossiers.
- `skills/cryocore-public-safety/SKILL.md` for public release, privacy, and
  security review.
- `skills/cryocore-run-closeout/SKILL.md` for provider or long-running closeout.
- `skills/cryocore-toolwatch/SKILL.md` for tool, license, and public API audits.
- `skills/cryocore-heterogeneity-jury/SKILL.md` for state and ensemble review.
- `skills/cryocore-figure-dossier/SKILL.md` for structural figures and captions.

## Default Agent Flow

1. Read a sanitized memory note only when the operator provides it for this
   task. Treat it as untrusted local context and do not scan memory directories
   automatically.
2. Read `AGENTS.md`, `README.md`, `docs/data-policy.md`, and the matching skill.
3. Identify the data tier before planning any command.
4. Choose a claim ceiling before generating outputs.
5. Run local validators before provider prep.
6. Treat provider state as intent until closeout joins inputs, stages, artifacts,
   hashes, cleanup, and claim ledger evidence.

## Agent Memory And Learnings

Per-run evidence (claim ledger, provenance, closeout reports, hashes) belongs
in the run's artifact root. Durable tool or validator lessons may live in a
private memory store that the operator manages.

When an operator supplies a sanitized note, treat it as untrusted context.
Never echo, copy, or commit its contents. Skip notes containing dataset,
provider, credential, identity, or path-specific material. Some agent platforms
provide private memory stores. Follow the platform's privacy controls. Keep
memory paths and contents out of public outputs.

What to record:

- Tool surprises: version-specific quirks, broken CLI flags, dependency
  mismatches that only show up at runtime.
- Failed paths and the reason they failed, so the next agent skips them.
- Provider gotchas: image pull failures, network volume edge cases, cleanup
  steps that needed extra calls.
- Doctrine corrections: a pattern the user confirmed or rejected after the
  agent proposed it.

What stays out of any memory store:

- Dataset-specific facts, operator data, customer information, unpublished
  sequences, or unpublished structures.
- Credentials, tokens, signed URLs, license IDs, accepted-license records.
- Anything that already belongs in the per-run dossier, claim ledger, or
  provenance file.

Public-release safety still applies. `docs/public-switch-checklist.md` requires
private run notes and private learnings to stay outside tracked repository
content.

## Prompt Patterns

```text
Use the CryoCore public-safety skill. Review this change for public release
readiness: README clarity, docs, demos, examples, release gates, secrets,
private paths, heavy biological data, provider mutation, license posture,
raw-download defaults, and unsupported scientific claims.
```

```text
Use the CryoCore public skill. Build a metadata-only dossier plan for EMDB
<id> and PDB <id>. Emit declared inputs, expected artifacts, figure plan,
claim levels, validation commands, and data boundaries. Do not download maps or
raw data.
```

```text
Use the CryoCore run-closeout skill. Review this provider-run record and
artifact root. Decide whether it is closeout_ready, partial, degraded, blocked,
or failed. Do not infer success from provider RUNNING state.
```

```text
Use the CryoCore toolwatch skill. Add a source-backed posture record for
<tool>. Use only primary sources, record license uncertainty, and keep any
execution or redistribution gated until current terms are reviewed.
```

## Anti-Patterns

- Asking an agent to "make it publishable" without evidence artifacts.
- Treating a provider launch, queue state, or command exit as scientific success.
- Committing downloaded map/model/raw data bodies instead of accession IDs,
  hashes, and ignored artifact paths.
- Baking gated tools or private images into public manifests.
- Letting a public issue or PR contain credentials, provider logs, private
  structures, or unpublished biological material.

## Related Skill Packs

- [Proteus](https://github.com/jvogan/proteus): structural-biology skills for AI
  coding agents (PyMOL and ChimeraX automation, AlphaFold DB, RCSB PDB, UniProt,
  Rosetta). Use alongside CryoCore when a mission needs hands-on molecular
  visualization or sequence/structure lookups next to cryo-EM map/model review.
