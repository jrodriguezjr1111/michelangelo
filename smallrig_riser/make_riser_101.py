"""
SmallRig riser — 101 mm variant.

Rectangular standoff block, 80 × 16 × 35 mm. All holes centered in Y,
along the X axis:
  - 2× Ø3.80 straight through, spaced 58.49 mm (X = ±29.245)
  - 2× Ø4.90 (inner) through, spaced 17.97 mm (X = ±8.985)
  - 2× Ø6.20 (outer) through, spaced 35.72 mm (X = ±17.860), with a
    Ø11 × 4 mm bolt-head counterbore on the BOTTOM face (concentric)

Coordinate frame (origin = block center):
  X = long axis (80). Y = width axis (16). Z = height (35), z=0 = bottom.

Output:
  smallrig_riser_101.stl
"""

from build123d import *
from pathlib import Path

# =============================================================================
# Block envelope
# =============================================================================
BLOCK_L = 80.00      # X
BLOCK_W = 16.00      # Y
BLOCK_H = 35.00      # Z

# =============================================================================
# Through-hole pattern (centered in Y, along X) + top head pocket
# =============================================================================
HOLE_SPACING = 58.49
HOLE_D       = 3.80      # screw shaft (straight through, no pocket)

# Original make_riser.py pattern
INNER_SPACING = 17.97
INNER_D       = 4.90

OUTER_SPACING = 35.72
OUTER_D       = 6.20
BOT_HEAD_D    = 11.00    # bolt-head counterbore Ø (BOTTOM face)
BOT_HEAD_DEPTH = 4.00

OUT_DIR = Path(__file__).parent

# =============================================================================
# Sanity
# =============================================================================
assert HOLE_SPACING / 2 + HOLE_D / 2 + 0.5 < BLOCK_L / 2, "Ø3.80 hole hits X edge"
assert OUTER_SPACING / 2 + OUTER_D / 2 + 0.5 < BLOCK_L / 2, "Outer hole hits X edge"
assert BOT_HEAD_D / 2 + 0.5 < BLOCK_W / 2, "Bottom counterbore exceeds block width"
assert BOT_HEAD_DEPTH < BLOCK_H, "Bottom counterbore deeper than block"
# Outer bottom pocket must not collide with the inner through-holes in X
assert (OUTER_SPACING - INNER_SPACING) / 2 - (BOT_HEAD_D / 2 + INNER_D / 2) > 0.3, \
    "Outer bottom counterbore overlaps inner hole"


def build_riser() -> Part:
    body = Box(BLOCK_L, BLOCK_W, BLOCK_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 2× Ø3.80 straight through-holes (no pocket)
    for sx in (-1, 1):
        cx = sx * HOLE_SPACING / 2
        body -= Pos(cx, 0, -0.2) * Cylinder(
            HOLE_D / 2, BLOCK_H + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 2× inner Ø4.90 through-holes
    for sx in (-1, 1):
        cx = sx * INNER_SPACING / 2
        body -= Pos(cx, 0, -0.2) * Cylinder(
            INNER_D / 2, BLOCK_H + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 2× outer Ø6.20 through-holes + Ø11 × 4 counterbore on the BOTTOM face
    for sx in (-1, 1):
        cx = sx * OUTER_SPACING / 2
        body -= Pos(cx, 0, -0.2) * Cylinder(
            OUTER_D / 2, BLOCK_H + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        body -= Pos(cx, 0, -0.05) * Cylinder(
            BOT_HEAD_D / 2, BOT_HEAD_DEPTH + 0.1,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    return body


if __name__ == "__main__":
    part = build_riser()
    out = OUT_DIR / "smallrig_riser_101.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Block:  {BLOCK_L} × {BLOCK_W} × {BLOCK_H} mm")
    print(f"  Ø3.80:  2× straight thru at X=±{HOLE_SPACING/2:.3f}")
    print(f"  Inner:  2× Ø{INNER_D} thru at X=±{INNER_SPACING/2:.3f}")
    print(f"  Outer:  2× Ø{OUTER_D} thru at X=±{OUTER_SPACING/2:.3f}, "
          f"bottom pocket Ø{BOT_HEAD_D} × {BOT_HEAD_DEPTH}")
    inner_to_outerpocket = (OUTER_SPACING - INNER_SPACING) / 2 - (BOT_HEAD_D + INNER_D) / 2
    print(f"  Inner hole ↔ outer bottom pocket gap: {inner_to_outerpocket:.2f} mm")
    print(f"  Material above bottom pocket: {BLOCK_H - BOT_HEAD_DEPTH:.2f} mm")
