# Recipe: Heterogeneity Jury

Mode: planning and validation scaffold. Particle classification, state
assignment, and GPU analysis happen in lanes that consume this scaffold and
live outside git.

## Inputs

- Particle, map, or state references outside git.
- Method list and expected comparison artifacts.
- Claim ledger target.

## Commands

```bash
make module-check
make public-release-report
```

## Files Produced

- state-selection rationale
- disagreement matrix
- particle subset references
- caveats for ambiguous states

## Claim Ceiling

`candidate` unless state assignments are joined to map/model validation and
expert scientific review.

## Failure Handling

Treat conflicting states as evidence. Record the disagreement and downgrade
the claim ledger so the ambiguity stays visible to the reviewer.

## Related

- [Linear template: Heterogeneity Jury](../../templates/linear-heterogeneity-jury.md): tracker-ready issue shape for this recipe.
- [Heterogeneity Jury skill](../../skills/cryocore-heterogeneity-jury/SKILL.md): the skill an agent loads to run this recipe.
- [Glossary: heterogeneity, map / model fit](../glossary.md#cryo-em-vocabulary): vocabulary the disagreement matrix uses.
- [Claim Levels](../claim-levels.md): the ladder this recipe downgrades against when states conflict.
