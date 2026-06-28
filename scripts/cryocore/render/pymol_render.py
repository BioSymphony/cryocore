#!/usr/bin/env python3
"""CryoCore headless figure renderer (PyMOL backend).

PyMOL's software ray tracer renders without any display, so this is the reliable
local macOS/Linux path for cryo-EM map/model snapshots and turntable movies.
ChimeraX is the license-controlled GPU/Linux-offscreen path (see chimerax_render.py)
and is often better for whole-map surfaces; this PyMOL path is the fallback renderer.

Run it THROUGH PyMOL (not plain python):

    pymol -cqr scripts/cryocore/render/pymol_render.py -- <subcommand> [opts]

Subcommands:
  map-model    map+model overlay (mesh or transparent surface) still
  map-surface  map-only isosurface/mesh still (real density hero)
  cartoon      model-only cartoon still (rainbow/chain/bfactor); RNA ring mode
  density-zoom carve density around a residue selection and zoom in
  spin         360-degree turntable -> PNG frames -> MP4 (ffmpeg) + GIF (palettegen)

Implementation notes:
  * "model" is a RESERVED PyMOL object name -> we load coordinates as "mol".
  * orient/zoom need an atom selection; map/mesh objects are not selections, so
    map-only scenes are framed via bounding-box pseudoatoms.
  * contour level for a real .map is in ABSOLUTE map units; we auto-pick
    mean + N*sigma from the map data unless --level is given.
  * always cmd.quit() at the end or PyMOL hangs.
  * heavy PNG/MP4/GIF outputs belong under .runtime/ (gitignored).
"""

from __future__ import annotations

import argparse
import os
import shutil
import struct
import subprocess
import sys

try:
    from pymol import cmd
    HAVE_PYMOL = True
except Exception:
    HAVE_PYMOL = False

MOL = "mol"   # coordinate object ("model" is reserved in PyMOL)
DENS = "density"


