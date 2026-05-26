#!/usr/bin/env python3
"""Validate RunPod bridge manifests are scoped to CryoCore resources."""

from __future__ import annotations

import argparse
import base64
import binascii
import io
import json
import re
import subprocess
import tarfile
import tempfile
from pathlib import PurePosixPath
from pathlib import Path
from typing import Any

try:
    from public_snapshot_check import PUBLIC_PRIVATE_MARKERS, SECRET_PATTERNS, denied_extension
except ModuleNotFoundError:
    from scripts.cryocore.public_snapshot_check import PUBLIC_PRIVATE_MARKERS, SECRET_PATTERNS, denied_extension


ALLOWED_RESOURCE_PREFIXES = ("cryocore-",)
FORBIDDEN_CROSS_CAMPAIGN_MARKERS = ("GENECLUSTER", "BIOPROSPECTOR", "DOE_", "OBS_", "PARAMETER_GOLF")
CRYOCORE_VOLUME_REF = "CRYOCORE_RUNPOD_NETWORK_VOLUME_ID"
ALLOWED_SOFTWARE_ROOTS = ("/workspace/cryocore/", "/workspace/software")
ALLOWED_REPO_SOURCES = {"git_remote_or_snapshot", "inline_commands"}
SOURCELESS_WORKDIR_BASENAMES = {"biosymphony-cryocore", "biosymphony-cryocore-public"}
INLINE_PAYLOAD_RE = re.compile(r"payload\s*=\s*(['\"])(?P<payload>[A-Za-z0-9+/=]+)\1")
MAX_INLINE_BUNDLE_BYTES = 2_000_000
MAX_INLINE_MEMBER_BYTES = 1_000_000
PUBLIC_ARTIFACT_SERVER_MARKERS = (
    "--directory runpod-execution/artifacts",
    "cd runpod-execution/artifacts",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def bridge_paths(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.glob("*.json"))
    return [path]


def string_contains_forbidden_marker(value: Any) -> str | None:
    text = json.dumps(value, sort_keys=True) if not isinstance(value, str) else value
    upper = text.upper()
    for marker in FORBIDDEN_CROSS_CAMPAIGN_MARKERS:
        if marker in upper:
            return marker
    return None


def is_hex_commit(value: str) -> bool:
    return len(value) == 40 and all(char in "0123456789abcdef" for char in value.lower())


def remote_commit_visible(url: str, commit: str, timeout_seconds: int = 30) -> tuple[bool, str]:
    """Return whether the declared remote can satisfy a checkout of the pinned commit."""
    if not url or not is_hex_commit(commit):
        return False, "repo url or commit pin is invalid"
    try:
        ls_remote = subprocess.run(
            ["git", "ls-remote", url],
            check=False,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"git ls-remote failed: {exc}"
    if ls_remote.returncode == 0 and any(line.startswith(f"{commit}\t") for line in ls_remote.stdout.splitlines()):
        return True, "commit is advertised by a remote ref"

    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "init", "-q", tmp], check=True, text=True, capture_output=True)
        fetch = subprocess.run(
            ["git", "-C", tmp, "fetch", "--depth=1", "--filter=blob:none", url, commit],
            check=False,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
        )
    if fetch.returncode == 0:
        return True, "commit is fetchable by SHA"
    stderr = fetch.stderr.strip().splitlines()
    detail = stderr[-1] if stderr else "git fetch by SHA failed"
    return False, detail


def embedded_text_errors(text: str, label: str, profile: str) -> list[str]:
    errors: list[str] = []
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{label}: secret-like content matched {pattern.pattern}")
    private_hits = [marker for marker in PUBLIC_PRIVATE_MARKERS if marker in text]
    if private_hits and profile == "public":
        errors.append(f"{label}: private/workshop markers present: {', '.join(private_hits)}")
    return errors


