# Public Repo And Private Image Policy

CryoCore separates public contracts from private runtime material.

## Public Repo May Contain

- Source code for validation, manifest checks, and public demos.
- Provider-neutral launch and stage contracts.
- Public accession identifiers and metadata-only examples.
- Tiny synthetic fixtures.
- Documentation for gates, limitations, and expected artifacts.

## Public Repo Must Not Contain

- Provider API keys, registry tokens, cloud credentials, deploy keys, or license
  identifiers.
- Private GitHub URLs, private clone instructions, or organization-internal
  paths.
- Raw cryo-EM movies, particle stacks, maps, half-maps, masks, private
  structures, unpublished sequences, or model weights.
- Proprietary installers, binary license files, or private container contents.

## Private Runtime Material

Private images and provider credentials belong in operator-owned infrastructure.
The public repo may validate that a launch packet is well formed, but it should
not make a paid remote mutation by itself.

Before a public switch, run:

```bash
make release-check
```

## Related

- [Data Policy](data-policy.md): the data tiers and git boundaries this policy enforces.
- [Privacy Threat Model](privacy-threat-model.md): assets to protect and the scanners that defend them.
- [License Scope](license-scope.md): the MIT-license boundary on CryoCore source.
- [Tooling and Licensing](tooling-and-licensing.md): per-tool license posture for runtime gating.
- [Public Switch Checklist](public-switch-checklist.md): the readiness list before a public switch.

