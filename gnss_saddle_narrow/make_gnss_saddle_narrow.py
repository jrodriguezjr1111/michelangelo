"""
CyberWing Canary — GNSS dual-tube saddle clamp (NARROW variant).

Like gnss_saddle, but Y (across-tubes) is only 60 mm and the center bolt
through-hole is removed. Tube centers stay at Y = ±30.09 mm (outboard of
the block edges at Y = ±30), so each saddle half only scoops a QUARTER of
each tube (90° wrap per piece, 180° total wrap with the two stacked halves).
Use two narrow saddles back-to-back on each tube pair for a full clamp, or
use as a partial-engagement support.

Coordinate frame:
  X = along tube axis
  Y = across tubes
  Z = build direction (split plane at Z = HALF_HT)

Outputs:
  gnss_saddle_narrow_half.stl   (print 2 copies, mirror-identical)
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

TUBE_OD         = 15.39      # mm
TUBE_CENTER_SEP = 60.17      # mm, center-to-center across Y
CLEARANCE       = 0.4

BLOCK_LEN = 50.0             # X, tube-axis grip length
BLOCK_WID = 60.0             # Y, across tubes (TUBE_CENTER_SEP - small inset)
BLOCK_HT  = 28.0             # Z, total assembled height

# 4× M4 clamp bolts; inboard of the tube centers
BOLT_X_OFFSET = 18.0
BOLT_Y_OFFSET = 18.0
SCREW_CLEAR_D    = 4.4
SCREW_HEAD_D     = 8.0
SCREW_HEAD_DEPTH = 4.5

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived
# =============================================================================

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
TUBE_Y  = TUBE_CENTER_SEP / 2

# Sanity checks (relaxed: tubes are outboard of block, intentional quarter wrap)
assert R_IN + 2.0 <= HALF_HT, "Half-height too small for tube bore radius + wall"
_bolt_to_tube_xy = TUBE_Y - BOLT_Y_OFFSET
assert _bolt_to_tube_xy > R_IN + SCREW_CLEAR_D / 2 + 1.0, \
    "Bolt clearance hole clashes with tube bore"

# =============================================================================
# Build one half
# =============================================================================

def build_half() -> Part:
    block = Box(BLOCK_LEN, BLOCK_WID, HALF_HT,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Tube scoops — full cylinders centered at the split plane, at Y=±TUBE_Y.
    # Because |TUBE_Y| > BLOCK_WID/2, only a quarter of each cylinder lies
    # inside the block, producing a 90° corner scoop on each long edge.
    for sy in (-1, 1):
        bore = Cylinder(R_IN, BLOCK_LEN + 0.2,
                        rotation=(0, 90, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        bore = Pos(0.0, sy * TUBE_Y, HALF_HT) * bore
        block -= bore

    # 4× M4 clamp-bolt through-holes + outer-face counterbore
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = sx * BOLT_X_OFFSET
            cy = sy * BOLT_Y_OFFSET
            thru = Cylinder(SCREW_CLEAR_D / 2, HALF_HT + 0.4,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            thru = Pos(cx, cy, -0.2) * thru
            block -= thru
            head = Cylinder(SCREW_HEAD_D / 2, SCREW_HEAD_DEPTH + 0.1,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            head = Pos(cx, cy, -0.05) * head
            block -= head

    return block


def main() -> None:
    print("=" * 60)
    print("CyberWing GNSS narrow saddle (quarter-wrap) — build123d")
    print("=" * 60)
    print(f"Block:    {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT} mm assembled")
    print(f"Tubes:    Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f} "
          f"(center-to-center {TUBE_CENTER_SEP})")
    print(f"Bore ID:  Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"Wrap:     ~90° per half (tube center outboard of block edge)")
    print(f"Bolts:    4× M4 at (±{BOLT_X_OFFSET}, ±{BOLT_Y_OFFSET})")

    half = build_half()
    out = OUT_DIR / "gnss_saddle_narrow_half.stl"
    export_stl(half, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)")

    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Print 2 copies per saddle.")
    print("Hardware: 4× M4 × 30 mm socket caps + M4 nuts per saddle.")


if __name__ == "__main__":
    main()
