#!/usr/bin/env python3
"""Small stdlib JSON Schema subset checker for CryoCore contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def type_matches(instance: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(instance, dict)
    if expected == "array":
        return isinstance(instance, list)
    if expected == "string":
        return isinstance(instance, str)
    if expected == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if expected == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if expected == "boolean":
        return isinstance(instance, bool)
    if expected == "null":
        return instance is None
    return True


def validate(schema: dict[str, Any], instance: Any, path: str = "$") -> list[str]:
    errors: list[str] = []

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']!r}, got {instance!r}")

    expected_type = schema.get("type")
    if expected_type is not None:
        choices = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(type_matches(instance, choice) for choice in choices):
            errors.append(f"{path}: expected type {choices!r}, got {type(instance).__name__}")
            return errors

    any_of = schema.get("anyOf")
    if isinstance(any_of, list):
        branch_errors: list[str] = []
        matched = False
        for index, subschema in enumerate(any_of):
            if not isinstance(subschema, dict):
                continue
            candidate_errors = validate(subschema, instance, path)
            if not candidate_errors:
                matched = True
                break
            branch_errors.append(f"anyOf[{index}]: " + "; ".join(candidate_errors))
        if not matched:
            detail = " | ".join(branch_errors) if branch_errors else "no valid schemas"
            errors.append(f"{path}: does not match anyOf ({detail})")

    if isinstance(instance, str):
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(instance) < min_length:
            errors.append(f"{path}: string shorter than minLength {min_length}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if isinstance(minimum, (int, float)) and instance < minimum:
            errors.append(f"{path}: value {instance} < minimum {minimum}")
        if isinstance(maximum, (int, float)) and instance > maximum:
            errors.append(f"{path}: value {instance} > maximum {maximum}")

    if isinstance(instance, list):
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(instance) < min_items:
            errors.append(f"{path}: array shorter than minItems {min_items}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                errors.extend(validate(item_schema, item, f"{path}[{index}]"))

    if isinstance(instance, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if key not in instance:
                    errors.append(f"{path}: missing required key {key}")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, subschema in properties.items():
                if key in instance and isinstance(subschema, dict):
                    errors.extend(validate(subschema, instance[key], f"{path}.{key}"))
        additional = schema.get("additionalProperties", True)
        if isinstance(additional, dict):
            for key, value in instance.items():
                if key not in properties:
                    errors.extend(validate(additional, value, f"{path}.{key}"))
        elif additional is False:
            for key in instance:
                if key not in properties:
                    errors.append(f"{path}: additional property not allowed: {key}")

    return errors


def validate_file(schema_path: Path, instance_path: Path, *, jsonl: bool = False) -> dict[str, Any]:
    schema = load_json(schema_path)
    if jsonl:
        errors: list[str] = []
        count = 0
        for line_number, raw in enumerate(instance_path.read_text().splitlines(), start=1):
            if not raw.strip():
                continue
            count += 1
            try:
                instance = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: malformed JSON: {exc.msg}")
                continue
            errors.extend(validate(schema, instance, f"$[{line_number}]"))
    else:
        count = 1
        errors = validate(schema, load_json(instance_path))
    return {
        "ok": not errors,
        "check_type": "cryocore_schema_check",
        "schema": str(schema_path.resolve()),
        "instance": str(instance_path.resolve()),
        "jsonl": jsonl,
        "checked": count,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--jsonl", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = validate_file(args.schema, args.instance, jsonl=args.jsonl)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"ok: {summary['ok']}")
        for error in summary["errors"]:
            print(f"error: {error}")
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
