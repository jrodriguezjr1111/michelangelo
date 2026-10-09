#!/usr/bin/env python3
"""
render_web.py — CAD-style line-art renders of canary_unit_web.scad for the public site.

    python3 render_web.py --out <dir> [--width 2400] [--ss 2] [--views hero,opp,front,side,top,sheet]

Pipeline (no OpenSCAD GUI, no third-party mesh libs — numpy + PIL + scipy only):
  1. openscad exports three colour groups as binary STL: body (grey), dome (white), ledbar (grey / amber).
  2. Orthographic camera -> z-buffer rasteriser (supersampled) gives flat-shaded faces.
  3. Feature edges (dihedral > EDGE_DEG) + silhouette edges, hidden-line removed against the z-buffer,
     drawn as thin navy lines -> PNG (transparent + white) and SVG (visible edge segments only).
Style: paper white, navy #0B1F3A edges, flat light-grey faces #EEF1F5, amber #E29A1F only on the LED bar.
"""
from __future__ import annotations
import argparse, math, subprocess, sys, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = Path(__file__).resolve().parent
SCAD = HERE / "canary_unit_web.scad"
OSC = "/opt/homebrew/bin/openscad"

NAVY = (11, 31, 58)
GREY = (238, 241, 245)          # #EEF1F5
WHITE_FACE = (250, 251, 252)
AMBER = (226, 154, 31)          # #E29A1F
PAPER = (255, 255, 255)
EDGE_DEG = 20.0
EDGE_W_MM = 0.0                 # edges are fixed pixel width, not mm

GROUPS = ["body", "dome", "ledbar"]


# ----------------------------------------------------------------------------- mesh
def export_stl(group: str, out: Path, defs: dict | None = None) -> None:
    args = [OSC, "-q", "--backend=Manifold", "--export-format", "binstl", "-D", f'part="{group}"']
    for k, v in (defs or {}).items():
        args += ["-D", f"{k}={v}"]
    r = subprocess.run(args + ["-o", str(out), str(SCAD)], capture_output=True, text=True)
    if r.returncode or not out.exists():
        raise SystemExit(f"openscad failed ({group}):\n{r.stderr[-2000:]}")


def load_binstl(path: Path) -> np.ndarray:
    buf = path.read_bytes()
    n = int(np.frombuffer(buf[80:84], dtype="<u4")[0])
    rec = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
    tris = np.frombuffer(buf[84:84 + 50 * n], dtype=rec)["v"].astype(np.float64)
    return tris  # (n, 3, 3)


class Mesh:
    def __init__(self, tris: np.ndarray, color, name: str):
        self.name, self.color = name, color
        tris = tris[np.isfinite(tris).all(axis=(1, 2))]
        self.tris = tris
        v = tris.reshape(-1, 3)
        q = np.round(v, 4)
        uniq, inv = np.unique(q, axis=0, return_inverse=True)
        self.V = uniq
        self.F = inv.reshape(-1, 3)
        e1 = self.V[self.F[:, 1]] - self.V[self.F[:, 0]]
        e2 = self.V[self.F[:, 2]] - self.V[self.F[:, 0]]
        n = np.cross(e1, e2)
        l = np.linalg.norm(n, axis=1)
        keep = l > 1e-9
        self.F = self.F[keep]
        self.N = n[keep] / l[keep][:, None]
        # edge table: sorted vertex pairs -> faces
        E = np.concatenate([self.F[:, [0, 1]], self.F[:, [1, 2]], self.F[:, [2, 0]]])
        fid = np.tile(np.arange(len(self.F)), 3)
        Es = np.sort(E, axis=1)
        key = Es[:, 0].astype(np.int64) * len(self.V) + Es[:, 1]
        order = np.argsort(key, kind="stable")
        key, fid, Es = key[order], fid[order], Es[order]
        uk, start, cnt = np.unique(key, return_index=True, return_counts=True)
        self.E = Es[start]                       # (m, 2)
        self.EF0 = fid[start]
        self.EF1 = np.where(cnt > 1, fid[np.minimum(start + 1, len(fid) - 1)], -1)
        n0 = self.N[self.EF0]
        n1 = np.where(self.EF1[:, None] >= 0, self.N[np.maximum(self.EF1, 0)], n0)
        cosang = np.clip((n0 * n1).sum(1), -1, 1)
        self.E_angle = np.degrees(np.arccos(cosang))
        self.E_boundary = self.EF1 < 0


