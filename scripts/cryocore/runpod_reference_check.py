#!/usr/bin/env python3
"""Validate RunPod contracts and entrypoints reference files that exist.

This is a public-release hygiene check: resumable commands should not point to
private operator scripts or stale local-only paths.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
from pathlib import Path
from typing import Any


ENTRYPOINT_DIR_REF_RE = re.compile(r"\$\{ENTRYPOINT_DIR\}/([^\"'\s]+\.sh)")
SCRIPT_PATH_PREFIXES = ("runpod/entrypoints/", "scripts/cryocore/")
INTERPRETERS = {"bash", "sh", "python", "python3"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def collect_resume_commands(value: Any) -> list[str]:
    commands: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "resume_command" and isinstance(item, str):
                commands.append(item)
            else:
                commands.extend(collect_resume_commands(item))
    elif isinstance(value, list):
        for item in value:
            commands.extend(collect_resume_commands(item))
    return commands


def path_tokens(command: str) -> list[str]:
    try:
        tokens = shlex.split(command)
    except ValueError:
        return []
    paths: list[str] = []
    if len(tokens) >= 2 and tokens[0] in INTERPRETERS and "/" in tokens[1] and not tokens[1].startswith("/"):
        paths.append(tokens[1])
    for token in tokens:
        if token.startswith(SCRIPT_PATH_PREFIXES):
            paths.append(token)
    return sorted(set(paths))


def check_stage_contracts(root: Path, contracts_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    checked: list[str] = []
    for contract in sorted(contracts_dir.glob("*.json")):
        commands = collect_resume_commands(load_json(contract))
        for command in commands:
            for token in path_tokens(command):
                checked.append(f"{contract.relative_to(root)}::{token}")
                if not (root / token).exists():
                    errors.append(f"{contract.relative_to(root)}: resume_command references missing file {token}")
    return errors, checked


def check_entrypoints(root: Path, entrypoints_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    checked: list[str] = []
    for entrypoint in sorted(entrypoints_dir.glob("*.sh")):
        text = entrypoint.read_text()
        for match in ENTRYPOINT_DIR_REF_RE.finditer(text):
            rel = f"runpod/entrypoints/{match.group(1)}"
            checked.append(f"{entrypoint.relative_to(root)}::{rel}")
            if not (root / rel).exists():
                errors.append(f"{entrypoint.relative_to(root)}: ENTRYPOINT_DIR references missing file {rel}")
    return errors, checked


def run_check(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    checked: list[str] = []
    contract_errors, contract_checked = check_stage_contracts(root, root / "runpod" / "stage-contracts")
    entrypoint_errors, entrypoint_checked = check_entrypoints(root, root / "runpod" / "entrypoints")
    errors.extend(contract_errors)
    errors.extend(entrypoint_errors)
    checked.extend(contract_checked)
    checked.extend(entrypoint_checked)
    return {
        "ok": not errors,
        "check_type": "cryocore_runpod_reference_check",
        "repo_root": str(root.resolve()),
        "checked": len(checked),
        "references": checked,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = run_check(args.repo_root.resolve())
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"ok: {summary['ok']}")
        print(f"checked: {summary['checked']}")
        for error in summary["errors"]:
            print(f"error: {error}")
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
