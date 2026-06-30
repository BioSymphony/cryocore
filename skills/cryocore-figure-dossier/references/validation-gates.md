# CryoCore Validation Gates

CryoCore campaigns move through explicit evidence gates. Runner flags are intent; success requires artifacts joined to declared inputs and validation outputs.

## No-False-Success Rule

Every provider-backed or long-running CryoCore run emits:

- `validation/input-audit.json` before execution
- `validation/fanout-estimate.json` before raw-subset or multiplicative lanes
- `stage-progress.jsonl` while work is running
- `validation/stage-contract-check.json` before closeout
- `validation/contract-self-check.json` before an external-agent issue closes as successful

Mock and dry-run artifacts must carry `mock_tools`, `mock_gpu`, or `dry_run` markers. Real execution fails if those markers appear in required evidence.

## Maturity Ladder

- L0 `plan_exists` - issue, manifest, and artifact contract exist.
- L1 `tools_ready` - environment, tool, GPU, and license checks pass.
- L2 `inputs_materialized` - data ledgers join accessions to concrete files or accepted no-download posture.
- L3 `execution_performed` - commands ran and emitted expected result artifacts.
- L4 `evidence_joined` - results join back to inputs, tool versions, and processing ledgers.
- L5 `claim_audited_dossier` - claims have evidence, confidence, caveats, and review status.

## Gate 0: Contract

- Issue body conforms to `templates/linear-issue.md`.
- Inputs are public accessions or secure external references.
- Raw movies, maps, private structures, secrets, and model weights are not committed.
- Expected artifacts and validation commands are exact.

## Gate 1: Environment

- Tool versions are recorded.
- GPU and driver compatibility are recorded.
- License constraints are recorded.
- Smoke commands pass or the lane is explicitly blocked.
- Private registry auth and gated tool access are runtime references only.
- Digest-pinned images are required before real remote launch.

## Gate 2: Data Intake

- Dataset accession, source, expected size, and download method are recorded.
- Checksums or file counts are recorded where practical.
- Storage path is outside git.
- Raw-subset lanes include a bounded fanout estimate before transfer.

## Gate 3: Processing

- Motion correction, CTF, picking, classification, reconstruction, refinement, model-build, or render outputs are recorded according to the lane.
- Failed branches are recorded, not hidden.
- Executed-command ledgers join stage IDs to command strings, exit codes, timestamps, and result paths.

## Gate 4: Model And Map

- Model, map, half-map, mask, and validation artifacts are recorded when applicable.
- Chain assignment and biological assembly assumptions are recorded.
- Map/model agreement metrics are emitted for map/model dossiers.
- `validation/map_model_fit.json` should join geometry validation, global FSC, model-map FSC, local correlation or SMOC-like scores, Q-score or Strudel-style local scores when available, deposition report identifiers, source hashes, caveats, and claim level.
- Foundation-model map enhancement, inpainting, denoising, or style transfer is derived evidence only. It must record original maps, weights, parameters, hashes, and independent validation before it can support a stronger claim.

## Gate 5: Figure Dossier

- Figures are nonblank, labeled, reproducible, and backed by scripts or sessions.
- Captions include contour levels, accessions, software, and caveats.
- Web viewer states, MolViewSpec scenes, ChimeraX sessions, PyMOL scripts, Blender scenes, notebooks, and static renders should all join back to the same source accessions and artifact hashes.

## Gate 6: Claim Audit

- Every claim maps to evidence.
- Unresolved weaknesses are listed.
- Next experiments are proposed when evidence is insufficient.
- Claim level is explicit: `candidate`, `processed`, `validated`, `publishable`, `insufficient_evidence`, or `blocked`.
