"""
CyberWing — minimal single Jetson Nano saddle clamp, Ø20 tubes.

Stripped from make_nano_saddle_20mm.py down to the smallest footprint that still
mounts a Jetson Nano:
  KEEP   : Ø20 tube bores, 4× Ø5 assembly holes (Ø9 head c'bore) in the central
           bridge, 4× M3 Jetson Nano mounts (top half outer face).
  REMOVE : Jetson Orin M3 pattern, 4× #8-32 platform holes.
  SIZE   : block trimmed in X and Y to wrap just these features. The +Y side
           (which the Orin used) is trimmed to a wall past the +tube bore, so the
           block is ASYMMETRIC in Y — the Nano cantilevers to −Y where its two
           hole rows clear both tube bores (inner row in the bridge, outer row on
           the far −Y wing).

Coordinate frame (model == print orientation):
  X = along tube axis, Y = across tubes (tubes at Y = ±TUBE_CENTER_SEP/2),
  Z = build. z=0 = BED (outer face), z=HALF_HT = SPLIT face (up).

Output (top half only, per request):
  nano_saddle_nano_top.stl
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

# Tubes
TUBE_OD         = 20.0
TUBE_CENTER_SEP = 60.17
CLEARANCE       = 0.4

# Block
BLOCK_LEN = 99.0            # X, along tube axis (driven by the Ø5 clamp pattern)
BLOCK_HT  = 28.0            # Z, total assembled height

# Ø5 assembly holes (Ø9 head counterbore on the outer face) — clamp the halves.
HOLE5_CLEAR_D    = 5.0
HOLE5_HEAD_D     = 9.0
HOLE5_HEAD_DEPTH = 5.0
HOLE5_PAT_X      = 84.84
HOLE5_PAT_Y      = 17.73

# Jetson Nano mount holes (M3) — top half outer face.
NANO_PATTERN_X = 58.25
NANO_PATTERN_Y = 86.14
M3_CLEAR_D     = 3.4
M3_HEAD_D      = 5.34
M3_HEAD_DEPTH  = 2.94

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived
# =============================================================================

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
TUBE_Y  = TUBE_CENTER_SEP / 2
BRIDGE  = TUBE_Y - R_IN                    # half clear span between bores (19.885)

# Nano placement: inner row in the central bridge, outer row on the far −Y wing.
NANO_INNER_Y  = -9.17                       # inner row Y (clears +bore, in bridge)
NANO_Y_CENTER = NANO_INNER_Y - NANO_PATTERN_Y / 2     # -52.24
NANO_OUTER_Y  = NANO_Y_CENTER - NANO_PATTERN_Y / 2    # -95.31

# Asymmetric block in Y: +Y trimmed to a wall past the +bore; −Y reaches the Nano.
WALL_OUTER = 4.0           # wall past +tube bore (+Y side)
NANO_EDGE  = 1.5           # outer Nano hole head → −Y edge
Y_TOP =  TUBE_Y + R_IN + WALL_OUTER                       # +44.285
Y_BOT =  NANO_OUTER_Y - M3_HEAD_D / 2 - NANO_EDGE         # -99.48
BLOCK_WID   = Y_TOP - Y_BOT                                # 143.77
BLOCK_Y_MID = (Y_TOP + Y_BOT) / 2                          # -27.60

# =============================================================================
# Sanity
# =============================================================================
assert R_IN + 2.0 <= HALF_HT, "Half-height must clear tube bore radius + wall"
assert Y_TOP >= TUBE_Y + R_IN + 2.0, "Not enough +Y wall past tube bore"
assert Y_BOT <= -(TUBE_Y + R_IN), "Block must contain the −Y tube bore"

# Ø5 group lives in the central bridge between the bores.
assert HOLE5_PAT_X / 2 + HOLE5_HEAD_D / 2 + 0.4 < BLOCK_LEN / 2, "Ø5 holes exit block in X"
assert HOLE5_PAT_Y / 2 + HOLE5_CLEAR_D / 2 + 0.5 < BRIDGE, "Ø5 holes clash with tube bores in Y"
assert HOLE5_HEAD_DEPTH + 1.0 < HALF_HT, "Ø5 head counterbore too deep for half"

# Nano holes: X inside block; inner row clears +bore; outer row clears −bore.
assert NANO_PATTERN_X / 2 + M3_HEAD_D / 2 + 0.4 < BLOCK_LEN / 2, "Nano holes exit block in X"
assert abs(NANO_INNER_Y) + M3_HEAD_D / 2 + 0.4 < BRIDGE, "Nano inner row counterbore clashes a bore"
assert NANO_OUTER_Y - M3_HEAD_D / 2 > -(BLOCK_WID + BLOCK_Y_MID) , "Nano outer row exits block"
assert (-(TUBE_Y + R_IN)) - NANO_OUTER_Y > M3_HEAD_D / 2 + 0.4, "Nano outer row clashes the −bore"
assert M3_HEAD_DEPTH + 1.0 < HALF_HT, "M3 head counterbore too deep for half"


# =============================================================================
# Build
# =============================================================================

def build_half() -> Part:
    """Tubes + Ø5 assembly holes — shared by both halves (asymmetric block)."""
    block = Pos(0.0, BLOCK_Y_MID, 0.0) * Box(
        BLOCK_LEN, BLOCK_WID, HALF_HT,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Two tube half-bores scooped from the split face (z=HALF_HT).
    for sy in (-1, 1):
        bore = Cylinder(R_IN, BLOCK_LEN + 0.2,
                        rotation=(0, 90, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        block -= Pos(0.0, sy * TUBE_Y, HALF_HT) * bore

    # 4× Ø5 through-holes + Ø9 head counterbore on the outer face (z=0).
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * HOLE5_PAT_X / 2, sy * HOLE5_PAT_Y / 2
            block -= Pos(cx, cy, -0.2) * Cylinder(
                HOLE5_CLEAR_D / 2, HALF_HT + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            block -= Pos(cx, cy, -0.05) * Cylinder(
                HOLE5_HEAD_D / 2, HOLE5_HEAD_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return block


def build_top() -> Part:
    """Top half = build_half() + 4× Jetson Nano M3 mounts (head c'bore cut from
    the split/inner face)."""
    block = build_half()
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = sx * NANO_PATTERN_X / 2
            cy = NANO_Y_CENTER + sy * NANO_PATTERN_Y / 2
            block -= Pos(cx, cy, -0.2) * Cylinder(
                M3_CLEAR_D / 2, HALF_HT + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            block -= Pos(cx, cy, HALF_HT + 0.05) * Cylinder(
                M3_HEAD_D / 2, M3_HEAD_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MAX))
    return block


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("CyberWing minimal Jetson Nano saddle — Ø20 tubes (top half)")
    print("=" * 60)
    print(f"Block:        {BLOCK_LEN} × {BLOCK_WID:.2f} × {BLOCK_HT} mm "
          f"(asymmetric Y, center {BLOCK_Y_MID:+.2f})")
    print(f"Tubes:        Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f} (sep {TUBE_CENTER_SEP})")
    print(f"Bore ID:      Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"Ø5 clamp:     4× Ø{HOLE5_CLEAR_D} at (±{HOLE5_PAT_X/2:.2f}, ±{HOLE5_PAT_Y/2:.2f}), "
          f"Ø{HOLE5_HEAD_D}×{HOLE5_HEAD_DEPTH} head c'bore (outer face)")
    print(f"Nano mounts:  4× Ø{M3_CLEAR_D} at (±{NANO_PATTERN_X/2:.2f}, "
          f"{NANO_Y_CENTER:+.2f}±{NANO_PATTERN_Y/2:.2f}) — rows at Y={NANO_INNER_Y:.2f}, {NANO_OUTER_Y:.2f}")
    print()

    top = build_top()
    out = OUT_DIR / "nano_saddle_nano_top.stl"
    export_stl(top, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)  — top half (Jetson Nano mounts)")
    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Assembly bolts use the Ø5 (Ø9 head) holes.")


if __name__ == "__main__":
    main()
