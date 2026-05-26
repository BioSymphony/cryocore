# Cloud Provider Prep Prompt

Use this prompt when an agent should prepare a cloud or HPC run contract without
launching paid compute or touching credentials.

```text
Use the CryoCore skill pack. Prepare a provider workflow plan for
<RunPod/AWS Batch/SSH-HPC/local/generic cloud>. Stay in prep mode. Include the
provider profile, execution profile, launch-request shape, expected artifact
root, validation commands, budget gate, cleanup gate, and closeout proof. Do not
launch providers, create paid resources, download raw data, install gated tools,
expose credentials, or write provider logs to git.

Read docs/workflows.md, docs/compute-backends.md,
docs/provider-execution-model.md, docs/no-false-success-hardening.md,
runpod/README.md if RunPod is involved, and the relevant provider profile under
modules/provider-profiles/.

Return:
- selected provider and execution profile
- declared input boundary and data tier
- expected stage contract and artifact root
- required operator gate, budget, storage, image, license, and cleanup decisions
- local validation commands to run before launch request prep
- exact blockers and residual risks
```
