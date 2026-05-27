# CryoCore Toolwatch 2026-05-27

This note updates the May 15 toolwatch with cryo-EM and cryo-ET tools,
preprints, repositories, and data-source posture checked on May 27, 2026.

It is a triage record, not approval to install, run, upload, download, or
redistribute gated software, raw movies, particle stacks, maps, tomograms,
model weights, private structures, license files, or unpublished data.

## What Changed

| Area | Candidate | Posture | Source-backed signal | CryoCore use |
| --- | --- | --- | --- | --- |
| Raw SPA | CryoSPARC `v5.0.6` | gated | Public CryoSPARC site listed `v5.0.6` as latest on May 5, 2026. | Strong gated raw-processing route if license and runtime access are cleared. |
| Raw SPA | CryoSPARC Tools `v5.0.3` | planned | GitHub lists BSD-3-Clause and latest release `v5.0.3` on May 4, 2026. | Metadata export and scripting adapter when CryoSPARC access is already cleared. |
| Raw SPA | Topaz `0.3.20` | planned | PyPI lists `topaz-em 0.3.20` on May 11, 2026. | Open particle-picking lane for raw SPA runs. |
| Raw SPA | CryoFSL | watch | MIT repo uses SAM2 Hiera-Large weights for few-shot particle picking. | Small picking run from annotated micrographs if checkpoint terms are recorded. |
| Raw SPA | ParSeek | watch | May 11 bioRxiv preprint reports synthetic-data particle picking; no public code found in this scan. | Track as a possible Topaz comparison, not a first run. |
| Heterogeneity | Cas9 heterogeneous reconstruction benchmark | watch | May 7 and May 11 bioRxiv preprints report experimentally grounded labels and limited method classification accuracy. | High-signal benchmark candidate if data access is bounded. |
| Heterogeneity | CryoARC | watch | May 26 bioRxiv preprint and GPLv3 GitLab repo. | Conformational-landscape method; dependency and data footprint must be pinned first. |
| Heterogeneity | CryoHype | watch | CVPR 2026 project and GPLv3 repo. | Compositional heterogeneity research lane, not a default runtime. |
| Heterogeneity | CryoDECO | watch | GPLv3 repo uses Cryo-IEF priors and CryoSPARC particle inputs. | Comparison lane after weight and CryoSPARC gates are cleared. |
| Heterogeneity | CryoWizard | gated | MIT repo, academic-only README language, CryoSPARC automation. | Automation reference only until CryoSPARC, model, and secret gates are explicit. |
| Heterogeneity | DynaMight | planned | Nature Methods and package metadata describe BSD distribution. | Planned RELION-linked deformation and motion lane. |
| Cryo-ET | AreTomoLive | planned | Nature Methods paper published May 25, 2026. | Live tilt-series preprocessing and denoising pattern for bounded public data. |
| Cryo-ET | DenoisET | planned | MIT repo with pretrained models and AreTomoLive paper. | Denoising lane; outputs are derived evidence. |
| Cryo-ET | Easymode | watch | May 21 bioRxiv preprint, PyPI GPLv3 package, SBGrid package about 4.9 GB. | Cellular feature segmentation; model-weight posture needs review. |
| Cryo-ET | copick | planned | Current docs describe storage-agnostic cryoET project API, CZDP, Napari, ChimeraX, and MCP paths. | Default project and annotation glue for bounded cellular cryoET workflows. |
| Cryo-ET | MissAlignment | watch | May 2 preprint and May 13 `v0.1.6` release. | ML alignment-refinement comparison after AreTomo3 baseline. |
| Cryo-ET | PP7 cryoET standard | watch | May 22 bioRxiv preprint proposes an in situ cryoET standard. | Track for benchmark data availability. |
| Map to model | ModelAngelo `v1.0.17` | planned | May 18 release includes nucleotide postprocessing alignment fixes. | First-pass builder for RNA/DNA/protein map-to-model runs. |
| Map to model | CryoAtom2 `v2.1.0` | planned | March 17 release, MIT, multi-GPU posture. | Second builder for protein/RNA/DNA complexes. |
| Map to model | CryoREAD | gated | Kihara nucleic-acid builder, GPLv3 plus commercial-contact language. | RNA-specific builder if use context is cleared. |
| Map to model | CryoNet.Refine | watch | ICLR 2026 code pushed May 20, MIT. | Stretch refinement lane after reproducibility tests. |
| Map to model | PhenixCraft | watch | May 6 arXiv method pattern, no runnable code found. | Track as Phenix plus predicted-model idea, not a runtime. |
| Map to model | StructAgent | watch | May 18 bioRxiv preprint and Apache-2.0 repo for agent-guided model building and validation. | Orchestration reference; workflows should still run concrete cryo-EM tasks. |
| Validation | wwPDB validation reports | planned | Public XML/PDF reports are available for released PDB entries. | Default first validation source before local recompute. |
| Map enhancement | EMReady2 | watch | Nature Communications paper published May 16, 2026. | Derived-map lane only; never replaces original-map validation. |
| Calibration | WebCalEM | watch | May 26 bioRxiv preprint. | Pixel-size calibration signal; hosted upload needs review. |
| Dataset | cryoPANDA | watch | May 3 preprint reports 37M annotated particles from 252 experiments. | Future ML benchmark metadata, not a repo asset. |

