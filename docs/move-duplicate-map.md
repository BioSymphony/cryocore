# Move And Duplicate Map

Last reviewed: 2026-05-15

This is the first-pass shape for splitting CryoCore from Structure Factory without breaking existing campaigns.

## Move Later

Move these only after this repo has matching validators and an active issue:

- `campaigns/cryoem-raw-to-atomic-dossier/`
- cryo-only RunPod no-download smoke manifests
- raw-subset and map/model dossier stage contracts
- cryo-core bootstrap pieces that install RELION, Warp/M, MotionCor3, Topaz, and related tools
- map/model validation utilities whose inputs are deposited maps and models rather than RFdiffusion, Boltz, Chai, or MPNN outputs

## Duplicate Intentionally

Duplicate small public-safe contracts where both repos need local context:

- ChimeraX posture and gates
- ChimeraX and generic gemmi/Mol*/Blender visualization posture
- CryoCore-owned ModelAngelo/Coot/Phenix posture for model building and refinement
- public/private image policy for shared tools
- operator-gate templates for license-sensitive render lanes
- artifact-contract schema fragments for `map_model_dossier`, `figure_dossier`, and `claim_ledger`

ChimeraX is intentionally in both repos. In CryoCore it supports map/model review and experimental figure dossiers. In Structure Factory it supports design- and atlas-facing visualization. Neither repo should store ChimeraX installers, binaries, license IDs, or accepted-license notes in tracked files.

## Leave In Structure Factory

Keep these in Structure Factory unless a separate issue says otherwise:

- RFdiffusion execution
- Boltz and Chai prediction execution
- ProteinMPNN/LigandMPNN design execution
- Genie-style generation stacks
- screening, binder-design, model-jury synthesis, and design-candidate promotion logic
- campaign reports whose primary claim is design or prediction rather than experimental evidence

## Shared Handoff

Use file-level contracts rather than shared code imports:

```text
CryoCore output bundle
  artifact_manifest.json
  input_audit.json
  validation_summary.json
  claim_ledger.md
  figures/
  methods.md

Structure Factory input pointer
  source_repo
  source_commit
  artifact_manifest_sha256
  accepted_claim_level
  downstream_use
```

## Synchronization Rule

When a duplicated tool posture changes in one repo, update the other repo or add a dated note explaining why the divergence is intentional. A source-backed audit date is required in CryoCore for RELION, Warp/M, MotionCor3, ModelAngelo, ChimeraX, cryoDRGN, RECOVAR, and any gated model/refinement tool. Structure Factory only needs synchronized dates for tools it actively carries, such as ChimeraX and generic visualization/parser lanes.

## Related

- [Split Evaluation](split-evaluation.md): the rationale for the two-repo split this map operationalizes.
- [ChimeraX Shared Posture](chimerax-shared-posture.md): the worked posture record for the most-shared license-gated tool.
- [Tooling and Licensing](tooling-and-licensing.md): per-tool license posture that informs cross-repo placement.
