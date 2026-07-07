"""
LILYGO SX1262 housing — TOP piece, STACKED variant.

Same plate concept as `make_top.py`, but widened in Y to 65 mm to match
the stacked base (`make_base_stacked.py`) and the flycatcher gps_rtk2
platform footprint. LILYGO M2 mount pattern, inner cutout, and M3
top→base attach pattern are unchanged so the existing PCB and the
base's internal bosses still mate.

  Top piece: 101 × 65 × 4 mm
"""

from build123d import *
from pathlib import Path

# =============================================================================
# Top-piece envelope
# =============================================================================
TOP_L = 101.0           # X (unchanged)
TOP_W = 65.0            # Y — matches make_base_stacked.py BASE_W
TOP_T = 4.0             # Z

# Inner rectangular cutout (battery / module access) — unchanged
CUT_L = 86.0
CUT_W = 23.0
CUT_EXTEND_PLUS_X = 4.7

# LILYGO M2 mount pattern (board sits on top of the standoffs) — unchanged
M2_PATTERN_X = 95.33
M2_PATTERN_Y = 28.55
M2_CLEAR_D   = 2.4
M2_BOSS_D    = 4.5
M2_BOSS_H    = 5.0

# M3 attach pattern (joins top to bottom) — unchanged so existing
# make_base_stacked.py bosses (70 × 32) still mate.
M3_PATTERN_X = 70.0
M3_PATTERN_Y = 32.0
M3_CLEAR_D   = 3.4
M3_CSK_D     = 5.5
M3_CSK_DEPTH = 1.6

OUT_DIR = Path(__file__).parent


def build_top() -> Part:
    body = Box(TOP_L, TOP_W, TOP_T,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Inner rectangular cutout for battery — extended asymmetrically on +X
    cut_total_L = CUT_L + CUT_EXTEND_PLUS_X
    cut_center_x = CUT_EXTEND_PLUS_X / 2
    body -= Pos(cut_center_x, 0, -0.2) * Box(
        cut_total_L, CUT_W, TOP_T + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # M2 standoffs + clearance holes
    hx, hy = M2_PATTERN_X / 2, M2_PATTERN_Y / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * hx, sy * hy
            body += Pos(cx, cy, TOP_T) * Cylinder(
                M2_BOSS_D / 2, M2_BOSS_H,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= Pos(cx, cy, -0.2) * Cylinder(
                M2_CLEAR_D / 2, TOP_T + M2_BOSS_H + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # M3 attach holes (top → bottom), countersunk on top face
    hx, hy = M3_PATTERN_X / 2, M3_PATTERN_Y / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * hx, sy * hy
            body -= Pos(cx, cy, -0.2) * Cylinder(
                M3_CLEAR_D / 2, TOP_T + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= Pos(cx, cy, TOP_T - M3_CSK_DEPTH) * Cylinder(
                M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return body


if __name__ == "__main__":
    part = build_top()
    out = OUT_DIR / "lilygo_sx1262_top_stacked.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Top piece: {TOP_L} × {TOP_W} × {TOP_T} mm  (stacked variant)")
    print(f"  Inner cutout: {CUT_L + CUT_EXTEND_PLUS_X} × {CUT_W} mm "
          f"(extended +{CUT_EXTEND_PLUS_X} on +X)")
    print(f"  M2 LILYGO mount: 4× Ø{M2_CLEAR_D} at {M2_PATTERN_X} × {M2_PATTERN_Y} mm")
    print(f"  M2 standoffs:    Ø{M2_BOSS_D} × {M2_BOSS_H} mm tall above top face")
    print(f"  M3 attach holes: 4× Ø{M3_CLEAR_D} at {M3_PATTERN_X} × {M3_PATTERN_Y} mm, "
          f"csk Ø{M3_CSK_D}×{M3_CSK_DEPTH}")
    m2_edge_x = TOP_L/2 - M2_PATTERN_X/2 - M2_CLEAR_D/2
    m2_edge_y = TOP_W/2 - M2_PATTERN_Y/2 - M2_CLEAR_D/2
    m3_edge_x = TOP_L/2 - M3_PATTERN_X/2 - M3_CSK_D/2
    m3_edge_y = TOP_W/2 - M3_PATTERN_Y/2 - M3_CSK_D/2
    m3_to_cut_x = M3_PATTERN_X/2 - (CUT_L + CUT_EXTEND_PLUS_X)/2 - M3_CSK_D/2
    m3_to_cut_y = M3_PATTERN_Y/2 - CUT_W/2 - M3_CSK_D/2
    m2_to_m3 = ((M2_PATTERN_X/2 - M3_PATTERN_X/2)**2 +
                (M2_PATTERN_Y/2 - M3_PATTERN_Y/2)**2) ** 0.5 \
               - (M2_CLEAR_D/2 + M3_CSK_D/2)
    print(f"  M2 edge clearance: {m2_edge_x:.2f} (X), {m2_edge_y:.2f} (Y) mm")
    print(f"  M3 edge clearance: {m3_edge_x:.2f} (X), {m3_edge_y:.2f} (Y) mm")
    print(f"  M3 → cutout:       {m3_to_cut_x:.2f} (X), {m3_to_cut_y:.2f} (Y) mm")
    print(f"  M2 ↔ M3 hole gap:  {m2_to_m3:.2f} mm")
