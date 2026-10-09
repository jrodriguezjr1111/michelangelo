#!/usr/bin/env python3
"""CANARY CUTOUT plate for the row-2 bay (t1_sideplates format="cutout", 2026-10-07).

Owner: "a single piece that is 12 inches wide and 80.80 mm tall with the word CANARY as cutouts, and then a single
yellow piece behind it, vented to make the CANARY pop out in yellow."
Two letterings, both sized as large as the plate allows:
  "native"     the house wordmark (t1_panels/brand/canary-wordmark.svg), its own tracking  -> cap ~30
  "condensed"  DIN Condensed Bold (installed; the Saira-Condensed class used on the concept board — Saira itself is not
               installed), with stencil bridges in the A and R counters                     -> cap ~55
Writes cutout_layout_<lettering>.scad (letters with holes, bridges, front field cells, backer cells, pegs, bosses, stats).
"""
import re, json, subprocess
from pathlib import Path
import numpy as np
from matplotlib.path import Path as MPath
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("wl", HERE / "make_wordmark_layout.py"); wl = importlib.util.module_from_spec(spec); spec.loader.exec_module(wl)
OSC = "/opt/homebrew/bin/openscad"

W, H = 304.8, 80.80                       # owner: 12 in x 80.80 mm, sits INSIDE the 81.86 row-2 bay
RIM = 5.0                                 # front rear-rebate rim (full 5.0 thickness round the edge)
WEB_EDGE = 6.0; WEB_LET = 4.0; WEB_BOSS = 6.0
BOSS = [(20, 9.0), (W - 13, 9.0), (20, H - 9.0), (W - 13, H - 9.0)]   # M4 screw bosses (plate coords, origin bottom-left): ends, outside the word
BOSS_D = 14.0
FIN = (30.15, 119.15)                     # EST case-fin span along the plate (frame x 100-189 from the I/O end)
FRONT_HEX = (5.0, 1.6)                    # front field (black, house cell), through front + backer (aligned)
BACK_HEX = (1.6, 0.8)                     # backer under the letters: reads as solid yellow at 3 m, still breathes
BRIDGE_W = 4.5
OFF_FINS = True                           # condensed: keep the word right of the fin zone so the fins see an unbroken vent field


TRACK = 1.08                              # condensed: DIN letter spacing opened 8 % -> >= 4 mm between letters


def din_paths(size=10.0):
    scad = Path("/tmp/_din.scad"); svg = Path("/tmp/_din.svg")
    scad.write_text(f'text("CANARY", size = {size}, font = "DIN Condensed:style=Bold", halign = "left", valign = "baseline", spacing = {TRACK});\n')
    subprocess.run([OSC, "-o", str(svg), str(scad)], capture_output=True, check=True)
    d = re.search(r'd="([^"]+)"', svg.read_text()).group(1)
    subs = []
    for chunk in re.split(r"M", d)[1:]:
        pts = np.array([[float(a), -float(b)] for a, b in re.findall(r"(-?[\d.]+),(-?[\d.]+)", chunk)])
        if len(pts) > 2: subs.append(pts)
    return subs                                   # mm at size 10, y up, baseline 0


def group_letters(subs):
    """outer outlines + the holes inside them -> [(outer, [holes])], sorted left to right"""
    areas = [wl.area(p) for p in subs]
    order = sorted(range(len(subs)), key=lambda i: -areas[i])
    letters = []
    for i in order:
        host = next((L for L in letters if MPath(L[0]).contains_point(subs[i].mean(0))), None)
        if host is None: letters.append((subs[i], []))
        else: host[1].append(subs[i])
    return sorted(letters, key=lambda L: L[0][:, 0].min())


def native_letters():
    G = wl.glyphs()
    return [(g, []) for g in G]


def place(letters, cap0, ux=(RIM + WEB_EDGE, W - RIM - WEB_EDGE)):
    """scale to the largest size that fits the x-range ux and the plate height with the webs; tracking kept"""
    xs0 = min(L[0][:, 0].min() for L in letters); xs1 = max(L[0][:, 0].max() for L in letters)
    ys0 = min(L[0][:, 1].min() for L in letters); ys1 = max(L[0][:, 1].max() for L in letters)
    kx = (ux[1] - ux[0]) / (xs1 - xs0)
    ky = (H - 2 * (RIM + WEB_EDGE)) / (ys1 - ys0)
    k = min(kx, ky)
    ox = (ux[0] + ux[1] - (xs1 - xs0) * k) / 2 - xs0 * k; oy = (H - (ys1 - ys0) * k) / 2 - ys0 * k
    out = [(L[0] * k + [ox, oy], [h * k + [ox, oy] for h in L[1]]) for L in letters]
    return out, k, cap0 * k, ("width" if kx < ky else "height")


