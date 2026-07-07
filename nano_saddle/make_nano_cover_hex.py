"""
Hex-lattice top cover for the dual-Jetson nano saddle.

Open honeycomb lattice across the entire footprint — no solid skin, so every
cell vents directly to ambient. Replaces make_nano_cover.py's perforated
plate (Orin fan grille + Nano heatsink louvers) with a uniform pattern.

Structure:
  • Perimeter frame (FRAME_W mm wide solid border)
  • Solid bosses (BOSS_D Ø) at each of the 8× M3 Jetson mount positions
  • Hex cell lattice (HEX_CELL_R circumradius, HEX_WALL walls) filling the
    interior between frame and bosses

Mounts to the saddle via the same 8× M3 Jetson hole pattern on 30 mm
standoffs (Nano on −Y, Orin on +Y).

Print flat on the bed (vents-up). Use a wide brim — the lattice has small
first-layer contact and needs the brim to anchor.
"""

from build123d import *
from pathlib import Path
import math

# =============================================================================
# PARAMETERS  (mirror make_nano_cover.py where shared)
# =============================================================================

BLOCK_LEN = 70.0          # X
BLOCK_WID = 197.0         # Y
PLATE_T   = 3.0
CLEAR_H   = 30.0          # standoff height (hardware, BOM only)

# Jetson M3 mount patterns
NANO_PATTERN_Y = 86.14
NANO_PATTERN_X = 58.25
ORIN_PATTERN_Y = 92.12
ORIN_PATTERN_X = 57.59
M3_CLEAR_D     = 3.4
M3_CB_D        = 5.3
M3_CB_DEPTH    = 1.6

ORIN_Y_CENTER =  BLOCK_WID / 4                                  # +49.25
NANO_Y_CENTER = -(BLOCK_WID / 2 - NANO_PATTERN_Y / 2 - 3.19)    # −52.24

# Lattice / frame
FRAME_W      = 3.5        # perimeter solid border width
BOSS_D       = 9.0        # solid pad Ø around each M3 hole
HEX_CELL_R   = 5.0        # pointy-top hex circumradius (vertex→center, open cell)
HEX_WALL     = 1.6        # wall thickness between adjacent cells
CLEARANCE    = 1.0        # extra gap from lattice to frame / bosses

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived
# =============================================================================
HEX_F = HEX_CELL_R * math.sqrt(3)              # flat-to-flat of open cell
PITCH_X = HEX_F + HEX_WALL                     # horizontal pitch (same row)
PITCH_Y = 1.5 * HEX_CELL_R + HEX_WALL * math.sqrt(3) / 2  # vertical row pitch

# Hex extent from its center
HEX_DX = HEX_F / 2                             # to flat side
HEX_DY = HEX_CELL_R                            # to vertex

# =============================================================================
# Sanity
# =============================================================================
for nm, py, yc in (("Nano", NANO_PATTERN_Y, NANO_Y_CENTER),
                   ("Orin", ORIN_PATTERN_Y, ORIN_Y_CENTER)):
    # M3 c'bore (mandatory) must fit on the plate; bosses are optional for
    # holes that fall in the lattice interior — outer holes get material from
    # the solid perimeter frame.
    assert abs(yc) + py / 2 + M3_CB_D / 2 + 0.4 < BLOCK_WID / 2, \
        f"{nm} M3 c'bore exits plate in Y"
    assert py / 2 + M3_CB_D / 2 + 0.4 < BLOCK_WID / 2, \
        f"{nm} M3 c'bore exits plate in X"
assert HEX_WALL >= 1.0, "Hex wall too thin to print reliably"
assert HEX_CELL_R >= 3.0, "Hex cell too small — clogs airflow"
assert FRAME_W >= 2.5, "Frame too thin"

# =============================================================================
# Geometry
# =============================================================================

