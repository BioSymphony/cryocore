# Data Policy

CryoCore is a control-plane repository, not a data lake.

## Data Tiers

| Tier | Examples | Git policy | Runtime policy |
| --- | --- | --- | --- |
| Metadata-only | accession IDs, API endpoint ledgers, response hashes, validation summary pointers | allowed when small and public-safe | may be fetched by local checks |
| Deposited public artifacts | deposited maps, coordinates, validation reports | do not commit downloaded bodies unless tiny and explicitly fixture-safe | may be fetched into ignored `.runtime/`, `artifacts/`, `outputs/`, or external storage |
| Raw cryo-EM data | movies, EER/TIFF/MRC stacks, particle stacks, half-maps, masks | never commit | requires explicit operator authorization and external storage |
| Private or unpublished data | private structures, sequences, maps, model weights, lab data | never commit | operator-controlled storage only |

## Allowed In Git

- public accession identifiers
- small manifests
- checksums
- metadata-only public archive API ledgers
- command templates
- validation summaries
- public-safe result narratives
- small synthetic fixtures
- source-backed tool and license posture records

## Not Allowed In Git

- raw cryo-EM movies
- maps, half-maps, masks, particles, or particle stacks
- private or unpublished structures
- unpublished sequences
- model weights
- downloaded databases
- license files, license IDs, private installer URLs, API keys, tokens, registry credentials, or cloud credentials

## Storage Pattern

Heavy artifacts belong in one of:

- RunPod Network Volumes
- secure local storage
- institutional storage
- ignored `.runtime/`, `artifacts/`, or `outputs/` directories

Tracked files should point to heavy artifacts by accession, path reference, checksum, and provenance rather than copying the artifact.

## Public Metadata APIs

EMPIAR, EMDB, RCSB PDB, PDBe, EMICSS, and wwPDB validation endpoints may be used to create small metadata ledgers. Metadata ledgers must record endpoints, retrieval time, linked accessions, response hashes when fetched, and `raw_data_download_required: false` unless a separate execution issue explicitly authorizes data transfer.

API metadata access does not authorize raw movie, map, half-map, mask, particle-stack, coordinate, sequence, validation-report body, or model-weight downloads into git.

## Related

- [Claim Levels](claim-levels.md): how data-tier evidence maps to a claim ceiling.
- [Privacy Threat Model](privacy-threat-model.md): privacy, secret, and release-risk controls that pair with these tiers.
- [Public Accession APIs](public-accession-apis.md): which public endpoints CryoCore is wired to read.
- [Public Repo and Private Image Policy](public-repo-and-private-image-policy.md): the public source vs private runtime split.
- [Public Accession Metadata schema](../modules/schemas/public-accession-metadata.v1.schema.json): contract for the metadata ledger entries this policy authorizes.
