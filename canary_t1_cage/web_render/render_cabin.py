#!/usr/bin/env python3
"""
render_cabin.py — scene A: the Canary unit (ghosted silhouette) in the baggage bay of a generic
high-wing single cabin, three cut-away views.  Label layer OFF: no text anywhere in the images.

    python3 render_cabin.py --out <dir> [--width 2400] [--ss 2] [--views iso,section,plan] [--ghost]

Groups: cabin (full-weight navy edges, #EEF1F5 tones), tail (fading: 0.7x weight, 50 % opacity,
lighter faces), unit (ghost: 0.4x weight, 45 % opacity, near-paper faces).  PNG transparent + white, SVG.

--ghost (2026-10-09 rev): the "you are here" locator.  A whole-airframe hull (grp="ghost", never cut) is
rendered in ITS OWN geometry pass sharing the frame, as hairlines at 0.25x the cut-away weight + a 3 % navy
tint, composited UNDER the section (so the section stays full weight and hides the ghost where it sits),
plus a dashed box marking the sectioned region.  Outputs take a `_ghost` suffix; a `_ghost_only` transparent
PNG carries the ghost + box alone so the site can layer it.
"""
from __future__ import annotations
import argparse
import numpy as np
from pathlib import Path
from PIL import Image
from render_kit import (HERE, export_stl, geometry_pass, edge_layers, compose, save_svg_groups, dashed_layer,
                        downsample, over, GroupStyle, Mesh, load_binstl, save_png, GREY, NAVY)

SCAD = HERE / "canary_cabin_cutaway.scad"
GROUPS = ["cabin", "tail", "unit"]
GHOST_GROUPS = ["ghost", "ghost_wing"]      # fuselage/empennage/gear/prop/struts, and the wing (own hidden-line pass)
STYLES = [GroupStyle(None, 1.0, 1.0, "cabin"),
          GroupStyle((246, 248, 250), 0.7, 0.6, "tailcone_fade", fade_from=0),   # ramps to ~0 away from the cabin group
          GroupStyle((249, 250, 252), 0.4, 0.45, "unit_ghost")]
VIEWS = {  # name: (cut, az, el)
    "iso": ("A1_cutaway_iso_above_left", "iso", 50, 32),
    "section": ("A2_section_side_aft_cabin", "section", 90, 0),
    "plan": ("A3_plan_aft_cabin", "plan", 0, 90),
}
# ghost layer: ~25 % of the cut-away line weight, same navy; 3 % tint; dashed section box at half weight
GHOST = GroupStyle(None, 0.25, 0.7, "airframe_ghost")
GHOST_TINT = 0.03
MARK_W, MARK_A, MARK_DASH = 0.5, 0.55, (14, 9)
# sectioned region (scene mm, from the SCAD: shell x X_BULK-1..X_FWD, outer half-width CAB_W/2+WALL, z -(BELLY+WALL)..CAB_H-BELLY+WALL)
SECTION_BOX = ((-921, 620), (-555, 555), (-180, 1060))
BOX_MARGIN = 90


