# T2R14 Open Dossier Demo

Small local CryoCore demo using public RCSB/EMDB metadata and PDB coordinates:

- PDB: `9W0Q`
- EMDB: `EMD-65512`
- target: bitter taste receptor T2R14 ligand/G-protein cryo-EM complex
- runtime: CPU-only, about one minute on a typical laptop

The demo downloads public RCSB metadata and the PDB mmCIF coordinate file. It
does not download the EMDB map. It computes chain and ligand-neighborhood
summaries, emits SVG figures, and writes a review package with provenance and
explicit claim limits.

Run locally:

```bash
python3 scripts/cryocore/t2r14_open_dossier.py \
  --out .runtime/t2r14-open-dossier \
  --json
```

Prepare the RunPod bridge packet:

```bash
make demo-t2r14-check
```

`demo-t2r14-check` requires an optional operator-owned provider bridge CLI. The
default command is `symphony-neocloud-bridge`. If the CLI is not installed, run
the local dossier command instead.

Expected local output shape:

```text
.runtime/t2r14-open-dossier/
  status.json
  artifact_hashes.json
  artifacts/
    report.html
    claim_ledger.md
    dossier_manifest.json
    figures/
    runpod-execution.tar.gz
```

To run the bridge steps directly, use:

```bash
python3 scripts/cryocore/build_t2r14_bridge_manifest.py
symphony-neocloud-bridge validate-manifest \
  runpod/bridge-manifests/t2r14-open-dossier.json \
  --json
symphony-neocloud-bridge prepare \
  runpod/bridge-manifests/t2r14-open-dossier.json \
  --out-dir .runtime/t2r14-open-dossier-packet \
  --json
```

A live RunPod launch is operator-owned and is outside the public release gate.
The following pseudocode shows the external launcher interface:

```text
operator-owned-provider-launch \
  --manifest runpod/bridge-manifests/t2r14-open-dossier.json \
  --out-dir .runtime/t2r14-open-dossier-remote \
  --max-spend-usd 1
```

The demo uses the Python standard library and public RCSB and EMDB metadata
APIs. It does not use CryoSPARC, Phenix, ChimeraX, MotionCor, Rosetta, AlphaFold
3, raw movies, private data, or persistent storage.
