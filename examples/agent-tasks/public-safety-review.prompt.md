# Prompt: Public Release Review

Review this local `biosymphony-cryocore-public` checkout for public release
readiness. Stay local. Do not push, publish, launch providers, or request
credentials.

Use the public safety skill. Check README clarity, onboarding docs, examples,
diagrams, release gates, privacy, secrets, heavy artifacts, license posture,
bridge manifests, issue templates, and claim boundaries. Run the smallest local
validators first, then `make release-check` if the repo looks ready.

Return:

- findings ordered by release risk
- files changed, if any
- validation commands and results
- residual risks before public switch
