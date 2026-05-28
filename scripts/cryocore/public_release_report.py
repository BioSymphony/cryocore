#!/usr/bin/env python3
"""Build a public-release readiness report for CryoCore.

The report is read-only. It does not launch providers, touch networks, mutate
git state, or inspect ignored runtime directories except through explicit file
listing checks.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

try:
    from public_snapshot_check import run_check
    from runpod_manifest_check import load_json as load_runpod_manifest
    from runpod_manifest_check import validate as validate_runpod_manifest
except ModuleNotFoundError:
    from scripts.cryocore.public_snapshot_check import run_check
    from scripts.cryocore.runpod_manifest_check import load_json as load_runpod_manifest
    from scripts.cryocore.runpod_manifest_check import validate as validate_runpod_manifest


REQUIRED_RELEASE_FILES = [
    "README.md",
    "AGENTS.md",
    "PUBLIC_RELEASE.md",
    "BIOSAFETY.md",
    "NON_CLAIMS.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "GOVERNANCE.md",
    "MAINTAINERS.md",
    "CITATION.cff",
    "CHANGELOG.md",
    "LICENSE",
    "NOTICE.md",
    "SUPPORT.md",
    "FAQ.md",
    "ROADMAP.md",
    "pyproject.toml",
    "requirements-dev.txt",
    ".gitattributes",
    ".github/CODEOWNERS",
    ".github/workflows/ci.yml",
    ".github/workflows/release.yml",
    ".github/dependabot.yml",
    ".github/labels.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/docs_gap.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/help_wanted_demo.yml",
    ".github/ISSUE_TEMPLATE/public_accession_demo.yml",
    ".github/ISSUE_TEMPLATE/question.yml",
    ".github/ISSUE_TEMPLATE/privacy_security.yml",
    "docs/PUBLIC_LAUNCH_PAD.md",
    "docs/README.md",
    "docs/public-quickstart.md",
    "docs/agent-quickstart.md",
    "docs/workflows.md",
    "docs/use-cases.md",
    "docs/adoption-guide.md",
    "docs/local-installation.md",
    "docs/agent-skill-guide.md",
    "docs/skill-installation.md",
    "docs/validation-command-matrix.md",
    "docs/failure-modes.md",
    "docs/recipes/README.md",
    "docs/recipes/public-accession-example.md",
    "docs/recipes/map-model-dossier.md",
    "docs/recipes/provider-closeout.md",
    "docs/recipes/toolwatch-audit.md",
    "docs/recipes/figure-dossier.md",
    "docs/recipes/heterogeneity-jury.md",
    "docs/prompt-library.md",
    "docs/demo-gallery.md",
    "docs/glossary.md",
    "docs/license-scope.md",
    "docs/public-repo-and-private-image-policy.md",
    "docs/public-switch-checklist.md",
    "docs/provider-execution-model.md",
    "docs/provider-readiness.md",
    "docs/github-repo-profile.md",
    "docs/claim-levels.md",
    "docs/data-policy.md",
    "docs/schema-catalog.md",
    "docs/module-catalog.md",
    "docs/privacy-threat-model.md",
    "docs/troubleshooting.md",
    "docs/no-false-success-hardening.md",
    "docs/tooling-and-licensing.md",
    "docs/assets/cryocore-overview.svg",
    "docs/assets/agent-loop.svg",
    "docs/assets/use-case-map.svg",
    "docs/assets/workflow-selector.svg",
    "docs/assets/demo-gallery/t2r14-preview.svg",
    "docs/assets/demo-gallery/t2r14-claim-excerpt.md",
    "skills/README.md",
    "skills/index.yaml",
    "skills/cryocore-public-safety/SKILL.md",
    "examples/README.md",
    "examples/agent-tasks/README.md",
    "examples/agent-tasks/public-safety-review.prompt.md",
    "examples/agent-tasks/map-model-dossier.prompt.md",
    "examples/agent-tasks/cloud-provider-prep.prompt.md",
    "examples/agent-tasks/linear-wave-planning.prompt.md",
    "examples/t2r14-open-dossier-preview/README.md",
    "examples/t2r14-open-dossier-preview/dossier_manifest.sample.json",
    "examples/t2r14-open-dossier-preview/validation-summary.sample.json",
    "examples/t2r14-open-dossier-preview/claim_ledger.sample.md",
    "templates/README.md",
    "templates/agent-handoff.md",
    "templates/final-outcome-block.md",
    "modules/README.md",
    "runpod/README.md",
    "runpod/entrypoints/bootstrap-repo.sh",
    "runpod/entrypoints/bootstrap-gated-tools.sh",
    "scripts/README.md",
    "scripts/cryocore/docs_link_check.py",
    "scripts/cryocore/runpod_reference_check.py",
    "scripts/cryocore/tooling_freshness_check.py",
]

BLOCKED_DIR_PARTS = {
    ".runtime",
    "raw-data",
    "raw-cryoem-data",
    "empiar-cache",
    "emdb-cache",
    "pdb-cache",
    "model-weights",
    "runpod-runs",
    "runpod-volumes",
    "scratch",
}

HEAVY_SUFFIXES = {
    ".mrc",
    ".mrc.gz",
    ".mrcs",
    ".mrcs.gz",
    ".map",
    ".map.gz",
    ".eer",
    ".tif",
    ".tiff",
    ".dm4",
    ".star",
    ".star.gz",
    ".cs",
    ".h5",
    ".hdf5",
    ".npy",
    ".npz",
    ".pt",
    ".pth",
    ".safetensors",
    ".ckpt",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".tar",
    ".tar.gz",
    ".tgz",
    ".zip",
}

PRIVATE_SOURCE_DOCS = {
    "docs/migration-inventory.md",
    "logs/2026-05-15-cryo-core-split-eval.md",
}

TEXT_SUFFIXES = {
    ".bash",
    ".cfg",
    ".css",
    ".html",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

CONTENT_SCAN_EXCLUDE = {
    "scripts/cryocore/issue_check.py",
    "scripts/cryocore/public_release_report.py",
    "scripts/cryocore/public_snapshot_check.py",
}


def prohibited_release_markers() -> list[str]:
    # Markers that should never appear in the public release. Several entries
    # are operator-specific (e.g. the operator's private repo name). Strings are
    # split with string concatenation so this scanner's own source does not trip
    # itself. Adopters of CryoCore should replace operator-specific markers with
    # their own private identifiers. Links to the operator's own public repos
    # (e.g. the Proteus skill pack at github.com/jvogan/proteus) are allowed.
    runpod_key = "RUNPOD" + "_API_KEY"
    private_repo_name = "biosymphony-" + "CryoCore"
    keychain_marker = "Keychain-" + "backed"
    provider_doctor = "runpod-global-" + "doctor"
    operator_env_path = "path/to/" + "operator"
    snapshot_path = "/path/to/" + "cryocore-snapshot"
    closeout_path = "path/to/" + "trusted-closeout.py"
    remote_launch_true = '"remote_launch_allowed": ' + "true"
    raw_download_env = '"CRYOCORE_ALLOW_RAW_DOWNLOADS": ' + '"1"'
    paid_run_flag = "--yes-create-" + "paid-runpod"
    private_clone_text = "private GitHub " + "clone"
    return [
        private_repo_name,
        keychain_marker,
        provider_doctor,
        operator_env_path,
        snapshot_path,
        closeout_path,
        remote_launch_true,
        raw_download_env,
        paid_run_flag,
        runpod_key,
        private_clone_text,
    ]


def git_output(root: Path, args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        text=True,
        capture_output=True,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def tracked_or_candidate_files(root: Path) -> list[Path]:
    code, stdout, _ = git_output(root, ["ls-files", "--cached", "--others", "--exclude-standard"])
    if code == 0:
        return [root / line for line in stdout.splitlines() if line.strip()]
    return [path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts]


def rel(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve()))


def suffix_match(path: Path, suffixes: set[str]) -> str | None:
    lower = path.name.lower()
    for suffix in sorted(suffixes, key=len, reverse=True):
        if lower.endswith(suffix):
            return suffix
    return None


def text_files_for_content_scan(root: Path, files: list[Path]) -> list[Path]:
    result: list[Path] = []
    for path in files:
        relative = rel(root, path)
        if relative in CONTENT_SCAN_EXCLUDE:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"Makefile", "AGENTS.md", "README.md"}:
            result.append(path)
    return result


def prohibited_content_matches(root: Path, files: list[Path]) -> list[str]:
    matches: list[str] = []
    markers = prohibited_release_markers()
    for path in text_files_for_content_scan(root, files):
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for marker in markers:
                if marker in line:
                    matches.append(f"{rel(root, path)}:{line_number}: {marker}")
    return sorted(matches)


def runpod_manifest_warnings(root: Path) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    for path in sorted((root / "runpod" / "launch-manifests").glob("*.json")):
        result = validate_runpod_manifest(load_runpod_manifest(path), manifest_path=path)
        for warning in result.get("warnings", []):
            warnings.append({"path": rel(root, path), "warning": warning})
    return warnings


def git_value(root: Path, args: list[str]) -> str:
    code, stdout, _ = git_output(root, args)
    return stdout if code == 0 else ""


def run_report(root: Path, max_file_bytes: int, expected_remote: str = "") -> dict[str, Any]:
    files = tracked_or_candidate_files(root)
    git_code, git_status, git_status_err = git_output(root, ["status", "--short", "--branch"])
    remote_code, remote_out, _ = git_output(root, ["remote", "-v"])
    has_commits = git_output(root, ["rev-parse", "--verify", "HEAD"])[0] == 0
    current_head = git_value(root, ["rev-parse", "--short=12", "HEAD"]) if has_commits else ""
    current_branch = git_value(root, ["branch", "--show-current"]) or git_value(root, ["symbolic-ref", "--short", "HEAD"])
    tags_at_head = git_value(root, ["tag", "--points-at", "HEAD"]).splitlines() if has_commits else []
    remotes = remote_out.splitlines() if remote_code == 0 and remote_out else []
    status_lines = git_status.splitlines() if git_code == 0 else []
    working_tree_clean = git_code == 0 and all(line.startswith("## ") for line in status_lines)

    missing_release_files = [item for item in REQUIRED_RELEASE_FILES if not (root / item).exists()]
    private_source_docs_present = [item for item in PRIVATE_SOURCE_DOCS if (root / item).exists()]
    blocked_dirs_present = sorted(
        {
            str(Path(rel(root, path)).parts[0])
            for path in files
            if any(part in BLOCKED_DIR_PARTS for part in Path(rel(root, path)).parts)
        }
    )
    heavy_candidates = sorted(
        rel(root, path)
        for path in files
        if path.is_file() and suffix_match(path, HEAVY_SUFFIXES) is not None
    )
    oversize_candidates = sorted(
        f"{rel(root, path)} ({path.stat().st_size} bytes)"
        for path in files
        if path.is_file() and path.stat().st_size > max_file_bytes
    )
    content_matches = prohibited_content_matches(root, files)

    snapshot = run_check(root, "public", max_file_bytes)
    runpod_warnings = runpod_manifest_warnings(root)
    blockers = []
    if missing_release_files:
        blockers.append("missing release files")
    if private_source_docs_present:
        blockers.append("private-source docs present")
    if blocked_dirs_present:
        blockers.append("blocked runtime/data directories present")
    if heavy_candidates:
        blockers.append("heavy/private artifact suffixes present")
    if oversize_candidates:
        blockers.append("oversize files present")
    if not snapshot["ok"]:
        blockers.append("public snapshot check failed")
    if content_matches:
        blockers.append("prohibited public-release content markers present")
    public_switch_blockers = []
    if not has_commits:
        public_switch_blockers.append("no initial public commit yet")
    if has_commits and not working_tree_clean:
        public_switch_blockers.append("working tree has uncommitted changes")
    if not remotes:
        public_switch_blockers.append("no public remote configured yet")
    if expected_remote and not any(expected_remote in remote for remote in remotes):
        public_switch_blockers.append(f"expected public remote not configured: {expected_remote}")
    if has_commits and not tags_at_head:
        public_switch_blockers.append("current HEAD is not tagged for release")

    return {
        "ok": not blockers,
        "check_type": "cryocore_public_release_report",
        "repo_root": str(root.resolve()),
        "git": {
            "available": git_code == 0,
            "status": git_status,
            "status_error": git_status_err,
            "has_commits": has_commits,
            "current_head": current_head,
            "current_branch": current_branch,
            "tags_at_head": tags_at_head,
            "remotes": remotes,
            "working_tree_clean": working_tree_clean,
            "fresh_history_ready": has_commits and working_tree_clean,
        },
        "public_switch": {
            "ready": not blockers and not public_switch_blockers,
            "blockers": public_switch_blockers,
            "expected_remote": expected_remote,
            "note": "Local content gates can pass before the public GitHub remote, initial commit, CI run, and tag exist.",
        },
        "file_count": len(files),
        "max_file_bytes": max_file_bytes,
        "missing_release_files": missing_release_files,
        "private_source_docs_present": private_source_docs_present,
        "blocked_dirs_present": blocked_dirs_present,
        "heavy_candidates": heavy_candidates,
        "oversize_candidates": oversize_candidates,
        "prohibited_content_matches": content_matches,
        "public_snapshot": {
            "ok": snapshot["ok"],
            "checked": snapshot["checked"],
            "errors": snapshot["errors"],
            "warnings": snapshot["warnings"],
        },
        "runpod_manifest_warnings": runpod_warnings,
        "blockers": blockers,
        "notes": [
            "This report is local and read-only.",
            "Provider execution readiness still requires digest-pinned images and operator authorization.",
            "A clean public history should be committed only after this report and make release-check pass.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--max-file-bytes", type=int, default=2_000_000)
    parser.add_argument("--expected-remote", default="")
    parser.add_argument("--publish-ready", action="store_true", help="Fail if git remote/commit/tag public-switch state is incomplete")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = run_report(args.repo_root.resolve(), args.max_file_bytes, args.expected_remote)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
        summary["report_path"] = str(args.out.resolve())

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"ok: {summary['ok']}")
        for blocker in summary["blockers"]:
            print(f"blocker: {blocker}")
        for note in summary["notes"]:
            print(f"note: {note}")
    if args.publish_ready and summary["public_switch"]["blockers"]:
        return 1
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
