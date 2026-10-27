#!/usr/bin/env python3
"""Run reviewed native Miffi on unchanged MRC micrographs; emit advisory scores.

Provider-neutral optional adapter. Scientific dependencies are imported only at
execution time. This file does not download, deploy, submit, or delete resources.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import pickle
import platform
import signal
import subprocess
import sys
import time

SOURCE_COMMIT = "697c72545fcf1e72d8dcaf6250dfd42139a864e7"
SOURCE_URL = "https://github.com/ando-lab/miffi"
SOURCE_FILES = {
    "__init__.py": "5af1eb79cdc4c2c244e66a1457bf05c554ce94d3975fe1bd8d6a9d488938c469",
    "inference.py": "c97497d9b81b21e316b948af30ae3481b685c6653f6ae9ad08ea86506e541372",
    "datasets.py": "04e53247a1c3cdcabbccc184c796b9ebe369e4849025cd41d1f067ab07da1f66",
    "parameters.py": "4021be275ba30497bd29e81c1473b36e3b6f2446dbfea03f92fe3c15ce948bfc",
    "utils.py": "336a0ec71e4693381d2cd9c5d2aec63f97d5bdc6a4342573a4ce99bbb5911171",
}
MODEL_MD5 = {
    "miffi_v1": "4bfaefa7fd9e730deb0e06431e43c18a",
    "miffi_no_ps_v1": "4ef7d70994c6196db5c296657650a681",
}
LABELS = [
    ["no_film", "minor_film", "major_film", "film"],
    ["no_crack_drift", "crack_drift_empty"],
    ["not_crystalline", "minor_crystalline", "major_crystalline"],
    ["minor_contamination", "major_contamination"],
]
CATEGORIES = ["film", "drift", "crystalline", "contamination"]


def digest(path: Path, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def verify_source(source: Path) -> dict:
    actual = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != SOURCE_COMMIT:
        raise ValueError(f"Miffi source commit mismatch: {actual}")
    for name, expected in SOURCE_FILES.items():
        if digest(source / "miffi" / name) != expected:
            raise ValueError(f"Miffi source bytes changed: {name}")
    # Do not allow an injected compiled module to take priority over reviewed .py.
    package_files = list((source / "miffi").iterdir())
    if any(p.suffix in (".so", ".pyd") for p in package_files):
        raise ValueError("Unexpected compiled module in Miffi source package")
    return {"url": SOURCE_URL, "commit": actual, "license": "GPL-3.0", "files_sha256": SOURCE_FILES}


def inspect_inputs(input_dir: Path, pixel_size: float) -> list[dict]:
    import mrcfile
    import numpy as np

    paths = sorted(input_dir.glob("*.mrc"))
    if not paths:
        raise ValueError("Input directory contains no .mrc micrographs")
    rows = []
    for path in paths:
        if "\n" in path.name or "\r" in path.name:
            raise ValueError("Micrograph filename contains newline")
        with mrcfile.mmap(path, permissive=False, mode="r") as mrc:
            data = mrc.data
            if data.ndim != 2 or min(data.shape) < 32:
                raise ValueError(f"Expected a 2D experimental micrograph: {path.name}")
            if not np.isfinite(data).all():
                raise ValueError(f"Nonfinite input pixels: {path.name}")
            std = float(np.std(data, dtype=np.float64))
            if std <= 0:
                raise ValueError(f"Constant input micrograph: {path.name}")
            rows.append({
                "name": path.name, "sha256": digest(path), "bytes": path.stat().st_size,
                "shape_yx": list(data.shape), "dtype": str(data.dtype),
                "header_pixel_size_angstrom": [float(mrc.voxel_size[k]) for k in ("x", "y", "z")],
                "effective_pixel_size_angstrom": pixel_size,
                "pixel_statistics": {"min": float(np.min(data)), "max": float(np.max(data)),
                                     "mean": float(np.mean(data, dtype=np.float64)), "std": std},
                "pixel_bytes_sha256": hashlib.sha256(memoryview(np.ascontiguousarray(data)).cast("B")).hexdigest(),
            })
    if len({tuple(row["shape_yx"]) for row in rows}) != 1:
        raise ValueError("Miffi derives transforms from first input: input dimensions must match")
    return rows


def preprocessing(shape_yx: list[int], pixel_size: float, no_ps: bool) -> dict:
    small, large = sorted(shape_yx)
    target_pixel = max(1.5, pixel_size)
    resized = round(small * pixel_size / target_pixel) // 2 * 2
    if resized < 2:
        raise ValueError("Fourier crop has invalid dimension")
    return {
        "external_image_changes": "none; native MRC pixel arrays supplied unchanged",
        "transpose": shape_yx[0] > shape_yx[1],
        "square_split_count": math.ceil(large / small),
        "square_split_rule": "native top/left consecutive squares, final square aligned to far edge",
        "requested_downsample_pixel_size_angstrom": 1.5,
        "effective_downsample_pixel_size_angstrom": target_pixel,
        "fourier_crop_shape_yx": [resized, resized],
        "image_transform": "torch.fft.rfft2; native unshifted Fourier crop; torch.fft.irfft2",
        "spectrum_transform": "none" if no_ps else "native fft_to_ps: centered mirrored abs(rfft2), amplitude spectrum (not squared)",
        "channel_count": 1 if no_ps else 2,
        "resize": "torchvision Resize(384, antialias=True), per native source",
        "normalization": "per channel, 3 iterations mean/std excluding outside 3 std; standardize; clip to [-2.5,2.5]",
        "split_combination": "native default rules, retain all per-split probabilities and logits",
        "training_pixel_size_mismatch": bool(pixel_size > 1.5 and not no_ps),
    }


def native_command(args: argparse.Namespace, miclist: Path, native: Path) -> list[str]:
    cmd = [sys.executable, "-m", "miffi.inference", "-f", str(miclist),
           "-d", str(args.input_dir), "-o", str(native), "--outname", args.model_name,
           "--pixel-size", str(args.pixel_size), "--downsample-pixel-size", "1.5",
           "--fm", str(args.checkpoint), "--batch-size", str(args.batch_size),
           "--num-workers", str(args.num_workers), "--gpu-id", str(args.gpu_id)]
    if args.model_name == "miffi_no_ps_v1":
        cmd.append("--no-ps")
    if args.use_cpu:
        cmd.append("--use-cpu")
    return cmd


def run_native(cmd: list[str], cwd: Path, env: dict, log: Path, timeout: int) -> dict:
    start = time.time()
    with log.open("wb") as stream:
        process = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=stream,
                                   stderr=subprocess.STDOUT, start_new_session=True)
        timed_out = False
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGKILL)
            code = process.wait()
    return {"argv": cmd, "cwd": str(cwd), "returncode": code,
            "timed_out": timed_out, "elapsed_seconds": time.time() - start,
            "log": log.name, "log_sha256": digest(log)}


def export_native(result_path: Path, expected_names: list[str], output: Path) -> dict:
    # Only call on the sole file just generated by the verified pinned subprocess
    # in this worker's freshly created private output directory. Never expose this
    # function as a converter for uploaded pickle files; tensors contain pickle.
    before = digest(result_path)
    with result_path.open("rb") as handle:
        result = pickle.load(handle)
    if before != digest(result_path):
        raise ValueError("Native result changed during conversion")
    names = [Path(name).name for name in result["mic_list"]]
    if names != expected_names:
        raise ValueError("Native predictions do not match exact ordered input cohort")
    probabilities = result["mic_pred_confidence"].tolist()
    logits = result["outputs"].tolist()
    combined = result["combined_preds"].tolist()
    if not probabilities or len(combined) != 2:
        raise ValueError("Malformed native prediction dimensions")
    if len(logits) != len(probabilities):
        raise ValueError("Native logits/split count mismatch")
    if any(len(part) != len(names) for part in combined):
        raise ValueError("Native combined prediction/input count mismatch")
    for mic_index in range(len(names)):
        if any(len(combined[part][mic_index]) != 4 for part in (0, 1)):
            raise ValueError("Native combined category count mismatch")
        for category_index, labels in enumerate(LABELS):
            pred = combined[0][mic_index][category_index]
            selected = combined[1][mic_index][category_index]
            if pred not in range(len(labels)) or selected not in range(len(probabilities)):
                raise ValueError("Native combined label/split index out of range")
    rows = []
    for split_index, split in enumerate(probabilities):
        if len(split) != len(names) or len(logits[split_index]) != len(names):
            raise ValueError("Native prediction/input count mismatch")
        for mic_index, values in enumerate(split):
            if len(values) != 11 or len(logits[split_index][mic_index]) != 11:
                raise ValueError("Native output does not have 11 expected class scores")
            if any(not math.isfinite(v) for v in logits[split_index][mic_index]):
                raise ValueError("Native logits contain nonfinite values")
            offset = 0
            for category, labels in zip(CATEGORIES, LABELS):
                scores = values[offset:offset + len(labels)]
                if any(not math.isfinite(v) or v < 0 or v > 1 for v in scores) or abs(sum(scores) - 1) > 1e-5:
                    raise ValueError("Native category probabilities invalid")
                for idx, (label, score) in enumerate(zip(labels, scores)):
                    rows.append({"micrograph": names[mic_index], "split": split_index,
                                 "category": category, "label": label,
                                 "probability": score, "logit": logits[split_index][mic_index][offset + idx]})
                offset += len(labels)
    safe = {"micrographs": names, "label_names": LABELS, "probabilities": probabilities,
            "logits": logits, "combined_predictions_and_selected_split": combined,
            "native_pickle_sha256": before, "policy": "advisory_only_no_rejection_or_deletion"}
    write_json(output / "predictions.json", safe)
    with (output / "micrograph_filter_scores.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return {"micrograph_count": len(names), "split_count": len(probabilities), "score_rows": len(rows)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("input-dir", "checkpoint", "source-dir", "output-dir"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--checkpoint-sha256", required=True)
    parser.add_argument("--model-name", choices=sorted(MODEL_MD5), required=True)
    parser.add_argument("--pixel-size", type=float, required=True)
    parser.add_argument("--gpu-id", type=int, default=0)
    parser.add_argument("--use-cpu", action="store_true")
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args(argv)
    if not math.isfinite(args.pixel_size) or args.pixel_size <= 0.01:
        parser.error("--pixel-size must be finite and greater than 0.01 angstrom")
    if args.batch_size < 1 or args.num_workers < 0 or args.timeout_seconds < 1:
        parser.error("invalid batch/worker/timeout bound")
    for name in ("input_dir", "checkpoint", "source_dir", "output_dir"):
        setattr(args, name, getattr(args, name).resolve())
    args.output_dir.mkdir(parents=True, exist_ok=False, mode=0o700)
    manifest = {"schema_version": 1, "status": "started", "model_name": args.model_name,
                "claim_boundary": "Advisory model class scores; no reviewed labels, accuracy estimate, automatic filtering, or image deletion. Experimental provenance is established separately by the caller's frozen input ledger."}
    try:
        manifest["source"] = verify_source(args.source_dir)
        checkpoint_sha = digest(args.checkpoint)
        if checkpoint_sha != args.checkpoint_sha256 or digest(args.checkpoint, "md5") != MODEL_MD5[args.model_name]:
            raise ValueError("Checkpoint does not match supplied SHA256 and reviewed Zenodo MD5")
        manifest["checkpoint"] = {"name": args.checkpoint.name, "sha256": checkpoint_sha,
                                  "md5": MODEL_MD5[args.model_name], "bytes": args.checkpoint.stat().st_size,
                                  "url": f"https://zenodo.org/api/records/8342009/files/{args.model_name}.pt/content",
                                  "license": "CC-BY-4.0", "format": "trusted pinned upstream TorchScript"}
        manifest["inputs"] = inspect_inputs(args.input_dir, args.pixel_size)
        manifest["preprocessing"] = preprocessing(manifest["inputs"][0]["shape_yx"], args.pixel_size,
                                                  args.model_name == "miffi_no_ps_v1")
        import torch
        if not args.use_cpu and not torch.cuda.is_available():
            raise ValueError("GPU requested but CUDA unavailable; refusing silent CPU fallback")
        manifest["runtime"] = {"python": sys.version, "platform": platform.platform(),
                               "cuda": torch.version.cuda, "gpu": None if args.use_cpu else torch.cuda.get_device_name(args.gpu_id),
                               "packages": {p: importlib.metadata.version(p) for p in ("torch", "torchvision", "numpy", "mrcfile", "timm", "miffi")}}
        miclist = args.output_dir / "micrographs.txt"
        miclist.write_text("".join(row["name"] + "\n" for row in manifest["inputs"]))
        native = args.output_dir / "native"
        native.mkdir(mode=0o700)
        env = dict(os.environ)
        # Only reviewed source participates in Python module lookup.
        env["PYTHONPATH"] = str(args.source_dir)
        env["PYTHONNOUSERSITE"] = "1"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["OMP_NUM_THREADS"] = "2"
        env["MKL_NUM_THREADS"] = "2"
        manifest["execution"] = run_native(native_command(args, miclist, native), native, env,
                                            args.output_dir / "native-inference.log", args.timeout_seconds)
        if manifest["execution"]["returncode"] != 0:
            raise ValueError("Native Miffi failed; inspect retained log")
        results = list(native.glob("*_inference_result_*.pkl"))
        if len(results) != 1 or not results[0].is_file() or results[0].is_symlink():
            raise ValueError("Expected exactly one freshly generated native prediction file")
        manifest["validation"] = export_native(results[0], [r["name"] for r in manifest["inputs"]], args.output_dir)
        # Detect input mutation during native execution before reporting success.
        for row in manifest["inputs"]:
            if digest(args.input_dir / row["name"]) != row["sha256"]:
                raise ValueError(f"Input changed during inference: {row['name']}")
        if digest(args.checkpoint) != checkpoint_sha:
            raise ValueError("Checkpoint changed during inference")
        manifest["status"] = "completed_advisory_only"
    except Exception as exc:
        manifest["status"] = "failed"
        manifest["error"] = f"{type(exc).__name__}: {exc}"
    manifest["artifacts"] = [{"path": str(p.relative_to(args.output_dir)), "sha256": digest(p), "bytes": p.stat().st_size}
                             for p in sorted(args.output_dir.rglob("*")) if p.is_file()]
    write_json(args.output_dir / "miffi_qc_manifest.json", manifest)
    print(json.dumps({"status": manifest["status"], "manifest": str(args.output_dir / "miffi_qc_manifest.json")}))
    return 0 if manifest["status"] == "completed_advisory_only" else 1


if __name__ == "__main__":
    raise SystemExit(main())
