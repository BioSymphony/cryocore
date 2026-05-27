import base64
import gzip
import io
import json
import shutil
import subprocess
import tarfile
from datetime import date
from pathlib import Path

import pytest

from scripts.cryocore.contract_self_check import self_check
from scripts.cryocore.bridge_manifest_check import check_manifests
from scripts.cryocore.docs_link_check import run_check as docs_link_check
from scripts.cryocore.figure_manifest_check import check_manifest
from scripts.cryocore.goal_brief_check import validate_goal_brief
from scripts.cryocore.public_release_report import run_report as public_release_report
from scripts.cryocore.public_snapshot_check import run_check
from scripts.cryocore.runpod_reference_check import run_check as runpod_reference_check
from scripts.cryocore.runpod_launch_preflight import runtime_ref_ready
from scripts.cryocore.runpod_scope_check import validate_bridge
from scripts.cryocore.schema_check import validate
from scripts.cryocore.source_bundle import encoded_source_bundle, validate_bundle_name
from scripts.cryocore.tooling_freshness_check import run_check as tooling_freshness_check


ROOT = Path(__file__).resolve().parents[1]


def test_public_snapshot_check_blocks_secret_like_content(tmp_path: Path) -> None:
    secret_file = tmp_path / "notes.md"
    secret_key = "RUNPOD" + "_API_KEY"
    secret_file.write_text(f"{secret_key}=not-a-real-key\n")
    summary = run_check(tmp_path, "workshop", 2_000_000)
    assert summary["ok"] is False
    assert any("secret-like content" in error for error in summary["errors"])


def test_public_snapshot_check_blocks_public_private_marker(tmp_path: Path) -> None:
    local_file = tmp_path / "notes.md"
    local_path = "/Users/" + "jacobvogan/" + "autonomy" + "/bin/runpod-bridge"
    local_file.write_text(f"Use {local_path} here.\n")
    summary = run_check(tmp_path, "public", 2_000_000)
    assert summary["ok"] is False
    assert any("private/workshop markers" in error for error in summary["errors"])


def test_public_snapshot_check_blocks_forced_heavy_artifact(tmp_path: Path) -> None:
    heavy_file = tmp_path / "forced-added.star"
    heavy_file.write_text("data_particles\n")
    summary = run_check(tmp_path, "workshop", 2_000_000)
    assert summary["ok"] is False
    assert any("denied heavy/private artifact extension .star" in error for error in summary["errors"])


def test_runpod_scope_blocks_public_workspace_http_server() -> None:
    data = {
        "manifest_kind": "symphony_runpod_launch",
        "provider": {"name": "runpod", "adapter": "runpod_pod_v1"},
        "repo": {"source": "inline_commands", "url_or_path": "inline", "commit_or_snapshot": "inline:test"},
        "worker_coordination": {
            "resource_name_prefix": "cryocore-test",
            "single_mutating_worker": True,
            "read_only_monitors_allowed": True,
        },
        "runpod": {"name": "cryocore-test", "env": {}, "networkVolumeId": ""},
        "access": {"public_services_require_auth": False},
        "startup": {"commands": ["python3 -m http.server 8000 --bind 0.0.0.0"]},
        "closeout": {"stop_or_delete_pod": True, "retain_pod": False},
    }
    summary = validate_bridge(data, Path("fixture.json"))
    assert summary["ok"] is False
    assert any("public_services_require_auth=true" in error for error in summary["errors"])
    assert any("serve runpod-execution/artifacts" in error for error in summary["errors"])


def test_runpod_reference_check_current_repo_passes() -> None:
    summary = runpod_reference_check(ROOT)
    assert summary["ok"] is True, summary["errors"]
    assert summary["checked"] > 0


def test_tooling_freshness_check_current_docs_pass() -> None:
    summary = tooling_freshness_check(ROOT, 120, today=date(2026, 5, 27))
    assert summary["ok"] is True, summary["errors"]


