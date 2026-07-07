"""
CyberWing Canary — Jetson Orin platform (rides on SlimRig 15 mm railblocks).

A 8.75 × 4 in PLA plate. Jetson Orin Nano dev kit mounts at the +X end. Two
SlimRig Super-Lightweight 15 mm railblocks sit underneath on the -X half,
fastened with 1/4"-20 socket-cap screws.

Coordinate frame (print orientation):
  X = long axis (8.75 in)         +X end holds the Jetson Orin
  Y = short axis (4 in)
  Z = build direction, thickness

Counterbore convention:
  - 1/4" railblock screws: counterbored from TOP so the head sits flush with
    the top mounting surface (clean for equipment above).
  - M3 Orin screws: counterbored from BOTTOM so the head sits flush with the
    bottom; M3 threads up into the Orin standoff.

Outputs:
  orin_platform.stl
"""

import argparse
import math
from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

# Plate
INCH = 25.4
PLATE_L = 8.75 * INCH        # 222.25 mm (X)
PLATE_W = 4.25 * INCH        # 107.95 mm (Y)
PLATE_T = 4.0                # thickness

# --- Jetson Orin Nano dev kit (matches sub-panel measurements) ---
# As measured: PCB 100 × 78.79 mm; M3 hole pattern 92.12 × 57.59 mm.
# Orientation: ROTATED 90° — the long axis of the PCB runs along platform Y,
# short axis along platform X. Effective footprint on platform: 78.79 (X) ×
# 100 (Y), pattern: 57.59 (X) × 92.12 (Y).
ORIN_ROTATED   = True
_ORIN_PCB_LONG  = 100.0
_ORIN_PCB_SHORT = 78.79
_ORIN_PAT_LONG  = 92.12
_ORIN_PAT_SHORT = 57.59
ORIN_PCB_X     = _ORIN_PCB_SHORT if ORIN_ROTATED else _ORIN_PCB_LONG
ORIN_PCB_Y     = _ORIN_PCB_LONG  if ORIN_ROTATED else _ORIN_PCB_SHORT
ORIN_PAT_X     = _ORIN_PAT_SHORT if ORIN_ROTATED else _ORIN_PAT_LONG
ORIN_PAT_Y     = _ORIN_PAT_LONG  if ORIN_ROTATED else _ORIN_PAT_SHORT
M3_CLEAR_D     = 3.4
M3_CSK_D       = 6.0
M3_CSK_DEPTH   = 2.5          # counterbore from BOTTOM

# Place Orin centered in the +X half, with this margin from the +X edge
ORIN_END_MARGIN = 5.0         # from +X plate edge to Orin PCB edge

# --- SlimRig Super-Lightweight 15 mm railblock mounts (1/4"-20) ---
# 4-hole rectangular pattern per block.
RAIL_PAT_W       = 54.52      # Y (widthwise on platform)
RAIL_PAT_L       = 36.33      # X (lengthwise on platform)
QUARTER_CLEAR_D  = 6.8        # 1/4" clearance (6.35 mm + fit)
QUARTER_CSK_D    = 11.0       # socket-cap head counterbore Ø
QUARTER_CSK_DEPTH = 3.0       # counterbore depth from TOP face

# Single railblock centered on the platform.
RAIL_CENTER_X  = 0.0
RAIL_CENTER_Y  = 0.0

# Minimum clearances (for assertions).
MIN_HOLE_EDGE_CLR  = 5.0
MIN_HOLE_HOLE_CLR  = 3.0

OUT_DIR = Path(__file__).parent


# =============================================================================
# Derived
# =============================================================================

orin_center_x = +PLATE_L / 2 - ORIN_END_MARGIN - ORIN_PCB_X / 2
orin_center_y = 0.0

# Collect all hole centers with their effective radii for conflict checking
orin_holes    = [(orin_center_x + sx * ORIN_PAT_X / 2,
                  orin_center_y + sy * ORIN_PAT_Y / 2,
                  M3_CLEAR_D / 2, "Orin M3")
                 for sx in (-1, 1) for sy in (-1, 1)]

rail_holes    = [(RAIL_CENTER_X + sx * RAIL_PAT_L / 2,
                  RAIL_CENTER_Y + sy * RAIL_PAT_W / 2,
                  QUARTER_CLEAR_D / 2, "rail 1/4\"")
                 for sx in (-1, 1) for sy in (-1, 1)]

all_holes = orin_holes + rail_holes

