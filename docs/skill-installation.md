# Skill Installation

This repo is usable as a local skill pack without publishing anything.

## Use In Place

Point an agent at this checkout and ask it to read:

- `AGENTS.md`
- `skills/cryocore/SKILL.md`
- the specialized skill for the task

This is the safest default because validators, schemas, examples, and docs stay
together.

## Copy Skills Into Another Agent Environment

If your agent runtime supports local skills, copy the directories under
`skills/` into that runtime's skill directory. Keep the repo checkout available
too, because the skills refer to docs, schemas, templates, and validators.

Recommended install set:

- `cryocore`
- `cryocore-public-safety`
- `cryocore-map-model-dossier`
- `cryocore-run-closeout`
- `cryocore-toolwatch`
- `cryocore-heterogeneity-jury`
- `cryocore-figure-dossier`

## Safety Rule

Do not copy private run notes, ignored runtime directories, credentials, provider
logs, license files, or downloaded biological data into a public skill bundle.
Run `make release-check` before sharing a packaged copy.

