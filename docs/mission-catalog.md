# Mission Catalog

A menu of seed missions your coding agents can take on with CryoCore. Each
entry names a starting point, the resource mode, the artifact that proves
progress, and the rough scope. Pick one, hand it to your agent, and review
what comes back.

![Mission arc](assets/mission-arc.svg)

The catalog is sorted from smallest to largest. Local-only missions need no
network and no credentials. Public-metadata missions hit EMDB, PDB, and wwPDB.
Provider missions stay in prep mode by default; a real paid run requires
operator authorization.

## Local-only missions

| Mission | Resource mode | First artifact | Rough scope |
| --- | --- | --- | --- |
| Run `make demo-local` and write a one-paragraph summary of the review shape. | local | The summary itself, plus a pointer into `.runtime/t2r14-open-dossier/`. | 15 minutes. |
| Compare two skills under `skills/` and report when each one fires. | local | A short skill-comparison note in your agent's reply. | 15 minutes. |
| Validate that every JSON file under `modules/schemas/` and `modules/campaigns/` parses cleanly. | local | `make module-check` output appended to a brief report. | 15 minutes. |
| Audit `references/software-registry.yaml` for missing fields, stale versions, or broken posture entries. | local | A diff-or-note list of findings with suggested edits. | 30 minutes. |
| Read `docs/glossary.md` and propose three new entries that would help a newcomer. | local | A short proposal block your agent posts back to you. | 30 minutes. |

## Public-accession review missions

| Mission | Resource mode | First artifact | Rough scope |
| --- | --- | --- | --- |
| Build a public-accession map/model review for an EMDB and PDB pair of your choice. | public-metadata-network | An input audit and figure-rendering plan that lists declared inputs and the claim ceiling. | 1-2 hours. |
| Compare two public deposited structures of the same target and produce a state or structure-review plan. | public-metadata-network | A comparison plan citing both deposits and the difference axes the agent would compare. | 1-2 hours. |
| Audit one PDB entry's wwPDB validation report and summarize what the deposit supports. | public-metadata-network | A bounded-claims note plus a short prose summary of the validation report. | 1-2 hours. |
| Reproduce the Pol Theta map/model prep check and describe the contract-self-check output. | public-metadata-network | The prep-check log plus a contract-self-check pass record. | 1 hour. |

## Tracker wave missions

| Mission | Resource mode | First artifact | Rough scope |
| --- | --- | --- | --- |
| Draft a Linear-style wave for a four-stage raw-to-atomic campaign on EMPIAR-10204. | tracker-wave | Four issue bodies with dependencies, labels, and operator gates. | 2 hours. |
| Plan a heterogeneity jury wave that compares two structural interpretations of one public dataset. | tracker-wave | A wave plan with the comparison contract spelled out. | 2 hours. |
| Re-shape the [Pol Theta sample wave](../examples/sample-linear-wave/) into one that runs the same checks against a different EMDB/PDB pair. | tracker-wave | Updated issue bodies pointing at the new accessions. | 1 hour. |

## Provider missions (prep mode)

| Mission | Resource mode | First artifact | Rough scope |
| --- | --- | --- | --- |
| Prepare a RunPod bridge manifest for a public-accession map/model review and confirm `make runpod-scope-check` and `make runpod-reference-check` pass. | operator-gated-provider (prep only) | Validated bridge manifest, scope report. | 1-2 hours. |
| Audit one provider profile under `modules/provider-profiles/` and propose updates to its launch-request template. | operator-gated-provider (prep only) | A diff or note listing proposed updates with justifications. | 1-2 hours. |
| Draft a stage contract for a map-to-model lane on a generic cloud VM. | operator-gated-provider (prep only) | New stage-contract JSON under `runpod/stage-contracts/` with passing validators. | 2 hours. |

## Provider run review missions

| Mission | Resource mode | First artifact | Rough scope |
| --- | --- | --- | --- |
| Review a hypothetical RunPod artifact package and decide whether it should be treated as complete. | provider-closeout | A pass/blocker report referencing artifacts, hashes, cost records, and cleanup proof. | 1 hour. |
| Score the contract-self-check output of one fixture run and explain any blockers in plain English. | local | A short report mapping each blocker to the contract field it failed. | 30 minutes. |

## Skill-pack and adoption missions

| Mission | Resource mode | First artifact | Rough scope |
| --- | --- | --- | --- |
| Adapt CryoCore patterns into a new structural-biology repo (X-ray, NMR, or hybrid). | local | A starter `SKILL.md` and adoption notes pointing at the parts that need domain re-wiring. | 1 day. |
| Add a new skill under `skills/<your-skill>/SKILL.md` for a workflow that is currently missing from the skill pack. Run `make skill-check`. | local | New skill directory with passing validators and an entry in `skills/index.yaml`. | 1 day. |
| Copy the skill pack into another scientific repo and report which validators carry over without changes. | local | A short adoption report with the carry-over list and the gaps. | 1 day. |

## Documentation and polish missions

| Mission | Resource mode | First artifact | Rough scope |
| --- | --- | --- | --- |
| Add a glossary entry for a cryo-EM term that is currently missing. | local | Updated `docs/glossary.md` with the new entry and links from related docs. | 30 minutes. |
| Expand a recipe in `docs/recipes/` with concrete copy-paste flows and expected outputs. | local | Updated recipe doc and a passing `make docs-link-check`. | 1 hour. |
| Add a new agent-task prompt fixture under `examples/agent-tasks/` for a use case not yet covered. | local | New `.prompt.md` and an entry in `examples/agent-tasks/README.md`. | 1 hour. |

## How to use the catalog

Pick the smallest mission that captures the work you actually want done. Paste
the row's mission text into your agent along with the [Agent Prompt](../README.md#agent-prompt)
from the README. The agent will read the relevant skill, run the validators
named in the linked docs, and report what it found.

If a mission ends up larger than expected, your agent should split it into a
tracker wave using the [Linear Wave Planning prompt](../examples/agent-tasks/linear-wave-planning.prompt.md)
and stop at the first operator gate.
