#!/usr/bin/env python3
"""Check CryoCore public snapshot safety.

The public profile blocks secrets, heavyweight cryo-EM artifacts, local
workstation paths, private image references, and private execution markers.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
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

# Generic markers that should not appear in a public snapshot. Patterns are
# kept operator-neutral so the public checker does not publish local usernames,
# private repo names, or machine-specific paths.
PUBLIC_PRIVATE_MARKERS = [
    "private-workshop" + "/bin",
    "ghcr.io/" + "private-org",
    "private_github" + "_clone",
    "private-cloud" + "-bridge",
    "runpod" + "-bridge",
]

PUBLIC_PRIVATE_PATTERNS = [
    ("macOS home path", re.compile(r"/Users/[A-Za-z0-9._-]+(?:/|$)")),
    ("Linux home path", re.compile(r"/home/[A-Za-z0-9._-]+(?:/|$)")),
    (
        "Windows home path",
        re.compile(r"\b[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9._-]+(?:[\\/]|$)", re.IGNORECASE),
    ),
]

INTERNAL_LEAKAGE_PATTERNS = [
    (
        "copied internal writing guidance",
        re.compile(r"(?im)^\s*(?:[#>*-]\s*)*(?:copied\s+)?internal\s+writing[- ](?:guidelines?|guidance)\b"),
    ),
    (
        "private deliberation header",
        re.compile(r"(?im)^\s*(?:[#>*-]\s*)*(?:private|internal)\s+deliberation\b"),
    ),
    (
        "hidden reasoning material",
        re.compile(r"(?i)\b(?:chain[- ]of[- ]thought|hidden\s+reasoning)\s+(?:notes?|transcript|content|instructions?)\b"),
    ),
]

PUBLIC_MARKER_ALLOWLIST: set[str] = set()

IGNORED_PARTS = {".git", ".runtime", ".pytest_cache", "__pycache__"}
PUBLIC_FORBIDDEN_ROOTS = {
    ".cryocore-memory",
    "internal",
    "logs",
    ".runtime",
    "artifacts",
    "outputs",
    "raw-data",
    "model-weights",
}


def _git_paths(root: Path, args: list[str]) -> list[str] | None:
    try:
        result = subprocess.run(
            ["git", "ls-files", *args, "-z"],
            cwd=root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return [os.fsdecode(raw) for raw in result.stdout.split(b"\0") if raw]


def _candidate_records(root: Path) -> list[tuple[Path, bool]]:
    listed = _git_paths(root, ["--cached", "--others", "--exclude-standard"])
    if listed is not None:
        tracked_paths = _git_paths(root, ["--cached"])
        tracked = set(tracked_paths or [])
        seen: set[str] = set()
        return [
            (root / rel, rel in tracked)
            for rel in listed
            if not (rel in seen or seen.add(rel))
        ]
    return [
        (path, False)
        for path in root.rglob("*")
        if path.is_file() or path.is_symlink()
    ]


def candidate_paths(root: Path) -> list[Path]:
    return [path for path, _tracked in _candidate_records(root)]


def repo_rel(root: Path, path: Path) -> str:
    root_abs = Path(os.path.abspath(os.fspath(root)))
    path_abs = Path(os.path.abspath(os.fspath(path)))
    return path_abs.relative_to(root_abs).as_posix()


def is_ignored(rel: str) -> bool:
    parts = Path(rel).parts
    return any(part in IGNORED_PARTS for part in parts) or (
        bool(parts) and parts[0] in PUBLIC_FORBIDDEN_ROOTS
    )


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


def _symlink_message(root: Path, path: Path, rel: str) -> str:
    try:
        target = os.readlink(path)
    except OSError:
        return f"{rel}: symlink could not be inspected and was not dereferenced"
    target_path = Path(target) if os.path.isabs(target) else path.parent / target
    target_abs = Path(os.path.abspath(os.fspath(target_path)))
    root_abs = Path(os.path.abspath(os.fspath(root)))
    try:
        target_abs.relative_to(root_abs)
    except ValueError:
        return f"{rel}: symlink target escapes repository and was not dereferenced"
    if not os.path.lexists(target_abs):
        return f"{rel}: dangling symlink was not dereferenced"
    return f"{rel}: symlink content was not scanned"


def _symlink_component(root: Path, rel: str) -> Path | None:
    current = Path(os.path.abspath(os.fspath(root)))
    for part in Path(rel).parts:
        current /= part
        if current.is_symlink():
            return current
    return None


def check_path(
    root: Path,
    path: Path,
    profile: str,
    max_file_bytes: int,
    *,
    tracked: bool | None = None,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        rel = repo_rel(root, path)
    except ValueError:
        return ["candidate path is outside repository and was not scanned"], warnings

    if tracked is None:
        tracked_paths = _git_paths(root, ["--cached"])
        tracked = tracked_paths is not None and rel in set(tracked_paths)
    if is_ignored(rel) and not tracked:
        return errors, warnings
    if is_ignored(rel) and tracked and profile == "public":
        errors.append(f"{rel}: tracked ignored path is not allowed in public profile")

    symlink = _symlink_component(root, rel)
    if symlink is not None:
        symlink_rel = repo_rel(root, symlink)
        message = _symlink_message(root, symlink, symlink_rel)
        if profile == "public":
            errors.append(message)
        else:
            warnings.append(message)
        return errors, warnings
    if not path.is_file():
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
        return errors, warnings

    text = read_text(path)
    if text is None:
        return errors, warnings

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{rel}: secret-like content matched {pattern.pattern}")
    for label, pattern in INTERNAL_LEAKAGE_PATTERNS:
        if pattern.search(text):
            message = f"{rel}: copied internal guidance marker: {label}"
            if profile == "public":
                errors.append(message)
            else:
                warnings.append(message)

    private_hits = [marker for marker in PUBLIC_PRIVATE_MARKERS if marker in text]
    private_hits.extend(label for label, pattern in PUBLIC_PRIVATE_PATTERNS if pattern.search(text))
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
    for path, tracked in _candidate_records(root):
        path_errors, path_warnings = check_path(
            root,
            path,
            profile,
            max_file_bytes,
            tracked=tracked,
        )
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
