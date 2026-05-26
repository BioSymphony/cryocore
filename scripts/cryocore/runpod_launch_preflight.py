#!/usr/bin/env python3
"""No-launch RunPod readiness preflight for CryoCore manifests."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

try:
    from runpod_manifest_check import validate
    from runpod_scope_check import remote_commit_visible
except ModuleNotFoundError:
    from scripts.cryocore.runpod_manifest_check import validate
    from scripts.cryocore.runpod_scope_check import remote_commit_visible


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def runtime_ref_ready(refs: list[str]) -> tuple[bool, list[str], str]:
    present = [ref for ref in refs if os.environ.get(ref)]
    auth_id_ready = "RUNPOD_GHCR_REGISTRY_AUTH_ID" in present
    user_token_ready = "RUNPOD_GHCR_USERNAME" in present and "RUNPOD_GHCR_TOKEN" in present
    if auth_id_ready:
        return True, present, "registry_auth_id"
    if user_token_ready:
        return True, present, "username_token_pair"
    return False, present, "missing_auth_id_or_username_token_pair"


def preflight(manifest_path: Path, execution_ready: bool) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    manifest_check = validate(manifest, manifest_path=manifest_path, execution_ready=execution_ready)
    blockers: list[str] = []
    warnings = list(manifest_check["warnings"])
    runpod = manifest.get("runpod", {})
    repo = manifest.get("repo", {})

    registry_auth = runpod.get("registry_auth", {}) if isinstance(runpod, dict) else {}
    runtime_refs = registry_auth.get("runtime_secret_refs", []) if isinstance(registry_auth, dict) else []
    registry_ready, present_refs, registry_mode = (
        runtime_ref_ready(runtime_refs) if isinstance(runtime_refs, list) else (False, [], "invalid_runtime_refs")
    )
    if registry_auth.get("required") is True and not registry_ready:
        blockers.append(
            "private registry image requires RUNPOD_GHCR_REGISTRY_AUTH_ID or both RUNPOD_GHCR_USERNAME and RUNPOD_GHCR_TOKEN; declared refs: "
            + ", ".join(str(ref) for ref in runtime_refs)
        )

    image_name = str(runpod.get("image_name", ""))
    if "@sha256:" not in image_name:
        blockers.append("image is not digest-pinned; use a digest-pinned image or verified bootstrap posture before real launch")

    git_ref = str(repo.get("git_ref", ""))
    commit_pinned = len(git_ref) == 40 and all(char in "0123456789abcdef" for char in git_ref.lower())
    if not commit_pinned:
        blockers.append("repo.git_ref is not a 40-character commit SHA visible to the RunPod clone")
    elif execution_ready:
        repo_url = str(repo.get("url", ""))
        visible, detail = remote_commit_visible(repo_url, git_ref)
        if not visible:
            blockers.append(f"repo.git_ref is not fetchable from repo.url: {git_ref} ({detail})")

    stage_contract = manifest.get("stage_contract")
    if isinstance(stage_contract, str):
        stage_path = (manifest_path.resolve().parents[2] / stage_contract).resolve()
        if not stage_path.exists():
            blockers.append(f"stage contract is not present in cloneable repo path: {stage_contract}")
    else:
        blockers.append("stage_contract is missing")

    launch_authorization = os.environ.get("CRYOCORE_REMOTE_LAUNCH_ALLOWED") in {"1", "true", "yes"}
    if execution_ready and not launch_authorization:
        blockers.append("CRYOCORE_REMOTE_LAUNCH_ALLOWED must be truthy for execution-ready launch")

    return {
        "ok": manifest_check["ok"] and (not execution_ready or not blockers),
        "check_type": "cryocore_runpod_launch_preflight",
        "execution_ready": execution_ready,
        "manifest_path": str(manifest_path.resolve()),
        "manifest_check": manifest_check,
        "registry_auth": {
            "required": registry_auth.get("required") is True,
            "runtime_secret_refs": runtime_refs,
            "ready": registry_ready,
            "present_refs": present_refs,
            "mode": registry_mode,
        },
        "repo_commit_pinned": commit_pinned,
        "image_digest_pinned": "@sha256:" in image_name,
        "remote_launch_authorized": launch_authorization,
        "blockers": blockers,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--execution-ready", action="store_true")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = preflight(args.manifest, args.execution_ready)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
        summary["report_path"] = str(args.out.resolve())

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"ok: {summary['ok']}")
        for warning in summary["warnings"]:
            print(f"warning: {warning}")
        for blocker in summary["blockers"]:
            print(f"blocker: {blocker}")
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
