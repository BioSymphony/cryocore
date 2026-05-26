# Provider Readiness

Use this page before asking an agent or operator to touch cloud or HPC
resources. CryoCore separates public prep from real execution and final
closeout.

## Readiness Levels

| Level | Meaning | Allowed from public repo |
| --- | --- | --- |
| prep-ready | Manifests, stage contracts, provider profiles, and issue text validate. | yes |
| execution-ready | Operator has approved spend, credentials, image/ref pinning, storage, and cleanup. | no, operator-owned |
| closeout-ready | Artifacts were fetched, hashed, costed, cleaned up, and validated. | review only |

## Provider Matrix

| Provider | Public status | Required external state | Artifact root | Local checks | Closeout proof |
| --- | --- | --- | --- | --- | --- |
| Local workstation | execution-ready for validators and tiny demos | Python environment | `.runtime/` | `make demo-local`, `make release-check` | local reports and manifests |
| RunPod | prep-ready; real launch operator-gated | credentials, budget, network volume, image digest or audited bootstrap, launch authorization | `/workspace/cryocore/runs/<run-id>/` | `make runpod-check`, `make runpod-scope-check`, `make launch-preflight-prep` | artifact pull report, hashes, cost report, cleanup proof |
| AWS Batch | contract-only | Batch queue, job definition, IAM, artifact bucket, budget | `s3://CRYOCORE_AWS_ARTIFACT_BUCKET/runs/<run-id>` | `make provider-check` | artifact sync, hashes, cost, cleanup or retained-resource approval |
| AWS EC2 or cloud VM | contract-only | instance profile, subnet/security group, artifact bucket, budget | provider storage or synced artifact directory | `make provider-check` | fetched artifacts, hashes, cost, termination or retained-resource approval |
| SSH/HPC | contract-only | site scheduler, shared storage, transfer path, local license rules | `$CRYOCORE_HPC_WORKSPACE/runs/<run-id>` | `make provider-check` | fetched artifacts, hashes, scheduler/runtime evidence |
| Neocloud GPU pod | contract-only | provider-specific pod auth, storage, budget, cleanup | provider artifact volume | `make provider-check` | fetched artifacts, hashes, cost, cleanup proof |

## Operator Handoff

1. Validate public prep locally.
2. Fill an operator gate record outside public issue bodies.
3. Generate a prep launch request under `.runtime/`.
4. Run `make launch-preflight-real` only in an operator-controlled environment.
5. Launch through operator-owned tooling that lives outside the public worker shell.
6. Fetch and hash declared artifacts.
7. Record cost and cleanup proof.
8. Run closeout against fetched artifacts.

Provider status, job IDs, pod IDs, queue state, and command exit are intent
signals. The claim level rises when fetched artifacts, hashes, validation
outputs, cost records, and cleanup proof join the declared inputs.

## Related

- [Provider Execution Model](provider-execution-model.md): the launch-is-intent model these readiness levels sit on top of.
- [Compute Backends](compute-backends.md): mapping from CryoCore workloads to provider shapes.
- [RunPod Stack](runpod-stack.md): the RunPod-specific bridge, manifests, and entrypoints.
- [No-False-Success Hardening](no-false-success-hardening.md): the closeout discipline behind the readiness ladder.
- [Operator Gate Record template](../templates/operator-gate-record.md): the operator-gate shape this hand-off step uses.
