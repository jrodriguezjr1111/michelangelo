"""
Orin box tube base — the foundation the Orin box stack sits on.

Mirrors the GNSS dual-tube saddle: a two-part clamp that grips TWO parallel
SmallRig tubes (Ø15.39, 60.17 mm centers) with 4× M4 bolts. The upper saddle's
TOP face carries a pocket that receives the Orin box's nesting foot, so the
lowest box drops straight onto this base (same interface as the box lid).

Two parts (print both):
  orin_tube_base_saddle.stl  — upper piece: tube scoops (down) + box-foot pocket (up)
  orin_tube_base_clamp.stl   — lower clamp: tube scoops (up) + M4 nut counterbores

Coordinate frame (model == assembly orientation):
  X = across tubes (separation)   Y = along tube axis   Z = build height
  z = 0 is the tube-axis plane AND the saddle/clamp parting plane.
  Tubes run parallel to the 148 mm (Y) edge of the box footprint.
"""

from build123d import *
from pathlib import Path

# =============================================================================
# Parameters
# =============================================================================
# Box interface (must match make_orin_box.py)
OUTER_X   = 110.0
OUTER_Y   = 148.0
FOOT_X    = 98.0
FOOT_Y    = 136.0
FOOT_H    = 5.0
FIT_CLEAR = 0.4
POCKET_X  = FOOT_X + 2 * FIT_CLEAR     # 98.8
POCKET_Y  = FOOT_Y + 2 * FIT_CLEAR     # 136.8
POCKET_D  = FOOT_H + 0.5               # 5.5 (matches lid pocket)

# SmallRig tubes (match gnss_saddle/make_gnss_saddle.py)
TUBE_OD         = 15.39
TUBE_CENTER_SEP = 60.17
TUBE_CLEAR      = 0.4

# Saddle (upper) — footprint matches box outer so it stacks cleanly
SADDLE_X = OUTER_X          # across tubes (separation)
SADDLE_Y = OUTER_Y          # along tube axis
SADDLE_H = 20.0             # build height above the tube-axis plane

# Lower clamp bar (spans across tubes in X, grips along Y)
CLAMP_X = 84.0             # across tubes
CLAMP_Y = OUTER_Y          # along tube axis
CLAMP_H = 12.0

# M4 clamp bolts (4×, in the bridge between the two tubes)
BOLT_X      = 18.0          # ±X between tubes (inboard of bores)
BOLT_Y      = 18.0          # ±Y along tube
M4_CLEAR_D  = 4.4
M4_HEAD_D   = 8.0
M4_HEAD_DEP = 4.0           # head c'bore (saddle) / nut c'bore (clamp)

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived + sanity
# =============================================================================
R_IN   = TUBE_OD / 2 + TUBE_CLEAR / 2
TUBE_X = TUBE_CENTER_SEP / 2           # tube centers at X = ±TUBE_X
POCKET_FLOOR = SADDLE_H - POCKET_D
BRIDGE = TUBE_X - R_IN                 # half clear span between bores (in X)

assert TUBE_X + R_IN + 3.0 <= SADDLE_X / 2, "Saddle too narrow for tubes + wall"
assert TUBE_X + R_IN + 3.0 <= CLAMP_X / 2, "Clamp too narrow for tubes + wall"
assert BOLT_X + M4_CLEAR_D / 2 + 1.0 < BRIDGE, "M4 bolts clash with tube bores in X"
assert BOLT_Y + M4_HEAD_D / 2 < SADDLE_Y / 2, "M4 bolts exit saddle in Y"
assert BOLT_X < POCKET_X / 2 and BOLT_Y < POCKET_Y / 2, "Bolt heads must sit inside pocket floor"
assert POCKET_FLOOR - M4_HEAD_DEP > R_IN, "Pocket-floor c'bore breaks into tube scoop region"
assert POCKET_X < SADDLE_X and POCKET_Y < SADDLE_Y, "Pocket larger than saddle footprint"


# =============================================================================
# Upper saddle — tube scoops open DOWN, box-foot pocket opens UP
# =============================================================================
def build_saddle() -> Part:
    part = Box(SADDLE_X, SADDLE_Y, SADDLE_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Box-foot pocket on top.
    part -= Pos(0, 0, POCKET_FLOOR) * Box(POCKET_X, POCKET_Y, POCKET_D + 0.1,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Two tube half-bores (axis along Y at z=0 -> upper half removed -> scoop down).
    for sx in (-1, 1):
        bore = Cylinder(R_IN, SADDLE_Y + 0.2, rotation=(90, 0, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        part -= Pos(sx * TUBE_X, 0, 0) * bore

    # 4× M4 through-holes + head counterbore recessed into the pocket floor.
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Pos(sx * BOLT_X, sy * BOLT_Y, -0.2)
            part -= c * Cylinder(M4_CLEAR_D / 2, SADDLE_H + 0.4,
                                 align=(Align.CENTER, Align.CENTER, Align.MIN))
            part -= Pos(sx * BOLT_X, sy * BOLT_Y, POCKET_FLOOR - M4_HEAD_DEP) * Cylinder(
                M4_HEAD_D / 2, M4_HEAD_DEP + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return part


# =============================================================================
# Lower clamp — tube scoops open UP, M4 nut counterbore on the bottom face
# =============================================================================
def build_clamp() -> Part:
    part = Box(CLAMP_X, CLAMP_Y, CLAMP_H,
               align=(Align.CENTER, Align.CENTER, Align.MAX))   # top at z=0

    # Two tube half-bores (axis along Y at z=0 -> lower half removed -> scoop up).
    for sx in (-1, 1):
        bore = Cylinder(R_IN, CLAMP_Y + 0.2, rotation=(90, 0, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        part -= Pos(sx * TUBE_X, 0, 0) * bore

    # 4× M4 through-holes + nut counterbore on the bottom (bed) face.
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Pos(sx * BOLT_X, sy * BOLT_Y, -CLAMP_H - 0.2)
            part -= c * Cylinder(M4_CLEAR_D / 2, CLAMP_H + 0.4,
                                 align=(Align.CENTER, Align.CENTER, Align.MIN))
            part -= Pos(sx * BOLT_X, sy * BOLT_Y, -CLAMP_H - 0.1) * Cylinder(
                M4_HEAD_D / 2, M4_HEAD_DEP + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return part


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    saddle, clamp = build_saddle(), build_clamp()
    for name, part in (("orin_tube_base_saddle", saddle),
                       ("orin_tube_base_clamp", clamp)):
        out = OUT_DIR / f"{name}.stl"
        export_stl(part, str(out))
        print(f"✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)")
    print(f"  Saddle:   {SADDLE_X} × {SADDLE_Y} × {SADDLE_H} mm")
    print(f"  Clamp:    {CLAMP_X} × {CLAMP_Y} × {CLAMP_H} mm")
    print(f"  Tubes:    Ø{TUBE_OD} along Y, centers at X=±{TUBE_X:.2f} (bore Ø{2*R_IN:.2f})")
    print(f"  Pocket:   {POCKET_X} × {POCKET_Y} × {POCKET_D} (receives box foot)")
    print(f"  Bolts:    4× M4 at (±{BOLT_X}, ±{BOLT_Y}); use M4×30 + nuts")
    print("  Print:    clamp scoop-UP as-is; saddle prints pocket-up "
          "(tube scoops bridge ~15.4 mm).")
