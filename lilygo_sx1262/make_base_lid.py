"""
ZED-F9P + IMU carrier base — LID (for make_base_stacked.py).

Cover for the carrier's open top that ALSO serves as the LILYGO mounting plate:
  - 101 × 65 × 3 plate seats on the rim and the 4 corner-boss tops.
  - 4× M3 holes, csk on the LID's top face, at the carrier's corner-boss
    pattern (±45, ±27).
  - 4× M2 standoff EXTRUSIONS (Ø7 × 5, clipped flush at the footprint edge)
    at the LILYGO pattern (±47.665, ±14.275). Stepped bore:
      Ø5.2 pocket from below through the plate — swallows the carrier's
        Ø4.5 M2 bosses (2 mm proud above the rim);
      Ø2.4 above through the extrusion — a long M2 ties
        LILYGO board → this lid → the carrier boss's own Ø2.4 channel.
    Board seat: 5 mm above the lid top (z = 8 from the rim).
  - Central rectangular cutout 94.98 (X) × 23.49 (Y) through the plate
    (battery / board-underside access, as on make_top.py).
  - The carrier's −Y wall openings sit below the rim — not blocked.

Print flat, extrusions UP. No supports.

Output: lilygo_sx1262_base_lid.stl
"""

from build123d import *
from pathlib import Path

# Carrier interface (from make_base_stacked.py)
BASE_L, BASE_W = 101.0, 65.0
CB_X, CB_Y     = 45.0, 27.0          # corner-boss centers
CB_CLEAR_D     = 3.4
M2_PX, M2_PY   = 95.33, 28.55        # M2 LILYGO boss pattern
M2_BOSS_D      = 4.5
M2_BOSS_H      = 5.0                 # carrier boss height above its rim

# Lid
LID_T          = 3.0
M3_CSK_D       = 6.0
M3_CSK_DEPTH   = 1.8
M2_PASS_D      = 5.2                 # lower pocket (swallows the proud boss)
M2_EXT_OD      = 7.0                 # standoff extrusion OD (clipped at edges)
M2_EXT_H       = 5.0                 # extrusion height above the lid top
M2_CLEAR_D     = 2.4                 # upper bore (M2 clearance)

# Central cutout — 94.98 base, trimmed asymmetrically along X:
# 7.4 off the −X side, 1.5 off the +X side → 86.08 long, center at +2.95.
CUT_TRIM_NEG   = 7.4
CUT_TRIM_POS   = 1.5
CUT_X          = 94.98 - CUT_TRIM_NEG - CUT_TRIM_POS   # 86.08
CUT_Y          = 23.49
CUT_XC         = (CUT_TRIM_NEG - CUT_TRIM_POS) / 2     # +2.95

OUT_DIR = Path(__file__).parent

# Sanity
assert CB_X + M3_CSK_D / 2 < BASE_L / 2, "Corner M3 csk exits the lid (X)"
assert CB_Y + M3_CSK_D / 2 < BASE_W / 2, "Corner M3 csk exits the lid (Y)"
assert LID_T >= M2_BOSS_H - LID_T, "Ø5.2 pocket (lid depth) must swallow the 2 mm proud boss"
assert CUT_XC + CUT_X / 2 + 1 < BASE_L / 2, "Central cutout exits the lid (+X)"
assert -(CUT_XC - CUT_X / 2) + 1 < BASE_L / 2, "Central cutout exits the lid (−X)"
assert CUT_Y / 2 + 1 < BASE_W / 2, "Central cutout exits the lid (Y)"
# cutout vs corner M3 csk
assert (CB_Y - CUT_Y / 2) - M3_CSK_D / 2 > 2, "Central cutout too close to a corner M3 csk"
# cutout corners vs M2 upper bores: the Ø2.4 channel wall must survive.
for _sx in (-1, 1):
    _edge_x = CUT_XC + _sx * CUT_X / 2
    _d_bore = ((_sx * M2_PX / 2 - _edge_x) ** 2 + (M2_PY / 2 - CUT_Y / 2) ** 2) ** 0.5
    assert _d_bore - M2_CLEAR_D / 2 > 1.0, "Central cutout breaches an M2 bore wall"


def build_lid() -> Part:
    lid = Box(BASE_L, BASE_W, LID_T, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M2 standoff extrusions above the top face (stepped bore).
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * M2_PX / 2, sy * M2_PY / 2
            lid += Pos(cx, cy, LID_T) * Cylinder(
                M2_EXT_OD / 2, M2_EXT_H,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            # lower pocket: swallows the carrier's proud boss
            lid -= Pos(cx, cy, -0.2) * Cylinder(
                M2_PASS_D / 2, LID_T + 0.2,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            # upper bore: M2 clearance through the extrusion
            lid -= Pos(cx, cy, LID_T - 0.1) * Cylinder(
                M2_CLEAR_D / 2, M2_EXT_H + 0.3,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Clip everything flush to the 101 × 65 footprint (the edge extrusions
    # would otherwise overhang by ~0.9 mm).
    lid &= Pos(0, 0, -1) * Box(
        BASE_L, BASE_W, LID_T + M2_EXT_H + 3,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M3 corner holes, csk on the top face.
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * CB_X, sy * CB_Y
            lid -= Pos(cx, cy, -0.2) * Cylinder(
                CB_CLEAR_D / 2, LID_T + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            lid -= Pos(cx, cy, LID_T - M3_CSK_DEPTH) * Cylinder(
                M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Central rectangular cutout through the plate (X-shifted by the trims).
    lid -= Pos(CUT_XC, 0, -0.2) * Box(
        CUT_X, CUT_Y, LID_T + M2_EXT_H + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    return lid


if __name__ == "__main__":
    part = build_lid()
    out = OUT_DIR / "lilygo_sx1262_base_lid.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Lid:        {BASE_L} × {BASE_W} × {LID_T} mm (+{M2_EXT_H} mm M2 extrusions)")
    print(f"  M3 corner:  4× Ø{CB_CLEAR_D} at (±{CB_X}, ±{CB_Y}), csk Ø{M3_CSK_D}×{M3_CSK_DEPTH} on top")
    print(f"  M2 standoffs: 4× Ø{M2_EXT_OD}×{M2_EXT_H} (edge-clipped) at "
          f"(±{M2_PX/2:.2f}, ±{M2_PY/2:.2f}); bore Ø{M2_PASS_D} below / Ø{M2_CLEAR_D} above")
    print(f"              board seat z = {LID_T + M2_EXT_H} above the carrier rim")
    print(f"  Cutout:     {CUT_X:.2f} × {CUT_Y} mm at X={CUT_XC:+.2f} "
          f"(−X trimmed {CUT_TRIM_NEG}, +X trimmed {CUT_TRIM_POS})")
    print(f"  Print flat, extrusions UP. No supports.")
