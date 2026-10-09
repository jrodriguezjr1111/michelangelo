#!/usr/bin/env python3
"""
render_web_v3.py — the 2026-10-09 v3 website set: CAD line-art of canary_unit_web_v3.scad (black flush box, antennas
under a clear acrylic top) with the SAME camera, scale, canvas and filenames as the v2 set (a site swap is a file
replacement: every v3 canvas is framed against the v2 meshes' envelope, so the pixel sizes match v2 exactly).

    python3 render_web_v3.py --out <dir> [--width 2400] [--ss 2] [--views hero,hero_lit,opp,front,side,top,sheet]

Views (v2 names with the v3_ prefix):
  v3_01_hero_iso_dome_end            az -38 el 27  (from the battery end, wordmark plate facing)
  v3_01b_hero_iso_dome_end_backlit   the same pass, stencil letters emissive #FFC247 with a soft glow
  v3_02_iso_opposite_end             az 142 el 27  (opposite corner, plain plate facing)
  v3_03_ortho_front / _side / _top   az -90 / 0 / top (one scale, set by the v2 front view's X extent)
  v3_03_ortho_sheet                  third-angle sheet, crops at the v2 crop boxes
Style (dark product on light paper): faces near-black in three orientation tones #1B2129 (top) / #14191F (long faces,
oblique) / #0F1317 (end faces); vent floors #0A0D10; feature edges pale cool grey #C9D2DD at the house 1.6 px, silhouette
edges 1.3x; faint navy contact shadow; amber #E29A1F chevron inlays; backer behind the stencil letters #353E49 (off) /
#FFC247 + glow (backlit).  Acrylic top: a second geometry pass; where the panel is in front, the interior is tinted
#DCE6F0 at 30 % and the interior's edges are drawn ghosted at 45 % (hidden-line see-through, no refraction); the panel's
own outline is drawn at full weight after a z-test against the body.  PNG transparent + white, SVG of the visible edges
(groups body / dome / chevron / backer / acrylic; feature + silhouette sub-groups; ghosted segments carry their opacity).
"""
from __future__ import annotations
import argparse, math
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from render_kit import HERE, export_stl, geometry_pass, compose, edge_layers, GroupStyle, Mesh, load_binstl, save_png, \
    gaussian_alpha, over, GREY, NAVY, downsample
from render_web import camera, rasterise, EDGE_DEG, WHITE_FACE

SCAD = HERE / "canary_unit_web_v3.scad"
SCAD_V2 = HERE / "canary_unit_web_v2.scad"          # framing reference only (canvas parity)
GROUPS = ["body", "dome", "chevron", "backer", "vents"]   # pass A (the opaque world); gid order = this list
ACRYLIC = "acrylic"                                  # pass B
SVG_GROUPS = ["body", "dome", "chevron", "backer"]   # vents carry no edges
BI = {g: i for i, g in enumerate(GROUPS)}

EDGE = (201, 210, 221)          # #C9D2DD
TONE_TOP, TONE_Y, TONE_X = (27, 33, 41), (20, 25, 31), (15, 19, 23)   # #1B2129 / #14191F / #0F1317
DOME_TONE = (178, 188, 199)     # one flat pale tone for the GNSS cap
VENT_BACK = (10, 13, 16)        # #0A0D10 vent floors
AMBER_FILL = (226, 154, 31)     # #E29A1F chevrons
AMBER_LIT = (255, 194, 71)      # #FFC247 emissive letters
BACKER_OFF = (53, 62, 73)       # #353E49: slightly lighter than the face so the letters read on black
ACR_TINT, ACR_A, GHOST = (220, 230, 240), 0.30, 0.45   # #DCE6F0
SIL_W = 1.3                     # silhouette line weight multiplier
HERO = (-38, 27); OPP = (142, 27)
FACE_L, DP = 444.5, 279.0       # frame footprint (contact shadow only; echoed by the SCAD)
# render_web.shade() tones per orientation class on a (255,255,255) mesh colour -> remapped to the house tones
RAW = {255: "top", 244: "x", 233: "y", 238: "obl"}
TONES = {"body": {"top": TONE_TOP, "x": TONE_X, "y": TONE_Y, "obl": TONE_Y},
         "dome": {k: DOME_TONE for k in ("top", "x", "y", "obl")},
         "chevron": {k: AMBER_FILL for k in ("top", "x", "y", "obl")},
         "vents": {k: VENT_BACK for k in ("top", "x", "y", "obl")}}


