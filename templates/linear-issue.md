# <Issue Title>

## Summary

<One-paragraph scientific contract.>

## Required Fields

- subgroup: `cryocore`
- campaign ID:
- routing label: `sym:cryocore`
- provider: `local`, `runpod`, `aws-batch`, `ssh-hpc`, `generic-cloud`, `neocloud`, or `provider-neutral`
- execution profile:
- operator gate required: `yes` or `no`
- exact inputs:
- expected artifacts:
- owned paths:
- dependencies:
- license and capability caveats:
- risk notes:

## Acceptance Criteria

- [ ] Declared inputs are audited before execution.
- [ ] Required artifacts are produced, fetched when remote, and hashed.
- [ ] Validation outputs join back to declared inputs.
- [ ] Claim level is stated explicitly.
- [ ] Any partial, degraded, blocked, or failed outcome is recorded honestly.

## Validation Commands

```bash
python3 scripts/cryocore/preflight.py --repo-root . --json
python3 scripts/cryocore/software_registry_check.py references/software-registry.yaml --json
```

Provider-mutating commands must not appear in worker validation blocks. For
RunPod work, use `scripts/cryocore/runpod_launch_request.py` after local
validation passes and let trusted host-side closeout perform provider mutation.

## Touched Areas

- TBD

## Dependencies

- TBD

<!-- symphony:schema -->
```yaml
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
claim_level: candidate
```
