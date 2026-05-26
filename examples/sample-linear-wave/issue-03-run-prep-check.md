# Run Pol Theta dossier prep check and validate shape

## Summary

Run the Pol Theta prep check end to end, then confirm the produced dossier
shape matches the contract under
`modules/artifact-contracts/structure-dossier.v1.json`. Close the wave when
the contract self-check and the public-snapshot check pass.

## Required Fields

- subgroup: `cryocore`
- campaign ID: `cryocore-poltheta-map-model-dossier-w1`
- routing label: `sym:cryocore`
- provider: `local`
- execution profile: `local-cpu-no-gpu`
- operator gate required: `no`
- exact inputs: `.runtime/public-accession-metadata.json` from `CRYOCORE-W1-01`, validated bridge manifest from `CRYOCORE-W1-02`.
- expected artifacts: prep-check log, contract self-check result, optional dossier shape sample appended to the issue.
- owned paths: `.runtime/poltheta-map-model-prep-check.log`.
- dependencies: `CRYOCORE-W1-01`, `CRYOCORE-W1-02`.
- license and capability caveats: prep mode only.
- risk notes: a contract self-check failure means the next wave (paid run) stays in Backlog until the dossier shape is correct.

## Acceptance Criteria

- [ ] Declared inputs are audited before execution.
- [ ] Required artifacts are produced and hashed.
- [ ] Validation outputs join back to declared inputs.
- [ ] Claim level is stated explicitly.
- [ ] Any partial, degraded, blocked, or failed outcome is recorded honestly.

## Validation Commands

```bash
make demo-poltheta-prep-check
make contract-self-check
make public-snapshot-check
```

## Touched Areas

- `.runtime/poltheta-map-model-prep-check.log` (gitignored)

## Dependencies

- `CRYOCORE-W1-01`
- `CRYOCORE-W1-02`

<!-- symphony:schema -->
```yaml
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
claim_level: candidate
```
