# Paid Provider Run

Public issue bodies must use aliases only. Keep concrete provider IDs, account
IDs, volume IDs, billing details, private logs, credentials, signed URLs, and
license files in an operator-owned private record.

## Operator Gate

- Provider:
- Pod/job alias or name prefix:
- Budget cap:
- Expected duration:
- Data volume:
- Gated tools:
- Cleanup expectation:
- Approval record:

## Scope

- Campaign:
- Launch manifest:
- Stage contract:
- Artifact contract:
- Expected claim level:

## Required Artifacts

- provider run record
- `stage-progress.jsonl`
- `validation/input-audit.json`
- `validation/stage-contract-check.json`
- fetched artifact index
- artifact hashes
- cost report
- cleanup proof
- `validation/contract-self-check.json`

## Fallback Policy

Any provider, image, data, tool, or renderer fallback must close as `partial`,
`degraded`, or `blocked` unless the original contract is updated and revalidated.

## Validation

```bash
make launch-preflight-prep
make launch-preflight-real
make contract-self-check
make provider-check
make provider-closeout-check
```

## Worker Boundary

Workers prepare and validate only. They must not call provider-mutating
commands such as pod creation, remote execution, or paid-run confirmation
flags. Use `scripts/cryocore/runpod_launch_request.py` to write an
operator-reviewed launch request JSON; operator-owned closeout owns paid
provider mutation, artifact fetch/hash, cost reporting, and cleanup.
