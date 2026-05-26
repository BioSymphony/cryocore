# FAQ

## Is this a cryo-EM processing engine?

No. This repo is an agent-ready workflow layer: manifests, schemas, validators,
skills, issue contracts, map/model review demos, figure workflows, and provider
run checks. Real processing uses operator-owned runtimes and storage outside git.

## How is this different from RELION, CryoSPARC, or Scipion?

Those are processing or workflow systems. CryoCore helps agents plan and review
the work around them: declared inputs, map/model questions, figure outputs,
state comparisons, provider runs, provenance, artifact checks, and claim
boundaries. It can describe lanes that use tools such as RELION or CryoSPARC,
but it does not redistribute or bypass those tools.

## Can I run it without credentials?

Yes. The main release checks and no-download fixtures are local. Some examples
query public accession APIs when explicitly run.

## What runs on a laptop?

The validators, release checks, public snapshot scans, docs link checks, skill
checks, schemas, and the tiny T2R14 public-coordinate demo. Start with
[Public Quickstart](docs/public-quickstart.md).

## What costs money?

Nothing in the default release gate. Paid provider execution, GPU runs, raw data
transfer, and large storage are operator-owned activities outside this public
repo. See [Provider Execution Model](docs/provider-execution-model.md).

## Does it download raw EMPIAR movies?

No public default does that. Raw movie lanes are gated and must run outside git
with explicit operator authorization, scratch storage, and fetched-artifact
review.

## Why are license-gated tools mentioned?

Cryo-EM workflows often need tools with noncommercial, academic, binary, or
redistribution constraints. Public docs can model those gates; public images and
default commands must not bypass them.

## Can I use it in a private repo?

Yes. Use [Adoption Guide](docs/adoption-guide.md). Keep private data, local
paths, credentials, license files, and provider logs out of any public skill
bundle or issue text.

## How do I cite it?

Use [CITATION.cff](CITATION.cff) for the software repo, and also cite the
specific public accessions, tools, and datasets used by your run. CryoCore is
not a substitute for primary scientific citations.

## What should I copy into another repo?

Start with the skills, schemas, claim-level docs, provider run checks, and
public snapshot checks. Keep project-specific accessions, licenses, and private
data out of reusable templates.

## Is this clinical or therapeutic advice?

No. The demos and validators are engineering support for evidence workflows.
They do not establish clinical, therapeutic, regulatory, or final biological
mechanism claims.
