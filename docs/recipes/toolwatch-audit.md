# Recipe: Toolwatch Audit

## Inputs

- Tool name.
- Primary sources: official docs, repository, paper, release notes, or archive
  API docs.

## Commands

```bash
make registry-check
make public-release-report
```

## Files Produced

- Updated dated toolwatch note when the audit is broad.
- Updated `references/software-registry.yaml` only when posture is useful and
  source-backed.
- Updated `docs/tooling-and-licensing.md` for durable policy.

## Claim Ceiling

Tool posture only. Do not claim installation, license approval, performance, or
redistribution readiness without current evidence.

## Failure Handling

When terms, source, weights, or redistribution are unclear, classify as `watch`
or `gated`.

## Related

- [Linear template: Toolwatch Audit](../../templates/linear-toolwatch-audit.md): tracker-ready issue shape for this recipe.
- [Toolwatch skill](../../skills/cryocore-toolwatch/SKILL.md): the skill an agent loads to run this recipe.
- [Tooling and Licensing](../tooling-and-licensing.md): the durable posture doc that audits land in.
- [Toolwatch To Lane Policy](../toolwatch-to-lane-policy.md): when a tool moves from watch into a lane.
- [Software Registry](../../references/software-registry.yaml): machine-readable posture records.

