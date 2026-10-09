#!/usr/bin/env python3
"""CANARY monolith layout for t1_sideplates (2026-10-07).

Parses the REAL wordmark (t1_panels/brand/canary-wordmark.svg: six single-outline glyphs, letter spacing kept), sizes it
as large as the 304.8 plate allows, places the vertical seam in a letter gap, lays a micro-hex (3.2 AF / 1.2 web; stencil fill round the letters and the applique field)
(applique) round the letters, checks webs, and writes wm_layout_<layout>.scad for make_t1_sideplates.scad to include.
    layouts: "twoline"  CAN over ARY (CAN in row 2 over the case fins, ARY in row 1)  — RECOMMENDED, cap ~63
             "oneline"  CANARY on one line in row 2, seam in the N|A gap ("CAN|ARY") — cap ~30
"""
import re, json
from pathlib import Path
import numpy as np
from matplotlib.path import Path as MPath

HERE = Path(__file__).resolve().parent
SVG = HERE.parent / "t1_panels" / "brand" / "canary-wordmark.svg"
# frame (must match make_t1_sideplates.scad)
ROW_H = [92.56, 81.86, 40.96]; RAIL = 20
RZ = [0, RAIL + ROW_H[0], 2 * RAIL + ROW_H[0] + ROW_H[1], 3 * RAIL + sum(ROW_H)]
SLOT = [z + RAIL / 2 for z in RZ]
BAY = [(RZ[i] + RAIL, RZ[i + 1]) for i in range(3)]
W = 304.8; X0 = (444.5 - W) / 2
EDGE_IN = 2.0; MZ0, MZ1 = SLOT[0] - EDGE_IN, SLOT[3] + EDGE_IN            # 279.38 tall: fits the 281 bed
MARGIN = 12.0
FIN = (30.15, 119.15, BAY[1][0], BAY[1][1])                                # EST case-fin zone (frame x 100-189 from the I/O end), row 2
SEAT_R = 11.6 / 2
HEX = {"stencil": (3.2, 1.2), "applique": (3.2, 1.2)}                      # AF, web: micro-hex (the house 5 AF loses too much round the letters)
PEG_D = 4.0; PEG_RIM = 1.6; GAP = 2.5                                     # applique: letters stand GAP off the face on 3 x O4 pegs each (0.2 press-fit), hex runs under them


def glyphs():
    s = SVG.read_text()
    out = []
    for m in re.finditer(r'translate\(([\d.]+),0\) scale\(([\d.]+),-?[\d.]+\)" d="([^"]+)"', s):
        tx, sc, d = float(m.group(1)), float(m.group(2)), m.group(3)
        toks = re.findall(r"[MLHVCZ]|-?\d+\.?\d*", d)
        pts, cur, cmd, i = [], (0, 0), None, 0
        while i < len(toks):
            t = toks[i]
            if t in "MLHVCZ":
                cmd = t; i += 1
                if cmd == "Z": continue
            if cmd in ("M", "L"):
                cur = (float(toks[i]), float(toks[i + 1])); pts.append(cur); i += 2
                if cmd == "M": cmd = "L"
            elif cmd == "H":
                cur = (float(toks[i]), cur[1]); pts.append(cur); i += 1
            elif cmd == "V":
                cur = (cur[0], float(toks[i])); pts.append(cur); i += 1
            elif cmd == "C":
                p1 = (float(toks[i]), float(toks[i + 1])); p2 = (float(toks[i + 2]), float(toks[i + 3])); p3 = (float(toks[i + 4]), float(toks[i + 5]))
                for t_ in np.linspace(0, 1, 13)[1:]:
                    a = (1 - t_) ** 3; b = 3 * (1 - t_) ** 2 * t_; c = 3 * (1 - t_) * t_ ** 2; e = t_ ** 3
                    pts.append((a * cur[0] + b * p1[0] + c * p2[0] + e * p3[0], a * cur[1] + b * p1[1] + c * p2[1] + e * p3[1]))
                cur = p3; i += 6
            else:
                i += 1
        P = np.array([(tx + sc * x, sc * y) for x, y in pts])           # SVG units, y up, baseline 0
        if np.allclose(P[0], P[-1]): P = P[:-1]
        out.append(P)
    return out


