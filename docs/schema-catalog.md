# Schema Catalog

CryoCore schemas are small public contracts for evidence and closeout.

| Schema | Purpose |
| --- | --- |
| `modules/schemas/public-accession-metadata.v1.schema.json` | Metadata-only public accession ledgers. |
| `modules/schemas/provider-run.v1.schema.json` | Provider state, actual runtime evidence, and closeout intent. |
| `modules/schemas/stage-progress.v1.schema.json` | Stage event ledgers for long-running workflows. |
| `modules/schemas/workflow-run.v1.schema.json` | Workflow provenance and execution metadata. |
| `modules/schemas/container-provenance.v1.schema.json` | Container/image provenance and runtime posture. |
| `modules/schemas/artifact-index.v1.schema.json` | Artifact lists, hashes, and provenance. |
| `modules/schemas/artifact-pull-report.v1.schema.json` | Fetched artifact acceptance and proxy-error checks. |
| `modules/schemas/cost-report.v1.schema.json` | Budget and paid-provider cost evidence. |
| `modules/schemas/cleanup-proof.v1.schema.json` | Proof that temporary provider resources were cleaned up. |
| `modules/schemas/claim-ledger.v1.schema.json` | Claim levels, evidence artifacts, and caveats. |
| `modules/schemas/figure-manifest.v1.schema.json` | Reproducible structural figure inventory. |
| `modules/schemas/map-model-fit.v1.schema.json` | Map/model validation and density-support summaries. |

Validate fixtures with:

```bash
make schema-check
```

## Related

- [Module Catalog](module-catalog.md): the campaign, data, lane, and provider-profile contracts that reference these schemas.
- [Validation Command Matrix](validation-command-matrix.md): which validator to reach for when a schema fails.
- [Claim Levels](claim-levels.md): how the `claim-ledger` schema's enum values map to the ladder.

