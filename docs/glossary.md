# Glossary

A bridge between cryo-EM domain vocabulary, the tools the field uses, and the
orchestration terms CryoCore adds on top.

## CryoCore Orchestration Terms

`control plane`: Manifests, schemas, scripts, docs, and checks that define how
work should run. Heavy data lives elsewhere.

`artifact root`: A local or provider-side directory containing outputs from one
run. Heavy artifact roots stay ignored or external.

`claim ledger`: A structured record of claims, evidence, and caveats. It
downgrades unsupported claims so an agent cannot turn a summary into a
biological conclusion by default.

`stage contract`: The list of required workflow stages and acceptable terminal
states.

`closeout`: The final evidence bundle proving what ran, which inputs were used,
which artifacts were fetched, which hashes matched, and whether cleanup was
verified.

`operator gate`: A human or organization-specific approval step for cost,
licenses, credentials, private data, or wet-lab implications.

`reference provider`: A provider path with the most complete contract coverage.
Launch still requires explicit operator authorization.

`prep mode`: A dry or local validation mode that proves contracts. Paid
execution and scientific success live elsewhere.

`real mode`: A mode that requires actual runtime evidence, artifact hashes,
stage terminal evidence, and closeout checks.

## Cryo-EM Vocabulary

`EMDB`: Electron Microscopy Data Bank. Public repository for cryo-EM density
maps and associated metadata. Entries use IDs like `EMD-43816`.

`EMPIAR`: Electron Microscopy Public Image Archive. Public repository for raw
cryo-EM movies, particle stacks, and image-tier data. Entries use IDs like
`EMPIAR-10204`.

`PDB`: Protein Data Bank. Public repository for atomic-coordinate models.
Entries use four-character IDs like `9ASJ` or `9W0Q`.

`wwPDB`: Worldwide Protein Data Bank. The international consortium that runs
deposition, annotation, and validation for the PDB.

`mmCIF`: Macromolecular Crystallographic Information File. The modern atomic
coordinate format, replacing legacy PDB text format for large or complex
structures.

`MRC` / `MAP`: Density map file formats used for 3D cryo-EM reconstructions.

`movie`: A stack of frames captured per electron-microscope exposure. Frame
alignment uses these stacks to correct beam-induced motion.

`micrograph`: A single integrated image produced from a movie after motion
correction.

`CTF`: Contrast Transfer Function. The microscope-induced phase distortion
that affects every micrograph. Estimating and correcting the CTF is a standard
preprocessing step.

`particle` / `particle stack`: Single-particle images cropped out of
micrographs. A stack is the dataset used for 2D and 3D classification and
reconstruction.

`half-maps`: Two independently reconstructed maps from random halves of the
particle stack. They drive the resolution estimate, local resolution maps,
and sharpening or post-processing parameters.

`FSC`: Fourier Shell Correlation. The resolution metric derived from
half-maps. The 0.143 threshold is standard for reporting "gold-standard"
resolution.

`resolution`: The smallest spatial feature resolved in a map, reported in
ångströms. Lower numbers are better.

`B-factor`: In atomic models, the atomic displacement parameter (also called
the temperature factor) that reflects local flexibility or local map noise
around each atom. At the map level, a Guinier-derived "map B" is used for
sharpening the reconstruction. They are different quantities used in
different contexts and reported separately.

`heterogeneity`: The structural variability inside a particle stack. Multiple
conformational or compositional states can coexist and are separated by 3D
classification.

`map / model fit`: The agreement between an atomic model and the underlying
density map. Metrics include cross-correlation, Q-score, and per-residue
density support.

`ligand`: A small molecule, ion, or cofactor bound to the protein or RNA in
the structure.

`deposition`: The public release of a map (to EMDB) and an atomic model (to
PDB), with metadata and validation reports.

## Cryo-EM Tools At A Glance

One-liners for tools referenced in this repo. Full posture lives in
[references/software-registry.yaml](../references/software-registry.yaml) and
[docs/tooling-and-licensing.md](tooling-and-licensing.md).

### Reconstruction and processing

`RELION`: Single-particle reconstruction pipeline covering particle picking,
2D and 3D classification, and refinement. Widely used; open source.

`CryoSPARC`: Reconstruction pipeline with strong heterogeneity handling
(3D variability, 3D flex). Commercial license with an academic free tier.

`MotionCor3`: GPU-accelerated frame alignment for cryo-EM movies.

`CTFFind`: CTF estimation from micrographs.

`Topaz`: Neural-network particle picker for sparse or low-contrast datasets.

`Warp` / `Warp-M`: Preprocessing, particle picking, and multi-particle
refinement. Used broadly for single-particle analysis, time-resolved data,
and tomography.

### Model building and refinement

`ModelAngelo`: Neural-network atomic-model builder that grows a backbone trace
and sequence into a cryo-EM map.

`Coot`: Interactive model building and inspection. Originally developed for
X-ray crystallography, now standard in cryo-EM workflows too.

`Phenix`: Refinement and validation suite. Includes `phenix.real_space_refine`
for cryo-EM model refinement and validation utilities used during deposition.

`ChimeraX`: Molecular visualization for maps and models, figure rendering,
density inspection, and publication-quality images.

Several adjacent tools are common in modern cryo-EM model work but outside the
current CryoCore lane coverage: `ISOLDE` (interactive model building inside
ChimeraX), `Servalcat` (refinement and map calculation for cryo-EM in CCP-EM
and Phenix workflows), and CCP-EM components such as `Buccaneer`. Add a
posture entry for any of these when a campaign needs them.

### Validation and deposition

`wwPDB validation`: The deposition-time validation pipeline that produces
PDF and XML reports covering geometry, density fit, clashes, and outliers.

### Design and prediction (consumed by CryoCore outputs)

`AlphaFold`, `RFdiffusion`, `Boltz`, `Chai`, `ProteinMPNN`: AI-driven
prediction and design tools. CryoCore tracks them as downstream consumers of
deposited maps and models, with separate runtimes and license postures from
the cryo-EM processing stack.

## Related

- [Claim Levels](claim-levels.md): the ladder that uses several terms defined here.
- [Tooling and Licensing](tooling-and-licensing.md): authoritative license, version, and posture detail for the tools listed here.
- [Software Registry](../references/software-registry.yaml): machine-readable posture records per tool.
- [Public Accession APIs](public-accession-apis.md): the EMDB, EMPIAR, RCSB PDB, and wwPDB endpoints behind these accession types.
