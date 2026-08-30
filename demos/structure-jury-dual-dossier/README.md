# Dual Structure Comparison Demo

CryoCore comparison example that joins two public deposited-structure lanes
into one review package:

- T2R14 receptor complex: `PDB 9W0Q`, `EMD-65512`
- Pol theta helicase map/model: `PDB 9ASJ`, `EMD-43816`

An operator-authorized run downloads public deposited coordinates, the public
EMDB map and wwPDB reports for the Pol Theta lane, and public RCSB metadata into
ignored runtime storage. The preparation check below performs no map download.
Raw movies, particle stacks, private data, and license-gated tools stay outside
the campaign.

Prepare the RunPod bridge packet without launching:

```bash
make demo-structure-jury-prep-check
```

A live RunPod launch is operator-owned and is outside the public release gate.
The following pseudocode shows the external launcher interface:

```text
operator-owned-provider-launch \
  --manifest runpod/bridge-manifests/structure-jury-dual-dossier.json \
  --out-dir .runtime/structure-jury-dual-dossier-runpod \
  --max-spend-usd 2 \
  --timeout-seconds 7200
```

Closeout passes only after the artifacts are fetched and hashed, cleanup is
verified, and the closeout package links all outputs to the declared inputs.