# ----------------------------------------------------------------------------- camera
def camera(az_deg: float, el_deg: float):
    """Orthographic basis. Viewer sits at unit vector v (az from +X about Z, el above the XY plane)."""
    az, el = math.radians(az_deg), math.radians(el_deg)
    v = np.array([math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)])
    if abs(el_deg) > 89.9:                      # top view: +X right, +Y up on the page
        r = np.array([1.0, 0, 0]); u = np.array([0, 1.0, 0])
    else:
        f = -v
        r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r)
        u = np.cross(r, f); u /= np.linalg.norm(u)
    return r, u, v                             # screen x, screen y, depth (toward viewer)


# ----------------------------------------------------------------------------- raster
def shade(color, n, view_v, flat=False):
    """Flat tones by face orientation: top lightest, X faces / Y faces stepped down, oblique + curved one mid tone.
    flat=True (the dome) -> one tone, so a tessellated sphere never shows facet bands."""
    c = np.array(color, dtype=float)
    if flat or abs(n[2]) > 0.7:
        k = 1.0
    elif abs(n[0]) > 0.98:
        k = 0.955
    elif abs(n[1]) > 0.98:
        k = 0.915
    else:
        k = 0.935
    return tuple(int(round(x)) for x in np.clip(c * k, 0, 255))


def rasterise(meshes, r, u, v, scale, origin, W, H):
    """Returns zbuf (H, W) [-inf = empty], rgb (H, W, 3), group id (H, W) [-1 = empty]."""
    zbuf = np.full((H, W), -np.inf, dtype=np.float64)
    rgb = np.zeros((H, W, 3), dtype=np.uint8)
    gid = np.full((H, W), -1, dtype=np.int16)
    for gi, m in enumerate(meshes):
        P = m.V @ np.stack([r, u, v], axis=1)          # (nv, 3): sx, sy, depth
        px = (P[:, 0] - origin[0]) * scale
        py = H - 1 - (P[:, 1] - origin[1]) * scale
        pz = P[:, 2]
        a = px[m.F]; b = py[m.F]; d = pz[m.F]
        # signed area in screen space (y down): front-facing if the mesh normal points to the viewer
        front = (m.N @ v) > 1e-9
        # cache per-colour tones
        tone_cache = {}
        idx = np.nonzero(front)[0]
        for fi in idx:
            x0, x1 = a[fi].min(), a[fi].max()
            y0, y1 = b[fi].min(), b[fi].max()
            ix0, ix1 = max(int(math.floor(x0)), 0), min(int(math.ceil(x1)), W - 1)
            iy0, iy1 = max(int(math.floor(y0)), 0), min(int(math.ceil(y1)), H - 1)
            if ix1 < ix0 or iy1 < iy0:
                continue
            xs = np.arange(ix0, ix1 + 1) + 0.5
            ys = np.arange(iy0, iy1 + 1) + 0.5
            X, Y = np.meshgrid(xs, ys)
            (xa, xb, xc), (ya, yb, yc) = a[fi], b[fi]
            det = (xb - xa) * (yc - ya) - (xc - xa) * (yb - ya)
            if abs(det) < 1e-12:
                continue
            l1 = ((xb - X) * (yc - Y) - (xc - X) * (yb - Y)) / det
            l2 = ((xc - X) * (ya - Y) - (xa - X) * (yc - Y)) / det
            l3 = 1.0 - l1 - l2
            eps = -1e-7
            inside = (l1 >= eps) & (l2 >= eps) & (l3 >= eps)
            if not inside.any():
                continue
            depth = l1 * d[fi][0] + l2 * d[fi][1] + l3 * d[fi][2]
            sub = zbuf[iy0:iy1 + 1, ix0:ix1 + 1]
            upd = inside & (depth > sub)
            if not upd.any():
                continue
            sub[upd] = depth[upd]
            key = (gi, round(m.N[fi][0], 2), round(m.N[fi][1], 2), round(m.N[fi][2], 2))
            tone = tone_cache.get(key)
            if tone is None:
                tone = tone_cache[key] = shade(m.color, m.N[fi], v, flat=(m.name == "dome"))
            rgb[iy0:iy1 + 1, ix0:ix1 + 1][upd] = tone
            gid[iy0:iy1 + 1, ix0:ix1 + 1][upd] = gi
    return zbuf, rgb, gid


