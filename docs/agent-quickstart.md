# Agent Quickstart

Give your agent a task and `skills/cryocore/SKILL.md`. CryoCore supplies tool
knowledge, callable helpers, and rules for passing checked outputs between
tools. Start with the [tool-use guide](tool-use-and-chaining.md) for concrete
calls and runtime requirements.

## Best First Prompt

This is the canonical CryoCore agent prompt. The README's
[Agent Prompt](../README.md#agent-prompt) section uses the same text.

```text
Use CryoCore for [my task]. Read AGENTS.md, skills/cryocore/SKILL.md,
docs/tool-use-and-chaining.md, and the relevant software registry records.
Choose tools and explain why they fit. Build a sequence of calls with explicit
inputs and outputs. Run supported calls within my authorized scope, and check
each output before passing it to the next tool. If a tool is unavailable,
identify the missing requirement and continue independent steps.
Use paid compute, raw downloads, and gated tools only with explicit authorization.
Keep private data, secrets, logs, heavy data, weights, and license files out of
git and public outputs. Report the calls made, results, checks, and limitations.
```

## What The Agent Should Read

| Task | Skill |
| --- | --- |
| General CryoCore work | `skills/cryocore/SKILL.md` |
| Public release, privacy, or secrets | `skills/cryocore-public-safety/SKILL.md` |
| Map/model review | `skills/cryocore-map-model-dossier/SKILL.md` |
| Provider run review | `skills/cryocore-run-closeout/SKILL.md` |
| Tool/license audit | `skills/cryocore-toolwatch/SKILL.md` |
| Heterogeneity/state review | `skills/cryocore-heterogeneity-jury/SKILL.md` |
| Figure workflow | `skills/cryocore-figure-dossier/SKILL.md` |

## What The Agent Should Produce

- Tool choices and the reason for each choice.
- Calls with explicit inputs, outputs, parameters, and runtime requirements.
- Results and checks for each handoff, including failures or substitutions.
- The next usable outputs and the conclusions supported by the evidence.

## Minimum Acceptable Agent Run

For a public release or release-readiness review, an agent should at least:

1. Read `AGENTS.md`, `README.md`, this guide, and the relevant skill.
2. State whether the task is local-only, networked public metadata, or
   operator-gated provider work.
3. Run:

   ```bash
   make docs-link-check
   make skill-check
   make goal-brief-check
   make public-snapshot-check
   ```

4. For release readiness, also run:

   ```bash
   make release-check
   ```

5. Report blockers first, then changed files, check results, claim ceiling, and
   remaining issues.

Support the outcome with artifact checks and scientific validation results,
including any missing evidence.

## Starter Tasks

Use fixtures under `examples/agent-tasks/`:

- `public-safety-review.prompt.md`
- `map-model-dossier.prompt.md`
- `cloud-provider-prep.prompt.md`
- `goal-to-campaign.prompt.md`

## Local Validation Ladder

```bash
make doctor
make goal-brief-check
make skill-check
make runpod-scope-check
make provider-closeout-check
make release-check
```

See `docs/validation-command-matrix.md` for side effects and network behavior.
