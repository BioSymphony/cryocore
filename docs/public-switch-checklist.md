# Public Switch Checklist

Use this checklist before changing the local public staging repo into a public GitHub repository.

## Local Readiness

- Run `make release-check`.
- Run `python3 scripts/cryocore/public_release_report.py --repo-root . --json`.
- After the initial public commit, remote, and tag exist, run
  `python3 scripts/cryocore/public_release_report.py --repo-root . --publish-ready --expected-remote https://github.com/BioSymphony/biosymphony-cryocore-public.git --json`.
- Confirm `git remote -v` is empty or points only to the intended public repository.
- Confirm the first commit is created from the scrubbed public tree, not from private history.
- Confirm `.runtime/`, `artifacts/`, `outputs/`, raw-data caches, provider logs, and model weights are absent or ignored.

## Privacy And Security

- No local workstation paths.
- No private image namespaces.
- No private clone markers.
- No provider IDs, volume IDs, account IDs, billing ledgers, or raw provider logs.
- No API keys, tokens, signed URLs, registry auth, SSH keys, or license files.
- No private structures, unpublished sequences, raw movies, maps, half-maps, masks, particle stacks, or model weights.

## Scientific Claim Boundary

- Public demos are accession-based or synthetic.
- Claim ledgers use explicit claim levels.
- Provider `RUNNING` or command exit is never described as scientific success.
- Real closeout requires fetched artifacts, hashes, input audit, contract self-check, cost report, cleanup proof, and claim ledger.
- Tool and license posture is documented as engineering policy, not legal advice.

## Provider Readiness

The public repo can publish prep manifests with placeholder images. A real paid provider run needs a separate operator gate and:

- digest-pinned image or audited bootstrap route
- pinned fetchable public commit
- current provider credentials outside git
- current tool/license use-context review
- declared max spend and cleanup action
- persistent external artifact storage or fetched local artifacts with hashes

## After The Switch

- Add the public remote explicitly.
- Run CI on the public remote before announcing readiness.
- Keep private run notes and private learnings outside this repository.
- Convert reusable private lessons into generic docs, tests, or fixtures only after scrub review.
