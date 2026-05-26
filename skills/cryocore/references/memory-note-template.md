# Memory Note Template

Use this shape when you write a note in `.cryocore-memory/`. One file per note,
named `YYYY-MM-DD-<slug>.md`. Keep it short. Five sections.

The memory folder is gitignored and never travels upstream. It is for
cross-campaign behavior change. Per-run evidence (claim ledger, provenance,
closeout reports, hashes) belongs in the run's artifact root.

Do not include in any memory note:

- secrets, tokens, signed URLs, API keys, accepted-license records
- private paths, hostnames, project IDs, billing identifiers
- campaign-specific data, dataset accessions tied to private work,
  raw or unpublished sequences, raw or unpublished structures
- provider-allocation IDs that identify private runs
- large outputs, log dumps, or artifact bodies

If you cannot describe the lesson without one of those, the lesson belongs in
the per-run dossier, not in memory.

## Template

```markdown
---
title: <short title>
date: YYYY-MM-DD
applies_to: <skill name, lane, validator, or workflow step>
---

## What happened

One or two sentences describing what surprised you. Be concrete enough that
the next agent can recognize the same situation.

## What was tried

Bullet list of the routes you tried before finding the working one.

- attempt 1
- attempt 2

## What worked

The route that resolved the situation, written so the next agent can apply it
without re-deriving the reasoning.

## When this applies

The conditions under which this note is relevant. Be specific so the next
agent does not over-generalize.

## What to skip

Routes that look plausible but do not work, with a one-line reason each.
```

## Realistic Example

Below is a sample memory note. It is illustrative only. It uses an example
about the repo's own validators, so the shape is obvious without pretending
to validate any biological claim.

```markdown
---
title: readonly-check bundle includes an intentional fail fixture
date: 2026-05-26
applies_to: make readonly-check, scripts/cryocore/provider_closeout_check.py
---

## What happened

`make readonly-check` produced a block of output containing `"ok": false` from
`provider_closeout_check.py` against
`tests/fixtures/provider-closeout/bad-intent/`. The first read suggested the
repo was broken. The bundle as a whole still finished green elsewhere.

## What was tried

- Re-ran `make readonly-check` to confirm the failure was reproducible.
- Read `provider_closeout_check.py` to see whether the check itself was wrong.

## What worked

Read `tests/fixtures/provider-closeout/bad-intent/README.md` (or the fixture
contents). The fixture is a negative-test case. The check is supposed to
return `ok: false` for it. The validator is working as designed.

## When this applies

When scanning `make readonly-check` output and seeing a single `ok: false`
block. Confirm the failing item is the intentional bad-intent fixture before
escalating. If a different fixture fails, that is a real regression.

## What to skip

- Do not patch the validator to suppress the failure. The negative test would
  stop catching real regressions.
- Do not change the bad-intent fixture to make it pass. It is intentionally
  broken so the validator has something to fail on.
```
