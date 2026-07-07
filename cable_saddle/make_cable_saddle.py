"""
USB Cable Saddle — horizontal split (top cap + bottom tray).

Full assembly: 108.49 × 20 × 12 mm, split at the cable center height.
Bottom tray: semi-circular channels where cables rest.
Top cap: mirror image that clamps down over cables.
M3 bolts pass vertically through both halves at each end.

Print 2× the same STL — one becomes bottom tray, flip the other for the top cap.

Outputs: cable_saddle_half.stl
"""

from build123d import *
from pathlib import Path
import math

# =============================================================================
# Parameters
# =============================================================================

SADDLE_L = 108.49       # length (X) — along cable row
SADDLE_W = 20.0         # width (Y) — cable runs along Y
SADDLE_H = 12.0         # total assembled height (Z)

N_CABLES = 7
CABLE_D = 5.0           # USB cable diameter
SLOT_D = CABLE_D + 0.8  # channel diameter (clearance)

# Split plane at cable center height
SLOT_R = SLOT_D / 2
SPLIT_Z = SADDLE_H / 2  # split at geometric center
HALF_H = SPLIT_Z        # each half height

# M3 clamping bolts (vertical, one on each end)
M3_CLEAR_D = 3.4
M3_CSK_D = 6.2
M3_CSK_DEPTH = 2.0      # countersink from top of the top cap
M3_INSET_X = 5.0        # from each X-end
M3_POSITIONS = [
    (-SADDLE_L / 2 + M3_INSET_X, 0),   # left end
    (+SADDLE_L / 2 - M3_INSET_X, 0),   # right end
]

# Derived
SLOT_SPACING = SADDLE_L / (N_CABLES + 1)

OUT_DIR = Path(__file__).parent


def build_half() -> Part:
    """Build one half (bottom tray). Flip Z to use as top cap."""
    half = Box(SADDLE_L, SADDLE_W, HALF_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Semi-circular cable channels on the top face (split plane)
    for i in range(N_CABLES):
        cx = -SADDLE_L / 2 + SLOT_SPACING * (i + 1)
        # Half-cylinder channel: center at top face, radius = SLOT_R
        channel = Pos(cx, 0, HALF_H) * Rot(90, 0, 0) * Cylinder(
            SLOT_R, SADDLE_W + 2,
            align=(Align.CENTER, Align.CENTER, Align.CENTER))
        half -= channel

    # M3 through-holes (vertical)
    for hx, hy in M3_POSITIONS:
        hole = Pos(hx, hy) * Cylinder(
            M3_CLEAR_D / 2, HALF_H,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        half -= hole
        # Countersink from bottom (becomes top when flipped for cap)
        csk = Pos(hx, hy) * Cylinder(
            M3_CSK_D / 2, M3_CSK_DEPTH,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        half -= csk

    return half


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()

    half = build_half()
    out = OUT_DIR / "cable_saddle_half.stl"
    export_stl(half, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Each half: {SADDLE_L} × {SADDLE_W} × {HALF_H} mm")
    print(f"  Channels: {N_CABLES} × Ø{SLOT_D:.1f} mm (semi-circular)")
    print(f"  Spacing: {SLOT_SPACING:.2f} mm center-to-center")
    print(f"  M3 holes: {len(M3_POSITIONS)} (Ø{M3_CLEAR_D}, csk Ø{M3_CSK_D}×{M3_CSK_DEPTH})")
    print(f"  Assembly: stack 2 halves, flip top one, bolt with M3")

    if args.preview:
        show(half)
