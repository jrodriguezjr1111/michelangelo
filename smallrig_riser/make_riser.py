"""
SmallRig riser — rectangular prism that sits underneath a SmallRig
component to add 13 mm of standoff.

Top face: 64.23 × 15.30 mm.
Four through-holes drilled along the X axis, centered in Y:
  - 2 inner holes  (Ø4.90):  spaced 17.97 mm apart.
  - 2 outer holes  (Ø6.20):  spaced 35.72 mm apart, with bottom-side
    counterbore Ø11 × 4 mm deep (bolt head pocket).

Coordinate frame (origin = block center):
  X = long axis (64.23). Y = width axis (15.30). Z = height (13).

Output:
  smallrig_riser.stl
"""

from build123d import *
from pathlib import Path

# =============================================================================
# Block envelope
# =============================================================================
BLOCK_L = 64.23      # X
BLOCK_W = 15.30      # Y
BLOCK_H = 18.00      # Z

# =============================================================================
# Through-hole patterns (centered in Y, along X)
# =============================================================================
INNER_SPACING = 17.97
INNER_D       = 4.90

OUTER_SPACING = 35.72
OUTER_D       = 6.20
HEAD_D        = 11.00
HEAD_DEPTH    = 4.00     # counterbore on the BOTTOM face (outer holes)

OUT_DIR = Path(__file__).parent

# =============================================================================
# Sanity
# =============================================================================
assert OUTER_SPACING / 2 + OUTER_D / 2 + 0.5 < BLOCK_L / 2, "Outer hole hits X edge"
assert HEAD_D / 2 + 0.5 < BLOCK_W / 2, "Bolt-head counterbore exceeds block width"
assert HEAD_DEPTH < BLOCK_H, "Counterbore deeper than block"


def build_riser() -> Part:
    body = Box(BLOCK_L, BLOCK_W, BLOCK_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Inner holes — Ø4.90 through
    for sx in (-1, 1):
        cx = sx * INNER_SPACING / 2
        body -= Pos(cx, 0, -0.2) * Cylinder(
            INNER_D / 2, BLOCK_H + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Outer holes — Ø6.20 through + Ø11 × 4 counterbore on bottom
    for sx in (-1, 1):
        cx = sx * OUTER_SPACING / 2
        body -= Pos(cx, 0, -0.2) * Cylinder(
            OUTER_D / 2, BLOCK_H + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        body -= Pos(cx, 0, -0.05) * Cylinder(
            HEAD_D / 2, HEAD_DEPTH + 0.1,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    return body


if __name__ == "__main__":
    part = build_riser()
    out = OUT_DIR / "smallrig_riser.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Block:  {BLOCK_L} × {BLOCK_W} × {BLOCK_H} mm")
    print(f"  Inner: 2× Ø{INNER_D} thru at X=±{INNER_SPACING/2:.3f}")
    print(f"  Outer: 2× Ø{OUTER_D} thru at X=±{OUTER_SPACING/2:.3f}, "
          f"counterbore Ø{HEAD_D} × {HEAD_DEPTH} on bottom")
    head_radial = HEAD_D / 2 - OUTER_D / 2
    head_to_inner = (OUTER_SPACING - INNER_SPACING) / 2 - (HEAD_D + INNER_D) / 2
    head_to_yedge = BLOCK_W / 2 - HEAD_D / 2
    head_to_xedge = BLOCK_L / 2 - OUTER_SPACING / 2 - HEAD_D / 2
    floor_under_head = BLOCK_H - HEAD_DEPTH
    print(f"  Counterbore radial wall (around outer thru): {head_radial:.2f} mm")
    print(f"  Counterbore ↔ inner hole gap: {head_to_inner:.2f} mm")
    print(f"  Counterbore ↔ Y edge: {head_to_yedge:.2f} mm")
    print(f"  Counterbore ↔ X edge: {head_to_xedge:.2f} mm")
    print(f"  Material above counterbore: {floor_under_head:.2f} mm")
