"""
CyberWing Canary — GNSS dual-tube saddle clamp.

Clamps onto TWO parallel cylinders (e.g., a horizontal support frame) with a
central through-hole for the GNSS antenna mount bolt.

Geometry:
  Two rectangular blocks split along Z=HALF_HT.  Each half is identical (print
  two copies).  Each half has:
    - two half-cylinder scoops on its split face (one per tube)
    - a full Ø GNSS_HOLE_D through-hole on the Z axis (for the antenna bolt)
    - 4× M4 clamp bolt holes with head/nut counterbore on the outer face

Coordinate frame (model == print orientation):
  X = along tube axis (tubes run parallel in +X / -X)
  Y = across tubes (tube centers at Y = ±TUBE_CENTER_SEP/2)
  Z = build direction.  z=0 = BED (outer face), z=HALF_HT = SPLIT face (up).

Printability: tube scoops open UPWARD at the split face (no overhang); the
GNSS through-hole is a vertical cylinder (no overhang).  No supports needed.

Outputs:
  gnss_saddle_half.stl    (print 2 copies, mirror-identical)
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

# Tubes (MEASURE WITH CALIPERS)
TUBE_OD         = 15.39      # mm, both tubes
TUBE_CENTER_SEP = 60.17      # mm, center-to-center across Y
CLEARANCE       = 0.4        # total diametral clearance

# GNSS antenna bolt through-hole (centered on block)
GNSS_HOLE_D     = 30.0       # Ø, goes fully through both halves

# Block (assembled, both halves combined)
BLOCK_LEN = 50.0             # X, along tube axis — clamp grip length
BLOCK_WID = 101.54           # Y — widened from 90 to match make_gnss_saddle_nano.py
                             #     so the two sit flush on the same rail
BLOCK_HT  = 28.0             # Z, total height assembled

# Clamp bolts (M4 stainless socket cap, 4× at corners of a rectangle between
# tubes and inboard of each tube end)
BOLT_X_OFFSET = 18.0         # ±X from center (along tube axis)
BOLT_Y_OFFSET = 18.0         # ±Y from center (between tubes, inboard)
SCREW_CLEAR_D  = 4.4
SCREW_HEAD_D   = 8.0
SCREW_HEAD_DEPTH = 4.5       # counterbore depth on outer face (fits M4 cap head or M4 nut)

OUT_DIR = Path(__file__).parent


# =============================================================================
# Derived
# =============================================================================

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
TUBE_Y  = TUBE_CENTER_SEP / 2      # ± this
GNSS_R  = GNSS_HOLE_D / 2

# Sanity checks
assert TUBE_Y + R_IN + 3.0 <= BLOCK_WID / 2, \
    f"Block too narrow ({BLOCK_WID} mm) for tube centers ±{TUBE_Y} + bore {R_IN:.2f}"
assert R_IN + 2.0 <= HALF_HT, \
    "Half-height must clear tube bore radius + wall"
assert GNSS_R + 2.0 < BOLT_X_OFFSET, \
    "GNSS hole too close to clamp bolts in X"
assert abs(BOLT_Y_OFFSET) + SCREW_CLEAR_D / 2 + 1.0 < TUBE_Y - R_IN, \
    "Clamp bolts clash with tube bores (move BOLT_Y_OFFSET inboard)"
assert GNSS_R + SCREW_CLEAR_D / 2 + 1.0 < (BOLT_X_OFFSET**2 + BOLT_Y_OFFSET**2)**0.5, \
    "GNSS hole too close to a clamp bolt (diagonal clearance)"


# =============================================================================
# Build one half (both halves are identical — print twice)
# =============================================================================

def build_half() -> Part:
    block = Box(BLOCK_LEN, BLOCK_WID, HALF_HT,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # --- Two tube half-bores scooped from split face (z=HALF_HT) ---
    # A full cylinder centered at the split plane; the part above Z=HALF_HT is
    # outside the block so we get a clean half-cylinder scoop.
    for sy in (-1, 1):
        bore = Cylinder(R_IN, BLOCK_LEN + 0.2,
                        rotation=(0, 90, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        bore = Pos(0.0, sy * TUBE_Y, HALF_HT) * bore
        block -= bore

    # --- GNSS center through-hole (Z axis) ---
    gnss = Cylinder(GNSS_R, HALF_HT + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
    gnss = Pos(0.0, 0.0, -0.2) * gnss
    block -= gnss

    # --- 4× clamp-bolt through-holes + outer-face counterbore ---
    # Counterbore accepts an M4 socket-cap head on one copy and an M4 nut
    # (across-flats ~7 mm, thickness 3.2 mm) on the other.
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


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("CyberWing GNSS dual-tube saddle — build123d generator")
    print("=" * 60)
    print(f"Block:          {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT} mm assembled")
    print(f"Tubes:          Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f} "
          f"(center-to-center {TUBE_CENTER_SEP} mm)")
    print(f"Bore ID:        Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"GNSS hole:      Ø{GNSS_HOLE_D} through, centered")
    print(f"Clamp bolts:    4× M4 at (±{BOLT_X_OFFSET}, ±{BOLT_Y_OFFSET})")
    print()

    half = build_half()
    out = OUT_DIR / "gnss_saddle_half.stl"
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
