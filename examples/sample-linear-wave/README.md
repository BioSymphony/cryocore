# Sample Linear Wave

A small worked Linear-style wave for the Pol Theta map and model dossier
mission. Three issues that an agent can pick up in order. Public accessions
only.

The matching prompt fixture is
[examples/agent-tasks/linear-wave-planning.prompt.md](../agent-tasks/linear-wave-planning.prompt.md).
The matching goal brief is
[examples/sample-goal-brief/](../sample-goal-brief/).

## Wave order

| Issue | Title | Provider | Operator gate | Wave |
| --- | --- | --- | --- | --- |
| `CRYOCORE-W1-01` | [Audit public accessions for Pol Theta map+model lane](./issue-01-audit-accessions.md) | local | no | 1 |
| `CRYOCORE-W1-02` | [Prep RunPod manifest for Pol Theta dossier](./issue-02-prep-runpod-manifest.md) | provider-neutral | no | 1 |
| `CRYOCORE-W1-03` | [Run Pol Theta dossier prep check and validate shape](./issue-03-run-prep-check.md) | local | no | 1 |

Future-wave work (paid RunPod launch, real-mode closeout review, deposition
mirroring) stays in Backlog until an operator opens the cost and license gates.

## How to read it

Each issue is a small, self-contained worker contract. It names exact inputs,
expected artifacts, validation commands, and acceptance criteria. The labels
keep the wave routable through Symphony or any Linear-driven worker harness.

Use these as references when filling out new issues for your own campaign.