def mrc_sigma_level(path: str, n_sigma: float = 2.0):
    with open(path, "rb") as fh:
        hdr = fh.read(1024)
        nx, ny, nz, mode = struct.unpack("<4i", hdr[:16])
        nsymbt = struct.unpack("<i", hdr[92:96])[0]
        fh.seek(1024 + nsymbt)
        raw = fh.read()
    size = {0: 1, 1: 2, 2: 4, 6: 2}.get(mode, 4)
    try:
        import numpy as np
        npdt = {0: np.int8, 1: np.int16, 2: np.float32, 6: np.uint16}.get(mode, np.float32)
        data = np.frombuffer(raw, dtype=npdt).astype(np.float64)
        mean, sigma = float(data.mean()), float(data.std())
    except Exception:
        fmt = {0: "b", 1: "h", 2: "f", 6: "H"}.get(mode, "f")
        n = len(raw) // size
        step = max(1, n // 200000)
        vals = [struct.unpack_from("<" + fmt, raw, i * size)[0] for i in range(0, n, step)]
        mean = sum(vals) / len(vals)
        sigma = (sum((v - mean) ** 2 for v in vals) / len(vals)) ** 0.5
    return mean + n_sigma * sigma, mean, sigma


def base_scene(bg="white", outline=False):
    cmd.bg_color(bg)
    cmd.set("ray_opaque_background", 1)
    cmd.set("antialias", 2)
    cmd.set("ray_shadows", 1)
    cmd.set("specular", 0.25)
    cmd.set("ambient", 0.35)
    cmd.set("cartoon_fancy_helices", 1)
    cmd.set("cartoon_smooth_loops", 1)
    cmd.set("cartoon_flat_sheets", 1)
    cmd.set("ray_trace_mode", 1 if outline else 0)
    if outline:
        cmd.set("ray_trace_color", "black")


def style_model(obj=MOL, color_mode="auto"):
    cmd.hide("everything", obj)
    if cmd.count_atoms(f"{obj} and polymer.nucleic") > 0:
        cmd.set("cartoon_ring_mode", 3)
        cmd.set("cartoon_ring_finder", 1)
        cmd.set("cartoon_nucleic_acid_mode", 4)
    cmd.show("cartoon", obj)
    cmd.show("sticks", f"{obj} and organic")
    cmd.show("spheres", f"{obj} and inorganic")
    if color_mode == "rainbow":
        cmd.spectrum("count", "rainbow", f"{obj} and name CA+P")
    elif color_mode == "chain":
        cmd.do(f"util.cbc('{obj}')")
    elif color_mode == "bfactor":
        cmd.spectrum("b", "blue_white_red", obj)
    else:
        if len(cmd.get_chains(obj)) > 1:
            cmd.do(f"util.cbc('{obj}')")
        else:
            cmd.color("teal", obj)
    cmd.do(f"util.cnc('{obj} and (organic or inorganic)')")


def add_density(map_obj, level, around, style, carve, color, transparency):
    if style == "mesh":
        cmd.isomesh(DENS, map_obj, level, around, carve=carve)
        cmd.color(color, DENS)
        cmd.set("mesh_width", 0.4, DENS)
    else:
        cmd.isosurface(DENS, map_obj, level, around, carve=carve)
        cmd.color(color, DENS)
        cmd.set("transparency", transparency, DENS)
        cmd.set("two_sided_lighting", 1)


def load_map_or_simulate(a):
    """Load a real map into 'emap' (return sigma contour) or simulate gaussian
    density from MOL (return level 1.0). Simulate previews a model's expected
    density before a real map exists."""
    if getattr(a, "map", None):
        cmd.load(a.map, "emap")
        return a.level if a.level is not None else mrc_sigma_level(a.map, a.sigma)[0]
    if getattr(a, "simulate", False):
        cmd.map_new("emap", "gaussian", a.sim_grid, MOL, 6)
        return a.level if a.level is not None else 1.0
    sys.exit("ERROR: provide --map (real density) or --simulate (gaussian from model)")


def frame(target, buffer):
    """Orient+zoom on an atom selection; for map/CGO objects (no atoms) frame
    the bounding box via temporary pseudoatoms."""
    if cmd.count_atoms(target) > 0:
        cmd.orient(target)
        cmd.zoom(target, buffer)
    else:
        ext = cmd.get_extent(target)
        cmd.pseudoatom("__bb", pos=list(ext[0]))
        cmd.pseudoatom("__bb", pos=list(ext[1]))
        cmd.zoom("__bb", buffer)
        cmd.delete("__bb")


def save_png(path, width, height, dpi=200):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    cmd.png(path, width=width, height=height, dpi=dpi, ray=1)
    if not (os.path.exists(path) and os.path.getsize(path) > 0):
        raise RuntimeError(f"PyMOL did not write a non-empty PNG: {path}")
    print(f"[render] wrote {path} ({os.path.getsize(path)//1024} KB)")


def encode_movie(frames_dir, prefix, out_mp4, out_gif, fps=24, gif_width=480):
    ff = shutil.which("ffmpeg")
    pattern = os.path.join(frames_dir, f"{prefix}%04d.png")
    if not ff:
        print("[render] ffmpeg not found; frames written, no movie")
        return
    subprocess.run([ff, "-y", "-framerate", str(fps), "-i", pattern,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", "-movflags", "+faststart",
                    out_mp4], check=False, capture_output=True)
    if os.path.exists(out_mp4):
        print(f"[render] wrote {out_mp4} ({os.path.getsize(out_mp4)//1024} KB)")
    pal = os.path.join(frames_dir, "_palette.png")
    vf = f"fps={min(fps,15)},scale={gif_width}:-1:flags=lanczos"
    subprocess.run([ff, "-y", "-i", pattern, "-vf", vf + ",palettegen", pal],
                   check=False, capture_output=True)
    subprocess.run([ff, "-y", "-framerate", str(fps), "-i", pattern, "-i", pal,
                    "-lavfi", f"{vf}[x];[x][1:v]paletteuse", out_gif],
                   check=False, capture_output=True)
    if os.path.exists(out_gif):
        print(f"[render] wrote {out_gif} ({os.path.getsize(out_gif)//1024} KB)")


# ----------------------------- subcommands -----------------------------------

def cmd_map_model(a):
    cmd.load(a.model, MOL)
    level = load_map_or_simulate(a)
    base_scene(a.bg)
    style_model(MOL, a.color)
    add_density("emap", level, MOL, a.map_style, a.carve, a.map_color, a.transparency)
    frame(MOL, a.buffer)
    save_png(a.out, a.width, a.height)
    print(f"[render] contour level (map units) = {level:.4f} (sigma x {a.sigma})")


def cmd_map_surface(a):
    """Map-ALONE density hero. This is a ChimeraX job: PyMOL's headless whole-map
    contour (no VTKm) stalls even on tiny maps, whereas its CARVED isomesh path
    (map-model) is fast. We route here instead of hanging."""
    if not a.map:
        sys.exit("map-surface requires --map")
    # PyMOL swallows stdout in headless mode; route guidance to stderr.
    sys.stderr.write(
        "[render] map-alone isosurface is a ChimeraX task: PyMOL's headless "
        "contour lacks VTKm and stalls on whole maps.\n"
        "[render] Linux:  python3 scripts/cryocore/render/chimerax_render.py "
        f"map-surface --map {a.map} --out {a.out} --execute\n"
        "[render] PyMOL alternative: a carved map+MODEL overlay via "
        "pymol_render.py map-model (fast, real density around the model).\n")
    sys.exit(2)


def cmd_cartoon(a):
    cmd.load(a.model, MOL)
    base_scene(a.bg, outline=a.outline)
    style_model(MOL, a.color)
    frame(MOL, a.buffer)
    save_png(a.out, a.width, a.height)


def cmd_density_zoom(a):
    if not a.map:
        sys.exit("density-zoom requires --map")
    cmd.load(a.model, MOL)
    cmd.load(a.map, "emap")
    level = a.level if a.level is not None else mrc_sigma_level(a.map, a.sigma)[0]
    base_scene(a.bg)
    cmd.hide("everything", MOL)
    cmd.show("cartoon", MOL)
    cmd.set("cartoon_transparency", 0.6, MOL)
    cmd.show("sticks", f"{MOL} and ({a.select})")
    cmd.do(f"util.cnc('{MOL} and ({a.select})')")
    add_density("emap", level, f"{MOL} and ({a.select})", a.map_style,
                a.carve, a.map_color, a.transparency)
    frame(f"{MOL} and ({a.select})", a.buffer)
    save_png(a.out, a.width, a.height)


def cmd_spin(a):
    cmd.load(a.model, MOL)
    base_scene(a.bg)
    style_model(MOL, a.color)
    if a.map or getattr(a, "simulate", False):
        level = load_map_or_simulate(a)
        add_density("emap", level, MOL, a.map_style, a.carve, a.map_color, a.transparency)
    frame(MOL, a.buffer)
    frames_dir = a.frames_dir or os.path.join(
        os.path.dirname(os.path.abspath(a.out_mp4)), "frames")
    os.makedirs(frames_dir, exist_ok=True)
    step = 360.0 / a.frames
    for i in range(a.frames):
        cmd.turn("y", step)
        cmd.png(os.path.join(frames_dir, f"spin_{i:04d}.png"),
                width=a.width, height=a.height, ray=1)
    print(f"[render] wrote {a.frames} frames to {frames_dir}")
    encode_movie(frames_dir, "spin_", a.out_mp4, a.out_gif, fps=a.fps, gif_width=a.gif_width)


# ----------------------------- CLI -------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(description="CryoCore PyMOL headless renderer")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, need_map=True, need_model=True):
        if need_model:
            sp.add_argument("--model", required=True)
        if need_map:
            sp.add_argument("--map", default=None, help="MRC/CCP4 map (omit with --simulate)")
            sp.add_argument("--simulate", action="store_true",
                            help="simulate gaussian density from the model")
            sp.add_argument("--sim-grid", type=float, default=0.6)
        sp.add_argument("--level", type=float, default=None)
        sp.add_argument("--sigma", type=float, default=2.0)
        sp.add_argument("--map-style", choices=["mesh", "surface"], default="mesh")
        sp.add_argument("--map-color", default="grey70")
        sp.add_argument("--transparency", type=float, default=0.5)
        sp.add_argument("--carve", type=float, default=2.5)
        sp.add_argument("--color", default="auto")
        sp.add_argument("--bg", default="white")
        sp.add_argument("--buffer", type=float, default=3.0)
        sp.add_argument("--width", type=int, default=1000)
        sp.add_argument("--height", type=int, default=1000)

    sp = sub.add_parser("map-model"); common(sp); sp.add_argument("--out", required=True)
    sp = sub.add_parser("map-surface"); common(sp, need_model=False); sp.add_argument("--out", required=True)
    sp = sub.add_parser("cartoon"); common(sp, need_map=False); sp.add_argument("--outline", action="store_true"); sp.add_argument("--out", required=True)
    sp = sub.add_parser("density-zoom"); common(sp); sp.add_argument("--select", required=True); sp.add_argument("--out", required=True)
    sp = sub.add_parser("spin"); common(sp)
    sp.add_argument("--frames", type=int, default=48)
    sp.add_argument("--fps", type=int, default=24)
    sp.add_argument("--gif-width", type=int, default=480)
    sp.add_argument("--frames-dir", default=None)
    sp.add_argument("--out-mp4", required=True)
    sp.add_argument("--out-gif", required=True)
    return p


def main():
    argv = sys.argv[1:]
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    args = build_parser().parse_args(argv)
    if not HAVE_PYMOL:
        sys.exit("ERROR: run through PyMOL:  pymol -cqr pymol_render.py -- <subcommand> ...")
    dispatch = {
        "map-model": cmd_map_model, "map-surface": cmd_map_surface,
        "cartoon": cmd_cartoon, "density-zoom": cmd_density_zoom, "spin": cmd_spin,
    }
    try:
        dispatch[args.cmd](args)
    finally:
        try:
            cmd.quit()
        except Exception:
            pass


if __name__ == "__main__" or HAVE_PYMOL:
    main()
