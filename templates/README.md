# Templates

Templates are public-safe starting points for issue packs, operator gates, and
evidence bundles.

Use:

- `linear-issue.md` for tracker-neutral external-agent issues.
- `goal-brief.md` for broad `/goal`-style requests before issue splitting.
- `linear-no-download-lane-scaffold.md` for local/prep lanes.
- `linear-paid-provider-run.md` only as an operator-gated paid-provider contract.
- `operator-gate-record.md` to record approval outside public issue bodies when
  needed.
- `symphony-cryocore.WORKFLOW.md` as public pseudocode for operator-owned agent
  orchestration; copy it into a private operator repo before adding credentials,
  local paths, or provider commands.
- `public-accession-metadata.example.json` for metadata-only examples.
- `artifact-pull-report.json` and `derived-evidence-bundle.json` for closeout
  evidence shapes.
- `agent-handoff.md` for passing bounded work between agents or maintainers.
- `final-outcome-block.md` for closeout comments that keep evidence and claim
  boundaries visible.

For the larger workflow around these templates, see
[Workflow Blueprints](../docs/workflows.md) and
[Tracker Orchestration](../docs/linear-orchestration.md).

Before committing a filled template, run:

```bash
make issue-check
make goal-brief-check
make release-check
```
