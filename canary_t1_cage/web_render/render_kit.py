#!/usr/bin/env python3
"""
render_kit.py — shared geometry pass + per-group compositing on top of render_web.py's rasteriser.

render_web.render_view() bakes faces, one LED mask and one edge style into a single pass.  The 2026-10-09
scenes need (a) per-group line weight / opacity (ghosted unit, fading tailcone) and (b) many frames
composited from ONE geometry pass (LED breathe / strobe), so the pass and the compose are split here.
Style is unchanged: navy #0B1F3A edges, flat #EEF1F5 faces, paper white or transparent.
"""
from __future__ import annotations
import subprocess, warnings
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from render_web import (Mesh, load_binstl, camera, rasterise, visible_edges, gaussian_alpha, save_png,
                        NAVY, GREY, OSC)

HERE = Path(__file__).resolve().parent
# macOS Accelerate BLAS raises spurious overflow/invalid RuntimeWarnings on small float64 matmuls; results are finite (checked)
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*matmul")


def export_stl(scad: Path, out: Path, defs: dict) -> None:
    args = [OSC, "-q", "--backend=Manifold", "--export-format", "binstl"]
    for k, v in defs.items():
        args += ["-D", f"{k}={v}"]
    r = subprocess.run(args + ["-o", str(out), str(scad)], capture_output=True, text=True)
    if r.returncode or not out.exists():
        raise SystemExit(f"openscad failed ({defs}):\n{r.stderr[-2000:]}")
    if "WARNING" in r.stderr or "ERROR" in r.stderr:
        print(r.stderr.strip())


@dataclass
class GroupStyle:
    face: tuple | None = None          # flat colour override (ghost / dark panel); None = render_web tones of mesh.color
    edge_w: float = 1.0                # multiplier on the house 1.6 px line
    edge_a: float = 1.0                # line opacity
    svg_id: str = "edges"
    fade_from: int | None = None       # screen-x opacity ramp 1 -> FADE_END, starting at the end nearest this group id


FADE_END = 0.06


def fade_ramp(p: "Pass", gi: int, anchor: int) -> np.ndarray:
    """(H, W) multiplier: 1.0 at the group's end nearest the anchor group, FADE_END at its far end (smoothstep)."""
    cols = np.nonzero((p.gid == gi).any(axis=0))[0]
    if len(cols) == 0:
        return np.ones((p.H, p.W), dtype=np.float32)
    x0, x1 = cols.min(), cols.max()
    acols = np.nonzero((p.gid == anchor).any(axis=0))[0]
    ax = acols.mean() if len(acols) else x0
    near, far = (x0, x1) if abs(ax - x0) <= abs(ax - x1) else (x1, x0)
    t = np.clip((np.arange(p.W) - near) / (far - near + 1e-9), 0, 1)
    t = t * t * (3 - 2 * t)
    row = (1 - t) * 1.0 + t * FADE_END
    return np.tile(row.astype(np.float32)[None, :], (p.H, 1))


@dataclass
class Pass:
    meshes: list
    W: int; H: int; ss: int
    zbuf: np.ndarray; rgb: np.ndarray; gid: np.ndarray
    segs: list = field(default_factory=list)      # per group: list of (x0,y0,x1,y1) at ss resolution
    scale: float = 1.0; origin: tuple = (0.0, 0.0); az: float = 0.0; el: float = 0.0

    @property
    def size(self):
        return self.W // self.ss, self.H // self.ss

    def project(self, pts) -> np.ndarray:
        """World points (n, 3) -> pixel (n, 2) at ss resolution in this pass's frame."""
        r, u, v = camera(self.az, self.el)
        P = np.asarray(pts, dtype=float) @ np.stack([r, u, v], axis=1)
        return np.stack([(P[:, 0] - self.origin[0]) * self.scale, self.H - 1 - (P[:, 1] - self.origin[1]) * self.scale], axis=1)


def geometry_pass(meshes, az, el, width, ss, margin=0.07, scale_override=None, frame_meshes=None) -> Pass:
    """frame_meshes: fit the frame to these meshes instead (so several passes share one scale/origin/size)."""
    r, u, v = camera(az, el)
    allP = np.concatenate([m.V for m in (frame_meshes or meshes)]) @ np.stack([r, u, v], axis=1)
    xmin, xmax = allP[:, 0].min(), allP[:, 0].max()
    ymin, ymax = allP[:, 1].min(), allP[:, 1].max()
    W = width * ss
    scale = W * (1 - 2 * margin) / (xmax - xmin) if scale_override is None else scale_override * ss
    mx = (W - (xmax - xmin) * scale) / 2
    H = int(round((ymax - ymin) * scale + 2 * mx))
    my = (H - (ymax - ymin) * scale) / 2
    origin = (xmin - mx / scale, ymin - my / scale)
    zbuf, rgb, gid = rasterise(meshes, r, u, v, scale, origin, W, H)
    segs = [visible_edges([m], r, u, v, scale, origin, W, H, zbuf) for m in meshes]
    print(f"  pass {W // ss}x{H // ss}: " + ", ".join(f"{m.name} {len(s)}" for m, s in zip(meshes, segs)))
    return Pass(meshes, W, H, ss, zbuf, rgb, gid, segs, scale, origin, az, el)


