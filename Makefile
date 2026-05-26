REQUIRE_GITLEAKS ?= 0

.PHONY: help doctor preflight registry-check tooling-freshness-check docs-link-check module-check skill-check goal-brief-check public-metadata-check public-snapshot-check public-audit public-release-report schema-check runpod-check runpod-scope-check runpod-reference-check bridge-manifest-check issue-check stage-contract-check launch-preflight launch-preflight-prep launch-preflight-real launch-bundle toolcheck license-gate-check fanout-estimate input-audit contract-self-check provider-check provider-local provider-closeout-check figure-manifest-check readonly-check ci test release-check secret-scan clean list demo-local demo-t2r14-local demo-t2r14-check demo-poltheta-prep-check demo-structure-jury-prep-check

help:
	@printf '%s\n' \
		'CryoCore release gates:' \
		'  make release-check            full public release gate, including secret scan when available' \
		'  make readonly-check           validators without network/provider mutation' \
		'  make doctor                   public readiness report' \
		'' \
		'Public repo hygiene:' \
		'  make public-release-report    read-only publishability report' \
		'  make public-snapshot-check    block secrets, private markers, and heavy scientific artifacts' \
		'  make docs-link-check          validate local Markdown links and images' \
		'  make tooling-freshness-check  verify license/tool posture review freshness' \
		'  make skill-check              validate public skill-pack metadata' \
		'  make goal-brief-check         validate the reusable /goal brief template' \
		'' \
			'Contracts and providers:' \
			'  make runpod-check             validate RunPod manifests, stage contracts, and references' \
			'  make runpod-scope-check       validate public bridge-manifest scope' \
			'  make bridge-manifest-check    fail if generated bridge manifests are stale' \
			'  make launch-preflight-prep    prep-mode launch checks; expected green for public scaffolds' \
			'  make launch-preflight-real    execution-ready launch checks; expected to fail until operator gates are supplied' \
			'  make provider-closeout-check  validate fetched artifact closeout fixtures' \
			'  make provider-local           run local no-download provider lane into .runtime' \
		'' \
		'Examples:' \
		'  make demo-local               run the tiny public-coordinate T2R14 demo locally' \
		'  make public-metadata-check    metadata-only accession smoke check' \
		'  make toolcheck                local no-download toolcheck fixture' \
		'  make clean                    remove local caches and ignored runtime output'

preflight:
	python3 scripts/cryocore/preflight.py --repo-root . --json

registry-check:
	python3 scripts/cryocore/software_registry_check.py references/software-registry.yaml --json

tooling-freshness-check:
	python3 scripts/cryocore/tooling_freshness_check.py --repo-root . --json

docs-link-check:
	python3 scripts/cryocore/docs_link_check.py --repo-root . --json

