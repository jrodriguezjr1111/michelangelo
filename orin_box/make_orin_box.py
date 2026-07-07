"""
NVIDIA Jetson Orin Nano stackable sensor box.

Two parts (print both):
  orin_box_base.stl  — tray with board standoffs, USB cutout, nesting foot
  orin_box_lid.stl   — lid with top pocket that receives the foot of the box above

Stacking:
  Each box's BOTTOM is a smaller rectangular foot. The LID's TOP has a matching
  pocket, so a box drops into the lid of the box below it. 4× M3 screws (2 per
  long side) clamp the lid to the base through side bosses.

Coordinate frame (origin = footprint center):
  X = board width (100). Y = elongated for USB cables (142). Z = build height.
"""

from build123d import *
from pathlib import Path

# =============================================================================
# Parameters
# =============================================================================
# Jetson Orin Nano dev-kit board (measured by user)
BOARD_X   = 100.0
BOARD_Y   = 81.0
HOLE_X    = 92.0          # mounting-hole rectangle
HOLE_Y    = 58.0
STANDOFF_D     = 6.0
STANDOFF_H     = 7.0      # board sits this high above the floor
STANDOFF_PILOT = 2.1      # M2.5 self-tap pilot
BOARD_Y_OFF    = -12.0    # shift board away from +Y (USB) wall for cable space

# Interior (Y elongated for USB cable clearance)
INNER_X   = 104.0
INNER_Y   = 142.0
INNER_H   = 40.0          # interior clear height (board + connectors)

WALL      = 3.0
FLOOR_T   = 3.0
LID_T     = 3.0

# Nesting foot (smaller bottom that drops into the lid pocket below)
FOOT_STEP = 6.0           # foot is inset this much per side from outer wall
FOOT_H    = 5.0
FIT_CLEAR = 0.4           # foot-to-pocket clearance per side

# Side joining screws (M3, 2 per long side -> 4 total)
SCREW_CLEAR_D = 3.4
SCREW_PILOT_D = 2.6       # self-tap into base boss
SCREW_HEAD_D  = 6.0
SCREW_HEAD_H  = 3.2
SCREW_BOSS_D  = 8.0
SCREW_Y       = 45.0      # ±Y position of the two screws on each side

# USB cable opening (on +Y end wall)
USB_W = 70.0
USB_H = 22.0

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived + sanity
# =============================================================================
OUTER_X = INNER_X + 2 * WALL
OUTER_Y = INNER_Y + 2 * WALL
FOOT_X  = OUTER_X - 2 * FOOT_STEP
FOOT_Y  = OUTER_Y - 2 * FOOT_STEP
BODY_H  = FLOOR_T + INNER_H        # base height above the foot
SCREW_X = OUTER_X / 2 - WALL / 2   # screw column centered in side wall

assert BOARD_X + 1.0 < INNER_X, "Board too wide for interior"
assert BOARD_Y + 1.0 < INNER_Y, "Board too long for interior"
assert HOLE_X < BOARD_X and HOLE_Y < BOARD_Y, "Hole pattern outside board"
assert SCREW_Y + SCREW_BOSS_D / 2 < INNER_Y / 2, "Screw bosses exit interior in Y"
assert USB_W + 2.0 < INNER_X, "USB opening wider than interior"
assert FOOT_X > 0 and FOOT_Y > 0, "Foot step too large"


# =============================================================================
# Base
# =============================================================================
def build_base() -> Part:
    # Nesting foot (z=0..FOOT_H), then full body on top.
    foot = Box(FOOT_X, FOOT_Y, FOOT_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))
    body = Pos(0, 0, FOOT_H) * Box(OUTER_X, OUTER_Y, BODY_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))
    part = foot + body

    # Hollow interior (leave FLOOR_T above the foot).
    cav_z = FOOT_H + FLOOR_T
    part -= Pos(0, 0, cav_z) * Box(INNER_X, INNER_Y, INNER_H + 1,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Board standoffs on the floor (4× at HOLE pattern).
    floor_top = FOOT_H + FLOOR_T
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Pos(sx * HOLE_X / 2, sy * HOLE_Y / 2 + BOARD_Y_OFF, floor_top)
            part += c * Cylinder(STANDOFF_D / 2, STANDOFF_H,
                                  align=(Align.CENTER, Align.CENTER, Align.MIN))
            part -= c * Pos(0, 0, STANDOFF_H - STANDOFF_H + 0.0) * Cylinder(
                STANDOFF_PILOT / 2, STANDOFF_H + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Side screw bosses + pilot holes (2 per long side).
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Pos(sx * SCREW_X, sy * SCREW_Y, FOOT_H)
            part += c * Cylinder(SCREW_BOSS_D / 2, BODY_H,
                                  align=(Align.CENTER, Align.CENTER, Align.MIN))
            part -= Pos(sx * SCREW_X, sy * SCREW_Y, FOOT_H + 2.0) * Cylinder(
                SCREW_PILOT_D / 2, BODY_H,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # USB opening on +Y end wall.
    usb_z = FOOT_H + FLOOR_T + STANDOFF_H
    part -= Pos(0, OUTER_Y / 2 - WALL / 2, usb_z) * Box(
        USB_W, WALL + 1, USB_H,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    return part


# =============================================================================
# Lid
# =============================================================================
def build_lid() -> Part:
    lid = Box(OUTER_X, OUTER_Y, LID_T,
              align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Top pocket that receives the foot of the box above.
    pocket_d = FOOT_H + 0.5
    lid -= Pos(0, 0, LID_T - pocket_d) * Box(
        FOOT_X + 2 * FIT_CLEAR, FOOT_Y + 2 * FIT_CLEAR, pocket_d + 0.1,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Locating lip on the underside (plugs into interior).
    lip_h = 3.0
    lid += Pos(0, 0, -lip_h) * Box(INNER_X - 0.6, INNER_Y - 0.6, lip_h,
              align=(Align.CENTER, Align.CENTER, Align.MIN))
    # keep lip a frame, not a solid plate
    lid -= Pos(0, 0, -lip_h) * Box(INNER_X - 0.6 - 2 * WALL,
              INNER_Y - 0.6 - 2 * WALL, lip_h + 0.1,
              align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Side screw clearance holes + head counterbore (top).
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Pos(sx * SCREW_X, sy * SCREW_Y, -0.1)
            lid -= c * Cylinder(SCREW_CLEAR_D / 2, LID_T + 0.2,
                                align=(Align.CENTER, Align.CENTER, Align.MIN))
            lid -= Pos(sx * SCREW_X, sy * SCREW_Y, LID_T - SCREW_HEAD_H) * Cylinder(
                SCREW_HEAD_D / 2, SCREW_HEAD_H + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return lid


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    base, lid = build_base(), build_lid()
    for name, part in (("orin_box_base", base), ("orin_box_lid", lid)):
        out = OUT_DIR / f"{name}.stl"
        export_stl(part, str(out))
        print(f"✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)")
    print(f"  Outer:    {OUTER_X} × {OUTER_Y} × {FOOT_H + BODY_H + LID_T} mm")
    print(f"  Interior: {INNER_X} × {INNER_Y} × {INNER_H} mm")
    print(f"  Foot:     {FOOT_X} × {FOOT_Y} × {FOOT_H} (inset {FOOT_STEP}/side)")
    print(f"  Board:    {BOARD_X} × {BOARD_Y}, holes {HOLE_X} × {HOLE_Y}")
    print(f"  Screws:   4× M3 side (X=±{SCREW_X:.1f}, Y=±{SCREW_Y})")
    print(f"  USB slot: {USB_W} × {USB_H} on +Y end")
