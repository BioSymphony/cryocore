# Contributing

Thanks for helping improve `cryocore`.

## New here?

If this is your first visit, the warmest landing pad is the [Tour](docs/tour.md).
It walks through the repo in fifteen minutes and points to the parts you are
most likely to extend. The [Glossary](docs/glossary.md) covers the cryo-EM
vocabulary and CryoCore terms you will hit while reading code and docs.

Good first contributions: docs polish, recipe expansion, additional public
demo fixtures, glossary entries, and skill-pack improvements. The ground rules
below apply to any contribution.

## Ground Rules

- Public-safe synthetic or public-accession examples only.
- Do not add private biological data, generated structure archives, provider logs, credentials, or local operator notes.
- Keep claim levels explicit.
- Keep validators dependency-free at runtime unless an optional adapter is clearly separated.
- Prefer compact ledgers and manifests over large generated artifacts.
- Run `make release-check` before opening a pull request.

## Local Workflow

```bash
python3 -m pip install -r requirements-dev.txt
make readonly-check
python3 -m pytest -q
make release-check
```

Use `docs/validation-command-matrix.md` to choose a smaller check while you are
iterating. Use `make clean` before a final public release check if you generated
ignored runtime output.

## Adding A Campaign Example

1. Create `examples/<campaign-id>/`.
2. Add `campaign-manifest.json`.
3. Add a compact target-window or input dossier.
4. Add `stage-contract.json` if the example has long-running or GPU stages.
5. Add a compact claim ledger or dossier manifest only when claim levels and evidence modes are clear.
6. Add `README.md` describing scope, public data sources, and non-claims.
7. Run `make release-check`.

## Adding An Issue Pack

Issue packs should stay tracker-neutral. Use IDs like `CRYOCORE-W00` rather than private tracker IDs. A private workflow can map those IDs to Linear, GitHub Issues, or another system after public validation.

## Adding A Skill Or Agent Prompt

1. Add or update `skills/<skill-id>/SKILL.md`.
2. Add `skills/<skill-id>/agents/openai.yaml`.
3. Update `skills/index.yaml`.
4. Add a prompt fixture under `examples/agent-tasks/` when useful.
5. Run `make skill-check` and `make release-check`.

## Security Review Before PR

Run:

```bash
make public-snapshot-check
make runpod-scope-check
make runpod-reference-check
make tooling-freshness-check
```

Do not paste provider credentials, private repository URLs, internal machine
paths, license acceptance records, or unpublished biological data into issues,
PRs, docs, logs, manifests, or fixtures.

## Style

- ASCII text by default.
- Stdlib-only runtime code.
- Small, deterministic tests.
- Warnings for guidance gaps, errors for public-safety or structural blockers.
