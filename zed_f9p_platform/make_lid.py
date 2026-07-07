"""
ZED-F9P platform lid — recessed cover.

Same 60 × 60 mm footprint and 37.6 mm M3 pattern as the platform.
Underside has a recess that clears the ZED-F9P board + components
(~8 mm tall). A side cutout on the -X wall aligns with the USB
connector on the board (18 mm from one edge, 10 mm wide).

Print orientation: top face DOWN on the bed (same as platform).
No supports required — recess faces up during printing.
"""

from build123d import *
from pathlib import Path

# =============================================================================
# Parameters
# =============================================================================

LID_L = 60.0            # X
LID_W = 60.0            # Y
LID_H = 11.0            # Z total (TOP_T 3 + recess 8)
TOP_T = 3.0             # solid cover thickness
WALL_T = 2.5            # outer wall thickness (around recess)

# M3 hole pattern — matches platform
M3_PATTERN   = 37.6
M3_CLEAR_D   = 3.4
M3_CSK_D     = 6.2
M3_CSK_DEPTH = 1.8

# Recess (clears the board and top-side components)
BOARD_CLEAR_L = LID_L - 2 * WALL_T   # 55 mm
BOARD_CLEAR_W = LID_W - 2 * WALL_T   # 55 mm
BOARD_CLEAR_H = 8.0                  # component clearance

# USB connector cutout in the -X wall
# "18 mm from one side, 10 mm wide" — placed on the +Y side of the wall
USB_CUT_W = 10.0                             # Y extent
USB_CUT_H = BOARD_CLEAR_H                    # full recess height
USB_CUT_Y_CENTER = LID_W / 2 - 18.0 - USB_CUT_W / 2  # = +7 mm

OUT_DIR = Path(__file__).parent


def build_lid() -> Part:
    body = Box(LID_L, LID_W, LID_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Recess on the underside (z=0 up to BOARD_CLEAR_H)
    recess = Pos(0, 0, 0) * Box(
        BOARD_CLEAR_L, BOARD_CLEAR_W, BOARD_CLEAR_H,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    body -= recess

    # M3 clearance holes + countersink on top face
    half = M3_PATTERN / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * half, sy * half
            thru = Pos(cx, cy, 0) * Cylinder(
                M3_CLEAR_D / 2, LID_H + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= thru
            csk = Pos(cx, cy, LID_H - M3_CSK_DEPTH) * Cylinder(
                M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= csk

    # USB cutout through the -X wall (opens to the recess interior)
    usb = Pos(-LID_L / 2 - 0.2, USB_CUT_Y_CENTER, 0) * Box(
        WALL_T + 0.8, USB_CUT_W, USB_CUT_H,
        align=(Align.MIN, Align.CENTER, Align.MIN))
    body -= usb

    return body


if __name__ == "__main__":
    part = build_lid()
    # Flip so the top (mount) face sits on the bed for printing
    part = Rot(180, 0, 0) * part
    part = Pos(0, 0, LID_H) * part
    out = OUT_DIR / "zed_f9p_lid.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Lid: {LID_L} × {LID_W} × {LID_H} mm")
    print(f"  Top thickness: {TOP_T} mm, walls: {WALL_T} mm")
    print(f"  Recess: {BOARD_CLEAR_L} × {BOARD_CLEAR_W} × {BOARD_CLEAR_H} mm (board clearance)")
    print(f"  M3 holes: 4× Ø{M3_CLEAR_D} in {M3_PATTERN} mm square pattern")
    print(f"            countersunk Ø{M3_CSK_D}×{M3_CSK_DEPTH} on top face")
    print(f"  USB cutout: {USB_CUT_W} × {USB_CUT_H} mm on -X wall, Y-center = {USB_CUT_Y_CENTER:+.1f}")
    print(f"  Print top-face DOWN on bed (recess faces up). No supports.")
