# BioSymphony CryoCore Agent Guide

This repo is the public BioSymphony CryoCore control plane. It owns cryo-EM evidence production, map/model validation, heterogeneity review, and structural rendering lanes that should not be coupled to AI design runtimes.

## Operating Rules

- Keep durable design docs in `docs/`.
- Keep campaign specs in `campaigns/<campaign-id>/`.
- Keep public-safe example manifests and tiny fixtures in `examples/`.
- Keep reusable module contracts in `modules/`.
- Keep tool and licensing posture in `references/software-registry.yaml` and `docs/tooling-and-licensing.md`.
- Keep reusable scripts under `scripts/cryocore/`.
- Use `templates/linear-issue.md` when drafting tracker-neutral external-agent issues.
- Record durable learnings (tool surprises, failed paths, provider gotchas, doctrine corrections) in `.cryocore-memory/` in this checkout (gitignored, never committed) or in your harness's own memory store. See [Agent Memory And Learnings](docs/agent-skill-guide.md#agent-memory-and-learnings) for scope, exclusions, harness pointers, and the note shape at `skills/cryocore/references/memory-note-template.md`.
- Do not store API keys, tokens, raw cryo-EM movies, maps, half-maps, private structures, unpublished sequences, model weights, license files, or heavy outputs in this repo.
- Store heavy outputs under ignored directories such as `.runtime/`, `artifacts/`, `outputs/`, provider volumes, or secure local storage.
- Treat ChimeraX as intentionally duplicated with Structure Factory: runtime-gated, noncommercial/commercial-license posture recorded per campaign, and never redistributed in this public repo.

## Ownership Boundary

CryoCore owns:

- raw cryo-EM movie intake contracts
- motion correction, CTF, picking, classification, refinement, and map postprocessing plans
- map/model validation and atomic model build lanes
- heterogeneity and conformational-state evidence lanes
- ChimeraX/Coot/PyMOL/Blender/Mol* figure and review scaffolding
- provider-neutral cryo-EM execution contracts for local, RunPod, AWS Batch, SSH/HPC, and neocloud-style backends

CryoCore does not own:

- RFdiffusion/Boltz/Chai/ProteinMPNN design execution stacks
- screening or binder-design campaign logic beyond consuming structures as inputs or emitting evidence artifacts
- BioSymphony core policy

Those belong in BioSymphony Structure Factory or a private BioSymphony core workspace unless a cross-repo issue explicitly says otherwise.

## Dev Commands

```bash
git status --short --branch
find campaigns docs examples modules references scripts templates tests -maxdepth 4 -type f | sort
python3 scripts/cryocore/preflight.py --repo-root . --json
python3 scripts/cryocore/software_registry_check.py references/software-registry.yaml --json
make preflight
make registry-check
make module-check
make runpod-check
make runpod-scope-check
make provider-check
make issue-check
make launch-preflight
make toolcheck
make input-audit
make contract-self-check
make release-check
```

## Key Patterns And Conventions

- Experimental cryo-EM outputs are evidence; prediction/design outputs are hypotheses until validated against evidence.
- Keep cryo-EM C++/CUDA/system-tool stacks separate from ML design stacks to avoid dependency, image-size, and licensing collisions.
- Use manifests, checksums, artifact contracts, and claim ledgers to pass outputs between repos.
- A provider status such as `RUNNING` is intent only. Scientific success requires artifacts joined to declared inputs and validation outputs.
- Missing optional renderers such as ChimeraX should block only the renderer lane, not raw processing or model-build lanes.
- Public docs may mention gated tools, but install, image inclusion, execution, or redistribution requires current terms and user use-context review.

## Risks To Watch

- Public EMPIAR/EMDB/PDB identifiers are acceptable; raw downloads are too large for git.
- CryoSPARC, Phenix, ChimeraX, MotionCor2, and some visualization or refinement tools have license constraints.
- GPU toolchains are brittle across CUDA, driver, compiler, MPI, and Python versions.
- RunPod containers are ephemeral unless outputs land on persistent volumes and are fetched/hashed.
- Predicted models, ligand fits, density interpretation, state assignments, and biological mechanism claims must be caveated and validated.
