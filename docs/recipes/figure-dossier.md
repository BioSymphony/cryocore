# Recipe: Figure Workflow

Mode: planning and validation scaffold. Actual figure rendering happens
through a renderer lane and source artifacts that live outside git, with this
recipe staging the manifest, captions, and validators around them.

## Inputs

- Public accessions or artifact references.
- Renderer posture and version records.
- Figure manifest.

## Commands

```bash
make figure-manifest-check
make public-release-report
```

## Files Produced

- `figure_manifest.json`
- renderer commands or scene/session references
- captions with accessions, contour levels, software versions, and caveats

## Claim Ceiling

Figures are explanatory evidence. Density interpretation and mechanism rest
on validation artifacts and expert review.

## Failure Handling

A missing optional renderer blocks only the renderer lane. Do not downgrade raw
processing or model validation just because a figure exporter is unavailable.

## Related

- [Figure Rendering](rendering.md): concrete PyMOL, ChimeraX, FSC, and HTML helper commands.
- [Linear template: Figure Workflow](../../templates/linear-figure-dossier.md): tracker-ready issue shape for this recipe.
- [Figure Workflow skill](../../skills/cryocore-figure-dossier/SKILL.md): the skill an agent loads to run this recipe.
- [ChimeraX Shared Posture](../chimerax-shared-posture.md): renderer license posture and license-gate conventions.
- [Figure Manifest schema](../../modules/schemas/figure-manifest.v1.schema.json): contract for the figure manifest.
