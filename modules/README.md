# Modules

Modules are machine-readable CryoCore contracts.

- `schemas/`: JSON Schema subset contracts used by validators.
- `campaigns/`: campaign-level compositions.
- `data-modules/`: public accession and data-tier contracts.
- `lane-modules/`: workflow lane and tool posture contracts.
- `provider-profiles/`: local and remote execution profile contracts.
- `artifact-contracts/`: required evidence and claim maturity contracts.
- `image-modules/`: public image posture records.
- `smoke-checks/`: small environment and artifact-shape checks.

Run:

```bash
make module-check
make schema-check
make provider-check
```

