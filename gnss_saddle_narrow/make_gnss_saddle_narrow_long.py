"""
CyberWing Canary — GNSS dual-tube saddle clamp, LONG variant.

Same quarter-wrap dual-tube geometry as `make_gnss_saddle_narrow.py`,
but the X axis is extended to 197 mm so the plate provides two device-
mounting zones outboard of the central tube grip:

Device-mount zones:
  +X end (concentric M3 patterns):
    - ZED-F9P    (4× M3, 37.6 × 37.6 sq)
    - Flycatcher (4× M3, 57.6 × 49.18 rect)
  −X end (two M2 patterns sharing one X center, side-by-side in Y):
    - M2 large   (4× M2, 45.90 × 18.27) shifted to +Y
    - M2 small   (4× M2, 19.95 × 17.80) shifted to −Y

The tube bores are limited to the central GRIP_LEN region so the
extension zones stay flat (no scoop intruding into the device mounts).

Coordinate frame:
  X = along tube axis (long plate axis)
  Y = across tubes
  Z = build direction (split plane at Z = HALF_HT)

Outputs:
  gnss_saddle_narrow_long_half.stl   (print 2 copies, mirror-identical)
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

TUBE_OD         = 15.39
TUBE_CENTER_SEP = 60.17
CLEARANCE       = 0.4

BLOCK_LEN = 197.0            # X — extended plate
BLOCK_WID = 60.0             # Y, across tubes (unchanged)
BLOCK_HT  = 28.0             # Z, total assembled height (unchanged)

GRIP_LEN  = 50.0             # X-length over which the tubes are actually clamped

# 4× M4 clamp bolts (unchanged)
BOLT_X_OFFSET = 18.0
BOLT_Y_OFFSET = 18.0
SCREW_CLEAR_D    = 4.4
SCREW_HEAD_D     = 8.0
SCREW_HEAD_DEPTH = 4.5

# Device-mount M3 holes — Ø3.4 clearance, thru
M3_D = 3.4

# ZED-F9P mount (square pattern), centered at (+ZED_CX, 0)
ZED_PAT  = 37.6
ZED_CX   = +65.0             # toward +X edge

# Flycatcher mount (rectangular pattern), CONCENTRIC with ZED on +X side
FLY_PAT_X = 57.6
FLY_PAT_Y = 49.18
FLY_CX    = +65.0

# M2 mounts on the −X side (Ø2.4 clearance)
M2_D = 2.4
M2A_PAT_X = 45.90
M2A_PAT_Y = 18.27
M2A_CX    = -62.0            # shared X center for both M2 patterns
M2A_CY    = +17.0            # pushed toward +Y edge
M2B_PAT_X = 19.95
M2B_PAT_Y = 17.80
M2B_CX    = -62.0            # same X center as M2A
M2B_CY    = -17.0            # pushed toward −Y edge

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived + sanity
# =============================================================================

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
TUBE_Y  = TUBE_CENTER_SEP / 2

assert R_IN + 2.0 <= HALF_HT, "Half-height too small for tube bore radius + wall"
assert TUBE_Y - BOLT_Y_OFFSET > R_IN + SCREW_CLEAR_D / 2 + 1.0, \
    "Clamp bolt clearance hole clashes with tube bore"

# ZED holes
_zed_x_min = ZED_CX - ZED_PAT / 2
_zed_x_max = ZED_CX + ZED_PAT / 2
assert _zed_x_min > GRIP_LEN / 2 + 1.0, \
    f"ZED pattern at X={_zed_x_min} clashes with tube grip end {GRIP_LEN/2}"
assert _zed_x_max + M3_D / 2 + 2.0 <= BLOCK_LEN / 2, \
    f"ZED pattern hits +X edge (need {_zed_x_max + M3_D/2 + 2.0} ≤ {BLOCK_LEN/2})"
assert ZED_PAT / 2 + M3_D / 2 + 1.0 <= BLOCK_WID / 2, "ZED pattern hits Y edge"

# Flycatcher holes
_fly_x_min = FLY_CX - FLY_PAT_X / 2
_fly_x_max = FLY_CX + FLY_PAT_X / 2
assert _fly_x_min > GRIP_LEN / 2 + 1.0, \
    f"Flycatcher pattern at X={_fly_x_min} clashes with tube grip end {GRIP_LEN/2}"
assert _fly_x_max + M3_D / 2 + 1.0 <= BLOCK_LEN / 2, \
    f"Flycatcher pattern hits +X edge"
assert FLY_PAT_Y / 2 + M3_D / 2 + 1.0 <= BLOCK_WID / 2, "Flycatcher Y hits edge"

# M2 patterns (−X side, shared X center, Y-offset)
for _nm, _cx, _cy, _px, _py in (("M2A", M2A_CX, M2A_CY, M2A_PAT_X, M2A_PAT_Y),
                                ("M2B", M2B_CX, M2B_CY, M2B_PAT_X, M2B_PAT_Y)):
    _x_near = _cx + _px / 2     # less negative (toward grip)
    _x_far  = _cx - _px / 2     # more negative (toward −X edge)
    assert _x_near < -GRIP_LEN / 2 - 1.0, \
        f"{_nm} pattern at X={_x_near} clashes with tube grip end {-GRIP_LEN/2}"
    assert _x_far - M2_D / 2 - 1.0 >= -BLOCK_LEN / 2, \
        f"{_nm} pattern hits −X edge"
    assert abs(_cy) + _py / 2 + M2_D / 2 + 0.5 <= BLOCK_WID / 2, \
        f"{_nm} pattern Y hits edge"
_m2_y_gap = (M2A_CY - M2A_PAT_Y / 2) - (M2B_CY + M2B_PAT_Y / 2)
assert _m2_y_gap >= 1.0, f"M2A and M2B overlap/too close in Y (gap {_m2_y_gap:.2f})"

# =============================================================================
# Build one half
# =============================================================================

def build_half() -> Part:
    block = Box(BLOCK_LEN, BLOCK_WID, HALF_HT,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Tube scoops — limited to the central grip region only
    for sy in (-1, 1):
        bore = Cylinder(R_IN, GRIP_LEN,
                        rotation=(0, 90, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        block -= Pos(0.0, sy * TUBE_Y, HALF_HT) * bore

    # 4× M4 clamp-bolt thru-holes + outer-face counterbore (head pocket)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * BOLT_X_OFFSET, sy * BOLT_Y_OFFSET
            block -= Pos(cx, cy, -0.2) * Cylinder(
                SCREW_CLEAR_D / 2, HALF_HT + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            block -= Pos(cx, cy, -0.05) * Cylinder(
                SCREW_HEAD_D / 2, SCREW_HEAD_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M3 ZED-F9P mount (37.6 × 37.6 square)
    for sx in (-1, 1):
        for sy in (-1, 1):
            block -= Pos(ZED_CX + sx * ZED_PAT / 2,
                         sy * ZED_PAT / 2, -0.2) * Cylinder(
                M3_D / 2, HALF_HT + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M3 flycatcher mount (57.6 × 49.18 rectangle)
    for sx in (-1, 1):
        for sy in (-1, 1):
            block -= Pos(FLY_CX + sx * FLY_PAT_X / 2,
                         sy * FLY_PAT_Y / 2, -0.2) * Cylinder(
                M3_D / 2, HALF_HT + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M2 mounts on −X side — two patterns, shared X center, Y-offset
    for cx, cy, px, py in ((M2A_CX, M2A_CY, M2A_PAT_X, M2A_PAT_Y),
                           (M2B_CX, M2B_CY, M2B_PAT_X, M2B_PAT_Y)):
        for sx in (-1, 1):
            for sy in (-1, 1):
                block -= Pos(cx + sx * px / 2,
                             cy + sy * py / 2, -0.2) * Cylinder(
                    M2_D / 2, HALF_HT + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))

    return block


def main() -> None:
    print("=" * 64)
    print("CyberWing GNSS narrow saddle (LONG, 197 mm) — build123d")
    print("=" * 64)
    print(f"Block:      {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT} mm assembled")
    print(f"Tubes:      Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f}, grip span {GRIP_LEN} mm "
          f"(X = ±{GRIP_LEN/2})")
    print(f"Bore ID:    Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"Clamp:      4× M4 at (±{BOLT_X_OFFSET}, ±{BOLT_Y_OFFSET}) "
          f"with Ø{SCREW_HEAD_D}×{SCREW_HEAD_DEPTH} head pocket")
    print(f"ZED-F9P:    4× Ø{M3_D} at X={ZED_CX:+}±{ZED_PAT/2}, Y=±{ZED_PAT/2} "
          f"({ZED_PAT}×{ZED_PAT} sq)")
    print(f"Flycatcher: 4× Ø{M3_D} at X={FLY_CX:+}±{FLY_PAT_X/2}, "
          f"Y=±{FLY_PAT_Y/2} ({FLY_PAT_X}×{FLY_PAT_Y} rect)")
    print(f"M2 large:   4× Ø{M2_D} at X={M2A_CX:+}±{M2A_PAT_X/2}, "
          f"Y={M2A_CY:+}±{M2A_PAT_Y/2} ({M2A_PAT_X}×{M2A_PAT_Y})")
    print(f"M2 small:   4× Ø{M2_D} at X={M2B_CX:+}±{M2B_PAT_X/2}, "
          f"Y={M2B_CY:+}±{M2B_PAT_Y/2} ({M2B_PAT_X}×{M2B_PAT_Y})")

    half = build_half()
    out = OUT_DIR / "gnss_saddle_narrow_long_half.stl"
    export_stl(half, str(out))
    print(f"\n  ✓ {out.name} ({out.stat().st_size:,} bytes)")
    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Print 2 copies per saddle.")
    print("Hardware: 4× M4 × 30 mm socket caps + M4 nuts per saddle.")


if __name__ == "__main__":
    main()
