# Goal Orchestration

CryoCore gives Codex, Claude Code, Symphony, Linear, and `/goal`-style agents a
domain contract for cryo-EM work: what to read, what to keep out of git, what
artifacts prove progress, what validators to run, and where scientific claims
rest.

Use [templates/goal-brief.md](../templates/goal-brief.md) when the request is
bigger than one obvious edit. The brief should be just complete enough for a
capable agent to plan the first useful step.

## Goal Brief Loop

1. Restate the user goal in one sentence.
2. Classify the resource mode.
3. Name the first artifact that would make progress inspectable.
4. Decide whether the work is a single-agent task or a tracker issue wave.
5. Keep future, provider, and cost-bearing work blocked until gates are explicit.
6. Run the smallest local validator before broadening the work.
7. Close with [templates/final-outcome-block.md](../templates/final-outcome-block.md) or a concise handoff.

## Resource Modes

| Mode | Use when | First check |
| --- | --- | --- |
| `local_only` | docs, manifests, fixtures, local validators, or tiny demos are enough | `make goal-brief-check` |
| `public_metadata_network` | released accessions or public metadata are allowed | `make public-metadata-check` |
| `operator_gated_provider` | GPU cost, RunPod, SSH/HPC, raw downloads, or gated tools enter scope | `make provider-check` |
| `tracker_wave` | the goal needs multiple bounded work packets or review gates | `make issue-check` |
| `provider_closeout` | a remote or long-running workflow claims to be done | `make provider-closeout-check` |

The mode names a starting point. From there, a capable agent reads the relevant
skill, inspects current files, and chooses the smallest next artifact.

## When To Split

Keep the work as one agent task when the output is one document, one manifest,
one local fixture, or one validation pass. Split into tracker issues when the
goal has independent artifact families, provider mutation, license gates, large
data movement, or multiple review stages.

Use [Workflow Blueprints](workflows.md), [Tracker Orchestration](linear-orchestration.md),
and [Provider Readiness](provider-readiness.md) for the surrounding checks. The
public [workflow template](../templates/symphony-cryocore.WORKFLOW.md) is a
checklist for a private operator workflow. Credentials live outside the repo.

## Useful First Prompt

```text
Use CryoCore goal orchestration. Read AGENTS.md, README.md,
docs/goal-orchestration.md, templates/goal-brief.md, and the relevant skill
under skills/. Treat this as a long-horizon goal, but only activate the first
bounded local/prep step. Classify the resource mode, produce or update the goal
brief, identify first artifacts, validation commands, claim ceiling, blockers,
and whether this should become a tracker issue wave. Do not launch providers or
expose secrets unless an explicit operator gate allows it.
```

## Handoff

When handing work between agents, use [templates/agent-handoff.md](../templates/agent-handoff.md).
The handoff should name the repo, goal, claim ceiling, data boundary, commands
run, artifact root, and smallest next validation command. It should not attempt
to encode every possible downstream decision; that is the agent's job.
