---
name: cryocore-run-closeout
description: Use when closing out CryoCore provider runs, RunPod/AWS/HPC executions, or long-running cryo-EM workflow issues.
---

# CryoCore Run Closeout

Scientific success requires fetched artifacts, hashes, validation outputs,
cost records, cleanup proof, and a claim ledger that joins everything back to
the declared inputs. Use this skill for any closeout that mentions RunPod,
AWS, SSH/HPC, remote execution, paid compute, or long-running cryo-EM
processing.

## Read First

- `references/no-false-success-hardening.md`
- `references/validation-gates.md`
- `references/structure-dossier.v1.json`
- the launch manifest
- the stage contract

## Required Evidence

- `validation/input-audit.json`
- `stage-progress.jsonl`
- `validation/stage-contract-check.json`
- `validation/contract-self-check.json`
- artifact index with hashes
- tool versions manifest (such as `validation/versions.json`) joining exact tool versions to the artifacts they produced
- provider run record
- cost report when paid compute was used
- cleanup proof when temporary provider resources were created

## Outcome Labels

Final closeout must classify the run as one of:

- `success`
- `partial`
- `degraded`
- `blocked`
- `failed`

Use `partial` or `degraded` when a tool fallback, missing renderer, incomplete
artifact, provider mismatch, or validation gap remains.
