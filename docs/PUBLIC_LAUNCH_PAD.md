# Public Launch Pad

Use this document as the first map for the public CryoCore repo.

## Start Here

- `README.md`: product boundary and workflow.
- `AGENTS.md`: agent operating rules.
- `PUBLIC_RELEASE.md`: release gates and scrub rules.
- `docs/data-policy.md`: what may and may not live in git.
- `docs/no-false-success-hardening.md`: how CryoCore confirms artifacts, hashes, validation, and cleanup before treating a run as complete.
- `docs/tooling-and-licensing.md`: open, watch, and runtime-gated tool posture.

## First Workflows

1. Validate the public surface:

   ```bash
   make release-check
   ```

2. Inspect the no-download smoke contract:

   ```bash
   python3 scripts/cryocore/runpod_manifest_check.py runpod/launch-manifests/no-download-smoke.json --json
   python3 scripts/cryocore/runpod_launch_preflight.py --manifest runpod/launch-manifests/no-download-smoke.json --json
   ```

3. Review the map/model and figure contracts:

   ```bash
   python3 scripts/cryocore/module_manifest_check.py modules/campaigns/map-model-dossier-emdb-43816-pdb-9asj.v1.json --check-all --json
   python3 scripts/cryocore/figure_manifest_check.py --manifest tests/fixtures/figure-dossier/figure_manifest.json --artifact-root tests/fixtures/figure-dossier --json
   ```

## Public Boundary

The public repo contains contracts, validators, examples, and docs. Heavy data
and real outputs belong in external storage or ignored runtime directories. Paid
provider execution requires explicit operator authorization and fetched,
checked artifacts before any success claim.