# ----------------------------------------------------------------------------- edges
def visible_edges(meshes, r, u, v, scale, origin, W, H, zbuf, step_px=1.0, eps_mm=0.6):
    """Feature + silhouette edges, sampled along their length and tested against a 3x3 min-filtered z-buffer.
    Returns a list of (x0, y0, x1, y1) visible runs in pixel coordinates."""
    zmin = ndimage.minimum_filter(np.where(np.isfinite(zbuf), zbuf, -1e9), size=3)
    segs = []
    for m in meshes:
        P = m.V @ np.stack([r, u, v], axis=1)
        px = (P[:, 0] - origin[0]) * scale
        py = H - 1 - (P[:, 1] - origin[1]) * scale
        pz = P[:, 2]
        fdot = m.N @ v
        f0 = fdot[m.EF0] > 0
        f1 = np.where(m.EF1 >= 0, fdot[np.maximum(m.EF1, 0)] > 0, False)
        silhouette = f0 != f1
        feature = (m.E_angle > EDGE_DEG) | m.E_boundary
        # de-clutter the hex vents: drop the 6 hole-wall edges (short, along Y, between two vertical walls) and the
        # hole's back outline (short silhouette against the plate's back face) -> one hexagon per vent
        ev = m.V[m.E[:, 1]] - m.V[m.E[:, 0]]
        elen = np.linalg.norm(ev, axis=1)
        edir_y = np.abs(ev[:, 1]) / np.maximum(elen, 1e-9)
        n0 = m.N[m.EF0]; n1 = m.N[np.maximum(m.EF1, 0)]
        wall = (elen <= 5.3) & (edir_y > 0.996) & (np.abs(n0[:, 2]) < 0.02) & (np.abs(n1[:, 2]) < 0.02)
        backface_y = np.where(f0, np.abs(n1[:, 1]), np.abs(n0[:, 1])) > 0.999
        back_outline = silhouette & (elen < 4.0) & backface_y
        sel = np.nonzero((feature | silhouette) & (f0 | f1) & ~wall & ~back_outline)[0]
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
            # runs of True
            if not vis.any():
                continue
            d = np.diff(np.concatenate([[0], vis.astype(np.int8), [0]]))
            starts = np.nonzero(d == 1)[0]; ends = np.nonzero(d == -1)[0] - 1
            for s, e in zip(starts, ends):
                if e == s and n > 2:
                    continue  # single-sample specks
                segs.append((xs[s], ys[s], xs[e], ys[e]))
    return segs


# ----------------------------------------------------------------------------- compose
def gaussian_alpha(mask: np.ndarray, sigma: float) -> np.ndarray:
    return ndimage.gaussian_filter(mask.astype(np.float32), sigma)


