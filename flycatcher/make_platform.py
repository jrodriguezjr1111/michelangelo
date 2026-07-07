"""
Flycatcher platform with USB cable wrap-post underneath.

Top face: 65 × 56.1 mm mounting plate with 4× M3 clearance holes in a
57.6 × 49.18 mm rectangular pattern.
Underside: hollow cavity with central cylindrical post; cable wraps
around the post for organized coiling. Two side openings (37 × 7.8 mm)
on the ±X walls let the cable in and out.

Print orientation: top face DOWN on the bed (STL pre-flipped).
No supports needed.
"""

from build123d import *
from pathlib import Path

# =============================================================================
# Parameters
# =============================================================================

PLATE_L = 68.0          # X (length) — enlarged from 65 for edge clearance
PLATE_W = 60.0          # Y (width)  — enlarged from 56.1 for edge clearance
PLATE_H = 14.0          # Z total
TOP_T   = 3.0           # top plate thickness
WALL_T  = 2.5           # outer wall thickness

# M3 mounting pattern (rectangular, length-wise × width-wise)
M3_PATTERN_X = 57.6     # along length
M3_PATTERN_Y = 49.18    # along width
M3_CLEAR_D   = 3.4
M3_CSK_D     = 6.2
M3_CSK_DEPTH = 1.8

# Wrap post (central)
POST_D = 14.0
POST_H = PLATE_H - TOP_T

# Cable openings: 37 × 7.8 mm on ±X walls
CABLE_D       = 5.0
SLOT_W        = 37.0    # along the wall (Y axis)
SLOT_H        = 7.8     # along Z
SLOT_Z_CENTER = (PLATE_H - TOP_T) / 2  # centered in side wall
SLOT_Y_OFFSET = 0.0     # centered on wall (slot is 37 mm — fills most of 56.1 mm)

OUT_DIR = Path(__file__).parent


def build_platform() -> Part:
    body = Box(PLATE_L, PLATE_W, PLATE_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Hollow underside
    cavity = Pos(0, 0, 0) * Box(
        PLATE_L - 2 * WALL_T, PLATE_W - 2 * WALL_T, PLATE_H - TOP_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    body -= cavity

    # Central wrap post
    post = Pos(0, 0, 0) * Cylinder(
        POST_D / 2, POST_H,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    body += post

    # 4× M3 holes + countersink (rectangular pattern)
    hx, hy = M3_PATTERN_X / 2, M3_PATTERN_Y / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * hx, sy * hy
            thru = Pos(cx, cy, 0) * Cylinder(
                M3_CLEAR_D / 2, PLATE_H + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= thru
            csk = Pos(cx, cy, PLATE_H - M3_CSK_DEPTH) * Cylinder(
                M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= csk

    # Cable opening on +X wall
    slot1 = Pos(PLATE_L / 2 + 0.2, SLOT_Y_OFFSET, SLOT_Z_CENTER - SLOT_H / 2) * Box(
        WALL_T + 0.8, SLOT_W, SLOT_H,
        align=(Align.MAX, Align.CENTER, Align.MIN))
    body -= slot1

    # Cable opening on -X wall
    slot2 = Pos(-PLATE_L / 2 - 0.2, SLOT_Y_OFFSET, SLOT_Z_CENTER - SLOT_H / 2) * Box(
        WALL_T + 0.8, SLOT_W, SLOT_H,
        align=(Align.MIN, Align.CENTER, Align.MIN))
    body -= slot2

    return body


if __name__ == "__main__":
    part = build_platform()
    # Flip so top face sits on the bed
    part = Rot(180, 0, 0) * part
    part = Pos(0, 0, PLATE_H) * part
    out = OUT_DIR / "flycatcher_platform.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Plate: {PLATE_L} × {PLATE_W} × {PLATE_H} mm")
    print(f"  M3 holes: 4× Ø{M3_CLEAR_D} in {M3_PATTERN_X} × {M3_PATTERN_Y} mm rect pattern")
    print(f"            countersunk Ø{M3_CSK_D}×{M3_CSK_DEPTH} on top face")
    print(f"  Wrap post: Ø{POST_D} × {POST_H} mm")
    print(f"  Cable openings: {SLOT_W} × {SLOT_H} mm on ±X walls")
    edge_x = PLATE_L/2 - M3_PATTERN_X/2 - M3_CSK_D/2
    edge_y = PLATE_W/2 - M3_PATTERN_Y/2 - M3_CSK_D/2
    print(f"  M3 edge clearance: {edge_x:.2f} mm (X), {edge_y:.2f} mm (Y)")
    print(f"  Print top-face DOWN on bed. No supports.")
