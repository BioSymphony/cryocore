# CryoCore Toolwatch 2026-06-21

This note records a targeted June 21, 2026 scan for cryo-EM, cryo-ET,
agent-facing project APIs, and workflow provenance tools that fit CryoCore.

The update is small. Entries were added or refreshed only when they help a new
agent run, inspect, package, or compare public cryo-EM/cryo-ET work:

- public cryo-ET intake and project APIs
- map/model refinement and review helpers
- workflow provenance, fixity, SBOM, and attestation checks
- agent-operated visualization references

Paper-only methods and young bridges remain watch notes until there is a clear
runnable path, a bounded public benchmark, or a source-backed license posture.

## Registry Updates

| Area | Candidate | Posture | Useful update | CryoCore use |
| --- | --- | --- | --- | --- |
| Map/model build | ModelAngelo `v1.0.18` | planned | June release updates install-script termination; `v1.0.17` nucleotide fixes remain relevant. | First-pass model building with version and weight hashes recorded. |
| Map/model refine | Servalcat `0.4.131` | planned | MPL-2.0 refinement and map/model scoring tool for SPA. | Lightweight refinement and reporting lane; Refmac/CCP4 calls remain gated. |
| Figures/review | Agentic PyMOL `v1.0.0` | watch | MIT MCP bridge for a live PyMOL session with structured readback. | Reference pattern for agent-operated figure and structure review tasks. |
| Cryo-ET intake | CryoET Data Portal client `4.8.0` | planned | Public Python client with PyPI hashes and provenance metadata. | Default public cryo-ET metadata and bounded dataset discovery path. |
| Cryo-ET project API | copick `v1.24.1` | planned | Registry now points to the current `copick/copick` repo. | Project and annotation glue for public CZDP or OME-Zarr examples. |
| Cryo-ET agent API | copick-MCP `v0.6.0` | planned | MCP server for read-only project exploration and CLI introspection. | Lets an agent inspect copick projects and discover commands before running tools. |
| Cryo-ET benchmark | POPSICLE | watch | June arXiv benchmark built from CryoET Data Portal datasets. | Regression fixture for segmentation and localization skills; data stays outside git. |
| Cryo-ET picking | OCTOPI `v1.6.0` | planned | MIT copick-native 3D particle-picking package from CZI. | Public-data particle-picking lane after a small fixture is pinned. |
| Cryo-ET STA | py2rely `v0.1.0` | gated | MIT adapter from AreTomo and copick metadata into RELION5 STA. | HPC/SLURM adapter when RELION and dependency posture are already clear. |
| Cryo-ET picking | pytom-match-pick `0.13.2` | planned | GPL-2 GPU template matching package. | Non-ML particle-localization baseline for tomogram tasks. |
| Cryo-ET heterogeneity | tomoDRGN `v1.0.3` | watch | GPL-3 cryoDRGN-style heterogeneity analysis for subtomograms. | Future in situ heterogeneity lane after a small public fixture is tested. |
| Workflow provenance | Workflow Run RO-Crate `0.5.0` | planned | June profile adds a stronger target for run, step, resource, and output records. | Target format for long-running agent workflow packets. |
| Workflow provenance | `nf-prov` `1.7.0` | planned | Nextflow plugin emits BioCompute Object and Workflow Run RO-Crate outputs. | First concrete Nextflow provenance adapter when a workflow lane is active. |
| Provenance checks | `rocrate-validator` `0.10.0` | planned | Apache-2.0 validator for generated RO-Crates. | Release and run-closeout check when a crate is produced. |
| Fixity | `bagit-python` `1.9.0` | planned | CC0 Python implementation for BagIt create/validate flows. | Checksum packaging for exported artifacts and transfer bundles. |
| Containers | Apptainer `v1.5.1` | planned | June release supports reproducible SIF build posture. | HPC container record with SIF hashes and runtime provenance. |
| SBOM | Syft `v1.45.1` | planned | Apache-2.0 SBOM generator for images and filesystems. | Public image and artifact-bundle inventory. |
| Signatures | Cosign | planned | Apache-2.0 signing and verification tool for OCI artifacts and binaries. | Verify images by digest and record signature checks. |
| Provenance checks | SLSA verifier `v2.7.1` | planned | Apache-2.0 verifier for SLSA-compliant build provenance. | Check artifact provenance where upstream supplies attestations. |
| Cryo-ET segmentation | Easymode | watch | Registry now records the public GitHub install path as well as PyPI/SBGrid posture. | Cellular feature segmentation watch lane with weight and package-size gates. |