## Promotion Notes

- Promote DynaMight license posture to open BSD only with exact source and
  dependency capture in the runtime image.
- Keep CryoARC on watch until OpenFold or AlphaFold parameters, MSA/database
  paths, and example data size are recorded.
- Keep CryoDECO and CryoWizard gated by Cryo-IEF weight terms, CryoSPARC
  access, and secret-handling posture before any run.
- Keep Easymode on watch until pretrained model terms, hashes, package sources,
  and package size are recorded.
- Keep EMReady2 and DenoisET outputs at derived-evidence level unless original
  maps, weights, parameters, and independent validation are joined.
- Keep CTFFIND5 planned/gated until exact Janelia source or binary terms are
  recorded.
- Treat CryoSPARC and Phenix as runtime-gated even when adapters or public
  reports are planned.

## Sources Checked

- CryoSPARC: https://cryosparc.com/
- CryoSPARC Tools: https://github.com/cryoem-uoft/cryosparc-tools
- CryoSPARC guide: https://guide.cryosparc.com/setup-configuration-and-management/software-updates
- RELION releases: https://github.com/3dem/relion/releases
- Warp README: https://github.com/warpem/warp/blob/main/README.md
- Topaz PyPI: https://pypi.org/project/topaz-em/
- CryoFSL: https://github.com/biplabpoudel25/CryoFSL
- ParSeek: https://doi.org/10.64898/2026.05.07.720949
- cryoDRGN PyPI: https://pypi.org/project/cryodrgn/4.2.1/
- CryoDECO: https://github.com/yanyang1998/CryoDECO
- CryoWizard: https://github.com/SMART-StructBio-AI/CryoWizard
- DynaMight: https://www.nature.com/articles/s41592-024-02377-5
- CryoARC: https://doi.org/10.64898/2026.05.25.727696
- CryoARC GitLab: https://gricad-gitlab.univ-grenoble-alpes.fr/GruLab/cryoarc
- CryoHype: https://cryohype.cs.princeton.edu/
- CryoHype repo: https://github.com/ml-struct-bio/cryoHYPE
- AreTomoLive: https://www.nature.com/articles/s41592-026-03093-y
- AreTomo3: https://github.com/czimaginginstitute/AreTomo3
- DenoisET: https://github.com/apeck12/denoiset
- Easymode PyPI: https://pypi.org/project/easymode/
- Easymode preprint: https://doi.org/10.64898/2026.05.19.726344
- Easymode SBGrid: https://sbgrid.org/software/titles/easymode
- copick: https://copick.github.io/copick/
- MissAlignment: https://github.com/warpem/miss-alignment
- WebCalEM: https://doi.org/10.64898/2026.05.26.726020
- PP7 cryoET standard: https://doi.org/10.64898/2026.05.20.726049
- ModelAngelo: https://github.com/3dem/model-angelo/releases
- CryoAtom: https://github.com/YangLab-SDU/CryoAtom/releases
- CryoREAD: https://github.com/kiharalab/CryoREAD
- CryoNet.Refine: https://github.com/kuixu/cryonet.refine
- PhenixCraft: https://arxiv.org/abs/2605.05259
- StructAgent: https://www.biorxiv.org/content/10.64898/2026.05.18.725842v1
- StructAgent repo: https://github.com/bhgtiger/StructAgent
- EMReady2: https://www.nature.com/articles/s41467-026-71794-1
- Cas9 benchmark: https://www.biorxiv.org/content/10.64898/2026.05.04.721978v1
- Cas9 method accuracy: https://www.biorxiv.org/content/10.64898/2026.05.08.722747v1
- cryoPANDA: https://www.biorxiv.org/content/10.64898/2026.04.29.720997v1
