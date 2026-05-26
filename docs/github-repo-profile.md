# GitHub Repo Profile

Use this when creating or switching the public GitHub repository.

## Suggested Description

Agent-ready workflows for cryo-EM map/model review, density support, figures,
states, provider plans, schemas, validators, and tracker-ready issue waves.

## Suggested Topics

- `cryo-em`
- `cryoem`
- `cryo-electron-microscopy`
- `structural-biology`
- `protein-structure`
- `computational-biology`
- `bioinformatics`
- `scientific-workflows`
- `research-agents`
- `agent-tools`
- `ai-agents`
- `agentic-workflows`
- `workflow-validation`
- `reproducibility`
- `provenance`
- `runpod`
- `emdb`
- `pdb`
- `public-data`
- `open-science`

## Homepage

Leave blank until a stable public docs page exists, or point to the repository
README.

## Social Preview

Use `docs/assets/cryocore-banner.jpg` as the source social-preview image.

Do not upload screenshots containing private paths, provider IDs, private run
logs, unpublished structures, or heavy/generated scientific artifacts.

## Pinned README Sections

The first screen should show:

- one-line value proposition
- overview image
- five-minute start
- copy-paste agent prompt
- core superpowers

## Initial Announcement

Suggested wording:

```text
BioSymphony CryoCore gives scientific agents cryo-EM map/model review
workflows: public accession summaries, density-support checks, structural
figure plans, state-comparison plans, cloud/HPC execution prep, provider run
review, tracker-ready issue waves, and explicit claim boundaries.
```

Avoid claiming:

- full cryo-EM processing engine
- turnkey provider execution
- clinical or therapeutic conclusions
- license clearance for gated tools
- publication-grade mechanism claims from demos alone

## Release-Switch Checklist

Before publishing:

```bash
make clean
make release-check
python3 scripts/cryocore/public_release_report.py --repo-root . --json
git remote -v
```

Expected:

- no private remotes
- no tracked runtime output
- no private markers or secret-like content
- no heavy scientific artifacts
- public release report `ok: true`
