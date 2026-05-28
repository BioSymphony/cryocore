# Agent Skill Guide

CryoCore can be used as a skill pack for agents that need to plan, validate, or
close out cryo-EM evidence workflows. It gives agents reusable instructions,
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

1. Read every Markdown note under `.cryocore-memory/` if the folder exists.
   These are durable lessons captured by past agents on this user's machine.
2. Read `AGENTS.md`, `README.md`, `docs/data-policy.md`, and the matching skill.
3. Identify the data tier before planning any command.
4. Choose a claim ceiling before generating outputs.
5. Run local validators before provider prep.
6. Treat provider state as intent until closeout joins inputs, stages, artifacts,
   hashes, cleanup, and claim ledger evidence.

## Agent Memory And Learnings

Per-run evidence (claim ledger, provenance, closeout reports, hashes) belongs
in the run's artifact root. Some things an agent picks up are durable and
worth keeping in a memory store so the next run starts smarter.

The repo supports two complementary memory paths:

- **Repo-co-located memory at `.cryocore-memory/`.** Gitignored. Lives in
  the checkout so the agent finds it without needing to reach into an
  out-of-tree store. The root SKILL.md tells the agent to read this folder
  first. Note shape and exclusions are documented in
  `skills/cryocore/references/memory-note-template.md`. This is the path
  most users want.
- **Harness-native memory.** Useful when the same agent works across multiple
  repos and the harness already has its own store. Claude Code uses
  auto-memory under the project's `~/.claude/.../memory/` directory. Codex
  CLI and Symphony workers can write per-skill notes under the worker's
  shared skills tree. Linear-driven runs can keep dated retrospective notes
  on the issue or epic.

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

Public-release safety still applies. `docs/public-switch-checklist.md`
requires private run notes and private learnings to stay outside this
repository. The `.cryocore-memory/` folder is gitignored for that reason and
must not be committed.

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
