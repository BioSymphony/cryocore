# CryoCore Goal Brief

A worked example brief for the Pol Theta map and model dossier mission. Public
accessions only.

## Goal

- User goal: Produce a claim-bounded dossier for the human Pol Theta helicase domain in complex with AMP-PNP using public EMDB and PDB deposits.
- Success signal: A reviewable HTML dossier, a claim ledger, a machine-readable manifest, and a wwPDB validation summary live under `.runtime/poltheta-map-model-remote/` with all artifacts hashed and joined to declared inputs.
- Claim ceiling: `processed`. Mechanism, ligand-action, and therapeutic claims stay out.

## Starting Inputs

- Public accessions: EMDB `EMD-43816`, PDB `9ASJ`.
- Operator-provided local paths: none.
- Existing artifacts or issue links: [demos/poltheta-map-model-dossier/](../../demos/poltheta-map-model-dossier/), [modules/data-modules/emdb-43816-pdb-9asj.map-model.v1.json](../../modules/data-modules/emdb-43816-pdb-9asj.map-model.v1.json).
- Unknowns the agent should resolve first: wwPDB validation report URL freshness, current EMDB header version, whether AMP-PNP ligand neighborhood is fully modeled in `9ASJ`.

## Resource Mode

- [ ] `local_only`
- [x] `public_metadata_network` (EMDB and wwPDB metadata fetches are allowed)
- [ ] `operator_gated_provider`
- [ ] `tracker_wave` (consider splitting once the prep check passes)
- [ ] `provider_closeout`

## Desired Outputs

- Dossier/report: `report.html` with input audit, map header summary, model inventory, AMP-PNP neighborhood, density-support checks, SVG figures.
- Issue wave or handoff: optional Linear wave after the local prep check passes. See [sample-linear-wave](../sample-linear-wave/).
- Provider launch request: prep mode only on this brief. A real RunPod launch is operator-owned.
- Validation/closeout evidence: `validation-summary.json`, `dossier_manifest.json`, `claim_ledger.md`, all hashed.
- Downstream Structure Factory handoff: none on this brief.

## Boundaries

- Data allowed in git: manifests, schemas, brief, claim ledger, SVG figures, validation summary.
- Data that must stay outside git: the EMDB map (`emd_43816.map.gz`), the wwPDB validation PDF, any raw movies or particle stacks.
- Secrets/license files: none required.
- Provider or budget limits: prep mode only. No paid execution on this brief.
- Gated tools requiring approval: none for prep. A real run would require operator authorization for paid GPU time.

## Agent Orchestration

- Single-agent task or multi-agent wave: single-agent for prep. Multi-agent wave is appropriate when scaling to a real RunPod launch.
- First wave only: yes. Stop after the prep check passes and the dossier shape is verified locally.
- Blocked/future work: real RunPod launch, paid closeout review, deposition-mirroring of validation reports.
- Human/operator gates: paid execution, raw-data downloads, license-gated tooling beyond the public deposit.
- Files or directories likely to change: `demos/poltheta-map-model-dossier/`, `.runtime/poltheta-map-model-remote/`, `runpod/bridge-manifests/poltheta-map-model-dossier.json` if the manifest needs an update.

## Validation And Closeout

- Minimum local commands:
  - `python3 scripts/cryocore/preflight.py --repo-root . --json`
  - `make demo-poltheta-prep-check`
  - `make contract-self-check`
- Public/network commands allowed: `python3 scripts/cryocore/fetch_public_accession_metadata.py --emdb EMD-43816 --pdb 9ASJ --out .runtime/public-accession-metadata.json`
- Provider closeout commands: `make provider-closeout-check` once an operator-owned run has produced fetched artifacts.
- Required artifacts: `report.html`, `dossier_manifest.json`, `claim_ledger.md`, `validation-summary.json`, SVG figures.
- Final outcome block or comment target: append `templates/final-outcome-block.md` to the calling issue or thread when the prep check passes.

## Open Questions

- Should the dossier include the AMP-PNP analog comparison against ADP-bound homologs, or is that downstream Structure Factory work?
- Does the current wwPDB validation report URL still resolve, or has the entry been re-validated since first deposit?
