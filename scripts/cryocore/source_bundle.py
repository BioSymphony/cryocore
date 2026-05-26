"""Deterministic inline source bundle helpers for bridge manifests."""

from __future__ import annotations

import base64
import gzip
import io
import tarfile
from pathlib import Path
from typing import Mapping


BUNDLE_MTIME = 0


def validate_bundle_name(name: str) -> None:
    path = Path(name)
    if path.is_absolute() or ".." in path.parts or not name:
        raise ValueError(f"unsafe bundle member path: {name}")


def encoded_source_bundle(files: Mapping[str, str]) -> str:
    """Return a reproducible base64-encoded tar.gz source bundle."""

    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", mtime=BUNDLE_MTIME) as gzip_file:
        with tarfile.open(fileobj=gzip_file, mode="w") as archive:
            for name, text in sorted(files.items()):
                validate_bundle_name(name)
                data = text.encode("utf-8")
                info = tarfile.TarInfo(name)
                info.mode = 0o644
                info.size = len(data)
                info.mtime = BUNDLE_MTIME
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""
                archive.addfile(info, io.BytesIO(data))
    return base64.b64encode(buffer.getvalue()).decode("ascii")
