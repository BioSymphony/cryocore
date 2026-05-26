# Privacy Threat Model

CryoCore is designed to be public, but it sits near sensitive scientific and
provider workflows. The main threats are accidental disclosure and false success.

## Assets To Protect

- credentials, tokens, SSH keys, signed URLs, registry auth, provider secrets
- provider IDs, account IDs, billing records, pod logs, volume IDs
- private or unpublished structures, sequences, maps, masks, particle stacks,
  raw cryo-EM movies, model weights, and license files
- internal tracker content, local workstation paths, private image namespaces

## Controls

- `.gitignore` blocks common scientific, credential, cache, and runtime outputs.
- `public_snapshot_check.py` scans candidate files for heavy suffixes, private
  markers, and secret-like content.
- `public_release_report.py` requires public release files and blocks known
  public-switch markers.
- `provider_closeout_check.py` rejects intent-only provider state.
- GitHub issue and PR templates instruct contributors not to post sensitive
  material.

## Residual Risk

No scanner is complete. Before public switch, run `make release-check`, inspect
`git status --short`, and review any new files that touch providers, raw data,
license gates, or claim ledgers.

## Related

- [Data Policy](data-policy.md): the data tiers and git boundaries these controls enforce.
- [Public Repo and Private Image Policy](public-repo-and-private-image-policy.md): the public source vs private runtime split.
- [Public Switch Checklist](public-switch-checklist.md): the readiness list before a public switch.
- [No-False-Success Hardening](no-false-success-hardening.md): the closeout discipline that catches false-success exposure.

