# CryoCore Split Evaluation

Last reviewed: 2026-05-15

![CryoCore and Structure Factory boundary](assets/cryocore-sf-boundary.svg)

## Decision

Create `biosymphony-cryocore-public` as a sidecar repo for cryo-EM evidence production and structural review. Start by duplicating the contracts that need to exist in both repos, then promote concrete campaigns or scripts only after each lane has a clear owner.

## Why This Split Is Useful

The cryo-EM and AI design stacks are complementary, but operationally different.

CryoCore needs heavy system tools:

- RELION, Warp/M/WarpTools, MotionCor3, Topaz, CTFFIND
- ModelAngelo, Coot, Phenix, gemmi, validation utilities
- cryoDRGN/RECOVAR-style heterogeneity tooling
- ChimeraX and other render/review tools

Structure Factory design lanes need ML/prediction tools:

- Boltz, Chai, RFdiffusion
- ProteinMPNN and LigandMPNN
- Genie-style generation stacks and downstream jury scoring

Trying to put both classes into one image makes the system brittle. The dependency surface becomes a collision between C++/MPI/CUDA cryo tools and Python/PyTorch/JAX design tools. The licensing posture also gets harder because GPL cryo tools, no-cost noncommercial GUI tools, public model weights, and restricted design tools all end up in one packaging decision.

## Complementarity

The handoff should be artifact-based:

```text
CryoCore
  maps, models, state assignments, validation metrics, figure packs
    -> Structure Factory
       prediction/design candidates, Boltz/Chai re-predictions, RFdiffusion designs
    -> CryoCore or Structure Factory review
       structural plausibility, figure dossier, claim ledger
```

Experimental evidence outranks predicted structure output. Design lanes can propose hypotheses or candidates, but CryoCore artifacts define the evidence boundary.

## Initial Repo Shape

The first version should contain:

- a smaller software registry focused on cryo and model-build tools
- explicit duplicate-tool policy for ChimeraX and visualization tools
- provider-neutral lane modules
- no-download smoke examples
- local validators
- templates for tracker-neutral issue contracts

It should not contain raw movies, maps, heavy public datasets, model weights, installers, or license records.

## Migration Strategy

1. Keep Structure Factory intact until CryoCore validators pass.
2. Duplicate shared posture docs for tools that really span both repos.
3. Move cryo-only campaign scaffolds after the new validators pass.
4. Keep cross-repo handoffs through artifact contracts, not Python imports.
5. Leave RFdiffusion/Boltz/Chai in Structure Factory unless a CryoCore campaign only consumes their finished outputs as comparison evidence.

## Success Bar

CryoCore is useful when a worker can answer these questions from this repo alone:

- What tools are allowed, gated, or blocked for cryo-EM processing?
- What artifacts prove a cryo-EM lane succeeded?
- What can be run locally without paid compute or raw-data download?
- How does a map/model evidence pack hand off to Structure Factory?
- Which tools are duplicated intentionally, and how are their license gates kept synchronized?

## Related

- [Move/Duplicate Map](move-duplicate-map.md): which posture records are intentionally duplicated across CryoCore and Structure Factory.
- [ChimeraX Shared Posture](chimerax-shared-posture.md): the worked posture record for the most-shared license-gated tool.
- [Tooling and Licensing](tooling-and-licensing.md): per-tool license posture that informs cross-repo placement.
