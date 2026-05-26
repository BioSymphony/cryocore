#!/usr/bin/env python3
"""Validate a lightweight CryoCore goal brief."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED_HEADINGS = [
    "# CryoCore Goal Brief",
    "## Goal",
    "## Starting Inputs",
    "## Resource Mode",
    "## Desired Outputs",
    "## Boundaries",
    "## Agent Orchestration",
    "## Validation And Closeout",
    "## Open Questions",
]

RESOURCE_MODES = {
    "local_only",
    "public_metadata_network",
    "operator_gated_provider",
    "tracker_wave",
    "provider_closeout",
}

CHECKED_BOX_RE = re.compile(r"^\s*[-*]\s+\[[xX]\]\s+`?(?P<mode>[a-z0-9_-]+)`?")
ANGLE_PLACEHOLDER_RE = re.compile(r"<[^>\n]+>")
TEXT_PLACEHOLDER_RE = re.compile(r"\b(TBD|TODO|REPLACE_ME)\b", flags=re.IGNORECASE)
SECRET_MARKERS = [
    "RUNPOD" + "_API_KEY=",
    "OPENAI" + "_API_KEY=",
    "ANTHROPIC" + "_API_KEY=",
    "BEGIN PRIVATE KEY",
    "ghp_",
    "sk-",
    "hf_",
]


def selected_resource_modes(text: str) -> list[str]:
    modes: list[str] = []
    in_resource_section = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            in_resource_section = stripped == "## Resource Mode"
            continue
        if not in_resource_section:
            continue
        match = CHECKED_BOX_RE.match(line)
        if match:
            modes.append(match.group("mode"))
    return modes


def validate_goal_brief(path: Path, allow_placeholders: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not path.exists():
        return {
            "ok": False,
            "check_type": "cryocore_goal_brief_check",
            "path": str(path),
            "errors": [f"goal brief not found: {path}"],
            "warnings": [],
            "selected_resource_modes": [],
        }

    text = path.read_text()
    lines = {line.strip() for line in text.splitlines()}
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in lines]
    for heading in missing:
        errors.append(f"missing required heading: {heading}")

    selected_modes = selected_resource_modes(text)
    unknown_modes = sorted(set(selected_modes) - RESOURCE_MODES)
    for mode in unknown_modes:
        errors.append(f"unknown selected resource mode: {mode}")
    if not allow_placeholders and not selected_modes:
        errors.append("select at least one Resource Mode checkbox")

    placeholders = ANGLE_PLACEHOLDER_RE.findall(text) + TEXT_PLACEHOLDER_RE.findall(text)
    if placeholders and not allow_placeholders:
        errors.append(f"unresolved placeholders present: {len(placeholders)}")

    for marker in SECRET_MARKERS:
        if marker in text:
            errors.append(f"secret-like marker present: {marker}")

    if len(selected_modes) > 2:
        warnings.append("more than two resource modes selected; consider splitting the goal")

    return {
        "ok": not errors,
        "check_type": "cryocore_goal_brief_check",
        "path": str(path),
        "required_headings": REQUIRED_HEADINGS,
        "selected_resource_modes": selected_modes,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--allow-template", action="store_true", help="Allow placeholders in reusable templates")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = validate_goal_brief(args.path, allow_placeholders=args.allow_template)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"ok: {summary['ok']}")
        print("selected_resource_modes: " + ", ".join(summary["selected_resource_modes"]))
        for error in summary["errors"]:
            print(f"error: {error}")
        for warning in summary["warnings"]:
            print(f"warning: {warning}")
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
