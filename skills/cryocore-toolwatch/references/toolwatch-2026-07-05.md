# CryoCore Toolwatch 2026-07-05

This focused audit covers two public repositories:

- `phonchi/Computational-CryoEM`
- `ml-struct-bio/cryodrgn`

Use the first repository only as a curated pointer list. Do not copy helper code
from it without a separate license review, because its repo-level CC0 posture is
not enough to clear code that says it was derived from other projects.

The second repository is already a planned CryoCore heterogeneity lane. The
July audit recorded cryoDRGN `4.3.0` and its dashboard and command-builder
posture. Later releases are tracked in newer dated notes.

## Registry Updates

| Candidate | Posture | What it adds | Main blocker |
| --- | --- | --- | --- |
| cryoDRGN `4.3.0` | planned | Continuous heterogeneity, ab initio reconstruction, landscape analysis, dashboard review. | GPLv3 source compliance, trusted pickle artifacts, dashboard must not be exposed on provider-public ports. |
| ASPIRE-Python `v0.14.3` | watch | Known-answer synthetic fixtures, covariance/denoising baselines, math-heavy benchmark checks. | Pin tiny public fixture and dependency footprint before promoting to a lane. |
| Miffi | watch | Micrograph quality filtering using image and Fourier-space features. | No tagged GitHub release. The `1.0.1` PyPI package, model, checkpoint, training-data, and serialized-output posture need review. |
| EMAN2 e2gmm | watch | Independent heterogeneity/state comparison against cryoDRGN, RECOVAR, or DynaMight. | Inherits EMAN2 mixed license/dependency/runtime review. |
| MAVEn `v1.0` | watch | Downstream cryoDRGN volume-ensemble analysis protocol. | Upstream documents cryoDRGN 0.3.2 compatibility and dependencies on RELION, Chimera, and ChimeraX. A bounded example and output contract are also required. |
| ResMap | gated | Local-resolution validation comparator. | Public source advertises CC BY-NC-ND terms. Do not include it in public images without terms review. |
| MonoRes / MonoDir | watch | Local and local-directional resolution validation through Scipion/Xmipp. | Plugin terms and output contract need review. |
| FSC-Q | watch | Local map-to-model support and overfitting signal through Scipion/Xmipp. | Plugin terms and small map/model fixture needed. |
| InSilicoTEM `v2.1.0` | watch | Synthetic TEM image fixtures for demos or regression tests. | GitHub metadata does not identify a license. Review MATLAB and DIPimage runtime terms. |

## Watch Notes

These candidates were reviewed but not added to the registry:

| Candidate | Reason |
| --- | --- |
| TEM Simulator | Source, build, and license posture need a primary-source audit before a registry entry. |
| cisTEM `simulate` | The broader cisTEM watch entry covers this command. Review the exact cisTEM terms first. |
| APPLE picker and CWF denoise | Potential ASPIRE-adjacent baselines, but lower priority than ASPIRE-Python itself. |
| NoiseTransfer2Clean, Restore, JANNI | Denoising references with lower priority than Miffi, Topaz, MicrographCleaner, and DenoisET. |
| CryoSPARC 3DVA / 3DFlex | Heterogeneity workflows that inherit the CryoSPARC runtime gate. |

## Sources Checked

- Computational-CryoEM: https://github.com/phonchi/Computational-CryoEM
- cryoDRGN: https://github.com/ml-struct-bio/cryodrgn
- cryoDRGN releases: https://github.com/ml-struct-bio/cryodrgn/releases
- cryoDRGN PyPI: https://pypi.org/project/cryodrgn/
- ASPIRE-Python: https://github.com/ComputationalCryoEM/ASPIRE-Python
- ASPIRE-Python docs: https://computationalcryoem.github.io/ASPIRE-Python/
- Miffi: https://github.com/ando-lab/miffi
- Miffi paper: https://pubmed.ncbi.nlm.nih.gov/38431179/
- MAVEn: https://github.com/lkinman/MAVEn
- EMAN2: https://github.com/cryoem/eman2
- EMAN2 e2gmm: https://blake.bcm.edu/emanwiki/EMAN2/e2gmm
- ResMap: https://resmap.sourceforge.net/
- ResMap source mirror: https://github.com/akucukelbir/resmap
- MonoRes Scipion protocol: https://scipion-em.github.io/docs/release-3.0.0/docs/user/tutorials/modelBuilding/a102-localMonoRes.html
- MonoDir paper: https://www.nature.com/articles/s41467-019-13742-w
- FSC-Q paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC7782520/
- Scipion/Xmipp plugin: https://github.com/I2PC/scipion-em-xmipp
- InSilicoTEM: https://github.com/M4I-nanoscopy/InSilicoTEM
