# Goal To Campaign Prompt

```text
Use the CryoCore skill pack and treat this as a `/goal`-style long-horizon
request. Read AGENTS.md, README.md, docs/goal-orchestration.md,
docs/workflows.md, templates/goal-brief.md, and the relevant skill under
skills/.

Goal:
<paste the user goal here>

Work locally first. Fill or draft a CryoCore goal brief, classify the resource
mode, identify the first useful artifact, and decide whether this should remain
a single-agent task or become a tracker issue wave. Keep future and cost-bearing
work blocked until a human/operator gate is explicit. Do not put secrets,
license files, raw/heavy cryo-EM data, model weights, or provider logs in git,
issue bodies, or public artifacts.

Return:
- goal brief summary
- first wave or single-task plan
- expected artifacts and claim ceiling
- validation commands to run now
- blockers, operator gates, and residual risks
```
