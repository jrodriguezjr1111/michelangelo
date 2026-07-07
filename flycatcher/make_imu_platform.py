"""
BNO085 IMU mounting platform.

A flat rectangular plate (29 × 78.9 × 3 mm) with two 4-hole patterns:
  - Set A: 20.41 × 18.04 mm  (X × Y)
  - Set B: 18.04 × 20.41 mm  (90° rotated)

The two sets are spaced along the long axis so the user can mount the IMU
in either orientation by choosing which pattern to use.

IMU holes are Ø2.7 mm (M2.5 clearance). Two additional M3 mounting holes
(Ø3.4) on the centerline, 58 mm apart, allow mounting the platform itself.
"""

from build123d import *
from pathlib import Path

# Platform
PLATE_L = 78.9          # X
PLATE_W = 29.0          # Y
PLATE_T = 3.0           # Z

# IMU hole pattern (one set)
PAT_A = 20.41           # along the longer axis of the IMU
PAT_B = 18.04           # along the shorter axis
HOLE_D = 2.7            # M2.5 clearance

# Centerline mounting holes
M3_SPACING = 58.0       # X spacing (lengthwise)
M3_D       = 3.4        # M3 clearance

# Two pattern centers along X, symmetric about origin
SET_A_CX = -PLATE_L / 4   # -19.725
SET_B_CX = +PLATE_L / 4   # +19.725

OUT_DIR = Path(__file__).parent


def hole_positions(cx, cy, dx, dy):
    """4 corner positions around (cx, cy) with full-pattern spacing dx × dy."""
    return [(cx + sx * dx / 2, cy + sy * dy / 2)
            for sx in (-1, 1) for sy in (-1, 1)]


def build_platform() -> Part:
    body = Box(PLATE_L, PLATE_W, PLATE_T,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Set A (pattern aligned with platform long axis: X = PAT_A, Y = PAT_B)
    for x, y in hole_positions(SET_A_CX, 0, PAT_A, PAT_B):
        body -= Pos(x, y, -0.2) * Cylinder(
            HOLE_D / 2, PLATE_T + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Set B (90° rotated: X = PAT_B, Y = PAT_A)
    for x, y in hole_positions(SET_B_CX, 0, PAT_B, PAT_A):
        body -= Pos(x, y, -0.2) * Cylinder(
            HOLE_D / 2, PLATE_T + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Centerline M3 mount holes
    for sx in (-1, 1):
        body -= Pos(sx * M3_SPACING / 2, 0, -0.2) * Cylinder(
            M3_D / 2, PLATE_T + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    return body


if __name__ == "__main__":
    part = build_platform()
    out = OUT_DIR / "imu_platform.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Plate: {PLATE_L} × {PLATE_W} × {PLATE_T} mm")
    print(f"  Set A center ({SET_A_CX}, 0): {PAT_A} × {PAT_B} mm, 4× Ø{HOLE_D}")
    print(f"  Set B center ({SET_B_CX}, 0): {PAT_B} × {PAT_A} mm (rotated 90°)")
    print(f"  Centerline M3: 2× Ø{M3_D} at X=±{M3_SPACING/2}, Y=0")

    # Edge clearance check (worst hole = farthest from center)
    a_max_x = abs(SET_A_CX) + PAT_A / 2
    a_max_y = PAT_B / 2
    b_max_x = abs(SET_B_CX) + PAT_B / 2
    b_max_y = PAT_A / 2
    print(f"  Set A edge clearance: X={PLATE_L/2 - a_max_x - HOLE_D/2:.2f}, "
          f"Y={PLATE_W/2 - a_max_y - HOLE_D/2:.2f} mm")
    print(f"  Set B edge clearance: X={PLATE_L/2 - b_max_x - HOLE_D/2:.2f}, "
          f"Y={PLATE_W/2 - b_max_y - HOLE_D/2:.2f} mm")
