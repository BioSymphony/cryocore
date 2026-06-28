#!/usr/bin/env python3
"""CryoCore FSC / resolution curve plotter (matplotlib, headless).

Cryo-EM workflows often report resolution with a Fourier Shell Correlation curve
and the 0.143 (half-map "gold standard") and 0.5 (map-model) thresholds. This renders
that panel from a TSV the reconstruction emits, OR a labelled demo
curve to prove the capability before real FSC data exists.

Usage:
  python3 fsc_plot.py --fsc half=halfmap_fsc.tsv --fsc map-model=mm_fsc.tsv \\
      --out fsc.png --title "EMD-XXXXX FSC"
  python3 fsc_plot.py --demo --out fsc_demo.png --title "FSC (illustrative)"

TSV format: two columns per file -> spatial_frequency(1/A)\\tFSC  (header optional).
Heavy PNG output belongs under .runtime/ (gitignored).
"""

from __future__ import annotations

import argparse
import math
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_tsv(path):
    freqs, vals = [], []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.replace(",", "\t").split()
            try:
                f, v = float(parts[0]), float(parts[1])
            except (ValueError, IndexError):
                continue  # header row
            freqs.append(f)
            vals.append(v)
    return freqs, vals


def demo_curve(label, res_cutoff, n=60):
    """Synthetic but realistic sigmoidal FSC falloff for capability proof."""
    freqs, vals = [], []
    fmax = 1.0 / 1.8
    for i in range(1, n + 1):
        f = fmax * i / n
        # logistic drop centred near 1/res_cutoff
        v = 1.0 / (1.0 + math.exp((f - 1.0 / res_cutoff) * 38.0))
        freqs.append(f)
        vals.append(max(0.0, min(1.0, v)))
    return label, freqs, vals


def crossing_resolution(freqs, vals, threshold):
    for i in range(1, len(vals)):
        if vals[i - 1] >= threshold > vals[i]:
            f0, f1 = freqs[i - 1], freqs[i]
            v0, v1 = vals[i - 1], vals[i]
            fr = f0 + (f1 - f0) * (v0 - threshold) / (v0 - v1) if v0 != v1 else f1
            return 1.0 / fr if fr > 0 else None
    return None


def main():
    ap = argparse.ArgumentParser(description="CryoCore FSC curve plotter")
    ap.add_argument("--fsc", action="append", default=[],
                    help="label=path.tsv (repeatable)")
    ap.add_argument("--demo", action="store_true", help="render an illustrative demo panel")
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="Fourier Shell Correlation")
    ap.add_argument("--thresholds", default="0.143,0.5")
    args = ap.parse_args()

    series = []
    if args.demo:
        series.append(demo_curve("half-map FSC", 2.9))
        series.append(demo_curve("map-model FSC", 3.3))
    for spec in args.fsc:
        label, _, path = spec.partition("=")
        if not path:
            label, path = path or label, label
        freqs, vals = read_tsv(path)
        if freqs:
            series.append((label, freqs, vals))
    if not series:
        sys.exit("ERROR: provide --fsc label=path or --demo")

    thresholds = [float(t) for t in args.thresholds.split(",") if t.strip()]

    fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=150)
    colors = ["#1f6feb", "#d1495b", "#2a9d8f", "#6a4c93"]
    annot = []
    for i, (label, freqs, vals) in enumerate(series):
        ax.plot(freqs, vals, color=colors[i % len(colors)], lw=2.2, label=label, zorder=3)
        for th in thresholds:
            r = crossing_resolution(freqs, vals, th)
            if r:
                annot.append((label, th, r))

    for th in thresholds:
        ax.axhline(th, ls="--", lw=1.0, color="#777", zorder=1)
        ax.text(0.001, th + 0.01, f"FSC = {th:g}", fontsize=8, color="#555")

    ax.set_xlabel("Spatial frequency (1/Angstrom)")
    ax.set_ylabel("Fourier Shell Correlation")
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(left=0)
    ax.set_title(args.title)
    ax.grid(True, alpha=0.25)

    # top axis in resolution (Angstrom)
    def f2r(f):
        return ["%.1f" % (1.0 / t) if t > 0 else "" for t in f]
    secax = ax.secondary_xaxis("top")
    ticks = [t for t in ax.get_xticks() if t > 0]
    secax.set_xticks(ticks)
    secax.set_xticklabels(f2r(ticks))
    secax.set_xlabel("Resolution (Angstrom)")

    caption = "  ".join(f"{lbl}: {r:.2f} Angstrom @ {th:g}" for lbl, th, r in annot)
    if caption:
        ax.text(0.5, -0.22, caption, transform=ax.transAxes, ha="center",
                fontsize=8, color="#333")
    if args.demo:
        ax.text(0.98, 0.95, "ILLUSTRATIVE - synthetic curve", transform=ax.transAxes,
                ha="right", va="top", fontsize=8, color="#b00", style="italic")

    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
    fig.tight_layout()
    fig.savefig(args.out, bbox_inches="tight")
    print(f"[fsc] wrote {args.out}")
    for lbl, th, r in annot:
        print(f"[fsc] {lbl}: {r:.2f} A at FSC={th:g}")


if __name__ == "__main__":
    main()