def test_docs_link_check_current_docs_pass() -> None:
    summary = docs_link_check(ROOT, ["README.md", "FAQ.md", "ROADMAP.md", "docs", "examples", "skills", "templates", "demos"])
    assert summary["ok"] is True, summary["errors"]


def test_goal_brief_template_passes_as_template() -> None:
    summary = validate_goal_brief(ROOT / "templates/goal-brief.md", allow_placeholders=True)
    assert summary["ok"] is True, summary["errors"]


def test_goal_brief_requires_selected_resource_mode(tmp_path: Path) -> None:
    brief = tmp_path / "goal.md"
    brief.write_text((ROOT / "templates/goal-brief.md").read_text().replace("<one sentence>", "Build dossier"))
    summary = validate_goal_brief(brief)
    assert summary["ok"] is False
    assert any("select at least one Resource Mode" in error for error in summary["errors"])


def test_goal_brief_accepts_filled_minimal_copy(tmp_path: Path) -> None:
    brief = tmp_path / "goal.md"
    text = (ROOT / "templates/goal-brief.md").read_text()
    text = text.replace("- [ ] `local_only`", "- [x] `local_only`")
    text = text.replace("<one sentence>", "Build a local no-download dossier")
    text = text.replace("<what should exist when this is done>", ".runtime dossier and validation output")
    text = text.replace("<question>", "none")
    brief.write_text(text)
    summary = validate_goal_brief(brief)
    assert summary["ok"] is True, summary["errors"]
    assert summary["selected_resource_modes"] == ["local_only"]