def bridges_for(letters):
    br = []
    for outer, holes in letters:
        for h in holes:                                     # vertical bridge from the counter up through the top stroke
            cx = (h[:, 0].min() + h[:, 0].max()) / 2
            br.append((cx - BRIDGE_W / 2, h[:, 1].max() - 0.5, cx + BRIDGE_W / 2, outer[:, 1].max() + 1.0))
    return br


def inside_cut(pts, letters, br):
    """point is in the CUT region: inside an outer, not inside its holes, not on a bridge"""
    m = np.zeros(len(pts), bool)
    for outer, holes in letters:
        a = MPath(outer).contains_points(pts)
        for h in holes: a &= ~MPath(h).contains_points(pts)
        m |= a
    for (x0, y0, x1, y1) in br:
        m &= ~((pts[:, 0] >= x0) & (pts[:, 0] <= x1) & (pts[:, 1] >= y0) & (pts[:, 1] <= y1))
    return m


def edge_dist(pts, letters, br):
    d = np.full(len(pts), np.inf)
    for outer, holes in letters:
        for P in [outer] + holes: d = np.minimum(d, wl.seg_dist(pts, P))
    for (x0, y0, x1, y1) in br:
        R = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]); d = np.minimum(d, wl.seg_dist(pts, R))
    return d


def hexgrid(u0, u1, v0, v1, af, web):
    R = af / np.sqrt(3); px = af + web; py = px * np.sqrt(3) / 2; m = R + web / 2
    c = [(u0 + m + i * px + (j % 2) * px / 2, v0 + m + j * py) for j in range(int((v1 - v0) / py) + 1) for i in range(int((u1 - u0) / px) + 2)]
    c = np.array([p for p in c if p[0] <= u1 - m and p[1] <= v1 - m]); return c, R


