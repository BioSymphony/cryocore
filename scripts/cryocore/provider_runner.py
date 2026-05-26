#!/usr/bin/env python3
"""Run a supported CryoCore provider profile locally and write closeout evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SUPPORTED_ENTRYPOINTS = {
    "no-download-smoke": "runpod/entrypoints/no-download-smoke.sh",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def relative_artifact_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != "artifact_hashes.json":
            hashes[str(path.relative_to(root))] = sha256(path)
    return hashes


def write_runner_artifacts(
    run_root: Path,
    command: list[str],
    returncode: int,
    started_at: str,
    finished_at: str,
) -> None:
    write_jsonl(
        run_root / "executed-commands.jsonl",
        {
            "stage_id": "local_provider_runner",
            "command": " ".join(command),
            "exit_code": returncode,
            "outputs": ["provider-run.json", "validation/provider-closeout-check.json"],
            "timestamp": finished_at,
        },
    )
    write_json(
        run_root / "claim_ledger.json",
        {
            "schema_version": 1,
            "claims": [
                {
                    "claim": "Local provider runner executed the no-download CryoCore control lane.",
                    "claim_level": "processed" if returncode == 0 else "blocked",
                    "evidence_artifact": "validation/provider-closeout-check.json",
                    "caveat": "Local prep evidence does not prove paid provider readiness or biological validity.",
                }
            ],
        },
    )
    provenance = f"""# Local Provider Runner Provenance

- started_at: `{started_at}`
- finished_at: `{finished_at}`
- command: `{' '.join(command)}`
- provider: `local`
- claim boundary: local prep/control evidence only
"""
    (run_root / "provenance.md").write_text(provenance)


def provider_run_payload(
    run_id: str,
    manifest: Path,
    returncode: int,
    started_at: str,
    finished_at: str,
    elapsed: float,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "provider": "local",
        "provider_run_id": f"local-{run_id}",
        "run_id": run_id,
        "manifest_path": str(manifest),
        "status": "completed" if returncode == 0 else "failed",
        "desired_status": "local_execution",
        "actual_status": "exited",
        "runtime_uptime_seconds": round(elapsed, 3),
        "image": "local-workstation",
        "gpu_type": os.environ.get("CRYOCORE_LOCAL_GPU"),
        "cost_usd": 0,
        "started_at": started_at,
        "finished_at": finished_at,
        "claim_level": "processed" if returncode == 0 else "blocked",
        "evidence_mode": "fixture_or_demo",
        "errors": [] if returncode == 0 else [f"entrypoint exited {returncode}"],
    }


def run_closeout(root: Path, run_root: Path, provider_run: Path, execution_mode: str) -> int:
    out = run_root / "validation/provider-closeout-check.json"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/cryocore/provider_closeout_check.py",
            "--provider-run",
            str(provider_run),
            "--artifact-root",
            str(run_root),
            "--execution-mode",
            execution_mode,
            "--json",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result.stdout or json.dumps({"ok": False, "errors": [result.stderr]}, indent=2) + "\n")
    if result.stderr:
        (run_root / "logs/provider-closeout.stderr.log").write_text(result.stderr)
    return result.returncode


def run_local(args: argparse.Namespace) -> dict[str, Any]:
    root = args.repo_root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    manifest = load_json(manifest_path)
    profile = manifest.get("execution_profile")
    if profile not in SUPPORTED_ENTRYPOINTS:
        return {
            "ok": False,
            "errors": [f"unsupported local provider execution_profile: {profile}"],
        }

    run_id = args.run_id or str(manifest.get("run_id") or profile)
    volume_root = args.out.resolve()
    run_root = volume_root / "runs" / run_id
    if run_root.exists():
        shutil.rmtree(run_root)
    stage_contract = manifest.get("stage_contract")
    stage_contract_path = root / stage_contract if isinstance(stage_contract, str) else Path("")
    entrypoint = root / SUPPORTED_ENTRYPOINTS[profile]

    env = os.environ.copy()
    env.update(
        {
            "CRYOCORE_RUN_ID": run_id,
            "CRYOCORE_VOLUME_ROOT": str(volume_root),
            "CRYOCORE_REPO_ROOT": str(root),
            "CRYOCORE_LAUNCH_MANIFEST": str(manifest_path),
            "CRYOCORE_STAGE_CONTRACT": str(stage_contract_path),
            "CRYOCORE_EXECUTION_MODE": args.execution_mode,
        }
    )
    if args.mock_gpu:
        env["CRYOCORE_MOCK_GPU"] = "1"

    command = ["bash", str(entrypoint)]
    started_at = now()
    start = time.time()
    result = subprocess.run(command, cwd=root, env=env, text=True, capture_output=True, check=False)
    elapsed = time.time() - start
    finished_at = now()

    (run_root / "logs").mkdir(parents=True, exist_ok=True)
    (run_root / "logs/provider-runner.stdout.log").write_text(result.stdout)
    (run_root / "logs/provider-runner.stderr.log").write_text(result.stderr)
    write_runner_artifacts(run_root, command, result.returncode, started_at, finished_at)
    provider_run = run_root / "provider-run.json"
    write_json(provider_run, provider_run_payload(run_id, manifest_path, result.returncode, started_at, finished_at, elapsed))
    closeout_rc = run_closeout(root, run_root, provider_run, args.execution_mode)
    write_json(run_root / "artifact_hashes.json", {"sha256": relative_artifact_hashes(run_root)})

    return {
        "ok": result.returncode == 0 and closeout_rc == 0,
        "check_type": "cryocore_provider_runner",
        "provider": "local",
        "execution_profile": profile,
        "execution_mode": args.execution_mode,
        "run_id": run_id,
        "run_root": str(run_root),
        "provider_run": str(provider_run),
        "entrypoint_returncode": result.returncode,
        "closeout_returncode": closeout_rc,
        "errors": [] if result.returncode == 0 and closeout_rc == 0 else ["local provider runner did not close cleanly"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path, default=Path("runpod/launch-manifests/no-download-smoke.json"))
    parser.add_argument("--out", type=Path, default=Path(".runtime/provider-local"))
    parser.add_argument("--run-id")
    parser.add_argument("--execution-mode", choices=["prep", "real"], default="prep")
    parser.add_argument("--mock-gpu", action="store_true", default=True)
    parser.add_argument("--no-mock-gpu", action="store_false", dest="mock_gpu")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = run_local(args)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"ok: {summary['ok']}")
        print(f"run_root: {summary.get('run_root')}")
        for error in summary.get("errors", []):
            print(f"error: {error}")
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
