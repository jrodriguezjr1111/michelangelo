"""
GNSS saddle (Y-wide) — TOP PLATE for the −Y wing.

A flat cover/mount plate that bolts onto the −Y wing of
`make_gnss_saddle_wide.py`, carrying the two M2 hole patterns:

  - M2 small : 19.95 × 17.81 mm
  - M2 large : 45.90 × 18.27 mm

Hole centers (X, Y) match the saddle exactly (constants imported from
`make_gnss_saddle_wide`), so the plate drops straight onto the wing.
Holes are Ø2.4 M2 clearance with a countersink on the top face so M2
screw heads sit flush.

Output:
  gnss_saddle_wide_top.stl
"""

from build123d import *
from pathlib import Path

from make_gnss_saddle_wide import (
    BLOCK_LEN, BLOCK_WID, M2_CLEAR_D,
    M2S_PAT_X, M2S_PAT_Y, M2S_Y_CENTER,
    M2L_PAT_X, M2L_PAT_Y, M2L_Y_CENTER,
)

# =============================================================================
# Plate parameters
# =============================================================================
PLATE_T = 3.0                # thickness
MARGIN  = 4.0                # material around the outermost holes

M2_CSK_D     = 4.0           # countersink OD on top face (M2 pan/csk head)
M2_CSK_DEPTH = 1.2

# Both M2 patterns as (pat_x, pat_y, y_center) triples.
M2_PATTERNS = [
    (M2S_PAT_X, M2S_PAT_Y, M2S_Y_CENTER),
    (M2L_PAT_X, M2L_PAT_Y, M2L_Y_CENTER),
]

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived plate footprint (Y span covers both patterns, clamped to block edge)
# =============================================================================
_y_holes = [cy + sy * py / 2 for _, py, cy in M2_PATTERNS for sy in (-1, 1)]
PLATE_Y_MIN = max(min(_y_holes) - MARGIN, -BLOCK_WID / 2)   # don't exceed −Y edge
PLATE_Y_MAX = max(_y_holes) + MARGIN
PLATE_WID   = PLATE_Y_MAX - PLATE_Y_MIN
PLATE_Y_CEN = (PLATE_Y_MAX + PLATE_Y_MIN) / 2

# X width: at least the saddle clamp length, widened if the csk needs room.
_max_hole_x = max(px / 2 for px, _, _ in M2_PATTERNS)
PLATE_X = max(BLOCK_LEN, 2 * (_max_hole_x + M2_CSK_D / 2 + MARGIN))

# =============================================================================
# Sanity
# =============================================================================
assert _max_hole_x + M2_CSK_D / 2 + 0.5 < PLATE_X / 2, "M2 csk hits plate X edge"
assert min(_y_holes) - M2_CSK_D / 2 > PLATE_Y_MIN, "M2 csk hits −Y plate edge"
assert max(_y_holes) + M2_CSK_D / 2 < PLATE_Y_MAX, "M2 csk hits +Y plate edge"
assert M2_CSK_DEPTH < PLATE_T, "Countersink deeper than plate"


def build_plate() -> Part:
    plate = Pos(0.0, PLATE_Y_CEN, 0.0) * Box(
        PLATE_X, PLATE_WID, PLATE_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # M2 clearance holes + top-face countersink, both patterns.
    for px, py, cy in M2_PATTERNS:
        for sx in (-1, 1):
            for sy in (-1, 1):
                mx, my = sx * px / 2, cy + sy * py / 2
                plate -= Pos(mx, my, -0.2) * Cylinder(
                    M2_CLEAR_D / 2, PLATE_T + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
                plate -= Pos(mx, my, PLATE_T - M2_CSK_DEPTH) * Cylinder(
                    M2_CSK_D / 2, M2_CSK_DEPTH + 0.1,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))

    return plate


def main() -> None:
    print("=" * 64)
    print("GNSS saddle (Y-wide) — −Y wing TOP PLATE")
    print("=" * 64)
    print(f"Plate:    {PLATE_X} × {PLATE_WID:.2f} × {PLATE_T} mm "
          f"(Y center {PLATE_Y_CEN:.2f})")
    print(f"Y span:   {PLATE_Y_MIN:.2f} .. {PLATE_Y_MAX:.2f} mm")
    print(f"M2 small: 4× Ø{M2_CLEAR_D} at (±{M2S_PAT_X/2:.2f}, "
          f"{M2S_Y_CENTER - M2S_PAT_Y/2:.2f}..{M2S_Y_CENTER + M2S_PAT_Y/2:.2f})")
    print(f"M2 large: 4× Ø{M2_CLEAR_D} at (±{M2L_PAT_X/2:.2f}, "
          f"{M2L_Y_CENTER - M2L_PAT_Y/2:.2f}..{M2L_Y_CENTER + M2L_PAT_Y/2:.2f})")
    print(f"Csk:      Ø{M2_CSK_D} × {M2_CSK_DEPTH} on top face (flush M2 heads)")

    plate = build_plate()
    out = OUT_DIR / "gnss_saddle_wide_top.stl"
    export_stl(plate, str(out))
    print(f"\n  ✓ {out.name} ({out.stat().st_size:,} bytes)")
    print("\nPrint flat on bed, csk face UP. No supports.")


if __name__ == "__main__":
    main()