def edge_layers(p: Pass, styles: list[GroupStyle]) -> list[np.ndarray]:
    """One float alpha mask per group (already multiplied by the group's edge opacity)."""
    out = []
    for gi, st in enumerate(styles):
        ed = Image.new("L", (p.W, p.H), 0)
        dr = ImageDraw.Draw(ed)
        lw = max(1, int(round(1.6 * st.edge_w * p.ss)))
        for x0, y0, x1, y1 in p.segs[gi]:
            dr.line([(x0, y0), (x1, y1)], fill=255, width=lw)
        ea = np.asarray(ed).astype(np.float32) / 255 * st.edge_a
        if st.fade_from is not None:
            ea *= fade_ramp(p, gi, st.fade_from)
        out.append(ea)
    return out


def over(img, colour, a):
    """Premultiplied 'over' of a flat colour with per-pixel alpha a (H, W)."""
    c = np.array(colour, dtype=np.float32)[None, None] / 255
    img[..., :3] = c * a[..., None] + img[..., :3] * (1 - a[..., None])
    img[..., 3] = a + img[..., 3] * (1 - a)


def downsample(img: np.ndarray, ss: int) -> np.ndarray:
    """Premultiplied RGBA at ss resolution -> straight-alpha RGBA at output resolution (box filter)."""
    H, W = img.shape[:2]
    Hd, Wd = H // ss, W // ss
    small = img[:Hd * ss, :Wd * ss].reshape(Hd, ss, Wd, ss, 4).mean(axis=(1, 3))
    alpha = small[..., 3:4]
    straight = np.where(alpha > 1e-6, small[..., :3] / np.maximum(alpha, 1e-6), 0)
    return np.concatenate([np.clip(straight, 0, 1), np.clip(alpha, 0, 1)], axis=2)


def compose(p: Pass, styles: list[GroupStyle], edges: list[np.ndarray], pre=None, post=None, under=None) -> np.ndarray:
    """Faces (with per-group flat overrides) -> pre(img) hook -> edges -> post(img) hook -> box downsample.
    under: optional premultiplied RGBA layer (ss resolution) the faces are composited OVER (ghost layers).
    Returns straight-alpha RGBA at output resolution."""
    H, W = p.H, p.W
    img = np.zeros((H, W, 4), dtype=np.float32) if under is None else under.astype(np.float32).copy()
    face_rgb = p.rgb.astype(np.float32) / 255
    for gi, st in enumerate(styles):
        if st.face is not None:
            face_rgb[p.gid == gi] = np.array(st.face, dtype=np.float32) / 255
    fa = (p.gid >= 0).astype(np.float32)
    for gi, st in enumerate(styles):
        if st.fade_from is not None:
            sel = p.gid == gi
            fa[sel] *= fade_ramp(p, gi, st.fade_from)[sel]
    img[..., :3] = face_rgb * fa[..., None] + img[..., :3] * (1 - fa[..., None])
    img[..., 3] = fa + img[..., 3] * (1 - fa)
    if pre:
        pre(img)
    for ea in edges:
        over(img, NAVY, ea)
    if post:
        post(img)
    return downsample(img, p.ss)


def dashed_layer(p: Pass, segs, w_mult: float, dash: float = 14.0, gap: float = 9.0) -> np.ndarray:
    """Float alpha mask (ss resolution) of dashed line segments ((x0,y0,x1,y1) at ss resolution; dash/gap in output px)."""
    ed = Image.new("L", (p.W, p.H), 0)
    dr = ImageDraw.Draw(ed)
    lw = max(1, int(round(1.6 * w_mult * p.ss)))
    d, g = dash * p.ss, gap * p.ss
    for x0, y0, x1, y1 in segs:
        L = float(np.hypot(x1 - x0, y1 - y0))
        t = 0.0
        while t < L:
            t2 = min(t + d, L)
            dr.line([(x0 + (x1 - x0) * t / L, y0 + (y1 - y0) * t / L), (x0 + (x1 - x0) * t2 / L, y0 + (y1 - y0) * t2 / L)],
                    fill=255, width=lw)
            t = t2 + g
    return np.asarray(ed).astype(np.float32) / 255


def save_svg_groups(p: Pass, styles: list[GroupStyle], path: Path, extra: str = "") -> None:
    W, H = p.size
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', extra]
    for gi, st in enumerate(styles):
        parts.append(f'<g id="{st.svg_id}" fill="none" stroke="#0B1F3A" stroke-width="{1.6 * st.edge_w:.2f}" '
                     f'stroke-opacity="{st.edge_a:.2f}" stroke-linecap="round">')
        ramp = fade_ramp(p, gi, st.fade_from)[0] if st.fade_from is not None else None
        for x0, y0, x1, y1 in p.segs[gi]:
            op = "" if ramp is None else f' stroke-opacity="{st.edge_a * ramp[int(np.clip((x0 + x1) / 2, 0, p.W - 1))]:.2f}"'
            parts.append(f'<line x1="{x0 / p.ss:.1f}" y1="{y0 / p.ss:.1f}" x2="{x1 / p.ss:.1f}" y2="{y1 / p.ss:.1f}"{op}/>')
        parts.append("</g>")
    parts.append("</svg>")
    path.write_text("\n".join(parts))
