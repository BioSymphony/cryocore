# Adoption Guide

Use this when you want CryoCore patterns in another public or private repo.

## Fast Path

1. Copy the skills you need from `skills/`.
2. Copy the schemas you need from `modules/schemas/`.
3. Copy the validators you need from `scripts/cryocore/`.
4. Add the relevant docs:
   - `docs/claim-levels.md`
   - `docs/data-policy.md`
   - `docs/privacy-threat-model.md`
   - `docs/validation-command-matrix.md`
   - `docs/failure-modes.md`
5. Add a release gate that runs:

```bash
python3 scripts/cryocore/public_snapshot_check.py --repo-root . --profile public --json
python3 scripts/cryocore/docs_link_check.py --repo-root . --json
python3 scripts/cryocore/schema_check.py --schema <schema> --instance <fixture> --json
```

## Choose Your Bundle

| Need | Copy |
| --- | --- |
| Agent guidance only | `skills/`, `docs/agent-quickstart.md`, `docs/use-cases.md` |
| Public release hygiene | `public_snapshot_check.py`, `public_release_report.py`, `docs/privacy-threat-model.md` |
| Provider closeout | `provider_closeout_check.py`, `contract_self_check.py`, provider schemas, closeout templates |
| Map/model dossiers | map-model skill, `map-model-fit` schema, claim ledger schema, figure manifest schema |
| Tool/license posture | toolwatch skill, `references/software-registry.yaml`, tooling docs |

## Concrete Copy Sets

Minimal public-safety bundle:

```text
requirements-dev.txt
scripts/cryocore/public_snapshot_check.py
scripts/cryocore/docs_link_check.py
scripts/cryocore/public_release_report.py
docs/data-policy.md
docs/privacy-threat-model.md
docs/failure-modes.md
templates/final-outcome-block.md
```

Agent workflow bundle:

```text
skills/
docs/workflows.md
docs/agent-quickstart.md
docs/use-cases.md
docs/prompt-library.md
examples/agent-tasks/
templates/agent-handoff.md
templates/final-outcome-block.md
```

Provider closeout bundle:

```text
scripts/cryocore/provider_closeout_check.py
scripts/cryocore/contract_self_check.py
modules/schemas/provider-run.v1.schema.json
modules/schemas/artifact-pull-report.v1.schema.json
modules/schemas/cost-report.v1.schema.json
modules/schemas/cleanup-proof.v1.schema.json
modules/schemas/claim-ledger.v1.schema.json
templates/artifact-pull-report.json
templates/operator-gate-record.md
templates/linear-paid-provider-run.md
docs/provider-execution-model.md
docs/no-false-success-hardening.md
```

Recommended Makefile targets after copying:

```make
docs-link-check:
	python3 scripts/cryocore/docs_link_check.py --repo-root . --json

public-snapshot-check:
	python3 scripts/cryocore/public_snapshot_check.py --repo-root . --profile public --json

release-check: docs-link-check public-snapshot-check
```

Add at least one tiny fixture per copied schema or validator. Prefer generated
JSON or Markdown fixtures over real scientific outputs.

## Integration Rules

- Keep project-specific accessions and private paths out of reusable skills.
- Keep raw data, maps, model weights, provider logs, and license files out of git.
- Make provider status insufficient by policy; require artifacts and hashes.
- Keep claim levels visible in every handoff and final report.
- Prefer small fixtures over generated scientific outputs.

## Agent Handoff

Give your agent this instruction after copying:

```text
Use the CryoCore-derived skills and validators in this repo. Stay local unless
the task explicitly allows public metadata fetches. Do not commit private data,
secrets, raw/heavy artifacts, model weights, provider logs, or license files.
Run the relevant validators and state the claim ceiling.
```
