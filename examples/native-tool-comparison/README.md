# Native Tool Comparison

Use these manifests to compare GCtfFind with a native CTFFIND record or
MotionCor3 with a RELION global-motion record.

1. Copy [gctffind.json](gctffind.json) or [motioncor3.json](motioncor3.json)
   to your run directory.
2. Replace every path and zero hash with the actual file identity. Compute
   SHA256 with `shasum -a 256 FILE`.
3. Set microscope and processing parameters for your data. The numerical values
   in these templates are illustrative. For GCtfFind, copy the reference
   metadata and ordered defocus values from the native CTFFIND text file.
4. Describe the actual differences between the two processing methods.
5. Run the adapter from the repository root with a fresh output directory:

   ```bash
   python scripts/cryocore/em_tool_czi_worker_v1.py \
     "$COMPARISON_MANIFEST" .runtime/czi-comparison
   ```

Read `validation.json` and the per-input native logs before using the output.
Paths in a manifest resolve from the working directory.

The MotionCor3 template uses global alignment and zero dose weighting. Set
`gain` to `null` only when the input needs no gain correction. For TIFF input,
install `tifffile==2024.9.20` and `imagecodecs==2024.9.22`; MRC checks use
Python's standard library. Install the pinned native executable separately.

See the [usage guide](../../docs/micrograph-qc-and-output-checks.md) for Miffi,
header normalization, and provider environment setup.
