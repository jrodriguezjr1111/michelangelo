"""
GNSS enclosure that hangs UNDER the +Y wing of the dual-tube saddle
from make_gnss_saddle_wide.py. Houses the ZED-F9P breakout.

Assembled orientation:
    saddle wing
    ───────────       ← M3 csk on saddle bottom
    ┌─[floor]─┐       ← enclosure mount face (TOP of enclosure)
    │ cavity  │
    └─ open ──┘       ← cavity opens DOWNWARD

The −X wall carries both cable openings side-by-side:
  • USB-C rectangular passthrough
  • Ø6.3 GNSS antenna passthrough

Mounting:
  4× M3 bolts drop DOWN from above through the saddle's countersunk ZED
  holes and engage M3 hex nuts captive in pockets on the underside
  (cavity side) of the enclosure floor. Insert nuts from below into
  pockets before mating to the saddle — friction holds them while the
  bolt threads down. Heat-set inserts are a drop-in upgrade.

Print orientation: floor on the bed (cavity opens UP during printing).
The model is built in assembled orientation (mount face at top) and
rotated 180° about X before STL export. No supports needed.
"""

from math import cos, pi
from pathlib import Path
from build123d import (
    Align, Box, Cylinder, Part, Pos, RegularPolygon, Rot, export_stl, extrude,
)

# =============================================================================
# Parameters
# =============================================================================

ENC_L = 52.0          # X (along saddle tube axis)
ENC_W = 52.0          # Y (across the saddle wing)
ENC_H = 18.0          # Z (total; cavity height = ENC_H − FLOOR_T)
# Footprint sized for a 45 × 45 mm ZED-F9P breakout with ~1 mm clearance
# per side (cavity = 47 × 47 mm at WALL_T = 2.5).

FLOOR_T = 3.0
WALL_T  = 2.5

# Mount pattern — must match the saddle's ZED-F9P 37.6 mm sq csk holes.
M3_PATTERN = 37.6
M3_CLEAR_D = 3.4

# Captive M3 hex-nut pocket (opens upward into the cavity).
M3_NUT_AF = 5.6       # across-flats (DIN-934 M3 ≈ 5.5, +0.1 print slop)
M3_NUT_T  = 2.5

# Floor occupies Z ∈ [FLOOR_Z0, ENC_H] (top of the enclosure).
# Cavity occupies Z ∈ [0, FLOOR_Z0] (open downward).
FLOOR_Z0 = ENC_H - FLOOR_T

# Cable openings on the −X wall (both on the same side).
# Z is measured in assembled orientation, Z=0 is the cavity opening.
# Each cutout is centered 5.5 mm below the floor (mid-height of a typical
# USB-C plug hanging from a board mounted to the enclosure ceiling).
USB_W        = 18.0                # along Y (wide enough for USB-C boot/overmold)
USB_H        = 9.0                 # along Z
USB_Y        = +8.0
USB_Z_CENTER = FLOOR_Z0 - 5.5      # = 9.5 mm above the cavity opening

GNSS_D        = 6.3
GNSS_Y        = -8.0
GNSS_Z_CENTER = USB_Z_CENTER

OUT_DIR = Path(__file__).parent

# =============================================================================
# Sanity
# =============================================================================
assert ENC_L >= M3_PATTERN + 2 * WALL_T + 2, "Footprint too small for M3 pattern (X)"
assert ENC_W >= M3_PATTERN + 2 * WALL_T + 2, "Footprint too small for M3 pattern (Y)"
assert USB_Z_CENTER - USB_H / 2  >= 1,             "USB cutout exits cavity opening"
assert USB_Z_CENTER + USB_H / 2  <= FLOOR_Z0 - 0.5, "USB cutout overlaps floor"
assert GNSS_Z_CENTER - GNSS_D / 2 >= 1,            "GNSS cutout exits cavity opening"
assert GNSS_Z_CENTER + GNSS_D / 2 <= FLOOR_Z0 - 0.5, "GNSS cutout overlaps floor"
assert abs(USB_Y - GNSS_Y) > (USB_W + GNSS_D) / 2 + 1.0, \
    "USB and GNSS cutouts too close in Y"
_interior_y_half = ENC_W / 2 - WALL_T
assert abs(USB_Y)  + USB_W / 2  <= _interior_y_half - 0.5, "USB cutout exits −X wall in Y"
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

    # 4× M3 thru-holes in the floor (top) + captive hex-nut pockets opening
    # DOWN into the cavity.
    half = M3_PATTERN / 2
    nut_circ_r = (M3_NUT_AF / 2) / cos(pi / 6)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * half, sy * half
            # Clearance hole all the way through the floor.
            body -= Pos(cx, cy, FLOOR_Z0 - 0.2) * Cylinder(
                M3_CLEAR_D / 2, FLOOR_T + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            # Hex nut pocket: open at Z = FLOOR_Z0 (cavity side), recessed into floor.
            hex_sk = RegularPolygon(nut_circ_r, 6)
            nut_pocket = Pos(cx, cy, FLOOR_Z0 - 0.1) * extrude(
                hex_sk, amount=M3_NUT_T + 0.2)
            body -= nut_pocket

    # USB-C rectangular cutout in the −X wall.
    body -= Pos(-ENC_L / 2 - 0.2, USB_Y, USB_Z_CENTER - USB_H / 2) * Box(
        WALL_T + 0.8, USB_W, USB_H,
        align=(Align.MIN, Align.CENTER, Align.MIN))

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
    out = OUT_DIR / "gnss_enclosure.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print("=" * 64)
    print("GNSS enclosure for saddle +Y wing — build123d")
    print("=" * 64)
    print(f"  Footprint:  {ENC_L} × {ENC_W} × {ENC_H} mm")
    print(f"  Floor:      {FLOOR_T} mm   Wall: {WALL_T} mm")
    print(f"  Cavity:     {ENC_L - 2*WALL_T} × {ENC_W - 2*WALL_T} × "
          f"{ENC_H - FLOOR_T} mm (opens downward in service)")
    print(f"  Mount:      4× M3 Ø{M3_CLEAR_D} at {M3_PATTERN} mm sq "
          f"(matches saddle ZED pattern)")
    print(f"              hex-nut pockets AF {M3_NUT_AF} × {M3_NUT_T} mm "
          f"on cavity floor")
    print(f"  USB-C:      {USB_W} × {USB_H} mm at Y={USB_Y:+.1f}, "
          f"Z={USB_Z_CENTER:.1f} (assembled coords)")
    print(f"  GNSS:       Ø{GNSS_D} at Y={GNSS_Y:+.1f}, Z={GNSS_Z_CENTER:.1f}")
    print(f"  ✓ {out.name}  ({kb:.0f} KB)")
    print("\nAssembled: enclosure hangs UNDER the saddle's +Y wing. Mount face")
    print("is the TOP of the enclosure; cavity opens DOWNWARD.")
    print("Bolts drop from above through the saddle csk holes and tighten into")
    print("M3 nuts seated in the floor pockets (or use heat-set inserts).")
    print("STL is pre-flipped — print floor-on-bed, cavity-up. No supports.")
