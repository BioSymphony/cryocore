# Scripts

Scripts are Python standard-library utilities unless noted otherwise.

High-use commands:

- `public_release_report.py`: read-only public readiness report.
- `public_snapshot_check.py`: secret, heavy-artifact, and private-marker scan.
- `docs_link_check.py`: local Markdown link and image target validation.
- `provider_closeout_check.py`: provider/run closeout validator.
- `provider_runner.py`: local no-download provider lane runner.
- `contract_self_check.py`: joins manifests, artifacts, and claim levels.
- `schema_check.py`: local JSON Schema subset validator.
- `module_manifest_check.py`: module and campaign contract validator.
- `runpod_manifest_check.py`: launch manifest validator.
- `runpod_scope_check.py`: RunPod bridge boundary validator.
- `bridge_manifest_check.py`: generated bridge manifest freshness validator.
- `runpod_reference_check.py`: stale resume-command and entrypoint reference validator.
- `tooling_freshness_check.py`: license/tool review freshness validator.
- `skill_pack_check.py`: public skill-pack index and agent metadata validator.
- `goal_brief_check.py`: lightweight `/goal` brief validator.
- `issue_check.py`: tracker issue-pack validator.

Run the aggregate gate:

```bash
make release-check
```
