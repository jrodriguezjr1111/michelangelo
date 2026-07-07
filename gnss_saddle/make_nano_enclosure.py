"""
Jetson Nano enclosure that bolts on TOP of the GNSS dual-tube saddle
(make_gnss_saddle.py) using the saddle's existing 4× M4 screw pattern.

Base tray:
  - Floor mates flat on the saddle's top face; cavity opens UP.
  - Perimeter walls around the Jetson Nano dev-kit board.
  - 4 board standoffs at the Nano's 86.14 × 58.25 mm hole pattern (M3 self-tap).
  - 4 M4 through-holes at the saddle's ±18 mm bolt pattern. Longer M4 screws drop
    in from the cavity, clamp the two saddle halves AND fasten the enclosure
    (head sits on the floor, under the board which clears it on the standoffs).
  - Central Ø20 cable passthrough aligned with the saddle's Ø30 GNSS hole.
  - One open-top I/O notch on a long (+X) wall (placeholder for the real ports).

Coordinate frame (assembled == print orientation):
  X = along the saddle tube axis, Y = across (board long axis), Z = up.
  z=0 = floor underside (on the saddle top); cavity opens UP.

Print: floor on the bed, no supports.

Output: nano_enclosure.stl   (base tray; lid + exact port cutouts TBD)
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

# Jetson Nano dev-kit board
BOARD_X = 80.0          # board short dim (along saddle X)
BOARD_Y = 100.0         # board long dim (along saddle Y)
HOLE_X  = 58.25         # mount-hole spacing (X)
HOLE_Y  = 86.14         # mount-hole spacing (Y)
STANDOFF_OD    = 6.0
STANDOFF_H     = 8.0    # board sits this high above the floor (clears M4 heads)
STANDOFF_PILOT = 2.5    # M3 self-tap pilot

# Enclosure shell
CLEAR   = 2.0           # board-to-wall clearance per side
WALL_T  = 2.5
FLOOR_T = 3.0
WALL_H  = 20.0          # wall height above the floor

INNER_X = BOARD_X + 2 * CLEAR        # 84
INNER_Y = BOARD_Y + 2 * CLEAR        # 104
OUTER_X = INNER_X + 2 * WALL_T       # 89
OUTER_Y = INNER_Y + 2 * WALL_T       # 109
ENC_H   = FLOOR_T + WALL_H           # 23

# Saddle mount interface (from make_gnss_saddle.py)
M4_PAT     = 18.0       # ±X and ±Y
M4_CLEAR_D = 4.4

# Central cable passthrough (aligned with the saddle's Ø30 GNSS hole)
PASS_D = 20.0

# I/O notch (open-top placeholder) on the +X long wall
IO_W  = 60.0            # along Y
IO_Z0 = 5.0             # notch starts this high above the floor

OUT_DIR = Path(__file__).parent

# =============================================================================
# Sanity
# =============================================================================
assert HOLE_X / 2 + STANDOFF_OD / 2 < INNER_X / 2, "Standoffs exit cavity in X"
assert HOLE_Y / 2 + STANDOFF_OD / 2 < INNER_Y / 2, "Standoffs exit cavity in Y"
assert M4_PAT + M4_CLEAR_D / 2 + 1.0 < OUTER_X / 2, "M4 holes exit floor in X"
assert M4_PAT + M4_CLEAR_D / 2 + 1.0 < OUTER_Y / 2, "M4 holes exit floor in Y"
assert (M4_PAT**2 + M4_PAT**2) ** 0.5 - M4_CLEAR_D / 2 - PASS_D / 2 > 1.0, "M4 hole clashes passthrough"
assert STANDOFF_H > 5.0, "Standoff too short to clear an M4 cap head"
assert IO_W / 2 < INNER_Y / 2, "I/O notch wider than the wall"


# =============================================================================
# Build
# =============================================================================

def build_enclosure() -> Part:
    body = Box(OUTER_X, OUTER_Y, ENC_H, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Hollow cavity (opens up)
    body -= Pos(0, 0, FLOOR_T) * Box(
        INNER_X, INNER_Y, WALL_H + 0.1, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Board standoffs (M3 self-tap), with pilot holes
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Pos(sx * HOLE_X / 2, sy * HOLE_Y / 2, FLOOR_T)
            body += c * Cylinder(STANDOFF_OD / 2, STANDOFF_H,
                                 align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= c * Cylinder(STANDOFF_PILOT / 2, STANDOFF_H + 0.1,
                                 align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M4 saddle-mount through-holes (floor)
    for sx in (-1, 1):
        for sy in (-1, 1):
            body -= Pos(sx * M4_PAT, sy * M4_PAT, -0.1) * Cylinder(
                M4_CLEAR_D / 2, FLOOR_T + 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Central cable passthrough (floor)
    body -= Pos(0, 0, -0.1) * Cylinder(
        PASS_D / 2, FLOOR_T + 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # I/O notch on +X wall (open to the top rim — placeholder for real ports)
    body -= Pos(OUTER_X / 2 + 0.5, 0, FLOOR_T + IO_Z0) * Box(
        WALL_T + 1.2, IO_W, WALL_H,  # extends past the top rim
        align=(Align.MAX, Align.CENTER, Align.MIN))

    return body


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("Jetson Nano enclosure — mounts on the GNSS saddle (M4)")
    print("=" * 60)
    print(f"Outer:        {OUTER_X} × {OUTER_Y} × {ENC_H} mm "
          f"(floor {FLOOR_T}, walls {WALL_T}, wall H {WALL_H})")
    print(f"Cavity:       {INNER_X} × {INNER_Y} × {WALL_H} mm")
    print(f"Board:        {BOARD_X} × {BOARD_Y}; holes {HOLE_X} × {HOLE_Y}")
    print(f"Standoffs:    4× ⌀{STANDOFF_OD} × {STANDOFF_H} mm, {STANDOFF_PILOT} pilot (M3 self-tap)")
    print(f"Saddle mount: 4× Ø{M4_CLEAR_D} (M4) at (±{M4_PAT}, ±{M4_PAT}) — matches the saddle bolts")
    print(f"Passthrough:  Ø{PASS_D} central (over the saddle's Ø30 GNSS hole)")
    print(f"I/O notch:    {IO_W} mm on +X wall (placeholder)")
    print()

    enc = build_enclosure()
    out = OUT_DIR / "nano_enclosure.stl"
    export_stl(enc, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)")
    print("\nPrint floor-down, no supports. Mounts to the saddle with 4× longer M4 screws")
    print("(through the floor + both saddle halves; nut in the saddle's bottom counterbore).")


if __name__ == "__main__":
    main()