def boss_centers():
    """Return list of (x, y) for the 8 M3 mount positions."""
    out = []
    for py, px, yc in ((NANO_PATTERN_Y, NANO_PATTERN_X, NANO_Y_CENTER),
                       (ORIN_PATTERN_Y, ORIN_PATTERN_X, ORIN_Y_CENTER)):
        for sx in (-1, 1):
            for sy in (-1, 1):
                out.append((sx * px / 2, yc + sy * py / 2))
    return out


def build_cover() -> Part:
    plate = Box(BLOCK_LEN, BLOCK_WID, PLATE_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # --- Hex lattice subtraction ---
    # Inner usable region (clear of frame)
    inner_hx = BLOCK_LEN / 2 - FRAME_W - CLEARANCE   # half-extent in X
    inner_hy = BLOCK_WID / 2 - FRAME_W - CLEARANCE   # half-extent in Y

    bosses = boss_centers()
    boss_keepout_r = BOSS_D / 2 + CLEARANCE          # distance from boss center
                                                     # below which we skip hex

    # Sweep enough rows to cover the inner region
    n_rows = int(math.ceil(inner_hy / PITCH_Y)) + 1
    n_cols = int(math.ceil(inner_hx / PITCH_X)) + 1

    cut = Part()
    for jr in range(-n_rows, n_rows + 1):
        cy = jr * PITCH_Y
        row_offset = (PITCH_X / 2) if (jr % 2) else 0.0
        for ic in range(-n_cols, n_cols + 1):
            cx = ic * PITCH_X + row_offset
            # Skip if outside inner region (hex would clip frame)
            if abs(cx) + HEX_DX > inner_hx:        continue
            if abs(cy) + HEX_DY > inner_hy:        continue
            # Skip if too close to any boss
            if any((cx - bx) ** 2 + (cy - by) ** 2 < boss_keepout_r ** 2
                   for (bx, by) in bosses):
                continue
            # Subtract pointy-top hex through full thickness
            hex_sk = RegularPolygon(HEX_CELL_R, 6, major_radius=True)
            hex_prism = extrude(hex_sk, amount=PLATE_T + 0.4)
            cut += Pos(cx, cy, -0.2) * hex_prism

    plate -= cut

    # --- 8× M3 clearance + top counterbore at boss centers ---
    for (cx, cy) in bosses:
        plate -= Pos(cx, cy, -0.2) * Cylinder(
            M3_CLEAR_D / 2, PLATE_T + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        plate -= Pos(cx, cy, PLATE_T - M3_CB_DEPTH) * Cylinder(
            M3_CB_D / 2, M3_CB_DEPTH + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    return plate


def main() -> None:
    cover = build_cover()
    out = OUT_DIR / "nano_cover_hex.stl"
    export_stl(cover, str(out))
    print("=" * 62)
    print("Dual-Jetson nano saddle — hex-lattice top cover")
    print("=" * 62)
    print(f"Footprint:    {BLOCK_LEN} × {BLOCK_WID} × {PLATE_T} mm")
    print(f"Frame:        {FRAME_W} mm solid border")
    print(f"Hex cell:     R={HEX_CELL_R} (flat-to-flat {HEX_F:.2f}), "
          f"wall {HEX_WALL} mm")
    print(f"Pitch:        X={PITCH_X:.2f} mm, Y={PITCH_Y:.2f} mm")
    print(f"Bosses:       8× Ø{BOSS_D} at Nano + Orin M3 patterns "
          f"(c'bore Ø{M3_CB_D}×{M3_CB_DEPTH})")
    print(f"Standoffs:    {CLEAR_H} mm (hardware) board-top → cover")
    print(f"  ✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)")
    print("\nPrint flat on bed, lattice-up. Use a 5-8 mm brim — the lattice "
          "has small first-layer contact area.")
    print("Hardware: 8× M3 screws + 8× M3 standoffs (≈{:.0f} mm).".format(CLEAR_H))


if __name__ == "__main__":
    main()
