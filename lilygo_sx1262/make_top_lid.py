"""
LILYGO SX1262 housing — LID over the TOP plate (covers the board).

A tunnel cover for the assembly of `make_top.py` (LILYGO top plate, board on
5 mm M2 standoffs above it) sitting on `flycatcher/make_imu_platform_saddle.py`:

  - 101 × 65 footprint, same plate frame as make_top.py (incl. the +10.5 mm
    export shift, so the STLs assemble in the same coordinates).
  - Top 3 mm + two long (±Y) walls dropping to the top plate's face.
  - ±X ends OPEN — the LILYGO board spans nearly the full 101 mm (M2 at
    ±47.67), and the +X end carries the over-hanging connector/antenna.
  - 4× M3 csk holes on the flycatcher 58 × 49 assembly pattern (same as the
    top plate): long M3 screws pass lid → top plate → saddle (through-bolt).
  - Interior height 14 mm clears standoffs (5) + PCB (1.6) + components.

Print top-face DOWN (walls up). No supports.

Output: lilygo_sx1262_top_lid.stl
"""

from build123d import *
from pathlib import Path

# Envelope — matches make_top.py
LID_L = 101.0
LID_W = 65.0
TOP_T = 3.0
WALL_T = 2.5
INTERIOR_H = 14.0        # clearance over the top plate's face
LID_H = TOP_T + INTERIOR_H

# Assembly frame (matches make_top.py)
X_FLUSH_OFFSET = 10.5    # export shift, same as the top plate

# M3 attach — flycatcher 58 × 49 assembly pattern; asymmetric in plate-local.
FLYCATCHER_M3_X = 58.0
FLYCATCHER_M3_Y = 49.0
M3_CLEAR_D   = 3.4
M3_CSK_D     = 5.5
M3_CSK_DEPTH = 1.6

# LILYGO stack clearance check (info): standoff 5 + PCB 1.6 + parts ≈ 6
STACK_H = 5.0 + 1.6 + 6.0

OUT_DIR = Path(__file__).parent

M3_POS = [(sx * FLYCATCHER_M3_X / 2 - X_FLUSH_OFFSET, sy * FLYCATCHER_M3_Y / 2)
          for sx in (-1, 1) for sy in (-1, 1)]

# Sanity
assert INTERIOR_H > STACK_H + 1, "Interior too low for the LILYGO stack"
for _x, _y in M3_POS:
    assert abs(_x) + M3_CSK_D / 2 + 1 < LID_L / 2, "M3 csk hits an X end"
    assert abs(_y) + M3_CSK_D / 2 < LID_W / 2 - WALL_T, "M3 csk lands on a Y wall"


def build_lid() -> Part:
    # Top plate of the lid
    lid = Pos(0, 0, INTERIOR_H) * Box(
        LID_L, LID_W, TOP_T, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Two long walls (±Y), full X length, dropping to the top plate's face.
    for sy in (-1, 1):
        lid += Pos(0, sy * (LID_W / 2 - WALL_T / 2), 0) * Box(
            LID_L, WALL_T, INTERIOR_H,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M3 through-holes, csk on the lid's outer (top) face.
    for cx, cy in M3_POS:
        lid -= Pos(cx, cy, -0.2) * Cylinder(
            M3_CLEAR_D / 2, LID_H + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        lid -= Pos(cx, cy, LID_H - M3_CSK_DEPTH) * Cylinder(
            M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    return lid


if __name__ == "__main__":
    part = build_lid()
    # Same assembly shift as make_top.py so the STLs line up.
    part = Pos(X_FLUSH_OFFSET, 0, 0) * part
    out = OUT_DIR / "lilygo_sx1262_top_lid.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Lid:        {LID_L} × {LID_W} × {LID_H} mm (top {TOP_T}, walls {WALL_T})")
    print(f"  Interior:   {LID_L} × {LID_W - 2*WALL_T} × {INTERIOR_H} mm, ±X ends OPEN")
    print(f"  Clearance:  stack ≈{STACK_H} mm under {INTERIOR_H} mm interior "
          f"({INTERIOR_H - STACK_H:.1f} mm spare)")
    tx = sorted({round(x, 2) for x, _ in M3_POS})
    print(f"  M3 attach:  4× Ø{M3_CLEAR_D}, csk Ø{M3_CSK_D}×{M3_CSK_DEPTH} on the top "
          f"face — flycatcher {FLYCATCHER_M3_X}×{FLYCATCHER_M3_Y} (assembly), "
          f"plate-local X {tx[0]:+.1f}/{tx[1]:+.1f}, Y ±{FLYCATCHER_M3_Y/2}")
    print(f"  Through-bolt: lid → top plate → saddle (all three share the pattern)")
    print(f"  Export X shift: +{X_FLUSH_OFFSET} (same frame as lilygo_sx1262_top.stl)")
    print(f"  Print top-face DOWN, walls up. No supports.")