# ----------------------------------------------------------------------------- edges with a silhouette flag
def visible_edges_v3(m: Mesh, r, u, v, scale, origin, W, H, zbuf, step_px=1.0, eps_mm=0.6):
    """render_web.visible_edges for ONE mesh, returning (feature_segs, silhouette_segs); same de-clutter rules."""
    zmin = ndimage.minimum_filter(np.where(np.isfinite(zbuf), zbuf, -1e9), size=3)
    P = m.V @ np.stack([r, u, v], axis=1)
    px = (P[:, 0] - origin[0]) * scale
    py = H - 1 - (P[:, 1] - origin[1]) * scale
    pz = P[:, 2]
    fdot = m.N @ v
    f0 = fdot[m.EF0] > 0
    f1 = np.where(m.EF1 >= 0, fdot[np.maximum(m.EF1, 0)] > 0, False)
    silhouette = f0 != f1
    feature = (m.E_angle > EDGE_DEG) | m.E_boundary
    ev = m.V[m.E[:, 1]] - m.V[m.E[:, 0]]
    elen = np.linalg.norm(ev, axis=1)
    edir_y = np.abs(ev[:, 1]) / np.maximum(elen, 1e-9)
    n0 = m.N[m.EF0]; n1 = m.N[np.maximum(m.EF1, 0)]
    wall = (elen <= 5.3) & (edir_y > 0.996) & (np.abs(n0[:, 2]) < 0.02) & (np.abs(n1[:, 2]) < 0.02)
    backface_y = np.where(f0, np.abs(n1[:, 1]), np.abs(n0[:, 1])) > 0.999
    back_outline = silhouette & (elen < 4.0) & backface_y
    sel = np.nonzero((feature | silhouette) & (f0 | f1) & ~wall & ~back_outline)[0]
    out = ([], [])
    for ei in sel:
        i0, i1 = m.E[ei]
        x0, y0, z0 = px[i0], py[i0], pz[i0]
        x1, y1, z1 = px[i1], py[i1], pz[i1]
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(int(L / step_px) + 1, 2)
        t = np.linspace(0, 1, n)
        xs = x0 + (x1 - x0) * t; ys = y0 + (y1 - y0) * t; zs = z0 + (z1 - z0) * t
        ix = np.clip(np.round(xs).astype(int), 0, W - 1)
        iy = np.clip(np.round(ys).astype(int), 0, H - 1)
        vis = zs >= zmin[iy, ix] - eps_mm
        if not vis.any():
            continue
        d = np.diff(np.concatenate([[0], vis.astype(np.int8), [0]]))
        starts = np.nonzero(d == 1)[0]; ends = np.nonzero(d == -1)[0] - 1
        dst = out[1] if silhouette[ei] else out[0]
        for s, e in zip(starts, ends):
            if e == s and n > 2:
                continue
            dst.append((xs[s], ys[s], xs[e], ys[e]))
    return out


# ----------------------------------------------------------------------------- the two-pass geometry
@dataclass
class PassV3:
    W: int; H: int; ss: int
    zA: np.ndarray; rgbA: np.ndarray; gidA: np.ndarray
    segsA: list                              # per group: (feature, silhouette)
    segsB: tuple                             # acrylic: (feature, silhouette)
    cover: np.ndarray                        # bool (H, W): acrylic in front of the opaque world
    scale: float; origin: tuple; az: float; el: float

    @property
    def size(self):
        return self.W // self.ss, self.H // self.ss

    def project(self, pts):
        r, u, v = camera(self.az, self.el)
        P = np.asarray(pts, dtype=float) @ np.stack([r, u, v], axis=1)
        return np.stack([(P[:, 0] - self.origin[0]) * self.scale, self.H - 1 - (P[:, 1] - self.origin[1]) * self.scale], axis=1)


