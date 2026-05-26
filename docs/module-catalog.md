# Module Catalog

Modules are reusable contracts that agents can compose into campaigns.

## Campaign Modules

- `cryoem-raw-to-atomic-no-download`: local/prep smoke campaign.
- `cryoem-raw-subset-open-empiar-13124`: operator-gated raw subset route using
  open/default tools.
- `cryoem-raw-subset-gated-empiar-13124`: operator-gated raw subset route with
  license-gated lanes.
- `map-model-dossier-emdb-43816-pdb-9asj`: deposited public map/model dossier.

## Data Modules

- `empiar-10204.metadata-only`: metadata-only public accession fixture.
- `empiar-13124.raw-subset`: raw-data contract with downloads disabled by
  default and operator-gated at runtime.
- `emdb-43816-pdb-9asj.map-model`: deposited public map/model artifact plan.

## Lane Modules

Lane modules describe raw-to-map, map-to-model, figure dossier, toolcheck, and
license-gated runtime posture. They are contracts. Install or redistribution
permission for third-party tools rests with the operator and the upstream
license.

## Provider Profiles

Provider profiles cover local, RunPod, AWS Batch, SSH/HPC, generic cloud VM,
and neocloud-style backends. Non-local provider profiles require operator gates
before any paid or mutating execution.

Validate modules with:

```bash
make module-check
make provider-check
```

## Related

- [Schema Catalog](schema-catalog.md): the JSON Schema contracts these modules instantiate.
- [Validation Command Matrix](validation-command-matrix.md): full validator list with side-effect and network notes.
- [Provider Execution Model](provider-execution-model.md): how provider profiles inform execution and closeout.
- [Recipes](recipes/README.md): runnable workflows that use these modules.

