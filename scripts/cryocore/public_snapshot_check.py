#!/usr/bin/env python3
"""Check CryoCore public snapshot safety.

The public profile blocks secrets, heavyweight cryo-EM artifacts, local
workstation paths, private image references, and private execution markers.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
from pathlib import Path


DENIED_NAME_PATTERNS = [
    ".env",
    ".env.*",
    "env.sh",
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "*.lic",
    "*.license",
    "*license-acceptance*",
    "*license_acceptance*",
]

DENIED_EXTENSIONS = [
    ".mrc",
    ".mrc.gz",
    ".mrcs",
    ".mrcs.gz",
    ".map",
    ".map.gz",
    ".eer",
    ".tif",
    ".tiff",
    ".dm4",
    ".pdb",
    ".pdb.gz",
    ".cif",
    ".cif.gz",
    ".mmcif",
    ".mmcif.gz",
    ".bcif",
    ".fasta",
    ".fa",
    ".faa",
    ".fna",
    ".fastq",
    ".fastq.gz",
    ".fq",
    ".fq.gz",
    ".star",
    ".star.gz",
    ".cs",
    ".h5",
    ".hdf5",
    ".npy",
    ".npz",
    ".pt",
    ".pth",
    ".safetensors",
    ".ckpt",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".tar",
    ".tar.gz",
    ".tgz",
    ".zip",
]

SECRET_PATTERNS = [
    re.compile(("RUNPOD" + "_API_KEY") + r"\s*=", re.IGNORECASE),
    re.compile(("LINEAR" + "_API_KEY") + r"\s*=", re.IGNORECASE),
    re.compile(r"github_pat_[A-Za-z0-9_]+"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"lin_api_[A-Za-z0-9_]+"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY-----"),
]

# Operator-specific markers that point at this operator's private workshop.
# If a file in the public repo contains any of these strings, something
# escaped from the operator's private environment. The strings are split with
# string concatenation so this scanner's own source does not trip itself.
# Adopters of CryoCore should replace these with markers that match their own
# private workshop paths, image registries, and tool names.
PUBLIC_PRIVATE_MARKERS = [
    "/Users/" + "jacobvogan/",
    "autonomy" + "/bin",
    "ghcr.io/" + "jvogan",
    "private_github" + "_clone",
    "biosymphony" + "-runpod-bridge",
]

CONTENT_PATTERN_ALLOWLIST = {
    "scripts/cryocore/public_snapshot_check.py",
    "tests/test_cryocore_hardening.py",
}

PUBLIC_MARKER_ALLOWLIST: set[str] = set()

IGNORED_PARTS = {".git", ".runtime", ".pytest_cache", "__pycache__"}


def candidate_paths(root: Path) -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return [path for path in root.rglob("*") if path.is_file()]
    return [root / rel for rel in result.stdout.splitlines() if rel.strip()]


def repo_rel(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve()))


def is_ignored(rel: str) -> bool:
    return any(part in IGNORED_PARTS for part in Path(rel).parts)


def denied_extension(name: str) -> str | None:
    lower = name.lower()
    for suffix in DENIED_EXTENSIONS:
        if lower.endswith(suffix):
            return suffix
    return None


def read_text(path: Path) -> str | None:
    try:
        return path.read_text()
    except (UnicodeDecodeError, OSError):
        return None


def check_path(root: Path, path: Path, profile: str, max_file_bytes: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    rel = repo_rel(root, path)
    if is_ignored(rel) or not path.is_file():
        return errors, warnings

    name = path.name
    for pattern in DENIED_NAME_PATTERNS:
        if fnmatch.fnmatch(name, pattern):
            errors.append(f"{rel}: denied secret/license filename pattern {pattern}")
    extension = denied_extension(name)
    if extension:
        errors.append(f"{rel}: denied heavy/private artifact extension {extension}")

    size = path.stat().st_size
    if size > max_file_bytes:
        errors.append(f"{rel}: file exceeds max public/workshop size {size} > {max_file_bytes}")

    text = read_text(path)
    if text is None:
        return errors, warnings

    if rel not in CONTENT_PATTERN_ALLOWLIST:
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel}: secret-like content matched {pattern.pattern}")

    private_hits = [marker for marker in PUBLIC_PRIVATE_MARKERS if marker in text]
    if private_hits:
        message = f"{rel}: private/workshop markers present: {', '.join(private_hits)}"
        if profile == "public" and rel not in PUBLIC_MARKER_ALLOWLIST:
            errors.append(message)
        else:
            warnings.append(message)

    return errors, warnings


def run_check(root: Path, profile: str, max_file_bytes: int) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    checked = 0
    for path in candidate_paths(root):
        path_errors, path_warnings = check_path(root, path, profile, max_file_bytes)
        checked += 1
        errors.extend(path_errors)
        warnings.extend(path_warnings)
    return {
        "ok": not errors,
        "check_type": "cryocore_public_snapshot_check",
        "profile": profile,
        "repo_root": str(root.resolve()),
        "checked": checked,
        "max_file_bytes": max_file_bytes,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--profile", choices=["workshop", "public"], default="workshop")
    parser.add_argument("--max-file-bytes", type=int, default=2_000_000)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = run_check(args.repo_root.resolve(), args.profile, args.max_file_bytes)
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
