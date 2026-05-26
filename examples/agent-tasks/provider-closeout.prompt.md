# Prompt: Provider Closeout Review

Review a provider run for closeout completeness. Confirm that fetched
artifacts, hashes, validation outputs, cost records, and cleanup proof are
actually present before declaring the stage complete. Do not treat provider
state, pod ID, or `RUNNING` status as scientific success.

Return:

- the closeout status: `processed`, `validated`, `partial`, `degraded`, `blocked`, or `failed`
- a per-required-artifact present/missing table joined to declared expected artifacts
- cost and cleanup evidence summary
- claim ledger entries with claim levels, downgrades, and reasons
- next-step suggestions for any missing evidence
