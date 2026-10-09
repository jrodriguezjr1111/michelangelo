"""
CyberWing tube_platform rev B — TRUE B-REP (analytic) rebuild + STEP ASSEMBLY.

WHY THIS FILE EXISTS
    make_tube_platform.scad stays the SOURCE OF TRUTH for printing.  OpenSCAD
    only emits meshes, so a STEP derived from those meshes is a faceted polygon
    soup — reference-only in SolidWorks.  This script rebuilds the SAME geometry
    in build123d (OCCT) so the exported STEP carries genuine analytic surfaces
    (real cylinders on every bore, real cones on every insert chamfer, real
    planes), and then places every solid in its TRUE assembly position and
    writes one multi-body STEP that opens in SolidWorks as the system.

    Same contract as slimrig_mounts/make_slimrig_brep.py, whose ORIN/NANO plate,
    cap and spacer builders this file IMPORTS rather than duplicates: every
    parameter below is transcribed VERBATIM from the .scad, CSG epsilons and
    all.  Nothing is re-derived, rounded, or "improved".  If a dimension
    changes, it changes in the .scad first and is copied here second.

COORDINATE FRAME — the platform DESIGN frame (not a print frame)
    plate underside z = 0, plate top z = PL_T = 7
    tubes run along Y at x = +/- TUBE_X = 30, tube axis z = TZ = -61.7
    +Y = north (the end the Jetson Nano inserts from)
    Individual part STEPs are emitted in this same frame, already oriented as
    they sit in the machine — NOT in their print orientation.  Print STLs come
    from the .scad; do not slice anything here.

OUTPUTS (this directory)
    tube_platform_assembly.step   every solid, positioned, one compound
    tp_plate.step / tp_fence.step / tp_tower.step / tp_carrier.step /
    tp_retainer_bar.step / tp_rail.step / tp_cap.step / tp_spacer.step
    plus .stl companions

Run:  .venv/bin/python tube_platform/cad_exchange/make_tube_platform_brep.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from build123d import (
    Align,
    Box,
    Circle,
    Color,
    Compound,
    Cone,
    Cylinder,
    Part,
    Plane,
    Pos,
    Rectangle,
    RectangleRounded,
    Rot,
    export_step,
    Face,
    Shell,
    Solid,
    Vector,
    Wire,
    export_stl,
    extrude,
    mirror,
)

HERE = Path(__file__).resolve().parent          # tube_platform/cad_exchange
TP_DIR = HERE.parent                            # tube_platform
REPO = TP_DIR.parent
SLIM = REPO / "slimrig_mounts"

sys.path.insert(0, str(SLIM))
import make_slimrig_brep as slim               # noqa: E402  (canon cap/spacer/plates)

MIN_Z = (Align.CENTER, Align.CENTER, Align.MIN)
MIN_XYZ = (Align.MIN, Align.MIN, Align.MIN)

# =============================================================================
# PARAMETERS — transcribed verbatim from tube_platform/make_tube_platform.scad
# =============================================================================
PL_X, PL_Y, PL_T = 94.0, 134.0, 7.0
TUBE_D, CLR = 15.0, 0.4
BR = (TUBE_D + CLR) / 2                          # 7.7
TUBE_X = 30.0
CABLE_GAP = 54.0
TZ = -(CABLE_GAP + BR)                           # -61.7

CAP_T, CAP_W, PINCH = 11.0, 20.0, 1.0
BOLT_DX = 12.5
KO_S, KO_N = 26.6, 52.3
BAND_S = -PL_Y / 2 + KO_S                        # -40.4
BAND_N = PL_Y / 2 - KO_N                         #  14.7
CAPY = [BAND_S + 10, BAND_N - 10]                # -30.4 / 4.7
FT_D = 19.0
RISY = [-33.0, 9.0]
RBX = 40.0
RBY = [-29.0, -19.0, -9.0]
PB = [(sx * RBX, by) for sx in (-1, 1) for by in RBY]
M3B, CB_D, CB_H = 3.4, 6.2, 3.5
INS_D, INS_DEP, INS_CHAM = 4.4, 6.0, 0.6
SP_OD, SP_H = 7.0, 6.0
NANO_OVER_TUBE = (12 - BR) + 7 + 6 + 36          # 53.3

RTK_P = 37.6 / 2
RTK_C = (-16.0, 38.0)
EG_C, EG_P = (0.0, 38.0), (70.80 / 2, 24.21 / 2)
FC_C, FC_P = (14.0, -30.0), (49 / 2, 58 / 2)
TWR_LEG = [(-26.0, 16.0), (-6.0, 16.0), (-26.0, 60.0), (-6.0, 60.0)]
TWR_H, TWR_T = 29.0, 4.0
TWR = (-40.0, 13.0, 8.0, 63.0)

WX0, WX1, WALL_H = 44.5, 47.0, 35.0
SMA_D, SMA_Z = 6.5, 17.0
SMA_Y = [44.0, 16.0, -12.0]
ZIP_Y = [52.0, 34.0, 2.0, -26.0, -52.0]
FENCE_SCR = [(42.0, -52.0), (42.0, -38.0), (42.0, 20.0), (42.0, 57.0)]

BB, BB_T, BB_CLR = (55.0, 83.0), 9.0, 0.5
ESP_DROP = 17.0
CAR_W, CAR_T, CAR_EW = 3.0, 4.0, 8.0
CAR = (-31.0, -91.0, 31.0, 9.0)
CARM = [(sx * 25, y) for sx in (-1, 1) for y in (6, -22, -42, -62)]
CAR_DEPTH = CAR_T + BB_T + ESP_DROP              # 30
BAR_W = 12.0
CAR_BAR_Y = [CAR[1] + CAR_EW / 2, CAR[3] - CAR_EW / 2]   # -87 / 5
CAR_BAR_X = 12.0
LIGHTEN = [(-20, -8), (-8, -8), (20, -52), (-40, -20), (26, -8)]
EPS = 0.01


def pat(c, p):
    return [(c[0] + sx * p[0], c[1] + sy * p[1])
            for sx in (-1, 1) for sy in (-1, 1)]


EG_INS = pat(EG_C, EG_P)
FC_INS = pat(FC_C, FC_P)
RTK_INS = pat(RTK_C, (RTK_P, RTK_P))

# --- canon-interface cross-checks against the slimrig engine -----------------
assert (TUBE_D, CLR, BR) == (slim.TUBE_D, slim.CLR, slim.BR), "tube canon drift"
assert (CAP_T, CAP_W, PINCH) == (slim.CAP_T, slim.CAP_W, slim.PINCH), "cap drift"
assert BOLT_DX == slim.BOLT_DY, "cap bolt spacing drift"
assert (M3B, CB_D, CB_H) == (slim.M3B, slim.CB_D, slim.CB_H), "M3 canon drift"
assert (INS_D, INS_DEP, INS_CHAM) == (slim.INS_D, slim.INS_DEP, slim.INS_CHAM)
assert (SP_OD, SP_H) == (slim.SP_OD, slim.SP_H), "printed spacer drift"
assert TUBE_X == slim.TUBE_Y, "60 c-c drift between platform and tube plates"


# =============================================================================
# HELPERS — the .scad's flushins / flushins_dn / rrect, epsilons preserved
# =============================================================================
def flushins(part, x, y, zt):
    """M3 heat-set bore opening UPWARD through the face at z = zt."""
    part -= Pos(x, y, zt - INS_DEP) * Cylinder(INS_D / 2, INS_DEP + 0.1, align=MIN_Z)
    part -= Pos(x, y, zt - INS_CHAM) * Cone(
        INS_D / 2, INS_D / 2 + INS_CHAM, INS_CHAM + 0.05, align=MIN_Z)
    return part


def flushins_dn(part, x, y, zb):
    """M3 heat-set bore opening DOWNWARD through the face at z = zb."""
    part -= Pos(x, y, zb - 0.1) * Cylinder(INS_D / 2, INS_DEP + 0.1, align=MIN_Z)
    part -= Pos(x, y, zb - 0.05) * Cone(
        INS_D / 2 + INS_CHAM, INS_D / 2, INS_CHAM + 0.05, align=MIN_Z)
    return part


def thru_cb(part, x, y, z0, h, zcb, hcb, d=M3B, dcb=CB_D):
    part -= Pos(x, y, z0) * Cylinder(d / 2, h, align=MIN_Z)
    part -= Pos(x, y, zcb) * Cylinder(dcb / 2, hcb, align=MIN_Z)
    return part


def frustum(a, zA, b, zB):
    """Planar-faced frustum between two axis-aligned rects (x0,y0,x1,y1).

    Used for the rail's hull() blend.  A loft() would do it, but OCCT
    represents the ruled sides as B-spline surfaces; the four side quads here
    are provably planar (each joins two parallel X- or Y-parallel edges), so
    building them explicitly keeps the STEP 100 % analytic — the same standard
    slimrig_mounts/cad_exchange holds.
    """
    A = [(a[0], a[1], zA), (a[2], a[1], zA), (a[2], a[3], zA), (a[0], a[3], zA)]
    B = [(b[0], b[1], zB), (b[2], b[1], zB), (b[2], b[3], zB), (b[0], b[3], zB)]
    faces = [Face(Wire.make_polygon([Vector(*p) for p in A], close=True)),
             Face(Wire.make_polygon([Vector(*p) for p in B], close=True))]
    for i in range(4):
        j = (i + 1) % 4
        faces.append(Face(Wire.make_polygon(
            [Vector(*A[i]), Vector(*A[j]), Vector(*B[j]), Vector(*B[i])],
            close=True)))
    return Solid(Shell(faces))


def rrect(x0, y0, x1, y1, r):
    """.scad rrect(): hull of four r-circles at the inset corners.

    Built as (cross of two rectangles) + (4 corner circles) rather than
    RectangleRounded, because the tower's lightening windows are 10 x 6 with
    r = 3 — degenerate stadiums that RectangleRounded rejects but OpenSCAD's
    hull() produces happily.  Geometrically identical to the .scad.
    """
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s = None
    if w - 2 * r > 1e-9:
        s = Pos(cx, cy) * Rectangle(w - 2 * r, h)
    if h - 2 * r > 1e-9:
        t = Pos(cx, cy) * Rectangle(w, h - 2 * r)
        s = t if s is None else s + t
    for px in (x0 + r, x1 - r):
        for py in (y0 + r, y1 - r):
            c = Pos(px, py) * Circle(r)
            s = c if s is None else s + c
    return s


# =============================================================================
# PARTS — one module per .scad module, same order, same operations
# =============================================================================
def build_plate():
    p = Pos(-PL_X / 2, -PL_Y / 2, 0) * Box(PL_X, PL_Y, PL_T, align=MIN_XYZ)
    for (bx, by) in PB:                                   # plate -> rail bolts
        p = thru_cb(p, bx, by, -0.1, PL_T + 0.2, PL_T - CB_H, CB_H + 0.1)
    for (x, y) in EG_INS + FC_INS + TWR_LEG + FENCE_SCR:  # top-face heat-sets
        p = flushins(p, x, y, PL_T)
    for (x, y) in CARM:                                   # underside heat-sets
        p = flushins_dn(p, x, y, 0)
    for (x, y) in LIGHTEN:
        p -= Pos(x, y, -0.1) * Cylinder(8 / 2, PL_T + 0.2, align=MIN_Z)
    return p


def build_fence():
    f = Pos(WX0, -PL_Y / 2, 0) * Box(WX1 - WX0, PL_Y, WALL_H, align=MIN_XYZ)
    for (sx, sy) in FENCE_SCR:
        f += Pos(sx, sy, 0) * Cylinder(9 / 2, 3, align=MIN_Z)
        f += Pos(sx, sy - 4.5, 0) * Box(WX0 - sx + 0.1, 9, 3, align=MIN_XYZ)
    for jy in SMA_Y:                                       # SMA bulkheads
        f -= Pos(WX0 - 0.1, jy, SMA_Z) * Rot(0, 90, 0) * Cylinder(
            SMA_D / 2, WX1 - WX0 + 0.2, align=MIN_Z)
    for zy in ZIP_Y:                                       # zip columns
        for zz in (21, 27):
            f -= Pos(WX0 - 0.1, zy, zz) * Rot(0, 90, 0) * Cylinder(
                M3B / 2, WX1 - WX0 + 0.2, align=MIN_Z)
    for (sx, sy) in FENCE_SCR:                             # hold-downs
        f = thru_cb(f, sx, sy, -0.1, 3.2, 3 - CB_H, CB_H + 2)
    return f


def build_tower():
    deck = rrect(*TWR, 5)
    deck -= rrect(TWR[0] + 7, TWR[1] + 22, TWR[0] + 17, TWR[3] - 22, 3)
    deck -= rrect(TWR[2] - 17, TWR[1] + 22, TWR[2] - 7, TWR[3] - 22, 3)
    t = extrude(deck, TWR_T)
    for (lx, ly) in TWR_LEG:
        t += Pos(lx, ly, -TWR_H) * Cylinder(9 / 2, TWR_H + EPS, align=MIN_Z)
    for (lx, ly) in TWR_LEG:                               # M3x35 from deck top
        t = thru_cb(t, lx, ly, -TWR_H - 1, TWR_H + TWR_T + 1.2,
                    TWR_T - CB_H, CB_H + 0.1)
    for (x, y) in RTK_INS:
        t = flushins(t, x, y, TWR_T)
    return t


def build_carrier():
    c = extrude(rrect(*CAR, 4), CAR_T)
    walls = rrect(*CAR, 4) - rrect(CAR[0] + CAR_W, CAR[1] + CAR_EW,
                                   CAR[2] - CAR_W, CAR[3] - CAR_EW, 2)
    c += extrude(walls, CAR_T + BB_T)
    for (x, y) in CARM:
        c = thru_cb(c, x, y, -0.1, CAR_T + 0.2, CAR_T - CB_H, CB_H + 0.1)
    for sx in (-1, 1):
        for by in CAR_BAR_Y:
            c = flushins(c, sx * CAR_BAR_X, by, CAR_T + BB_T)
    c -= Pos(CAR[0] + 12, CAR[1] + 16, -0.1) * Cylinder(
        10 / 2, CAR_T + 0.2, align=MIN_Z)
    return c


def build_retainer_bar():
    b = Pos(CAR[0], -BAR_W / 2, 0) * Box(CAR[2] - CAR[0], BAR_W, 4, align=MIN_XYZ)
    for sx in (-1, 1):
        b = thru_cb(b, sx * CAR_BAR_X, 0, -0.1, 4.2, 4 - CB_H, CB_H + 0.2)
    return b


def build_west_rail():
    # main body + riser blade + the hull that blends them
    r = Pos(-TUBE_X - FT_D, BAND_S, TZ - 17) * Box(
        FT_D, BAND_N - BAND_S, 34, align=MIN_XYZ)
    r += Pos(-TUBE_X - FT_D, RISY[0], TZ + 17 - EPS) * Box(
        16, RISY[1] - RISY[0], CABLE_GAP + BR - 17 + EPS, align=MIN_XYZ)
    # hull(cubeA z TZ+13..TZ+17, cubeB z TZ+17..TZ+21): B's footprint is inside
    # A's, so hull == A + loft(A_top -> B_top)
    r += Pos(-TUBE_X - FT_D, BAND_S, TZ + 13) * Box(
        FT_D, BAND_N - BAND_S, 4, align=MIN_XYZ)
    r += frustum((-TUBE_X - FT_D, BAND_S, -TUBE_X, BAND_N), TZ + 17,
                 (-TUBE_X - FT_D, RISY[0], -TUBE_X - FT_D + 16, RISY[1]), TZ + 21)

    # tube trough (full cylinder cut on the tube line: the body is west of it)
    r -= Pos(-TUBE_X, BAND_S - 1, TZ) * Rot(-90, 0, 0) * Cylinder(
        BR, BAND_N - BAND_S + 2, align=MIN_Z)
    # 45-degree mouth relief at the trough crown and root
    for sz in (-1, 1):
        r -= Pos(-TUBE_X, (BAND_S + BAND_N) / 2, TZ + sz * BR) * Rot(0, 45, 0) * \
            Box(1.7, BAND_N - BAND_S + 2.4, 1.7)
    # cap bolts, horizontal, heads counterbored on the OUTBOARD (west) face
    for cy in CAPY:
        for sb in (-1, 1):
            r -= Pos(-TUBE_X - FT_D - 1, cy, TZ + sb * BOLT_DX) * Rot(0, 90, 0) * \
                Cylinder(M3B / 2, FT_D + 2, align=MIN_Z)
            r -= Pos(-TUBE_X - FT_D - 0.1, cy, TZ + sb * BOLT_DX) * Rot(0, 90, 0) * \
                Cylinder(CB_D / 2, CB_H + 0.1, align=MIN_Z)
    # rail-top heat-sets (the plate bolts down into these)
    for by in RBY:
        r -= Pos(-RBX, by, -INS_DEP) * Cylinder(INS_D / 2, INS_DEP + 0.1, align=MIN_Z)
        r -= Pos(-RBX, by, -INS_CHAM) * Cone(
            INS_D / 2, INS_D / 2 + INS_CHAM, INS_CHAM + 0.05, align=MIN_Z)
    return r


# canon parts come straight from the slimrig engine (proves interchangeability)
def build_cap():
    """canon cap in the .scad `part="cap"` PRINT frame (z 0..CAP_T)."""
    return slim.build_cap()


def build_cap_design():
    """canon cap in the .scad cap() MODULE frame: body z -CAP_T..0, trough
    axis at z = +PINCH.  This is the frame every assembly placement uses."""
    return Pos(0, 0, -CAP_T) * slim.build_cap()


def build_spacer():
    return slim.build_spacer()


# =============================================================================
# ASSEMBLY PLACEMENT — the same transforms make_system_assembly.scad uses
# =============================================================================
# Nano plate frame -> platform frame
NN_ST_DEP, NN_PL_X, NN_PL_T, NN_TUBE_Y = (
    slim.ST_DEP, slim.NANO["PL_X"], slim.PL_T, slim.TUBE_Y)
NN_DZ = TZ + NN_ST_DEP                                   # -49.7
NN_TY = BAND_N + NN_PL_X / 2                             #  52.7
OO_PL_X = slim.ORIN["PL_X"]
OO_DZ = TZ + slim.ST_DEP
OO_TY = CAR[1] - OO_PL_X / 2                             # -142


def design_frame_plate(p):
    """slimrig plates are emitted in the PRINT frame; undo it to get design."""
    return Pos(0, 0, slim.PL_T) * Rot(180, 0, 0) * p


def placed_bodies(with_orin: bool = False):
    """(label, solid, rgb) in the platform DESIGN frame."""
    out = []
    # the SlimRig tube pair itself (Ø15.0 stock, not a printed part) — carried
    # so the interference check proves every trough really clears the tube
    ty0, ty1 = min(-PL_Y / 2, CAR[1]) - 25, NN_TY + NN_PL_X / 2 + 25
    for sx, nm in ((-1, "tube_west"), (1, "tube_east")):
        out.append((nm, Pos(sx * TUBE_X, ty0, TZ) * Rot(-90, 0, 0) *
                    Cylinder(TUBE_D / 2, ty1 - ty0, align=MIN_Z), (0.45, 0.55, 0.62)))
    out.append(("tp_plate", build_plate(), (0.74, 0.72, 0.42)))
    out.append(("tp_fence", Pos(0, 0, PL_T) * build_fence(), (0.27, 0.51, 0.71)))
    out.append(("tp_tower", Pos(0, 0, PL_T + TWR_H) * build_tower(),
                (0.58, 0.44, 0.86)))
    out.append(("tp_carrier", mirror(build_carrier(), Plane.XY), (0.80, 0.36, 0.36)))
    for i, by in enumerate(CAR_BAR_Y):
        out.append((f"tp_retainer_bar_{i + 1}",
                    Pos(0, by, -(CAR_T + BB_T)) *
                    mirror(build_retainer_bar(), Plane.XY),
                    (0.70, 0.13, 0.13)))
    rail = build_west_rail()
    out.append(("tp_rail_west", rail, (0.85, 0.65, 0.13)))
    out.append(("tp_rail_east", mirror(rail, Plane.YZ), (0.85, 0.65, 0.13)))
    cap = build_cap_design()
    n = 0
    for cy in CAPY:
        # scad rotate([-90,0,90]) == Rz(90).Rx(-90); build123d's 3-angle Rot()
        # composes in a different order, so compose the two explicitly.  The
        # cap closes the rail's trough from INBOARD: body x -29..-18, flat face
        # 1.0 (PINCH) off the rail face at x -30.  East side is the MIRROR of
        # the west placement, exactly as the .scad does it.
        west = Pos(-(TUBE_X - PINCH), cy, TZ) * Rot(0, 0, 90) * Rot(-90, 0, 0) * cap
        n += 1
        out.append((f"tp_cap_W{n}", west, (0.20, 0.80, 0.20)))
        out.append((f"tp_cap_E{n}", mirror(west, Plane.YZ), (0.20, 0.80, 0.20)))
    sp = build_spacer()
    for tag, pts in (("EG25", EG_INS), ("FC", FC_INS)):
        for (x, y) in pts:
            out.append((f"tp_spacer_{tag}({x:+.1f},{y:+.1f})",
                        Pos(x, y, PL_T) * sp, (0.63, 0.32, 0.18)))
    for (x, y) in RTK_INS:
        out.append((f"tp_spacer_RTK({x:+.1f},{y:+.1f})",
                    Pos(x, y, PL_T + TWR_H + TWR_T) * sp, (0.63, 0.32, 0.18)))

    # ---- the Jetson Nano on its own plate, inserted from the north ----
    nano = design_frame_plate(slim.build_plate(slim.NANO))
    out.append(("nano_tube_plate",
                Pos(0, NN_TY, NN_DZ) * Rot(0, 0, 90) * nano, (0.00, 0.81, 0.82)))
    for i, sy in enumerate((-1, 1)):
        out.append((f"nano_cap_{i + 1}",
                    Pos(0, NN_TY, NN_DZ) * Rot(0, 0, 90) *
                    Pos(0, sy * NN_TUBE_Y, -NN_ST_DEP - PINCH) * cap,
                    (0.00, 0.98, 0.60)))
    nx, ny = slim.NANO["PATTERN"][0] / 2, slim.NANO["PATTERN"][1] / 2
    n = 0
    for sx in (-1, 1):
        for sy in (-1, 1):
            n += 1
            out.append((f"nano_spacer_{n}",
                        Pos(0, NN_TY, NN_DZ) * Rot(0, 0, 90) *
                        Pos(sx * nx, sy * ny, NN_PL_T) * sp, (0.63, 0.32, 0.18)))

    if with_orin:
        orin = design_frame_plate(slim.build_plate(slim.ORIN))
        out.append(("orin_tube_plate",
                    Pos(0, OO_TY, OO_DZ) * Rot(0, 0, 90) * orin, (0.42, 0.35, 0.80)))
        for i, sy in enumerate((-1, 1)):
            out.append((f"orin_cap_{i + 1}",
                        Pos(0, OO_TY, OO_DZ) * Rot(0, 0, 90) *
                        Pos(0, sy * slim.TUBE_Y, -slim.ST_DEP - PINCH) * cap,
                        (0.00, 0.98, 0.60)))
        ox, oy = slim.ORIN["PATTERN"][0] / 2, slim.ORIN["PATTERN"][1] / 2
        n = 0
        for sx in (-1, 1):
            for sy in (-1, 1):
                n += 1
                out.append((f"orin_spacer_{n}",
                            Pos(0, OO_TY, OO_DZ) * Rot(0, 0, 90) *
                            Pos(sx * ox, sy * oy, slim.PL_T) * sp,
                            (0.63, 0.32, 0.18)))
    return out


# =============================================================================
# Volume cross-check against the printed OpenSCAD meshes
# =============================================================================
def stl_volume(path: Path) -> tuple[int, float]:
    txt = path.read_text(errors="ignore")
    v = [tuple(map(float, m)) for m in
         re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", txt)]
    vol = 0.0
    for i in range(0, len(v), 3):
        a, b, c = v[i], v[i + 1], v[i + 2]
        cx = (b[1] * c[2] - b[2] * c[1],
              b[2] * c[0] - b[0] * c[2],
              b[0] * c[1] - b[1] * c[0])
        vol += sum(a[k] * cx[k] for k in range(3))
    return len(v) // 3, vol / 6.0


MESH_CHECK = [
    # (label, B-rep volume expression, OpenSCAD STL that contains it)
    ("tp_plate",   lambda P: P["tp_plate"],                       "tp_plate.stl"),
    ("tp_fence",   lambda P: P["tp_fence"],                       "tp_fence.stl"),
    ("tp_tower",   lambda P: P["tp_tower"],                       "tp_tower.stl"),
    ("tp_carrier", lambda P: P["tp_carrier"] + 2 * P["tp_bar"],   "tp_carrier.stl"),
    ("tp_clamps",  lambda P: 2 * P["tp_rail"],                    "tp_clamps.stl"),
    ("tp_caps_spacers",
     lambda P: 4 * P["tp_cap"] + 12 * P["tp_spacer"],             "tp_caps_spacers.stl"),
]


def main() -> None:
    print("=" * 78)
    print("tube_platform rev B — analytic B-rep rebuild + STEP assembly (build123d)")
    print("=" * 78)
    print(f"  datum   plate underside z0, top z{PL_T:.0f}; tubes along Y at "
          f"x=+/-{TUBE_X:.0f}, axis z={TZ}; corridor {CABLE_GAP} (floor z{TZ + BR})")
    print(f"  canon   cap {CAP_W}x34x{CAP_T} pinch {PINCH}, spacer "
          f"O{SP_OD}x{SP_H}, insert O{INS_D}x{INS_DEP}, M3 clr {M3B}/CB {CB_D}x{CB_H}")

    parts = {
        "tp_plate": build_plate(),
        "tp_fence": build_fence(),
        "tp_tower": build_tower(),
        "tp_carrier": build_carrier(),
        "tp_bar": build_retainer_bar(),
        "tp_rail": build_west_rail(),
        "tp_cap": build_cap(),
        "tp_spacer": build_spacer(),
    }

    print("\n" + "-" * 78)
    print("PER-PART B-REP")
    for name, s in parts.items():
        bb = s.bounding_box()
        print(f"  {name:<14} solids {len(s.solids())}  faces {len(s.faces()):>4}  "
              f"vol {s.volume:11.3f}  bbox "
              f"({bb.min.X:7.2f},{bb.min.Y:7.2f},{bb.min.Z:7.2f}).."
              f"({bb.max.X:7.2f},{bb.max.Y:7.2f},{bb.max.Z:7.2f})")
        assert len(s.solids()) == 1, f"{name} is not one solid"

    print("\n" + "-" * 78)
    print("VOLUME CROSS-CHECK vs the printed OpenSCAD meshes ($fn=52)")
    V = {k: v.volume for k, v in parts.items()}
    worst = 0.0
    for label, expr, mesh in MESH_CHECK:
        mp = TP_DIR / mesh
        if not mp.exists():
            print(f"  {label:<16} (no {mesh})")
            continue
        n, mv = stl_volume(mp)
        bv = expr(V)
        d = bv - mv
        pct = 100 * d / mv
        worst = max(worst, abs(pct))
        flag = "OK " if abs(pct) < 0.2 else "!! "
        print(f"  {flag}{label:<16} B-rep {bv:11.3f}  mesh {mv:11.3f}  "
              f"delta {d:+8.3f} ({pct:+.3f} %, {n} tris)")
    print(f"  worst deviation {worst:.3f} %  "
          f"[expected: $fn=52 inscribed bores under-remove material -> mesh high]")

    # ---------------- exports ----------------
    print("\n" + "-" * 78)
    print("EXPORTS")
    for name, s in parts.items():
        stem = name if name != "tp_bar" else "tp_retainer_bar"
        export_step(s, str(HERE / f"{stem}.step"))
        export_stl(s, str(HERE / f"{stem}.stl"),
                   tolerance=0.005, angular_tolerance=0.05)
        print(f"  {stem}.step / .stl")

    for tag, with_orin in (("", False), ("_with_orin", True)):
        bodies = placed_bodies(with_orin)
        kids = []
        for label, solid, rgb in bodies:
            body = Part(solid.wrapped)      # normalise Solid/Compound -> Part so
            body.label = label              # export_step attaches colour to the
            body.color = Color(*rgb)        # wrapped solid, not just the wrapper
            kids.append(body)
        asm = Compound(children=kids)
        asm.label = "tube_platform_rev_B" + tag
        out = HERE / f"tube_platform_assembly{tag}.step"
        export_step(asm, str(out))
        bb = asm.bounding_box()
        print(f"  {out.name}: {len(kids)} bodies, "
              f"bbox ({bb.min.X:.1f},{bb.min.Y:.1f},{bb.min.Z:.1f}).."
              f"({bb.max.X:.1f},{bb.max.Y:.1f},{bb.max.Z:.1f}), "
              f"{out.stat().st_size:,} B")

    print("\n" + "-" * 78)
    print("The .scad files remain the source of truth for PRINTING.")
    print("These STEP files are the CAD-exchange copies (analytic surfaces).")


if __name__ == "__main__":
    main()
