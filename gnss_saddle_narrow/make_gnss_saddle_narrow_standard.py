"""
CyberWing Canary — GNSS narrow saddle, STANDARD-PROFILE variant.

Geometry is identical to `make_gnss_saddle_narrow.py` (50 mm grip length,
±18 bolt pattern, 90° quarter-wrap on dual Ø15.39 tubes at C-C 60.17 mm).
Only difference: the output STL name is distinct so this part is sliced
with the OrcaSlicer default `0.20mm Standard @Qidi XPlus4` process
profile (crosshatch 20% infill) — matching `nano_saddle_top.gcode` and
`gnss_saddle_narrow_nano_half.gcode` — instead of the `--fast` override
(lightning 10%) used for the original `gnss_saddle_narrow_half.gcode`.

Slice with:
    python plus4_print.py slice gnss_saddle_narrow/gnss_saddle_narrow_standard_half.stl
(no `--fast` flag).

Outputs:
  gnss_saddle_narrow_standard_half.stl   (print 2 copies, mirror-identical)
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS  (identical to make_gnss_saddle_narrow.py)
# =============================================================================

TUBE_OD         = 15.39
TUBE_CENTER_SEP = 60.17
CLEARANCE       = 0.4

BLOCK_LEN = 50.0             # X, tube-axis grip length
BLOCK_WID = 60.0             # Y, across tubes
BLOCK_HT  = 28.0             # Z, total assembled height

BOLT_X_OFFSET    = 18.0
BOLT_Y_OFFSET    = 18.0
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

    for sy in (-1, 1):
        bore = Cylinder(R_IN, BLOCK_LEN + 0.2,
                        rotation=(0, 90, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        block -= Pos(0.0, sy * TUBE_Y, HALF_HT) * bore

    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * BOLT_X_OFFSET, sy * BOLT_Y_OFFSET
            thru = Cylinder(SCREW_CLEAR_D / 2, HALF_HT + 0.4,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            block -= Pos(cx, cy, -0.2) * thru
            head = Cylinder(SCREW_HEAD_D / 2, SCREW_HEAD_DEPTH + 0.1,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            block -= Pos(cx, cy, -0.05) * head

    return block


def main() -> None:
    print("=" * 60)
    print("CyberWing GNSS narrow saddle (standard-profile) — build123d")
    print("=" * 60)
    print(f"Block:    {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT} mm assembled")
    print(f"Tubes:    Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f} "
          f"(center-to-center {TUBE_CENTER_SEP})")
    print(f"Bore ID:  Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"Wrap:     ~90° per half (tube center outboard of block edge)")
    print(f"Bolts:    4× M4 at (±{BOLT_X_OFFSET}, ±{BOLT_Y_OFFSET})")

    half = build_half()
    out = OUT_DIR / "gnss_saddle_narrow_standard_half.stl"
    export_stl(half, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)")

    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Print 2 copies per saddle. Slice with default")
    print("  '0.20mm Standard @Qidi XPlus4' profile (crosshatch 20% infill).")
    print("Hardware: 4× M4 × 30 mm socket caps + M4 nuts per saddle.")


if __name__ == "__main__":
    main()