def run(lettering):
    if lettering == "native":
        L0 = native_letters(); cap0 = max(g[:, 1].max() for g, _ in L0)
        letters, k, cap, limit = place(L0, cap0)                                    # full width: it needs all of it
    else:
        L0 = group_letters(din_paths(10.0)); cap0 = max(L[0][:, 1].max() for L in L0)    # cap height of C at size 10
        lettering_x = (FIN[1] + WEB_EDGE, W - 13 - BOSS_D / 2 - WEB_BOSS) if OFF_FINS else (RIM + WEB_EDGE, W - RIM - WEB_EDGE)
        letters, k, cap, limit = place(L0, cap0, lettering_x)                       # right of the case fins: the fin zone stays all vent
    br = bridges_for(letters)
    # webs
    polys = [L[0] for L in letters]
    d_ll = min(wl.seg_dist(polys[i], polys[j]).min() for i in range(len(polys)) for j in range(len(polys)) if i != j)
    d_edge = min(min(P[:, 0].min(), W - P[:, 0].max(), P[:, 1].min(), H - P[:, 1].max()) for P in polys)
    d_boss = min(wl.seg_dist(np.array([b]), P).min() for b in BOSS for P in polys) - BOSS_D / 2
    br_w = min((b[2] - b[0]) for b in br) if br else None
    # cut area (raster 0.2)
    gx, gy = np.meshgrid(np.arange(0, W, 0.2), np.arange(0, H, 0.2)); G = np.c_[gx.ravel(), gy.ravel()]
    cut = inside_cut(G, letters, br); a_cut = cut.sum() * 0.04
    a_cut_fin = (cut & (G[:, 0] >= FIN[0]) & (G[:, 0] <= FIN[1])).sum() * 0.04
    # backer fine hex under the letters (cells fully inside the cut region, 0.8 rim)
    Cb, Rb = hexgrid(RIM + 0.5, W - RIM - 0.5, RIM + 0.5, H - RIM - 0.5, *BACK_HEX)
    okb = inside_cut(Cb, letters, br) & (edge_dist(Cb, letters, br) >= Rb + 0.6)
    Cb = Cb[okb]
    # front field (black) outside the letters over the whole rebate area, >= WEB_LET from letters, clear of bosses and pegs
    Cf, Rf = hexgrid(3.0, W - 3.0, 3.0, H - 3.0, *FRONT_HEX)                  # field runs into the full-thickness rim too
    okf = ~inside_cut(Cf, letters, br) & (edge_dist(Cf, letters, br) >= Rf + WEB_LET)
    for b in BOSS: okf &= np.sqrt(((Cf - b) ** 2).sum(1)) >= BOSS_D / 2 + Rf + 2.0
    PEGS = [(W / 2, 7.0), (W / 2, H - 7.0)]                 # two locating pegs (front rebate floor -> backer)
    for p in PEGS: okf &= np.sqrt(((Cf - p) ** 2).sum(1)) >= 1.6 + Rf + 2.0
    Cf = Cf[okf]
    aB = (np.sqrt(3) / 2) * BACK_HEX[0] ** 2; aF = (np.sqrt(3) / 2) * FRONT_HEX[0] ** 2
    fin_b = ((Cb[:, 0] >= FIN[0]) & (Cb[:, 0] <= FIN[1])).sum() * aB; fin_f = ((Cf[:, 0] >= FIN[0]) & (Cf[:, 0] <= FIN[1])).sum() * aF
    st = dict(lettering=lettering, k=k, cap=cap, limit=limit, d_letters=d_ll, d_edge=d_edge, d_boss=d_boss, bridge_w=br_w,
              a_cut_cm2=a_cut / 100, a_cut_fin_cm2=a_cut_fin / 100,
              back_cells=len(Cb), letters_open_cm2=len(Cb) * aB / 100, front_cells=len(Cf), field_open_cm2=len(Cf) * aF / 100,
              fin_open_cm2=(fin_b + fin_f) / 100, fin_letters_cm2=fin_b / 100, fin_field_cm2=fin_f / 100)
    pre = "CN_" if lettering == "native" else "CC_"
    f = HERE / f"cutout_layout_{lettering}.scad"
    with f.open("w") as o:
        o.write(f"// GENERATED by make_cutout_layout.py — do not edit.  {json.dumps({a: (round(b, 2) if isinstance(b, float) else b) for a, b in st.items()})}\n")
        o.write(f"{pre}CAP = {cap:.2f};\n")
        o.write(f"{pre}LETTERS = [\n")
        rows = []
        for outer, holes in letters:
            pts = np.vstack([outer] + holes); paths = []; n = 0
            for P in [outer] + holes: paths.append(list(range(n, n + len(P)))); n += len(P)
            rows.append("  [[" + ", ".join(f"[{x:.2f}, {y:.2f}]" for x, y in pts) + "], " + json.dumps(paths) + "]")
        o.write(",\n".join(rows) + "];\n")
        o.write(f"{pre}BRIDGES = {json.dumps([[round(v, 2) for v in b] for b in br])};\n")
        o.write(f"{pre}CELLS_B = [" + ", ".join(f"[{x:.2f}, {y:.2f}]" for x, y in Cb) + "];\n")
        o.write(f"{pre}CELLS_F = [" + ", ".join(f"[{x:.2f}, {y:.2f}]" for x, y in Cf) + "];\n")
        o.write(f"{pre}STATS = [{st['letters_open_cm2']:.1f}, {st['field_open_cm2']:.1f}, {st['fin_open_cm2']:.1f}, {st['a_cut_cm2']:.1f}];\n")
    if lettering == "native":
        (HERE / "cutout_common.scad").write_text(
            f"// GENERATED by make_cutout_layout.py\nCO_W = {W}; CO_H = {H}; CO_RIM = {RIM}; CO_BOSS = {json.dumps([list(b) for b in BOSS])}; CO_BOSS_D = {BOSS_D};\n"
            f"CO_PEGS = {json.dumps([list(p) for p in PEGS])}; CO_FHEX = {list(FRONT_HEX)}; CO_BHEX = {list(BACK_HEX)}; CO_FIN = {list(FIN)};\n")
    return st


if __name__ == "__main__":
    for lt in ("native", "condensed"):
        s = run(lt)
        print(f"\n[{lt}] CAP HEIGHT {s['cap']:.1f} mm ({s['limit']}-limited)  webs: letter-letter {s['d_letters']:.1f} (>= 4), letter-edge {s['d_edge']:.1f} (>= {RIM + WEB_EDGE}), "
              f"letter-boss {s['d_boss']:.1f} (>= 6)" + (f", stencil bridges {s['bridge_w']:.1f} wide" if s['bridge_w'] else ", no counters -> no bridges"))
        print(f"  letters cut {s['a_cut_cm2']:.1f} cm2 -> through the yellow backer's fine hex ({BACK_HEX[0]} AF / {BACK_HEX[1]}): {s['letters_open_cm2']:.1f} cm2 open; "
              f"black field {s['front_cells']} x {FRONT_HEX[0]} AF = {s['field_open_cm2']:.1f} cm2")
        print(f"  over the case fins (u {FIN}): letters {s['fin_letters_cm2']:.1f} + field {s['fin_field_cm2']:.1f} = {s['fin_open_cm2']:.1f} cm2 "
              f"(R4.2 >= 32 {'MET' if s['fin_open_cm2'] >= 32 else 'NOT MET'}); total open {s['letters_open_cm2'] + s['field_open_cm2']:.1f} cm2")
