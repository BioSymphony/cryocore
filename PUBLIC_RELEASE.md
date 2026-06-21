# Public Release Readiness

Last reviewed: 2026-05-23

This repository is ready to publish when it is a clean-history public control
plane for BioSymphony CryoCore: useful for external cryo-EM users and agents,
with no private history, credentials, heavy artifacts, license files, provider
logs, or unsupported biological claims.

## Release Positioning

BioSymphony CryoCore is a public-safe harness for cryo-EM agent workflows. It
helps a user or long-running agent convert a public accession or
operator-provided dataset into:

- input and data-policy contracts
- lane and image manifests
- provider launch and stage contracts
- artifact indexes, hashes, and closeout checks
- map/model review and figure dossier scaffolds
- claim ledgers for scientist review

Out of scope: raw-data storage, wet-lab protocol management, clinical use,
therapeutic claims, and license bypass.

## Release Gates

Run from the repository root before publishing:

```bash
make release-check
```

GitHub profile setup is in `docs/github-repo-profile.md`.

While staying local, use:

```bash
python3 scripts/cryocore/public_release_report.py --repo-root . --json
```

For the final public switch after an initial commit, remote, and tag exist, use:

```bash
python3 scripts/cryocore/public_release_report.py \
  --repo-root . \
  --publish-ready \
  --expected-remote https://github.com/BioSymphony/cryocore.git \
  --json
```

The `--publish-ready` check is expected to fail before the public remote and
release tag are created.

Recommended independent checks:

```bash
find . -type f \( -name '*.mrc' -o -name '*.mrcs' -o -name '*.map' -o -name '*.star' -o -name '*.cs' -o -name '*.pdb' -o -name '*.cif' -o -name '*.mmcif' -o -name '*.fasta' -o -name '*.fastq' -o -name '*.pt' -o -name '*.safetensors' -o -name '*.zip' -o -name '*.tar' -o -name '*.tar.gz' -o -name '*.tgz' \) -not -path './.git/*' -print
find . -type f -size +25M -not -path './.git/*' -print
python3 scripts/cryocore/public_snapshot_check.py --repo-root . --profile public --json
```

Expected release state:

- `make release-check` passes.
- No `.runtime`, `artifacts`, `outputs`, raw data, maps, model weights, provider logs, or cache directories are tracked.
- No private workstation paths, private image namespaces, private clone markers, credentials, signed URLs, or license files appear.
- RunPod manifests use public placeholders or digest-pinned public images; real execution still requires operator gates.
- Claim levels stay on the schema ladder: `candidate`, `processed`, `validated`, `publishable`, `insufficient_evidence`, or `blocked`, with supporting artifacts attached at each level. A `publishable` claim still requires expert scientific review before public biological conclusions.
- Git history is created only after the release safety checks pass.

## First Agent Handoff

1. Read `AGENTS.md`, `README.md`, `PUBLIC_RELEASE.md`, and `docs/data-policy.md`.
2. Run `make release-check` before making public-readiness claims.
3. Treat all provider launch commands as review-only until an operator explicitly authorizes paid execution.
4. Do not move a provider run to success unless fetched artifacts, hashes, cost report, cleanup proof, and claim ledger all pass closeout.
5. Keep examples public-accession-only or synthetic unless a separate issue authorizes private data handling outside git.

## Known Status

This is a pre-alpha public harness. It is strongest as a skill pack, contract
set, and orchestration layer for agents. Real cryo-EM processing still depends
on current tool terms, GPU/runtime compatibility, external heavy storage, and
expert scientific review.
