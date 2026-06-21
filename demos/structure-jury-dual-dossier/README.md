# Dual Structure Comparison Demo

Small, real, no-license CryoCore campaign that runs two public
deposited-structure lanes and joins them into one review package:

- T2R14 receptor complex: `PDB 9W0Q`, `EMD-65512`
- Pol theta helicase map/model: `PDB 9ASJ`, `EMD-43816`

The campaign downloads only public deposited coordinates, public EMDB map/model
files and wwPDB reports for the pol theta lane, and public RCSB metadata. Raw
movies, particle stacks, private data, and license-gated tools stay outside the
campaign.

Prepare the RunPod bridge packet without launching:

```bash
make demo-structure-jury-prep-check
```

Real RunPod launch is operator-owned and sits outside the public release
gate. The block below is pseudocode for an external launcher to illustrate
what a paid run would look like:

```text
operator-owned-provider-launch \
  --manifest runpod/bridge-manifests/structure-jury-dual-dossier.json \
  --out-dir .runtime/structure-jury-dual-dossier-runpod \
  --max-spend-usd 2 \
  --timeout-seconds 7200
```

Closeout passes when the artifacts are fetched and hashed, the pod cleanup is verified, and the closeout package joins everything back to the declared inputs.