## Watch Notes

These were useful to know about and stayed out of the registry in this pass:

| Candidate | Current posture | Reason |
| --- | --- | --- |
| CryoDiff | watch | June map-enhancement preprint; no public code found in this scan. |
| 3dcon | watch | June tomogram denoising preprint; wait for source, terms, and fixture. |
| DMcloud | watch | Local map-fitting preprint; no runnable package found in this scan. |
| Multiscale conformations from cryo-EM images | watch | June arXiv method; research signal with no tool lane yet. |
| CryoDRGN-AI / `drgnai` | watch | Useful ab initio reconstruction direction; needs runtime and dependency review before a public lane. |
| AR-Decon | watch | Promising non-ML deconvolution path; add after release and fixture posture are clearer. |
| CryoFM / CryoLVM / CryoNet.Refine | watch | Already tracked as map-enhancement/refinement directions where weights and downstream checks matter. |
| SABER, TopCUP, TomoSwin3D, MemBrain | watch | Relevant cryo-ET segmentation/picking tools, but less useful than copick, OCTOPI, and pytom-match-pick for a first public agent lane. |
| cryoAgent and CryoWizard | watch/gated | Agentic cryo-EM automation references; execution inherits third-party tool and license gates. |
| ChimeraX MCP server | watch | Useful bridge idea, but young and still inherits ChimeraX terms. |
| Snakemake RO-Crate report plugin | watch | Interesting provenance adapter; upstream production posture is not ready. |
| PROV-AGENT and schema-gated scientific-agent preprints | docs watch | Good concepts for agent ledgers; no runtime dependency needed. |

## Sources Checked

- ModelAngelo releases: https://github.com/3dem/model-angelo/releases
- Servalcat: https://github.com/keitaroyam/servalcat
- Agentic PyMOL: https://github.com/Arcadia-Science/agentic-pymol/tree/v1.0.0
- Agentic PyMOL publication: https://thestacks.org/publications/resource-agentic-pymol
- CryoET Data Portal: https://cryoetdataportal.czscience.com/
- CryoET Data Portal repo: https://github.com/chanzuckerberg/cryoet-data-portal
- CryoET Data Portal PyPI: https://pypi.org/project/cryoet-data-portal/
- copick: https://github.com/copick/copick
- copick-MCP: https://github.com/copick/copick-mcp
- POPSICLE: https://arxiv.org/abs/2606.10255
- OCTOPI: https://github.com/chanzuckerberg/octopi
- py2rely: https://github.com/chanzuckerberg/py2rely
- pytom-match-pick: https://github.com/SBC-Utrecht/pytom-match-pick
- tomoDRGN: https://github.com/bpowell122/tomodrgn
- Workflow Run RO-Crate profile: https://www.researchobject.org/workflow-run-crate/profiles/provenance_run_crate/
- Workflow Run RO-Crate releases: https://github.com/ResearchObject/workflow-run-crate/releases
- nf-prov: https://github.com/nextflow-io/nf-prov
- nf-prov registry: https://registry.nextflow.io/plugins/nf-prov%401.7.0
- rocrate-validator: https://github.com/crs4/rocrate-validator
- bagit-python: https://github.com/LibraryOfCongress/bagit-python
- Apptainer releases: https://github.com/apptainer/apptainer/releases
- Syft: https://github.com/anchore/syft
- Cosign: https://github.com/sigstore/cosign
- SLSA verifier: https://github.com/slsa-framework/slsa-verifier
- Easymode: https://github.com/mgflast/easymode
- CryoDiff: https://www.biorxiv.org/content/10.64898/2026.06.04.730282v1.full-text
- 3dcon: https://www.biorxiv.org/content/10.64898/2026.06.15.732138v1.full.pdf
- DMcloud: https://www.biorxiv.org/content/biorxiv/early/2026/06/16/2026.06.12.731990.full.pdf
- Multiscale conformations: https://arxiv.org/abs/2606.18058
