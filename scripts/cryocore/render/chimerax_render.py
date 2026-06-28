#!/usr/bin/env python3
"""CryoCore ChimeraX figure/movie renderer (license-controlled path).

ChimeraX is a strong cryo-EM map renderer, but it needs an OpenGL context, so
the headless path is platform-specific:

  * Linux          : xvfb-run ChimeraX --offscreen --nogui --script x.cxc --exit
  * macOS          : ChimeraX --offscreen HANGS (no OSMesa). Use the GUI + REST
                     API (renders via Metal/GPU) -- opt in with --rest. PyMOL
                     (scripts/cryocore/render/pymol_render.py) is the reliable
                     window-free local alternative.

This tool generates the .cxc script for a figure/movie and runs it on the
available path; with no runnable path it writes the .cxc and prints the exact
Linux command. ChimeraX is not redistributed from this repo.

Usage:
  python3 chimerax_render.py map-model  --map M.mrc --model X.cif --level 0.03 --out fig.png
  python3 chimerax_render.py turntable  --map M.mrc --model X.cif --level 0.03 --out spin.mp4
  python3 chimerax_render.py local-res  --map M.mrc --localres LR.mrc --out lr.png
  python3 chimerax_render.py orthoslices --map M.mrc --out ortho.png
  python3 chimerax_render.py density-zone --map M.mrc --model X.cif --range 6 --out zone.png
Add --rest to drive a GUI ChimeraX on macOS; --execute to actually run (else
prep-only: writes the .cxc and the command).
"""

from __future__ import annotations

import argparse
import glob
import os
import platform
import shutil
import subprocess
import sys
import time


def find_chimerax():
    for c in ("chimerax", "ChimeraX"):
        p = shutil.which(c)
        if p:
            return p
    apps = sorted(glob.glob("/Applications/ChimeraX*.app/Contents/MacOS/ChimeraX"))
    return apps[-1] if apps else None


SCENE = [
    "set bgColor white",
    "graphics silhouettes true width 1.4",
    "graphics quality 3",
    "lighting simple",            # simple lighting keeps density colours true
]


def model_style_lines(model_id="#2"):
    # works for protein, RNA, DNA; nucleotides as ladder, ligands as stick
    return [
        f"cartoon {model_id}",
        f"nucleotides {model_id} ladder",
        f"style {model_id} & ligand stick",
        f"color {model_id} bychain",
    ]


def cxc_map_model(a):
    lines = ["close session", f"windowsize {a.width} {a.height}"] + SCENE
    lines += [f"open {a.map}", f"open {a.model}"]
    lvl = f"level {a.level}" if a.level is not None else "sdLevel 4"
    style = "mesh" if a.map_style == "mesh" else "surface"
    lines += [f"volume #1 style {style} {lvl} step 1 color #9aa6b2"]
    if a.map_style == "surface":
        lines += ["transparency #1 55"]
    lines += model_style_lines("#2")
    lines += ["view", f"save {a.out} width {a.width} height {a.height} supersample 3"]
    return lines


def cxc_map_surface(a):
    lines = ["close session", f"windowsize {a.width} {a.height}"] + SCENE
    lines += [f"open {a.map}"]
    lvl = f"level {a.level}" if a.level is not None else "sdLevel 4"
    lines += [f"volume #1 style surface {lvl} step 1 color #7fb3d5",
              "view", f"save {a.out} width {a.width} height {a.height} supersample 3"]
    return lines


def cxc_turntable(a):
    lines = ["close session", f"windowsize {a.width} {a.height}"] + SCENE
    lines += [f"open {a.map}", f"open {a.model}"]
    lvl = f"level {a.level}" if a.level is not None else "sdLevel 4"
    lines += [f"volume #1 style mesh {lvl} step 1 color #9aa6b2"]
    lines += model_style_lines("#2")
    lines += ["view", "movie record",
              f"turn y {round(360.0/a.frames, 3)} {a.frames}", f"wait {a.frames}",
              f"movie encode {a.out} framerate {a.fps} quality higher"]
    return lines


def cxc_local_res(a):
    # color the model/map surface by an accompanying local-resolution map
    lines = ["close session", f"windowsize {a.width} {a.height}"] + SCENE
    lines += [f"open {a.map}", f"open {a.localres}"]
    lvl = f"level {a.level}" if a.level is not None else "sdLevel 4"
    lines += [f"volume #1 style surface {lvl} step 1",
              "color sample #1 map #2 palette 2.5,blue:3.0,cyan:3.5,green:4.0,yellow:5.0,red",
              "key blue:2.5 cyan:3.0 green:3.5 yellow:4.0 red:5.0 pos 0.80,0.08 size 0.18,0.025",
              "2dlabels create lrlabel text 'local resolution (A)' xpos 0.78 ypos 0.12 size 22",
              "view", f"save {a.out} width {a.width} height {a.height} supersample 3"]
    return lines


