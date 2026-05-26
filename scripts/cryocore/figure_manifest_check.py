#!/usr/bin/env python3
"""Validate CryoCore figure manifest files and rendered lightweight outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def is_nonblank_render(path: Path) -> bool:
    if not path.exists() or not path.is_file() or path.stat().st_size <= 20:
        return False
    sample = path.read_text(errors="ignore")[:4096].lower()
    if path.suffix.lower() == ".svg":
        return "<svg" in sample and "</svg" in sample
    if path.suffix.lower() in {".html", ".htm"}:
        return "<html" in sample or "<!doctype html" in sample
    return True


def missing_value(value: Any) -> bool:
    return value is None or value == "" or value == []


def check_manifest(manifest_path: Path, artifact_root: Path) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    errors: list[str] = []
    warnings: list[str] = []
    figures = manifest.get("figures")
    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not isinstance(figures, list) or not figures:
        errors.append("figures must be a non-empty list")
        figures = []
    for index, figure in enumerate(figures):
        if not isinstance(figure, dict):
            errors.append(f"figures[{index}] must be an object")
            continue
        figure_id = figure.get("figure_id")
        rel_path = figure.get("path")
        for key in ["figure_id", "path", "caption", "renderer", "source_accessions", "software_versions", "caveats"]:
            if key not in figure or missing_value(figure.get(key)):
                errors.append(f"figure {figure_id or index} missing {key}")
        if not isinstance(figure.get("source_accessions"), list):
            errors.append(f"figure {figure_id or index} source_accessions must be a list")
        if not isinstance(figure.get("software_versions"), dict):
            errors.append(f"figure {figure_id or index} software_versions must be an object")
        if rel_path:
            output = artifact_root / str(rel_path)
            if not is_nonblank_render(output):
                errors.append(f"figure {figure_id or index} output is missing, empty, or not a recognized render: {rel_path}")
        if figure.get("contour_levels") in {None, ""}:
            warnings.append(f"figure {figure_id or index} does not record contour_levels")
    return {
        "ok": not errors,
        "check_type": "cryocore_figure_manifest_check",
        "manifest": str(manifest_path.resolve()),
        "artifact_root": str(artifact_root.resolve()),
        "figure_count": len(figures),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = check_manifest(args.manifest, args.artifact_root)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"ok: {summary['ok']}")
        for warning in summary["warnings"]:
            print(f"warning: {warning}")
        for error in summary["errors"]:
            print(f"error: {error}")
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
