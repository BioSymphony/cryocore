# cryo-core Image Plan

## Purpose

Open-source cryo-EM prep lane for no-download smoke checks, environment validation, and future RELION/Warp/M/Topaz/CTF workflows.

## Candidate Contents

- Ubuntu 22.04 or 24.04 CUDA devel base
- Python 3.11+
- RELION lane
- Warp/M lane with GPLv3/source-compliance records; current v2 dev builds require CUDA 12.9/.NET 10
- Topaz
- MotionCor3 from the CZI BSD-3-Clause source repository
- CTFFIND/Gctf gated by terms
- pyem/starfile/mrcfile/gemmi/numpy/scipy/pandas
- CryoCore scripts copied to `/opt/cryocore`

## Smoke Command

```bash
python3 /opt/cryocore/scripts/cryocore/toolcheck_runner.py \
  --manifest /opt/cryocore/runpod/launch-manifests/no-download-smoke.json \
  --out /workspace/cryocore/runs/${CRYOCORE_RUN_ID}
```

## License Policy

Do not include restricted installers or license IDs. Record unavailable tools as gated or missing in `toolcheck.json`.
