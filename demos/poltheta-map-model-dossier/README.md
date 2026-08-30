# Pol Theta Map/Model Dossier Demo

CryoCore map-and-model example that uses public EMDB, PDB, and wwPDB validation
data:

- EMDB: `EMD-43816`
- PDB: `9ASJ`
- target: human DNA polymerase theta helicase domain with AMP-PNP, dimer form
- runtime: CPU-only RunPod Pod, intended under two hours

An operator-authorized run downloads only the deposited EMDB map, PDB mmCIF
model, and wwPDB validation XML/PDF into ignored runtime storage. The local
preparation check below validates the contract shape without downloading the
map. The full workflow computes map header and density summaries, model
inventory, AMP-PNP neighborhoods, density-support checks, SVG figures,
provenance, a claim ledger, and a real-mode contract self-check.

Prep check without downloading the map locally:

```bash
make demo-poltheta-prep-check
```

A live RunPod launch is operator-owned and is outside the public release gate.
The following pseudocode shows the external launcher interface:

```text
operator-owned-provider-launch \
  --manifest runpod/bridge-manifests/poltheta-map-model-dossier.json \
  --out-dir .runtime/poltheta-map-model-remote \
  --max-spend-usd 1
```

This example does not use raw EMPIAR movies, CryoSPARC, Phenix, ChimeraX,
MotionCor, Rosetta, AlphaFold 3, private data, or persistent RunPod storage.
