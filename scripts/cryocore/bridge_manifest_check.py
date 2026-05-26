#!/usr/bin/env python3
"""Check generated bridge manifests match their checked-in files."""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

BUILDERS = [
    {
        "builder": "scripts/cryocore/build_t2r14_bridge_manifest.py",
        "manifest": "runpod/bridge-manifests/t2r14-open-dossier.json",
    },
    {
        "builder": "scripts/cryocore/build_poltheta_bridge_manifest.py",
        "manifest": "runpod/bridge-manifests/poltheta-map-model-dossier.json",
    },
    {
        "builder": "scripts/cryocore/build_structure_jury_bridge_manifest.py",
        "manifest": "runpod/bridge-manifests/structure-jury-dual-dossier.json",
    },
]


def run_builder(root: Path, builder: str, out: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, builder, "--out", str(out)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0, result.stdout + result.stderr


def check_manifests(root: Path, *, write: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as temp:
        temp_root = Path(temp)
        for item in BUILDERS:
            builder = item["builder"]
            manifest = item["manifest"]
            expected = root / manifest
            generated = temp_root / Path(manifest).name
            ok, output = run_builder(root, builder, generated)
            result: dict[str, Any] = {
                "builder": builder,
                "manifest": manifest,
                "generated": str(generated),
                "builder_ok": ok,
                "fresh": False,
            }
            if not ok:
                message = f"{builder} failed"
                errors.append(message)
                result["error"] = message
                result["builder_output"] = output
                results.append(result)
                continue
            if not expected.exists():
                errors.append(f"{manifest} is missing")
                result["error"] = "manifest missing"
                results.append(result)
                continue
            fresh = filecmp.cmp(generated, expected, shallow=False)
            result["fresh"] = fresh
            if not fresh and write:
                shutil.copyfile(generated, expected)
                result["written"] = True
                result["fresh"] = True
            elif not fresh:
                errors.append(f"{manifest} is stale; run {builder}")
            results.append(result)
    return {
        "ok": not errors,
        "check_type": "cryocore_bridge_manifest_check",
        "repo_root": str(root.resolve()),
        "checked": len(results),
        "results": results,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--write", action="store_true", help="Update stale checked-in manifests")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = check_manifests(args.repo_root.resolve(), write=args.write)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"ok: {summary['ok']}")
        for error in summary["errors"]:
            print(f"error: {error}")
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
