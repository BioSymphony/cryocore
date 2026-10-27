#!/usr/bin/env python3
"""Create a fresh MRC header derivative without changing scientific pixels.

Optional adapter: install mrcfile and numpy in a separate scientific environment.
Only the MAP identifier and density statistics may change. Native inputs remain
unchanged; a full mrcfile validation is required before publishing the copy.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import tempfile


ALLOWED_FIELDS = {
    "dmin_dmax_dmean": [76, 88],
    "map_identifier": [208, 212],
    "rms": [216, 220],
}


def digest(path: Path, offset: int = 0) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        handle.seek(offset)
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def identity(path: Path) -> dict:
    return {"path": str(path.resolve()), "bytes": path.stat().st_size,
            "sha256": digest(path)}


def changed_ranges(left: bytes, right: bytes) -> list[list[int]]:
    """Return half-open byte intervals; reject any unapproved header mutation."""
    if len(left) != 1024 or len(right) != 1024:
        raise ValueError("Expected two complete 1024-byte MRC headers")
    ranges: list[list[int]] = []
    for index, (a, b) in enumerate(zip(left, right)):
        if a == b:
            continue
        if not any(start <= index < stop for start, stop in ALLOWED_FIELDS.values()):
            raise ValueError(f"Unapproved header change at byte {index}")
        if ranges and ranges[-1][1] == index:
            ranges[-1][1] = index + 1
        else:
            ranges.append([index, index + 1])
    return ranges


def validation(mrcfile, path: Path) -> dict:
    stream = io.StringIO()
    passed = bool(mrcfile.validate(path, print_file=stream))
    return {"passed": passed, "messages": stream.getvalue()}


def normalize_mrc_header(input_path: Path, output_path: Path) -> dict:
    # Keep optional scientific packages out of ordinary workspace imports.
    import mrcfile
    import numpy as np

    input_path = Path(input_path).resolve(strict=True)
    output_path = Path(output_path).absolute()
    if output_path.resolve() == input_path:
        raise ValueError("Output must be a separate, fresh file")
    if output_path.exists() or output_path.is_symlink():
        raise FileExistsError(f"Output already exists: {output_path}")
    before = identity(input_path)
    with input_path.open("rb") as handle:
        original_header = handle.read(1024)
    original_tail = digest(input_path, 1024)
    native_validation = validation(mrcfile, input_path)
    with mrcfile.open(input_path, mode="r", permissive=False) as mrc:
        if mrc.data is None or not np.isfinite(mrc.data).all():
            raise ValueError("Input must contain finite density values")
        payload_offset = 1024 + int(mrc.header.nsymbt)
        dimensions = [int(mrc.header.nz), int(mrc.header.ny), int(mrc.header.nx)]
    payload_hash = digest(input_path, payload_offset)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".mrc-header-", suffix=".mrc", dir=output_path.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    created_output = False
    try:
        shutil.copyfile(input_path, temporary)
        with mrcfile.open(temporary, mode="r+", permissive=False) as mrc:
            mrc.header.map = b"MAP "
            mrc.update_header_stats()
        with temporary.open("rb") as handle:
            repaired_header = handle.read(1024)
        changes = changed_ranges(original_header, repaired_header)
        if temporary.stat().st_size != before["bytes"]:
            raise ValueError("Header repair changed file length")
        if digest(temporary, 1024) != original_tail:
            raise ValueError("Header repair changed extended header or pixel payload")
        repaired_validation = validation(mrcfile, temporary)
        if not repaired_validation["passed"]:
            raise ValueError("Derivative failed full MRC validation: "
                             + repaired_validation["messages"])
        if digest(input_path) != before["sha256"]:
            raise ValueError("Native input changed during header repair")
        # Exclusive creation also refuses a path created after the initial check.
        with output_path.open("xb") as target:
            created_output = True
            with temporary.open("rb") as source:
                shutil.copyfileobj(source, target)
        if digest(output_path) != digest(temporary):
            raise ValueError("Derivative changed during final copy")
        final_validation = validation(mrcfile, output_path)
        if not final_validation["passed"]:
            raise ValueError("Final derivative failed full MRC validation")
        if digest(input_path) != before["sha256"]:
            raise ValueError("Native input changed during final copy")
        with mrcfile.open(output_path, mode="r", permissive=False) as mrc:
            statistics = {key: float(mrc.header[key])
                          for key in ("dmin", "dmax", "dmean", "rms")}
        return {
            "schema_version": 1,
            "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "operation": "separate_MAP_and_density_statistics_header_derivative",
            "software": {"mrcfile": mrcfile.__version__, "numpy": np.__version__},
            "input": before, "output": identity(output_path),
            "input_sha256_after": digest(input_path),
            "native_input_unchanged": True,
            "shape_zyx": dimensions,
            "allowed_header_fields_half_open": ALLOWED_FIELDS,
            "changed_byte_ranges_half_open": changes,
            "all_bytes_outside_allowed_fields_identical": True,
            "bytes_from_1024_sha256": original_tail,
            "extended_header_and_pixel_payload_unchanged": True,
            "pixel_payload_offset": payload_offset,
            "input_pixel_payload_sha256": payload_hash,
            "output_pixel_payload_sha256": digest(output_path, payload_offset),
            "native_full_validation": native_validation,
            "derivative_full_validation": final_validation,
            "derivative_strict_open_accepted": True,
            "density_statistics": statistics,
            "claim_limit": "Header metadata repair only; no scientific pixels or sampling changed.",
        }
    except Exception:
        if created_output:
            output_path.unlink(missing_ok=True)
        raise
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if args.receipt.exists() or args.receipt.is_symlink():
        parser.error("Receipt must be a fresh file")
    if args.receipt.resolve() in (args.input.resolve(), args.output.resolve()):
        parser.error("Receipt must be separate from input and output")
    result = normalize_mrc_header(args.input, args.output)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open("x") as handle:
        json.dump(result, handle, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": result["output"], "receipt": str(args.receipt)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
