#!/usr/bin/env python3
"""Run pinned CZI tools on hash-bound experimental inputs and retain native evidence.

Input schema: {tool, binary, expected_version, source_commit, items, parameters}.
File identities are {path, sha256}; each item has id, input and reference.
Motion parameters: input_flag, gain, gain_rotation, gain_flip, gain_inverse,
patch, group, throw, trunc, ftbin, pixel_size_angstrom, voltage_kv,
frame_dose_e_per_a2, initial_dose_e_per_a2, iterations, tolerance, bfactor.
CTF parameters: pixel_size_angstrom, voltage_kv, cs_mm, amplitude_contrast,
tile_size, defocus_center_range_angstrom, ast_ratio_center_range,
ast_angle_center_range_deg, extra_phase_center_range_deg.
Each reference has identity, metadata, and differences. CTF reference also has
min_defocus_angstrom and max_defocus_angstrom. Metadata must match CTF parameters
for pixel size, voltage, Cs, amplitude contrast, and tile size.
"""
import argparse
import hashlib
import json
import math
import re
import struct
import subprocess
import sys
from pathlib import Path

COMMITS = {"motioncor3": "dd8b6831ae66ef016fb7ef3b9b6172f8b56c79aa", "gctffind": "b291ddfc9a44c3bb9a9f597358c3066808eb970a"}
VERSIONS = {"motioncor3": "MotionCor3 version 1.2.4", "gctffind": "GCtfFind version 1.2.5"}
CTF_META = ("pixel_size_angstrom", "voltage_kv", "cs_mm", "amplitude_contrast", "tile_size")


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def identity(spec):
    p = Path(spec["path"]).resolve(strict=True)
    if not p.is_file() or not re.fullmatch(r"[0-9a-f]{64}", spec["sha256"]):
        raise ValueError("Invalid file identity")
    actual = digest(p)
    if actual != spec["sha256"]:
        raise ValueError(f"SHA256 mismatch: {p}")
    return {"path": str(p), "sha256": actual, "bytes": p.stat().st_size}


def dimensions(path):
    p = Path(path)
    if p.suffix.lower() in (".tif", ".tiff"):
        import tifffile
        with tifffile.TiffFile(p) as tf:
            shape = tf.series[0].shape
            return {"shape": list(shape), "axes": tf.series[0].axes}
    with p.open("rb") as f:
        header = f.read(1024)
    if len(header) != 1024 or header[208:212] not in (b"MAP ", b"MAP\x00"):
        raise ValueError(f"Invalid MRC header: {p}")
    nx, ny, nz, mode = struct.unpack_from("<4i", header)
    if min(nx, ny, nz) <= 0 or mode not in (0, 1, 2, 6, 12):
        raise ValueError(f"Unsupported MRC dimensions/mode: {p}")
    nsymbt = struct.unpack_from("<i", header, 92)[0]
    sizes = {0: 1, 1: 2, 2: 4, 6: 2, 12: 2}
    if nsymbt < 0 or p.stat().st_size < 1024 + nsymbt + nx * ny * nz * sizes[mode]:
        raise ValueError(f"Truncated MRC data: {p}")
    return {"shape": [nz, ny, nx], "axes": "ZYX", "mrc_mode": mode}


def validate_mrc_pixels(path):
    info = dimensions(path)
    mode = info["mrc_mode"]
    fmt = {0: "b", 1: "h", 2: "f", 6: "H", 12: "e"}[mode]
    item_bytes = struct.calcsize("<" + fmt)
    count = math.prod(info["shape"])
    low, high = math.inf, -math.inf
    with open(path, "rb") as f:
        header = f.read(1024)
        f.seek(1024 + struct.unpack_from("<i", header, 92)[0])
        remaining = count
        while remaining:
            n = min(remaining, 262144)
            data = f.read(n * item_bytes)
            if len(data) != n * item_bytes:
                raise ValueError("Truncated MRC payload")
            for (value,) in struct.iter_unpack("<" + fmt, data):
                if not math.isfinite(value):
                    raise ValueError("Non-finite MRC pixels")
                low, high = min(low, value), max(high, value)
            remaining -= n
    return {**info, "finite": True, "minimum": low, "maximum": high}


def pair(value, key):
    if not isinstance(value, list) or len(value) != 2 or any(not isinstance(x, (int, float)) or not math.isfinite(x) for x in value):
        raise ValueError(f"{key} requires two finite numbers")
    return [str(x) for x in value]


