#!/usr/bin/env python3
"""
render_cutout.py — scene B: hero three-quarter of the unit with the CANARY stencil side plate and a
diffuser behind it.  ONE geometry pass per resolution; every still / frame is composited from it.

    python3 render_cutout.py --out <dir> [--still-width 2400] [--frame-width 1600] [--ss 2]
                             [--what stills,breathe,strobe]

Stills (2400): B1_cutout_led_off, B2_cutout_led_on  (PNG transparent + white, SVG edges).
breathe_00..23 (1600): intensity k = (1 - cos(2*pi*i/24)) / 2 -> 0 -> 1 -> 0 over 2.4 s at 10 fps, loops seamlessly.
strobe_00..11  (1600): hard on/off, 50 % duty (6 on, 6 off).
LED colour #FFC247; off state = flat dark panel #1C283A behind the letters.  No internals exist in the model.
"""
from __future__ import annotations
import argparse, math
from pathlib import Path
import numpy as np
from render_kit import (HERE, export_stl, geometry_pass, edge_layers, compose, save_svg_groups,
                        GroupStyle, Mesh, load_binstl, save_png, gaussian_alpha, over, GREY)
from render_web import WHITE_FACE

SCAD = HERE / "canary_unit_cutout.scad"
GROUPS = ["body", "dome", "diffuser"]
AMBER = (255, 194, 71)      # #FFC247
DARK = (28, 40, 58)         # #1C283A
AZ, EL = -38, 27            # the house hero view (01_hero_iso_dome_end)


def styles(k: float) -> list[GroupStyle]:
    kc = k ** 0.6                                   # colour reaches amber early so mid-breathe reads as dim amber, not olive
    c = tuple(int(round(d + (a - d) * kc)) for d, a in zip(DARK, AMBER))
    return [GroupStyle(None, 1.0, 1.0, "body"), GroupStyle(None, 1.0, 1.0, "dome"), GroupStyle(c, 1.0, 0.0, "diffuser")]


def glow_hook(p, k: float):
    """Emissive spill: tight glow + wide halo around the letter apertures, scaled by k, under the edges."""
    if k <= 0:
        return None
    letters = (p.gid == 2).astype(np.float32)
    ss = p.ss

    def pre(img):
        g1 = np.clip(gaussian_alpha(letters, 9 * ss) * 2.4, 0, 0.62) * k
        g2 = np.clip(gaussian_alpha(letters, 34 * ss) * 1.6, 0, 0.22) * k
        over(img, AMBER, np.clip(g1 + g2 * (1 - g1), 0, 1) * (1 - letters))   # spill around, apertures stay exactly #FFC247
    return pre


def render(p, k, out_png_t, out_png_w, out_svg=None):
    st = styles(k)
    rgba = compose(p, st, edge_layers(p, st), pre=glow_hook(p, k))
    save_png(rgba, out_png_t, out_png_w)
    if out_svg:
        save_svg_groups(p, st, out_svg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--still-width", type=int, default=2400)
    ap.add_argument("--frame-width", type=int, default=1600)
    ap.add_argument("--ss", type=int, default=2)
    ap.add_argument("--what", default="stills,breathe,strobe")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    tmp = out / "_mesh"; tmp.mkdir(exist_ok=True)
    meshes = []
    for g, col in zip(GROUPS, [GREY, WHITE_FACE, GREY]):
        pth = tmp / f"cutout_{g}.stl"
        export_stl(SCAD, pth, {"grp": f'"{g}"'})
        meshes.append(Mesh(load_binstl(pth), col, g))
        print(f"{g}: {len(meshes[-1].F)} tris")
    what = args.what.split(",")
    if "stills" in what:
        print(f"[stills] {args.still_width}px az {AZ} el {EL}")
        p = geometry_pass(meshes, AZ, EL, args.still_width, args.ss)
        render(p, 0.0, out / "B1_cutout_led_off_transparent.png", out / "B1_cutout_led_off_white.png", out / "B1_cutout_led_off.svg")
        render(p, 1.0, out / "B2_cutout_led_on_transparent.png", out / "B2_cutout_led_on_white.png", out / "B2_cutout_led_on.svg")
    if "breathe" in what or "strobe" in what:
        print(f"[frames] {args.frame_width}px")
        p = geometry_pass(meshes, AZ, EL, args.frame_width, args.ss)
        if "breathe" in what:
            for i in range(24):
                k = (1 - math.cos(2 * math.pi * i / 24)) / 2
                render(p, k, out / f"breathe_{i:02d}_transparent.png", out / f"breathe_{i:02d}_white.png")
            print("  breathe: 24 frames, k = (1-cos(2*pi*i/24))/2, 10 fps = 2.4 s period")
        if "strobe" in what:
            for i in range(12):
                k = 1.0 if i < 6 else 0.0
                render(p, k, out / f"strobe_{i:02d}_transparent.png", out / f"strobe_{i:02d}_white.png")
            print("  strobe: 12 frames, 6 on / 6 off")
    print("done:", out)


if __name__ == "__main__":
    main()
