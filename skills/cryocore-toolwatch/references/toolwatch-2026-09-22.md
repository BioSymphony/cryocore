# CryoCore toolwatch: September 22, 2026

The next evaluation priorities are independent validation of AI outputs,
cryo-ET picking and segmentation, and recent runtime fixes. This review links
public sources to the evidence required before adopting each tool. Candidates
have not been benchmarked in CryoCore.

Dates refer to papers, releases, or commits, as labeled. The
[registry](../references/software-registry.yaml) records exact versions and
revisions. `watch` and `gated` records remain outside default execution.

## Selected AI methods

| Method and primary sources | Verified evidence | CryoCore decision |
| --- | --- | --- |
| [EM3DFold source](https://github.com/huang-laboratory/EM3DFold), [preprint](https://doi.org/10.64898/2026.09.16.752067) | Preprint posted September 18; source revision dated July 23. Protein, RNA, and DNA model building with language-model features. | **Watch.** Code and checkpoint terms remain unresolved. Compare against ModelAngelo/CryoAtom using original-map fit, geometry, and sequence-assignment errors. |
| [DAQplugin source](https://github.com/kiharalab/DAQplugin), [paper](https://doi.org/10.64898/2026.06.11.731735) | Source revision dated August 31; residue-level fit and register-error review in ChimeraX. GPL-3.0 code. | **Gated.** Review ChimeraX use context and downloaded weights. Preserve DAQ scores and alternative placements alongside independent local fit and geometry. |
| [LocScale releases](https://github.com/cryoTUD/locscale/releases/tag/v2.4.1), [paper](https://doi.org/10.1038/s41467-026-75327-8) | Paper July 17; v2.4.1 July 27. BSD-3-Clause code; [MC-EMmerNet v0.3 weights](https://zenodo.org/records/8211668) list CC BY 4.0. Feature-enhanced maps and predictive uncertainty. | **Watch.** Review checkpoint terms. Retain original, baseline, enhanced, and uncertainty maps; evaluate against untouched experimental inputs. |
| [CryoUNI/WAVE source and terms](https://github.com/Cellverse/cryouni), [preprint](https://doi.org/10.64898/2026.04.10.717737) | Verified code revision July 14. PolyForm Noncommercial code; CC BY-NC 4.0 weights and datasets. | **Gated.** Evaluate particle embeddings and state assignments. Occupancy and latent coordinates alone cannot establish free energies or transition mechanisms. |
| [Emap2lig source](https://github.com/kiharalab/Emap2lig), [weight terms](https://huggingface.co/KiharaLab/Emap2lig/blob/main/LICENSE.md) | Version 0.4.1 package dated June 19. GPL-3.0 code; separate academic/nonprofit research terms for trained weights. | **Gated.** Evaluate ligand candidates with chemistry, identity alternatives, local map fit, and explicit unsupported regions. |
| [ETSAM source](https://github.com/jianlin-cheng/ETSAM), [model record](https://zenodo.org/records/17571925) | v1.0.1 released August 17, targeting the June 23 code revision. MIT code; the separate model record lists CC BY 4.0. SAM2-based membrane segmentation. | **Watch.** Retain masks before postprocessing; measure thin-membrane loss against independent annotations. Keep the large checkpoints external. |
| [OPUS-ET revision](https://github.com/alncat/opusTomo/commit/0f84aeb606fc7d49783ef90292def9a920fef70b), [agent revision](https://github.com/alncat/opus-et-agent/commit/256b213b80c3243fb8e25d090d9a601be7ddb787) | September 17 revisions in the reconstruction and agent repositories. GPL-3.0 reconstruction code; MIT agent code with separately governed dependencies. | **Watch.** Review the WARP fork, processing tools, and renderer terms separately. Treat agent-reported results as reproduction targets. |

## Existing AI records

- [OCTOPI 1.7.0](https://pypi.org/project/octopi/1.7.0/) was released September 9.
  Its picking, segmentation, and copick integration make it a useful first
  evaluation target. The [selected model card](https://huggingface.co/Biohub/octopi/blob/db1e5c200ffbf954d019bd45949309666aaacfb4/README.md)
  declares MIT separately from the source. Record checkpoint hashes and training
  provenance; review MCP tools and storage writes before exposing a project.
- [Easymode v1.2.5](https://github.com/mgflast/easymode/releases/tag/v1.2.5)
  and its PyPI package were released September 17. The same-day
  [main revision](https://github.com/mgflast/easymode/commit/544572cfc071869113eb0567ef607791946a81c1)
  differs from the release target; record the selected source explicitly.
  The [model card](https://huggingface.co/mgflast/easymode/blob/c3d5ac705405b8b25dfdbca40fc6a54a725f1eb0/README.md)
  declares GPL-3.0. Check checkpoint hashes, training provenance, and the
  TensorFlow/CUDA environment before testing.
- [CryoDECO's September 2 revision](https://github.com/yanyang1998/CryoDECO/commit/f44bcf69d3aa26ccb4b739e050c3bf4bb8417900)
  adds `k_est`, but the README still describes incomplete release support.
  Keep automatic cluster-count estimation unverified until tested.
- [cryoDRGN 4.3.1](https://github.com/ml-struct-bio/cryodrgn/releases/tag/4.3.1)
  and [ModelAngelo v1.0.18](https://github.com/3dem/model-angelo/releases/tag/v1.0.18)
  remain the latest tagged releases checked in this review. Preserve their
  existing source, checkpoint, and independent-validation requirements.

## Runtime updates and corrections

| Record | Source-backed change | Consequence |
| --- | --- | --- |
| [Apptainer 1.5.4](https://github.com/apptainer/apptainer/releases/tag/v1.5.4) | Released September 22. [Upstream advisory](https://github.com/apptainer/apptainer/security/advisories/GHSA-4wg8-vhjg-jq8p) identifies local privilege escalation in `apptainer-suid` 1.5.0 through 1.5.3. | Require a patched runtime for the affected mode before HPC execution. |
| [Warp dev41](https://github.com/warpem/warp/releases/tag/v2.0.0dev41) | Released September 17 with Linux ARM64 support. | Review architecture and CUDA/.NET compatibility before changing an image. |
| [Syft 1.52.0](https://github.com/anchore/syft/releases/tag/v1.52.0) | Released September 17; bounds several archive and binary-parser allocations. | Refresh the SBOM-tool record; retain immutable scan targets and output hashes. |
| [rocrate-validator 0.11.4](https://github.com/crs4/rocrate-validator/releases/tag/0.11.4) | Released September 16; fixes JSON-LD singleton-array handling and misleading metadata/version errors. | Recheck generated crates with their declared profile. |
| [AreTomo3 v2.2.2](https://github.com/czimaginginstitute/AreTomo3/releases/tag/v2.2.2) | The release date is July 16, **2025**. | Correct the 2026 date recorded in the August review; the version is unchanged. |
| [copick 1.27.0](https://pypi.org/project/copick/1.27.0/) | GitHub and PyPI both published 1.27.0 on August 18. | Correct the earlier package-lag note and record the exact `copick-v1.27.0` tag. |
| [copick-mcp releases](https://github.com/copick/copick-mcp/releases) | `copick-mcp-v0.6.1` remains the non-prerelease record; 2.0.0-alpha.3 is a separate prerelease. | Keep alpha compatibility changes outside the selected 0.6.1 record. |

## Research to revisit

| Source | Reason to retain as a reference |
| --- | --- |
| [CryoFlex v1](https://www.biorxiv.org/content/10.64898/2026.09.01.748519v1), posted September 4 | Motion estimation between state maps; public code and weights were not verified. |
| [Map postprocessing benchmark](https://doi.org/10.1038/s41597-026-07949-y), July 23 | Candidate evaluation splits, half-maps, fitted models, and metrics. Track accession and split metadata; review data terms before fetching. |
| [TomoSwin3D](https://github.com/jianlin-cheng/TomoSwin3D) | Alternative 3D picker with MIT code and a separate model record. Compare after establishing the OCTOPI baseline. |
| [CryoSplat](https://github.com/Chen-Suyi/cryosplat) | Gaussian-splatting reconstruction under research/noncommercial terms; requires a distinct benchmark and license review. |
| [CryoLVM](https://arxiv.org/abs/2602.02620), [CryoSampler](https://jayshenoy.com/cryosampler) | Relevant model-based methods; usable public implementations were not verified. |
| [QuantEM](https://doi.org/10.64898/2026.08.06.743293), August 7 | General EM/organelle segmentation; a cryo-ET-specific evaluation remains to be established. |

## Evaluation order

1. Resolve source and checkpoint terms, pin revisions, and define small public
   evaluation inputs. Keep source access, software readiness, and scientific
   performance as separate records.
2. Compare OCTOPI with a conventional picker and ETSAM with independent membrane
   annotations. Record precision/recall, failure classes, runtime, and memory.
3. Compare DAQ/LocScale outputs with existing fit metrics and unmodified maps.
   Use EM3DFold only after its terms are resolved; preserve incorrect or
   ambiguous chain and sequence assignments in the report.
4. Evaluate heterogeneity methods against a shared particle split and known
   baseline. Test stability across seeds and resampling before interpreting
   states or populations.

Each evaluation must satisfy the [AI evidence requirements](../references/validation-gates.md)
and [tool promotion policy](toolwatch-to-lane-policy.md). No candidate advances
on the strength of a paper score or repository demo alone.