def area(P):
    x, y = P[:, 0], P[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def seg_dist(pts, P):
    """min distance from each point in pts (N,2) to the closed polyline P (M,2)."""
    A = P; B = np.roll(P, -1, axis=0); AB = B - A; L2 = (AB ** 2).sum(1); L2[L2 == 0] = 1e-12
    d = np.full(len(pts), np.inf)
    for k in range(0, len(pts), 2000):
        q = pts[k:k + 2000][:, None, :]
        t = np.clip(((q - A) * AB).sum(2) / L2, 0, 1)
        proj = A + t[..., None] * AB
        d[k:k + 2000] = np.sqrt(((q - proj) ** 2).sum(2)).min(1)
    return d


def layout(name):
    G = glyphs()
    names = ["C", "A", "N", "A", "R", "Y"]
    xmin = [g[:, 0].min() for g in G]; xmax = [g[:, 0].max() for g in G]
    cap = max(g[:, 1].max() for g in G)
    lines = [[0, 1, 2], [3, 4, 5]] if name == "twoline" else [[0, 1, 2, 3, 4, 5]]
    widths = [xmax[l[-1]] - xmin[l[0]] for l in lines]
    k = (W - 2 * MARGIN) / max(widths)
    # line offsets: the widest line sits on the margins; the narrower line slides inside its slack so that a letter gap
    # is common to BOTH lines (the vertical seam runs in it) — widest common gap wins, then the most central
    def place(offs):
        L_ = []
        for li, l in enumerate(lines):
            bay = BAY[1] if li == 0 else BAY[0]                              # line 1 over the case fins (row 2), line 2 in row 1
            zc = (bay[0] + bay[1]) / 2; z0 = zc - cap * k / 2
            for g in l:
                L_.append((names[g], np.c_[(G[g][:, 0] - xmin[l[0]]) * k + offs[li], G[g][:, 1] * k + z0], li))
        return L_
    def gaps_of(L_):
        out_ = []
        for li in range(len(lines)):
            Ls = sorted([L for L in L_ if L[2] == li], key=lambda L: L[1][:, 0].min())
            out_.append([(Ls[i][1][:, 0].max(), Ls[i + 1][1][:, 0].min()) for i in range(len(Ls) - 1)])
        return out_
    best = None
    slack = [W - 2 * MARGIN - w * k for w in widths]
    for o1 in np.arange(0, slack[0] + 0.01, 0.25):
        for o2 in (np.arange(0, slack[1] + 0.01, 0.25) if len(lines) > 1 else [0]):
            offs = [MARGIN + o1, MARGIN + o2]
            gp = gaps_of(place(offs))
            for a in gp[0]:
                for b in (gp[1] if len(gp) > 1 else [(-1e9, 1e9)]):
                    lo, hi = max(a[0], b[0]), min(a[1], b[1]); mid = (lo + hi) / 2
                    if hi - lo <= 8 or mid > 281 or W - mid > 281: continue          # >= 4 web each side
                    if FIN[0] - 12 < mid < FIN[1] + 12: continue                       # keep the seam strip off the case fins
                    score = (round(hi - lo, 1), -abs(mid - W / 2))
                    if best is None or score > best[0]: best = (score, (lo, hi), offs)
    relaxed = False
    if best is None:                                                          # one-line: the N|A gap is the only central gap -> take it, flag the web
        relaxed = True
        for o1 in [0.0]:
            gp = gaps_of(place([MARGIN + o1, MARGIN]))
            a = min(gp[0], key=lambda g: abs((g[0] + g[1]) / 2 - W / 2)); best = (None, a, [MARGIN + o1, MARGIN])
    letters = place(best[2]); best = best[1]
    seam = (best[0] + best[1]) / 2
    seam_web = (best[1] - best[0]) / 2
    # bolts (must match the SCAD): 4 per slot row
    bu = [32, 118, seam - 14, (seam + W) / 2]
    bolts = np.array([(u, z) for z in SLOT for u in bu])
    # stencil webs
    polys = [L[1] for L in letters]
    d_letters = min(seg_dist(polys[i], polys[j]).min() for i in range(len(polys)) for j in range(len(polys)) if i != j)
    d_bolt = min(seg_dist(bolts, P).min() for P in polys) - SEAT_R
    d_edge = min(min(P[:, 0].min(), W - P[:, 0].max(), P[:, 1].min() - MZ0, MZ1 - P[:, 1].max()) for P in polys)
    d_rail = min(min(P[:, 1].min() - BAY[L[2] == 0 and 1 or 0][0], BAY[L[2] == 0 and 1 or 0][1] - P[:, 1].max()) for L, P in zip(letters, polys))
    neck = np.inf                                                              # plate necks inside a letter's own concavities
    for P in polys:
        seg = np.r_[0, np.cumsum(np.sqrt((np.diff(np.r_[P, P[:1]], axis=0) ** 2).sum(1)))]
        n = int(seg[-1] / 0.5); s = np.linspace(0, seg[-1], n, endpoint=False)
        Q = np.c_[np.interp(s, seg, np.r_[P[:, 0], P[0, 0]]), np.interp(s, seg, np.r_[P[:, 1], P[0, 1]])]
        path = MPath(P)
        D = np.sqrt(((Q[:, None] - Q[None]) ** 2).sum(2)); arc = np.abs(s[:, None] - s[None]); arc = np.minimum(arc, seg[-1] - arc)
        cand = np.argwhere((arc > 20) & (D < 12))
        for i, j in cand:
            if i < j and not path.contains_point(((Q[i] + Q[j]) / 2)):
                neck = min(neck, D[i, j])
    # letter open areas (stencil) total + over the fin zone (raster)
    a_letters = sum(area(P) for P in polys)
    gx, gy = np.meshgrid(np.arange(FIN[0], FIN[1], 0.25), np.arange(FIN[2], FIN[3], 0.25)); G2 = np.c_[gx.ravel(), gy.ravel()]
    infin = np.zeros(len(G2), bool)
    for P in polys: infin |= MPath(P).contains_points(G2)
    a_letters_fin = infin.sum() * 0.0625
    # hex cells
    # applique pegs: 3 per letter, >= PEG_RIM inside the outline, spread out (greedy farthest-point)
    pegs, peg_of = [], []
    for li, P in enumerate(polys):
        x0, x1, y0, y1 = P[:, 0].min(), P[:, 0].max(), P[:, 1].min(), P[:, 1].max()
        gx, gy = np.meshgrid(np.arange(x0, x1, 1.0), np.arange(y0, y1, 1.0)); Q = np.c_[gx.ravel(), gy.ravel()]
        Q = Q[MPath(P).contains_points(Q)]; dq = seg_dist(Q, P); Q = Q[dq >= min(PEG_D / 2 + PEG_RIM, dq.max() * 0.9)]   # thin strokes (one-line): best available
        pick = [Q[np.argmax(seg_dist(Q, P))]]
        for _ in range(2):
            dd = np.min([np.sqrt(((Q - p_) ** 2).sum(1)) for p_ in pick], axis=0); pick.append(Q[np.argmax(dd)])
        pegs += pick; peg_of += [li] * 3
    pegs = np.array(pegs)
    out, inside = {}, {}
    for var, (af, web) in HEX.items():
        R = af / np.sqrt(3); px = af + web; py = px * np.sqrt(3) / 2
        if var == "stencil":
            zones = [(FIN[0] - 4, FIN[1] + 4, FIN[2] + 2.0, FIN[3] - 2.0), (16, W - 16, BAY[2][0] + 2.5, BAY[2][1] - 2.5)]
            keep = 4.0
        else:
            zones = [(10, W - 10, b[0] + 1.5, b[1] - 1.5) for b in BAY]
            keep = None
        cells = []
        for zi, (u0, u1, v0, v1) in enumerate(zones):
            m = R + web / 2
            for j in range(int((v1 - v0) / py) + 1):
                for i in range(int((u1 - u0) / px) + 2):
                    c = (u0 + m + i * px + (j % 2) * px / 2, v0 + m + j * py)
                    if c[0] > u1 - m or c[1] > v1 - m: continue
                    if abs(c[0] - seam) < R + 6.5: continue                  # seam strip + spline groove
                    if var == "stencil" and zi == 1 and (c[0] < 34 or c[0] > W - 34): continue   # row-3 chevron zone
                    cells.append(c)
        C = np.array(cells)
        dmin = np.full(len(C), np.inf); ins = np.zeros(len(C), bool)
        for P in polys:
            dmin = np.minimum(dmin, seg_dist(C, P)); ins |= MPath(P).contains_points(C)
        if var == "stencil":
            ok = (dmin >= R + keep) & ~ins
        else:                                                                 # applique: hex runs under the letters; only the pegs keep out
            ok = np.ones(len(C), bool)
            for pg in pegs: ok &= np.sqrt(((C - pg) ** 2).sum(1)) >= R + PEG_D / 2 + 1.2
        out[var] = C[ok]; inside[var] = ins[ok]
    cell_a = {v: (np.sqrt(3) / 2) * HEX[v][0] ** 2 for v in HEX}
    fin_cells = {v: ((out[v][:, 0] >= FIN[0]) & (out[v][:, 0] <= FIN[1]) & (out[v][:, 1] >= FIN[2]) & (out[v][:, 1] <= FIN[3])).sum() for v in HEX}
    under = np.zeros(len(out["applique"]), bool)
    for P in polys: under |= MPath(P).contains_points(out["applique"])
    infz = (out["applique"][:, 0] >= FIN[0]) & (out["applique"][:, 0] <= FIN[1]) & (out["applique"][:, 1] >= FIN[2]) & (out["applique"][:, 1] <= FIN[3])
    a_out = (infz & ~under).sum() * cell_a["applique"]
    a_eff_under = 0.0
    for P in polys:
        u_ = (infz & MPath(P).contains_points(out["applique"])).sum() * cell_a["applique"]
        E = np.r_[P, P[:1]]; mids = (E[1:] + E[:-1]) / 2; lens = np.sqrt((np.diff(E, axis=0) ** 2).sum(1))
        per = lens[(mids[:, 0] >= FIN[0]) & (mids[:, 0] <= FIN[1]) & (mids[:, 1] >= FIN[2]) & (mids[:, 1] <= FIN[3])].sum()
        a_eff_under += min(u_, per * GAP)
    stats = dict(layout=name, k=k, cap=cap * k, seam=seam, seam_web=seam_web, halves=(seam, W - seam), plate_h=MZ1 - MZ0,
                 d_letters=d_letters, d_bolt=d_bolt, d_edge=d_edge, d_rail=d_rail, neck=neck,
                 a_letters_cm2=a_letters / 100, a_letters_fin_cm2=a_letters_fin / 100,
                 st_cells=len(out["stencil"]), st_hex_cm2=len(out["stencil"]) * cell_a["stencil"] / 100,
                 st_fin_cm2=(a_letters_fin + fin_cells["stencil"] * cell_a["stencil"]) / 100,
                 ap_cells=len(out["applique"]), ap_hex_cm2=len(out["applique"]) * cell_a["applique"] / 100,
                 ap_fin_cm2=fin_cells["applique"] * cell_a["applique"] / 100, ap_fin_eff_cm2=(a_out + a_eff_under) / 100, relaxed=relaxed, bolts_u=bu)
    pre = "L2_" if name == "twoline" else "L1_"
    f = HERE / f"wm_layout_{name}.scad"
    with f.open("w") as o:
        o.write(f"// GENERATED by make_wordmark_layout.py — do not edit.  {json.dumps({k_: (round(v, 2) if isinstance(v, float) else v) for k_, v in stats.items() if k_ != 'bolts_u'})}\n")
        o.write(f"{pre}CAP = {stats['cap']:.2f}; {pre}SEAM = {seam:.3f}; {pre}BOLT_U = [{', '.join(f'{u:.2f}' for u in bu)}];\n")
        o.write(f"{pre}NAMES = {json.dumps([L[0] for L in letters])};\n")
        o.write(f"{pre}LINE_Z = [{', '.join(f'[{P[:, 1].min():.2f}, {P[:, 1].max():.2f}]' for P in polys)}];\n")
        o.write(f"{pre}LETTERS = [\n" + ",\n".join("  [" + ", ".join(f"[{x:.2f}, {y:.2f}]" for x, y in P) + "]" for P in polys) + "];\n")
        for var, v in (("stencil", "ST"), ("applique", "AP")):
            o.write(f"{pre}CELLS_{v} = [" + ", ".join(f"[{x:.2f}, {y:.2f}]" for x, y in out[var]) + "];\n")
        o.write(f"{pre}PEGS = [" + ", ".join(f"[{x:.2f}, {y:.2f}]" for x, y in pegs) + "]; " + f"{pre}PEG_OF = {peg_of};\n")
        o.write(f"{pre}STATS = [{stats['st_hex_cm2']:.1f}, {stats['a_letters_cm2']:.1f}, {stats['st_fin_cm2']:.1f}, {stats['ap_hex_cm2']:.1f}, {stats['ap_fin_eff_cm2']:.1f}];\n")
    return stats


if __name__ == "__main__":
    for n in ("twoline", "oneline"):
        s = layout(n)
        print(f"\n[{n}] k {s['k']:.3f} mm/unit -> CAP HEIGHT {s['cap']:.1f} mm; seam u {s['seam']:.1f} (halves {s['halves'][0]:.1f} + {s['halves'][1]:.1f} wide, "
              f"{s['plate_h']:.2f} tall); seam web {s['seam_web']:.1f} each side")
        print(f"  webs: letter-letter {s['d_letters']:.1f}, letter-bolt seat {s['d_bolt']:.1f} (>= 6), letter-plate edge {s['d_edge']:.1f}, "
              f"letter-rail face {s['d_rail']:.1f}, narrowest neck inside a letter {s['neck']:.1f} (>= 4)")
        print(f"  STENCIL: letters {s['a_letters_cm2']:.1f} cm2 through + {s['st_cells']} micro-hex = {s['st_hex_cm2']:.1f} cm2 -> total "
              f"{s['a_letters_cm2'] + s['st_hex_cm2']:.1f}; over the case fins {s['st_fin_cm2']:.1f} cm2 (R4.2 >= 32 {'MET' if s['st_fin_cm2'] >= 32 else 'NOT MET'})")
        print(f"  APPLIQUE (letters {GAP} off the face on pegs, micro-hex unbroken): {s['ap_cells']} cells = {s['ap_hex_cm2']:.1f} cm2; over the case fins "
              f"{s['ap_fin_cm2']:.1f} plate, {s['ap_fin_eff_cm2']:.1f} cm2 effective (under-letter flow capped at perimeter x {GAP} gap) "
              f"(R4.2 >= 32 {'MET' if s['ap_fin_eff_cm2'] >= 32 else 'NOT MET'})")
        if s['relaxed']: print("  !! seam rules RELAXED: no letter gap gives >= 4 web each side off the fins")
