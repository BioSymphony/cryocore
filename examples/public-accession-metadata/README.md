# Public Accession Metadata Example

This example records API endpoints and validation report URLs only. It does not
download raw EMPIAR images, EMDB maps, PDB coordinate files, or validation report
bodies.

Regenerate with:

```bash
python3 scripts/cryocore/fetch_public_accession_metadata.py \
  --empiar 10204 \
  --emdb EMD-43816 \
  --pdb 9ASJ \
  --out examples/public-accession-metadata/metadata.json
```
