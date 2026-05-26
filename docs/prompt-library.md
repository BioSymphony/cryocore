# Prompt Library

For ready-to-run prompt fixtures, see
[Agent Task Prompts](../examples/agent-tasks/README.md).

These prompts are designed for agents using this repo to produce useful,
inspectable cryo-EM workflow artifacts.

## Goal To Campaign

```text
Use CryoCore goal orchestration. Turn <broad goal> into a goal brief, resource
mode, first useful artifact, validation commands, and split/no-split decision.
Stay local unless public metadata or operator-gated provider work is explicitly
allowed.
```

## Map/Model Review

```text
Use CryoCore. Plan a map/model review for EMDB <id> and PDB <id>. Classify
data tier, density and model questions, expected artifacts, figure plan, claim
ceiling, required validators, and what must stay outside git. Do not launch
providers or download heavy data.
```

## Claim Audit

```text
Use CryoCore claim-level rules. Review this claim ledger and downgrade any
claim that lacks direct evidence. Return claim, level, evidence artifact, and
caveat for each row.
```

## Provider Run Review

```text
Use CryoCore run-closeout. Given a provider-run JSON and artifact root, decide
whether the run is closeout_ready. Require input audit, terminal stage contract,
contract self-check, hashes, cost report, cleanup proof, and claim ledger.
```

## Cloud Provider Prep

```text
Use CryoCore provider prep. Choose the provider profile and execution profile,
then list the stage contract, artifact root, operator gate, budget/storage/image
requirements, local validation commands, and artifact-review proof. Stay in prep
mode; do not launch paid resources or touch credentials.
```

## Linear Wave Planning

```text
Use CryoCore tracker orchestration. Turn <campaign> into a small Linear-style
issue wave. Keep future and cost-bearing work in Backlog, activate only the
first local/prep wave, add provider/gate/risk labels, and require final outcome
blocks with artifacts, validators, claim level, and residual risk.
```

## Toolwatch

```text
Use CryoCore toolwatch. Research <tool> from primary sources only. Classify as
planned, gated, or watch. Record license, redistribution, runtime, model-weight,
and public-image posture. Do not add installer URLs, secrets, or license files.
```

## Public PR Review

```text
Review this CryoCore change for public release readiness. Prioritize newcomer
clarity, working examples, docs, release gates, secrets, private paths, heavy
artifacts, raw biological data, license posture, provider mutation,
false-success risk, and unsupported scientific claims.
```
