# Local Installation

CryoCore runs as a source checkout in the public pre-alpha. The whole value of
the repo is the bundle of skills, docs, schemas, manifests, fixtures,
templates, and validators that ship together, which agents read directly.

## Requirements

- Python 3.10 or newer.
- GNU Make or a compatible `make`.
- `gitleaks` for the strongest local release gate. CI installs it if missing.

## Setup

```bash
python3 -m venv .runtime/venv
. .runtime/venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements-dev.txt
make doctor
```

## Run A Demo

```bash
make demo-local
```

The demo writes ignored output under `.runtime/`.

## Run The Public Gate

```bash
make release-check
```

## Why a source checkout for now

The public repo is meant to be inspected and reused by agents. A source
checkout keeps the docs, skills, schemas, manifests, issue templates, and
examples visible alongside the code. Future releases may add a packaged CLI
while keeping the source-checkout workflow as the reference mode.
