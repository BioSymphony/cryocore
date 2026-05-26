# Linear Wave Planning Prompt

Use this prompt when an agent should turn CryoCore work into a bounded issue
wave for Linear or another tracker.

```text
Use the CryoCore skill pack. Plan a tracker issue wave for <campaign goal>.
Read docs/workflows.md, docs/linear-orchestration.md,
campaigns/cryoem-raw-to-atomic-dossier/issue-dag.md, templates/linear-issue.md,
and templates/symphony-cryocore.WORKFLOW.md.

Keep future and cost-bearing work in Backlog. Activate only the first local or
prep wave. Use one worker until issue references and validators pass. Do not put
secrets, provider IDs, raw logs, private data, or license files in issues.

Return:
- proposed wave order
- issue titles and dependencies
- labels for provider, gate, risk, and wave
- operator gates for paid, mutating, raw-data, or license-gated work
- validation commands for each issue
- final outcome block requirements
```
