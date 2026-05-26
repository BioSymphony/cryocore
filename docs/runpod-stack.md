# CryoCore RunPod Stack

CryoCore treats RunPod as an execution plane. Durable plans, manifests, stage contracts, and issue contracts live in git so they stay inspectable. Heavy runtime state lives on persistent volumes or ignored runtime directories.

## Image Families

```text
biosymphony-cryocore-core
biosymphony-cryocore-model-build
biosymphony-cryocore-cryosparc
```

## Execution Profiles

```text
no-download-smoke   zero biological downloads; validates repo, GPU, storage, toolcheck, and artifact shape
raw-subset-open     scaffold for a bounded public EMPIAR raw-movie subset with open/default tools only
raw-subset-gated    scaffold for a bounded raw subset with explicitly authorized gated tools
map-model-dossier   public EMDB/PDB map/model evidence dossier without raw movies
```

All non-smoke profiles require stage contracts, progress ledgers, input audits, and contract self-checks.

The public raw-subset entrypoint is scaffold-only: it records the declared
subset, fanout, and gates. Raw movies materialize when an operator-owned
downloader supplies explicit raw-download and authorization environment
outside git. Real raw-subset success requires downloaded files,
hashes, input audit, real-mode contract self-check, cost report, and cleanup
proof.

## Launch Gates

Use RunPod Pods for the first remote executions. A smoke pod should clone a pinned repo ref, run local Python checks, record GPU visibility, write artifacts to `/workspace/cryocore/runs/<run-id>/`, and exit without large biological downloads.

Do not interpret `desiredStatus: RUNNING` as execution progress. Closeout needs provider actual status, runtime uptime, image pull success or failure, and `stage-progress.jsonl` events.

For externally dispatched runs, sandboxed workers prepare a launch request after local validation. Operator-owned host-side hooks create pods, verify workload artifacts, fetch and hash outputs, delete pods, confirm cleanup, and only then close the tracker item as successful.

## Storage Policy

- Use a dedicated CryoCore RunPod Network Volume for writable state.
- Public docs/templates should use `CRYOCORE_RUNPOD_NETWORK_VOLUME_ID`.
- Do not reuse sibling campaign volumes for writable state.
- Use container disk only for temporary scratch.
- Emit run manifests with software versions, GPU type, image digest, volume paths, and artifact hashes.

## Tool Setup

Valid setup postures are public/prebuilt image, private image with runtime registry auth, runtime install to scratch, or Network Volume bootstrap.

Network Volume bootstrap is the default alternative when GHCR auth is unnecessary friction or when a tool such as ChimeraX should not be redistributed through a public image. Bootstrap scripts must be idempotent, version-pinned, and followed by verifiers that record exact versions and hashes.

## Secrets And Licenses

Use runtime environment variables or RunPod secrets for registry auth, ChimeraX runtime access, CryoSPARC, Phenix, or model-build gates. Never commit secret values, license files, raw maps, raw movies, or tracker credentials to this repo.

## Related

- [Provider Execution Model](provider-execution-model.md): the launch-is-intent rules that apply to RunPod execution.
- [Provider Readiness](provider-readiness.md): operator-gated steps before any real RunPod launch.
- [Compute Backends](compute-backends.md): RunPod's place among the supported execution planes.
- [Demos: T2R14 Open Dossier](../demos/t2r14-open-dossier/README.md): a small public RunPod demo with bridge manifest.
- [No-False-Success Hardening](no-false-success-hardening.md): closeout artifacts a real RunPod run must produce.