# Edge clearance
for x, y, r, tag in all_holes:
    ex = min(PLATE_L / 2 - abs(x), PLATE_W / 2 - abs(y)) - r
    assert ex >= MIN_HOLE_EDGE_CLR, \
        f"{tag} hole @({x:+.1f},{y:+.1f}) too close to plate edge: {ex:.2f} mm"

# Hole-to-hole clearance
for i, (x1, y1, r1, t1) in enumerate(all_holes):
    for x2, y2, r2, t2 in all_holes[i + 1:]:
        d = math.hypot(x1 - x2, y1 - y2) - (r1 + r2)
        assert d >= MIN_HOLE_HOLE_CLR, \
            f"{t1} @({x1:+.1f},{y1:+.1f}) conflicts with {t2} @({x2:+.1f},{y2:+.1f}): {d:.2f} mm"


# =============================================================================
# Build
# =============================================================================

def _cut_hole(plate: Part, cx: float, cy: float,
              clear_d: float, csk_d: float, csk_depth: float,
              csk_top: bool) -> Part:
    """Subtract a through-hole plus counterbore on the chosen face."""
    thru = Cylinder(clear_d / 2, PLATE_T + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
    plate -= Pos(cx, cy, -0.2) * thru
    # Skip counterbore if it would punch through (e.g. thin test prints)
    if csk_depth > 0 and csk_depth + 0.4 < PLATE_T:
        csk = Cylinder(csk_d / 2, csk_depth + 0.1,
                       align=(Align.CENTER, Align.CENTER, Align.MIN))
        if csk_top:
            plate -= Pos(cx, cy, PLATE_T - csk_depth) * csk
        else:
            plate -= Pos(cx, cy, -0.05) * csk
    return plate


def build_platform() -> Part:
    plate = Box(PLATE_L, PLATE_W, PLATE_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× Orin M3 holes (counterbore on BOTTOM)
    for x, y, _r, _tag in orin_holes:
        plate = _cut_hole(plate, x, y, M3_CLEAR_D, M3_CSK_D, M3_CSK_DEPTH,
                          csk_top=False)

    # 1/4" railblock holes (counterbore on TOP for flush screw heads)
    for x, y, _r, _tag in rail_holes:
        plate = _cut_hole(plate, x, y,
                          QUARTER_CLEAR_D, QUARTER_CSK_D, QUARTER_CSK_DEPTH,
                          csk_top=True)

    return plate


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    global PLATE_T
    ap = argparse.ArgumentParser(description="Jetson Orin platform generator")
    ap.add_argument("--test", action="store_true",
                    help="Thin (1.2 mm) test print without counterbores.")
    ap.add_argument("--thickness", type=float, default=None,
                    help="Override plate thickness in mm.")
    args = ap.parse_args()

    if args.test:
        PLATE_T = 1.2
        out_name = "orin_platform_test.stl"
    elif args.thickness is not None:
        PLATE_T = args.thickness
        out_name = f"orin_platform_{PLATE_T:g}mm.stl"
    else:
        out_name = "orin_platform.stl"

    print("=" * 60)
    print("Orin platform — build123d generator")
    if args.test:
        print("  TEST PRINT MODE (thin, no counterbores)")
    print("=" * 60)
    print(f"Plate:         {PLATE_L:.2f} × {PLATE_W:.2f} × {PLATE_T} mm "
          f"(8.75 × 4.25 in)")
    print(f"Orin (rotated={ORIN_ROTATED}): PCB {ORIN_PCB_X} × {ORIN_PCB_Y}, "
          f"holes {ORIN_PAT_X} × {ORIN_PAT_Y}, center X = {orin_center_x:+.2f}")
    print(f"Railblock:     1× at center, pattern "
          f"{RAIL_PAT_L} (X) × {RAIL_PAT_W} (Y) — 1/4\" screws")
    print(f"Counterbores:  M3 on BOTTOM (Ø{M3_CSK_D}×{M3_CSK_DEPTH}), "
          f"1/4\" on TOP (Ø{QUARTER_CSK_D}×{QUARTER_CSK_DEPTH})")
    print()

    plate = build_platform()
    out = OUT_DIR / out_name
    export_stl(plate, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)")

    print("\nPrint orientation: already flat on bed (+Z up). No supports.")
    print("Hardware BOM:")
    print("  - 4× M3 × 6 mm socket caps (Jetson Orin to platform)")
    print("  - 4× M3 standoffs or nuts (Orin side)")
    print("  - 4× 1/4\"-20 socket-cap screws (platform to railblock)")


if __name__ == "__main__":
    main()
