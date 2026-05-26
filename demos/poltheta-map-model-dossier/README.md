# Pol Theta Map/Model Dossier Demo

Small real CryoCore demo using public EMDB/PDB/wwPDB validation data:

- EMDB: `EMD-43816`
- PDB: `9ASJ`
- target: human DNA polymerase theta helicase domain with AMP-PNP, dimer form
- runtime: CPU-only RunPod Pod, intended under two hours

The demo downloads only the deposited EMDB map, PDB mmCIF model, and wwPDB validation XML/PDF. It computes map header/density summaries, model inventory, AMP-PNP neighborhoods, density-support checks, SVG figures, provenance, claim ledger, and a real-mode contract self-check.

Prep check without downloading the map locally:

```bash
make demo-poltheta-prep-check
```

Real RunPod launch is operator-owned and sits outside the public release
gate. The block below is pseudocode for an external launcher to illustrate
what a paid run would look like:

```text
operator-owned-provider-launch \
  --manifest runpod/bridge-manifests/poltheta-map-model-dossier.json \
  --out-dir .runtime/poltheta-map-model-remote \
  --max-spend-usd 1
```

This demo intentionally avoids raw EMPIAR movies, CryoSPARC, Phenix, ChimeraX, MotionCor, Rosetta, AlphaFold 3, private data, and persistent RunPod storage.
