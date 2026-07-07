"""
CyberWing Canary — GNSS dual-tube saddle (NARROW variant) + Ø16 GNSS bolt hole.

Identical to make_gnss_saddle_narrow.py (quarter-wrap, 50×60×28 block, tubes
Ø15.39 at Y=±30.09, 4× M4 clamp bolts at ±18/±18) but with a centered Ø16 mm
through-bore for the GNSS bolt — matching saddle_preview_gnss16.html.

Coordinate frame:
  X = along tube axis
  Y = across tubes
  Z = build direction (split plane at Z = HALF_HT)

Outputs:
  gnss_saddle_narrow_gnss16_half.stl   (print 2 copies, mirror-identical)
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
BLOCK_WID = 60.0             # Y, across tubes
BLOCK_HT  = 28.0             # Z, total assembled height

# 4× M4 clamp bolts; inboard of the tube centers
BOLT_X_OFFSET = 18.0
BOLT_Y_OFFSET = 18.0
SCREW_CLEAR_D    = 4.4
SCREW_HEAD_D     = 8.0
SCREW_HEAD_DEPTH = 4.5

# Centered GNSS bolt through-hole
GNSS_BOLT_D = 16.0

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived
# =============================================================================

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
TUBE_Y  = TUBE_CENTER_SEP / 2
GNSS_R  = GNSS_BOLT_D / 2

# Sanity checks
assert R_IN + 2.0 <= HALF_HT, "Half-height too small for tube bore radius + wall"
_bolt_to_tube_xy = TUBE_Y - BOLT_Y_OFFSET
assert _bolt_to_tube_xy > R_IN + SCREW_CLEAR_D / 2 + 1.0, \
    "Bolt clearance hole clashes with tube bore"
# Ø16 hole clears the M4 clamp bolts (nearest at radius sqrt(18^2+18^2)=25.46)
import math
_gnss_to_bolt = math.hypot(BOLT_X_OFFSET, BOLT_Y_OFFSET) - GNSS_R - SCREW_CLEAR_D / 2
assert _gnss_to_bolt > 1.0, "Ø16 GNSS hole clashes with an M4 clamp bolt"
# Ø16 hole clears the tube bores (nearest tube inner edge at TUBE_Y - R_IN)
_gnss_to_tube = (TUBE_Y - R_IN) - GNSS_R
assert _gnss_to_tube > 1.0, "Ø16 GNSS hole clashes with a tube bore"

# =============================================================================
# Build one half
# =============================================================================

def build_half() -> Part:
    block = Box(BLOCK_LEN, BLOCK_WID, HALF_HT,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Tube scoops — quarter-wrap (tube centers outboard of block edges)
    for sy in (-1, 1):
        bore = Cylinder(R_IN, BLOCK_LEN + 0.2,
                        rotation=(0, 90, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        bore = Pos(0.0, sy * TUBE_Y, HALF_HT) * bore
        block -= bore

    # Centered Ø16 GNSS bolt through-hole
    block -= Pos(0.0, 0.0, -0.2) * Cylinder(GNSS_R, HALF_HT + 0.4,
                                            align=(Align.CENTER, Align.CENTER, Align.MIN))

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
    print("CyberWing GNSS narrow saddle + Ø16 GNSS bolt — build123d")
    print("=" * 60)
    print(f"Block:    {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT} mm assembled")
    print(f"Tubes:    Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f} "
          f"(center-to-center {TUBE_CENTER_SEP})")
    print(f"GNSS hole: Ø{GNSS_BOLT_D} centered through-bore")
    print(f"  clear of M4 clamps by {_gnss_to_bolt:.2f} mm, tubes by {_gnss_to_tube:.2f} mm")
    print(f"Bolts:    4× M4 at (±{BOLT_X_OFFSET}, ±{BOLT_Y_OFFSET})")

    half = build_half()
    out = OUT_DIR / "gnss_saddle_narrow_gnss16_half.stl"
    export_stl(half, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)")

    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Print 2 copies per saddle.")
    print("Hardware: 4× M4 × 30 mm socket caps + M4 nuts per saddle.")


if __name__ == "__main__":
    main()