module-check:
	for manifest in modules/campaigns/*.json; do \
		python3 scripts/cryocore/module_manifest_check.py "$$manifest" --check-all --json || exit 1; \
	done

skill-check:
	python3 scripts/cryocore/skill_pack_check.py --index skills/index.yaml --json

goal-brief-check:
	python3 scripts/cryocore/goal_brief_check.py templates/goal-brief.md --allow-template --json

public-metadata-check:
	python3 -m json.tool examples/public-accession-metadata/metadata.json >/dev/null
	python3 scripts/cryocore/fetch_public_accession_metadata.py --empiar 10204 --emdb EMD-43816 --pdb 9ASJ >/dev/null

public-snapshot-check:
	python3 scripts/cryocore/public_snapshot_check.py --repo-root . --profile public --json

public-audit: public-snapshot-check

public-release-report:
	python3 scripts/cryocore/public_release_report.py --repo-root . --json

doctor: public-release-report

schema-check:
	python3 scripts/cryocore/schema_check.py --schema modules/schemas/public-accession-metadata.v1.schema.json --instance examples/public-accession-metadata/metadata.json --json
	python3 scripts/cryocore/schema_check.py --schema modules/schemas/provider-run.v1.schema.json --instance tests/fixtures/provider-closeout/good/provider-run.json --json
	python3 scripts/cryocore/schema_check.py --schema modules/schemas/artifact-pull-report.v1.schema.json --instance tests/fixtures/provider-closeout/good/artifacts/validation/artifact-pull-report.json --json
	python3 scripts/cryocore/schema_check.py --schema modules/schemas/cost-report.v1.schema.json --instance tests/fixtures/provider-closeout/good/artifacts/cost_report.json --json
	python3 scripts/cryocore/schema_check.py --schema modules/schemas/cleanup-proof.v1.schema.json --instance tests/fixtures/provider-closeout/good/artifacts/cleanup_proof.json --json
	python3 scripts/cryocore/schema_check.py --schema modules/schemas/claim-ledger.v1.schema.json --instance tests/fixtures/provider-closeout/good/artifacts/claim_ledger.json --json
	python3 scripts/cryocore/schema_check.py --schema modules/schemas/figure-manifest.v1.schema.json --instance tests/fixtures/figure-dossier/figure_manifest.json --json
	python3 scripts/cryocore/schema_check.py --schema modules/schemas/map-model-fit.v1.schema.json --instance tests/fixtures/map-model-fit/valid.json --json
	python3 scripts/cryocore/schema_check.py --schema modules/schemas/workflow-run.v1.schema.json --instance tests/fixtures/workflow-provenance/workflow-run.json --json
	python3 scripts/cryocore/schema_check.py --schema modules/schemas/container-provenance.v1.schema.json --instance tests/fixtures/workflow-provenance/container-provenance.json --json

runpod-check:
	for manifest in runpod/launch-manifests/*.json; do \
		python3 scripts/cryocore/runpod_manifest_check.py "$$manifest" --json || exit 1; \
	done
	for contract in runpod/stage-contracts/*.json; do \
		python3 scripts/cryocore/stage_contract_check.py --stage-contract "$$contract" --json || exit 1; \
	done
	python3 scripts/cryocore/runpod_reference_check.py --repo-root . --json
	python3 scripts/cryocore/bridge_manifest_check.py --repo-root . --json

runpod-scope-check:
	python3 scripts/cryocore/runpod_scope_check.py runpod/bridge-manifests --json

runpod-reference-check:
	python3 scripts/cryocore/runpod_reference_check.py --repo-root . --json

bridge-manifest-check:
	python3 scripts/cryocore/bridge_manifest_check.py --repo-root . --json

issue-check:
	python3 scripts/cryocore/issue_check.py campaigns/cryoem-raw-to-atomic-dossier/linear-issues --check-file-references --json

stage-contract-check:
	for contract in runpod/stage-contracts/*.json; do \
		python3 scripts/cryocore/stage_contract_check.py --stage-contract "$$contract" --json || exit 1; \
	done

launch-preflight: launch-preflight-prep

launch-preflight-prep:
	python3 scripts/cryocore/runpod_launch_preflight.py --manifest runpod/launch-manifests/no-download-smoke.json --json

launch-preflight-real:
	python3 scripts/cryocore/runpod_launch_preflight.py --manifest runpod/launch-manifests/no-download-smoke.json --execution-ready --json

launch-bundle:
	python3 scripts/cryocore/runpod_launch_bundle.py --manifest runpod/launch-manifests/no-download-smoke.json --out .runtime/cryocore-no-download-smoke/launch-bundle.json

toolcheck:
	python3 scripts/cryocore/toolcheck_runner.py --manifest runpod/launch-manifests/no-download-smoke.json --out .runtime/cryocore-toolcheck --mock-gpu

license-gate-check:
	python3 scripts/cryocore/license_gate_check.py --manifest runpod/launch-manifests/no-download-smoke.json --json

fanout-estimate:
	python3 scripts/cryocore/fanout_estimator.py --manifest runpod/launch-manifests/raw-subset-open.json --json

input-audit:
	python3 scripts/cryocore/input_audit.py --manifest runpod/launch-manifests/no-download-smoke.json --out .runtime/cryocore-toolcheck/validation/input-audit.json --json

contract-self-check: toolcheck input-audit
	python3 scripts/cryocore/contract_self_check.py --manifest runpod/launch-manifests/no-download-smoke.json --artifact-root .runtime/cryocore-toolcheck --execution-mode prep --json

provider-check:
	python3 scripts/cryocore/provider_profile_check.py modules/provider-profiles --json

provider-local:
	python3 scripts/cryocore/provider_runner.py --manifest runpod/launch-manifests/no-download-smoke.json --out .runtime/provider-local --execution-mode prep --json

provider-closeout-check:
	python3 scripts/cryocore/provider_closeout_check.py --provider-run tests/fixtures/provider-closeout/good/provider-run.json --artifact-root tests/fixtures/provider-closeout/good/artifacts --execution-mode real --json
	! python3 scripts/cryocore/provider_closeout_check.py --provider-run tests/fixtures/provider-closeout/bad-intent/provider-run.json --artifact-root tests/fixtures/provider-closeout/bad-intent/artifacts --execution-mode real --json

figure-manifest-check:
	python3 scripts/cryocore/figure_manifest_check.py --manifest tests/fixtures/figure-dossier/figure_manifest.json --artifact-root tests/fixtures/figure-dossier --json

readonly-check: preflight registry-check tooling-freshness-check docs-link-check module-check skill-check goal-brief-check public-snapshot-check schema-check runpod-check runpod-scope-check provider-check issue-check provider-closeout-check figure-manifest-check

ci: readonly-check
	python3 -m py_compile scripts/cryocore/*.py
	PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider

release-check: ci public-release-report secret-scan

secret-scan:
	@if command -v gitleaks >/dev/null 2>&1; then \
		gitleaks detect --source . --no-banner --redact --verbose; \
		gitleaks dir . --no-banner --redact --verbose; \
	elif [ "$(REQUIRE_GITLEAKS)" = "1" ]; then \
		echo "gitleaks is required for this release gate but is not installed."; \
		exit 1; \
	else \
		echo "gitleaks not installed; skipping optional secret scan."; \
	fi

test: preflight registry-check module-check goal-brief-check public-metadata-check runpod-check issue-check schema-check provider-closeout-check figure-manifest-check
	python3 -m py_compile scripts/cryocore/*.py
	python3 -m pytest -q

demo-local: demo-t2r14-local

demo-t2r14-local:
	python3 scripts/cryocore/t2r14_open_dossier.py --out .runtime/t2r14-open-dossier --json
	python3 -m json.tool .runtime/t2r14-open-dossier/status.json >/dev/null
	@printf '%s\n' 'Open .runtime/t2r14-open-dossier/artifacts/report.html'

# The three demo-*-check targets below build a bridge manifest and then validate
# it with the external runpod-bridge CLI. The CLI is operator-owned and lives
# outside this public repo. Install or stub it before running these targets.
# Newcomers should start with `make demo-local`, which is self-contained.

demo-t2r14-check:
	python3 scripts/cryocore/build_t2r14_bridge_manifest.py
	@command -v runpod-bridge >/dev/null 2>&1 || { echo 'runpod-bridge CLI not found; this target needs the operator-owned bridge CLI installed (see docs/runpod-stack.md). Newcomers can use make demo-local instead.'; exit 1; }
	runpod-bridge validate-manifest runpod/bridge-manifests/t2r14-open-dossier.json --json

demo-poltheta-prep-check:
	python3 scripts/cryocore/build_poltheta_bridge_manifest.py
	@command -v runpod-bridge >/dev/null 2>&1 || { echo 'runpod-bridge CLI not found; this target needs the operator-owned bridge CLI installed (see docs/runpod-stack.md). Newcomers can use make demo-local instead.'; exit 1; }
	runpod-bridge validate-manifest runpod/bridge-manifests/poltheta-map-model-dossier.json --json

demo-structure-jury-prep-check:
	python3 scripts/cryocore/build_structure_jury_bridge_manifest.py
	@command -v runpod-bridge >/dev/null 2>&1 || { echo 'runpod-bridge CLI not found; this target needs the operator-owned bridge CLI installed (see docs/runpod-stack.md). Newcomers can use make demo-local instead.'; exit 1; }
	runpod-bridge validate-manifest runpod/bridge-manifests/structure-jury-dual-dossier.json --json

list:
	find campaigns containers demos docs examples modules references runpod scripts skills templates tests -maxdepth 4 -type f | sort

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	rm -rf .runtime htmlcov .coverage
