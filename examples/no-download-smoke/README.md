# No-Download Smoke

A tiny local fixture for agents and humans who want to confirm CryoCore's
contract shape works on a fresh checkout without touching the network.

The manifest declares three local checks:

- `software_registry_shape`: parses `references/software-registry.yaml` and verifies the registry's structure.
- `repo_preflight`: runs the repository preflight from `scripts/cryocore/preflight.py`.
- `module_json_parse`: parses the JSON contracts under `modules/`.

Claim level is `candidate` because the fixture stops before any data fetch,
provider call, or scientific analysis. The smoke proves the contracts parse
and the validators work; nothing more.

## Run it

```bash
python3 scripts/cryocore/preflight.py --repo-root . --json
python3 scripts/cryocore/software_registry_check.py references/software-registry.yaml --json
make module-check
```

## When to use it

- First mission your agent runs after pointing at the repo, to confirm the contracts parse and the validators work.
- Smallest reproducible reference when a release-gate failure looks contract-shaped rather than data-shaped.
- Source fixture for skill-pack adopters who want a baseline that runs anywhere.

## Related

- [Tour](../../docs/tour.md)
- [Validation Command Matrix](../../docs/validation-command-matrix.md)
- [Examples index](../README.md)
