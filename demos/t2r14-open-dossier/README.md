# T2R14 Open Dossier Demo

Small, real, no-license CryoCore demo using public RCSB/EMDB metadata:

- PDB: `9W0Q`
- EMDB: `EMD-65512`
- target: bitter taste receptor T2R14 ligand/G-protein cryo-EM complex
- runtime: CPU-only, intended under one hour on RunPod

The demo downloads only public mmCIF and RCSB metadata, computes chain and ligand-neighborhood summaries, emits SVG figures, and writes a dossier packet with provenance and explicit claim limits.

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

`demo-t2r14-check` requires the optional operator-owned provider bridge CLI,
defaulting to `symphony-neocloud-bridge`. If that CLI is not installed, the
local dossier run above is still the recommended first success path.

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

Or run the bridge steps directly:

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

Real RunPod launch is operator-owned and sits outside the public release
gate. The block below is pseudocode for an external launcher to illustrate
what a paid run would look like:

```text
operator-owned-provider-launch \
  --manifest runpod/bridge-manifests/t2r14-open-dossier.json \
  --out-dir .runtime/t2r14-open-dossier-remote \
  --max-spend-usd 1
```

The demo uses only Python stdlib and public RCSB/EMDB metadata APIs. Tools like CryoSPARC, Phenix, ChimeraX, MotionCor, Rosetta, and AlphaFold 3, along with raw movies, private data, and persistent storage, live in lanes outside this demo.