def cxc_orthoslices(a):
    lines = ["close session", f"windowsize {a.width} {a.height}"] + SCENE
    lines += [f"open {a.map}", "volume #1 style image orthoplanes xyz",
              "view", f"save {a.out} width {a.width} height {a.height} supersample 3"]
    return lines


def cxc_density_zone(a):
    lines = ["close session", f"windowsize {a.width} {a.height}"] + SCENE
    lines += [f"open {a.map}", f"open {a.model}",
              f"volume zone #1 nearAtoms #2 range {a.range} newMap true"]
    lvl = f"level {a.level}" if a.level is not None else "sdLevel 4"
    lines += [f"volume #3 style mesh {lvl} step 1 color #9aa6b2"]
    lines += model_style_lines("#2")
    lines += ["view", f"save {a.out} width {a.width} height {a.height} supersample 3"]
    return lines


BUILDERS = {
    "map-model": cxc_map_model, "map-surface": cxc_map_surface,
    "turntable": cxc_turntable, "local-res": cxc_local_res,
    "orthoslices": cxc_orthoslices, "density-zone": cxc_density_zone,
}


def run_offscreen(chimerax, cxc_path):
    base = [chimerax, "--offscreen", "--nogui", "--script", cxc_path, "--exit"]
    if shutil.which("xvfb-run") and platform.system() == "Linux":
        return subprocess.run(["xvfb-run", "-a", "-s", "-screen 0 1920x1920x24"] + base)
    return subprocess.run(base)


def run_rest(chimerax, lines, out):
    """macOS GUI + REST. Pops a ChimeraX window; renders via GPU."""
    import socket
    import urllib.parse
    import urllib.request
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    proc = subprocess.Popen([chimerax, "--cmd",
                             f"remotecontrol rest start port {port} json true log false"])
    base = f"http://127.0.0.1:{port}/run"
    try:
        for _ in range(40):
            try:
                urllib.request.urlopen(base + "?command=" + urllib.parse.quote("version"), timeout=2)
                break
            except Exception:
                time.sleep(0.5)
        for cmd in lines:
            urllib.request.urlopen(base + "?command=" + urllib.parse.quote(cmd), timeout=240).read()
        # 0-byte PNG race fix: wait + re-poll
        if os.path.exists(out):
            os.unlink(out)
        for _ in range(16):
            if os.path.exists(out) and os.path.getsize(out) > 0:
                break
            time.sleep(0.5)
    finally:
        try:
            urllib.request.urlopen(base + "?command=" + urllib.parse.quote("exit"), timeout=5)
        except Exception:
            pass
        proc.terminate()


def main():
    ap = argparse.ArgumentParser(description="CryoCore ChimeraX renderer")
    ap.add_argument("kind", choices=list(BUILDERS))
    ap.add_argument("--map"); ap.add_argument("--model"); ap.add_argument("--localres")
    ap.add_argument("--level", type=float, default=None)
    ap.add_argument("--map-style", choices=["mesh", "surface"], default="mesh")
    ap.add_argument("--range", type=float, default=6.0)
    ap.add_argument("--frames", type=int, default=180)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=1600)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cxc-out", default=None, help="where to write the .cxc (default beside --out)")
    ap.add_argument("--rest", action="store_true", help="macOS GUI+REST render (pops a window)")
    ap.add_argument("--execute", action="store_true", help="actually run ChimeraX (else prep-only)")
    a = ap.parse_args()

    lines = BUILDERS[a.kind](a)
    cxc_path = a.cxc_out or (os.path.splitext(a.out)[0] + ".cxc")
    os.makedirs(os.path.dirname(os.path.abspath(cxc_path)) or ".", exist_ok=True)
    with open(cxc_path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"[chimerax] wrote scene script {cxc_path}")

    chimerax = find_chimerax()
    is_mac = platform.system() == "Darwin"
    linux_cmd = f"xvfb-run -a ChimeraX --offscreen --nogui --script {cxc_path} --exit"

    if not a.execute:
        print("[chimerax] prep-only (pass --execute to render).")
        print(f"[chimerax] Linux: {linux_cmd}")
        if is_mac:
            print("[chimerax] macOS: add --rest to render via a GUI instance, or use pymol_render.py.")
        return

    if not chimerax:
        sys.exit("[chimerax] ChimeraX not found; renderer output was not produced.")
    if is_mac and not a.rest:
        print("[chimerax] macOS offscreen hangs; re-run with --rest (GUI) or use pymol_render.py.")
        print(f"[chimerax] Linux: {linux_cmd}")
        return
    if a.rest and is_mac:
        run_rest(chimerax, lines, a.out)
    else:
        run_offscreen(chimerax, cxc_path)
    ok = os.path.exists(a.out) and os.path.getsize(a.out) > 0
    print(f"[chimerax] {'wrote ' + a.out if ok else 'no output produced'}")


if __name__ == "__main__":
    main()
