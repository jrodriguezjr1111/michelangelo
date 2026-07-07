"""
CyberWing — dual Jetson Nano saddle clamp, Ø20 / 101 mm-X variant.

Derived from `make_nano_saddle.py` with these changes:
  - Tube OD 15.39 → 20.0 mm
  - X-axis grip length (BLOCK_LEN) 70 → 101 mm
  - M4 clamp bolts REMOVED
  - Jetson Nano / Orin M3 mount patterns KEPT (top half, outer face)
  - Added 4× Ø5 clearance holes (Ø9 head counterbore on outer face)
        pattern 84.84 (X) × 17.73 (Y), in the central bridge between tubes
  - Added 4× #8-32 clearance holes (Ø4.4)
        pattern 51.83 (X) × 120.18 (Y)
  The Ø5 + #8-32 holes go through BOTH halves (assembly / platform mount).

Coordinate frame (model == print orientation):
  X = along tube axis (BLOCK_LEN, 101 mm)
  Y = across tubes   (BLOCK_WID, 197 mm)
  Z = build direction. z=0 = BED (outer face), z=HALF_HT = SPLIT face (up).

Outputs:
  nano_saddle_20mm_half.stl  (bottom half — tubes + Ø5 + #8-32)
  nano_saddle_20mm_top.stl   (top half — adds Jetson M3 mounts)
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

# Tubes
TUBE_OD         = 20.0       # ← was 15.39
TUBE_CENTER_SEP = 60.17
CLEARANCE       = 0.4

# Block (assembled, both halves combined)
BLOCK_LEN = 101.0            # X, along tube axis  ← was 70.0
BLOCK_WID = 197.0            # Y, across tubes
BLOCK_HT  = 28.0             # Z, total assembled height

# --- New hole group A: 4× Ø5 clearance + Ø9 head counterbore (outer face) ---
HOLE5_CLEAR_D    = 5.0
HOLE5_HEAD_D     = 9.0       # "9 mm space for the screw head"
HOLE5_HEAD_DEPTH = 5.0
HOLE5_PAT_X      = 84.84     # X spacing
HOLE5_PAT_Y      = 17.73     # Y spacing

# --- New hole group B: 4× #8-32 clearance ---
N8_CLEAR_D = 4.4             # #8-32 clearance (close fit)
N8_PAT_X   = 51.83           # X spacing
N8_PAT_Y   = 120.18          # Y spacing

# Jetson mount holes (M3) — top half outer face (unchanged geometry).
NANO_PATTERN_Y = 86.14
NANO_PATTERN_X = 58.25
ORIN_PATTERN_Y = 92.12
ORIN_PATTERN_X = 57.59
M3_CLEAR_D     = 3.4
M3_HEAD_D      = 5.34
M3_HEAD_DEPTH  = 2.94

ORIN_Y_CENTER =  BLOCK_WID / 4                                  # +49.25
NANO_Y_CENTER = -(BLOCK_WID / 2 - NANO_PATTERN_Y / 2 - 3.19)    # −Y side

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived
# =============================================================================

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
TUBE_Y  = TUBE_CENTER_SEP / 2
BRIDGE  = TUBE_Y - R_IN      # half clear span between the two bores

# =============================================================================
# Sanity
# =============================================================================
assert TUBE_Y + R_IN + 3.0 <= BLOCK_WID / 2, "Block too narrow for tubes + wall"
assert R_IN + 2.0 <= HALF_HT, "Half-height must clear tube bore radius + wall"

# Ø5 group — lives in the central bridge between the two bores.
assert HOLE5_PAT_X / 2 + HOLE5_HEAD_D / 2 + 0.4 < BLOCK_LEN / 2, "Ø5 holes exit block in X"
assert HOLE5_PAT_Y / 2 + HOLE5_CLEAR_D / 2 + 0.5 < BRIDGE, \
    f"Ø5 holes clash with tube bores in Y (bridge half-span {BRIDGE:.2f} mm)"
assert HOLE5_HEAD_DEPTH + 1.0 < HALF_HT, "Ø5 head counterbore too deep for half"

# #8-32 group — on the +Y/−Y wings, outboard of the bores.
assert N8_PAT_X / 2 + N8_CLEAR_D / 2 + 0.5 < BLOCK_LEN / 2, "#8-32 holes exit block in X"
assert N8_PAT_Y / 2 + N8_CLEAR_D / 2 + 0.5 < BLOCK_WID / 2, "#8-32 holes exit block in Y"
assert N8_PAT_Y / 2 - N8_CLEAR_D / 2 > TUBE_Y + R_IN, "#8-32 holes clash with tube bores"


def _check_pattern(name, py, px, ycen):
    assert px / 2 + M3_HEAD_D / 2 + 0.4 < BLOCK_LEN / 2, f"{name} mount holes exit block in X"
    y_hi = abs(ycen) + py / 2
    assert y_hi + M3_HEAD_D / 2 + 0.4 < BLOCK_WID / 2, f"{name} mount holes exit block in Y"
    assert M3_HEAD_DEPTH + 1.0 < HALF_HT, "M3 head counterbore too deep for half"


_check_pattern("Nano", NANO_PATTERN_Y, NANO_PATTERN_X, NANO_Y_CENTER)
_check_pattern("Orin", ORIN_PATTERN_Y, ORIN_PATTERN_X, ORIN_Y_CENTER)


# =============================================================================
# Build one half (tubes + new through-hole groups; both halves share these)
# =============================================================================

def build_half() -> Part:
    block = Box(BLOCK_LEN, BLOCK_WID, HALF_HT,
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

    # 4× #8-32 through-holes (plain clearance).
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * N8_PAT_X / 2, sy * N8_PAT_Y / 2
            block -= Pos(cx, cy, -0.2) * Cylinder(
                N8_CLEAR_D / 2, HALF_HT + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return block


def build_top() -> Part:
    """Top half: build_half() plus 4× M3 mount holes per Jetson on the
    outer face, with head counterbores cut from the inner (split) face."""
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
    print("CyberWing dual-Jetson saddle — Ø20 / 101 mm-X variant")
    print("=" * 60)
    print(f"Block:        {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT} mm assembled")
    print(f"Tubes:        Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f} (sep {TUBE_CENTER_SEP})")
    print(f"Bore ID:      Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"Bridge span:  {2 * BRIDGE:.2f} mm clear between bores")
    print(f"Ø5 holes:     4× Ø{HOLE5_CLEAR_D} at (±{HOLE5_PAT_X/2:.2f}, ±{HOLE5_PAT_Y/2:.2f}), "
          f"Ø{HOLE5_HEAD_D}×{HOLE5_HEAD_DEPTH} head c'bore (outer face)")
    print(f"#8-32 holes:  4× Ø{N8_CLEAR_D} at (±{N8_PAT_X/2:.2f}, ±{N8_PAT_Y/2:.2f})")
    print(f"Nano mounts:  4× Ø{M3_CLEAR_D} at (±{NANO_PATTERN_X/2:.2f}, "
          f"{NANO_Y_CENTER:+.2f}±{NANO_PATTERN_Y/2:.2f})  [−Y]")
    print(f"Orin mounts:  4× Ø{M3_CLEAR_D} at (±{ORIN_PATTERN_X/2:.2f}, "
          f"{ORIN_Y_CENTER:+.2f}±{ORIN_PATTERN_Y/2:.2f})  [+Y]")
    print()

    bot = build_half()
    out_bot = OUT_DIR / "nano_saddle_20mm_half.stl"
    export_stl(bot, str(out_bot))
    print(f"  ✓ {out_bot.name} ({out_bot.stat().st_size:,} bytes)  — bottom half")

    top = build_top()
    out_top = OUT_DIR / "nano_saddle_20mm_top.stl"
    export_stl(top, str(out_top))
    print(f"  ✓ {out_top.name} ({out_top.stat().st_size:,} bytes)  — top half (Jetson mounts)")

    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Assembly bolts use the Ø5 (Ø9 head) holes; #8-32 holes mount to platform.")


if __name__ == "__main__":
    main()
