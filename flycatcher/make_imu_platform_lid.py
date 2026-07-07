"""
Flycatcher platform saddle — snug-fit LID.

Closes the open (bottom) face of `imu_platform_saddle.stl` (101 × 65 outer,
96 × 60 cavity, walls 2.5). A SOLID rectangular extrusion on the plate nests
snugly inside the saddle's wall frame (press fit, 0.15 mm clearance per side).

  Plate:     101 × 65 × 3 mm  (same footprint as the saddle)
  Extrusion: 95.7 × 59.7 × 4 mm solid plug (0.15 mm/side in the 96 × 60 frame)
  Holes:     4× Ø3.4 (M3 clearance) at 58 × 49 mm, centered — same pattern as
             make_imu_platform_saddle.py, so through-bolts pass lid + saddle.

The plug occupies the first 4 mm of the cavity — below the saddle's cable
slots (which start ≈7 mm up), so it does not block them.

Print plate-down, plug UP. No supports.

Output: imu_platform_lid.stl
"""

from build123d import *
from pathlib import Path

# Saddle interface (from make_imu_platform_saddle.py)
SAD_L, SAD_W      = 101.0, 65.0
SAD_WALL          = 2.5
CAV_L, CAV_W      = SAD_L - 2 * SAD_WALL, SAD_W - 2 * SAD_WALL   # 96 × 60
SLOT_Z_BOTTOM     = (29.0 - 3.0) / 2 - 2.0 - 7.8 / 2             # 7.1 (saddle frame)

# Lid
LID_T     = 3.0
FIT_CLEAR = 0.15         # per-side clearance for a snug press fit
PLUG_H    = 4.0
PLUG_X    = CAV_L - 2 * FIT_CLEAR     # 95.7
PLUG_Y    = CAV_W - 2 * FIT_CLEAR     # 59.7

# M3 holes — same centered 58 × 49 pattern as the saddle.
M3_PAT_X, M3_PAT_Y, M3_D = 58.0, 49.0, 3.4

# Rectangular cutout — through plate + plug. 9 (X) × 18 (Y), centered in Y.
# Near face was 28 mm from the +X edge; shifted +11.30 in X → 16.7 mm.
CUT_W_X   = 9.0
CUT_L_Y   = 18.0
CUT_EDGE  = 28.0 - 11.30                           # 16.7: +X edge → near face
CUT_XC    = SAD_L / 2 - CUT_EDGE - CUT_W_X / 2     # +29.3 (spans 24.8..33.8)
CUT_YC    = 0.0

OUT_DIR = Path(__file__).parent

# Sanity
assert PLUG_H + 0.5 < SLOT_Z_BOTTOM, "Plug tall enough to block the saddle's cable slots"
assert M3_PAT_X / 2 + M3_D / 2 < PLUG_X / 2, "M3 hole exits the plug (X)"
assert M3_PAT_Y / 2 + M3_D / 2 < PLUG_Y / 2, "M3 hole exits the plug (Y)"

# Cutout inside the plug, clear of the M3 holes
assert CUT_XC + CUT_W_X / 2 < PLUG_X / 2 - 1, "Cutout exits the plug (X)"
assert CUT_L_Y / 2 < PLUG_Y / 2 - 1, "Cutout exits the plug (Y)"
for _sx in (-1, 1):
    for _sy in (-1, 1):
        _hx, _hy = _sx * M3_PAT_X / 2, _sy * M3_PAT_Y / 2
        _dx = max(abs(_hx - CUT_XC) - CUT_W_X / 2, 0.0)
        _dy = max(abs(_hy - CUT_YC) - CUT_L_Y / 2, 0.0)
        assert (_dx ** 2 + _dy ** 2) ** 0.5 > M3_D / 2 + 1, "Cutout too close to an M3 hole"


def build_lid() -> Part:
    # Base plate
    lid = Box(SAD_L, SAD_W, LID_T, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Solid rectangular extrusion — snug plug into the saddle's frame.
    lid += Pos(0, 0, LID_T) * Box(
        PLUG_X, PLUG_Y, PLUG_H, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M3 holes, 58 × 49 centered — matches the saddle.
    for sx in (-1, 1):
        for sy in (-1, 1):
            lid -= Pos(sx * M3_PAT_X / 2, sy * M3_PAT_Y / 2, -0.2) * Cylinder(
                M3_D / 2, LID_T + PLUG_H + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Rectangular cutout through plate + plug.
    lid -= Pos(CUT_XC, CUT_YC, -0.2) * Box(
        CUT_W_X, CUT_L_Y, LID_T + PLUG_H + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    return lid


if __name__ == "__main__":
    part = build_lid()
    out = OUT_DIR / "imu_platform_lid.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Plate:     {SAD_L} × {SAD_W} × {LID_T} mm")
    print(f"  Extrusion: {PLUG_X} × {PLUG_Y} × {PLUG_H} mm solid plug "
          f"({FIT_CLEAR}/side in the {CAV_L} × {CAV_W} frame — snug press fit)")
    print(f"  M3:        4× Ø{M3_D} at X=±{M3_PAT_X/2}, Y=±{M3_PAT_Y/2} "
          f"({M3_PAT_X} × {M3_PAT_Y}, centered — matches the saddle)")
    print(f"  Cutout:    {CUT_W_X} (X) × {CUT_L_Y} (Y) through plate+plug at "
          f"(X={CUT_XC:+.1f}, Y={CUT_YC:.0f}) — near face {CUT_EDGE} mm from the +X edge")
    print(f"  Plug top at z={LID_T + PLUG_H} stays below the saddle slots "
          f"(start ~{SLOT_Z_BOTTOM + LID_T:.1f})")
    print(f"  Print plate-down, plug UP. No supports.")
