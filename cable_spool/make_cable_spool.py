"""
Cable spool for a single 45" (1143 mm) cable, Ø5.28 mm.

Hub Ø50 mm gives ~6× bend radius (safe for most cables).
Wraps: ~7 turns at hub, fits in ~2 layers within 25 mm width.
Flange Ø80 mm retains up to 3 layers.

Features:
  - Cable entry slot through one flange
  - Edge notch on flange to clip the free end
  - Hollow hub (less material, faster print)
  - Flat-printable (no supports needed)

Outputs: cable_spool.stl
"""

import math
from build123d import *
from pathlib import Path

# =============================================================================
# Parameters
# =============================================================================

CABLE_D = 5.28               # cable diameter (mm)
CABLE_LEN = 45 * 25.4        # 45 inches → mm

HUB_OD = 50.0                # hub outer diameter (~6× cable dia bend radius)
HUB_ID = 38.0                # hub inner diameter (hollow core)
FLANGE_OD = 85.0             # flange outer diameter
FLANGE_T = 2.0               # flange thickness
SPOOL_W = 25.0               # winding width between flanges
HUB_H = SPOOL_W + 2 * FLANGE_T  # total hub height

SLOT_W = CABLE_D + 1.5       # cable entry slot width (clearance)
SLOT_DEPTH = (FLANGE_OD - HUB_OD) / 2 + 2  # extends from hub to flange edge

NOTCH_W = CABLE_D + 1.0      # end-clip notch width
NOTCH_DEPTH = 3.0            # how deep the clip notch cuts into flange edge

OUT_DIR = Path(__file__).parent

# Verify cable fits
hub_circ = math.pi * HUB_OD
wraps_per_layer = math.floor(SPOOL_W / CABLE_D)
layers_needed = math.ceil(CABLE_LEN / (hub_circ * wraps_per_layer))
max_od = HUB_OD + 2 * CABLE_D * layers_needed
print(f"  Hub circumference: {hub_circ:.0f} mm")
print(f"  Wraps/layer: {wraps_per_layer}, layers needed: {layers_needed}")
print(f"  Max wound OD: {max_od:.0f} mm (flange: {FLANGE_OD} mm)")
assert max_od < FLANGE_OD, "Cable won't fit — increase FLANGE_OD or SPOOL_W"


def build_spool() -> Part:
    # Hub — hollow cylinder
    hub_outer = Cylinder(HUB_OD / 2, HUB_H,
                         align=(Align.CENTER, Align.CENTER, Align.MIN))
    hub_inner = Cylinder(HUB_ID / 2, HUB_H,
                         align=(Align.CENTER, Align.CENTER, Align.MIN))
    spool = hub_outer - hub_inner

    # Bottom flange
    bottom = Cylinder(FLANGE_OD / 2, FLANGE_T,
                      align=(Align.CENTER, Align.CENTER, Align.MIN))
    spool += bottom

    # Top flange
    top = Pos(0, 0, HUB_H - FLANGE_T) * Cylinder(
        FLANGE_OD / 2, FLANGE_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    spool += top

    # Cable entry slot through top flange (radial cut from hub to edge)
    slot = Pos(HUB_OD / 2 + SLOT_DEPTH / 2 - 2, 0, HUB_H - FLANGE_T) * Box(
        SLOT_DEPTH, SLOT_W, FLANGE_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    spool -= slot

    # Cable guide ramp into the winding area
    ramp = Pos(HUB_OD / 2 + 2, 0, HUB_H - FLANGE_T - CABLE_D) * Box(
        6, SLOT_W, CABLE_D + FLANGE_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    spool -= ramp

    # Edge notch on bottom flange to clip the free cable end
    notch = Pos(FLANGE_OD / 2 - NOTCH_DEPTH / 2, 0, 0) * Box(
        NOTCH_DEPTH + 1, NOTCH_W, FLANGE_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    spool -= notch

    # Second notch 180° opposite for convenience
    notch2 = Pos(-FLANGE_OD / 2 + NOTCH_DEPTH / 2, 0, 0) * Box(
        NOTCH_DEPTH + 1, NOTCH_W, FLANGE_T,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    spool -= notch2

    return spool


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()

    part = build_spool()
    out = OUT_DIR / "cable_spool.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Spool: Ø{FLANGE_OD} × {HUB_H} mm")
    print(f"  Hub: Ø{HUB_OD} (wall {(HUB_OD - HUB_ID) / 2:.0f} mm)")
    print(f"  Winding width: {SPOOL_W} mm")
    print(f"  Cable: {CABLE_LEN:.0f} mm ({CABLE_LEN / 25.4:.0f}\"), Ø{CABLE_D} mm")

    if args.preview:
        show(part)
