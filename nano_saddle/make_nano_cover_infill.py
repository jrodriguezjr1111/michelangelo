"""
Slicer-infill top cover for the dual-Jetson nano saddle.

A plain 80 × 197 × 3 mm plate carrying only the 8× M3 mount features. The
*venting* is produced by the slicer itself: print with no top/bottom skin
and the default Qidi sparse infill (crosshatch @ 20%) becomes the visible
structure — exactly the pattern used everywhere else on this machine.

Pair with these slicer overrides:
    top_shell_layers      = 0
    bottom_shell_layers   = 0
    sparse_infill_pattern = crosshatch
    sparse_infill_density = 20
    wall_loop_count       = 3      (perimeter strength around hole + edge)

Mounts to the saddle via the same 8× M3 Jetson hole pattern on 30 mm
standoffs. Print flat, lattice-up, with a 5–8 mm brim.
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS  (mirror make_nano_cover.py)
# =============================================================================
BLOCK_LEN = 80.0
BLOCK_WID = 197.0
PLATE_T   = 3.0
CLEAR_H   = 30.0

NANO_PATTERN_Y = 86.14
NANO_PATTERN_X = 58.25
ORIN_PATTERN_Y = 92.12
ORIN_PATTERN_X = 57.59
M3_CLEAR_D     = 3.4
M3_CB_D        = 5.3
M3_CB_DEPTH    = 1.6

# Mount centers are pinned to the saddle's board positions (saddle BLOCK_WID
# = 197). The cover plate may extend beyond that for extra brim/overhang;
# the holes must stay aligned with the boards regardless of plate length.
SADDLE_REF_WID = 197.0
ORIN_Y_CENTER =  SADDLE_REF_WID / 4                                 # +49.25
NANO_Y_CENTER = -(SADDLE_REF_WID / 2 - NANO_PATTERN_Y / 2 - 3.19)   # −52.24

OUT_DIR = Path(__file__).parent

# =============================================================================
# Sanity
# =============================================================================
for nm, py, yc in (("Nano", NANO_PATTERN_Y, NANO_Y_CENTER),
                   ("Orin", ORIN_PATTERN_Y, ORIN_Y_CENTER)):
    assert abs(yc) + py / 2 + M3_CB_D / 2 + 0.4 < BLOCK_WID / 2, \
        f"{nm} M3 c'bore exits plate in Y"
    assert py / 2 + M3_CB_D / 2 + 0.4 < BLOCK_WID / 2, \
        f"{nm} M3 c'bore exits plate in X"


def boss_centers():
    out = []
    for py, px, yc in ((NANO_PATTERN_Y, NANO_PATTERN_X, NANO_Y_CENTER),
                       (ORIN_PATTERN_Y, ORIN_PATTERN_X, ORIN_Y_CENTER)):
        for sx in (-1, 1):
            for sy in (-1, 1):
                out.append((sx * px / 2, yc + sy * py / 2))
    return out


def build_cover() -> Part:
    plate = Box(BLOCK_LEN, BLOCK_WID, PLATE_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
    for (cx, cy) in boss_centers():
        plate -= Pos(cx, cy, -0.2) * Cylinder(
            M3_CLEAR_D / 2, PLATE_T + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        plate -= Pos(cx, cy, PLATE_T - M3_CB_DEPTH) * Cylinder(
            M3_CB_D / 2, M3_CB_DEPTH + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
    return plate


def main() -> None:
    cover = build_cover()
    out = OUT_DIR / "nano_cover_infill.stl"
    export_stl(cover, str(out))
    print("=" * 62)
    print("Dual-Jetson nano saddle — slicer-infill top cover")
    print("=" * 62)
    print(f"Footprint: {BLOCK_LEN} × {BLOCK_WID} × {PLATE_T} mm")
    print(f"Mount:     8× Ø{M3_CLEAR_D} M3 (Nano + Orin patterns), "
          f"Ø{M3_CB_D}×{M3_CB_DEPTH} c'bore on top")
    print(f"Standoffs: {CLEAR_H} mm (hardware) board-top → cover")
    print(f"  ✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)")
    print("\nVenting comes from the slicer infill (crosshatch 20%, no skin).")
    print("Pair with these process overrides when slicing:")
    print("  top_shell_layers=0  bottom_shell_layers=0")
    print("  sparse_infill_pattern=crosshatch  sparse_infill_density=20")
    print("  wall_loop_count=3")
    print("\nPrint flat, brim 5–8 mm.")


if __name__ == "__main__":
    main()
