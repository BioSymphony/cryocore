# RunPod Contracts

RunPod files in this public repo are contracts and prep scaffolds.

They are not authorization to launch paid resources.

Contents:

- `launch-manifests/`: provider-profile launch contracts.
- `stage-contracts/`: required stage-progress contracts.
- `bridge-manifests/`: prep-only bridge packets with `remote_launch_allowed`
  disabled.
- `entrypoints/`: public-safe runtime entrypoint scripts.
- `templates/`: placeholder image/template posture records.

Public bridge manifests are intentionally prep-only. `runpod_scope_check.py`
also verifies that inline source bundles decode safely, public artifact servers
serve only `runpod-execution/artifacts`, and unauthenticated workspace serving is
not allowed.

`bootstrap-gated-tools.sh` is a fail-closed public stub. Real gated-tool
bootstrap belongs in an operator-owned workflow after license, credential,
budget, and use-context review.

Before any real launch, an operator-owned workflow must provide current
credentials, budget approval, digest-pinned image or audited bootstrap route,
artifact fetch/hash, cost report, and cleanup proof outside the public release
gate.

## Remote Run Handoff

Public workers stop at prep artifacts. A real RunPod launch follows this shape:

1. Validate public scaffolds:

   ```bash
   make runpod-check
   make runpod-scope-check
   make launch-preflight-prep
   ```

2. Fill an operator gate record outside public issue bodies and redact concrete
   provider IDs from public copies.
3. Generate a prep-mode launch request in ignored runtime storage:

   ```bash
   python3 scripts/cryocore/runpod_launch_request.py \
     --manifest runpod/launch-manifests/no-download-smoke.json \
     --issue CRYOCORE-EXAMPLE \
     --max-spend-usd 1 \
     --execution-mode prep \
     --out .runtime/launch-request.json \
     --json
   ```

4. Operator-owned tooling creates the pod only after real preflight passes with
   a digest-pinned image or audited bootstrap, a 40-character public commit SHA,
   runtime credentials outside git, and explicit launch authorization.
5. Operator-owned tooling fetches artifacts, computes hashes, records cost,
   deletes or documents retained resources, and writes cleanup proof.
6. Closeout runs against fetched artifacts. `RUNNING`, `COMPLETED`, pod IDs, or
   command exit alone are not success.

## Provider Readiness Matrix

| Provider | Public status | Required external state | Artifact root | Closeout proof |
| --- | --- | --- | --- | --- |
| Local | execution-ready for validators and tiny demos | Python environment only | `.runtime/` | local validator output |
| RunPod | prep-ready, execution operator-gated | credentials, budget, volume, image digest/bootstrap, launch authorization | `/workspace/cryocore/runs/<run-id>/` | artifact pull report, hashes, cost, cleanup |
| AWS Batch | contract-only | Batch queue, job definition, S3 artifact bucket, IAM, budget | `s3://CRYOCORE_AWS_ARTIFACT_BUCKET/runs/<run-id>` | artifact sync, hashes, cost, cleanup or retained-resource approval |
| SSH/HPC | contract-only | site scheduler, storage, licenses, transfer path | `$CRYOCORE_HPC_WORKSPACE/runs/<run-id>` | fetched artifacts, hashes, scheduler/runtime evidence |
