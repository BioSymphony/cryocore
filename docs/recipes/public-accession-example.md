# Recipe: Public Accession Example

Fetch public metadata for one or more EMPIAR, EMDB, or PDB accessions and
write a small ledger your agent can use as the starting input audit for a
larger mission.

## When to use it

- Your agent needs to confirm that an accession is public, fetchable, and current.
- A mission brief needs an input audit before any heavier work starts.
- A campaign needs a reproducible metadata snapshot pinned to a specific date.

## Inputs

- One or more public accession IDs: EMPIAR, EMDB, PDB. Heavy artifacts
  (downloaded maps, raw movies, particle stacks, private structures, model
  weights) live outside this recipe.

## Commands

```bash
python3 scripts/cryocore/fetch_public_accession_metadata.py \
  --empiar 10204 \
  --emdb EMD-43816 \
  --pdb 9ASJ \
  --out .runtime/public-accession-metadata.json
```

The script queries each accession's public API and writes a compact JSON
ledger with the resolved metadata, the source endpoints, and a hash you can
pin in a campaign manifest.

## Files Produced

- `.runtime/public-accession-metadata.json`: machine-readable metadata ledger with endpoints, hashes, and timestamps.

## Claim Ceiling

`processed`: the ledger records what the public archives returned at the time
of fetch. Biological mechanism, ligand action, and density interpretation
require the heavier dossier recipe and expert review.

## Validation

```bash
make public-metadata-check
make public-release-report
```

## Failure Handling

When network access fails, keep the example metadata-only and record the
endpoints the agent should retry. Partial downloads stay out of git so the
ledger reflects what actually resolved.

## Related

- [Public Accession APIs](../public-accession-apis.md): full list of endpoints CryoCore uses.
- [Map/Model Dossier](map-model-dossier.md): next recipe up, consuming the metadata this one produces.
- [examples/public-accession-metadata/](../../examples/public-accession-metadata/): committed example of the ledger shape.

