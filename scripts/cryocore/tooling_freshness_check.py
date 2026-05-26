#!/usr/bin/env python3
"""Check that public tooling/license posture docs are recently reviewed."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


REVIEW_RE = re.compile(r"Last reviewed:\s*(?P<date>\d{4}-\d{2}-\d{2})")
TOOLWATCH_RE = re.compile(r"toolwatch-(?P<date>\d{4}-\d{2}-\d{2})\.md$")


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def tooling_review_date(path: Path) -> date | None:
    match = REVIEW_RE.search(path.read_text(errors="ignore"))
    return parse_date(match.group("date")) if match else None


def latest_toolwatch_date(docs_dir: Path) -> date | None:
    dates = []
    for path in docs_dir.glob("toolwatch-*.md"):
        match = TOOLWATCH_RE.match(path.name)
        if match:
            dates.append(parse_date(match.group("date")))
    return max(dates) if dates else None


def age_days(reviewed: date, today: date) -> int:
    return (today - reviewed).days


def run_check(root: Path, max_age_days: int, today: date | None = None) -> dict[str, Any]:
    today = today or datetime.now(timezone.utc).date()
    errors: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, Any]] = []

    tooling_path = root / "docs" / "tooling-and-licensing.md"
    tooling_date = tooling_review_date(tooling_path) if tooling_path.exists() else None
    if tooling_date is None:
        errors.append("docs/tooling-and-licensing.md must contain `Last reviewed: YYYY-MM-DD`")
    else:
        age = age_days(tooling_date, today)
        checks.append({"artifact": "docs/tooling-and-licensing.md", "reviewed": tooling_date.isoformat(), "age_days": age})
        if age < 0:
            errors.append("docs/tooling-and-licensing.md review date is in the future")
        elif age > max_age_days:
            errors.append(f"docs/tooling-and-licensing.md review is stale: {age} days > {max_age_days}")

    toolwatch_date = latest_toolwatch_date(root / "docs")
    if toolwatch_date is None:
        warnings.append("no docs/toolwatch-YYYY-MM-DD.md report found")
    else:
        age = age_days(toolwatch_date, today)
        checks.append({"artifact": "latest toolwatch report", "reviewed": toolwatch_date.isoformat(), "age_days": age})
        if age < 0:
            errors.append("latest toolwatch report date is in the future")
        elif age > max_age_days:
            errors.append(f"latest toolwatch report is stale: {age} days > {max_age_days}")

    return {
        "ok": not errors,
        "check_type": "cryocore_tooling_freshness_check",
        "repo_root": str(root.resolve()),
        "max_age_days": max_age_days,
        "today": today.isoformat(),
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--max-age-days", type=int, default=120)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = run_check(args.repo_root.resolve(), args.max_age_days)
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