def render_view(meshes, az, el, width, ss, margin_frac=0.07, led=False, shadow=True, scale_override=None,
                footprint=None, canvas_h=None):
    r, u, v = camera(az, el)
    allP = np.concatenate([m.V for m in meshes]) @ np.stack([r, u, v], axis=1)
    xmin, xmax = allP[:, 0].min(), allP[:, 0].max()
    ymin, ymax = allP[:, 1].min(), allP[:, 1].max()
    W = width * ss
    if scale_override is None:
        scale = W * (1 - 2 * margin_frac) / (xmax - xmin)
    else:
        scale = scale_override * ss
    mx = (W - (xmax - xmin) * scale) / 2
    my = mx if scale_override is None else margin_frac * W
    H = int(round((ymax - ymin) * scale + 2 * my)) if canvas_h is None else canvas_h * ss
    my = (H - (ymax - ymin) * scale) / 2
    origin = (xmin - mx / scale, ymin - my / scale)
    t0 = time.time()
    zbuf, rgb, gid = rasterise(meshes, r, u, v, scale, origin, W, H)
    t1 = time.time()
    segs = visible_edges(meshes, r, u, v, scale, origin, W, H, zbuf)
    t2 = time.time()
    print(f"  raster {t1 - t0:.1f}s, edges {t2 - t1:.1f}s, {len(segs)} segments, canvas {W // ss}x{H // ss}")

    covered = gid >= 0
    # --- layers (premultiplied float RGBA at supersampled res)
    img = np.zeros((H, W, 4), dtype=np.float32)
    # contact shadow: projected footprint polygon, blurred
    if shadow and footprint is not None and el > 0.5:
        fp = footprint @ np.stack([r, u, v], axis=1)
        poly = [((p[0] - origin[0]) * scale, H - 1 - (p[1] - origin[1]) * scale) for p in fp]
        sh = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh).polygon(poly, fill=255)
        a = gaussian_alpha(np.asarray(sh) / 255.0, 14 * ss) * 0.22
        img[..., :3] = np.array(NAVY, dtype=np.float32)[None, None] / 255 * a[..., None]
        img[..., 3] = a
    elif shadow and footprint is not None and abs(el) <= 0.5:
        fp = footprint @ np.stack([r, u, v], axis=1)
        xs = (fp[:, 0] - origin[0]) * scale; yb = H - 1 - (fp[:, 1].min() - origin[1]) * scale
        sh = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh).rectangle([xs.min() + 6 * ss, yb + 1 * ss, xs.max() - 6 * ss, yb + 5 * ss], fill=255)
        a = gaussian_alpha(np.asarray(sh) / 255.0, 6 * ss) * 0.35
        img[..., :3] = np.array(NAVY, dtype=np.float32)[None, None] / 255 * a[..., None]
        img[..., 3] = a
    # faces
    face_rgb = rgb.astype(np.float32) / 255
    if led:
        ledmask = gid == 2
        face_rgb[ledmask] = np.array(AMBER, dtype=np.float32) / 255
    fa = covered.astype(np.float32)
    img[..., :3] = face_rgb * fa[..., None] + img[..., :3] * (1 - fa[..., None])
    img[..., 3] = fa + img[..., 3] * (1 - fa)
    # LED glow (soft, under the edges)
    if led:
        g = gaussian_alpha(ledmask, 9 * ss) * 2.2
        g = np.clip(g, 0, 0.55)
        amber = np.array(AMBER, dtype=np.float32) / 255
        img[..., :3] = amber * g[..., None] + img[..., :3] * (1 - g[..., None])
        img[..., 3] = g + img[..., 3] * (1 - g)
    # edges
    ed = Image.new("L", (W, H), 0)
    dr = ImageDraw.Draw(ed)
    lw = max(1, int(round(1.6 * ss)))
    for x0, y0, x1, y1 in segs:
        dr.line([(x0, y0), (x1, y1)], fill=255, width=lw)
    ea = np.asarray(ed).astype(np.float32) / 255
    navy = np.array(NAVY, dtype=np.float32) / 255
    img[..., :3] = navy * ea[..., None] + img[..., :3] * (1 - ea[..., None])
    img[..., 3] = ea + img[..., 3] * (1 - ea)
    # downsample (box filter on premultiplied colour)
    Hd, Wd = H // ss, W // ss
    small = img[:Hd * ss, :Wd * ss].reshape(Hd, ss, Wd, ss, 4).mean(axis=(1, 3))
    alpha = small[..., 3:4]
    straight = np.where(alpha > 1e-6, small[..., :3] / np.maximum(alpha, 1e-6), 0)
    out_rgba = np.concatenate([np.clip(straight, 0, 1), np.clip(alpha, 0, 1)], axis=2)
    svg_segs = [(x0 / ss, y0 / ss, x1 / ss, y1 / ss) for x0, y0, x1, y1 in segs]
    return out_rgba, svg_segs, (Wd, Hd)


