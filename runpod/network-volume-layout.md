# Network Volume Layout

Mount persistent RunPod storage at `/workspace`.

```text
/workspace/cryocore/
  cache/
    apt/
    conda/
    pip/
    tool-downloads/
  datasets/
    empiar/
    emdb/
    pdb/
  models/
    predicted/
    refined/
    validation/
  runs/
    <run-id>/
      launch-manifest.json
      run-manifest.json
      validation/
      provenance.md
  scratch/
  software/
    chimerax/
    coot/
    relion/
    warp/
    modelangelo/
    miniconda3/
    envs/
      cryodrgn/
      recovar/
    manifests/
  weights/
    gated/
    public/
    modelangelo/
    cryodrgn/
```

On a dedicated CryoCore-only Network Volume, tool bootstrap may also use this shorter root:

```text
/workspace/software/
  chimerax/
  coot/
  relion/
  warp/
  modelangelo/
  miniconda3/
    envs/
      cryodrgn/
      recovar/
  manifests/
  weights/
```

## Policy

- Use a CryoCore-owned Network Volume for writable CryoCore state. Public docs/templates should reference `CRYOCORE_RUNPOD_NETWORK_VOLUME_ID`; operator-gated concrete bridge manifests may carry the resolved owned volume ID.
- Do not reuse sibling campaign volumes for writable state. In particular, never point CryoCore manifests at `GENECLUSTER_*` volume variables.
- `runs/<run-id>/` is the only required write target for smoke runs.
- `datasets/`, `models/`, and `weights/` are external heavy-data areas and must not be copied back into git.
- `software/` is for derivable runtime installs from committed bootstrap scripts. It must not contain secrets, license files, private installers, or unpublished biological data.
- Container-local paths outside `/workspace` are scratch and may disappear when the Pod is terminated.

## Bootstrap Pattern

Use this when avoiding private GHCR images:

1. Launch a small CryoCore setup pod from a public base image.
2. Install pinned tools into `/workspace/cryocore/software/`, or `/workspace/software/` when the whole volume is CryoCore-only.
3. Cache allowed public weights under `/workspace/cryocore/weights/public/`, `/workspace/software/weights/`, or tool-specific subfolders.
4. Write `software/manifests/<tool>.json` or `software/manifest.json` with tool version, source URL, install command, hash when available, license posture, and verification command.
5. Every later pod runs a verifier before scientific work. Missing or drifted tools fail before data download or paid analysis.

The Network Volume is mutable shared state. Treat it as a cache derived from tracked scripts and manifests, not as the source of truth.

Bootstrap scripts must also:

- verify git refs and download URLs before expensive package installs
- record requested refs, resolved commits, source URLs, and archive/hash checks in the manifest
- emit heartbeat/progress output during long installs
- enforce max runtime/spend from the operator gate
- mark optional or license-sensitive tools as `deferred` unless runtime access is explicit

For cryo/model-build runtime stacks, `scripts/runpod/bootstrap_cryocore_nv.sh`
should install only CryoCore-declared tools from `references/software-registry.yaml`.
Prediction/design environments such as RFdiffusion, Boltz, Chai, Genie, and MPNN
belong in Structure Factory unless a CryoCore issue explicitly consumes their
finished outputs as comparison evidence.

Avoid using a Network Volume as a many-small-file build filesystem when a tarball, cache, or digest-pinned image would be faster. If a tool must be built or installed there, write the expected slowdown into the issue budget and close partial rather than silently burning paid runtime.
