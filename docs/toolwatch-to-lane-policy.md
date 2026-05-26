# Toolwatch To Lane Policy

Toolwatch findings become useful only when they map to CryoCore lanes, gates,
and artifacts. This policy keeps new software from becoming an implicit runtime
dependency before its terms and evidence value are clear.

## Lane Mapping

| Lane | Default tools | Gated or watch tools | Minimum useful artifacts |
| --- | --- | --- | --- |
| Raw movie to map | RELION, Warp/M, MotionCor3, Topaz, CTFFIND after terms review | CryoSPARC, MotionCor2, crYOLO, nextPYP dependencies | `map_processing_manifest.json`, motion QC, CTF QC, pick manifest, refinement outputs, versions |
| CTF and preprocessing QC | MotionCor3, CTFFIND, MicrographCleaner | Gctf, proprietary picker stacks | `ctf_estimation_manifest.json`, contamination masks, command ledger |
| Map to model | ModelAngelo, CryoAtom2, gemmi | Phenix, CCP-EM/Buccaneer, CryoREAD, DiffModeler, DAQ | `model_build_manifest.json`, sequence/entity manifest, model, validation summary |
| Validation | EMDA, 3D-Strudel, public wwPDB/RCSB reports, MapQ parsing | Phenix validation, OneDep upload, CCP-EM suite | geometry, FSC, local fit metrics, deposition reports, caveats |
| Heterogeneity | cryoDRGN, DynaMight, CryoBench metrics | RECOVAR, CryoSPARC 3DVA/3DFlex, SOLVAR watch | latent/state manifests, state maps, subset rationale, disagreement matrix |
| Figure dossier | Mol*, MolViewSpec, py3Dmol, open-source PyMOL, Blender | ChimeraX, Incentive PyMOL, VMD | scene/viewer state, scripts, sessions, captions, hashes |
| Workflow provenance | Nextflow, Snakemake, Apptainer, RO-Crate, BagIt | hosted/enterprise data-lineage platforms | workflow trace, image/SIF digest, SBOM, artifact index |

## Promotion Rules

To move from `watch` to `planned`, a tool needs:

- primary source links for code/docs/paper
- license and redistribution posture
- install/runtime requirements
- smoke command or API check
- expected artifacts
- clear evidence value in one CryoCore lane

To move from `planned` to a default scaffold, it also needs:

- source-pinned version or release
- no required secrets, raw data, license files, or model weights in git
- local validator coverage or an issue template with acceptance checks
- documented failure/caveat behavior

To run a `gated` tool:

- record operator approval, license posture, budget/provider if applicable,
  source versions, runtime location, and cleanup expectations
- emit gate records and artifact hashes
- downgrade the outcome if a fallback or partial run is used

## Audit Note Convention

When updating tool posture, add a dated note in the relevant doc or registry
entry with:

- source checked
- date checked
- version or commit
- license delta
- lane impact
- next issue or blocker
