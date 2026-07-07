"""
Flycatcher GPS RTK2 platform variant.

Hollow-box (3 mm top, 2.5 mm walls). Through-holes:
  - 4× Ø3.4 (M3 clearance) — 38.03 × 38.03 mm square, centered (RTK2 mount).
  - 4× Ø3.4 (M3 clearance) — 58 × 49 mm rectangle, centered
    (matches IMU saddle plate's M3 pattern for stacking).

Cable openings on ±X walls:
  -X wall : 37 × 7.8 mm rectangular slot (cables exit parallel to tubes).
  +X wall : Ø6.38 mm circular hole (single cable / connector pass-through).

Coordinate frame (origin = plate center):
  X = long axis (80 mm). Y = short axis (PLATE_W; cavity = 60 mm).
  Z = build direction (PLATE_H = 20 mm). STL is flipped at export so
  top face prints DOWN on the bed.
"""

from build123d import *
from pathlib import Path

# Plate
PLATE_L  = 80.0
INNER_W  = 60.0
TOP_T    = 3.0
WALL_T   = 2.5
PLATE_W  = INNER_W + 2 * WALL_T   # 65.0
PLATE_H  = 20.0

# Cable slot on -X wall (rectangular)
SLOT_W        = 37.0
SLOT_H        = 7.8
SLOT_Z_CENTER = (PLATE_H - TOP_T) / 2 - 2.0   # matches IMU plate (-Z 2 mm)

# Circular cable hole on +X wall
HOLE_D        = 6.38
HOLE_Y_CENTER = 0.0
HOLE_Z_CENTER = SLOT_Z_CENTER

M3_D = 3.4

# 4× M3 holes — RTK2 mount, 38.03 × 38.03 mm square, centered.
M3_RTK_PAT_X = 38.03
M3_RTK_PAT_Y = 38.03

# 4× M3 holes — matches IMU saddle plate (58 × 49 mm), centered.
M3_IMU_PAT_X = 58.0
M3_IMU_PAT_Y = 49.0

OUT_DIR = Path(__file__).parent

# Sanity
assert M3_RTK_PAT_X / 2 + M3_D / 2 + 1 < PLATE_L / 2, "M3 (RTK) hole hits X edge"
assert M3_RTK_PAT_Y / 2 + M3_D / 2 + 0.5 < PLATE_W / 2, "M3 (RTK) hole hits Y edge"
assert M3_IMU_PAT_X / 2 + M3_D / 2 + 1 < PLATE_L / 2, "M3 (IMU) hole hits X edge"
assert M3_IMU_PAT_Y / 2 + M3_D / 2 + 0.5 < PLATE_W / 2, "M3 (IMU) hole hits Y edge"
assert HOLE_D / 2 + 0.5 < PLATE_W / 2, "Circular hole exceeds wall Y span"
assert HOLE_Z_CENTER + HOLE_D / 2 < PLATE_H - TOP_T, "Circular hole hits ceiling"
assert HOLE_Z_CENTER - HOLE_D / 2 > 0, "Circular hole hits floor"


def build_platform() -> Part:
    body = Box(PLATE_L, PLATE_W, PLATE_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Hollow underside
    body -= Box(PLATE_L - 2 * WALL_T,
                PLATE_W - 2 * WALL_T,
                PLATE_H - TOP_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Rectangular cable slot on -X wall
    body -= Pos(-PLATE_L / 2 - 0.2, 0, SLOT_Z_CENTER - SLOT_H / 2) * Box(
        WALL_T + 0.8, SLOT_W, SLOT_H,
        align=(Align.MIN, Align.CENTER, Align.MIN))

    # Circular cable hole on +X wall (Ø6.38). Axis along X.
    body -= Pos(PLATE_L / 2 + 0.2, HOLE_Y_CENTER, HOLE_Z_CENTER) * Rot(0, 90, 0) * Cylinder(
        HOLE_D / 2, WALL_T + 0.8,
        align=(Align.CENTER, Align.CENTER, Align.MAX))

    # 4× M3 (RTK2 mount), 38.03 × 38.03 mm square, centered.
    # 4× M3 (IMU plate pattern), 58 × 49 mm, centered.
    for pat_x, pat_y in ((M3_RTK_PAT_X, M3_RTK_PAT_Y),
                         (M3_IMU_PAT_X, M3_IMU_PAT_Y)):
        for sx in (-1, 1):
            for sy in (-1, 1):
                body -= Pos(sx * pat_x / 2, sy * pat_y / 2, -0.2) * Cylinder(
                    M3_D / 2, PLATE_H + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))

    return body


if __name__ == "__main__":
    part = build_platform()
    part = Rot(180, 0, 0) * part
    part = Pos(0, 0, PLATE_H) * part

    out = OUT_DIR / "gps_rtk2_platform.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Plate:        {PLATE_L} × {PLATE_W} × {PLATE_H} mm "
          f"(top {TOP_T}, walls {WALL_T}, hollow)")
    print(f"  -X cable slot: {SLOT_W} × {SLOT_H} mm rectangular (Z-center {SLOT_Z_CENTER})")
    print(f"  +X cable hole: Ø{HOLE_D} circular at Y=0, Z={HOLE_Z_CENTER}")
    print(f"  M3 (RTK2):    4× Ø{M3_D} at X=±{M3_RTK_PAT_X/2}, Y=±{M3_RTK_PAT_Y/2} "
          f"({M3_RTK_PAT_X} × {M3_RTK_PAT_Y} mm square, centered)")
    print(f"  M3 (IMU):     4× Ø{M3_D} at X=±{M3_IMU_PAT_X/2}, Y=±{M3_IMU_PAT_Y/2} "
          f"({M3_IMU_PAT_X} × {M3_IMU_PAT_Y} mm, centered)")
    print(f"  Print top-face DOWN on bed. No supports.")