def frame(frame_meshes, az, el, width, ss, margin=0.07, scale_override=None):
    """Canvas, scale and origin exactly as render_kit.geometry_pass computes them for frame_meshes (the v2 set)."""
    r, u, v = camera(az, el)
    allP = np.concatenate([m.V for m in frame_meshes]) @ np.stack([r, u, v], axis=1)
    xmin, xmax = allP[:, 0].min(), allP[:, 0].max()
    ymin, ymax = allP[:, 1].min(), allP[:, 1].max()
    W = width * ss
    scale = W * (1 - 2 * margin) / (xmax - xmin) if scale_override is None else scale_override * ss
    mx = (W - (xmax - xmin) * scale) / 2
    H = int(round((ymax - ymin) * scale + 2 * mx))
    my = (H - (ymax - ymin) * scale) / 2
    return r, u, v, W, H, scale, (xmin - mx / scale, ymin - my / scale)


def pass_v3(meshesA, acr: Mesh, frame_meshes, az, el, width, ss, scale_override=None) -> PassV3:
    r, u, v, W, H, scale, origin = frame(frame_meshes, az, el, width, ss, scale_override=scale_override)
    zA, rgbA, gidA = rasterise(meshesA, r, u, v, scale, origin, W, H)
    segsA = [visible_edges_v3(m, r, u, v, scale, origin, W, H, zA) for m in meshesA]
    zB, _, gidB = rasterise([acr], r, u, v, scale, origin, W, H)
    zc = np.maximum(zA, zB)
    segsB = visible_edges_v3(acr, r, u, v, scale, origin, W, H, zc)
    cover = (gidB >= 0) & (zB > zA + 0.02)
    print(f"  pass {W // ss}x{H // ss}: " + ", ".join(f"{m.name} {len(s[0])}+{len(s[1])}" for m, s in zip(meshesA, segsA))
          + f", acrylic {len(segsB[0])}+{len(segsB[1])}; acrylic covers {cover.mean() * 100:.1f} % of the canvas")
    return PassV3(W, H, ss, zA, rgbA, gidA, segsA, segsB, cover, scale, origin, az, el)


# ----------------------------------------------------------------------------- compose
def line_mask(p: PassV3, segs: tuple, w_mult: float = 1.0) -> np.ndarray:
    ed = Image.new("L", (p.W, p.H), 0)
    dr = ImageDraw.Draw(ed)
    for ss_segs, wm in ((segs[0], 1.0), (segs[1], SIL_W)):
        lw = max(1, int(round(1.6 * w_mult * wm * p.ss)))
        for x0, y0, x1, y1 in ss_segs:
            dr.line([(x0, y0), (x1, y1)], fill=255, width=lw)
    return np.asarray(ed).astype(np.float32) / 255


def shadow_layer(p: PassV3, el: float) -> np.ndarray:
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


def compose_v3(p: PassV3, lit: bool, under: np.ndarray | None) -> np.ndarray:
    H, W, ss = p.H, p.W, p.ss
    img = np.zeros((H, W, 4), dtype=np.float32) if under is None else under.copy()
    # faces: remap the rasteriser's orientation tones to the house near-blacks, per group
    face = np.zeros((H, W, 3), dtype=np.float32)
    raw = p.rgbA[..., 0]
    for g in GROUPS:
        gi = BI[g]
        if g == "backer":
            face[p.gidA == gi] = np.array(AMBER_LIT if lit else BACKER_OFF, dtype=np.float32) / 255
            continue
        for val, key in RAW.items():
            sel = (p.gidA == gi) & (raw == val)
            face[sel] = np.array(TONES[g][key], dtype=np.float32) / 255
    unmapped = int(((p.gidA >= 0) & (p.gidA != BI["backer"]) & ~np.isin(raw, list(RAW))).sum())
    assert unmapped == 0, f"{unmapped} face pixels carry a tone outside the RAW map"
    fa = (p.gidA >= 0).astype(np.float32)
    img[..., :3] = face * fa[..., None] + img[..., :3] * (1 - fa[..., None])
    img[..., 3] = fa + img[..., 3] * (1 - fa)
    if lit:                                                     # glow spill around the apertures (apertures stay exactly #FFC247)
        letters = (p.gidA == BI["backer"]).astype(np.float32)
        g1 = np.clip(gaussian_alpha(letters, 9 * ss) * 2.4, 0, 0.62)
        g2 = np.clip(gaussian_alpha(letters, 34 * ss) * 1.6, 0, 0.22)
        over(img, AMBER_LIT, np.clip(g1 + g2 * (1 - g1), 0, 1) * (1 - letters))
    over(img, ACR_TINT, ACR_A * p.cover.astype(np.float32))    # the acrylic panel over the interior
    ghost = np.where(p.cover, GHOST, 1.0).astype(np.float32)
    for g in GROUPS:
        if g == "vents":
            continue
        over(img, EDGE, line_mask(p, p.segsA[BI[g]]) * ghost)  # interior edges ghosted through the panel
    over(img, EDGE, line_mask(p, p.segsB))                      # the panel's own outline
    return downsample(img, ss)


