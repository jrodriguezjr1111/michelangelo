"""
GL.iNet hub mounting plate (inner / 60×37 boss pattern).

A 78 × 60 × 4 mm plate with 4 corner standoffs at 60 × 37 mm spacing for
8-32 bolts. Companion to glinet_plate (which had a 101.91 × 37 outer hub
pattern and a 60 × 37 inner case-mount pattern).
"""

from build123d import *
from pathlib import Path

PLATE_L = 78.0            # X
PLATE_W = 60.0            # Y
PLATE_T = 4.0             # Z

BOSS_SPACING_X = 60.0
BOSS_SPACING_Y = 37.0
STANDOFF_H    = 6.0
STANDOFF_OD   = 10.0
SCREW_CLEAR_D = 4.5       # 8-32 clearance

OUT_DIR = Path(__file__).parent

assert BOSS_SPACING_X + STANDOFF_OD <= PLATE_L, "Standoffs hang off long edge"
assert BOSS_SPACING_Y + STANDOFF_OD <= PLATE_W, "Standoffs hang off short edge"


def build_plate() -> Part:
    plate = Box(PLATE_L, PLATE_W, PLATE_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = sx * BOSS_SPACING_X / 2
            cy = sy * BOSS_SPACING_Y / 2
            boss = Cylinder(STANDOFF_OD / 2, STANDOFF_H,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            plate += Pos(cx, cy, PLATE_T) * boss
            thru = Cylinder(SCREW_CLEAR_D / 2, PLATE_T + STANDOFF_H + 0.4,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            plate -= Pos(cx, cy, -0.2) * thru

    return plate


def main() -> None:
    print("=" * 60)
    print("GL.iNet inner plate (60×37 bosses) — build123d")
    print("=" * 60)
    print(f"Plate:     {PLATE_L} × {PLATE_W} × {PLATE_T} mm")
    print(f"Standoffs: 4× Ø{STANDOFF_OD} × {STANDOFF_H} mm at "
          f"(±{BOSS_SPACING_X/2}, ±{BOSS_SPACING_Y/2})  "
          f"[spacing {BOSS_SPACING_X} × {BOSS_SPACING_Y}]")
    print(f"Bolt:      Ø{SCREW_CLEAR_D} clearance (8-32) through standoff + plate")

    plate = build_plate()
    out = OUT_DIR / "glinet_plate_inner.stl"
    export_stl(plate, str(out))
    print(f"\n  ✓ {out.name} ({out.stat().st_size:,} bytes)")
    print("Print orientation: plate flat on bed, standoffs UP. No supports.")


if __name__ == "__main__":
    main()
