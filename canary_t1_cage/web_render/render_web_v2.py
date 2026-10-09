#!/usr/bin/env python3
"""
render_web_v2.py — the 2026-10-09 v2 website set: CAD line-art of canary_unit_web_v2.scad (the re-railed three-row
cage with the one-line stencil CANARY monolith plate) in the house style of render_web.py / render_kit.py.

    python3 render_web_v2.py --out <dir> [--width 2400] [--ss 2] [--views hero,hero_lit,opp,front,side,top,sheet]

Views (same scale rules as the 2026-10-08 set: iso views fit the view with a 7 % margin; the ortho trio shares ONE
scale set by the front view's X extent; the sheet is third-angle at one native scale, top over front, side to the right):
  v2_01_hero_iso_dome_end            az -38 el 27  (from the dome / battery end, wordmark plate facing)
  v2_01b_hero_iso_dome_end_backlit   the same pass, stencil letters emissive #FFC247 with a soft glow (#mark section)
  v2_02_iso_opposite_end             az 142 el 27  (opposite corner, plain plate facing)
  v2_03_ortho_front / _side / _top   az -90 / 0 / top
  v2_03_ortho_sheet
Style: paper white or transparent, navy #0B1F3A feature + silhouette edges, flat #EEF1F5 faces in three orientation
tones (dome one tone), faint contact shadow, amber #E29A1F chevron fills (the only colour), flat dark #1C283A panel
behind the stencil letters (off) / #FFC247 + glow (backlit).  PNG transparent + white, SVG of the visible edges (groups
body / dome / chevron / backer; fills are not exported to the SVG).
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from render_kit import (HERE, export_stl, geometry_pass, edge_layers, compose, save_svg_groups, GroupStyle, Mesh,
                        load_binstl, save_png, gaussian_alpha, over, GREY, NAVY)
from render_web import WHITE_FACE

SCAD = HERE / "canary_unit_web_v2.scad"
GROUPS = ["body", "dome", "chevron", "backer"]
AMBER_FILL = (226, 154, 31)     # #E29A1F chevrons
AMBER_LIT = (255, 194, 71)      # #FFC247 emissive letters
DARK = (28, 40, 58)             # #1C283A panel behind the letters
HERO = (-38, 27); OPP = (142, 27)
FACE_L, DP = 444.5, 279.0       # frame footprint (contact shadow only; echoed by the SCAD)


def styles(lit: bool) -> list[GroupStyle]:
    return [GroupStyle(None, 1.0, 1.0, "body"), GroupStyle(None, 1.0, 1.0, "dome"),
            GroupStyle(AMBER_FILL, 1.0, 1.0, "chevron"), GroupStyle(AMBER_LIT if lit else DARK, 1.0, 0.0, "backer")]


def shadow_layer(p, el: float) -> np.ndarray | None:
    """Premultiplied RGBA (ss resolution) contact shadow: blurred footprint for raised views, a ground line for elevations."""
    H, W, ss = p.H, p.W, p.ss
    fp = np.array([[0, 0, 0], [FACE_L, 0, 0], [FACE_L, DP, 0], [0, DP, 0]], dtype=float)
    pix = p.project(fp)
    sh = Image.new("L", (W, H), 0)
    if el > 0.5:
        ImageDraw.Draw(sh).polygon([tuple(q) for q in pix], fill=255)
        a = gaussian_alpha(np.asarray(sh) / 255.0, 14 * ss) * 0.22
    else:
        xs = pix[:, 0]; yb = pix[:, 1].max()
        ImageDraw.Draw(sh).rectangle([xs.min() + 6 * ss, yb + 1 * ss, xs.max() - 6 * ss, yb + 5 * ss], fill=255)
        a = gaussian_alpha(np.asarray(sh) / 255.0, 6 * ss) * 0.35
    under = np.zeros((H, W, 4), dtype=np.float32)
    under[..., :3] = np.array(NAVY, dtype=np.float32)[None, None] / 255 * a[..., None]
    under[..., 3] = a
    return under


def glow_hook(p):
    letters = (p.gid == 3).astype(np.float32)
    ss = p.ss

    def pre(img):
        g1 = np.clip(gaussian_alpha(letters, 9 * ss) * 2.4, 0, 0.62)
        g2 = np.clip(gaussian_alpha(letters, 34 * ss) * 1.6, 0, 0.22)
        over(img, AMBER_LIT, np.clip(g1 + g2 * (1 - g1), 0, 1) * (1 - letters))   # spill around; apertures stay exactly #FFC247
    return pre


def render(p, name, out: Path, lit=False, shadow=True, el=27.0, svg=True):
    st = styles(lit)
    rgba = compose(p, st, edge_layers(p, st), pre=glow_hook(p) if lit else None, under=shadow_layer(p, el) if shadow else None)
    save_png(rgba, out / f"{name}_transparent.png", out / f"{name}_white.png")
    if svg:
        save_svg_groups(p, st, out / f"{name}.svg")
    print(f"  {name}: {rgba.shape[1]}x{rgba.shape[0]} px (aspect {rgba.shape[1] / rgba.shape[0]:.4f})")
    return rgba


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=2400)
    ap.add_argument("--ss", type=int, default=2)
    ap.add_argument("--views", default="hero,hero_lit,opp,front,side,top,sheet")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    tmp = out / "_mesh"; tmp.mkdir(exist_ok=True)
    meshes = []
    for g, col in zip(GROUPS, [GREY, WHITE_FACE, GREY, GREY]):
        pth = tmp / f"v2_{g}.stl"
        export_stl(SCAD, pth, {"grp": f'"{g}"'})
        meshes.append(Mesh(load_binstl(pth), col, g))
        print(f"{g}: {len(meshes[-1].F)} tris")
    allV = np.concatenate([m.V for m in meshes])
    lo, hi = allV.min(0), allV.max(0)
    print(f"envelope x {lo[0]:.1f}..{hi[0]:.1f}  y {lo[1]:.1f}..{hi[1]:.1f}  z {lo[2]:.1f}..{hi[2]:.1f}")
    views = args.views.split(",")
    if "hero" in views or "hero_lit" in views:
        print(f"[hero] az {HERO[0]} el {HERO[1]}")
        p = geometry_pass(meshes, *HERO, args.width, args.ss)
        if "hero" in views:
            render(p, "v2_01_hero_iso_dome_end", out, el=HERO[1])
        if "hero_lit" in views:
            render(p, "v2_01b_hero_iso_dome_end_backlit", out, lit=True, el=HERO[1])
    if "opp" in views:
        print(f"[opp] az {OPP[0]} el {OPP[1]}")
        p = geometry_pass(meshes, *OPP, args.width, args.ss)
        render(p, "v2_02_iso_opposite_end", out, el=OPP[1])
    # CAD trio at ONE scale: the front view's X extent (frame + battery) sets px/mm; side and top reuse it
    common = args.width * (1 - 2 * 0.07) / (hi[0] - lo[0])
    if "front" in views:
        print("[front] az -90 el 0")
        render(geometry_pass(meshes, -90, 0, args.width, args.ss, scale_override=common), "v2_03_ortho_front", out, el=0)
    if "side" in views:
        print("[side] az 0 el 0 (dome / battery end)")
        render(geometry_pass(meshes, 0, 0, args.width, args.ss, scale_override=common), "v2_03_ortho_side", out, el=0)
    if "top" in views:
        print("[top] el 90")
        render(geometry_pass(meshes, 0, 90, args.width, args.ss, scale_override=common), "v2_03_ortho_top", out, shadow=False)
    if "sheet" in views:
        gap_mm = 60
        sheet_scale = args.width * (1 - 2 * 0.05) / ((hi[0] - lo[0]) + (hi[1] - lo[1]) + gap_mm)
        crops = {}
        for name, az, el in [("top", 0, 90), ("front", -90, 0), ("side", 0, 0)]:
            print(f"[sheet/{name}]")
            p = geometry_pass(meshes, az, el, args.width, args.ss, scale_override=sheet_scale)
            st = styles(False)
            rgba = compose(p, st, edge_layers(p, st))
            a = rgba[..., 3] > 0.002
            ys, xs = np.nonzero(a)
            crops[name] = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        t, f, sd = crops["top"], crops["front"], crops["side"]
        gap = int(round(gap_mm * sheet_scale))
        pad = int(round(0.05 * args.width))
        Ws = max(f.shape[1] + gap + sd.shape[1], t.shape[1]) + 2 * pad
        Hs = t.shape[0] + gap + max(f.shape[0], sd.shape[0]) + 2 * pad
        sheet = np.zeros((Hs, Ws, 4), dtype=np.float32)
        sheet[pad:pad + t.shape[0], pad:pad + t.shape[1]] = t
        y0 = pad + t.shape[0] + gap
        sheet[y0:y0 + f.shape[0], pad:pad + f.shape[1]] = f
        x0 = pad + f.shape[1] + gap
        yb = y0 + f.shape[0] - sd.shape[0]                      # same scale: align the floor lines
        sheet[yb:yb + sd.shape[0], x0:x0 + sd.shape[1]] = sd
        if Ws != args.width:
            im = Image.fromarray((sheet * 255 + 0.5).astype(np.uint8), "RGBA")
            im = im.resize((args.width, int(round(Hs * args.width / Ws))), Image.LANCZOS)
            sheet = np.asarray(im).astype(np.float32) / 255
        save_png(sheet, out / "v2_03_ortho_sheet_transparent.png", out / "v2_03_ortho_sheet_white.png")
        print(f"  v2_03_ortho_sheet: {sheet.shape[1]}x{sheet.shape[0]} px (aspect {sheet.shape[1] / sheet.shape[0]:.4f})")
    print("done:", out)


if __name__ == "__main__":
    main()