def save_svg_v3(p: PassV3, path: Path) -> None:
    W, H = p.size
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']

    def seg_line(x0, y0, x1, y1, ghosted):
        op = f' stroke-opacity="{GHOST:.2f}"' if ghosted else ""
        return f'<line x1="{x0 / p.ss:.1f}" y1="{y0 / p.ss:.1f}" x2="{x1 / p.ss:.1f}" y2="{y1 / p.ss:.1f}"{op}/>'

    def group(gid, segs, ghost_test):
        parts.append(f'<g id="{gid}" fill="none" stroke="#C9D2DD" stroke-linecap="round">')
        for cls, ss_segs, wm in (("feature", segs[0], 1.0), ("silhouette", segs[1], SIL_W)):
            parts.append(f'<g class="{cls}" stroke-width="{1.6 * wm:.2f}">')
            for x0, y0, x1, y1 in ss_segs:
                parts.append(seg_line(x0, y0, x1, y1, ghost_test(x0, y0, x1, y1)))
            parts.append("</g>")
        parts.append("</g>")

    def covered(x0, y0, x1, y1):
        ix = int(np.clip((x0 + x1) / 2, 0, p.W - 1)); iy = int(np.clip((y0 + y1) / 2, 0, p.H - 1))
        return bool(p.cover[iy, ix])

    for g in SVG_GROUPS:
        group(g, p.segsA[BI[g]], covered)
    group(ACRYLIC, p.segsB, lambda *a: False)
    parts.append("</svg>")
    path.write_text("\n".join(parts))


def render(p: PassV3, name: str, out: Path, lit=False, shadow=True, el=27.0, svg=True):
    rgba = compose_v3(p, lit, shadow_layer(p, el) if shadow else None)
    save_png(rgba, out / f"{name}_transparent.png", out / f"{name}_white.png")
    if svg:
        save_svg_v3(p, out / f"{name}.svg")
    print(f"  {name}: {rgba.shape[1]}x{rgba.shape[0]} px (aspect {rgba.shape[1] / rgba.shape[0]:.4f})")
    return rgba


