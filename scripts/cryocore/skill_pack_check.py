#!/usr/bin/env python3
"""Validate the public CryoCore skill pack index and metadata."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
REQUIRED_METADATA_KEYS = {
    "schema_version",
    "id",
    "title",
    "description",
    "entrypoint",
    "read_first",
    "validators",
    "forbidden_actions",
    "output_contract",
}


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def resolves_from(base: Path, path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else base / candidate


def load_json_compatible_yaml(path: Path) -> Any:
    return json.loads(path.read_text())


def skill_name(skill_text: str) -> str | None:
    match = re.search(r"^name:\s*([A-Za-z0-9_-]+)\s*$", skill_text, flags=re.MULTILINE)
    return match.group(1) if match else None


def check_skill_pack(index_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    index_file = resolve(index_path)
    try:
        index = load_json_compatible_yaml(index_file)
    except Exception as exc:
        return {
            "ok": False,
            "check_type": "cryocore_skill_pack_check",
            "index": str(index_file),
            "skill_count": 0,
            "errors": [f"could not load index: {type(exc).__name__}: {exc}"],
            "warnings": [],
        }

    if not isinstance(index, dict):
        errors.append("index must be an object")
        skills = []
    else:
        if index.get("schema_version") != 1:
            errors.append("schema_version must be 1")
        skills = index.get("skills", [])
        if not isinstance(skills, list) or not skills:
            errors.append("skills must be a non-empty list")
            skills = []

    seen: set[str] = set()
    primary_count = 0
    checked: list[dict[str, Any]] = []
    actual_skill_paths = {path.relative_to(REPO_ROOT).as_posix() for path in (REPO_ROOT / "skills").glob("*/SKILL.md")}
    indexed_paths: set[str] = set()

    for item in skills:
        if not isinstance(item, dict):
            errors.append("each skills entry must be an object")
            continue
        skill_id = str(item.get("id") or "")
        path_value = str(item.get("path") or "")
        metadata_value = str(item.get("agent_metadata") or "")
        if not skill_id:
            errors.append("skill entry missing id")
            continue
        if skill_id in seen:
            errors.append(f"duplicate skill id: {skill_id}")
        seen.add(skill_id)
        if item.get("primary") is True:
            primary_count += 1
        skill_path = resolve(Path(path_value))
        metadata_path = resolve(Path(metadata_value))
        indexed_paths.add(path_value)
        entry = {
            "id": skill_id,
            "path": path_value,
            "agent_metadata": metadata_value,
            "skill_exists": skill_path.exists(),
            "metadata_exists": metadata_path.exists(),
        }
        if not skill_path.exists():
            errors.append(f"{skill_id}: SKILL.md missing: {path_value}")
        else:
            name = skill_name(skill_path.read_text())
            entry["skill_name"] = name
            if name != skill_id:
                errors.append(f"{skill_id}: SKILL.md name mismatch: {name!r}")
        if not metadata_path.exists():
            errors.append(f"{skill_id}: agent metadata missing: {metadata_value}")
        else:
            try:
                metadata = load_json_compatible_yaml(metadata_path)
            except Exception as exc:
                errors.append(f"{skill_id}: metadata load failed: {type(exc).__name__}: {exc}")
                metadata = {}
            if not isinstance(metadata, dict):
                errors.append(f"{skill_id}: metadata must be an object")
                metadata = {}
            missing = sorted(REQUIRED_METADATA_KEYS - set(metadata))
            if missing:
                errors.append(f"{skill_id}: metadata missing keys: {', '.join(missing)}")
            if metadata.get("id") != skill_id:
                errors.append(f"{skill_id}: metadata id mismatch: {metadata.get('id')!r}")
            entrypoint = metadata.get("entrypoint")
            if not isinstance(entrypoint, str) or resolves_from(skill_path.parent, entrypoint).resolve() != skill_path.resolve():
                errors.append(f"{skill_id}: metadata entrypoint must resolve to index path")
            for list_key in ["read_first", "validators", "forbidden_actions"]:
                if not isinstance(metadata.get(list_key), list) or not metadata.get(list_key):
                    errors.append(f"{skill_id}: metadata {list_key} must be a non-empty list")
            for doc in metadata.get("read_first", []) if isinstance(metadata.get("read_first"), list) else []:
                if not isinstance(doc, str):
                    continue
                repo_candidate = resolve(Path(doc))
                skill_candidate = resolves_from(skill_path.parent, doc)
                if not repo_candidate.exists() and not skill_candidate.exists():
                    errors.append(f"{skill_id}: read_first path missing: {doc}")
        checked.append(entry)

    missing_from_index = sorted(actual_skill_paths - indexed_paths)
    if missing_from_index:
        errors.append("skill directories missing from index: " + ", ".join(missing_from_index))
    if primary_count != 1:
        errors.append(f"exactly one primary skill is required, found {primary_count}")
    if len(skills) < 2:
        warnings.append("skill pack has fewer than two skills")

    return {
        "ok": not errors,
        "check_type": "cryocore_skill_pack_check",
        "index": str(index_file),
        "skill_count": len(skills),
        "checked": checked,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=Path, default=Path("skills/index.yaml"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    summary = check_skill_pack(args.index)
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
