"""
LILYGO SX1262 868/915 MHz housing — I-beam with 18650 battery channel.

Outer envelope: 101 × 35 × 31 mm.
Cross-section (end view) is an I-beam: wide top and bottom flanges (35 mm)
with a narrower central web holding a Ø18.2 mm through-channel for an
18650 Li-ion cell (open at both ends for easy insertion and wiring).

Top flange: 4× M2 clearance holes matching the LILYGO mounting pattern
(95.33 mm × 28.55 mm).
Bottom flange: 4× M3 clearance + countersunk holes for mounting the
housing to a surface.

Print orientation: as modeled (bottom flange on the bed). Battery channel
runs horizontally along X, so it self-supports once past the equator; a
short stretch around the ceiling will bridge cleanly. No supports needed
for typical PLA settings on a well-tuned machine.
"""

from build123d import *
from pathlib import Path

# =============================================================================
# Overall envelope
# =============================================================================
LENGTH = 101.0          # X
WIDTH  = 35.0           # Y (flange width)
HEIGHT = 31.0           # Z

FLANGE_T = 4.0          # top & bottom flange thickness
WEB_W    = 28.0         # central web width (narrower than flanges → I profile)
WEB_H    = HEIGHT - 2 * FLANGE_T  # 23 mm

# =============================================================================
# 18650 battery U-cutout (Ø22 × 65 mm cell, with clearance)
# Opens upward through the top flange so the cell drops in from above and is
# retained by the LILYGO PCB mounted on top. End caps in the top flange keep
# the M2 mount points in solid material.
# =============================================================================
BATT_D = 22.2           # diameter clearance for Ø22 cell
CUTOUT_LENGTH = 75.0    # X-extent of the U-cutout (leaves end caps)
CUTOUT_FLOOR_Z = 4.0    # bottom of the U sits on top of the bottom flange

# =============================================================================
# LILYGO M2 mount pattern on TOP flange (board sits on top, screwed down)
# =============================================================================
M2_PATTERN_X = 95.33
M2_PATTERN_Y = 28.55
M2_CLEAR_D   = 2.4      # Ø clearance for M2
# No countersink — M2 screw head sits on top (edges too tight for csk).

# =============================================================================
# M3 mounting holes on BOTTOM flange (housing → surface)
# =============================================================================
M3_PATTERN_X = 90.0
M3_PATTERN_Y = 25.0
M3_CLEAR_D   = 3.4
M3_CSK_D     = 6.0      # countersunk on bottom face so heads sit flush
M3_CSK_DEPTH = 1.8

OUT_DIR = Path(__file__).parent


def build_housing() -> Part:
    # --- Top flange ---
    top = Pos(0, 0, HEIGHT - FLANGE_T) * Box(
        LENGTH, WIDTH, FLANGE_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # --- Bottom flange ---
    bottom = Pos(0, 0, 0) * Box(
        LENGTH, WIDTH, FLANGE_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # --- Central web (narrower, forms the I-shape) ---
    web = Pos(0, 0, FLANGE_T) * Box(
        LENGTH, WEB_W, WEB_H,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    body = top + bottom + web

    # --- U-shaped battery cutout (curved floor + slot opening through top) ---
    R = BATT_D / 2
    curve_cz = CUTOUT_FLOOR_Z + R
    # Half-cylinder (gives the rounded floor of the U)
    curve = Pos(0, 0, curve_cz) * Rot(0, 90, 0) * Cylinder(
        R, CUTOUT_LENGTH,
        align=(Align.CENTER, Align.CENTER, Align.CENTER))
    # Rectangular slot from curve center up through the top flange
    slot = Pos(0, 0, curve_cz) * Box(
        CUTOUT_LENGTH, BATT_D, HEIGHT - curve_cz + 1.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    body -= curve
    body -= slot

    # --- M2 mount holes through top flange ---
    hx, hy = M2_PATTERN_X / 2, M2_PATTERN_Y / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * hx, sy * hy
            hole = Pos(cx, cy, HEIGHT - FLANGE_T - 0.2) * Cylinder(
                M2_CLEAR_D / 2, FLANGE_T + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= hole

    # --- M3 mount holes through bottom flange, countersunk from below ---
    hx, hy = M3_PATTERN_X / 2, M3_PATTERN_Y / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * hx, sy * hy
            thru = Pos(cx, cy, -0.2) * Cylinder(
                M3_CLEAR_D / 2, FLANGE_T + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= thru
            csk = Pos(cx, cy, 0) * Cylinder(
                M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= csk

    return body


if __name__ == "__main__":
    part = build_housing()
    out = OUT_DIR / "lilygo_sx1262_housing.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Envelope: {LENGTH} × {WIDTH} × {HEIGHT} mm")
    print(f"  Flanges: {FLANGE_T} mm each, web: {WEB_W} × {WEB_H} mm")
    print(f"  Battery U-cutout: Ø{BATT_D} × {CUTOUT_LENGTH} mm, opens through top flange")
    print(f"  M2 top holes: 4× Ø{M2_CLEAR_D} at {M2_PATTERN_X} × {M2_PATTERN_Y} mm")
    print(f"  M3 bottom holes: 4× Ø{M3_CLEAR_D} at {M3_PATTERN_X} × {M3_PATTERN_Y} mm, csk Ø{M3_CSK_D}×{M3_CSK_DEPTH}")
    # Edge checks
    m2_edge_x = LENGTH/2 - M2_PATTERN_X/2 - M2_CLEAR_D/2
    m2_edge_y = WIDTH/2  - M2_PATTERN_Y/2 - M2_CLEAR_D/2
    m3_edge_x = LENGTH/2 - M3_PATTERN_X/2 - M3_CSK_D/2
    m3_edge_y = WIDTH/2  - M3_PATTERN_Y/2 - M3_CSK_D/2
    print(f"  M2 edge clearance: {m2_edge_x:.2f} (X), {m2_edge_y:.2f} (Y) mm")
    print(f"  M3 edge clearance: {m3_edge_x:.2f} (X), {m3_edge_y:.2f} (Y) mm")
    # Battery/web clearance
    side_wall = (WEB_W - BATT_D) / 2
    end_cap  = (LENGTH - CUTOUT_LENGTH) / 2
    print(f"  Web wall around battery: {side_wall:.2f} mm per side")
    print(f"  Top-flange end caps: {end_cap:.2f} mm at each end")
