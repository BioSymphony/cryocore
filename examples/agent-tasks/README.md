# Agent Task Prompts

These prompts are fixtures for testing an agent against the skill pack. They
produce practical outputs: dossier plans, provider prep, issue waves, and
release-readiness reviews.

- [Public Release Review](public-safety-review.prompt.md): review the public checkout before a public switch.
- [Map/Model Dossier](map-model-dossier.prompt.md): produce a claim-bounded public accession dossier plan.
- [Cloud Provider Prep](cloud-provider-prep.prompt.md): prepare a cloud/HPC contract without launching paid compute.
- [Provider Closeout Review](provider-closeout.prompt.md): confirm a provider run's artifacts, hashes, cost, and cleanup before declaring the stage complete.
- [Linear Wave Planning](linear-wave-planning.prompt.md): split a campaign into bounded tracker issues.
- [Goal To Campaign](goal-to-campaign.prompt.md): turn a broad goal into a goal brief, issue wave, or local execution plan.

Expected first response from an agent:

1. Read `AGENTS.md`, `README.md`, and the relevant skill.
2. State the workflow goal, data boundary, and expected artifacts.
3. Run only local validators unless the prompt explicitly allows public metadata fetches.
4. Return concrete file references, validation results, and claim limits.
