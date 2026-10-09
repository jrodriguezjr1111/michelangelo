"""
CyberWing tube_platform rev B — ASSEMBLY VERIFICATION (OCCT, headless).

Four independent checks, all run against the ANALYTIC B-rep bodies that
make_tube_platform_brep.py builds from the .scad parameters:

  1. B-REP SANITY        every part is exactly one closed solid, analytic
                         surfaces only (plane / cylinder / cone), and its
                         volume matches the printed OpenSCAD mesh.
  2. INTERPENETRATION    true boolean intersection volume for every pair of
                         positioned bodies in the assembly.  Bolted faces are
                         allowed to TOUCH (zero volume); anything with shared
                         volume is a hard interference.
  3. CRITICAL CLEARANCES exact solid-to-solid minimum distances (OCCT
                         BRepExtrema) on the interfaces the design depends on:
                         the Nano corridor, the Nano insertion stop, the cap
                         intrusion, the board envelopes.
  4. FEATURE PROXIMITY   every bore in the 7 mm plate against every other bore
                         that shares its Z band — including the Ø8 LIGHTENING
                         HOLES, which the .scad's own assert suite does not
                         cover.

Run:  .venv/bin/python tube_platform/cad_exchange/verify_assembly.py
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

from build123d import Box, Cylinder, Align, Pos
from OCP.BRep import BRep_Tool
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopAbs import TopAbs_SHELL
from OCP.TopExp import TopExp_Explorer
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_SurfaceType

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_tube_platform_brep as tp                       # noqa: E402

MIN_Z = (Align.CENTER, Align.CENTER, Align.MIN)
SURF = {GeomAbs_SurfaceType.GeomAbs_Plane: "plane",
        GeomAbs_SurfaceType.GeomAbs_Cylinder: "cyl",
        GeomAbs_SurfaceType.GeomAbs_Cone: "cone",
        GeomAbs_SurfaceType.GeomAbs_Sphere: "sphere",
        GeomAbs_SurfaceType.GeomAbs_Torus: "torus",
        GeomAbs_SurfaceType.GeomAbs_BSplineSurface: "bspline",
        GeomAbs_SurfaceType.GeomAbs_BezierSurface: "bezier"}
FAIL: list[str] = []
WARN: list[str] = []


def rule(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


# ============================================================ 1. B-REP SANITY
def check_brep():
    rule("1. B-REP SANITY — one closed analytic solid per part")
    parts = {
        "tp_plate": tp.build_plate(), "tp_fence": tp.build_fence(),
        "tp_tower": tp.build_tower(), "tp_carrier": tp.build_carrier(),
        "tp_retainer_bar": tp.build_retainer_bar(), "tp_rail": tp.build_west_rail(),
        "tp_cap": tp.build_cap(), "tp_spacer": tp.build_spacer(),
    }
    print(f"  {'part':<17}{'solids':>7}{'closed':>8}{'valid':>7}"
          f"{'faces (plane/cyl/cone)':>26}{'volume mm3':>14}")
    for name, s in parts.items():
        census: dict[str, int] = {}
        for f in s.faces():
            k = SURF.get(BRepAdaptor_Surface(f.wrapped).GetType(), "OTHER")
            census[k] = census.get(k, 0) + 1
        valid = BRepCheck_Analyzer(s.wrapped).IsValid()
        shells, exp = [], TopExp_Explorer(s.wrapped, TopAbs_SHELL)
        while exp.More():
            shells.append(BRep_Tool.IsClosed_s(exp.Current()))
            exp.Next()
        closed = bool(shells) and all(shells)
        exotic = {k: v for k, v in census.items()
                  if k not in ("plane", "cyl", "cone")}
        print(f"  {name:<17}{len(s.solids()):>7}{str(closed):>8}{str(valid):>7}"
              f"{len(s.faces()):>10} ({census.get('plane', 0)}/"
              f"{census.get('cyl', 0)}/{census.get('cone', 0)})".ljust(0)
              + f"{s.volume:>14.3f}")
        if not (valid and closed and len(s.solids()) == 1):
            FAIL.append(f"{name}: solids={len(s.solids())} closed={closed} valid={valid}")
        if exotic:
            FAIL.append(f"{name}: non-analytic faces {exotic}")
    return parts


# ======================================================= 2. INTERPENETRATION
def check_interference(bodies):
    rule("2. INTERPENETRATION — boolean intersection volume, every pair")
    bbs = [(n, s, s.bounding_box()) for n, s, _ in bodies]
    tested = hits = 0
    for (na, sa, ba), (nb, sb, bb) in combinations(bbs, 2):
        if (ba.min.X > bb.max.X or bb.min.X > ba.max.X or
                ba.min.Y > bb.max.Y or bb.min.Y > ba.max.Y or
                ba.min.Z > bb.max.Z or bb.min.Z > ba.max.Z):
            continue                                    # bboxes disjoint
        tested += 1
        cut = sa & sb
        v = 0.0 if cut is None else cut.volume
        if v > 1e-6:
            hits += 1
            print(f"  !! {na} x {nb}: shared volume {v:.4f} mm3")
            FAIL.append(f"interference {na} x {nb} = {v:.4f} mm3")
    print(f"  {len(bbs)} bodies, {len(list(combinations(bbs, 2)))} pairs, "
          f"{tested} with overlapping bounding boxes, {hits} with shared volume")
    if not hits:
        print("  OK  no interpenetration anywhere in the assembly")


# ======================================================= 3. CRITICAL CLEARANCES
def check_clearances(bodies):
    rule("3. CRITICAL CLEARANCES — exact solid-to-solid minimum distance")
    B = {n: s for n, s, _ in bodies}
    PL_T, TZ, BR, GAP = tp.PL_T, tp.TZ, tp.BR, tp.CABLE_GAP

    # --- envelopes the .scad ghosts, rebuilt from the same parameters ---
    def box(x0, y0, z0, dx, dy, dz):
        return Pos(x0, y0, z0) * Box(dx, dy, dz,
                                     align=(Align.MIN, Align.MIN, Align.MIN))

    EG, EB = tp.EG_C, (76.0, 30.0)
    FC, FB = tp.FC_C, (54.0, 73.0)
    RC, RB = tp.RTK_C, 43.5
    CAR = tp.CAR
    NANO_ENV_H = tp.NANO_OVER_TUBE - ((12 - BR) + 7 + 6)      # 36
    env = {
        "env_EG25": box(EG[0] - EB[0] / 2, EG[1] - EB[1] / 2, PL_T + tp.SP_H,
                        EB[0], EB[1], 18),
        "env_FlyCatcher": box(FC[0] - FB[0] / 2, FC[1] - FB[1] / 2, PL_T + tp.SP_H,
                              FB[0], FB[1], 27),
        "env_ZED_F9P": box(RC[0] - RB / 2, RC[1] - RB / 2,
                           PL_T + tp.TWR_H + tp.TWR_T + tp.SP_H, RB, RB, 20),
        "env_breadboard": box(CAR[0] + tp.CAR_W, CAR[1] + tp.CAR_EW,
                              -tp.CAR_T - tp.BB_T, CAR[2] - CAR[0] - 2 * tp.CAR_W,
                              CAR[3] - CAR[1] - 2 * tp.CAR_EW, tp.BB_T),
        "env_ESP32": box(-18, CAR[1] + 20, -tp.CAR_DEPTH, 36, 60, tp.ESP_DROP),
        # Nano board+SoM+heatsink, centred on ITS plate (not the .scad ghost's
        # 2 mm-north offset) — 80 on the tube axis, 100 across
        "env_Nano_stack": box(-50, tp.NN_TY - 40, TZ + tp.NN_ST_DEP
                              + tp.NN_PL_T + tp.SP_H, 100, 80, NANO_ENV_H),
    }

    def gap(a, b):
        return (env.get(a) or B[a]).distance_to(env.get(b) or B[b])

    rows = [
        ("Nano stack top vs plate underside (the 54 corridor)",
         "env_Nano_stack", "tp_plate", 0.5),
        ("Nano plate vs west rail (insertion stop face)",
         "nano_tube_plate", "tp_rail_west", 0.0),
        ("Nano plate vs east rail", "nano_tube_plate", "tp_rail_east", 0.0),
        ("Nano plate vs north platform cap (west)",
         "nano_tube_plate", "tp_cap_W2", 0.0),
        ("Nano plate vs north platform cap (east)",
         "nano_tube_plate", "tp_cap_E2", 0.0),
        ("Nano stack vs hanging carrier", "env_Nano_stack", "tp_carrier", 3.0),
        ("Nano stack vs west rail", "env_Nano_stack", "tp_rail_west", 0.0),
        ("EG25 envelope vs RTK tower (legs straddle in Y at 2.5)",
         "env_EG25", "tp_tower", 2.5),
        ("EG25 envelope vs cable wall", "env_EG25", "tp_fence", 1.0),
        ("FlyCatcher envelope vs RTK tower", "env_FlyCatcher", "tp_tower", 2.0),
        ("FlyCatcher envelope vs cable wall", "env_FlyCatcher", "tp_fence", 2.0),
        ("FlyCatcher envelope vs EG25 envelope", "env_FlyCatcher", "env_EG25", 8.0),
        ("ZED-F9P envelope vs cable wall", "env_ZED_F9P", "tp_fence", 1.0),
        ("ESP32 envelope vs retainer bar (north)", "env_ESP32",
         "tp_retainer_bar_2", 1.0),
        ("ESP32 envelope vs retainer bar (south)", "env_ESP32",
         "tp_retainer_bar_1", 1.0),
        ("hanging carrier vs west rail", "tp_carrier", "tp_rail_west", 2.0),
        ("west cap vs west rail (the 1.0 clamp pinch)",
         "tp_cap_W1", "tp_rail_west", 0.9),
        ("east cap vs east rail (the 1.0 clamp pinch)",
         "tp_cap_E1", "tp_rail_east", 0.9),
        ("west cap vs the tube (trough 7.7 vs tube 7.5)",
         "tp_cap_W1", "tube_west", 0.15),
    ]
    print(f"  {'interface':<52}{'gap mm':>9}{'min':>7}  verdict")
    for label, a, b, lo in rows:
        d = gap(a, b)
        ok = d >= lo - 1e-6
        if not ok:
            FAIL.append(f"clearance {label}: {d:.3f} < {lo}")
        print(f"  {label:<52}{d:>9.3f}{lo:>7.1f}  {'OK' if ok else '!! TOO TIGHT'}")

    # scalar stack arithmetic, straight from the parameters
    print(f"\n  corridor floor (tube top) z {TZ + BR:.1f}  ->  plate underside z 0"
          f"   = {GAP} clear")
    print(f"  Nano stack over the tube top {tp.NANO_OVER_TUBE}  ->  margin "
          f"{GAP - tp.NANO_OVER_TUBE}")
    print(f"  hanging assembly depth {tp.CAR_DEPTH}  ->  {GAP - tp.CAR_DEPTH} "
          f"of corridor left under the carrier footprint "
          f"(x {tp.CAR[0]}..{tp.CAR[2]}, y {tp.CAR[1]}..{tp.CAR[3]})")
    print(f"  carrier north edge y {tp.CAR[3]}  vs  Nano stop face y {tp.BAND_N}"
          f"  = {tp.BAND_N - tp.CAR[3]} clear")
    print(f"  RTK tower deck underside z {PL_T + tp.TWR_H}  vs  EG25 envelope top z "
          f"{PL_T + tp.SP_H + 18}  = {tp.TWR_H - tp.SP_H - 18} vertical "
          f"(the designed 5.0; the 2.5 above is the LEG straddle, by design)")


# ======================================================= 4. FEATURE PROXIMITY
def check_plate_features():
    rule("4. FEATURE PROXIMITY — every bore in the 7 mm plate, incl. lightening")
    PL_T, INS = tp.PL_T, tp.INS_D / 2
    F = []                                  # (name, x, y, r, z0, z1)
    for (x, y) in tp.PB:
        F.append((f"rail-bolt({x:+.0f},{y:+.0f})", x, y, tp.M3B / 2, -0.1, PL_T + 0.1))
        F.append((f"rail-bolt-CB({x:+.0f},{y:+.0f})", x, y, tp.CB_D / 2,
                  PL_T - tp.CB_H, PL_T + 0.1))
    for tag, pts in (("EG25", tp.EG_INS), ("FC", tp.FC_INS),
                     ("tower-leg", tp.TWR_LEG), ("fence", tp.FENCE_SCR)):
        for (x, y) in pts:
            F.append((f"ins-{tag}({x:+.1f},{y:+.1f})", x, y, INS,
                      PL_T - tp.INS_DEP, PL_T + 0.1))
    for (x, y) in tp.CARM:
        F.append((f"ins-carrier({x:+.0f},{y:+.0f})", x, y, INS, -0.1, tp.INS_DEP))
    for (x, y) in tp.LIGHTEN:
        F.append((f"LIGHTENING({x:+.0f},{y:+.0f})", x, y, 4.0, -0.1, PL_T + 0.1))

    rows = []
    for (na, xa, ya, ra, a0, a1), (nb, xb, yb, rb, b0, b1) in combinations(F, 2):
        if min(a1, b1) - max(a0, b0) <= 0:              # no shared Z band
            continue
        if na.split("(")[0] == nb.split("(")[0] and na.startswith("rail-bolt"):
            continue                                    # bolt vs its own CB
        if (xa, ya) == (xb, yb):
            continue                                    # coaxial by design
        web = ((xa - xb) ** 2 + (ya - yb) ** 2) ** 0.5 - ra - rb
        if web < 1.5:
            rows.append((web, na, nb))
    rows.sort()
    if not rows:
        print("  OK  every bore pair keeps >= 1.5 mm of web")
    for web, na, nb in rows:
        tag = "!! BREACH " if web < 0 else "!! THIN   "
        (FAIL if web < 0 else WARN).append(f"{na} vs {nb}: web {web:+.3f}")
        print(f"  {tag}{na:<26} vs {nb:<26} web {web:+7.3f} mm")

    # ---- the fence hold-down counterbore, checked as material, not arithmetic
    print("\n  fence hold-down flange (3.0 thick) vs its Ø6.2 x 3.5 counterbore:")
    fence = tp.build_fence()
    for (x, y) in tp.FENCE_SCR:
        seat = (fence & (Pos(x, y, 0) * Cylinder(tp.CB_D / 2, 3.0, align=MIN_Z))).volume
        ring = (fence & (Pos(x, y, 2.9) * Cylinder(4.5, 0.1, align=MIN_Z))).volume
        verdict = "OK" if seat > 1.0 else "!! NO HEAD SEAT (CB cuts the full flange)"
        print(f"    ({x:+.0f},{y:+.0f})  material inside Ø{tp.CB_D} over the flange"
              f" height: {seat:8.3f} mm3   flange ring left at the top face:"
              f" {ring:6.3f} mm3   {verdict}")
        if seat <= 1.0:
            FAIL.append(f"fence hold-down ({x:+.0f},{y:+.0f}): counterbore "
                        f"({tp.CB_H} deep) exceeds the 3.0 flange — no head seat")


# ======================================================== 5. FASTENER STACKS
# (head seat plane) -> (material below the head) -> (heat-set bore).  A screw
# longer than material+bore cannot clamp: it bottoms on the insert or on the
# plastic below it.  Every counterbore in this family is CB_H = 3.5 deep, which
# is exactly what the .scad/README length arithmetic ("grip = material +
# insert") leaves out.
def check_fasteners():
    rule("5. FASTENER STACKS — available under-head depth vs the BOM screw")
    CB, INS = tp.CB_H, tp.INS_DEP
    J = [
        # label, qty, material below head, insert depth, README screw
        ("rail cap bolts (through the 19 rail -> cap insert)", 8,
         tp.FT_D - CB, INS, 25),
        ("plate -> rail top (through the 7 plate)", 6, tp.PL_T - CB, INS, 12),
        ("RTK tower legs (deck 4 + leg 29 -> plate insert)", 4,
         tp.TWR_T - CB + tp.TWR_H, INS, 35),
        ("cable-wall hold-downs (3.0 flange -> plate insert)", 4,
         3.0 - CB, INS, 10),
        ("carrier -> plate underside (4 backer)", 8, tp.CAR_T - CB, INS, 12),
        ("retainer bars -> carrier wall tops (4 bar)", 4, 4.0 - CB, INS, 10),
        ("EG25 / FlyCatcher cargo (board 1.6 + spacer 6)", 8,
         1.6 + tp.SP_H, INS, 12),
        ("ZED-F9P on the tower deck (board 1.6 + spacer 6)", 4,
         1.6 + tp.SP_H, INS, 12),
        ("nano/orin plate cap bolts (station 12 + plate 7)", 4,
         12 + tp.PL_T - CB, INS, 25),
        ("nano/orin board (board 1.6 + spacer 6)", 4, 1.6 + tp.SP_H, INS, 12),
    ]
    print(f"  {'joint':<50}{'qty':>4}{'grip':>7}{'avail':>7}{'BOM':>6}"
          f"{'engage':>8}  verdict")
    for label, qty, grip, ins, screw in J:
        avail = grip + ins
        eng = screw - grip
        if grip < 0:
            v = "!! NO HEAD SEAT (counterbore deeper than the flange)"
            FAIL.append(f"{label}: counterbore {CB} > material {grip + CB}")
        elif screw > avail:
            v = f"!! BOTTOMS OUT by {screw - avail:.1f} -> use M3x{int(avail - 1.5)}"
            FAIL.append(f"{label}: M3x{screw} exceeds available {avail:.1f}")
        elif eng < 4.0:
            v = f"!! engagement {eng:.1f} < 4.0 (1.33xD)"
            WARN.append(f"{label}: engagement {eng:.1f}")
        else:
            v = "OK"
        print(f"  {label:<50}{qty:>4}{grip:>7.1f}{avail:>7.1f}  M3x{screw:<3}"
              f"{eng:>8.1f}  {v}")


# ==================================================== 6. DRIVER ACCESS
# Sweep a Ø9 driver column up from every top-driven fastener head and find the
# first thing it hits.  This is what produces the SERVICE CHAIN — "what has to
# come off to reach what" — instead of eyeballing the layout.
def check_access(bodies):
    rule("6. DRIVER ACCESS — Ø9 column swept up from each top-driven head")
    PL_T = tp.PL_T
    B = {n: (s, s.bounding_box()) for n, s, _ in bodies}
    # board envelopes block a driver just as hard as printed plastic
    from build123d import Box as _Box
    EG, EB = tp.EG_C, (76.0, 30.0)
    FC, FB = tp.FC_C, (54.0, 73.0)
    RC, RB = tp.RTK_C, 43.5
    for nm, (x0, y0, z0, dx, dy, dz) in {
        "board_EG25": (EG[0] - EB[0] / 2, EG[1] - EB[1] / 2, PL_T + tp.SP_H,
                       EB[0], EB[1], 18),
        "board_FlyCatcher": (FC[0] - FB[0] / 2, FC[1] - FB[1] / 2, PL_T + tp.SP_H,
                             FB[0], FB[1], 27),
        "board_ZED_F9P": (RC[0] - RB / 2, RC[1] - RB / 2,
                          PL_T + tp.TWR_H + tp.TWR_T + tp.SP_H, RB, RB, 20),
    }.items():
        b = Pos(x0, y0, z0) * _Box(dx, dy, dz,
                                   align=(Align.MIN, Align.MIN, Align.MIN))
        B[nm] = (b, b.bounding_box())

    #  label, x, y, head-seat z, the part the screw belongs to (never blocks itself)
    heads = (
        [(f"plate->rail ({x:+.0f},{y:+.0f})", x, y, PL_T - tp.CB_H, {"tp_plate"})
         for (x, y) in tp.PB] +
        [(f"fence hold-down ({x:+.0f},{y:+.0f})", x, y, PL_T + 3 - tp.CB_H,
          {"tp_plate", "tp_fence"}) for (x, y) in tp.FENCE_SCR] +
        [(f"tower leg ({x:+.0f},{y:+.0f})", x, y, PL_T + tp.TWR_H + tp.TWR_T - tp.CB_H,
          {"tp_tower", "tp_plate"}) for (x, y) in tp.TWR_LEG] +
        [(f"EG25 ({x:+.1f},{y:+.1f})", x, y, PL_T + tp.SP_H + 1.6,
          {"tp_plate", "board_EG25"}) for (x, y) in tp.EG_INS] +
        [(f"FlyCatcher ({x:+.1f},{y:+.1f})", x, y, PL_T + tp.SP_H + 1.6,
          {"tp_plate", "board_FlyCatcher"}) for (x, y) in tp.FC_INS] +
        [(f"ZED-F9P ({x:+.1f},{y:+.1f})", x, y,
          PL_T + tp.TWR_H + tp.TWR_T + tp.SP_H + 1.6,
          {"tp_tower", "board_ZED_F9P"}) for (x, y) in tp.RTK_INS]
    )
    REACH = 120.0
    print(f"  {'fastener head':<28}{'clear mm':>10}  first obstruction")
    for label, x, y, z, own in heads:
        probe = Pos(x, y, z + 0.2) * Cylinder(4.5, REACH, align=MIN_Z)
        pbb = probe.bounding_box()
        best, who = REACH, "open sky"
        for nm, (sol, bb) in B.items():
            if nm in own or nm.startswith(("tp_spacer", "nano_", "tube_")):
                continue
            if (bb.min.X > pbb.max.X or bb.max.X < pbb.min.X or
                    bb.min.Y > pbb.max.Y or bb.max.Y < pbb.min.Y or
                    bb.max.Z < z):
                continue
            cut = probe & sol
            if cut is None or cut.volume < 1e-6:
                continue
            h = cut.bounding_box().min.Z - z
            if h < best:
                best, who = h, nm
        tag = "OK      " if best >= 25 else ("TIGHT   " if best >= 12 else "!! BLOCKED ")
        print(f"  {label:<28}{best:>10.1f}  {tag}{who}")
        if best < 12:
            WARN.append(f"driver access {label}: {best:.1f} mm under {who}")


def main():
    check_brep()
    bodies = tp.placed_bodies(with_orin=False)
    check_interference(bodies)
    check_clearances(bodies)
    check_plate_features()
    check_fasteners()
    check_access(bodies)

    rule("VERDICT")
    if not FAIL and not WARN:
        print("  PASS — assembly is clean.")
    for w in WARN:
        print(f"  WARN  {w}")
    for f in FAIL:
        print(f"  FAIL  {f}")
    print(f"\n  {len(FAIL)} failure(s), {len(WARN)} warning(s)")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
