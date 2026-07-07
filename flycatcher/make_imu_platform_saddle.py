"""
Flycatcher platform — saddle-mount variant.

Hollow-box (3 mm top, 2.5 mm walls) with cable openings on ±X walls.
Through-holes:
  - 4× Ø3.4 (M3 clearance), 58 × 49 mm pattern, centered.
  - 4× Ø4.4 (M4 clearance), 36.14 × 36.1 mm pattern, centered.

Coordinate frame (origin = plate center):
  X = long axis (101 mm, parallel to tubes).
  Y = short axis (PLATE_W mm; internal cavity = 60 mm).
  Cable openings on the ±X walls so cables exit parallel to the tubes.
  Z = build direction (PLATE_H = 29 mm). z=0 = bottom (cavity opening),
      z=PLATE_H = top face. STL is flipped at export so top face prints
      DOWN on the bed.
"""

from build123d import *
from pathlib import Path

# Plate
PLATE_L  = 101.0                 # X (long axis, parallel to tubes)
INNER_W  = 60.0                  # cavity Y (internal width)
TOP_T    = 3.0
WALL_T   = 2.5
PLATE_W  = INNER_W + 2 * WALL_T  # Y (short axis, external)
PLATE_H  = 29.0                  # Z

# Cable openings on ±X walls (60 mm sides), Y-centered — cables exit
# parallel to the tubes.
SLOT_W        = 38.0    # along Y
SLOT_H        = 7.8     # along Z
SLOT_Z_CENTER = (PLATE_H - TOP_T) / 2 - 2.0  # shifted -Z by 2 mm

# 4× M3 holes (M3 clearance) — 58 × 49 mm pattern, centered on plate.
M3_PAT_X = 58.0
M3_PAT_Y = 49.0
M3_D     = 3.4

# 4× M4 holes (M4 clearance) — 36.14 × 36.1 mm pattern, centered on plate.
M4_PAT_X            = 36.14
M4_PAT_Y            = 36.1
M4_D                = 4.4
M4_DY               = 0.0   # centered (no +Y offset)

OUT_DIR = Path(__file__).parent

# Sanity
assert M3_PAT_X / 2 + M3_D / 2 + 1 < PLATE_L / 2, "M3 hole hits X edge"
assert M3_PAT_Y / 2 + M3_D / 2 + 0.5 < PLATE_W / 2, "M3 hole hits Y edge"
assert M4_PAT_X / 2 + M4_D / 2 + 0.5 < PLATE_L / 2, "M4 hole hits X edge"
for _sy in (-1, 1):
    _y = M4_DY + _sy * M4_PAT_Y / 2
    assert abs(_y) + M4_D / 2 + 0.4 < PLATE_W / 2, f"M4 hole at Y={_y} hits Y edge"


def build_platform() -> Part:
    body = Box(PLATE_L, PLATE_W, PLATE_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Hollow underside (no central post)
    body -= Box(PLATE_L - 2 * WALL_T,
                PLATE_W - 2 * WALL_T,
                PLATE_H - TOP_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Cable openings on ±X walls (cables run parallel to tubes)
    body -= Pos(PLATE_L / 2 + 0.2, 0, SLOT_Z_CENTER - SLOT_H / 2) * Box(
        WALL_T + 0.8, SLOT_W, SLOT_H,
        align=(Align.MAX, Align.CENTER, Align.MIN))
    body -= Pos(-PLATE_L / 2 - 0.2, 0, SLOT_Z_CENTER - SLOT_H / 2) * Box(
        WALL_T + 0.8, SLOT_W, SLOT_H,
        align=(Align.MIN, Align.CENTER, Align.MIN))

    # 4× M3 holes, 58 × 49 mm pattern, centered.
    for sx in (-1, 1):
        for sy in (-1, 1):
            body -= Pos(sx * M3_PAT_X / 2, sy * M3_PAT_Y / 2, -0.2) * Cylinder(
                M3_D / 2, PLATE_H + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M4 holes, 36.14 × 36.1 mm pattern, centered.
    for sx in (-1, 1):
        for sy in (-1, 1):
            body -= Pos(sx * M4_PAT_X / 2,
                        M4_DY + sy * M4_PAT_Y / 2, -0.2) * Cylinder(
                M4_D / 2, PLATE_H + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return body


if __name__ == "__main__":
    part = build_platform()
    # Flip so top face sits on the bed
    part = Rot(180, 0, 0) * part
    part = Pos(0, 0, PLATE_H) * part

    out = OUT_DIR / "imu_platform_saddle.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Plate:        {PLATE_L} × {PLATE_W} × {PLATE_H} mm "
          f"(top {TOP_T}, walls {WALL_T}, hollow, no post)")
    print(f"  Cable slots:  {SLOT_W} × {SLOT_H} mm on ±X walls (Y-centered) — parallel to tubes")
    print(f"  M3 holes:     4× Ø{M3_D} at X=±{M3_PAT_X/2}, Y=±{M3_PAT_Y/2} "
          f"({M3_PAT_X} × {M3_PAT_Y} mm, centered)")
    print(f"  M4 holes:     4× Ø{M4_D} at X=±{M4_PAT_X/2}, Y=±{M4_PAT_Y/2} "
          f"({M4_PAT_X} × {M4_PAT_Y} mm, centered)")
    print(f"  Print top-face DOWN on bed. No supports.")