def test_public_release_report_unborn_git_not_history_ready(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-b", "main"], cwd=tmp_path, text=True, capture_output=True, check=True)

    summary = public_release_report(tmp_path, 2_000_000)

    assert summary["git"]["has_commits"] is False
    assert summary["git"]["current_branch"] == "main"
    assert summary["git"]["working_tree_clean"] is True
    assert summary["git"]["fresh_history_ready"] is False
    assert "no initial public commit yet" in summary["public_switch"]["blockers"]


def test_runtime_ref_ready_requires_auth_id_or_username_token(monkeypatch) -> None:
    refs = ["RUNPOD_GHCR_REGISTRY_AUTH_ID", "RUNPOD_GHCR_USERNAME", "RUNPOD_GHCR_TOKEN"]
    for ref in refs:
        monkeypatch.delenv(ref, raising=False)
    assert runtime_ref_ready(refs) == (False, [], "missing_auth_id_or_username_token_pair")

    monkeypatch.setenv("RUNPOD_GHCR_USERNAME", "user")
    assert runtime_ref_ready(refs)[0] is False

    monkeypatch.setenv("RUNPOD_GHCR_TOKEN", "token")
    ready, present, mode = runtime_ref_ready(refs)
    assert ready is True
    assert set(present) == {"RUNPOD_GHCR_USERNAME", "RUNPOD_GHCR_TOKEN"}
    assert mode == "username_token_pair"

    monkeypatch.delenv("RUNPOD_GHCR_USERNAME")
    monkeypatch.delenv("RUNPOD_GHCR_TOKEN")
    monkeypatch.setenv("RUNPOD_GHCR_REGISTRY_AUTH_ID", "auth-id")
    assert runtime_ref_ready(refs) == (True, ["RUNPOD_GHCR_REGISTRY_AUTH_ID"], "registry_auth_id")


def test_source_bundle_is_deterministic_and_metadata_pinned() -> None:
    left = encoded_source_bundle({"b/runner.py": "print('b')\n", "a.txt": "alpha\n"})
    right = encoded_source_bundle({"a.txt": "alpha\n", "b/runner.py": "print('b')\n"})
    assert left == right

    with gzip.GzipFile(fileobj=io.BytesIO(base64.b64decode(left)), mode="rb") as gzip_file:
        with tarfile.open(fileobj=gzip_file, mode="r:") as archive:
            members = archive.getmembers()
            assert [member.name for member in members] == ["a.txt", "b/runner.py"]
            for member in members:
                assert member.isfile()
                assert member.mode == 0o644
                assert member.mtime == 0
                assert member.uid == 0
                assert member.gid == 0
                assert member.uname == ""
                assert member.gname == ""

    with pytest.raises(ValueError):
        validate_bundle_name("../escape.py")


def test_bridge_manifest_builders_are_deterministic(tmp_path: Path) -> None:
    builders = [
        "build_t2r14_bridge_manifest.py",
        "build_poltheta_bridge_manifest.py",
        "build_structure_jury_bridge_manifest.py",
    ]
    for builder in builders:
        first = tmp_path / f"{builder}.first.json"
        second = tmp_path / f"{builder}.second.json"
        for out in [first, second]:
            result = subprocess.run(
                ["python3", f"scripts/cryocore/{builder}", "--out", str(out)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            assert result.returncode == 0, result.stdout + result.stderr
        assert first.read_text() == second.read_text()


def test_bridge_manifest_check_current_repo_passes() -> None:
    summary = check_manifests(ROOT)
    assert summary["ok"] is True, summary["errors"]


def test_schema_check_rejects_missing_required_key() -> None:
    schema = json.loads((ROOT / "modules/schemas/claim-ledger.v1.schema.json").read_text())
    errors = validate(schema, {"schema_version": 1})
    assert any("missing required key claims" in error for error in errors)


def test_schema_check_enforces_any_of_claim_name_or_claim() -> None:
    schema = json.loads((ROOT / "modules/schemas/claim-ledger.v1.schema.json").read_text())
    errors = validate(
        schema,
        {
            "schema_version": 1,
            "claims": [{"claim_level": "processed", "evidence_artifact": "validation/input-audit.json"}],
        },
    )
    assert any("anyOf" in error for error in errors)


def test_figure_manifest_fixture_passes() -> None:
    summary = check_manifest(
        ROOT / "tests/fixtures/figure-dossier/figure_manifest.json",
        ROOT / "tests/fixtures/figure-dossier",
    )
    assert summary["ok"] is True


def test_provider_closeout_fixture_passes() -> None:
    result = subprocess.run(
        [
            "python3",
            "scripts/cryocore/provider_closeout_check.py",
            "--provider-run",
            "tests/fixtures/provider-closeout/good/provider-run.json",
            "--artifact-root",
            "tests/fixtures/provider-closeout/good/artifacts",
            "--execution-mode",
            "real",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    summary = json.loads(result.stdout)
    assert summary["hash_evidence"]["hash_ledger_present"] is True
    assert summary["hash_evidence"]["mismatched_hashes"] == []
    assert summary["stage_contract_report"]["terminal_stage_count"] == 1


def test_provider_closeout_rejects_intent_only_run() -> None:
    result = subprocess.run(
        [
            "python3",
            "scripts/cryocore/provider_closeout_check.py",
            "--provider-run",
            "tests/fixtures/provider-closeout/bad-intent/provider-run.json",
            "--artifact-root",
            "tests/fixtures/provider-closeout/bad-intent/artifacts",
            "--execution-mode",
            "real",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    summary = json.loads(result.stdout)
    assert any("intent-only" in error or "desired_status" in error for error in summary["errors"])


def test_provider_closeout_rejects_mismatched_hash_ledger(tmp_path: Path) -> None:
    fixture_root = tmp_path / "provider-closeout"
    shutil.copytree(ROOT / "tests/fixtures/provider-closeout/good", fixture_root)
    ledger_path = fixture_root / "artifacts/artifact_hashes.json"
    ledger = json.loads(ledger_path.read_text())
    ledger["sha256"]["stage-progress.jsonl"] = "0" * 64
    ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    result = subprocess.run(
        [
            "python3",
            "scripts/cryocore/provider_closeout_check.py",
            "--provider-run",
            str(fixture_root / "provider-run.json"),
            "--artifact-root",
            str(fixture_root / "artifacts"),
            "--execution-mode",
            "real",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    summary = json.loads(result.stdout)
    assert "stage-progress.jsonl" in summary["hash_evidence"]["mismatched_hashes"]


def test_provider_closeout_rejects_missing_stage_contract_report(tmp_path: Path) -> None:
    fixture_root = tmp_path / "provider-closeout"
    shutil.copytree(ROOT / "tests/fixtures/provider-closeout/good", fixture_root)
    (fixture_root / "artifacts/validation/stage-contract-check.json").unlink()

    result = subprocess.run(
        [
            "python3",
            "scripts/cryocore/provider_closeout_check.py",
            "--provider-run",
            str(fixture_root / "provider-run.json"),
            "--artifact-root",
            str(fixture_root / "artifacts"),
            "--execution-mode",
            "real",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    summary = json.loads(result.stdout)
    assert any("stage-contract-check.json missing" in error for error in summary["errors"])


def test_provider_closeout_rejects_over_budget_cost(tmp_path: Path) -> None:
    fixture_root = tmp_path / "provider-closeout"
    shutil.copytree(ROOT / "tests/fixtures/provider-closeout/good", fixture_root)
    cost_path = fixture_root / "artifacts/cost_report.json"
    cost = json.loads(cost_path.read_text())
    cost["total_cost_usd"] = 25.00
    cost["max_authorized_spend_usd"] = 5.00
    cost_path.write_text(json.dumps(cost, indent=2, sort_keys=True) + "\n")

    result = subprocess.run(
        [
            "python3",
            "scripts/cryocore/provider_closeout_check.py",
            "--provider-run",
            str(fixture_root / "provider-run.json"),
            "--artifact-root",
            str(fixture_root / "artifacts"),
            "--execution-mode",
            "real",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    summary = json.loads(result.stdout)
    assert any("exceeds authorized spend" in error for error in summary["errors"])


def test_provider_closeout_rejects_incomplete_paid_cost_report(tmp_path: Path) -> None:
    fixture_root = tmp_path / "provider-closeout"
    shutil.copytree(ROOT / "tests/fixtures/provider-closeout/good", fixture_root)
    cost_path = fixture_root / "artifacts/cost_report.json"
    cost = json.loads(cost_path.read_text())
    cost.pop("budget_status")
    cost_path.write_text(json.dumps(cost, indent=2, sort_keys=True) + "\n")

    result = subprocess.run(
        [
            "python3",
            "scripts/cryocore/provider_closeout_check.py",
            "--provider-run",
            str(fixture_root / "provider-run.json"),
            "--artifact-root",
            str(fixture_root / "artifacts"),
            "--execution-mode",
            "real",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    summary = json.loads(result.stdout)
    assert "cost report does not include budget_status" in summary["errors"]


def test_issue_check_rejects_paid_worker_command(tmp_path: Path) -> None:
    issue = tmp_path / "issue.md"
    issue.write_text(
        """## Summary
Bad command.
## Inputs
- `runpod/launch-manifests/no-download-smoke.json`
## Expected Artifacts
- `runpod/stage-contracts/no-download-smoke.stage-contract.json`
## Provider / Execution Profile
- provider: `runpod`
- execution profile: `no-download-smoke`
- operator gate required: `yes`
## Acceptance Criteria
- [ ] no paid worker mutation
## Validation Commands
```bash
runpod-bridge run-remote runpod/bridge-manifests/t2r14-open-dossier.json --execute --yes-create-""" + """paid-runpod
```
## Touched Areas
- `runpod/`
## Dependencies
Blocked by: gate
## Risk Notes
- paid
## Complexity
tier: small
<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
target_state: Backlog
touched_areas:
  - runpod/
complexity: small
-->
"""
    )
    result = subprocess.run(
        [
            "python3",
            "scripts/cryocore/issue_check.py",
            str(issue),
            "--repo-root",
            str(ROOT),
            "--json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    summary = json.loads(result.stdout)
    errors = summary["failures"][0]["errors"]
    assert any("provider-mutating" in error for error in errors)


def test_issue_check_rejects_missing_stage_contract_reference(tmp_path: Path) -> None:
    issue = tmp_path / "issue.md"
    issue.write_text(
        """## Summary
Missing contract.
## Inputs
- `runpod/launch-manifests/no-download-smoke.json`
## Expected Artifacts
- `validation/contract-self-check.json`
## Provider / Execution Profile
- provider: `runpod`
- execution profile: `no-download-smoke`
- operator gate required: `no`
## Stage / Progress Contract
- stage contract: `runpod/stage-contracts/missing.stage-contract.json`
## Acceptance Criteria
- [ ] reference scan catches missing contract
## Validation Commands
```bash
python3 scripts/cryocore/runpod_launch_request.py --manifest runpod/launch-manifests/no-download-smoke.json --issue CRYOCORE-TEST --max-spend-usd 1 --execution-mode prep --out .runtime/request.json
```
## Touched Areas
- `runpod/`
## Dependencies
- `docs/compute-backends.md`
## Risk Notes
- reference drift
## Complexity
tier: small
<!-- symphony:schema
schema_version: 1
subgroup: cryocore
routing_label: sym:cryocore
target_state: Backlog
touched_areas:
  - runpod/
complexity: small
-->
"""
    )
    result = subprocess.run(
        [
            "python3",
            "scripts/cryocore/issue_check.py",
            str(issue),
            "--repo-root",
            str(ROOT),
            "--check-file-references",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    summary = json.loads(result.stdout)
    errors = summary["failures"][0]["errors"]
    assert any("missing referenced repo path: runpod/stage-contracts/missing.stage-contract.json" in error for error in errors)


def test_contract_self_check_rejects_dry_run_evidence_in_real_mode(tmp_path: Path) -> None:
    artifact_root = tmp_path / "artifacts"
    validation = artifact_root / "validation"
    validation.mkdir(parents=True)
    (artifact_root / "run-manifest.json").write_text(
        json.dumps({"run_id": "cryocore-no-download-smoke", "dry_run": True}) + "\n"
    )
    (artifact_root / "stage-progress.jsonl").write_text(
        json.dumps({"stage_id": "toolcheck", "status": "completed"}) + "\n"
    )
    (validation / "toolcheck.json").write_text(json.dumps({"ok": True}) + "\n")
    (validation / "gpu.json").write_text(json.dumps({"ok": True}) + "\n")
    (validation / "storage.json").write_text(json.dumps({"ok": True}) + "\n")
    (validation / "license-gates.json").write_text(json.dumps({"ok": True}) + "\n")
    (validation / "input-audit.json").write_text(json.dumps({"ok": True}) + "\n")
    (validation / "workflow-run.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "run_id": "cryocore-no-download-smoke",
                "workflow_engine": "bash",
                "workflow_version": "fixture",
                "workflow_ref": "runpod/entrypoints/no-download-smoke.sh",
                "profile": "no-download-smoke",
                "executor": "runpod",
                "trace_path": "stage-progress.jsonl",
                "output_root": str(artifact_root),
                "resume_mode": "fresh",
                "exit_status": "completed",
            }
        )
        + "\n"
    )
    (validation / "container-provenance.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "run_id": "cryocore-no-download-smoke",
                "container_runtime": "docker",
                "image": "ghcr.io/example/cryocore:fixture",
                "image_digest": "sha256:" + ("a" * 64),
                "sbom_path": "validation/sbom.json",
                "versions_path": "validation/versions.json",
            }
        )
        + "\n"
    )
    (artifact_root / "provenance.md").write_text("fixture provenance\n")

    summary = self_check(ROOT / "runpod/launch-manifests/no-download-smoke.json", artifact_root, "real")
    assert summary["ok"] is False
    assert any("dry_run" in error for error in summary["errors"])
