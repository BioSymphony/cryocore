# Micrograph QC And Native Output Checks

Use the Miffi adapter to score micrograph quality, the CZI adapter to compare
motion and CTF estimates with reference outputs, and the MRC helper to repair
header metadata without changing pixels.

## Score Micrographs With Miffi

The [Miffi adapter](../scripts/cryocore/em_tool_miffi_worker_v1.py) checks source
and checkpoint identities, runs native inference, and exports per-crop
probabilities, logits, and micrograph scores as JSON and CSV.

Use Python 3.10 with PyTorch 2.1.2+cu121, torchvision 0.16.2+cu121,
NumPy 1.26.4, mrcfile 1.5.4, and timm 0.9.16. The adapter pins
[Miffi source](https://github.com/ando-lab/miffi/tree/697c72545fcf1e72d8dcaf6250dfd42139a864e7).
On Linux with a CUDA 12.1-compatible NVIDIA driver, prepare a Python 3.10
environment with the recorded dependency versions:

```bash
python3.10 -m venv .runtime/miffi-env
. .runtime/miffi-env/bin/activate
python -m pip install pip==25.1.1
python -m pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu121
python -m pip install -r examples/native-tool-comparison/miffi-requirements.txt
git clone https://github.com/ando-lab/miffi .runtime/miffi-source
git -C .runtime/miffi-source checkout --detach 697c72545fcf1e72d8dcaf6250dfd42139a864e7
python -m pip install --no-deps --no-build-isolation .runtime/miffi-source
export MIFFI_SOURCE="$PWD/.runtime/miffi-source"
```

1. Obtain the pinned source and matching [checkpoint](https://zenodo.org/records/8342009). Put equal-sized, corrected
   MRC micrographs in one input directory.
2. Set the source, checkpoint, input directory, and specimen pixel size:

   ```bash
   python scripts/cryocore/em_tool_miffi_worker_v1.py \
     --source-dir "$MIFFI_SOURCE" \
     --checkpoint "$MIFFI_CHECKPOINT" \
     --checkpoint-sha256 80c68f3d1c52b317532467b95332a0d4b9d17adbe5ee7fac0edc5909783c7a64 \
     --input-dir "$MICROGRAPHS" --pixel-size "$PIXEL_SIZE_ANGSTROM" \
     --model-name miffi_v1 --output-dir .runtime/miffi-qc
   ```
3. Inspect `miffi_qc_manifest.json`, `predictions.json`, and
   `micrograph_filter_scores.csv`. Compare flagged images with their native
   pixels before selecting data for the next step.

For `miffi_no_ps_v1`, use its separate checkpoint with SHA256
`76b1946f6e5bdf6b53047ab29dfe9b2305777ed2732be26fc45a967a48d95894`.
These are two trained models. The adapter retains every crop score and records
native preprocessing, including overlapping crops and the FFT-amplitude channel.

## Compare Motion And CTF Estimates

The [CZI adapter](../scripts/cryocore/em_tool_czi_worker_v1.py) runs
MotionCor3 1.2.4 or GCtfFind 1.2.5. Its input manifest specifies the executable
hash, pinned source revision, input hashes, microscope parameters, and reference
files. Start with the [complete comparison examples](../examples/native-tool-comparison/README.md).

```bash
python scripts/cryocore/em_tool_czi_worker_v1.py \
  "$COMPARISON_MANIFEST" .runtime/czi-comparison
```

Read `validation.json` alongside each native log. GCtfFind comparisons use
ordered defocus components and matching microscope metadata. Motion comparisons
retain global trajectories and frame counts. Record differences in filtering,
local-motion models, and coordinate conventions when interpreting the results.

## Repair MRC Headers

Some native MRC files open successfully but fail full validation because their
MAP identifier or density statistics need correction. The
[header helper](../scripts/cryocore/normalize_mrc_header_v1.py) writes a separate
copy and verifies that every byte outside those fields remains identical.

With mrcfile 1.5.4 and NumPy installed:

```bash
python scripts/cryocore/normalize_mrc_header_v1.py \
  --input "$NATIVE_MRC" \
  --output .runtime/header-check/normalized.mrc \
  --receipt .runtime/header-check/receipt.json
```

Use fresh output paths. The receipt records both file hashes, changed byte
ranges, identical pixel payloads, and the full validation result.

## Run On Modal Or Fal

Keep the provider SDK and scientific packages in separate environments. Call
the scientific interpreter explicitly and clear inherited `PYTHONPATH` and
`PYTHONHOME`; set `PYTHONNOUSERSITE=1`.

For Modal, put variables needed during remote module imports into the image
environment. For fal, match the submitting Python minor version to the container,
and pin the package installer before installing CUDA-specific wheels.

Keep the same source, checkpoint, inputs, and preprocessing when comparing
providers. Compare exported numeric values and selected crops before chaining
their outputs into another tool. Keep native logs and manifests with the run.
