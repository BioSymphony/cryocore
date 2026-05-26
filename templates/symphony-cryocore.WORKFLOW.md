# Operator Workflow Template

This file is public pseudocode for private operator integration. It is not a
ready-to-run workflow and does not include tracker credentials, cloud commands,
or local workstation paths.

```yaml
tracker:
  kind: operator-selected
  routing_label: sym:cryocore
  active_states: [Todo, In Progress]
  terminal_states: [Done, Closed, Canceled, Duplicate]

campaign:
  mode: direct-done
  trust: trusted-local
  integration_owner: operator-owned-after-run

workspace:
  root: operator-owned-workspace-root

hooks:
  after_create:
    - copy_or_clone_clean_public_checkout
    - remove_operator_runtime_markers
  after_run:
    - if_launch_request_present_then_run_operator_owned_provider_closeout
    - fetch_hash_validate_artifacts
    - verify_budget_and_cleanup
    - update_tracker_only_after_closeout_passes

agent:
  max_concurrent_agents: 1
  overlap_aware: true
  max_turns: 8
```

## Operator Adaptation Checklist

Before using this as a real workflow, create a private operator copy outside the
public repo and fill in:

- tracker kind, credentials source, project slug, states, and routing label
- clean checkout or snapshot path for `hooks.after_create`
- worker command with a narrow environment allowlist
- host-side closeout commands for any paid provider run
- budget, cleanup, and artifact retention policy
- final outcome block format consumed by the chosen tracker

Do not add workstation paths, secrets, provider logs, billing data, private data,
license records, or raw scientific outputs to this public template.

You are working on tracker issue `{{ issue.identifier }}` for BioSymphony CryoCore.

Title: {{ issue.title }}

Body:
{{ issue.description }}

## Required behavior

- Read `AGENTS.md`, `README.md`, and `skills/cryocore/SKILL.md` before editing.
- Keep changes bounded to the issue and its declared touched areas.
- Run validation commands exactly as written.
- Skip `Todo` issues with unresolved `Blocked by:` dependencies; `Todo` can name
  the current wave, not immediate permission to ignore blockers.
- Do not launch RunPod, call provider create APIs, create tracker projects, or mutate cloud resources from the worker shell.
- For an explicitly authorized RunPod issue, generate a launch-request marker under `.runtime/` only with `scripts/cryocore/runpod_launch_request.py` after local validation passes.
- Do not download raw EMPIAR data, private data, model weights, or license-gated software unless the issue includes an explicit operator gate and the repo validators allow it.
- Provider status is not scientific success. Final success requires fetched artifacts, hashes, validation reports, cost report, and cleanup proof.
- For non-RunPod prep issues, move completed issues to `Done` after validation and self-review.
- For RunPod launch-request issues, write the launch request and final tracker comment, then let operator-owned closeout own provider mutation and final state.
- Final comments must include a structured outcome block with status, files touched, validation summary, and suggested action.