def validate_bundle_member(member: tarfile.TarInfo, archive: tarfile.TarFile, profile: str) -> list[str]:
    errors: list[str] = []
    member_path = PurePosixPath(member.name)
    if member_path.is_absolute() or ".." in member_path.parts or not member_path.parts:
        errors.append(f"embedded source bundle has unsafe member path: {member.name}")
    if member.issym() or member.islnk() or member.isdev():
        errors.append(f"embedded source bundle member is not a regular file: {member.name}")
    if member.isdir():
        return errors
    if not member.isfile():
        errors.append(f"embedded source bundle member must be a regular file: {member.name}")
        return errors
    if member.size > MAX_INLINE_MEMBER_BYTES:
        errors.append(f"embedded source bundle member exceeds {MAX_INLINE_MEMBER_BYTES} bytes: {member.name}")
    extension = denied_extension(member.name)
    if extension:
        errors.append(f"embedded source bundle member has denied public artifact extension {extension}: {member.name}")
    extracted = archive.extractfile(member)
    if extracted is None:
        errors.append(f"embedded source bundle member could not be read: {member.name}")
        return errors
    payload = extracted.read(MAX_INLINE_MEMBER_BYTES + 1)
    if len(payload) > MAX_INLINE_MEMBER_BYTES:
        errors.append(f"embedded source bundle member exceeds scan limit: {member.name}")
    text = payload.decode("utf-8", errors="ignore")
    errors.extend(embedded_text_errors(text, f"embedded source bundle member {member.name}", profile))
    return errors


def validate_inline_payloads(command: str, profile: str) -> list[str]:
    errors: list[str] = []
    for index, match in enumerate(INLINE_PAYLOAD_RE.finditer(command), start=1):
        payload = match.group("payload")
        try:
            decoded = base64.b64decode(payload, validate=True)
        except (ValueError, binascii.Error) as exc:
            errors.append(f"inline source bundle {index} is not valid base64: {exc}")
            continue
        if len(decoded) > MAX_INLINE_BUNDLE_BYTES:
            errors.append(f"inline source bundle {index} exceeds {MAX_INLINE_BUNDLE_BYTES} decoded bytes")
            continue
        try:
            with tarfile.open(fileobj=io.BytesIO(decoded), mode="r:gz") as archive:
                members = archive.getmembers()
                if not members:
                    errors.append(f"inline source bundle {index} is empty")
                total_size = 0
                for member in members:
                    total_size += max(member.size, 0)
                    errors.extend(validate_bundle_member(member, archive, profile))
                if total_size > MAX_INLINE_BUNDLE_BYTES:
                    errors.append(f"inline source bundle {index} expands beyond {MAX_INLINE_BUNDLE_BYTES} bytes")
        except tarfile.TarError as exc:
            errors.append(f"inline source bundle {index} is not a valid tar.gz archive: {exc}")
    return errors


