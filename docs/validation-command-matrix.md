# Validation Command Matrix

Use this matrix to pick the smallest local check that proves the thing you
changed. `make release-check` remains the public release gate.

| Goal | Command | Network | Provider mutation | Writes ignored output |
| --- | --- | --- | --- | --- |
| Public release readiness | `make release-check` | no | no | Python caches only |
| Fast repo doctor | `make doctor` | no | no | no |
| Markdown links and backticked path references | `make docs-link-check` | no | no | no |
| Secret, private marker, and heavy artifact scan | `make public-snapshot-check` | no | no | no |
| Skill-pack metadata | `make skill-check` | no | no | no |
| Reusable goal brief template | `make goal-brief-check` | no | no | no |
| Schema fixtures | `make schema-check` | no | no | no |
| RunPod manifest and reference integrity | `make runpod-check` | no | no | no |
| Bridge manifest public scope | `make runpod-scope-check` | no | no | no |
| Prep-mode launch preflight | `make launch-preflight-prep` | no | no | no |
| Real launch readiness check | `make launch-preflight-real` | may check public git ref | no | no |
| License/tool posture freshness | `make tooling-freshness-check` | no | no | no |
| Tiny public-coordinate demo | `make demo-local` | yes, public RCSB/mmCIF | no | `.runtime/` |
| Same tiny demo target, explicit name | `make demo-t2r14-local` | yes, public RCSB/mmCIF | no | `.runtime/` |
| Public accession metadata smoke | `make public-metadata-check` | yes | no | no by default |
| No-download toolcheck fixture | `make toolcheck` | no | no | `.runtime/` |
| No-false-success closeout fixture | `make provider-closeout-check` | no | no | no |
| Full local test suite | `make test` | may query public metadata | no | `.runtime/`, caches |

## Release Rule

Before a public switch, run:

```bash
make clean
make release-check
python3 scripts/cryocore/public_release_report.py --repo-root . --json
```

If `gitleaks` is unavailable locally, CI installs it and runs
`REQUIRE_GITLEAKS=1 make release-check`.

`make release-check` includes preflight, registry freshness, docs links,
module/skill/schema checks, RunPod contract and scope checks, provider closeout
fixtures, Python compile, pytest, public release report, and secret scanning
when `gitleaks` is available or required.

## Related

- [No-False-Success Hardening](no-false-success-hardening.md): the rules these validators enforce.
- [Schema Catalog](schema-catalog.md) and [Module Catalog](module-catalog.md): the contracts the schema and module checks evaluate.
- [Public Quickstart](public-quickstart.md): the smaller subset of commands a first-time reader runs.
- [Troubleshooting](troubleshooting.md): what to do when one of these checks fails.
