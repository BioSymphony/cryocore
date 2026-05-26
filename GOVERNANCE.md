# Governance

This public repo uses a lightweight maintainer model.

## Scope

CryoCore accepts public-safe improvements to:

- agent skills and prompts
- schemas, validators, and release gates
- public accession demos and tiny fixtures
- provider closeout contracts
- tooling/license posture docs
- claim-level and data-policy documentation

It does not accept private data, raw/heavy scientific artifacts, credentials,
license files, provider logs, or unsupported scientific claims.

## Decision Rules

- Safety gates may be made stricter without waiting for a major release.
- Loosening a safety gate requires maintainer review and a documented rationale.
- Runtime-gated tool posture must be source-backed and date-stamped.
- Provider success requires fetched artifacts, hashes, validation, cost, cleanup,
  and claim ledger evidence.

## Releases

Public releases are cut from a scrubbed tree after `make release-check` passes.
The first public switch also requires the checks in `docs/public-switch-checklist.md`.
