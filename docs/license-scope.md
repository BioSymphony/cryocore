# License Scope

This repository is MIT-licensed code and documentation unless a file says
otherwise. That license does not grant rights to third-party cryo-EM tools,
scientific databases, provider images, license files, installers, model
weights, or datasets referenced by the manifests.

## Public-Safe Defaults

- Use open metadata and tiny fixtures for local checks.
- Keep proprietary installers, license files, and access URLs out of git.
- Treat ChimeraX, CryoSPARC, Phenix, MotionCor2, and similar tools as
  runtime-gated until the operator confirms current terms and permitted use.
- Record tool posture in `references/software-registry.yaml` and
  `docs/tooling-and-licensing.md`.

## Provider Images

Public manifests may name an image pattern, but release-quality execution should
use digest-pinned images and operator-controlled registries. The public repo
does not redistribute licensed software or private container layers.

## Related

- [Tooling and Licensing](tooling-and-licensing.md): per-tool posture, open/watch/gated classification, and policy snippets.
- [Public Repo and Private Image Policy](public-repo-and-private-image-policy.md): the public source vs private runtime split.
- [ChimeraX Shared Posture](chimerax-shared-posture.md): a worked posture record for a shared license-gated tool.

