import json

import pytest

from scripts.cryocore.public_release_report import public_summary
from scripts.cryocore.public_snapshot_check import run_check


def test_public_summary_excludes_all_diagnostic_strings():
    local = "/Volumes/" + "example-drive/run"
    report = {
        "ok": False,
        "repo_root": local,
        "git": {"current_head": "a" * 40, "remotes": [local], "status": local},
        "public_snapshot": {"ok": False, "errors": [local], "warnings": [local]},
        "blockers": [local],
        "public_switch": {"ready": False, "blockers": [local]},
        "future_field": {"nested": local},
    }
    result = public_summary(report)
    encoded = json.dumps(result)
    assert local not in encoded
    assert result["commit"] == "a" * 40
    assert result["blocker_count"] == 1
    assert result["content_error_count"] == 1
    assert not result["ok"]


def test_public_summary_rejects_unexpected_commit_text():
    assert public_summary({"git": {"current_head": "local details"}})["commit"] is None


@pytest.mark.parametrize("prefix", ["/Volumes" + "/", "/media" + "/"])
def test_public_scan_blocks_mounted_storage_paths(tmp_path, prefix):
    (tmp_path / "notes.md").write_text(prefix + "example-drive/run/results")
    result = run_check(tmp_path, "public", 2_000_000)
    assert not result["ok"]
    assert any("mounted" in error for error in result["errors"])
