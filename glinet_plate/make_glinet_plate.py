"""
GL.iNet WiFi hub mounting plate.

A 122 × 78 × 4 mm plate that bolts to the OUTSIDE of a Pelican case using 4
inner 8-32 flat-head screws (countersunk on top), and supports the GL.iNet
hub on 4 corner standoffs that accept 8-32 bolts from below.

Coordinate frame:
  X = long axis (122 mm)
  Y = short axis (78 mm)
  Z = build direction; z=0 is the bed (bottom face of plate)
"""

from build123d import *
from pathlib import Path

# Plate
PLATE_L = 122.0           # X
PLATE_W = 78.0            # Y
PLATE_T = 4.0             # Z

# GL.iNet bolt extrusions (corner standoffs on top face)
HUB_SPACING_X = 101.91    # along long axis (between hub bolt centers)
HUB_SPACING_Y = 37.0      # along short axis
STANDOFF_H    = 6.0       # above plate top
STANDOFF_OD   = 10.0      # outer Ø of standoff boss

# Pelican case mount holes (inner pattern, through plate, countersunk top)
CASE_SPACING_X = 60.0
CASE_SPACING_Y = 37.0

# 8-32 hardware
# Major Ø 4.17 mm.  Use Ø4.5 clearance through-holes.
SCREW_CLEAR_D = 4.5
# 82° flat-head Ø is ~8.0 mm for 8-32; allow Ø8.4 for a clean countersink.
CSK_TOP_D    = 8.4
CSK_ANGLE    = 82.0       # degrees, included angle (flat-head 8-32 spec)

OUT_DIR = Path(__file__).parent

# Sanity
assert HUB_SPACING_X + STANDOFF_OD <= PLATE_L, "Standoffs hang off long edge"
assert HUB_SPACING_Y + STANDOFF_OD <= PLATE_W, "Standoffs hang off short edge"
assert CASE_SPACING_X < HUB_SPACING_X, "Inner mount pattern must be inside hub pattern"


def _csk_depth(top_d: float, shank_d: float, angle_deg: float) -> float:
    """Countersink axial depth so cone of given included angle meets shank Ø."""
    import math
    half = math.radians(angle_deg / 2)
    return (top_d - shank_d) / 2 / math.tan(half)


def build_plate() -> Part:
    plate = Box(PLATE_L, PLATE_W, PLATE_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # --- Corner standoffs for the GL.iNet hub (above the plate) ---
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = sx * HUB_SPACING_X / 2
            cy = sy * HUB_SPACING_Y / 2
            boss = Cylinder(STANDOFF_OD / 2, STANDOFF_H,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            boss = Pos(cx, cy, PLATE_T) * boss
            plate += boss
            # Clearance hole through standoff + plate
            thru = Cylinder(SCREW_CLEAR_D / 2, PLATE_T + STANDOFF_H + 0.4,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            thru = Pos(cx, cy, -0.2) * thru
            plate -= thru

    # --- Pelican case mount holes (inner pattern), countersunk on TOP face ---
    csk_depth = _csk_depth(CSK_TOP_D, SCREW_CLEAR_D, CSK_ANGLE)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = sx * CASE_SPACING_X / 2
            cy = sy * CASE_SPACING_Y / 2
            # Through clearance hole
            thru = Cylinder(SCREW_CLEAR_D / 2, PLATE_T + 0.4,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            thru = Pos(cx, cy, -0.2) * thru
            plate -= thru
            # Countersink cone on top face (apex points down into plate)
            csk = Cone(CSK_TOP_D / 2, SCREW_CLEAR_D / 2, csk_depth,
                       align=(Align.CENTER, Align.CENTER, Align.MAX))
            csk = Pos(cx, cy, PLATE_T + 0.001) * csk
            plate -= csk

    return plate


def main() -> None:
    print("=" * 60)
    print("GL.iNet hub mounting plate — build123d")
    print("=" * 60)
    print(f"Plate:        {PLATE_L} × {PLATE_W} × {PLATE_T} mm")
    print(f"Standoffs:    4× Ø{STANDOFF_OD} × {STANDOFF_H} mm "
          f"at (±{HUB_SPACING_X/2:.2f}, ±{HUB_SPACING_Y/2:.2f})  "
          f"[spacing {HUB_SPACING_X} × {HUB_SPACING_Y}]")
    print(f"Hub holes:    Ø{SCREW_CLEAR_D} clearance (8-32) through standoff + plate")
    print(f"Case holes:   Ø{SCREW_CLEAR_D} clearance, Ø{CSK_TOP_D} × 82° countersink on TOP "
          f"at (±{CASE_SPACING_X/2:.1f}, ±{CASE_SPACING_Y/2:.1f})  "
          f"[spacing {CASE_SPACING_X} × {CASE_SPACING_Y}]")

    plate = build_plate()
    out = OUT_DIR / "glinet_plate.stl"
    export_stl(plate, str(out))
    print(f"\n  ✓ {out.name} ({out.stat().st_size:,} bytes)")
    print("\nPrint orientation: plate flat on bed (standoffs UP). No supports needed.")
    print("Hardware: 4× 8-32 flat-head (case mount), 4× 8-32 bolts (hub mount).")


if __name__ == "__main__":
    main()
