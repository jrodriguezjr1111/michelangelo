"""
CyberWing — Jetson Nano tube-clamp plate (MERGED: nano_xbase ⊕ tube clamp).

Combines the Nano adapter plate (make_nano_xbase.py) with the GNSS dual-tube
clamp (make_jetson_tube_xframe.py) into ONE piece: the Nano plate itself grips
the two tubes (half-pipe scoops on the underside) instead of bolting to a
separate saddle. A matching lower clamp half bolts on via the 4× M4 pattern.

Frame (tube axis ∥ the short / 58.25 side, per spec):
  X = tube axis (Nano 58.25 dir);  Y = across tubes (Nano 86.14 dir);  Z = up.
  Tubes (Ø15.39) run along X at Y = ±30.085; Nano mounts on TOP, over the GNSS hole.

STEP A — core merge only (clamp + Nano standoffs + Ø30 GNSS passthrough + M4).
STEP B will add: strengthening, RSD side-mount (long edge ∥ ground), upright
component-plate posts.

Output: nano_tubeclamp.stl
"""

from build123d import *
from pathlib import Path

# ---- Nano mount pattern (tube axis = X = 58.25; across = Y = 86.14) ----
NANO_X, NANO_Y = 58.25 / 2, 86.14 / 2          # ±29.13, ±43.07
SO_OD, SO_H, SO_PILOT = 6.0, 6.0, 2.5          # M3 self-tap standoffs

# ---- tubes (along X) at Y = ±30.085 ----
TUBE_OD, TUBE_SEP, CLR = 15.39, 60.17, 0.4
R_IN   = TUBE_OD / 2 + CLR / 2                  # 7.895
TUBE_Y = TUBE_SEP / 2                           # 30.085

# ---- GNSS pass-through (kept) ----
GNSS_D = 30.0

# ---- M4 saddle clamp (mates the lower half) ----
M4_P, M4_CLR, M4_CB_D, M4_CB_DEPTH = 18.0, 4.4, 8.0, 4.5

# ---- hub (clamp block) ----
HUB_X, HUB_Y, HUB_H = 72.0, 100.0, 14.0         # X tube-axis length; Y spans the Nano rows; H clamp depth

# ---- 2 M3 inserts in the +X long-edge SIDE face (attach plate bolts to the side) ----
ATT_INS_D, ATT_INS_H, ATT_CHAM = 4.0, 6.0, 0.6  # M3 heat-set, bored horizontally (-X)
ATT_Y = 20.0                                     # ±20 -> 40 mm apart along the +X edge (Y)
ATT_Z = HUB_H / 2                                # 7.0 — mid-height of the 14 mm wall
SHORT_X = 20.0                                    # short-side inserts at X=±20 -> 40 mm apart

OUT_DIR = Path(__file__).parent

# ---- sanity ----
assert R_IN + 2.0 <= HUB_H, "hub too short for tube scoop + wall"
assert GNSS_D / 2 + 1.0 < TUBE_Y - R_IN, "GNSS hole clashes the tube scoops"
assert M4_P + M4_CLR / 2 + 1.0 < TUBE_Y - R_IN, "M4 bolt clashes a tube scoop"
assert NANO_Y + SO_OD / 2 + 1.0 < HUB_Y / 2, "Nano standoffs exit the hub in Y"
assert NANO_X + SO_OD / 2 < HUB_X / 2, "Nano standoffs exit the hub in X"


def build() -> Part:
    p = Box(HUB_X, HUB_Y, HUB_H, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # tube scoops: half-pipe grooves in the BOTTOM face (z=0), along X at Y=±TUBE_Y
    for sy in (-1, 1):
        bore = Cylinder(R_IN, HUB_X + 0.4, rotation=(0, 90, 0), align=(Align.CENTER,) * 3)
        p -= Pos(0.0, sy * TUBE_Y, 0.0) * bore

    # central Ø30 GNSS pass-through
    p -= Pos(0, 0, -0.2) * Cylinder(GNSS_D / 2, HUB_H + 0.4,
                                    align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M4 clamp: clearance through + head/nut counterbore on the TOP face
    for sx in (-1, 1):
        for sy in (-1, 1):
            p -= Pos(sx * M4_P, sy * M4_P, -0.2) * Cylinder(
                M4_CLR / 2, HUB_H + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN))
            p -= Pos(sx * M4_P, sy * M4_P, HUB_H - M4_CB_DEPTH) * Cylinder(
                M4_CB_D / 2, M4_CB_DEPTH + 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Nano standoffs on the TOP face (board over the GNSS hole)
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Pos(sx * NANO_X, sy * NANO_Y, HUB_H)
            p += c * Cylinder(SO_OD / 2, SO_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
            p -= c * Cylinder(SO_PILOT / 2, SO_H + 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 2 M3 inserts bored horizontally (-X) into the +X long-edge SIDE face
    for sy in (-1, 1):
        c = Pos(HUB_X / 2 + 0.01, sy * ATT_Y, ATT_Z)
        p -= c * (Rot(0, 90, 0) * Cylinder(ATT_INS_D / 2, ATT_INS_H,
                                           align=(Align.CENTER, Align.CENTER, Align.MAX)))
        p -= c * (Rot(0, 90, 0) * Cone(ATT_INS_D / 2, ATT_INS_D / 2 + ATT_CHAM, ATT_CHAM,
                                       align=(Align.CENTER, Align.CENTER, Align.MAX)))

    # 2 M3 inserts in EACH short (±Y) side face (bored horizontally, inward)
    for sx in (-1, 1):
        cp = Pos(sx * SHORT_X, HUB_Y / 2 + 0.01, ATT_Z)        # +Y face, bore -Y
        p -= cp * (Rot(-90, 0, 0) * Cylinder(ATT_INS_D / 2, ATT_INS_H,
                                             align=(Align.CENTER, Align.CENTER, Align.MAX)))
        p -= cp * (Rot(-90, 0, 0) * Cone(ATT_INS_D / 2, ATT_INS_D / 2 + ATT_CHAM, ATT_CHAM,
                                         align=(Align.CENTER, Align.CENTER, Align.MAX)))
        cm = Pos(sx * SHORT_X, -HUB_Y / 2 - 0.01, ATT_Z)       # -Y face, bore +Y
        p -= cm * (Rot(90, 0, 0) * Cylinder(ATT_INS_D / 2, ATT_INS_H,
                                            align=(Align.CENTER, Align.CENTER, Align.MAX)))
        p -= cm * (Rot(90, 0, 0) * Cone(ATT_INS_D / 2, ATT_INS_D / 2 + ATT_CHAM, ATT_CHAM,
                                        align=(Align.CENTER, Align.CENTER, Align.MAX)))

    return p


if __name__ == "__main__":
    part = build()
    out = OUT_DIR / "nano_tubeclamp.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  hub {HUB_X}×{HUB_Y}×{HUB_H}; tubes Ø{TUBE_OD} along X at Y=±{TUBE_Y:.2f}")
    print(f"  GNSS Ø{GNSS_D} center pass-through; 4× M4 clamp at ±{M4_P}")
    print(f"  Nano: 4× Ø{SO_OD}×{SO_H} standoffs (Ø{SO_PILOT} pilot) at (±{NANO_X:.2f}, ±{NANO_Y:.2f})")
    print("  STEP A (core merge). Print scoops-up; flip to use. Next: strengthen + RSD + posts.")