def validate_startup_commands(commands: Any, access: dict[str, Any], profile: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(commands, list):
        errors.append("startup.commands must be a list")
        return errors
    for index, command in enumerate(commands, start=1):
        if not isinstance(command, str):
            errors.append(f"startup.commands[{index}] must be a string")
            continue
        if "http.server" in command and "--bind 0.0.0.0" in command:
            if access.get("public_services_require_auth") is not True:
                errors.append(
                    "public 0.0.0.0 artifact services must set access.public_services_require_auth=true"
                )
            if not any(marker in command for marker in PUBLIC_ARTIFACT_SERVER_MARKERS):
                errors.append(
                    "public artifact server must serve runpod-execution/artifacts, not the repository workspace"
                )
        errors.extend(validate_inline_payloads(command, profile))
    return errors


def validate_bridge(
    data: dict[str, Any],
    path: Path,
    *,
    profile: str = "public",
    source_ready: bool = False,
    probe_remote: bool = False,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    runpod = data.get("runpod", {})
    repo = data.get("repo", {})
    worker = data.get("worker_coordination", {})
    closeout = data.get("closeout", {})
    artifact_egress = data.get("artifact_egress", {})
    tool_setup = runpod.get("toolSetup", {}) if isinstance(runpod, dict) else {}
    env = runpod.get("env", {}) if isinstance(runpod, dict) else {}

    if data.get("manifest_kind") != "symphony_runpod_launch":
        errors.append("manifest_kind must be symphony_runpod_launch")
    provider = data.get("provider", {})
    if provider.get("name") != "runpod" or provider.get("adapter") != "runpod_pod_v1":
        errors.append("provider must be runpod_pod_v1")
    if data.get("remote_launch_allowed") is True and profile == "public":
        errors.append("public bridge manifests must keep remote_launch_allowed=false")
    if data.get("remote_launch_allowed") is True and profile == "operator":
        authorization = data.get("launch_authorization", {})
        if not isinstance(authorization, dict):
            errors.append("operator bridge manifests with remote launch enabled require launch_authorization")
        else:
            if not authorization.get("approved_by") or authorization.get("approved_by") == "operator-required":
                errors.append("operator bridge launch_authorization.approved_by must identify the approving operator")
            if not authorization.get("approved_at"):
                errors.append("operator bridge launch_authorization.approved_at is required")

    if not isinstance(repo, dict):
        errors.append("repo must be an object")
    else:
        repo_source = str(repo.get("source", ""))
        repo_url = str(repo.get("url_or_path", ""))
        commit_or_snapshot = str(repo.get("commit_or_snapshot", ""))
        if repo_source not in ALLOWED_REPO_SOURCES:
            errors.append("repo.source must be git_remote_or_snapshot or inline_commands")
        if repo_source == "git_remote_or_snapshot":
            if not repo_url or repo_url == "inline":
                errors.append("git_remote_or_snapshot requires repo.url_or_path")
            if not is_hex_commit(commit_or_snapshot):
                errors.append("git_remote_or_snapshot requires repo.commit_or_snapshot to be a 40-character commit SHA")
            elif source_ready and probe_remote:
                visible, detail = remote_commit_visible(repo_url, commit_or_snapshot)
                if not visible:
                    errors.append(
                        "git_remote_or_snapshot commit is not fetchable from repo.url_or_path: "
                        f"{commit_or_snapshot} ({detail})"
                    )
        elif repo_source == "inline_commands":
            startup_commands = data.get("startup", {}).get("commands", [])
            if not isinstance(startup_commands, list) or not startup_commands:
                errors.append("inline_commands requires startup.commands")
            workdir = str(repo.get("workdir", ""))
            if source_ready and (
                not workdir or Path(workdir).name.casefold() in SOURCELESS_WORKDIR_BASENAMES
            ):
                warnings.append(
                    "inline_commands does not clone the repo; ensure commands are fully inline or repo.workdir is pre-synced"
                )

    resource_prefix = str(worker.get("resource_name_prefix", ""))
    if not resource_prefix:
        errors.append("worker_coordination.resource_name_prefix is required")
    elif not resource_prefix.startswith(ALLOWED_RESOURCE_PREFIXES):
        errors.append(
            "worker_coordination.resource_name_prefix must start with one of: "
            + ", ".join(ALLOWED_RESOURCE_PREFIXES)
        )
    if worker.get("single_mutating_worker") is not True:
        errors.append("worker_coordination.single_mutating_worker must be true")
    if worker.get("read_only_monitors_allowed") is not True:
        errors.append("worker_coordination.read_only_monitors_allowed must be true")

    pod_name = str(runpod.get("name", ""))
    if not pod_name:
        errors.append("runpod.name is required")
    elif not pod_name.startswith(ALLOWED_RESOURCE_PREFIXES):
        errors.append("runpod.name must start with a CryoCore prefix")

    network_volume_id = str(runpod.get("networkVolumeId", ""))
    if network_volume_id:
        marker = string_contains_forbidden_marker(network_volume_id)
        if marker:
            errors.append(f"runpod.networkVolumeId appears to reference another campaign: {marker}")
        if (
            "PENDING-set-at-launch-from-" in network_volume_id
            and CRYOCORE_VOLUME_REF not in network_volume_id
        ):
            errors.append(
                "pending networkVolumeId must use "
                f"{CRYOCORE_VOLUME_REF}, not a generic or sibling-campaign env var"
            )
        repo_source = env.get("CRYOCORE_REPO_SOURCE") if isinstance(env, dict) else None
        if artifact_egress.get("requires_network_volume") is not True and repo_source != "network_volume":
            warnings.append("networkVolumeId is set but artifact_egress.requires_network_volume is not true")

    if isinstance(env, dict):
        volume_root = env.get("CRYOCORE_VOLUME_ROOT")
        if network_volume_id and volume_root != "/workspace/cryocore":
            errors.append("network-volume runs must set CRYOCORE_VOLUME_ROOT=/workspace/cryocore")
    else:
        errors.append("runpod.env must be an object")

    marker = string_contains_forbidden_marker(data)
    if marker:
        errors.append(f"manifest contains forbidden cross-campaign marker: {marker}")

    access = data.get("access", {})
    if not isinstance(access, dict):
        errors.append("access must be an object")
        access = {}
    errors.extend(validate_startup_commands(data.get("startup", {}).get("commands", []), access, profile))

    if isinstance(tool_setup, dict) and tool_setup:
        tool_setup_env_ref = tool_setup.get("network_volume_env_var")
        tool_setup_volume_id = tool_setup.get("network_volume_id")
        if tool_setup_env_ref != CRYOCORE_VOLUME_REF and tool_setup_volume_id != network_volume_id:
            errors.append(
                "runpod.toolSetup must declare either "
                f"network_volume_env_var={CRYOCORE_VOLUME_REF} or a network_volume_id matching runpod.networkVolumeId"
            )
        software_root = str(tool_setup.get("software_root", ""))
        if software_root and not software_root.startswith(ALLOWED_SOFTWARE_ROOTS):
            errors.append(
                "runpod.toolSetup.software_root must live under /workspace/cryocore "
                "or /workspace/software on a dedicated CryoCore volume"
            )
        weights_root = str(tool_setup.get("weights_root", ""))
        if weights_root and not weights_root.startswith(ALLOWED_SOFTWARE_ROOTS):
            errors.append(
                "runpod.toolSetup.weights_root must live under /workspace/cryocore "
                "or /workspace/software on a dedicated CryoCore volume"
            )
    elif network_volume_id and not (
        isinstance(env, dict) and env.get("CRYOCORE_REPO_SOURCE") == "network_volume"
    ):
        warnings.append("networkVolumeId is set but runpod.toolSetup is not declared")

    if closeout.get("stop_or_delete_pod") is not True:
        errors.append("closeout.stop_or_delete_pod must be true")
    if closeout.get("retain_pod") is not False:
        errors.append("closeout.retain_pod must be false unless an issue explicitly authorizes retention")

    return {
        "ok": not errors,
        "path": str(path),
        "run_id": data.get("run_id"),
        "pod_name": pod_name,
        "resource_name_prefix": resource_prefix,
        "network_volume_id": network_volume_id,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="Bridge manifest JSON file or directory")
    parser.add_argument("--profile", choices=["public", "operator"], default="public")
    parser.add_argument("--source-ready", action="store_true", help="Require repo delivery to be ready for paid launch")
    parser.add_argument("--no-remote-probe", action="store_true", help="Skip git remote fetchability probe")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results = [
        validate_bridge(
            load_json(path),
            path,
            profile=args.profile,
            source_ready=args.source_ready,
            probe_remote=not args.no_remote_probe,
        )
        for path in bridge_paths(args.path)
    ]
    ok = bool(results) and all(result["ok"] for result in results)
    summary = {
        "ok": ok,
        "checked": len(results),
        "failures": [result for result in results if not result["ok"]],
        "warnings": [
            {"path": result["path"], "warning": warning}
            for result in results
            for warning in result["warnings"]
        ],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"ok: {ok}")
        print(f"checked: {len(results)}")
        for result in summary["failures"]:
            print(f"failed: {result['path']}")
            for error in result["errors"]:
                print(f"  {error}")
        for warning in summary["warnings"]:
            print(f"warning: {warning['path']}: {warning['warning']}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
