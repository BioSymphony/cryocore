# Recipe: Figure Rendering

CryoCore keeps renderer orchestration public while source maps, models, frames,
movies, and license-controlled software installations stay outside git. Use this recipe when
you need a reproducible map/model snapshot, turntable, FSC panel, or a renderer
script that can be run in a local or license-compliant environment.

## Renderer Choices

| Need | Default | Notes |
| --- | --- | --- |
| Local model or carved map/model still | PyMOL | Run with `pymol -cqr`; works without a window on macOS and Linux. |
| Map surface | ChimeraX | License-controlled. Use Linux offscreen or macOS GUI REST mode. |
| FSC / validation curve | matplotlib | Headless and local; demo mode creates an illustrative curve only. |
| Self-contained HTML report | inline helper | Inlines local `src` and `poster` assets into data URIs. |

## Commands

Generate a local PyMOL map/model overlay:

```bash
pymol -cqr scripts/cryocore/render/pymol_render.py -- map-model \
  --map .runtime/input/map.mrc \
  --model .runtime/input/model.cif \
  --out .runtime/figures/map_model.png
```

Prepare a ChimeraX map/model scene without executing ChimeraX:

```bash
python3 scripts/cryocore/render/chimerax_render.py map-model \
  --map .runtime/input/map.mrc \
  --model .runtime/input/model.cif \
  --level 0.03 \
  --out .runtime/figures/map_model.png
```

Render an illustrative FSC panel:

```bash
python3 scripts/cryocore/render/fsc_plot.py \
  --demo \
  --out .runtime/figures/fsc_demo.png \
  --title "FSC (illustrative)"
```

## Templates

- `templates/render/pymol/map_model_hero.pml`
- `templates/render/chimerax/map_model_hero.cxc`
- `templates/render/chimerax/turntable.cxc`

These are starting points. Replace placeholders with paths in ignored runtime
storage, not files committed to the repo.

## Data Boundary

- Do not commit rendered PNG/MP4/GIF outputs, raw maps, half-maps, fitted
  structures, session files, license files, or nonpublic run metadata.
- ChimeraX and commercial PyMOL remain license-controlled; this repo only
  stores orchestration scripts and templates.
- Captions and figure manifests must carry accessions, contour levels, software
  versions, renderer posture, and limitations.

## Related

- [ChimeraX Shared Posture](../chimerax-shared-posture.md)
- [Figure Manifest schema](../../modules/schemas/figure-manifest.v1.schema.json)
