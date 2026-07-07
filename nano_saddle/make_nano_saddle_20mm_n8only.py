"""
CyberWing — minimal #8-32-only saddle clamp, Ø20 tubes.

Stripped from make_nano_saddle_20mm.py to ONLY the #8-32 mounting holes:
  KEEP   : Ø20 tube bores, 4× #8-32 (Ø4.4) through-holes.
  REMOVE : Ø5 assembly holes, Jetson Nano M3, Jetson Orin M3.
  SIZE   : block reduced in X and Y to just wrap the #8-32 pattern (+6 mm edge).

Both halves are identical (the #8-32 holes both join the two halves and mount the
saddle to a platform) — print two copies of the one half.

Coordinate frame (model == print orientation):
  X = along tube axis, Y = across tubes (tubes at Y = ±TUBE_CENTER_SEP/2),
  Z = build. z=0 = BED (outer face), z=HALF_HT = SPLIT face (up).

Mirrors nano_saddle_20mm_n8only_preview.html.

Output:
  nano_saddle_20mm_n8only_half.stl   (print 2 copies, mirror-identical)
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

# #8-32 mounting holes — the only hole feature.
N8_CLEAR_D = 4.4
N8_PAT_X   = 51.83
N8_PAT_Y   = 120.18
N8_EDGE    = 6.0            # hole-center -> block edge margin (sets block size)

# Block sized to wrap the #8-32 pattern.
BLOCK_LEN = N8_PAT_X + 2 * N8_EDGE     # X  -> 63.83
BLOCK_WID = N8_PAT_Y + 2 * N8_EDGE     # Y  -> 132.18
BLOCK_HT  = 28.0                        # Z (set by tube bore)

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived
# =============================================================================

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
TUBE_Y  = TUBE_CENTER_SEP / 2

# =============================================================================
# Sanity
# =============================================================================
assert R_IN + 2.0 <= HALF_HT, "Half-height must clear tube bore radius + wall"
assert TUBE_Y + R_IN + 2.0 <= BLOCK_WID / 2, "Block too narrow for tubes + wall"
assert N8_PAT_X / 2 + N8_CLEAR_D / 2 + 0.5 < BLOCK_LEN / 2, "#8-32 holes exit block in X"
assert N8_PAT_Y / 2 + N8_CLEAR_D / 2 + 0.5 < BLOCK_WID / 2, "#8-32 holes exit block in Y"
assert N8_PAT_Y / 2 - N8_CLEAR_D / 2 > TUBE_Y + R_IN, "#8-32 holes clash with tube bores"


# =============================================================================
# Build one half (both halves identical — print twice)
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

    # 4× #8-32 through-holes (plain clearance, both halves).
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * N8_PAT_X / 2, sy * N8_PAT_Y / 2
            block -= Pos(cx, cy, -0.2) * Cylinder(
                N8_CLEAR_D / 2, HALF_HT + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return block


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("CyberWing #8-32-only saddle — Ø20 tubes (minimal)")
    print("=" * 60)
    print(f"Block:        {BLOCK_LEN:.2f} × {BLOCK_WID:.2f} × {BLOCK_HT} mm assembled")
    print(f"Tubes:        Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f} (sep {TUBE_CENTER_SEP})")
    print(f"Bore ID:      Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"#8-32 holes:  4× Ø{N8_CLEAR_D} at (±{N8_PAT_X/2:.2f}, ±{N8_PAT_Y/2:.2f}) "
          f"— {N8_PAT_X}×{N8_PAT_Y}, {N8_EDGE} mm edge margin")
    print()

    half = build_half()
    out = OUT_DIR / "nano_saddle_20mm_n8only_half.stl"
    export_stl(half, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)")
    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Print 2 copies (both halves identical). #8-32 bolts join halves + mount to platform.")


if __name__ == "__main__":
    main()
