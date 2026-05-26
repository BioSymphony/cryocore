#!/usr/bin/env python3
"""Generate a trusted-after-run RunPod launch request without launching pods."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from runpod_launch_preflight import preflight
except ModuleNotFoundError:
    from scripts.cryocore.runpod_launch_preflight import preflight


TRUTHY = {"1", "true", "yes", "y", "approved", "authorized"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def parse_operator_gate(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"present": False, "authorized": False, "errors": ["operator gate record missing"]}
    if not path.exists():
        return {"present": False, "authorized": False, "errors": [f"operator gate record not found: {path}"]}
    if path.suffix == ".json":
        payload = load_json(path)
        authorized = payload.get("authorized") is True or str(payload.get("explicit_authorization", "")).lower() in TRUTHY
        return {"present": True, "authorized": authorized, "record": str(path.resolve()), "errors": [] if authorized else ["operator gate is not authorized"]}
    fields: dict[str, str] = {}
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped.startswith("- ") or ":" not in stripped:
            continue
        key, value = stripped[2:].split(":", 1)
        fields[key.strip().lower().replace(" ", "_")] = value.strip().strip("`")
    explicit = fields.get("explicit_authorization", "")
    authorized = explicit.lower() in TRUTHY
    errors = [] if authorized else ["operator gate explicit authorization is not truthy"]
    return {"present": True, "authorized": authorized, "record": str(path.resolve()), "fields": fields, "errors": errors}


def build_request(
    manifest_path: Path,
    issue: str,
    max_spend_usd: float,
    operator_gate: Path | None,
    execution_mode: str,
) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    readiness = preflight(manifest_path, execution_ready=execution_mode == "real")
    gate = parse_operator_gate(operator_gate)
    errors: list[str] = []
    if readiness.get("manifest_check", {}).get("ok") is not True:
        errors.append("launch manifest check failed")
    if execution_mode == "real":
        errors.extend(readiness.get("blockers", []))
    if execution_mode == "real":
        errors.extend(gate["errors"])
        if max_spend_usd <= 0:
            errors.append("real launch request requires max_spend_usd > 0")
    stage_contract = manifest.get("stage_contract")
    if not isinstance(stage_contract, str) or not (manifest_path.resolve().parents[2] / stage_contract).exists():
        errors.append("stage contract is missing from the repo checkout")
    return {
        "ok": not errors,
        "schema_version": 1,
        "request_type": "cryocore_trusted_runpod_launch_request",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "issue": issue,
        "manifest_path": str(manifest_path),
        "manifest_id": manifest.get("manifest_id"),
        "run_id": manifest.get("run_id"),
        "provider": manifest.get("provider"),
        "execution_profile": manifest.get("execution_profile"),
        "requested_action": "trusted_after_run_create_verify_cleanup",
        "claim_level": "remote_artifact_execution_only",
        "max_spend_usd": max_spend_usd,
        "execution_mode": execution_mode,
        "operator_gate": gate,
        "readiness": readiness,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--issue", required=True)
    parser.add_argument("--max-spend-usd", type=float, required=True)
    parser.add_argument("--operator-gate-record", type=Path)
    parser.add_argument("--execution-mode", choices=["prep", "real"], default="real")
    parser.add_argument("--out", type=Path, default=Path(".runtime/runpod-launch-request.json"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = build_request(
        manifest_path=args.manifest,
        issue=args.issue,
        max_spend_usd=args.max_spend_usd,
        operator_gate=args.operator_gate_record,
        execution_mode=args.execution_mode,
    )
    if summary["ok"]:
        write_json(args.out, summary)
        summary["request_path"] = str(args.out.resolve())
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"ok: {summary['ok']}")
        for error in summary["errors"]:
            print(f"error: {error}")
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
