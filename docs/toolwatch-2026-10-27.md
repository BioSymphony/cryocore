# Toolwatch: October 27, 2026

This review adds template-bias measurement, map-guided model building, and
workflow orchestration to the [tool registry](../references/software-registry.yaml).
The [micrograph QC guide](micrograph-qc-and-output-checks.md) covers the
Miffi, MotionCor3, and GCtfFind adapters.

## Tools And Research

| Resource | Useful For | Next Step |
| --- | --- | --- |
| [2DTM postprocessing](https://github.com/kekexinz/2DTM_postprocess_tool/tree/87eea5503a7b3fc74e8b13d864563cb1baacb28c), [paper](https://elifesciences.org/articles/109790) | Measuring template bias with full-template and omit-template reconstructions | Planned: compare matched experimental reconstructions |
| [Scipion facility workflow paper](https://journals.iucr.org/d/issues/2026/08/00/bar5004/index.html) | Comparing individual QC filters with sequential rejection | Inspect the exact workflow and retain rejected-image counts |
| [CryoACE](https://github.com/Cellverse/CryoACE/tree/689f6b377e33680eb1a6f070bb40fe02a9ae3c2d), [ICML paper](https://proceedings.mlr.press/v306/li26eh.html) | Building candidate models with density and local-resolution guidance | Gated: review checkpoints and compare original-map fit and geometry |
| [Relay](https://github.com/warpem/relay/tree/8bb040a0d4b956cdd0905ea9de5642f2b540e9f0) | Defining cryo-EM jobs and connecting workers to schedulers | Watch: test execution records, cancellation, and restart |
| [Fold'EM v2](https://arxiv.org/abs/2610.01358v2) | Studying structure inference guided by particle images | Paper watch: inspect the runnable release when available |

## Details That Change The Call

The 2DTM measurement CLI defaults to a mask threshold divisor of 10. To match
the paper's mask, set `--top_n 100 --threshold_divisor 5`. Match grid, origin,
axis order, voxel size, and normalization before comparing reconstructions.
The `--templates` route writes a difference map beside its input; use working
copies. The helper source is BSD-3-Clause.

CryoACE's pinned source uses PolyForm Noncommercial terms; weights and datasets
use CC BY-NC 4.0. Its example accepts a sequence, map, and aligned starting model.
An external MSA server is optional input preparation that needs its own data
handling decision.

Relay's MIT-licensed orchestrator requires .NET 10 and Python 3.10+ for Bakery.
Processing tools and submodules retain their own terms. CPU and memory
reservations provide accounting rather than enforced resource limits.

## Runtime Records

RECOVAR's [pinned source license](https://github.com/ma-gilles/recovar/blob/b1ceda7c5e5d77eadbb229908d5e61139ee2fe34/LICENSE)
is MIT. Older packages retain their original licenses.

The Miffi adapter records the source and checkpoint separately. Its two model
variants have different trained weights. The CZI adapter checks executable
hashes and native version strings: MotionCor3 1.2.4 and GCtfFind 1.2.5.
See [tool terms](tooling-and-licensing.md) and the
[adoption policy](toolwatch-to-lane-policy.md) for runtime selection.