def alpha_box(rgba):
    a = rgba[..., 3] > 0.002
    ys, xs = np.nonzero(a)
    return ys.min(), ys.max(), xs.min(), xs.max()


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=2400)
    ap.add_argument("--ss", type=int, default=2)
    ap.add_argument("--views", default="hero,hero_lit,opp,front,side,top,sheet")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    tmp = out / "_mesh"; tmp.mkdir(exist_ok=True)
    white = (255, 255, 255)                                  # tones are remapped in compose_v3 (see RAW / TONES)
    meshes = []
    for g in GROUPS:
        pth = tmp / f"v3_{g}.stl"
        export_stl(SCAD, pth, {"grp": f'"{g}"'})
        meshes.append(Mesh(load_binstl(pth), white, g))
        print(f"{g}: {len(meshes[-1].F)} tris")
    pth = tmp / f"v3_{ACRYLIC}.stl"
    export_stl(SCAD, pth, {"grp": f'"{ACRYLIC}"'})
    acr = Mesh(load_binstl(pth), white, ACRYLIC)
    print(f"{ACRYLIC}: {len(acr.F)} tris")
    # v2 framing reference: the v2 body + dome meshes set every canvas / scale / crop box (chevron + backer lie inside them)
    v2 = []
    for g, col in (("body", GREY), ("dome", WHITE_FACE)):
        pth = tmp / f"v2ref_{g}.stl"
        export_stl(SCAD_V2, pth, {"grp": f'"{g}"'})
        v2.append(Mesh(load_binstl(pth), col, g))
    allV = np.concatenate([m.V for m in meshes + [acr]])
    lo, hi = allV.min(0), allV.max(0)
    v2V = np.concatenate([m.V for m in v2])
    lo2, hi2 = v2V.min(0), v2V.max(0)
    print(f"v3 envelope x {lo[0]:.1f}..{hi[0]:.1f}  y {lo[1]:.1f}..{hi[1]:.1f}  z {lo[2]:.1f}..{hi[2]:.1f}")
    print(f"v2 framing  x {lo2[0]:.1f}..{hi2[0]:.1f}  y {lo2[1]:.1f}..{hi2[1]:.1f}  z {lo2[2]:.1f}..{hi2[2]:.1f}")
    assert (lo >= lo2 - 1e-6).all() and (hi <= hi2 + 1e-6).all(), "v3 geometry leaves the v2 framing envelope"
    views = args.views.split(",")
    if "hero" in views or "hero_lit" in views:
        print(f"[hero] az {HERO[0]} el {HERO[1]}")
        p = pass_v3(meshes, acr, v2, *HERO, args.width, args.ss)
        if "hero" in views:
            render(p, "v3_01_hero_iso_dome_end", out, el=HERO[1])
        if "hero_lit" in views:
            render(p, "v3_01b_hero_iso_dome_end_backlit", out, lit=True, el=HERO[1])
    if "opp" in views:
        print(f"[opp] az {OPP[0]} el {OPP[1]}")
        p = pass_v3(meshes, acr, v2, *OPP, args.width, args.ss)
        render(p, "v3_02_iso_opposite_end", out, el=OPP[1])
    # CAD trio at ONE scale: the v2 front view's X extent (frame + battery; identical in v3) sets px/mm
    common = args.width * (1 - 2 * 0.07) / (hi2[0] - lo2[0])
    if "front" in views:
        print("[front] az -90 el 0")
        render(pass_v3(meshes, acr, v2, -90, 0, args.width, args.ss, scale_override=common), "v3_03_ortho_front", out, el=0)
    if "side" in views:
        print("[side] az 0 el 0 (battery end)")
        render(pass_v3(meshes, acr, v2, 0, 0, args.width, args.ss, scale_override=common), "v3_03_ortho_side", out, el=0)
    if "top" in views:
        print("[top] el 90")
        render(pass_v3(meshes, acr, v2, 0, 90, args.width, args.ss, scale_override=common), "v3_03_ortho_top", out, shadow=False)
    if "sheet" in views:
        # third-angle sheet at ONE native scale (v2 rule); each crop box is the v2 render's alpha box (the v3 box lies inside it)
        gap_mm = 60
        sheet_scale = args.width * (1 - 2 * 0.05) / ((hi2[0] - lo2[0]) + (hi2[1] - lo2[1]) + gap_mm)
        crops = {}
        v2_styles = [GroupStyle(None, 1.0, 1.0, "body"), GroupStyle(None, 1.0, 1.0, "dome")]
        for name, az, el in [("top", 0, 90), ("front", -90, 0), ("side", 0, 0)]:
            print(f"[sheet/{name}]")
            p = pass_v3(meshes, acr, v2, az, el, args.width, args.ss, scale_override=sheet_scale)
            rgba = compose_v3(p, False, None)
            print(f"  [sheet/{name}] v2 reference crop pass")
            p2 = geometry_pass(v2, az, el, args.width, args.ss, scale_override=sheet_scale)
            rgba2 = compose(p2, v2_styles, edge_layers(p2, v2_styles))
            b3, b2 = alpha_box(rgba), alpha_box(rgba2)
            y0, y1, x0, x1 = min(b3[0], b2[0]), max(b3[1], b2[1]), min(b3[2], b2[2]), max(b3[3], b2[3])
            print(f"  crop v3 {b3} v2 {b2} -> {(y0, y1, x0, x1)}")
            crops[name] = rgba[y0:y1 + 1, x0:x1 + 1]
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
        save_png(sheet, out / "v3_03_ortho_sheet_transparent.png", out / "v3_03_ortho_sheet_white.png")
        print(f"  v3_03_ortho_sheet: {sheet.shape[1]}x{sheet.shape[0]} px (aspect {sheet.shape[1] / sheet.shape[0]:.4f})")
    print("done:", out)


if __name__ == "__main__":
    main()
