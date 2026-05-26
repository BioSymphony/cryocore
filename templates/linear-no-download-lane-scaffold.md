# No-Download Lane Scaffold

## Scope

This issue is limited to manifest, schema, module, stage-contract, template, or
toolcheck scaffolding. It must not launch a provider run, download raw data,
install gated software, or cache model weights.

## Lane

- Tool or lane:
- Image family:
- Registry entry:
- Smoke command:
- Expected tiny fixtures:

## Acceptance

- No raw downloads.
- No pod launch or paid compute.
- No gated installer, license file, secret, or model weight.
- Local validators pass.
- Expected artifacts and blockers are documented.

## Validation

```bash
make preflight
make registry-check
make module-check
make test
```
