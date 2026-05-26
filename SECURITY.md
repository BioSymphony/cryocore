# Security And Data Policy

Do not open issues or pull requests containing private biological, operational, provider, or customer data.

## Supported Versions

| Version | Support |
| --- | --- |
| `0.1.x-prealpha` | Security and public-release hygiene fixes only. |

This pre-alpha repo is not a clinical, therapeutic, regulatory, or production
provider-execution system.

Never include:

- API keys, cloud credentials, SSH keys, tokens, signed URLs, registry auth, or license files
- private structures, unpublished sequences, private maps, raw reads, raw cryo-EM movies, or patient data
- provider pod IDs, network volume IDs, account IDs, billing records, or raw provider logs
- private workstation paths, private issue-tracker content, or internal run notes
- model weights, large public databases, checkpoints, or generated structure archives

Use synthetic examples or public accessions with source and transformation notes.

If you discover a security issue in the code or release process, report it
privately to the repository owner through GitHub's private vulnerability
reporting flow rather than posting sensitive details publicly.

Expected triage: best-effort initial maintainer acknowledgement within 7 days
after the public repository is live. If private vulnerability reporting is not
available, do not post sensitive details in a public issue; use the repository
owner contact path configured by the public GitHub organization.

Run before publication:

```bash
make release-check
make secret-scan
```
