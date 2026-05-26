# Public Accession APIs

CryoCore should use public archive APIs as metadata sources first. Raw movies,
maps, half-maps, masks, particle stacks, sequence files, and downloaded
databases remain outside git and behind explicit operator gates.

## Default Sources

| Source | Use | Default posture |
| --- | --- | --- |
| EMPIAR REST API | Raw image-set metadata, linked EMDB IDs, size/context checks. | Metadata-only; no raw downloads by default. |
| EMDB REST API | Map metadata, fitted models, validation analysis, EMICSS annotations. | Metadata-only; no map downloads by default. |
| RCSB PDB Data API | Structure metadata, experimental method, entities, validation fields. | Metadata-only. |
| wwPDB validation report archive | Public validation XML/PDF for released PDB/EMDB entries. | Link and hash metadata; do not commit reports unless a tiny public-safe fixture is approved. |
| PDBe API | Cross-reference and annotation helper when RCSB or EMDB fields are insufficient. | Metadata-only. |

Primary docs:

- EMPIAR schema: https://www.ebi.ac.uk/empiar/api/documentation/schema
- EMDB schema: https://www.ebi.ac.uk/emdb/api/schema
- RCSB Data API: https://data.rcsb.org/
- wwPDB validation reports: https://www.wwpdb.org/validation/validation-reports
- EMICSS: https://www.ebi.ac.uk/emdb/emicss

## Metadata Ledger

Use `modules/schemas/public-accession-metadata.v1.schema.json` for public
metadata ledgers. Each ledger should record:

- accessions requested
- source API endpoints
- retrieval timestamp
- linked accessions
- validation report URLs
- response status, byte count, content type, and SHA256 when fetched
- `raw_data_download_required: false` unless a separate execution issue says
  otherwise

## Helper Script

`scripts/cryocore/fetch_public_accession_metadata.py` builds metadata ledgers.
It does not fetch network resources unless `--fetch` is passed.

Examples:

```bash
python3 scripts/cryocore/fetch_public_accession_metadata.py \
  --empiar 10204 \
  --emdb EMD-43816 \
  --pdb 9ASJ \
  --out .runtime/public-accession-metadata.json
```

```bash
python3 scripts/cryocore/fetch_public_accession_metadata.py \
  --emdb EMD-43816 \
  --pdb 9ASJ \
  --fetch \
  --out .runtime/public-accession-metadata.fetched.json
```

## Policy

- Metadata-only ledgers may be committed when small and public-safe.
- API response hashes are useful even when response bodies are not committed.
- Raw data transfer, map downloads, validation-service uploads, and model-weight
  downloads need explicit issue scope and operator gates.

## Related

- [Data Policy](data-policy.md): the data tiers that authorize metadata-only versus heavy fetches.
- [Public Accession Metadata schema](../modules/schemas/public-accession-metadata.v1.schema.json): the JSON contract for ledger entries.
- [Public Accession Metadata example](../examples/public-accession-metadata/README.md): a small fixture showing the ledger shape.
- [Recipe: Public Accession Example](recipes/public-accession-example.md): runnable smoke for these endpoints.