def save_png(rgba: np.ndarray, path_t: Path, path_w: Path):
    arr = (rgba * 255 + 0.5).astype(np.uint8)
    Image.fromarray(arr, "RGBA").save(path_t, optimize=True)
    a = rgba[..., 3:4]
    paper = np.array(PAPER, dtype=np.float32)[None, None] / 255
    comp = rgba[..., :3] * a + paper * (1 - a)
    Image.fromarray((comp * 255 + 0.5).astype(np.uint8), "RGB").save(path_w, optimize=True)


def save_svg(segs, size, path: Path, led_segs=None):
    W, H = size
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
             f'<g fill="none" stroke="#0B1F3A" stroke-width="1.6" stroke-linecap="round">']
    for x0, y0, x1, y1 in segs:
        parts.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    parts.append("</g></svg>")
    path.write_text("\n".join(parts))


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=2400)
    ap.add_argument("--ss", type=int, default=2)
    ap.add_argument("--views", default="hero,hero_led,opp,front,side,top,sheet")
    ap.add_argument("--wordmark", default="true")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    tmp = out / "_mesh"; tmp.mkdir(exist_ok=True)
    meshes = []
    for g, col in zip(GROUPS, [GREY, WHITE_FACE, GREY]):
        p = tmp / f"{g}.stl"
        export_stl(g, p, {"wordmark": args.wordmark})
        meshes.append(Mesh(load_binstl(p), col, g))
        print(f"{g}: {len(meshes[-1].F)} tris, {len(meshes[-1].E)} edges")
    body = meshes[0]
    lo, hi = body.V.min(0), body.V.max(0)
    # footprint of the frame on the floor (battery overhangs, so use the frame rails: x 0..406)
    footprint = np.array([[0, 0, 0], [406, 0, 0], [406, 279, 0], [0, 279, 0]], dtype=float)
    views = args.views.split(",")
    results = {}

    def do(name, az, el, led=False, **kw):
        print(f"[{name}] az {az} el {el}")
        rgba, segs, size = render_view(meshes, az, el, args.width, args.ss, led=led, footprint=footprint, **kw)
        save_png(rgba, out / f"{name}_transparent.png", out / f"{name}_white.png")
        save_svg(segs, size, out / f"{name}.svg")
        results[name] = (rgba, segs, size)

    if "hero" in views:
        do("01_hero_iso_dome_end", az=-38, el=27)
    if "hero_led" in views:
        do("01b_hero_iso_dome_end_ledbar", az=-38, el=27, led=True)
    if "opp" in views:
        do("02_iso_opposite_end", az=142, el=27)
    # CAD trio at ONE scale: the front view (457 wide incl. battery) sets px/mm; side and top reuse it
    span_front = (hi[0] - lo[0]) + 51 + 0  # body includes the battery already
    common = args.width * (1 - 2 * 0.07) / (hi[0] - lo[0])
    if "front" in views:
        do("03_ortho_front", az=-90, el=0, scale_override=common)
    if "side" in views:
        do("03_ortho_side_dome_end", az=0, el=0, scale_override=common)
    if "top" in views:
        do("03_ortho_top", az=0, el=90, scale_override=common, shadow=False)
    if "sheet" in views:
        # third-angle sheet at ONE native scale: top over front, side (dome end) to the right of the front.
        gap_mm = 60
        sheet_scale = args.width * (1 - 2 * 0.05) / ((hi[0] - lo[0]) + (hi[1] - lo[1]) + gap_mm)
        crops = {}
        for name, az, el, sh in [("top", 0, 90, False), ("front", -90, 0, False), ("side", 0, 0, False)]:
            print(f"[sheet/{name}]")
            rgba, segs, size = render_view(meshes, az, el, args.width, args.ss, led=False, footprint=footprint,
                                           scale_override=sheet_scale, shadow=sh)
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
        save_png(sheet, out / "03_ortho_sheet_transparent.png", out / "03_ortho_sheet_white.png")
    print("done:", out)


if __name__ == "__main__":
    main()
