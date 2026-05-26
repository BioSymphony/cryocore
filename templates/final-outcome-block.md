# Final Outcome Block

Use this shape for closeout messages or issue comments.

Every final comment should include the machine-readable block first:

```yaml
<!-- symphony-outcome -->
outcome_version: 1
status: blocked | partial | degraded | completed
claim_level: candidate | processed | validated | publishable | insufficient_evidence | blocked
evidence_root: <path-or-artifact-root>
validation:
  - <command and result>
artifacts:
  reports: []
  ledgers: []
  figures: []
  hashes: []
boundaries:
  no_raw_private_data_in_git: true
  no_secrets_or_license_files_in_git: true
  provider_cleanup_proof: present | not_applicable | missing
residual_risk:
  - <risk or caveat>
```

## Outcome

- Status:
- Claim level:
- Evidence root:

## Validation

```bash
# commands run
```

## Artifacts

- Reports:
- Ledgers:
- Figures:
- Hashes:

## Boundaries

- No raw/private data in git:
- No secrets or license files in git:
- Gated tools used:
- Provider cleanup proof:

## Residual Risk

- Scientific caveats:
- Missing optional evidence:
- Follow-up validation:
