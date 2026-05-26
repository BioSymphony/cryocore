#!/usr/bin/env python3
"""Check local Markdown links and images."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote


MARKDOWN_LINK_RE = re.compile(r"(!?)\[[^\]]*\]\(([^)\s]+(?:\s+\"[^\"]*\")?)\)")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
DEFAULT_DIRS = ["README.md", "FAQ.md", "ROADMAP.md", "docs", "examples", "skills", "templates", "demos"]
LOCAL_PATH_PREFIXES = (
    ".github/",
    "campaigns/",
    "containers/",
    "demos/",
    "docs/",
    "examples/",
    "modules/",
    "references/",
    "runpod/",
    "scripts/",
    "skills/",
    "templates/",
    "tests/",
)
ROOT_FILE_NAMES = {
    "AGENTS.md",
    "BIOSAFETY.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "FAQ.md",
    "LICENSE",
    "Makefile",
    "NON_CLAIMS.md",
    "NOTICE.md",
    "PUBLIC_RELEASE.md",
    "README.md",
    "ROADMAP.md",
    "SECURITY.md",
    "SUPPORT.md",
    "pyproject.toml",
    "requirements-dev.txt",
}


def strip_code_fences(text: str) -> str:
    lines = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            lines.append("")
            continue
        lines.append("" if in_fence else line)
    return "\n".join(lines)


def markdown_files(root: Path, paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for item in paths:
        path = root / item
        if path.is_file() and path.suffix.lower() == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
    return sorted(set(files))


def normalize_target(target: str) -> str:
    target = target.strip()
    if " " in target and target.endswith('"'):
        target = target.split(" ", 1)[0]
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split("#", 1)[0]
    target = target.split("?", 1)[0]
    return unquote(target)


def is_external_or_anchor(target: str) -> bool:
    return not target or target.startswith("#") or SCHEME_RE.match(target) is not None


def looks_like_local_path(target: str) -> bool:
    if any(marker in target for marker in ["YYYY", "<", ">"]):
        return False
    if any(char in target for char in "*{}$"):
        return False
    if " " in target or target.startswith("-"):
        return False
    if target in ROOT_FILE_NAMES:
        return True
    return target.startswith(LOCAL_PATH_PREFIXES)


def target_errors(root: Path, path: Path, raw_target: str, label: str) -> list[str]:
    errors: list[str] = []
    target = normalize_target(raw_target)
    if is_external_or_anchor(target):
        return errors
    candidate = (path.parent / target).resolve()
    if path.parent == root or target.startswith(LOCAL_PATH_PREFIXES) or target in ROOT_FILE_NAMES:
        candidate = (root / target).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{path.relative_to(root)}: {label} escapes repo: {raw_target}")
        return errors
    if not candidate.exists():
        errors.append(f"{path.relative_to(root)}: missing {label} target: {raw_target}")
    return errors


def check_file(root: Path, path: Path) -> list[str]:
    errors: list[str] = []
    text = strip_code_fences(path.read_text(errors="ignore"))
    for match in MARKDOWN_LINK_RE.finditer(text):
        errors.extend(target_errors(root, path, match.group(2), "local link"))
    for match in BACKTICK_RE.finditer(text):
        raw_target = match.group(1)
        if looks_like_local_path(raw_target):
            errors.extend(target_errors(root, path, raw_target, "backticked path"))
    return errors


def run_check(root: Path, paths: list[str]) -> dict[str, Any]:
    files = markdown_files(root, paths)
    errors: list[str] = []
    for path in files:
        errors.extend(check_file(root, path))
    return {
        "ok": not errors,
        "check_type": "cryocore_docs_link_check",
        "repo_root": str(root.resolve()),
        "checked": len(files),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--path", action="append", dest="paths", help="File or directory to scan; repeatable")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = run_check(args.repo_root.resolve(), args.paths or DEFAULT_DIRS)
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