def box_edges(box, margin):
    (x0, x1), (y0, y1), (z0, z1) = box
    x0, y0, z0 = x0 - margin, y0 - margin, z0 - margin
    x1, y1, z1 = x1 + margin, y1 + margin, z1 + margin
    c = [(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    e = [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (1, 3), (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7)]
    return [(c[a], c[b]) for a, b in e]


def ghost_layer(ps, ghost_passes):
    """Premultiplied RGBA (ss res): ghost faces at 3 % navy, ghost hairlines (one hidden-line pass per ghost part, so the
    wing does not hide the fuselage under it), dashed section box.  Also returns the SVG groups."""
    img = np.zeros((ps.H, ps.W, 4), dtype=np.float32)
    tint = np.zeros((ps.H, ps.W), dtype=np.float32)
    for pg in ghost_passes:
        tint = np.maximum(tint, (pg.gid >= 0).astype(np.float32))
    over(img, NAVY, tint * GHOST_TINT)
    svg = [f'<g id="{GHOST.svg_id}" fill="none" stroke="#0B1F3A" stroke-width="{1.6 * GHOST.edge_w:.2f}" '
           f'stroke-opacity="{GHOST.edge_a:.2f}" stroke-linecap="round">']
    for pg in ghost_passes:
        over(img, NAVY, edge_layers(pg, [GHOST])[0])
        svg += [f'<line x1="{x0 / pg.ss:.1f}" y1="{y0 / pg.ss:.1f}" x2="{x1 / pg.ss:.1f}" y2="{y1 / pg.ss:.1f}"/>' for x0, y0, x1, y1 in pg.segs[0]]
    svg.append("</g>")
    segs = []
    for a, b in box_edges(SECTION_BOX, BOX_MARGIN):
        (xa, ya), (xb, yb) = ps.project([a, b])
        segs.append((xa, ya, xb, yb))
    over(img, NAVY, dashed_layer(ps, segs, MARK_W, *MARK_DASH) * MARK_A)
    svg.append(f'<g id="section_marker" fill="none" stroke="#0B1F3A" stroke-width="{1.6 * MARK_W:.2f}" '
               f'stroke-opacity="{MARK_A:.2f}" stroke-dasharray="{MARK_DASH[0]} {MARK_DASH[1]}">')
    svg += [f'<line x1="{x0 / ps.ss:.1f}" y1="{y0 / ps.ss:.1f}" x2="{x1 / ps.ss:.1f}" y2="{y1 / ps.ss:.1f}"/>' for x0, y0, x1, y1 in segs]
    svg.append("</g>")
    return img, "\n".join(svg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=2400)
    ap.add_argument("--ss", type=int, default=2)
    ap.add_argument("--views", default="iso,section,plan")
    ap.add_argument("--ghost", action="store_true", help="add the whole-airframe ghost locator (outputs *_ghost*)")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    tmp = out / "_mesh"; tmp.mkdir(exist_ok=True)
    fit = "true" if args.ghost else "false"
    sfx = "_ghost" if args.ghost else ""
    for key in args.views.split(","):
        name, cut, az, el = VIEWS[key]
        meshes = []
        for g in GROUPS:
            p = tmp / f"cabin_{g}_{cut}{sfx}.stl"
            export_stl(SCAD, p, {"grp": f'"{g}"', "cut": f'"{cut}"', "ghost_fit": fit})
            meshes.append(Mesh(load_binstl(p), GREY, g))
        print(f"[{name}{sfx}] cut {cut} az {az} el {el}")
        if not args.ghost:
            ps = geometry_pass(meshes, az, el, args.width, args.ss)
            rgba = compose(ps, STYLES, edge_layers(ps, STYLES))
            save_png(rgba, out / f"{name}_transparent.png", out / f"{name}_white.png")
            save_svg_groups(ps, STYLES, out / f"{name}.svg")
            continue
        ghosts = []
        for g in GHOST_GROUPS:
            pgh = tmp / f"cabin_{g}_none.stl"
            export_stl(SCAD, pgh, {"grp": f'"{g}"', "cut": '"none"', "ghost_fit": fit})
            ghosts.append(Mesh(load_binstl(pgh), GREY, g))
        frame = meshes + ghosts
        ps = geometry_pass(meshes, az, el, args.width, args.ss, frame_meshes=frame)
        gps = [geometry_pass([gm], az, el, args.width, args.ss, frame_meshes=frame) for gm in ghosts]
        gimg, gsvg = ghost_layer(ps, gps)
        rgba = compose(ps, STYLES, edge_layers(ps, STYLES), under=gimg)
        save_png(rgba, out / f"{name}{sfx}_transparent.png", out / f"{name}{sfx}_white.png")
        save_svg_groups(ps, STYLES, out / f"{name}{sfx}.svg", extra=gsvg)
        only = downsample(gimg, args.ss)
        Image.fromarray((only * 255 + 0.5).astype(np.uint8), "RGBA").save(out / f"{name}{sfx}_only.png", optimize=True)
    print("done:", out)


if __name__ == "__main__":
    main()
