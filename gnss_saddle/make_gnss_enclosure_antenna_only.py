"""
GNSS enclosure (antenna-only variant) that hangs UNDER the +Y wing of the
dual-tube saddle from make_gnss_saddle_wide.py. Houses the ZED-F9P breakout.

Identical to make_gnss_enclosure.py but with ONLY the Ø6.3 GNSS antenna
passthrough on the −X wall — no USB-C cutout.

Assembled orientation:
    saddle wing
    ───────────       ← M3 csk on saddle bottom
    ┌─[floor]─┐       ← enclosure mount face (TOP of enclosure)
    │ cavity  │
    └─ open ──┘       ← cavity opens DOWNWARD

Mounting:
  4× M3 bolts drop DOWN from above through the saddle's countersunk ZED
  holes and through the enclosure floor thru-holes (no captive nut pockets;
  use free nuts/washers or heat-set inserts as preferred).

Print orientation: floor on the bed (cavity opens UP during printing).
The model is built in assembled orientation (mount face at top) and
rotated 180° about X before STL export. No supports needed.
"""

from pathlib import Path
from build123d import Align, Box, Cylinder, Part, Pos, Rot, export_stl

# =============================================================================
# Parameters
# =============================================================================

ENC_L = 52.0          # X (along saddle tube axis)
ENC_W = 52.0          # Y (across the saddle wing)
ENC_H = 18.0          # Z (total; cavity height = ENC_H − FLOOR_T)

FLOOR_T = 3.0
WALL_T  = 2.5

# Mount pattern — must match the saddle's ZED-F9P 37.6 mm sq csk holes.
M3_PATTERN = 37.6
M3_CLEAR_D = 3.4

# Floor occupies Z ∈ [FLOOR_Z0, ENC_H] (top of the enclosure).
# Cavity occupies Z ∈ [0, FLOOR_Z0] (open downward).
FLOOR_Z0 = ENC_H - FLOOR_T

# GNSS antenna opening on the −X wall (centered in Y; only cutout).
GNSS_D        = 6.3
GNSS_Y        = 0.0
GNSS_Z_CENTER = FLOOR_Z0 - 5.5      # = 9.5 mm above the cavity opening

OUT_DIR = Path(__file__).parent

# =============================================================================
# Sanity
# =============================================================================
assert ENC_L >= M3_PATTERN + 2 * WALL_T + 2, "Footprint too small for M3 pattern (X)"
assert ENC_W >= M3_PATTERN + 2 * WALL_T + 2, "Footprint too small for M3 pattern (Y)"
assert GNSS_Z_CENTER - GNSS_D / 2 >= 1,            "GNSS cutout exits cavity opening"
assert GNSS_Z_CENTER + GNSS_D / 2 <= FLOOR_Z0 - 0.5, "GNSS cutout overlaps floor"
_interior_y_half = ENC_W / 2 - WALL_T
assert abs(GNSS_Y) + GNSS_D / 2 <= _interior_y_half - 0.5, "GNSS cutout exits −X wall in Y"

# =============================================================================
# Geometry
# =============================================================================

def build_enclosure() -> Part:
    body = Box(ENC_L, ENC_W, ENC_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Hollow cavity — open at the BOTTOM (no floor on the cavity side).
    cav_l = ENC_L - 2 * WALL_T
    cav_w = ENC_W - 2 * WALL_T
    body -= Pos(0, 0, -0.2) * Box(
        cav_l, cav_w, FLOOR_Z0 + 0.2,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M3 thru-holes in the floor (top). No hex-nut pockets.
    half = M3_PATTERN / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * half, sy * half
            body -= Pos(cx, cy, FLOOR_Z0 - 0.2) * Cylinder(
                M3_CLEAR_D / 2, FLOOR_T + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Ø6.3 GNSS round cutout in the −X wall (cylinder oriented along X).
    body -= Pos(-ENC_L / 2 - 0.2, GNSS_Y, GNSS_Z_CENTER) * Rot(0, 90, 0) * Cylinder(
        GNSS_D / 2, WALL_T + 0.8,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    return body


if __name__ == "__main__":
    part = build_enclosure()
    # Flip 180° about X so the floor (mount face) lands on the bed for printing.
    part = Rot(180, 0, 0) * part
    part = Pos(0, 0, ENC_H) * part
    out = OUT_DIR / "gnss_enclosure_antenna_only.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print("=" * 64)
    print("GNSS enclosure (antenna-only) for saddle +Y wing — build123d")
    print("=" * 64)
    print(f"  Footprint:  {ENC_L} × {ENC_W} × {ENC_H} mm")
    print(f"  Floor:      {FLOOR_T} mm   Wall: {WALL_T} mm")
    print(f"  Cavity:     {ENC_L - 2*WALL_T} × {ENC_W - 2*WALL_T} × "
          f"{ENC_H - FLOOR_T} mm (opens downward in service)")
    print(f"  Mount:      4× M3 Ø{M3_CLEAR_D} at {M3_PATTERN} mm sq "
          f"(matches saddle ZED pattern, thru-holes only)")
    print(f"  GNSS only:  Ø{GNSS_D} at Y={GNSS_Y:+.1f}, Z={GNSS_Z_CENTER:.1f} "
          f"(no USB-C cutout)")
    print(f"  ✓ {out.name}  ({kb:.0f} KB)")
    print("\nSTL is pre-flipped — print floor-on-bed, cavity-up. No supports.")
