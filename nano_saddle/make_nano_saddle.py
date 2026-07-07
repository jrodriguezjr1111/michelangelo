"""
CyberWing — dual Jetson Nano saddle clamp.

Same dual-tube clamp concept as the GNSS saddle, but resized to host two
Jetson Nano dev kits side-by-side on its top surface. Print-orientation,
split, and bolt scheme are identical to the GNSS variant.

Geometry:
  Two halves split along Z=HALF_HT. Each half has:
    - two half-cylinder tube scoops on its split face
    - 4× M4 clamp bolt holes with head/nut counterbore on the outer face

Coordinate frame (model == print orientation):
  X = along tube axis (BLOCK_LEN, 70 mm grip length)
  Y = across tubes   (BLOCK_WID, 197 mm — fits two Nanos along Y)
  Z = build direction. z=0 = BED (outer face), z=HALF_HT = SPLIT face (up).

Outputs:
  nano_saddle_half.stl  (plain — print this for the BOTTOM half)
  nano_saddle_top.stl   (adds 4× M3 mount holes per Jetson on the outer face —
                         Jetson Nano on −Y side, Jetson Nano Orin on +Y side)
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
BLOCK_LEN = 70.0             # X, along tube axis — grip length
BLOCK_WID = 197.0            # Y, across tubes — fits two Nanos side-by-side
BLOCK_HT  = 28.0             # Z, total height assembled

# Clamp bolts (M4 stainless socket cap) — inboard row only, between tubes
BOLT_X_OFFSET   = 25.0       # ±X from center (along tube axis)
BOLT_Y_INBOARD  = 18.0       # ±Y between tubes (inboard of ±TUBE_Y)
SCREW_CLEAR_D    = 4.4
SCREW_HEAD_D     = 8.0
SCREW_HEAD_DEPTH = 4.5

# Jetson mount holes (M3) — placed on the outer face of the TOP half only.
# Each board's hole pattern is rectangular; the long pattern dim is along Y
# (across tubes) so the boards sit lengthwise on the saddle.
#   Jetson Nano dev kit:        86.14 (Y) × 58.25 (X)
#   Jetson Nano Orin dev kit:   92.12 (Y) × 57.59 (X)
NANO_PATTERN_Y = 86.14
NANO_PATTERN_X = 58.25
ORIN_PATTERN_Y = 92.12
ORIN_PATTERN_X = 57.59
M3_CLEAR_D       = 3.4
M3_HEAD_D        = 5.34   # screw-head Ø (counterbore on outer face)
M3_HEAD_DEPTH    = 2.94   # counterbore depth

# Board center offsets in Y. Orin sits at +Y (outer edge clearance ~3.2 mm).
# Nano is pushed toward the −Y edge to match that same outer margin.
ORIN_Y_CENTER =  BLOCK_WID / 4                                  # +49.25
NANO_Y_CENTER = -(BLOCK_WID / 2 - NANO_PATTERN_Y / 2 - 3.19)    # −Y side, ~3.19 mm edge

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
assert BOLT_Y_INBOARD + SCREW_CLEAR_D / 2 + 1.0 < TUBE_Y - R_IN, \
    "Inboard clamp bolts clash with tube bores (decrease BOLT_Y_INBOARD)"

# Jetson mount-hole sanity (X-edge, Y-edge, and clearance vs clamp bolts)
def _check_pattern(name, py, px, ycen):
    assert px / 2 + M3_CLEAR_D / 2 + 1.0 < BLOCK_LEN / 2 and \
           px / 2 + M3_HEAD_D / 2 + 0.4 < BLOCK_LEN / 2, \
        f"{name} mount holes exit block in X"
    y_hi = abs(ycen) + py / 2
    assert y_hi + M3_CLEAR_D / 2 + 1.0 < BLOCK_WID / 2 and \
           y_hi + M3_HEAD_D / 2 + 0.4 < BLOCK_WID / 2, \
        f"{name} mount holes exit block in Y (extreme Y={y_hi:.2f}, head wall {(BLOCK_WID/2 - y_hi - M3_HEAD_D/2):.2f} mm)"
    assert M3_HEAD_DEPTH + 1.0 < HALF_HT, \
        f"M3 head counterbore ({M3_HEAD_DEPTH} mm) too deep for half height ({HALF_HT} mm)"
    # vs clamp bolts: any (±BOLT_X_OFFSET, ±BOLT_Y_INBOARD/OUTBOARD)
    for bx in (-BOLT_X_OFFSET, BOLT_X_OFFSET):
        for by in (-BOLT_Y_INBOARD, BOLT_Y_INBOARD):
            for sx in (-1, 1):
                for sy in (-1, 1):
                    mx = sx * px / 2
                    my = ycen + sy * py / 2
                    d = ((mx - bx) ** 2 + (my - by) ** 2) ** 0.5
                    gap = d - M3_HEAD_D / 2 - SCREW_HEAD_D / 2
                    assert gap > 0.5, \
                        (f"{name} hole at ({mx:.1f},{my:.1f}) too close to "
                         f"clamp bolt head at ({bx},{by}) (gap {gap:.2f} mm)")

_check_pattern("Nano", NANO_PATTERN_Y, NANO_PATTERN_X, NANO_Y_CENTER)
_check_pattern("Orin", ORIN_PATTERN_Y, ORIN_PATTERN_X, ORIN_Y_CENTER)


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

    # 4× clamp-bolt through-holes + outer-face counterbore (inboard row only)
    bolt_y_positions = (-BOLT_Y_INBOARD, BOLT_Y_INBOARD)
    for sx in (-1, 1):
        for cy in bolt_y_positions:
            cx = sx * BOLT_X_OFFSET
            thru = Cylinder(SCREW_CLEAR_D / 2, HALF_HT + 0.4,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            block -= Pos(cx, cy, -0.2) * thru
            head = Cylinder(SCREW_HEAD_D / 2, SCREW_HEAD_DEPTH + 0.1,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            block -= Pos(cx, cy, -0.05) * head

    return block


def build_top() -> Part:
    """Top half: same as build_half() plus 4× M3 holes per Jetson on the
    outer face (which is on the bed during printing and faces UP after
    assembly, since the upper half is flipped onto the lower one)."""
    block = build_half()

    patterns = [
        ("Nano", NANO_PATTERN_Y, NANO_PATTERN_X, NANO_Y_CENTER),
        ("Orin", ORIN_PATTERN_Y, ORIN_PATTERN_X, ORIN_Y_CENTER),
    ]
    for _name, py, px, ycen in patterns:
        for sx in (-1, 1):
            for sy in (-1, 1):
                cx = sx * px / 2
                cy = ycen + sy * py / 2
                thru = Cylinder(M3_CLEAR_D / 2, HALF_HT + 0.4,
                                align=(Align.CENTER, Align.CENTER, Align.MIN))
                block -= Pos(cx, cy, -0.2) * thru
                # Screw-head counterbore on inner (split) face (z = HALF_HT),
                # cut downward into the half so heads recess away from outer face
                head = Cylinder(M3_HEAD_D / 2, M3_HEAD_DEPTH + 0.1,
                                align=(Align.CENTER, Align.CENTER, Align.MAX))
                block -= Pos(cx, cy, HALF_HT + 0.05) * head

    return block


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("CyberWing dual-Jetson-Nano saddle — build123d generator")
    print("=" * 60)
    print(f"Block:          {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT} mm assembled")
    print(f"Tubes:          Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f} "
          f"(center-to-center {TUBE_CENTER_SEP} mm)")
    print(f"Bore ID:        Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"Clamp bolts:    4× M4 at (±{BOLT_X_OFFSET}, ±{BOLT_Y_INBOARD}) inboard")
    print(f"Nano mounts:    4× Ø{M3_CLEAR_D} at (±{NANO_PATTERN_X/2:.2f}, "
          f"{NANO_Y_CENTER:+.2f}±{NANO_PATTERN_Y/2:.2f})  [−Y side]")
    print(f"Orin mounts:    4× Ø{M3_CLEAR_D} at (±{ORIN_PATTERN_X/2:.2f}, "
          f"{ORIN_Y_CENTER:+.2f}±{ORIN_PATTERN_Y/2:.2f})  [+Y side]")
    print(f"M3 head c'bore: Ø{M3_HEAD_D} × {M3_HEAD_DEPTH} mm deep on inner (split) face")
    print()

    bot = build_half()
    out_bot = OUT_DIR / "nano_saddle_half.stl"
    export_stl(bot, str(out_bot))
    print(f"  ✓ {out_bot.name} ({out_bot.stat().st_size:,} bytes)  — bottom half (plain)")

    top = build_top()
    out_top = OUT_DIR / "nano_saddle_top.stl"
    export_stl(top, str(out_top))
    print(f"  ✓ {out_top.name} ({out_top.stat().st_size:,} bytes)  — top half (with Jetson mount holes)")

    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Print 1× of each half. Assemble with 4× M4 × 30 mm socket caps + M4 nuts.")
    print("Hardware BOM:")
    print("  - 4× M4 × 30 mm socket-cap screws (stainless)")
    print("  - 4× M4 nuts (standard, fits Ø8 counterbore)")
    print("  - 4× M4 washers (optional)")
    print("  - 8× M3 screws + standoffs (4 per Jetson) for top mount")


if __name__ == "__main__":
    main()
