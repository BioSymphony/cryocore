#!/usr/bin/env python3
"""Lightweight CryoCore repo preflight."""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
from pathlib import Path


FORBIDDEN_PATTERNS = [
    "*.mrc",
    "*.mrc.gz",
    "*.mrcs",
    "*.mrcs.gz",
    "*.eer",
    "*.tif",
    "*.tiff",
    "*.dm4",
    "*.map",
    "*.map.gz",
    "*.rec",
    "*.st",
    "*.ali",
    "*.rawtlt",
    "*.mdoc",
    "*.pdb",
    "*.pdb.gz",
    "*.cif",
    "*.cif.gz",
    "*.mmcif",
    "*.mmcif.gz",
    "*.bcif",
    "*.fasta",
    "*.fa",
    "*.faa",
    "*.fna",
    "*.fastq",
    "*.fastq.gz",
    "*.fq",
    "*.fq.gz",
    "*.star",
    "*.star.gz",
    "*.cs",
    "*.h5",
    "*.hdf5",
    "*.npy",
    "*.npz",
    "*.pt",
    "*.pth",
    "*.safetensors",
    "*.ckpt",
    "*.sqlite",
    "*.sqlite3",
    "*.db",
    ".env",
    ".env.*",
    "env.sh",
    "*.pem",
    "*.key",
    "*.lic",
]

REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "Makefile",
    "campaigns",
    "demos",
    "demos/t2r14-open-dossier/README.md",
    "demos/poltheta-map-model-dossier/README.md",
    "demos/structure-jury-dual-dossier/README.md",
    "docs",
    "docs/split-evaluation.md",
    "docs/move-duplicate-map.md",
    "docs/tooling-and-licensing.md",
    "docs/compute-backends.md",
    "examples/no-download-smoke/manifest.json",
    "modules/image-modules/cryo-core.v1.json",
    "modules/image-modules/model-build.v1.json",
    "modules/lane-modules/raw-to-map.v1.json",
    "modules/lane-modules/map-to-model.v1.json",
    "modules/lane-modules/figure-dossier.v1.json",
    "modules/provider-profiles/runpod/pod-no-download.v1.json",
    "references/software-registry.yaml",
    "modules/schemas/workflow-run.v1.schema.json",
    "modules/schemas/container-provenance.v1.schema.json",
    "modules/schemas/map-model-fit.v1.schema.json",
    "modules/schemas/figure-manifest.v1.schema.json",
    "scripts/cryocore/software_registry_check.py",
    "scripts/cryocore/public_snapshot_check.py",
    "scripts/cryocore/schema_check.py",
    "scripts/cryocore/runpod_launch_request.py",
    "templates/linear-issue.md",
    "templates/symphony-cryocore.WORKFLOW.md",
]


def is_ignored_area(path: Path) -> bool:
    ignored = {".git", ".runtime", "artifacts", "outputs", "raw-data", "model-weights", "__pycache__"}
    return any(part in ignored for part in path.parts)


def candidate_paths(root: Path) -> list[Path]:
    """Return tracked plus nonignored untracked files when inside a git repo."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return [
            path
            for path in root.rglob("*")
            if path.is_file() and not is_ignored_area(path.relative_to(root))
        ]
    return [root / rel for rel in result.stdout.splitlines() if rel.strip()]


def json_files(root: Path) -> list[str]:
    bad: list[str] = []
    for path in candidate_paths(root):
        rel = path.relative_to(root)
        if is_ignored_area(rel) or path.suffix != ".json":
            continue
        try:
            json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            bad.append(f"{rel}: {exc}")
    return bad


def text_hygiene_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for path in candidate_paths(root):
        rel = path.relative_to(root)
        if is_ignored_area(rel) or not path.is_file():
            continue
        try:
            lines = path.read_text().splitlines()
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(lines, start=1):
            if line.endswith((" ", "\t")):
                errors.append(f"{rel}:{index}: trailing whitespace")
            if line.startswith("<<<<<<< ") or line == "=======" or line.startswith(">>>>>>> "):
                errors.append(f"{rel}:{index}: merge conflict marker")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="CryoCore repo root")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    missing = [rel for rel in REQUIRED_PATHS if not (root / rel).exists()]
    forbidden = []

    for path in candidate_paths(root):
        rel = path.relative_to(root)
        if is_ignored_area(rel) or not path.is_file():
            continue
        if any(fnmatch.fnmatch(path.name, pattern) for pattern in FORBIDDEN_PATTERNS):
            forbidden.append(str(rel))

    invalid_json = json_files(root)
    text_hygiene = text_hygiene_errors(root)
    ok = not missing and not forbidden and not invalid_json and not text_hygiene
    summary = {
        "ok": ok,
        "repo_root": str(root),
        "missing_required_paths": missing,
        "forbidden_tracked_candidate_files": forbidden,
        "invalid_json": invalid_json,
        "text_hygiene_errors": text_hygiene,
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"ok: {ok}")
        if missing:
            print("missing required paths:")
            for item in missing:
                print(f"  - {item}")
        if forbidden:
            print("forbidden file candidates:")
            for item in forbidden:
                print(f"  - {item}")
        if text_hygiene:
            print("text hygiene errors:")
            for item in text_hygiene:
                print(f"  - {item}")
        if invalid_json:
            print("invalid json:")
            for item in invalid_json:
                print(f"  - {item}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
