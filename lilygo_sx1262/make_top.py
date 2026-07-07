"""
LILYGO SX1262 housing — TOP piece (split design, part 1 of 2).

A flat plate that sits on top of the housing as the closing/mounting face.
101 mm long × 65 mm wide × 4 mm thick.
  - Inner rectangular cutout 86 × 23 mm, extended +4.7 mm along +X
    (asymmetric: total 90.7 mm, accommodates an over-hanging connector)
  - 4× M2 holes (95.33 × 28.55 mm) for the LILYGO PCB, each surrounded
    by a 5 mm-tall standoff boss rising above the top face
  - 4× M3 holes for attaching the top to the bottom piece

Designed to drop onto flycatcher/make_imu_platform_saddle.py (80 × 65 mm):
  - Same 65 mm Y dimension → both Y edges flush with the platform.
  - X geometry is shifted +10.5 mm so the −X edge is flush with the
    platform’s −X edge; the +X end (connector side) overhangs the
    platform by 21 mm.
"""

from build123d import *
from pathlib import Path

# =============================================================================
# Top-piece envelope
# =============================================================================
TOP_L = 101.0           # X (length) — fits the 95.33 mm M2 mount pattern
TOP_W = 65.0            # Y (width) — matches IMU platform-saddle Y (65 mm)
TOP_T = 4.0             # Z (thickness)

# IMU platform-saddle footprint (flycatcher/make_imu_platform_saddle.py).
PLATFORM_L = 80.0       # X
PLATFORM_W = 65.0       # Y (must equal TOP_W for full Y flush)
# Flush placement: align the −X edge of the top with the −X edge of the
# platform. The +X (connector) end overhangs by (TOP_L − PLATFORM_L) = 21 mm.
X_FLUSH_OFFSET = (TOP_L - PLATFORM_L) / 2     # = +10.5 mm

# Inner rectangular cutout (battery access)
CUT_L = 86.0            # X (base length)
CUT_W = 23.0            # Y
CUT_EXTEND_PLUS_X = 4.7 # extra length added on the +X side only

# LILYGO M2 mount pattern (board sits on top of the standoffs)
M2_PATTERN_X = 95.33
M2_PATTERN_Y = 28.55
M2_CLEAR_D   = 2.4
M2_BOSS_D    = 4.5      # standoff outer diameter
M2_BOSS_H    = 5.0      # standoff height above the top face

# M3 attach pattern — aligned with the flycatcher IMU platform-saddle
# (make_imu_platform_saddle.py: M3_PAT_X = 58, M3_PAT_Y = 49, centered on
# the platform). Because this top is shifted +X_FLUSH_OFFSET in assembly,
# the holes are asymmetric in the plate's local frame: symmetric around
# the assembly origin (platform center), not the plate center.
FLYCATCHER_M3_X = 58.0
FLYCATCHER_M3_Y = 49.0
M3_CLEAR_D   = 3.4
M3_CSK_D     = 5.5
M3_CSK_DEPTH = 1.6

OUT_DIR = Path(__file__).parent