def command(tool, binary, input_path, out, p):
    if tool == "gctffind":
        args = [binary, "-InMrc", input_path, "-OutDir", str(out), "-Serial", "0", "-Gpu", "0"]
        for key, flag in (("pixel_size_angstrom", "-PixSize"), ("voltage_kv", "-kV"), ("cs_mm", "-Cs"), ("amplitude_contrast", "-AmpContrast"), ("tile_size", "-TileSize")):
            args += [flag, str(p[key])]
        for key, flag in (("defocus_center_range_angstrom", "-Defocus"), ("ast_ratio_center_range", "-AstRatio"), ("ast_angle_center_range_deg", "-AstAngle"), ("extra_phase_center_range_deg", "-ExtPhase")):
            args += [flag] + pair(p[key], key)
        return args
    if p["input_flag"] not in ("-InTiff", "-InMrc", "-InEer"):
        raise ValueError("Unsupported movie input flag")
    args = [binary, p["input_flag"], input_path, "-OutMrc", str(out / "corrected.mrc"), "-OutAln", str(out), "-LogDir", str(out), "-Gpu", "0", "-Serial", "0", "-Align", "1", "-Cs", "0"]
    gain = p["gain"]
    if gain is not None:
        args += ["-Gain", identity(gain)["path"]]
    for key, flag in (("gain_rotation", "-RotGain"), ("gain_flip", "-FlipGain"), ("gain_inverse", "-InvGain"), ("throw", "-Throw"), ("trunc", "-Trunc"), ("ftbin", "-FtBin"), ("pixel_size_angstrom", "-PixSize"), ("voltage_kv", "-kV"), ("frame_dose_e_per_a2", "-FmDose"), ("initial_dose_e_per_a2", "-InitDose"), ("iterations", "-Iter"), ("tolerance", "-Tol"), ("bfactor", "-Bft")):
        args += [flag, str(p[key])]
    for key, flag in (("patch", "-Patch"), ("group", "-Group")):
        args += [flag] + pair(p[key], key)
    return args


def parse_ctf(path):
    rows = [x.split() for x in path.read_text().splitlines() if x.strip() and not x.startswith("#")]
    if len(rows) != 1 or len(rows[0]) < 9:
        raise ValueError("Expected exactly one native CTF result")
    values = [float(x) for x in rows[0][1:9]]
    if not all(math.isfinite(x) for x in values) or min(values[1:3]) <= 0:
        raise ValueError("Invalid native CTF result")
    return dict(zip(("tilt_deg", "min_defocus_angstrom", "max_defocus_angstrom", "azimuth_deg", "phase_deg", "score", "estimated_fit_resolution_angstrom", "pixel_size_angstrom"), values))


def trajectory(path, marker, stop):
    lines = Path(path).read_text().splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == marker) + 1
    except StopIteration as exc:
        raise ValueError(f"Missing trajectory section {marker}") from exc
    values = []
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith(stop):
            break
        fields = stripped.split()
        if len(fields) == 3 and re.fullmatch(r"[0-9]+", fields[0]):
            x, y = float(fields[1]), float(fields[2])
            if not math.isfinite(x) or not math.isfinite(y):
                raise ValueError("Non-finite motion estimate")
            values.append((int(fields[0]), x, y))
    if len(values) < 2 or any(row[0] != values[0][0] + i for i, row in enumerate(values)):
        raise ValueError("Missing or discontinuous trajectory")
    return values


def trajectory_summary(rows, pixel_size):
    x0, y0 = rows[0][1:]
    x1, y1 = rows[-1][1:]
    return {"frames": len(rows), "endpoint_displacement_pixels": math.hypot(x1-x0, y1-y0), "endpoint_displacement_angstrom": pixel_size * math.hypot(x1-x0, y1-y0)}


