"""
Canary T1 cage — CAD HAND-OFF: true analytic B-rep STEP (build123d / OCCT).

Pattern: slimrig_mounts/make_slimrig_brep.py.  These are REFERENCE SOLIDS for a
human CAD team (SolidWorks): component envelopes with their mounting patterns
and keep-outs, plus the canon rod interface.  They are NOT part designs.

Naming carries the provenance:
    <name>.step            outline + hole PATTERN measured (hole DIAMETERS are
                           nominal unless stated — see cad_exchange/README.md)
    EST_<name>.step        unmeasured placeholder — never cut plastic against it
    PERCH_<name>.step      a DIFFERENT PRODUCT (Canary Perch, ground unit);
                           included so nobody mistakes it for the T1 compute
    CANON_<name>.step      print-validated rev-B rod interface, verbatim

Frame, every envelope: origin at the centre of the mounting face (underside of
the board / base of the box), X = long axis, Z = up (away from the mount face).

Run:  ../.venv/bin/python make_t1_brep.py  &&  ../.venv/bin/python verify_step.py
"""
from __future__ import annotations
from pathlib import Path
from build123d import Align, Box, Cone, Cylinder, Pos, Rot, export_step

import t1_params as P

OUT = Path(__file__).parent / "cad_exchange"
MIN_Z = (Align.CENTER, Align.CENTER, Align.MIN)
PCB_T = 1.6


def holes(part, pts, d, z0, h):
    for (x, y) in pts:
        part -= Pos(x, y, z0) * Cylinder(d / 2, h, align=MIN_Z)
    return part


def rect(px, py):
    return [(sx * px / 2, sy * py / 2) for sx in (-1, 1) for sy in (-1, 1)]


def board(L, W, pat, hole_d, body, body_h, under=0.0):
    """PCB slab + hole pattern + a component keep-out block that leaves the
    holes open.  `under` = keep-out below the board (solder side)."""
    part = Box(L, W, PCB_T, align=MIN_Z)
    part = holes(part, rect(*pat), hole_d, -0.1, PCB_T + 0.2)
    part += Pos(0, 0, PCB_T) * Box(body[0], body[1], body_h, align=MIN_Z)
    if under:
        part += Pos(0, 0, -under) * Box(body[0], body[1], under, align=MIN_Z)
    return part


def orin_devkit():
    L, W, H = P.COMPONENTS["orin_devkit"][:3]
    px, py = 91.86, 58.37                       # MEAS M3 pattern
    body_x = px - 3.4 - 4.0                     # keep-out stops 2 mm shy of the holes
    part = board(L, W, (px, py), 3.4, (body_x, W), H - PCB_T - 3.0, under=3.0)
    # top-draw fan: air keep-out column, EST O44 x 12 above the heatsink
    part += Pos(0, 0, H - 3.0) * Cylinder(22.0, 12.0, align=MIN_Z)
    # connector face (+Y long edge): plug keep-out slab, EST 55 deep
    part += Pos(0, W / 2 + P.PLUG_KEEPOUT / 2, PCB_T) * Box(body_x, P.PLUG_KEEPOUT, 20.0, align=MIN_Z)
    return part


def flycatcher():
    L, W, H = P.COMPONENTS["flycatcher"][:3]
    part = Box(L, W, H, align=MIN_Z)
    return holes(part, rect(*P.PAT_FLYCATCHER), 3.4, -0.1, 8.1)       # blind 8, dia EST


def co_stick():
    L, W, H = 114.00, 20.92, 15.12
    part = Box(L, W, H, align=MIN_Z)
    return holes(part, [(L / 2 - 6.0, 0)], 4.216, -0.1, H + 0.2)      # dia MEAS, position EST


def perch_stack():
    s = P.PERCH_STACK
    part = Box(s["L"], s["W"], s["H"], align=MIN_Z)
    pts = [(-s["PAT_DX"] / 2, sy * s["PAT_A"] / 2) for sy in (-1, 1)] + \
          [(+s["PAT_DX"] / 2, sy * s["PAT_B"] / 2) for sy in (-1, 1)]
    part = holes(part, pts, 2.0, -0.1, 6.1)                            # M2 standoff threads
    part += Pos(0, 0, s["H"]) * Cylinder(35.0, 10.0, align=MIN_Z)      # O70 fan keep-out EST
    return part


