"""
Top cover (lid) for the GNSS enclosure (make_gnss_enclosure.py).

In service the enclosure hangs UNDER the saddle's +Y wing — mount face on
TOP, cavity opens DOWNWARD. This lid closes that downward-facing opening.

Geometry:
  • Outer footprint matches the enclosure: 52 × 52 mm.
  • Recessed lip (LIP_T thick) drops into the 47 × 47 mm cavity with a
    snug friction fit (lip outer = cavity − 2 × FIT_GAP).
  • Top of lid is flush with the enclosure's bottom face.

Print orientation: lip-up. No supports.
"""

from pathlib import Path
from build123d import Align, Box, Cylinder, Part, Pos, export_stl

# Match the enclosure --------------------------------------------------------
ENC_L = 52.0
ENC_W = 52.0
WALL_T = 2.5
CAV_L = ENC_L - 2 * WALL_T   # 47.0
CAV_W = ENC_W - 2 * WALL_T   # 47.0

# Lid -----------------------------------------------------------------------
PLATE_T = 2.5     # outer flange thickness
LIP_T   = 2.0     # lip protrusion height into cavity
FIT_GAP = 0.20    # per-side clearance between lip and cavity wall (snug FF)

LIP_L = CAV_L - 2 * FIT_GAP   # 46.6
LIP_W = CAV_W - 2 * FIT_GAP   # 46.6

# 4× M3 clearance holes — SAME dimensions/pattern as the saddle's ZED-F9P
# csk holes and the enclosure floor's mount holes. Holes pass through both
# the flange and the lip.
M3_PATTERN = 37.6
M3_CLEAR_D = 3.4

OUT_DIR = Path(__file__).parent

# Sanity --------------------------------------------------------------------
assert PLATE_T >= 1.6, "Lid too thin"
assert LIP_T >= 1.0,  "Lip too short for reliable friction fit"
assert LIP_L < CAV_L and LIP_W < CAV_W, "Lip must fit inside cavity"
assert LIP_L > CAV_L - 1.0, "Lip too loose (gap > 0.5 mm per side)"
assert M3_PATTERN / 2 + M3_CLEAR_D / 2 + 1.0 < LIP_L / 2, \
    "M3 holes too close to lip edge — thin wall risk"

# Geometry ------------------------------------------------------------------

def build_lid() -> Part:
    plate = Box(ENC_L, ENC_W, PLATE_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
    lip = Box(LIP_L, LIP_W, LIP_T,
              align=(Align.CENTER, Align.CENTER, Align.MIN))
    lip = Pos(0, 0, PLATE_T) * lip
    body = plate + lip

    # 4× M3 Ø3.4 clearance holes at 37.6 mm sq (same as ZED / enclosure floor),
    # through the full lid (flange + lip).
    half = M3_PATTERN / 2
    total_h = PLATE_T + LIP_T
    for sx in (-1, 1):
        for sy in (-1, 1):
            body -= Pos(sx * half, sy * half, -0.2) * Cylinder(
                M3_CLEAR_D / 2, total_h + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
    return body


if __name__ == "__main__":
    part = build_lid()
    out = OUT_DIR / "gnss_enclosure_lid.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print("=" * 64)
    print("GNSS enclosure top cover — build123d")
    print("=" * 64)
    print(f"  Outer:      {ENC_L} × {ENC_W} × {PLATE_T} mm flange")
    print(f"  Lip:        {LIP_L} × {LIP_W} × {LIP_T} mm "
          f"(cavity {CAV_L} × {CAV_W}, gap {FIT_GAP} mm/side)")
    print(f"  Total H:    {PLATE_T + LIP_T} mm")
    print(f"  Mount:      4× M3 Ø{M3_CLEAR_D} at {M3_PATTERN} mm sq "
          f"(matches ZED / enclosure floor)")
    print(f"  ✓ {out.name}  ({kb:.0f} KB)")
    print("\nPrint lip-UP, flange on the bed. Friction-fit into the cavity")
    print("opening of gnss_enclosure.stl. Cable cutouts clear the lid.")
