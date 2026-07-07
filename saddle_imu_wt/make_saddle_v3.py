"""
CyberWing Canary - WT901 IMU saddle clamp v3 (build123d).

Simplified design: two rectangular blocks with a through-hole for the tube,
bolted together. Each half is essentially a brick with a half-cylinder scooped
out of its split face.

Why v3:
  v2's half-pipe + pad geometry was not printable without supports — the pad
  floated over the open arch. v3's blocks print with the OUTER face on the
  bed and the SPLIT face UP, so every layer is fully supported (bore widens
  upward = no overhang) and bed contact is a full rectangle.

GEOMETRY:
  Coordinate frame (model == print orientation):
    X = along tube axis
    Y = across split, horizontal (bolts pass through Z)
    Z = build direction. z=0 is the BED (outer face), z=HALF_HT is the
        SPLIT FACE (pointing up during print).

  The two halves are mirror-identical except for:
    - sensor features on the upper half
    - (optional) nut pockets on the outer face of one half

OUTPUTS:
  saddle_lower_v3.stl   (plain block with bore + bolt holes)
  saddle_upper_v3.stl   (same + sensor pocket + strap slots on outer face)
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

# Tube (MEASURE WITH CALIPERS)
TUBE_OD = 19.05           # mm  (= 0.75")
CLEARANCE = 0.4           # total diametral clearance

# Block (assembled, both halves combined)
BLOCK_LEN = 55.0          # X, along tube axis
BLOCK_WID = 44.0          # Y, across the split (must fit bore + bolt holes)
BLOCK_HT  = 30.0          # Z, total height of assembled clamp

# Bolt pattern (M5 stainless socket cap)
BOLT_Y_OFFSET = 16.0      # ± from center axis, outboard of bore
SCREW_CLEARANCE_DIAM = 5.4
SCREW_HEAD_DIAM = 9.0
SCREW_HEAD_DEPTH = 5.5    # counterbore depth on bolt-head side (lower half)
NUT_FLATS = 8.0           # M5 hex nut across-flats
NUT_DEPTH = 4.5           # M5 nut thickness
NUT_POCKET_ON_UPPER = True  # True: nut trapped in upper half outer face;
                            # False: nut trapped in lower half outer face.

# Sensor mount (WT901SDCL-BT50) — sits on OUTER face of upper half
USE_SENSOR_POCKET = False
SENSOR_LEN = 51.5
SENSOR_WID = 36.1
SENSOR_FIT = 0.4
POCKET_DEPTH = 2.0

# Strap slots through sensor pad area (zip-tie or velcro)
USE_STRAP_SLOTS = True
STRAP_SLOT_W = 4.0
STRAP_SLOT_L = 12.0
STRAP_INSET = 4.0         # distance from sensor pocket edge to slot

OUT_DIR = Path(__file__).parent


# =============================================================================
# Derived
# =============================================================================

HALF_HT = BLOCK_HT / 2
R_IN = TUBE_OD / 2 + CLEARANCE / 2

assert BOLT_Y_OFFSET + SCREW_HEAD_DIAM / 2 <= BLOCK_WID / 2, \
    "Bolt pattern too wide for block"
assert BOLT_Y_OFFSET - SCREW_CLEARANCE_DIAM / 2 >= R_IN + 1.0, \
    "Bolts too close to bore (need wall thickness)"
assert R_IN + 2.0 <= HALF_HT, \
    "Half-height must clear bore radius + wall"


# =============================================================================
# Build one half
# =============================================================================

def build_half(is_upper: bool) -> Part:
    """Build one half in print orientation: outer face at z=0, split at z=HALF_HT."""

    # Solid block
    half = Box(BLOCK_LEN, BLOCK_WID, HALF_HT,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Bore: half-cylinder cut from the split face downward.
    # Full cylinder along X, centered at (0, 0, HALF_HT). Cutting everything
    # inside that cylinder removes only the portion inside the block (i.e.
    # the half below HALF_HT), giving a half-round trough opening upward.
    bore = Cylinder(radius=R_IN, height=BLOCK_LEN + 0.2,
                    rotation=(0, 90, 0),
                    align=(Align.CENTER, Align.CENTER, Align.CENTER))
    bore.position = (0, 0, HALF_HT)
    half = half - bore

    # Bolt through-holes along Z at ±BOLT_Y_OFFSET
    for sign in (+1, -1):
        hole = Cylinder(radius=SCREW_CLEARANCE_DIAM / 2,
                        height=HALF_HT + 0.2,
                        align=(Align.CENTER, Align.CENTER, Align.MIN))
        hole.position = (0, sign * BOLT_Y_OFFSET, -0.1)
        half = half - hole

    # Bolt-head counterbore or nut pocket on the OUTER face (z=0)
    put_nut_pocket = (is_upper and NUT_POCKET_ON_UPPER) or \
                     (not is_upper and not NUT_POCKET_ON_UPPER)
    for sign in (+1, -1):
        if put_nut_pocket:
            # Hex nut pocket, opens at z=0 (bed side during print; outer face in use)
            nut = RegularPolygon(radius=NUT_FLATS / 2 / 0.866,
                                 side_count=6,
                                 align=(Align.CENTER, Align.CENTER))
            nut = extrude(nut, NUT_DEPTH)
            nut.position = (0, sign * BOLT_Y_OFFSET, 0)
            half = half - nut
        else:
            # Socket-cap counterbore
            cbore = Cylinder(radius=SCREW_HEAD_DIAM / 2,
                             height=SCREW_HEAD_DEPTH,
                             align=(Align.CENTER, Align.CENTER, Align.MIN))
            cbore.position = (0, sign * BOLT_Y_OFFSET, 0)
            half = half - cbore

    # Sensor features on the OUTER face of the upper half (z=0 in model).
    # In use, this face points away from the tube (up), so the sensor is
    # accessible. During print, this face is on the bed — the pocket shows
    # up as a shallow depression on layer 1 and bridges closed after
    # POCKET_DEPTH layers.
    if is_upper and USE_SENSOR_POCKET:
        pocket = Box(SENSOR_LEN + SENSOR_FIT,
                     SENSOR_WID + SENSOR_FIT,
                     POCKET_DEPTH + 0.01,
                     align=(Align.CENTER, Align.CENTER, Align.MIN))
        pocket.position = (0, 0, -0.005)
        half = half - pocket

        if USE_STRAP_SLOTS:
            for x_sign in (+1, -1):
                slot_x = x_sign * (SENSOR_LEN / 2 + STRAP_INSET + STRAP_SLOT_W / 2)
                if abs(slot_x) + STRAP_SLOT_W / 2 > BLOCK_LEN / 2:
                    continue
                slot = Box(STRAP_SLOT_W, STRAP_SLOT_L, HALF_HT + 0.2,
                           align=(Align.CENTER, Align.CENTER, Align.MIN))
                slot.position = (slot_x, 0, -0.1)
                half = half - slot

    return half


# =============================================================================
# Generate
# =============================================================================

def main():
    print("=" * 60)
    print("CyberWing Canary saddle clamp v3 (rectangular block)")
    print("=" * 60)
    print(f"Tube OD:         {TUBE_OD:.2f} mm  (= {TUBE_OD/25.4:.3f}\")")
    print(f"Bore ID:         {2*R_IN:.2f} mm")
    print(f"Block:           {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT} mm")
    print(f"Each half:       {BLOCK_LEN} × {BLOCK_WID} × {HALF_HT} mm")
    print(f"Bolt pattern:    2× M5 at Y = ±{BOLT_Y_OFFSET} mm")
    print(f"Nut pocket on:   {'upper' if NUT_POCKET_ON_UPPER else 'lower'} half")
    print()
    print("Hardware: 2× M5 socket cap (length ≈ BLOCK_HT + 4 mm) + 2× M5 hex nuts")
    print()

    for name, is_upper in (("lower", False), ("upper", True)):
        print(f"Building {name} half...")
        part = build_half(is_upper=is_upper)
        path = OUT_DIR / f"saddle_{name}_v3.stl"
        export_stl(part, str(path))
        print(f"  ✓ {path.name} ({path.stat().st_size:,} bytes)")

    print()
    print("Print notes:")
    print("  - Orientation is already set: OUTER face on bed, split face UP.")
    print("  - No supports needed. 0.2 mm layers, 4 walls, 40% gyroid.")
    print("  - Sensor pocket on upper half bridges over POCKET_DEPTH layers")
    print(f"    (~{int(POCKET_DEPTH/0.2)} layers at 0.2 mm). Slower first layer helps.")
    print()
    print("Assembly:")
    print("  1. Place WT901 in pocket on upper half outer face.")
    print("  2. Optional: zip-tie through strap slots.")
    print(f"  3. Press M5 nuts into hex pockets on {'upper' if NUT_POCKET_ON_UPPER else 'lower'} half.")
    print("  4. Position both halves around tube, split faces together.")
    print("  5. Insert M5 bolts from the opposite side, tighten evenly.")


if __name__ == "__main__":
    main()