def build_top() -> Part:
    body = Box(TOP_L, TOP_W, TOP_T,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Inner rectangular cutout for battery — extended asymmetrically on +X
    cut_total_L = CUT_L + CUT_EXTEND_PLUS_X
    cut_center_x = CUT_EXTEND_PLUS_X / 2   # shift box so extension is on +X
    cutout = Pos(cut_center_x, 0, -0.2) * Box(
        cut_total_L, CUT_W, TOP_T + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    body -= cutout

    # M2 standoffs (bosses above top face, with clearance holes through both)
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

    # M3 attach holes — aligned to the flycatcher M3 pattern (assembly
    # coords ±FLYCATCHER_M3_X/2, ±FLYCATCHER_M3_Y/2). Convert to plate-local
    # by subtracting the X assembly shift.
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = sx * FLYCATCHER_M3_X / 2 - X_FLUSH_OFFSET
            cy = sy * FLYCATCHER_M3_Y / 2
            body -= Pos(cx, cy, -0.2) * Cylinder(
                M3_CLEAR_D / 2, TOP_T + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= Pos(cx, cy, TOP_T - M3_CSK_DEPTH) * Cylinder(
                M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return body


if __name__ == "__main__":
    part = build_top()
    # Shift in X so the −X edge of this top sits flush with the −X edge of
    # the IMU platform-saddle (centered at the same origin in assembly).
    part = Pos(X_FLUSH_OFFSET, 0, 0) * part
    out = OUT_DIR / "lilygo_sx1262_top.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Top piece: {TOP_L} × {TOP_W} × {TOP_T} mm")
    print(f"  On platform {PLATFORM_L} × {PLATFORM_W}: −X edges flush; "
          f"+X overhang = {TOP_L - PLATFORM_L:.1f} mm (connector side)")
    print(f"  X shift applied at export: +{X_FLUSH_OFFSET:.2f} mm")
    print(f"  Inner cutout: {CUT_L + CUT_EXTEND_PLUS_X} × {CUT_W} mm (extended +{CUT_EXTEND_PLUS_X} on +X)")
    print(f"  M2 LILYGO mount: 4× Ø{M2_CLEAR_D} at {M2_PATTERN_X} × {M2_PATTERN_Y} mm")
    print(f"  M2 standoffs: Ø{M2_BOSS_D} × {M2_BOSS_H} mm tall (above top face)")
    print(f"  M3 attach holes: 4× Ø{M3_CLEAR_D} at flycatcher pattern "
          f"{FLYCATCHER_M3_X} × {FLYCATCHER_M3_Y} mm (assembly coords), csk Ø{M3_CSK_D}×{M3_CSK_DEPTH}")
    # M3 hole positions in plate-local coords (after the export shift).
    m3_local_x_plus  =  FLYCATCHER_M3_X / 2 - X_FLUSH_OFFSET
    m3_local_x_minus = -FLYCATCHER_M3_X / 2 - X_FLUSH_OFFSET
    print(f"  M3 plate-local X: {m3_local_x_minus:+.2f}, {m3_local_x_plus:+.2f} mm (Y = ±{FLYCATCHER_M3_Y/2})")

    # Edge & clearance checks
    m2_edge_x = TOP_L/2 - M2_PATTERN_X/2 - M2_CLEAR_D/2
    m2_edge_y = TOP_W/2 - M2_PATTERN_Y/2 - M2_CLEAR_D/2
    # M3 plate-edge clearance — X is asymmetric (use the worse side).
    m3_edge_x = min(TOP_L/2 - m3_local_x_plus, TOP_L/2 + m3_local_x_minus) - M3_CSK_D/2
    m3_edge_y = TOP_W/2 - FLYCATCHER_M3_Y/2 - M3_CSK_D/2
    # M3 holes sit in the Y side strips (±24.5), well outside CUT_W/2 = 11.5,
    # so the only relevant cutout clearance is in Y.
    m3_to_cut_y = FLYCATCHER_M3_Y/2 - CUT_W/2 - M3_CSK_D/2
    # Closest M2-to-M3 hole gap (−X corner: M2 at (−47.665, ±14.275),
    # M3 at (−39.5, ±24.5)).
    m2_to_m3 = ((M2_PATTERN_X/2 - abs(m3_local_x_minus))**2 +
                (FLYCATCHER_M3_Y/2 - M2_PATTERN_Y/2)**2) ** 0.5 \
               - (M2_CLEAR_D/2 + M3_CSK_D/2)
    print(f"  M2 edge clearance: {m2_edge_x:.2f} (X), {m2_edge_y:.2f} (Y) mm")
    print(f"  M3 edge clearance: {m3_edge_x:.2f} (X, worst), {m3_edge_y:.2f} (Y) mm")
    print(f"  M3 → cutout (Y): {m3_to_cut_y:.2f} mm material")
    print(f"  M2 ↔ M3 hole gap (−X corner): {m2_to_m3:.2f} mm")
