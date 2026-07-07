"""
X-shaped Jetson Nano adapter base for the GNSS dual-tube saddle.

Four arms radiate from the center to the Jetson Nano's mount holes
(58.25 × 86.14 → ±29.13, ±43.07). Each arm carries one of the saddle's M4
clamp bolts at (±18, ±18): Ø4.4 clearance with a Ø8 × 4.5 head/nut
counterbore sunk into a raised Ø12 × 4 boss (extrusion) — long M4 screws
clamp this base + both saddle halves in one stack.

  Plate:    4 arms, 20 wide × 4 thick (X-shape, ~110 × 96 envelope)
  M4:       4× Ø4.4 at (±18, ±18); cb Ø8 × 4.5 in Ø12 × 4 bosses
            (M4 points sit 4.8 mm off the arm axis → Ø14 pads in the plate)
  Nano:     4× Ø6 × 6 standoffs, Ø2.5 pilot (M3 self-tap) at arm ends
            (board bottom at z=10 clears the M4 boss tops at z=8)

NOTE: the arms cross over the saddle's central Ø30 GNSS hole — tell me if a
center passthrough is needed.

Print flat. No supports.

Output: nano_xbase.stl
"""

from build123d import *
from math import atan2, degrees, hypot
from pathlib import Path

# Jetson Nano mount pattern (this frame: 58.25 across X, 86.14 across Y)
NANO_HX, NANO_HY = 58.25, 86.14
NANO_X, NANO_Y   = NANO_HX / 2, NANO_HY / 2          # ±29.13, ±43.07

# Saddle M4 interface (make_gnss_saddle.py clamp bolts)
M4_P       = 18.0          # ± both axes
M4_CLEAR_D = 4.4
M4_CB_D    = 8.0
M4_CB_DEPTH = 4.5
M4_BOSS_OD = 12.0
M4_BOSS_H  = 4.0           # extrusion above the plate
M4_PAD_OD  = 14.0          # plate-level pad under each boss

# Plate / arms
PLATE_T  = 4.0
ARM_W    = 20.0
ARM_LEN  = hypot(NANO_X, NANO_Y) + 6.0               # past the Nano hole

# Nano standoffs
SO_OD, SO_H, SO_PILOT = 6.0, 6.0, 2.5                # M3 self-tap

BOARD_T = 1.6

OUT_DIR = Path(__file__).parent

# Derived: M4 off-axis distance from the arm centerline
_arm_len0 = hypot(NANO_X, NANO_Y)
_offaxis = abs(M4_P * NANO_Y - M4_P * NANO_X) / _arm_len0    # ≈4.83

# Sanity
assert _offaxis + M4_CB_D / 2 < ARM_W / 2, "M4 counterbore exits the arm"
assert _offaxis + M4_BOSS_OD / 2 < ARM_W / 2 + M4_PAD_OD / 2 - 2, \
    "M4 boss unsupported (enlarge pad or arm)"
assert M4_CB_DEPTH < PLATE_T + M4_BOSS_H - 1, "Counterbore punches through"
assert SO_H + PLATE_T > M4_BOSS_H + PLATE_T + 1, "Board would sit on the M4 bosses"
assert M4_CLEAR_D < M4_CB_D < M4_BOSS_OD, "M4 hole stack inconsistent"


def build_xbase() -> Part:
    part = None
    # 4 arms from the center toward each Nano hole
    for sx in (-1, 1):
        for sy in (-1, 1):
            ang = degrees(atan2(sy * NANO_Y, sx * NANO_X))
            arm = Rot(0, 0, ang) * Pos(ARM_LEN / 2, 0, 0) * Box(
                ARM_LEN, ARM_W, PLATE_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            part = arm if part is None else part + arm

    # Plate-level pads + raised bosses at the M4 points
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Pos(sx * M4_P, sy * M4_P, 0)
            part += c * Cylinder(M4_PAD_OD / 2, PLATE_T,
                                 align=(Align.CENTER, Align.CENTER, Align.MIN))
            part += Pos(sx * M4_P, sy * M4_P, PLATE_T) * Cylinder(
                M4_BOSS_OD / 2, M4_BOSS_H,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            # Ø4.4 through + Ø8 × 4.5 counterbore from the boss top
            part -= Pos(sx * M4_P, sy * M4_P, -0.2) * Cylinder(
                M4_CLEAR_D / 2, PLATE_T + M4_BOSS_H + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            part -= Pos(sx * M4_P, sy * M4_P,
                        PLATE_T + M4_BOSS_H - M4_CB_DEPTH) * Cylinder(
                M4_CB_D / 2, M4_CB_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Nano standoffs at the arm ends
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Pos(sx * NANO_X, sy * NANO_Y, PLATE_T)
            part += c * Cylinder(SO_OD / 2, SO_H,
                                 align=(Align.CENTER, Align.CENTER, Align.MIN))
            part -= c * Cylinder(SO_PILOT / 2, SO_H + 0.1,
                                 align=(Align.CENTER, Align.CENTER, Align.MIN))

    return part


if __name__ == "__main__":
    part = build_xbase()
    out = OUT_DIR / "nano_xbase.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  X-plate:   4 arms {ARM_W} wide × {PLATE_T} thick, "
          f"envelope ≈{2*(NANO_X+6):.0f} × {2*(NANO_Y+6):.0f} mm")
    print(f"  M4:        4× Ø{M4_CLEAR_D} at (±{M4_P}, ±{M4_P}); cb Ø{M4_CB_D}×{M4_CB_DEPTH} "
          f"in Ø{M4_BOSS_OD}×{M4_BOSS_H} bosses (pad Ø{M4_PAD_OD}; {_offaxis:.2f} mm off-axis)")
    print(f"  Nano:      4× Ø{SO_OD}×{SO_H} standoffs, Ø{SO_PILOT} pilot (M3 self-tap) "
          f"at (±{NANO_X:.2f}, ±{NANO_Y:.2f})")
    print(f"  Board bottom z={PLATE_T+SO_H} clears M4 boss tops z={PLATE_T+M4_BOSS_H} "
          f"by {SO_H-M4_BOSS_H:.0f} mm")
    print(f"  Long M4s clamp: this base → saddle top half → saddle bottom half.")
    print(f"  Print flat. No supports.")
