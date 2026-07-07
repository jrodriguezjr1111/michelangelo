"""
CyberWing Canary — GNSS saddle, NANO-MATCHED, Y-WIDE variant.

Same X (tube-axis) length and bolt pattern as `make_gnss_saddle_narrow_nano.py`,
but the plate is extended along Y to 197 mm so it can serve as a wide
mounting platform spanning beyond the dual-tube grip.

GEOMETRY NOTE — this is NOT a quarter-wrap clamp:
  Because BLOCK_WID (197) ≫ 2·(TUBE_Y + R_IN) ≈ 76, the tube centers
  (Y = ±30.09) sit well inside the block. Each tube becomes a full
  cylindrical tunnel through the block, and each printed half wraps
  180° around the tubes (full enclosure in assembly). Tubes must be
  inserted axially.

  If quarter-wrap behaviour is required, keep BLOCK_WID = 60.

Layout:
  X = along tube axis (70 mm grip, matches nano_saddle)
  Y = across tubes (197 mm wing-to-wing)
  Z = build direction (split plane at Z = HALF_HT)

Outputs:
  gnss_saddle_narrow_nano_wide_half.stl   (print 2 copies, mirror-identical)
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

TUBE_OD         = 15.39
TUBE_CENTER_SEP = 60.17
CLEARANCE       = 0.4

BLOCK_LEN = 70.0             # X — matches nano_saddle BLOCK_LEN
BLOCK_WID = 197.0            # Y — extended wing-to-wing
BLOCK_HT  = 28.0             # Z — matches nano_saddle BLOCK_HT

# 4× M4 clamp bolts — pattern matches nano_saddle inboard row
BOLT_X_OFFSET    = 25.0
BOLT_Y_OFFSET    = 18.0
SCREW_CLEAR_D    = 4.4
SCREW_HEAD_D     = 8.0
SCREW_HEAD_DEPTH = 4.5

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived + sanity
# =============================================================================

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
TUBE_Y  = TUBE_CENTER_SEP / 2

assert R_IN + 2.0 <= HALF_HT, "Half-height too small for tube bore radius + wall"
assert BOLT_X_OFFSET + SCREW_HEAD_D / 2 + 1.0 < BLOCK_LEN / 2, \
    "Clamp bolt heads exit the block in X"
_bolt_to_tube_xy = TUBE_Y - BOLT_Y_OFFSET
assert _bolt_to_tube_xy > R_IN + SCREW_CLEAR_D / 2 + 1.0, \
    "Bolt clearance hole clashes with tube bore"
assert TUBE_Y + R_IN < BLOCK_WID / 2 - 1.0, \
    "Tube tunnel exits the block in Y (this script assumes full enclosure)"

# =============================================================================
# Build one half
# =============================================================================

def build_half() -> Part:
    block = Box(BLOCK_LEN, BLOCK_WID, HALF_HT,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Tube tunnels — full cylinders along X at Y = ±TUBE_Y, Z = HALF_HT.
    # With wide BLOCK_WID, the tubes are fully enclosed (180° per half).
    for sy in (-1, 1):
        bore = Cylinder(R_IN, BLOCK_LEN + 0.2,
                        rotation=(0, 90, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        block -= Pos(0.0, sy * TUBE_Y, HALF_HT) * bore

    # 4× M4 clamp-bolt through-holes + outer-face counterbore
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * BOLT_X_OFFSET, sy * BOLT_Y_OFFSET
            block -= Pos(cx, cy, -0.2) * Cylinder(
                SCREW_CLEAR_D / 2, HALF_HT + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            block -= Pos(cx, cy, -0.05) * Cylinder(
                SCREW_HEAD_D / 2, SCREW_HEAD_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return block


def main() -> None:
    print("=" * 64)
    print("CyberWing GNSS saddle (nano-matched, Y-wide 197 mm) — build123d")
    print("=" * 64)
    print(f"Block:    {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT} mm assembled")
    print(f"Tubes:    Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f} "
          f"(center-to-center {TUBE_CENTER_SEP})")
    print(f"Bore ID:  Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"Wrap:     180° per half — full tube enclosure (axial insert)")
    print(f"Bolts:    4× M4 at (±{BOLT_X_OFFSET}, ±{BOLT_Y_OFFSET})  "
          f"— matches nano_saddle pattern")
    print(f"+Y wing:  {BLOCK_WID/2 - (TUBE_Y + R_IN):.2f} mm beyond tube tunnel")
    print(f"Bridge:   {2 * (TUBE_Y - R_IN):.2f} mm clear span between tubes")

    half = build_half()
    out = OUT_DIR / "gnss_saddle_narrow_nano_wide_half.stl"
    export_stl(half, str(out))
    print(f"\n  ✓ {out.name} ({out.stat().st_size:,} bytes)")
    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Print 2 copies per saddle.")
    print("Hardware: 4× M4 × 30 mm socket caps + M4 nuts per saddle.")


if __name__ == "__main__":
    main()
