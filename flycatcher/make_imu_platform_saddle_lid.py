"""
Flat lid for the saddle-mount platform (`make_imu_platform_saddle.py`).

Flat plate matching the platform footprint with only the 4× M3 inner
mount holes (countersunk on the top face).
"""

from build123d import *
from pathlib import Path

# Footprint matches the platform
LID_L = 68.0
LID_W = 60.0
LID_H = 3.0           # flat plate thickness

# 4× M3 inner mount pattern (matches flycatcher platform)
M3_PATTERN_X = 57.6
M3_PATTERN_Y = 49.18
M3_CLEAR_D   = 3.4
M3_CSK_D     = 6.2
M3_CSK_DEPTH = 1.8

OUT_DIR = Path(__file__).parent


def build_lid() -> Part:
    body = Box(LID_L, LID_W, LID_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M3 clearance + countersink (csk on top face)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = sx * M3_PATTERN_X / 2
            cy = sy * M3_PATTERN_Y / 2
            body -= Pos(cx, cy, -0.2) * Cylinder(
                M3_CLEAR_D / 2, LID_H + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= Pos(cx, cy, LID_H - M3_CSK_DEPTH) * Cylinder(
                M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return body


if __name__ == "__main__":
    part = build_lid()
    # Flip so top face (countersinks) sits on the bed
    part = Rot(180, 0, 0) * part
    part = Pos(0, 0, LID_H) * part

    out = OUT_DIR / "imu_platform_saddle_lid.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Lid:       {LID_L} × {LID_W} × {LID_H} mm (flat plate)")
    print(f"  M3 mounts: 4× Ø{M3_CLEAR_D} in {M3_PATTERN_X} × {M3_PATTERN_Y} mm "
          f"(csk Ø{M3_CSK_D}×{M3_CSK_DEPTH} on top)")
    edge_x = LID_L/2 - M3_PATTERN_X/2 - M3_CSK_D/2
    edge_y = LID_W/2 - M3_PATTERN_Y/2 - M3_CSK_D/2
    print(f"  M3 edge clearance: {edge_x:.2f} mm (X), {edge_y:.2f} mm (Y)")
    print(f"  Print top-face DOWN. No supports.")
