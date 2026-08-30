# CryoCore Toolwatch 2026-08-30

This focused audit covers public release records, security-sensitive workflow
helpers, and cryo-ET repositories that changed after the July audit. It records
metadata and operating posture only. No software, model weights, binaries, or
scientific data are included in this repository.

## Registry Updates

| Tool | Audited record | Posture | Public-safe consequence |
| --- | --- | --- | --- |
| cryoDRGN | `4.3.1`, released 2026-08-04 | planned | Record the in-browser volume view and WarpTools parser. Keep GPL source compliance, trusted-pickle handling, model hashes, and localhost-only dashboard access. |
| CryoSPARC | `v5.0.7`, released 2026-08-14 | gated | Update the runtime version record without changing the license, installer, secret, or project-data gates. |
| Servalcat | `0.4.142`, released 2026-06-21 | planned | Open-source modes remain planned. Refmac and CCP4-backed modes inherit their separate gates. |
| AreTomo3 | `v2.2.2`, released 2026-07-16 | planned | Record CTF and tilt-axis controls in run manifests. Keep raw tilt series and tomograms outside git. |
| pytom-match-pick | `0.14.0`, released 2026-08-04 | planned | Record WarpTools metadata handling, 3D CTF, whitening, and phase-randomization parameters. |
| tomoDRGN | `v1.0.4`, released 2026-07-13 | watch | Make the raw, non-CTF-premultiplied particle-series requirement explicit before fixture work. |
| copick | upstream `v1.27.0`, PyPI `1.26.1` | planned | Pin the selected source because the package index lagged the upstream release during this audit. Limit project writes to the declared output scope. |
| copick-mcp | `v0.6.1`, released 2026-06-29 | planned | Keep the alpha server read-only by default and require MCP security review before enabling writes. |
| Scipion / Xmipp | `scipion-em 3.11.0`, `scipion-em-xmipp 29.0.1` | planned | Pin the core and plugin separately. Preserve the terms of every invoked tool. |
| Apptainer | `v1.5.3`, released 2026-07-21 | planned | Update the HPC runtime record. Continue to hash SIF artifacts and record the build environment. |
| rocrate-validator | `0.11.3`, released 2026-07-28 | planned | Update the provenance-validation pin. |
| Syft | `v1.51.1`, released 2026-08-27 | planned | Update the SBOM generator pin. |
| Cosign | `v3.1.3`, released 2026-08-06 | planned | Use version 3.1.3 or a later patched release because 3.1.3 includes a verification-bypass fix. Continue to verify immutable digests and record identity policy. |

## New Registry Records

| Tool | Posture | Why it is tracked | Gate |
| --- | --- | --- | --- |
| GCtfFind `v1.0.0` | planned | BSD-3-Clause GPU CTF estimation for cryo-EM micrographs and cryo-ET tilt series. | Pin a small public fixture and CUDA compatibility before using it as a default lane. |
| FlyTomo | gated | On-the-fly cryo-ET processing and diagnosis with a public paper and binary distribution. | Upstream limits use to academic and noncommercial research and prohibits binary redistribution or modification without permission. Keep binaries and raw data outside public images and git. |

## Corrected Or Clarified Records

- Miffi has a public `1.0.1` package. Its models, state dictionaries, training
  data, and pickle outputs remain separate trust and provenance concerns.
- MAVEn `v1.0` is documented against cryoDRGN `0.3.2` and depends on RELION,
  Chimera, and ChimeraX. It remains `watch` until current compatibility and all
  inherited gates are tested.
- ResMap remains a legacy Python 2.7 comparator with noncommercial and
  no-derivatives terms. It is not a primary provider lane.
- Warp's changelog mentions an untagged development update, while the official
  package channel still publishes `v2.0.0dev39`. The installable pin stays at
  `dev39`.
- RELION `5.0.1` remains the stable release. Version `5.1.0` remains a prerelease.
- ModelAngelo `v1.0.18` remains the current tagged release. Code licensing does
  not clear model-weight provenance or redistribution.

## Watch Notes

The following repositories relate to CryoCore but do not have enough public
information for registry promotion:

| Repository | Reason to watch |
| --- | --- |
| OPUS-ET Agent | Young agent interface with no tagged release and inherited dependencies on processing, reconstruction, and visualization tools. |
| CoCryoViS | Collaborative hosted cryo-ET interface. Upload, privacy, storage, and execution boundaries need explicit documentation. |
| CryoLithe | Reconstruction approach with model weights and derived tomograms that need weight provenance, input joins, and independent validation. |

## Primary Sources

- cryoDRGN releases: https://github.com/ml-struct-bio/cryodrgn/releases
- CryoSPARC releases: https://cryosparc.com/
- Servalcat releases: https://github.com/keitaroyam/servalcat/releases
- AreTomo3 releases: https://github.com/czimaginginstitute/AreTomo3/releases
- pytom-match-pick releases: https://github.com/SBC-Utrecht/pytom-match-pick/releases
- tomoDRGN releases: https://github.com/bpowell122/tomodrgn/releases
- copick releases: https://github.com/copick/copick/releases
- copick PyPI: https://pypi.org/project/copick/
- copick-mcp releases: https://github.com/copick/copick-mcp/releases
- Scipion PyPI: https://pypi.org/project/scipion-em/
- Xmipp plugin PyPI: https://pypi.org/project/scipion-em-xmipp/
- Miffi source: https://github.com/ando-lab/miffi
- Miffi PyPI: https://pypi.org/project/miffi/
- MAVEn source: https://github.com/lkinman/MAVEn
- GCtfFind source and releases: https://github.com/czimaginginstitute/GCtfFind
- FlyTomo source: https://github.com/SaiLi-Lab/FlyTomo
- FlyTomo paper: https://www.nature.com/articles/s41467-026-75998-3
- Apptainer releases: https://github.com/apptainer/apptainer/releases
- rocrate-validator releases: https://github.com/crs4/rocrate-validator/releases
- Syft releases: https://github.com/anchore/syft/releases
- Cosign releases: https://github.com/sigstore/cosign/releases
- OPUS-ET Agent: https://github.com/alncat/opus-et-agent
- CoCryoViS: https://github.com/nanovis/cocryovis
- CryoLithe: https://github.com/swing-research/CryoLithe
