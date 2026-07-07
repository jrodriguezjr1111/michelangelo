"""
CyberWing — wide GNSS dual-tube saddle clamp (no center hole).

Same dual-tube clamp as the original GNSS saddle, but widened in Y
(across tubes) to 197 mm to host a larger payload on the top surface.
The center vertical through-hole is removed.

Geometry:
  Two halves split along Z=HALF_HT. Each half has:
    - two half-cylinder tube scoops on its split face
    - 4× M4 clamp bolt holes with head/nut counterbore on the outer face

Coordinate frame (model == print orientation):
  X = along tube axis (BLOCK_LEN, 50 mm grip length)
  Y = across tubes   (BLOCK_WID, 197 mm)
  Z = build direction. z=0 = BED (outer face), z=HALF_HT = SPLIT face (up).

Outputs:
  gnss_saddle_wide_half.stl  (print 2 copies, mirror-identical)
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

# Tubes (same as GNSS saddle)
TUBE_OD         = 15.39
TUBE_CENTER_SEP = 60.17
CLEARANCE       = 0.4

# Block (assembled, both halves combined)
BLOCK_LEN = 50.0             # X, along tube axis — same as original GNSS
BLOCK_WID = 197.0            # Y, across tubes — widened
BLOCK_HT  = 28.0             # Z, total height assembled

# Clamp bolts (M4 stainless socket cap, 4× inboard of tubes)
BOLT_X_OFFSET = 18.0         # ±X from center (along tube axis)
BOLT_Y_OFFSET = 18.0         # ±Y from center (between tubes, inboard)
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

# Sanity checks
assert TUBE_Y + R_IN + 3.0 <= BLOCK_WID / 2, \
    f"Block too narrow ({BLOCK_WID} mm) for tube centers ±{TUBE_Y} + bore {R_IN:.2f}"
assert R_IN + 2.0 <= HALF_HT, \
    "Half-height must clear tube bore radius + wall"
assert BOLT_X_OFFSET + SCREW_HEAD_D / 2 + 1.0 < BLOCK_LEN / 2, \
    "Clamp bolt heads exit the block in X"
assert abs(BOLT_Y_OFFSET) + SCREW_CLEAR_D / 2 + 1.0 < TUBE_Y - R_IN, \
    "Clamp bolts clash with tube bores (move BOLT_Y_OFFSET inboard)"


# =============================================================================
# Build one half (both halves identical — print twice)
# =============================================================================

def build_half() -> Part:
    block = Box(BLOCK_LEN, BLOCK_WID, HALF_HT,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Two tube half-bores scooped from the split face (z=HALF_HT)
    for sy in (-1, 1):
        bore = Cylinder(R_IN, BLOCK_LEN + 0.2,
                        rotation=(0, 90, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        bore = Pos(0.0, sy * TUBE_Y, HALF_HT) * bore
        block -= bore

    # 4× clamp-bolt through-holes + outer-face counterbore
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


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("CyberWing wide GNSS dual-tube saddle — build123d generator")
    print("=" * 60)
    print(f"Block:          {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT} mm assembled")
    print(f"Tubes:          Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f} "
          f"(center-to-center {TUBE_CENTER_SEP} mm)")
    print(f"Bore ID:        Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"Clamp bolts:    4× M4 at (±{BOLT_X_OFFSET}, ±{BOLT_Y_OFFSET})")
    print(f"Center hole:    NONE (removed vs original GNSS)")
    print()

    half = build_half()
    out = OUT_DIR / "gnss_saddle_wide_half.stl"
    export_stl(half, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)")

    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Print 2 copies. Assemble with 4× M4 × 30 mm socket caps + M4 nuts.")
    print("Hardware BOM:")
    print("  - 4× M4 × 30 mm socket-cap screws (stainless)")
    print("  - 4× M4 nuts (standard, fits Ø8 counterbore)")
    print("  - 4× M4 washers (optional)")


if __name__ == "__main__":
    main()
