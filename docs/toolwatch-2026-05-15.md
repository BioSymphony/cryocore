# CryoCore Toolwatch 2026-05-15

This note records current useful tools, repos, services, and preprints for
BioSymphony CryoCore. It is a triage document, not approval to install, run, or
redistribute any gated software, model weights, raw movies, maps, or private
data.

## Decision Rules

- `planned` means useful enough for docs, manifests, smoke checks, or public-safe
  adapters after normal license/source review.
- `gated` means public docs and placeholders are useful, but execution,
  packaging, upload, or redistribution needs an explicit operator/license gate.
- `watch` means scientifically relevant but not yet a dependable production
  dependency for evidence closeout.
- Provider status and ML-generated outputs are not evidence by themselves.
  Claims still require input joins, tool versions, hashes, validation artifacts,
  and caveats.

## Highest Value Additions

| Area | Candidate | Posture | Why it helps CryoCore | Source |
| --- | --- | --- | --- | --- |
| Atomic model building | CryoAtom2 | planned | MIT repo; protein, RNA, DNA, masked local builds, sequence-free and sequence-DB modes; newer complement to ModelAngelo. | https://github.com/YangLab-SDU/CryoAtom |
| Atomic model building | DiffModeler / ComplexModeler | gated | Intermediate-resolution complex modeling with diffusion tracing and predicted-model fitting; Kihara licensing requires use-context review. | https://github.com/kiharalab/DiffModeler |
| Atomic model building | CryoREAD | gated | Dedicated nucleic-acid model building for cryo-EM maps. | https://kiharalab.org/emsuites/cryoread.php |
| Model quality | DAQ score / DAQ refine | gated | Residue-wise map/model compatibility scores for claim ledgers; local code/assets need exact terms review. | https://kiharalab.org/emsuites/daq.php |
| Validation | 3D-Strudel | planned | Apache-2.0 map-feature validation around 2-4 A; useful local outlier panels. | https://www.ebi.ac.uk/emdb/strudel |
| Validation | EMDA | planned | MPL-2.0 map/model FSC, local correlation, difference-map utilities. | https://emda.readthedocs.io/en/latest/index.html |
| Validation | MapQ / Q-score | planned/gated | MIT plugin; public reports can be parsed, local recompute inherits Chimera/ChimeraX posture. | https://github.com/gregdp/mapq |
| Validation | wwPDB / RCSB validation APIs | planned/gated | Public validation report ingestion for released entries; upload of unpublished/private files needs explicit approval. | https://www.wwpdb.org/validation/validation-reports |
| Heterogeneity | DynaMight | planned | RELION 5 flexibility lane with deformation/backprojection evidence; complements cryoDRGN/RECOVAR. | https://github.com/3dem/DynaMight |
| Heterogeneity | CryoBench | planned | Benchmark datasets and metrics for state/ensemble claim calibration. | https://cryobench.cs.princeton.edu/ |
| Heterogeneity | SOLVAR | watch | 2026 covariance/pose-refinement method; repo exists but license must be clarified before packaging. | https://arxiv.org/abs/2602.17603 |
| Preprocessing | nextPYP | planned | End-to-end cryo-EM/ET workflow platform with Apptainer/HPC fit; dependencies need individual gates. | https://nextpyp.app/ |
| Preprocessing | CTFFIND5 | planned/gated | Improved CTF/tilt/thickness estimation; redistribution posture must be checked before image inclusion. | https://elifesciences.org/articles/97227 |
| Preprocessing | cisTEM | planned/gated | Independent SPA pipeline and cross-check lane; Janelia terms must be recorded. | https://cistem.org/ |
| Preprocessing | Scipion/Xmipp | planned/gated | Provenance, format conversion, many plugin integrations; plugin execution remains mixed-license. | https://scipion-em.github.io/docs/release-3.0.0/ |
| Preprocessing | pyem / csparc2star | planned | High-leverage metadata conversion between cryoSPARC and RELION. | https://github.com/asarnow/pyem |
| Preprocessing | AreTomo3 | planned | Real-time cryoET tilt-series preprocessing/reconstruction. | https://github.com/czimaginginstitute/AreTomo3 |
| Preprocessing | MicrographCleaner | planned | Contamination/carbon mask helper before picking and QC. | https://github.com/rsanchezgarc/micrograph_cleaner_em |
| Public data | EMPIAR REST API | planned | Public raw-data metadata and accession checks without storing raw assets. | https://www.ebi.ac.uk/empiar/ |
| Public data | EMDB REST API / EMICSS | planned | Map metadata, validation-analysis pointers, cross-resource annotations. | https://www.ebi.ac.uk/emdb/api/ |
| Public data | RCSB PDB Data API | planned | Structure metadata, validation report fields, GraphQL/REST enrichment for dossiers. | https://data.rcsb.org/ |
| Visualization | MolViewSpec | planned | Declarative Mol* scenes for reproducible web dossiers. | https://academic.oup.com/nar/article/53/W1/W408/8125619 |
| Visualization | py3Dmol / 3Dmol.js | planned | Lightweight notebook/static HTML molecular panels. | https://3dmol.org/ |
| Visualization | open-source PyMOL | planned | Scripted publication figures without Incentive license files. | https://github.com/schrodinger/pymol-open-source |
| Workflow | Nextflow | planned | Provider-neutral profiles for local, Slurm, AWS Batch, cloud, and containers. | https://github.com/nextflow-io/nextflow |
| Workflow | Snakemake | planned | Python-native local/HPC reproducibility for smaller demos and fixtures. | https://github.com/snakemake/snakemake |
| Workflow | Apptainer | planned | HPC-safe container runtime with SIF hashes for non-Docker environments. | https://github.com/apptainer/apptainer |
| Provenance | RO-Crate / BagIt / SBOM / SLSA | planned | Durable evidence bundles, fixity manifests, and container provenance. | https://www.researchobject.org/ro-crate/ |

