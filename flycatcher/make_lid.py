"""
Flycatcher platform lid — recessed cover matching the platform footprint.

Same footprint and M3 pattern as the platform. Underside recess clears
the board and top-side components. One side cutout on the -X wall sized
37 × 7.8 mm for a USB (multi-port) connector.

Print orientation: top face DOWN on the bed. Recess faces up → no supports.
"""

from build123d import *
from pathlib import Path

# =============================================================================
# Parameters — kept in sync with make_platform.py
# =============================================================================

LID_L = 68.0
LID_W = 60.0
LID_H = 11.0          # TOP_T 3 + recess 8
TOP_T = 3.0
WALL_T = 2.5

M3_PATTERN_X = 57.6
M3_PATTERN_Y = 49.18
M3_CLEAR_D   = 3.4
M3_CSK_D     = 6.2
M3_CSK_DEPTH = 1.8

# Recess under the lid
RECESS_L = LID_L - 2 * WALL_T
RECESS_W = LID_W - 2 * WALL_T
RECESS_H = 8.0

# USB cutout on -X wall (spans along Y, centered by default)
USB_CUT_W = 37.0
USB_CUT_H = 7.8
USB_CUT_Y_CENTER = 0.0
USB_CUT_Z_CENTER = RECESS_H / 2   # centered vertically in the recess wall

OUT_DIR = Path(__file__).parent


def build_lid() -> Part:
    body = Box(LID_L, LID_W, LID_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Recess (full clearance for board + components)
    recess = Pos(0, 0, 0) * Box(
        RECESS_L, RECESS_W, RECESS_H,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    body -= recess

    # M3 clearance + countersink
    hx, hy = M3_PATTERN_X / 2, M3_PATTERN_Y / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * hx, sy * hy
            thru = Pos(cx, cy, 0) * Cylinder(
                M3_CLEAR_D / 2, LID_H + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= thru
            csk = Pos(cx, cy, LID_H - M3_CSK_DEPTH) * Cylinder(
                M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= csk

    # USB cutout on -X wall
    usb = Pos(-LID_L / 2 - 0.2, USB_CUT_Y_CENTER,
              USB_CUT_Z_CENTER - USB_CUT_H / 2) * Box(
        WALL_T + 0.8, USB_CUT_W, USB_CUT_H,
        align=(Align.MIN, Align.CENTER, Align.MIN))
    body -= usb

    return body


if __name__ == "__main__":
    part = build_lid()
    # Flip so top face sits on the bed
    part = Rot(180, 0, 0) * part
    part = Pos(0, 0, LID_H) * part
    out = OUT_DIR / "flycatcher_lid.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Lid: {LID_L} × {LID_W} × {LID_H} mm")
    print(f"  Recess: {RECESS_L} × {RECESS_W} × {RECESS_H} mm")
    print(f"  M3 holes: 4× Ø{M3_CLEAR_D} in {M3_PATTERN_X} × {M3_PATTERN_Y} mm rect pattern")
    print(f"            countersunk Ø{M3_CSK_D}×{M3_CSK_DEPTH} on top")
    print(f"  USB cutout: {USB_CUT_W} × {USB_CUT_H} mm on -X wall, centered")
    edge_x = LID_L/2 - M3_PATTERN_X/2 - M3_CSK_D/2
    edge_y = LID_W/2 - M3_PATTERN_Y/2 - M3_CSK_D/2
    print(f"  M3 edge clearance: {edge_x:.2f} mm (X), {edge_y:.2f} mm (Y)")
    print(f"  Print top-face DOWN. Recess faces up. No supports.")