def canon_cap():
    part = Pos(0, 0, -P.CAP_T) * Box(P.CAP_W, P.ST_W, P.CAP_T, align=MIN_Z)
    part -= Pos(0, 0, P.PINCH) * Rot(0, 90, 0) * Cylinder(P.BR, P.CAP_W + 0.2)
    for sb in (-1, 1):
        part -= Pos(0, sb * P.BOLT_DY, -P.INS_DEP) * Cylinder(P.INS_D / 2, P.INS_DEP + 0.1, align=MIN_Z)
        part -= Pos(0, sb * P.BOLT_DY, -P.INS_CHAM) * Cone(
            P.INS_D / 2, P.INS_D / 2 + P.INS_CHAM, P.INS_CHAM + 0.05, align=MIN_Z)
    return Pos(0, 0, P.CAP_T) * part


def canon_station_pair(st_l=44.0, pl_w=96.0):
    """The canon rev-B plate segment: 7 mm plate, two 34 x 12 stations at
    y = +/-30, O15.4 troughs, 2 x M3 per tube flush-counterbored.  Design frame:
    plate z 0..7, stations hang to z = -12, trough axis at z = -12."""
    part = Box(st_l, pl_w, P.PL_T, align=MIN_Z)
    for sy in (-1, 1):
        part += Pos(0, sy * P.TUBE_CC / 2, -P.ST_DEP) * Box(st_l, P.ST_W, P.ST_DEP, align=MIN_Z)
    for sy in (-1, 1):
        part -= Pos(0, sy * P.TUBE_CC / 2, -P.ST_DEP) * Rot(0, 90, 0) * Cylinder(P.BR, st_l + 2)
        for sb in (-1, 1):
            by = sy * P.TUBE_CC / 2 + sb * P.BOLT_DY
            part -= Pos(0, by, -P.ST_DEP - 0.1) * Cylinder(P.M3B / 2, P.ST_DEP + P.PL_T + 0.2, align=MIN_Z)
            part -= Pos(0, by, P.PL_T - P.CB_H) * Cylinder(P.CB_D / 2, P.CB_H + 0.1, align=MIN_Z)
    return part


def rod(length=P.ROD_L):
    part = Rot(0, 90, 0) * Cylinder(P.TUBE_D / 2, length)
    part -= Rot(0, 90, 0) * Cylinder(P.TUBE_D / 2 - P.TUBE_WALL, length + 0.2)
    return part


JOBS = {
    "orin_devkit": orin_devkit,
    "flycatcher": flycatcher,
    "co_stick": co_stick,
    "zed_f9p": lambda: board(43.5, 43.5, P.PAT_ZED, 3.2, (30.0, 43.5), 10.4),
    "bno085": lambda: board(26.0, 24.0, P.PAT_BNO, 2.5, (12.0, 24.0), 3.4),
    "eg25g_lte": lambda: board(80.0, 35.0, P.PAT_EG25, 3.2, (62.0, 35.0), 10.4),
    "EST_vmount_battery": lambda: Box(107.0, 74.0, 64.0, align=MIN_Z),
    "EST_uhr204_hub": lambda: Box(139.0, 87.0, 35.0, align=MIN_Z),
    "EST_rod_15x400": rod,
    "PERCH_orin_ups_stack": perch_stack,
    "CANON_tube_cap": canon_cap,
    "CANON_station_pair": canon_station_pair,
}

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, fn in JOBS.items():
        solid = fn()
        bb = solid.bounding_box()
        assert len(solid.solids()) == 1, f"{name}: not a single solid"
        export_step(solid, str(OUT / f"{name}.step"))
        print(f"{name:24s} solids=1 faces={len(solid.faces()):3d} vol={solid.volume:11.1f} mm3  "
              f"bbox {bb.size.X:.2f} x {bb.size.Y:.2f} x {bb.size.Z:.2f}")