def parse_ctffind_reference(path):
    text = Path(path).read_text()
    match = re.search(r"# Pixel size:\s*([\d.]+).*?acceleration voltage:\s*([\d.]+).*?spherical aberration:\s*([\d.]+).*?amplitude contrast:\s*([\d.]+)", text)
    box = re.search(r"# Box size:\s*(\d+)", text)
    input_match = re.search(r"# Input file:\s*(.*?)\s*;", text)
    rows = [line.split() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    if not match or not box or not input_match or len(rows) != 1 or len(rows[0]) < 3:
        raise ValueError("Expected native single-micrograph CTFFIND text output")
    values = sorted([float(rows[0][1]), float(rows[0][2])])
    metadata = dict(zip(CTF_META[:4], (float(x) for x in match.groups())))
    metadata["tile_size"] = int(box.group(1))
    return metadata, values, Path(input_match.group(1)).name


def run(manifest_path, output):
    manifest = json.loads(Path(manifest_path).read_text())
    tool = manifest["tool"]
    if tool not in COMMITS or manifest["source_commit"] != COMMITS[tool] or manifest["expected_version"] != VERSIONS[tool]:
        raise ValueError("Source commit or version is not the pinned CZI build")
    p = manifest["parameters"]
    items = manifest["items"]
    if not isinstance(items, list) or not items:
        raise ValueError("No input items")
    ids = [i["id"] for i in items]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r"[A-Za-z0-9_-]+", i) for i in ids):
        raise ValueError("Item IDs must be unique and path-safe")
    binary = identity(manifest["binary"])
    prepared = []
    for item in items:
        inp = identity(item["input"])
        inp["dimensions"] = dimensions(inp["path"])
        ref = item["reference"]
        ref_identity = identity(ref["identity"])
        if not isinstance(ref["differences"], list) or not ref["differences"] or not all(isinstance(s, str) and s.strip() for s in ref["differences"]):
            raise ValueError("Describe comparison differences")
        if tool == "gctffind":
            if inp["dimensions"]["shape"][0] != 1:
                raise ValueError("CTF input must be a single micrograph")
            native_metadata, native_defocus, native_input_name = parse_ctffind_reference(ref_identity["path"])
            if native_input_name != Path(inp["path"]).name:
                raise ValueError("CTFFIND input basename does not match micrograph")
            for k in CTF_META:
                if ref["metadata"][k] != p[k] or not math.isclose(float(native_metadata[k]), float(p[k]), abs_tol=1e-6):
                    raise ValueError(f"CTF metadata mismatch: {k}")
            for k in ("min_defocus_angstrom", "max_defocus_angstrom"):
                if not math.isfinite(float(ref[k])) or float(ref[k]) <= 0:
                    raise ValueError("Invalid reference defocus")
            declared = [float(ref["min_defocus_angstrom"]), float(ref["max_defocus_angstrom"])]
            if any(not math.isclose(a, b, abs_tol=0.01) for a, b in zip(declared, native_defocus)):
                raise ValueError("Reference defocus does not match native CTFFIND output")
        prepared.append((item, inp, ref_identity))
    out = Path(output).resolve()
    out.mkdir(parents=True, exist_ok=False)
    version = subprocess.run([binary["path"], "--version"], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
    (out / "version.log").write_text(version)
    if VERSIONS[tool] not in version:
        raise ValueError("Executable version mismatch")
    report = {"status": "in_progress", "schema": "cryocore-czi-worker-v1", "tool": tool, "source_commit": COMMITS[tool], "binary": binary, "version": version.strip(), "parameters": p, "manifest_sha256": digest(manifest_path), "items": [], "claim_limit": "Experimental inputs; estimates are not ground truth or demonstrated accuracy. Comparison metadata and preprocessing differences remain explicit."}
    for item, inp, ref_id in prepared:
        dest = out / item["id"]
        dest.mkdir()
        cmd = command(tool, binary["path"], inp["path"], dest, p)
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (dest / "native.log").write_text(proc.stdout)
        record = {"id": item["id"], "input": inp, "reference": {**item["reference"], "identity": ref_id}, "command": cmd, "returncode": proc.returncode}
        report["items"].append(record)
        if proc.returncode != 0:
            raise RuntimeError(f"{item['id']}: command failed; native log retained")
        if tool == "gctffind":
            result = parse_ctf(dest / "CTF.txt")
            if not math.isclose(result["pixel_size_angstrom"], p["pixel_size_angstrom"], abs_tol=0.011):
                raise ValueError("CTF result pixel size mismatch")
            spectra = list(dest.glob("*_CTF.mrc"))
            if len(spectra) != 1:
                raise ValueError("Missing native CTF spectrum")
            record["spectrum_dimensions"] = validate_mrc_pixels(spectra[0])
            record["estimate"] = result
            record["difference_angstrom"] = {key: result[key] - float(item["reference"][key]) for key in ("min_defocus_angstrom", "max_defocus_angstrom")}
        else:
            corrected = dest / "corrected.mrc"
            record["corrected_dimensions"] = validate_mrc_pixels(corrected)
            alignments = list(dest.glob("*.aln"))
            if len(alignments) != 1:
                raise ValueError("Missing or ambiguous native alignment file")
            czi_shift = trajectory(alignments[0], "globalShift", "localShift")
            ref_shift = trajectory(ref_id["path"], "data_global_shift", "data_local_motion_model")
            if len(czi_shift) != len(ref_shift):
                raise ValueError("Global trajectory frame counts differ")
            record["global_trajectory_comparison"] = {
                "motioncor3": trajectory_summary(czi_shift, p["pixel_size_angstrom"]),
                "relion": trajectory_summary(ref_shift, p["pixel_size_angstrom"]),
                "interpretation": "Endpoint magnitudes are image-derived estimates; sign and axis conventions have not been reconciled. RELION also models local motion.",
            }
        record["outputs"] = [{"path": str(f), "sha256": digest(f), "bytes": f.stat().st_size} for f in sorted(dest.rglob("*")) if f.is_file()]
        (out / "validation.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    report["status"] = "complete"
    (out / "validation.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest")
    ap.add_argument("output")
    args = ap.parse_args()
    try:
        report = run(args.manifest, args.output)
        print(json.dumps({"status": "complete", "items": len(report["items"]), "output": args.output}))
    except (ValueError, KeyError, OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"worker failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