## Gated But Useful

- CryoSPARC and CryoSPARC Live remain high-value production tools, but runtime
  and commercial use are gated. `cryosparc-tools` can be a planned metadata
  adapter if its BSD-3-Clause posture is pinned.
- Phenix remains the canonical gated refinement/validation suite. Expand docs
  around `phenix.validation_cryoem`, `phenix.map_to_model`,
  `phenix.predict_and_build`, `phenix.real_space_refine`, and `mtriage`.
- ChimeraX remains gated but should be treated as a scripted renderer/review
  runtime: `.cxc` scripts, `--offscreen`, saved `.cxs`, Toolshed bundle
  inventory, exact version, and command ledger.
- CCP-EM/Buccaneer, VMD/NAMD/MDFF, crYOLO, RECOVAR current main, and Kihara
  suite tools need exact per-campaign use-context records.
- Large model weights for CryoAtom, ModelAngelo, CryoFM, Cryo-IEF, CryoWizard,
  and similar tools belong in runtime caches, volumes, or reviewed image layers
  with hashes, never in git.

## Preprints And Watchlist

These are worth tracking, but should not close scientific claims without
independent validation and license/runtime review.

| Candidate | Why watch | Why not productionize yet | Source |
| --- | --- | --- | --- |
| CryoFM | Apache-2.0 density foundation model for denoising, inpainting, anisotropy correction, and style enhancement. | Foundation-model outputs can alter apparent map quality; require explicit derived-map caveats and weight hashes. | https://github.com/ByteDance-Seed/cryofm |
| Cryo-IEF / CryoWizard / CryoDECO | Foundation model for image evaluation plus automated processing/ranking pipelines. | Interfaces with CryoSPARC and large weights; needs tool-by-tool license and evidence-gate review. | https://github.com/westlake-repl/Cryo-IEF |
| CryoNet.Refine | 2026 diffusion refinement preprint/code claims faster model-map refinement. | Needs local reproducibility, stereochemistry stress tests, and license confirmation. | https://arxiv.org/abs/2602.22263 |
| PhenixCraft | 2026 preprint for AlphaFold-assisted Phenix map segmentation/model building. | Preprint stage; determine whether it is a method pattern or a distributable tool. | https://arxiv.org/abs/2605.05259 |
| CryoHype | Large-scale compositional heterogeneity with transformer hypernetworks. | Research benchmark method; not an operator-ready evidence lane. | https://cryohype.cs.princeton.edu/ |
| CryoPANDA | Large annotated particle dataset preprint for data-driven cryo-EM analysis. | Dataset size and redistribution/access terms need review; use metadata pointers first. | https://preprints.epiforecasts.io/paper/10.64898/2026.04.29.720997 |
| CryoFSL | Few-shot SAM2 particle picking. | Model/data terms and local smoke tests needed before planned status. | https://pmc.ncbi.nlm.nih.gov/articles/PMC12458156/ |
| CryoSift | CNN 2D class selection and automated processing workflow. | Validate code/packaging and avoid over-trusting class rank output. | https://journals.iucr.org/f/issues/2025/12/00/ih5009/ |
| CryoFastAR | Fast ab initio reconstruction, but noncommercial/split licensing. | License blocks public/default runtime use. | https://github.com/Cellverse/CryoFastAR |
| CryoGEM / GEM / CryoGS | Neural/Gaussian reconstruction representations. | Method-development watch; not yet a default raw-to-map evidence lane. | https://github.com/Cellverse/CryoGEM |

## Repo Actions

1. Keep `references/software-registry.yaml` broad but conservative: add
   `planned` entries only for tools with clear public source/terms and immediate
   CryoCore value; use `gated` or `watch` when in doubt.
2. Add workflow provenance contracts: workflow engine/version/ref, executor,
   profile, container runtime, trace path, image digest or SIF hash, SBOM path,
   and tool versions.
3. Split map/model validation into explicit outputs: geometry, global FSC,
   model-map FSC, local CC, Q-score/Strudel/SMOC-like local metrics, deposition
   report IDs, source hashes, and caveats.
4. Add public accession metadata helpers for EMPIAR, EMDB, PDBe, RCSB, and
   wwPDB validation reports. These should emit JSON ledgers and never download
   raw movies or maps unless an operator gate allows it.
5. Add reusable repo-local skills so future agents can repeat toolwatch,
   closeout, map/model dossier, heterogeneity, and figure workflows with the
   same planned/gated/watch discipline.
