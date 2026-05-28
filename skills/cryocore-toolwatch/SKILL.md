---
name: cryocore-toolwatch
description: Use when researching, triaging, or updating BioSymphony CryoCore tool, preprint, workflow, data-source, or license posture records.
---

# CryoCore Toolwatch

Use this skill in the current `cryocore` checkout when a task
asks for new cryo-EM tools, repos, preprints, public data sources, validation
services, workflow engines, or repo skills.

## Read First

- `AGENTS.md`
- `README.md`
- `docs/tooling-and-licensing.md`
- `docs/toolwatch-2026-05-15.md` or a dated successor if the audit is new
- `references/software-registry.yaml`
- `references/validation-gates.md`

## Triage

Classify each candidate as:

- `planned`: source/terms are clear enough for public-safe docs, manifests, or
  adapters after normal review.
- `gated`: useful, but execution, upload, packaging, model weights, or binaries
  require explicit operator/license approval.
- `watch`: scientifically relevant, but not yet a dependable evidence-production
  dependency.

## Rules

- Prefer primary sources: official docs, GitHub repos, release pages, papers,
  preprints, and archive APIs.
- Record license and redistribution uncertainty instead of smoothing it over.
- Never add raw movies, maps, half-maps, particle stacks, model weights, private
  structures, unpublished sequences, license files, tokens, or secrets.
- Treat foundation-model map enhancement as derived evidence that needs caveats,
  input joins, weight hashes, and independent validation.
- For public archive integrations, default to metadata-only ledgers unless an
  operator gate explicitly allows heavy downloads or uploads.

## Output

When updating the repo:

1. Update `docs/toolwatch-YYYY-MM-DD.md` or create a dated successor.
2. Update `references/software-registry.yaml` only for candidates with enough
   source-backed posture to be useful to future runs.
3. Update `docs/tooling-and-licensing.md` for durable license policy.
4. Update `references/validation-gates.md` when a tool changes evidence gates.
5. Run `make preflight`, `make registry-check`, `make public-release-report`, and targeted tests.
