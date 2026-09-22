import subprocess
from pathlib import Path

import pytest

import scripts.cryocore.public_snapshot_check as snapshot_check
from scripts.cryocore.public_snapshot_check import candidate_paths, check_path, run_check


def _git_init(root: Path) -> None:
    subprocess.run(
        ["git", "init", "-q", "-b", "main"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )


def _ignore_runtime(root: Path) -> None:
    (root / ".gitignore").write_text(".runtime/\n")
    subprocess.run(["git", "add", ".gitignore"], cwd=root, check=True)


def test_public_snapshot_blocks_forced_tracked_ignored_secret(tmp_path: Path) -> None:
    _git_init(tmp_path)
    _ignore_runtime(tmp_path)
    forced = tmp_path / ".runtime" / "forced.txt"
    forced.parent.mkdir()
    forced.write_text("RUNPOD" + "_API_KEY=synthetic\n")
    subprocess.run(["git", "add", "-f", ".runtime/forced.txt"], cwd=tmp_path, check=True)

    summary = run_check(tmp_path, "public", 2_000_000)

    assert summary["ok"] is False
    assert any("secret-like content" in error for error in summary["errors"])


def test_public_snapshot_allows_ignored_untracked_runtime_file(tmp_path: Path) -> None:
    _git_init(tmp_path)
    _ignore_runtime(tmp_path)
    runtime_file = tmp_path / ".runtime" / "operator.txt"
    runtime_file.parent.mkdir()
    runtime_file.write_text("RUNPOD" + "_API_KEY=synthetic\n")

    summary = run_check(tmp_path, "public", 2_000_000)

    assert summary["ok"] is True
    assert not summary["errors"]


def test_public_snapshot_blocks_forced_tracked_ignored_benign_file(tmp_path: Path) -> None:
    _git_init(tmp_path)
    _ignore_runtime(tmp_path)
    forced = tmp_path / ".runtime" / "benign.json"
    forced.parent.mkdir()
    forced.write_text('{"synthetic": true}\n')
    subprocess.run(["git", "add", "-f", ".runtime/benign.json"], cwd=tmp_path, check=True)

    summary = run_check(tmp_path, "public", 2_000_000)

    assert summary["ok"] is False
    assert any("tracked ignored path" in error for error in summary["errors"])


@pytest.mark.parametrize(
    "relative_path",
    [
        ".cryocore-memory/note.md",
        "internal/private/notes.md",
        "logs/run.log",
        ".runtime/state.json",
        "artifacts/result.txt",
        "outputs/result.txt",
        "raw-data/metadata.txt",
        "model-weights/manifest.json",
    ],
)
def test_public_snapshot_blocks_forced_tracked_private_roots(
    relative_path: str, tmp_path: Path
) -> None:
    _git_init(tmp_path)
    path = tmp_path / relative_path
    path.parent.mkdir(parents=True)
    path.write_text("plain synthetic workshop note\n")
    subprocess.run(["git", "add", "-f", relative_path], cwd=tmp_path, check=True)

    public_summary = run_check(tmp_path, "public", 2_000_000)
    workshop_summary = run_check(tmp_path, "workshop", 2_000_000)

    assert public_summary["ok"] is False
    assert any("tracked ignored path" in error for error in public_summary["errors"])
    assert workshop_summary["ok"] is True


def test_public_snapshot_preserves_nested_fixture_artifacts(tmp_path: Path) -> None:
    _git_init(tmp_path)
    path = tmp_path / "tests" / "fixtures" / "example" / "artifacts" / "summary.json"
    path.parent.mkdir(parents=True)
    path.write_text('{"synthetic": true}\n')
    subprocess.run(["git", "add", "-f", str(path.relative_to(tmp_path))], cwd=tmp_path, check=True)

    summary = run_check(tmp_path, "public", 2_000_000)

    assert summary["ok"] is True


def test_public_snapshot_size_cap_skips_content_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    oversized = tmp_path / "oversized.txt"
    oversized.write_text("synthetic content\n")

    def fail_if_read(_path: Path) -> str:
        pytest.fail("oversized files must not be read")

    monkeypatch.setattr(snapshot_check, "read_text", fail_if_read)
    summary = run_check(tmp_path, "public", max_file_bytes=1)

    assert summary["ok"] is False
    assert any("file exceeds max" in error for error in summary["errors"])


def test_candidate_paths_does_not_fallback_after_empty_git_listing(tmp_path: Path) -> None:
    _git_init(tmp_path)
    (tmp_path / ".git" / "info" / "exclude").write_text(".runtime/\n")
    runtime_file = tmp_path / ".runtime" / "ignored.txt"
    runtime_file.parent.mkdir()
    runtime_file.write_text("synthetic\n")

    assert candidate_paths(tmp_path) == []
    assert run_check(tmp_path, "public", 2_000_000)["checked"] == 0


def test_public_snapshot_rejects_escaped_and_dangling_symlinks(tmp_path: Path) -> None:
    outside = tmp_path.parent / "public_snapshot_outside.txt"
    outside.write_text("RUNPOD" + "_API_KEY=synthetic\n")
    try:
        (tmp_path / "escaped.txt").symlink_to(outside)
        (tmp_path / "dangling.txt").symlink_to(tmp_path / "missing.txt")

        summary = run_check(tmp_path, "public", 2_000_000)

        assert summary["ok"] is False
        assert any("escapes repository" in error for error in summary["errors"])
        assert any("dangling symlink" in error for error in summary["errors"])
        assert all("public_snapshot_outside" not in error for error in summary["errors"])
    finally:
        outside.unlink(missing_ok=True)


def test_public_snapshot_checks_ancestor_symlink_without_dereferencing(tmp_path: Path) -> None:
    outside = tmp_path.parent / "public_snapshot_ancestor_outside"
    outside.mkdir()
    (outside / "notes.txt").write_text("RUNPOD" + "_API_KEY=synthetic\n")
    try:
        (tmp_path / "alias").symlink_to(outside, target_is_directory=True)

        errors, warnings = check_path(
            tmp_path,
            tmp_path / "alias" / "notes.txt",
            "public",
            2_000_000,
        )

        assert not warnings
        assert any("escapes repository" in error for error in errors)
        assert all("public_snapshot_ancestor_outside" not in error for error in errors)
    finally:
        (outside / "notes.txt").unlink(missing_ok=True)
        outside.rmdir()


def test_workshop_symlink_check_warns_without_dereferencing(tmp_path: Path) -> None:
    outside = tmp_path.parent / "public_snapshot_workshop_outside.txt"
    outside.write_text("synthetic\n")
    try:
        (tmp_path / "escaped.txt").symlink_to(outside)

        summary = run_check(tmp_path, "workshop", 2_000_000)

        assert summary["ok"] is True
        assert any("escapes repository" in warning for warning in summary["warnings"])
    finally:
        outside.unlink(missing_ok=True)


def test_candidate_paths_preserves_newline_filename_with_nul_git_listing(tmp_path: Path) -> None:
    _git_init(tmp_path)
    filename = "line\nname.txt"
    path = tmp_path / filename
    path.write_text("synthetic\n")
    subprocess.run(["git", "add", "--", filename], cwd=tmp_path, check=True)

    assert path in candidate_paths(tmp_path)
    assert run_check(tmp_path, "public", 2_000_000)["ok"] is True


@pytest.mark.parametrize(
    "operator_path, label",
    [
        ("/" + "Users/" + "account/private/notes.txt", "macOS home path"),
        ("/" + "home/" + "account/private/notes.txt", "Linux home path"),
        ("C:" + "\\" + "Users" + "\\account\\private\\notes.txt", "Windows home path"),
    ],
)
def test_public_snapshot_blocks_operator_paths(operator_path: str, label: str, tmp_path: Path) -> None:
    (tmp_path / "notes.md").write_text(operator_path + "\n")

    summary = run_check(tmp_path, "public", 2_000_000)

    assert summary["ok"] is False
    assert any(label in error for error in summary["errors"])


@pytest.mark.parametrize(
    "leakage",
    [
        "Internal writing " + "guideline: keep this private.\n",
        "Private " + "deliberation: unresolved reasoning.\n",
        "Hidden " + "reasoning notes: synthetic placeholder.\n",
    ],
)
def test_public_snapshot_blocks_copied_internal_guidance(leakage: str, tmp_path: Path) -> None:
    (tmp_path / "copied.md").write_text(leakage)

    summary = run_check(tmp_path, "public", 2_000_000)

    assert summary["ok"] is False
    assert any("copied internal guidance marker" in error for error in summary["errors"])


def test_workshop_copied_internal_guidance_is_a_warning(tmp_path: Path) -> None:
    (tmp_path / "copied.md").write_text("Private " + "deliberation: synthetic placeholder.\n")

    summary = run_check(tmp_path, "workshop", 2_000_000)

    assert summary["ok"] is True
    assert any("copied internal guidance marker" in warning for warning in summary["warnings"])
