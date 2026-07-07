"""
GNSS saddle (Y-wide) — TOP PLATE for the +Y wing (ZED-F9P side).

Companion to `make_gnss_saddle_wide_top.py` (which covers the −Y M2 wing).
This flat cover/mount plate bolts onto the +Y wing of
`make_gnss_saddle_wide.py`, carrying the ZED-F9P mount pattern:

  - ZED-F9P : 4× M3 on a 37.6 × 37.6 mm square, centered at Y = 75.5

Hole centers (X, Y) match the saddle exactly (constants imported from
`make_gnss_saddle_wide`), so the plate drops straight onto the wing.
Holes are Ø3.4 M3 clearance with a Ø6.2 countersink on the top face so
M3 heads sit flush.

Output:
  gnss_saddle_wide_top_zed.stl
"""

from build123d import *
from pathlib import Path

from make_gnss_saddle_wide import (
    BLOCK_LEN, BLOCK_WID,
    ZED_PATTERN, ZED_Y_CENTER,
    M3_CLEAR_D, M3_CSK_D, M3_CSK_DEPTH,
)

# =============================================================================
# Plate parameters
# =============================================================================
PLATE_T = 3.0                # thickness
MARGIN  = 4.0                # material around the outermost holes

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived footprint (Y span covers the ZED square, clamped to the +Y edge)
# =============================================================================
_zx = ZED_PATTERN / 2
_y_holes = [ZED_Y_CENTER + sy * ZED_PATTERN / 2 for sy in (-1, 1)]
PLATE_Y_MIN = min(_y_holes) - MARGIN
PLATE_Y_MAX = min(max(_y_holes) + MARGIN, BLOCK_WID / 2)     # don't exceed +Y edge
PLATE_WID   = PLATE_Y_MAX - PLATE_Y_MIN
PLATE_Y_CEN = (PLATE_Y_MAX + PLATE_Y_MIN) / 2

# X width: at least the saddle clamp length, widened if the csk needs room.
PLATE_X = max(BLOCK_LEN, 2 * (_zx + M3_CSK_D / 2 + MARGIN))

# =============================================================================
# Sanity
# =============================================================================
assert _zx + M3_CSK_D / 2 + 0.5 < PLATE_X / 2, "ZED csk hits plate X edge"
assert min(_y_holes) - M3_CSK_D / 2 > PLATE_Y_MIN, "ZED csk hits −Y plate edge"
assert max(_y_holes) + M3_CSK_D / 2 < PLATE_Y_MAX, "ZED csk hits +Y plate edge"
assert M3_CSK_DEPTH < PLATE_T, "Countersink deeper than plate"


def build_plate() -> Part:
    plate = Pos(0.0, PLATE_Y_CEN, 0.0) * Box(
        PLATE_X, PLATE_WID, PLATE_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M3 clearance holes + top-face countersink (ZED square).
    for sx in (-1, 1):
        for sy in (-1, 1):
            mx = sx * ZED_PATTERN / 2
            my = ZED_Y_CENTER + sy * ZED_PATTERN / 2
            plate -= Pos(mx, my, -0.2) * Cylinder(
                M3_CLEAR_D / 2, PLATE_T + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            plate -= Pos(mx, my, PLATE_T - M3_CSK_DEPTH) * Cylinder(
                M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return plate


def main() -> None:
    print("=" * 64)
    print("GNSS saddle (Y-wide) — +Y wing TOP PLATE (ZED-F9P side)")
    print("=" * 64)
    print(f"Plate:    {PLATE_X:.2f} × {PLATE_WID:.2f} × {PLATE_T} mm "
          f"(Y center {PLATE_Y_CEN:.2f})")
    print(f"Y span:   {PLATE_Y_MIN:.2f} .. {PLATE_Y_MAX:.2f} mm")
    print(f"ZED-F9P:  4× Ø{M3_CLEAR_D} at (±{_zx:.2f}, "
          f"{ZED_Y_CENTER - ZED_PATTERN/2:.2f}..{ZED_Y_CENTER + ZED_PATTERN/2:.2f}) "
          f"— {ZED_PATTERN} × {ZED_PATTERN}")
    print(f"Csk:      Ø{M3_CSK_D} × {M3_CSK_DEPTH} on top face (flush M3 heads)")

    plate = build_plate()
    out = OUT_DIR / "gnss_saddle_wide_top_zed.stl"
    export_stl(plate, str(out))
    print(f"\n  ✓ {out.name} ({out.stat().st_size:,} bytes)")
    print("\nPrint flat on bed, countersink face UP. No supports.")


if __name__ == "__main__":
    main()
