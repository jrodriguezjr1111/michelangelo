"""
CyberWing Canary — Jetson box tube-mount X-FRAME (top clamp half / hub).

A drone-style frame that sits on the two GNSS tubes and carries the Jetson/RSD
box. The tubes run PERPENDICULAR to the box's long side (along Y, crossing the
box). The HUB straddles both tubes (half-pipe scoops on the clamp face) and uses
the standard saddle clamp pattern (4× M4 at ±18,±18) so a matching bottom half
bolts on (rotated 90°) to capture the tubes. Four arms reach out to corner
bosses with M3 heat-set inserts at the box's bottom-plate pattern (172 × 104).

Coordinate frame (as modeled / as printed):
  X = across tubes (box long axis, 200 side)
  Y = tube axis (box short axis)
  Z = 0 is the BOX-MOUNT face (flat, on the bed); structure rises in +Z to the
      tube-clamp face at Z = HUB_H (tube scoops open there).
In use the part is flipped: tubes cup into the scoops below, box bolts on top.

Outputs:
  jetson_tube_xframe.stl
"""

from build123d import *
import math
from pathlib import Path

# ---- tubes (run along Y) ---------------------------------------------------
TUBE_OD         = 15.39
TUBE_CENTER_SEP = 60.17
CLEARANCE       = 0.4
R_IN   = TUBE_OD / 2 + CLEARANCE / 2     # 7.895
TUBE_X = TUBE_CENTER_SEP / 2             # 30.085  (tube positions in X now)

# ---- box bottom-plate mount pattern (172 × 104) ----------------------------
BOX_PAT_X = 172.0
BOX_PAT_Y = 104.0
CX = BOX_PAT_X / 2                       # 86
CY = BOX_PAT_Y / 2                       # 52

# ---- standard saddle clamp bolts (mate with the other half) ----------------
CLAMP_OFF = 18.0
CLAMP_D   = 4.4                          # M4 clearance

# ---- M3 heat-set inserts (box mount) ---------------------------------------
INSERT_D     = 4.4
INSERT_DEPTH = 6.0
INSERT_CHAM  = 0.6

# ---- hub / arms / bosses ---------------------------------------------------
HUB_X   = 96.0                           # across tubes; fully contains both scoops
HUB_Y   = 50.0                           # tube grip length (along Y)
HUB_H   = 14.0                           # clamp-face at top; scoops cut here
ARM_W   = 12.0
ARM_H   = 8.0
BOSS_OD = 13.0
BOSS_H  = 10.0
ARM_ATTACH = (45.0, 22.0)                # hub corner anchor (outboard of tube scoops)

OUT_DIR = Path(__file__).parent

# ---- sanity ----------------------------------------------------------------
assert TUBE_X + R_IN < HUB_X / 2 - 1.0, "tube scoop exits the hub in X"
assert R_IN + 2.0 <= HUB_H, "hub too short for tube scoop + wall"
assert CLAMP_OFF + CLAMP_D / 2 + 1.0 < TUBE_X - R_IN, "clamp bolt clashes tube scoop"
assert ARM_ATTACH[0] - ARM_W / 2 > TUBE_X + R_IN, "arm root overlaps tube scoop"
assert INSERT_DEPTH < BOSS_H - 1.0, "insert too deep for boss"


def build_frame() -> Part:
    # central hub
    frame = Box(HUB_X, HUB_Y, HUB_H, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # tube scoops on the clamp face (top, Z = HUB_H), full cylinders along Y
    for sx in (-1, 1):
        bore = Cylinder(R_IN, HUB_Y + 0.4, rotation=(90, 0, 0), align=(Align.CENTER,) * 3)
        frame -= Pos(sx * TUBE_X, 0.0, HUB_H) * bore

    # 4× M4 clamp holes (mate with the other half)
    for sx in (-1, 1):
        for sy in (-1, 1):
            frame -= Pos(sx * CLAMP_OFF, sy * CLAMP_OFF, -0.2) * Cylinder(
                CLAMP_D / 2, HUB_H + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4 arms + corner bosses (added AFTER scoops so they aren't carved)
    ax, ay = ARM_ATTACH
    for sx in (-1, 1):
        for sy in (-1, 1):
            hx, hy = sx * ax, sy * ay          # hub anchor
            bx, by = sx * CX, sy * CY          # boss center
            mx, my = (hx + bx) / 2, (hy + by) / 2
            ang = math.degrees(math.atan2(by - hy, bx - hx))
            L = math.hypot(bx - hx, by - hy) + 16
            arm = Box(L, ARM_W, ARM_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
            frame += Pos(mx, my, 0) * (Rot(0, 0, ang) * arm)
            frame += Pos(bx, by, 0) * Cylinder(
                BOSS_OD / 2, BOSS_H, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # M3 insert bores in the bosses, open on the BOX face (Z = 0)
    for sx in (-1, 1):
        for sy in (-1, 1):
            bx, by = sx * CX, sy * CY
            frame -= Pos(bx, by, -0.01) * Cylinder(
                INSERT_D / 2, INSERT_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MIN))
            frame -= Pos(bx, by, -0.01) * Cone(
                INSERT_D / 2 + INSERT_CHAM, INSERT_D / 2, INSERT_CHAM,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return frame


def main() -> None:
    print("CyberWing Jetson tube-mount X-frame — tubes ⟂ box long side (along Y)")
    print(f"  hub {HUB_X} × {HUB_Y} × {HUB_H}; tubes Ø{TUBE_OD} along Y at X±{TUBE_X:.2f}")
    print(f"  clamp: 4× M4 at ±{CLAMP_OFF} (mates a standard saddle half, rotated 90°)")
    print(f"  box mount: 4× M3 inserts Ø{INSERT_D}×{INSERT_DEPTH} at (±{CX}, ±{CY}) = {BOX_PAT_X}×{BOX_PAT_Y}")
    frame = build_frame()
    out = OUT_DIR / "jetson_tube_xframe.stl"
    export_stl(frame, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)")
    print("  Print box-face down (scoops open up). Flip to use; inserts in the up face.")


if __name__ == "__main__":
    main()
