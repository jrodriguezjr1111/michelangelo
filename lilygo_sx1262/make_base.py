"""
LILYGO SX1262 housing — BASE piece (split design, part 2 of 2).

Open-top box that mates with the top plate (lilygo_sx1262_top.stl).
  Outer:   101 × 40 × 27 mm  (with the 4 mm top plate → 31 mm total)
  Walls:   3 mm; floor: 4 mm
  Cavity:  95 × 34 × 23 mm (holds the 18650 cell + wiring)

Features:
  - 4× M3 countersunk holes through the floor (mount the housing to a
    surface) at the original 90 × 25 mm pattern.
  - 4× internal bosses (Ø6) at 70 × 32 mm with M3 self-tap pilot holes
    drilled from the top edge — receives the M3 screws coming down
    through the top plate's countersinks.
  - USB cutouts (11 × 6 mm) centered on both end walls.
"""

from build123d import *
from pathlib import Path

# =============================================================================
# Envelope
# =============================================================================
BASE_L = 101.0          # X
BASE_W = 40.0           # Y
BASE_H = 27.0           # Z (so total stacked height = 31 mm with 4 mm top)

WALL_T  = 3.0
FLOOR_T = 4.0

CAV_L = BASE_L - 2 * WALL_T   # 95
CAV_W = BASE_W - 2 * WALL_T   # 34
CAV_H = BASE_H - FLOOR_T      # 23

# =============================================================================
# M3 surface-mount holes on bottom (housing → surface)
# =============================================================================
M3_BOT_PX = 90.0
M3_BOT_PY = 25.0
M3_BOT_CLEAR_D   = 3.4
M3_BOT_CSK_D     = 6.0
M3_BOT_CSK_DEPTH = 1.8

# =============================================================================
# M3 attach (top plate → base) — pilot holes in internal bosses
# =============================================================================
M3_TOP_PX     = 70.0    # must match make_top.py
M3_TOP_PY     = 32.0
M3_PILOT_D    = 2.7     # self-tap pilot for M3 in PLA
M3_PILOT_DEPTH = 12.0
BOSS_OD       = 6.0

# =============================================================================
# USB-C cutouts on both end walls
# =============================================================================
USB_W        = 11.0     # along Y
USB_H        = 6.0      # along Z
USB_Z_CENTER = BASE_H / 2

OUT_DIR = Path(__file__).parent


def build_base() -> Part:
    # Solid outer block
    body = Box(BASE_L, BASE_W, BASE_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Hollow inner cavity (open top)
    cavity = Pos(0, 0, FLOOR_T) * Box(
        CAV_L, CAV_W, CAV_H + 1.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    body -= cavity

    # Internal bosses with M3 self-tap pilot holes
    hx, hy = M3_TOP_PX / 2, M3_TOP_PY / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * hx, sy * hy
            body += Pos(cx, cy, FLOOR_T) * Cylinder(
                BOSS_OD / 2, CAV_H,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= Pos(cx, cy, BASE_H - M3_PILOT_DEPTH) * Cylinder(
                M3_PILOT_D / 2, M3_PILOT_DEPTH + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # M3 surface-mount holes through floor (countersunk from below)
    hx, hy = M3_BOT_PX / 2, M3_BOT_PY / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * hx, sy * hy
            body -= Pos(cx, cy, -0.2) * Cylinder(
                M3_BOT_CLEAR_D / 2, FLOOR_T + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= Pos(cx, cy, 0) * Cylinder(
                M3_BOT_CSK_D / 2, M3_BOT_CSK_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # USB cutouts on both end walls
    for sx in (-1, 1):
        body -= Pos(sx * (BASE_L / 2 - WALL_T / 2), 0, USB_Z_CENTER) * Box(
            WALL_T + 1.0, USB_W, USB_H,
            align=(Align.CENTER, Align.CENTER, Align.CENTER))

    return body


if __name__ == "__main__":
    part = build_base()
    out = OUT_DIR / "lilygo_sx1262_base.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Base outer: {BASE_L} × {BASE_W} × {BASE_H} mm")
    print(f"  Cavity:     {CAV_L} × {CAV_W} × {CAV_H} mm (open top)")
    print(f"  Walls: {WALL_T} mm; floor: {FLOOR_T} mm")
    print(f"  M3 surface mount: 4× Ø{M3_BOT_CLEAR_D} at {M3_BOT_PX} × {M3_BOT_PY}, csk Ø{M3_BOT_CSK_D}×{M3_BOT_CSK_DEPTH}")
    print(f"  M3 top attach: 4× Ø{M3_PILOT_D} pilot ×{M3_PILOT_DEPTH} in Ø{BOSS_OD} bosses at {M3_TOP_PX} × {M3_TOP_PY}")
    print(f"  USB cutouts: {USB_W} × {USB_H} mm at Z center {USB_Z_CENTER} on both ends")
    # Clearance checks
    boss_to_mount = ((M3_BOT_PX/2 - M3_TOP_PX/2)**2 + (M3_BOT_PY/2 - M3_TOP_PY/2)**2) ** 0.5 \
                    - (M3_BOT_CSK_D/2 + BOSS_OD/2)
    usb_z_top = USB_Z_CENTER + USB_H/2
    usb_to_top = BASE_H - usb_z_top
    print(f"  Boss ↔ mount-hole gap: {boss_to_mount:.2f} mm")
    print(f"  USB cutout top → base top: {usb_to_top:.2f} mm")
