# Documentation

![BioSymphony CryoCore overview](assets/cryocore-overview.svg)

## Choose Your Path

| I need to... | Start here |
| --- | --- |
| Take a fifteen-minute walk through the repo | [Tour](tour.md) |
| Run the demo or release gate | [Public Quickstart](public-quickstart.md) |
| Point an agent at CryoCore | [Agent Quickstart](agent-quickstart.md) |
| Turn a broad `/goal` into bounded work | [Goal Orchestration](goal-orchestration.md) |
| Choose public-accession, cloud, Linear, or run-review path | [Workflow Blueprints](workflows.md) |
| Pick a workflow and copy a prompt | [Use Cases](use-cases.md) |
| Browse seed missions | [Mission Catalog](mission-catalog.md) |
| Walk through one mission end to end | [Pol Theta Walkthrough](missions/pol-theta-walkthrough.md) |
| Copy patterns into another repo | [Adoption Guide](adoption-guide.md) and [Agent Skill Guide](agent-skill-guide.md) |
| Install the skill pack in another scientific repo | [Skill Installation](skill-installation.md) |
| Understand source-checkout setup | [Local Installation](local-installation.md) |
| Look up cryo-EM vocabulary or CryoCore terms | [Glossary](glossary.md) |
| Find copyable prompts | [Prompt Library](prompt-library.md) and [Agent Task Prompts](../examples/agent-tasks/README.md) |
| Pick a smaller validator while iterating | [Validation Command Matrix](validation-command-matrix.md) |
| Debug a failing gate | [Troubleshooting](troubleshooting.md) and [Failure Modes](failure-modes.md) |

## Core Policy

- [Data Policy](data-policy.md): data tiers and git boundaries.
- [Claim Levels](claim-levels.md): evidence and claim ladder.
- [Privacy Threat Model](privacy-threat-model.md): privacy, secret, and public-switch controls.
- [No-False-Success Hardening](no-false-success-hardening.md): how CryoCore confirms artifacts, hashes, validation, and cleanup before treating a run as complete.
- [Public Repo And Private Image Policy](public-repo-and-private-image-policy.md): public/private runtime split.

Tool and license posture:

- [Tooling And Licensing](tooling-and-licensing.md)
- [License Scope](license-scope.md)
- [Toolwatch 2026-05-15](toolwatch-2026-05-15.md)
- [Toolwatch To Lane Policy](toolwatch-to-lane-policy.md)
- [ChimeraX Shared Posture](chimerax-shared-posture.md)

Contracts and execution:

- [Schema Catalog](schema-catalog.md)
- [Module Catalog](module-catalog.md)
- [Provider Execution Model](provider-execution-model.md)
- [Compute Backends](compute-backends.md)
- [Provider Readiness](provider-readiness.md)
- [RunPod Stack](runpod-stack.md)
- [Workflow Orchestration Provenance](workflow-orchestration-provenance.md)
- [Public Accession APIs](public-accession-apis.md)
- [Linear Orchestration](linear-orchestration.md)
- [Workflow Blueprints](workflows.md)
- [Goal Orchestration](goal-orchestration.md)

Public switch:

- [Public Launch Pad](PUBLIC_LAUNCH_PAD.md)
- [Public Switch Checklist](public-switch-checklist.md)
- [GitHub Repo Profile](github-repo-profile.md)

Architecture and split:

- [Split Evaluation](split-evaluation.md): CryoCore vs Structure Factory split rationale.
- [Move/Duplicate Map](move-duplicate-map.md): which posture records are intentionally duplicated across the two repos.

Community and examples:

- [Demo Gallery](demo-gallery.md)
- [Recipes](recipes/README.md)
- [FAQ](../FAQ.md)
- [Roadmap](../ROADMAP.md)
