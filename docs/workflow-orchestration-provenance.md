# Workflow Orchestration And Provenance

CryoCore stays provider-neutral. RunPod, local workstations, Slurm/HPC, AWS
Batch, and generic cloud VMs are execution planes. The source of truth lives
in fetched artifacts, contracts, and ledgers, wherever the execution happens.

## Recommended Stack

- Canonical workflow lane: Nextflow DSL2 profiles for `local`, `runpod`,
  `aws_batch`, `ssh_hpc_slurm`, and `generic_cloud`.
- Secondary workflow lane: Snakemake profiles for small demos, local Python
  checks, and Slurm-friendly fixtures.
- HPC container lane: Apptainer/Singularity-compatible SIF files with hashes.
- Evidence packaging: RO-Crate metadata plus BagIt-style checksum manifests,
  joined to the existing `artifact-index.v1` contract.
- Container provenance: OCI image digest or SIF SHA256, SBOM path, SLSA-style
  provenance when available, and `versions.json`.
- Observability: OpenTelemetry logs/spans are useful diagnostics, but telemetry
  cannot upgrade a claim level.

## Required Runtime Metadata

Every nontrivial workflow run should record:

- workflow engine and version
- workflow source ref or commit
- profile and executor
- container runtime and image digest or SIF hash
- task trace path
- work directory and output root
- resume/cache mode
- exit status
- stage-progress ledger
- artifact index and hashes
- tool versions
- license gates and operator approvals when applicable

## Non-Goals

- Do not store raw cryo-EM movies, maps, half-maps, masks, particle stacks,
  model weights, license files, or secrets in git.
- Do not make DVC, DataLad, lakeFS, or any object-store system mandatory for
  raw data. They are useful for metadata, pointers, and approved derived
  artifacts only.
- Do not treat a workflow engine's `completed` state as scientific success.
  Success requires evidence joined to declared inputs and validation outputs.
- Do not require a Kubernetes-native lineage platform unless future scale makes
  the operational cost worthwhile.

## First Integration Wave

1. Add `workflow-run.v1` and `container-provenance.v1` schemas.
2. Add templates for workflow summaries, RO-Crate metadata, BagIt info, and SBOM
   indexes.
3. Add checks that reject promoted runs without workflow trace, artifact index,
   checksums, and container provenance.
4. Add Nextflow and Snakemake profiles only after the current manifest contracts
   are stable enough to map each stage cleanly.
