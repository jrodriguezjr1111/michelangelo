"""
CyberWing Canary — GNSS dual-tube saddle clamp, Y-WIDE variant.

Same as `make_gnss_saddle.py` (central Ø30 GNSS through-hole, 4× M4 clamps,
two parallel tubes) but extended to 197 mm along Y for wing-style mounting.

GEOMETRY NOTE — this is NOT a quarter-wrap clamp:
  Because BLOCK_WID (197) ≫ 2·(TUBE_Y + R_IN) ≈ 76, the tube centers
  (Y = ±30.09) sit well inside the block. Each tube becomes a full
  cylindrical tunnel through the block, and each printed half wraps 180°
  around the tubes (full enclosure in assembly). Tubes must be inserted
  axially.

Outputs:
  gnss_saddle_wide_half.stl    (print 2 copies, mirror-identical)
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

TUBE_OD         = 15.39
TUBE_CENTER_SEP = 60.17
CLEARANCE       = 0.4

GNSS_HOLE_D     = 30.0       # Ø30 through-hole, centered

BLOCK_LEN = 50.0             # X — clamp grip length (same as base)
BLOCK_WID = 197.0            # Y — extended wing-to-wing
BLOCK_HT  = 28.0             # Z — assembled

BOLT_X_OFFSET    = 18.0
BOLT_Y_OFFSET    = 18.0
SCREW_CLEAR_D    = 4.4
SCREW_HEAD_D     = 8.0
SCREW_HEAD_DEPTH = 4.5

# ZED-F9P mounting pattern (4× M3, 37.6 × 37.6 mm square).
# Placed on the +Y wing, pushed as close to the +Y edge as clearances allow.
ZED_PATTERN    = 37.6
# A 90.60 mm-long rect piece sits centered on top, leaving ~53 mm of clear
# wing on each side (Y ∈ [45.30, 98.50]). Center ZED in the +Y wing zone.
ZED_Y_CENTER   = 75.5        # far holes csk ~1.1 mm wall to +Y edge
M3_CLEAR_D     = 3.4
M3_CSK_D       = 6.2
M3_CSK_DEPTH   = 1.8         # countersink on outer face

# M2 mounts on the −Y wing (from gnss_saddle_narrow/make_gnss_saddle_narrow_long.py).
# Both share Ø2.4 clearance; small lives near the −Y edge, large near the rect.
M2_CLEAR_D     = 2.4
# Small pattern (19.95 × 17.81) — pushed close to −Y edge.
M2S_PAT_X      = 19.95
M2S_PAT_Y      = 17.81
M2S_Y_CENTER   = -87.0       # far holes ~1.4 mm wall to −Y edge
# Large pattern (45.90 × 18.27) — placed between M2 small and the top rect.
M2L_PAT_X      = 45.90
M2L_PAT_Y      = 18.27
M2L_Y_CENTER   = -61.0

# Rect piece sitting on top (centered on plate, length along Y).
TOP_RECT_LEN_Y = 90.60

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived + sanity
# =============================================================================

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
TUBE_Y  = TUBE_CENTER_SEP / 2
GNSS_R  = GNSS_HOLE_D / 2

assert TUBE_Y + R_IN < BLOCK_WID / 2 - 1.0, \
    "Tube tunnel exits the block in Y (this script assumes full enclosure)"
assert R_IN + 2.0 <= HALF_HT, "Half-height too small for tube bore radius + wall"
assert GNSS_R + 2.0 < BOLT_X_OFFSET, "GNSS hole too close to clamp bolts in X"
assert abs(BOLT_Y_OFFSET) + SCREW_CLEAR_D / 2 + 1.0 < TUBE_Y - R_IN, \
    "Clamp bolts clash with tube bores"
assert GNSS_R + SCREW_CLEAR_D / 2 + 1.0 < (BOLT_X_OFFSET**2 + BOLT_Y_OFFSET**2)**0.5, \
    "GNSS hole too close to a clamp bolt (diagonal clearance)"
assert BOLT_X_OFFSET + SCREW_HEAD_D / 2 + 1.0 < BLOCK_LEN / 2, \
    "Clamp bolt heads exit the block in X"

# ZED hole sanity (4× corners at X=±ZED_PATTERN/2, Y=ZED_Y_CENTER±ZED_PATTERN/2)
_zed_x = ZED_PATTERN / 2
_zed_y_far = ZED_Y_CENTER + ZED_PATTERN / 2
_zed_y_near = ZED_Y_CENTER - ZED_PATTERN / 2
assert _zed_x + M3_CSK_D / 2 + 0.5 < BLOCK_LEN / 2, \
    "ZED holes exit block in X (countersink hits edge)"
assert _zed_y_far + M3_CSK_D / 2 + 0.5 < BLOCK_WID / 2, \
    "ZED far holes exit block in Y (countersink hits edge)"
assert _zed_y_near - M3_CSK_D / 2 > TUBE_Y + R_IN + 1.0, \
    "ZED near holes overlap tube tunnel in Y"
assert _zed_y_near - M3_CSK_D / 2 > TOP_RECT_LEN_Y / 2 + 0.5, \
    f"ZED near holes fall under the {TOP_RECT_LEN_Y} mm top rect"
assert _zed_y_far + M3_CSK_D / 2 < BLOCK_WID / 2 - 0.5, \
    "ZED far holes too close to +Y edge"
# Distance from each ZED hole to nearest M4 clamp (X=±18, Y=±18).
import math as _math
for _sy_zed in (-1, 1):
    _zhy = ZED_Y_CENTER + _sy_zed * ZED_PATTERN / 2
    _d = _math.hypot(_zed_x - BOLT_X_OFFSET, _zhy - BOLT_Y_OFFSET)
    assert _d > (SCREW_HEAD_D + M3_CSK_D) / 2 + 0.5, \
        f"ZED hole at Y={_zhy} too close to M4 clamp ({_d:.2f} mm)"

# M2 hole sanity (both small and large patterns on the −Y wing)
for _nm, _px, _py, _cy in (("M2S", M2S_PAT_X, M2S_PAT_Y, M2S_Y_CENTER),
                           ("M2L", M2L_PAT_X, M2L_PAT_Y, M2L_Y_CENTER)):
    _y_far  = _cy - _py / 2                  # more negative
    _y_near = _cy + _py / 2                  # less negative
    assert _px / 2 + M2_CLEAR_D / 2 + 0.5 < BLOCK_LEN / 2, \
        f"{_nm} holes exit block in X"
    assert -_y_far + M2_CLEAR_D / 2 + 0.5 < BLOCK_WID / 2, \
        f"{_nm} far holes exit block in −Y"
    assert -_y_near > TUBE_Y + R_IN + 1.0, \
        f"{_nm} near holes overlap tube tunnel in Y"
    assert -_y_near - M2_CLEAR_D / 2 > TOP_RECT_LEN_Y / 2 + 0.5, \
        f"{_nm} near holes fall under the {TOP_RECT_LEN_Y} mm top rect"
    for _sy in (-1, 1):
        _mhy = _cy + _sy * _py / 2
        _d = _math.hypot(_px / 2 - BOLT_X_OFFSET, _mhy - (-BOLT_Y_OFFSET))
        assert _d > (SCREW_HEAD_D + M2_CLEAR_D) / 2 + 0.5, \
            f"{_nm} hole at Y={_mhy} too close to M4 clamp ({_d:.2f} mm)"

# M2 small ↔ M2 large gap (their adjacent rows must clear M2 holes + 1 mm).
_gap = (M2L_Y_CENTER - M2L_PAT_Y / 2) - (M2S_Y_CENTER + M2S_PAT_Y / 2)
assert _gap > M2_CLEAR_D + 1.0, \
    f"M2 small and large patterns clash in Y (gap {_gap:.2f} mm)"

# =============================================================================
# Build one half
# =============================================================================

def build_half() -> Part:
    block = Box(BLOCK_LEN, BLOCK_WID, HALF_HT,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Tube tunnels — full cylinders along X at Y = ±TUBE_Y, Z = HALF_HT.
    # The half captures the lower 180° arc of each tube (full enclosure when
    # the mirrored second half is added on top).
    for sy in (-1, 1):
        bore = Cylinder(R_IN, BLOCK_LEN + 0.2,
                        rotation=(0, 90, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        block -= Pos(0.0, sy * TUBE_Y, HALF_HT) * bore

    # GNSS through-hole (Z axis), centered.
    block -= Pos(0.0, 0.0, -0.2) * Cylinder(
        GNSS_R, HALF_HT + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M4 clamp-bolt through-holes + outer-face head/nut counterbore.
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * BOLT_X_OFFSET, sy * BOLT_Y_OFFSET
            block -= Pos(cx, cy, -0.2) * Cylinder(
                SCREW_CLEAR_D / 2, HALF_HT + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            block -= Pos(cx, cy, -0.05) * Cylinder(
                SCREW_HEAD_D / 2, SCREW_HEAD_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× ZED-F9P M3 clearance holes + outer-face countersink (+Y wing).
    for sx in (-1, 1):
        for sy in (-1, 1):
            zx = sx * ZED_PATTERN / 2
            zy = ZED_Y_CENTER + sy * ZED_PATTERN / 2
            block -= Pos(zx, zy, -0.2) * Cylinder(
                M3_CLEAR_D / 2, HALF_HT + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            block -= Pos(zx, zy, -0.05) * Cylinder(
                M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M2 clearance holes per pattern (−Y wing, no countersink).
    for px, py, cy in ((M2S_PAT_X, M2S_PAT_Y, M2S_Y_CENTER),
                       (M2L_PAT_X, M2L_PAT_Y, M2L_Y_CENTER)):
        for sx in (-1, 1):
            for sy in (-1, 1):
                mx = sx * px / 2
                my = cy + sy * py / 2
                block -= Pos(mx, my, -0.2) * Cylinder(
                    M2_CLEAR_D / 2, HALF_HT + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))

    return block


def main() -> None:
    print("=" * 64)
    print("CyberWing GNSS dual-tube saddle (Y-wide 197 mm) — build123d")
    print("=" * 64)
    print(f"Block:    {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT} mm assembled")
    print(f"Tubes:    Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f} "
          f"(center-to-center {TUBE_CENTER_SEP})")
    print(f"Bore ID:  Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"GNSS:     Ø{GNSS_HOLE_D} through-hole, centered")
    print(f"Wrap:     180° per half — full tube enclosure (axial insert)")
    print(f"Bolts:    4× M4 at (±{BOLT_X_OFFSET}, ±{BOLT_Y_OFFSET})")
    print(f"ZED:      4× M3 at (±{ZED_PATTERN/2:.2f}, "
          f"{ZED_Y_CENTER - ZED_PATTERN/2:.2f}..{ZED_Y_CENTER + ZED_PATTERN/2:.2f}) "
          f"— {BLOCK_WID/2 - (ZED_Y_CENTER + ZED_PATTERN/2):.2f} mm from +Y edge")
    print(f"M2 small: 4× M2 at (±{M2S_PAT_X/2:.2f}, "
          f"{M2S_Y_CENTER - M2S_PAT_Y/2:.2f}..{M2S_Y_CENTER + M2S_PAT_Y/2:.2f}) "
          f"— {BLOCK_WID/2 - abs(M2S_Y_CENTER - M2S_PAT_Y/2):.2f} mm from −Y edge")
    print(f"M2 large: 4× M2 at (±{M2L_PAT_X/2:.2f}, "
          f"{M2L_Y_CENTER - M2L_PAT_Y/2:.2f}..{M2L_Y_CENTER + M2L_PAT_Y/2:.2f})")
    print(f"+Y wing:  {BLOCK_WID/2 - (TUBE_Y + R_IN):.2f} mm beyond tube tunnel")
    print(f"Bridge:   {2 * (TUBE_Y - R_IN):.2f} mm clear span between tubes")

    half = build_half()
    out = OUT_DIR / "gnss_saddle_wide_half.stl"
    export_stl(half, str(out))
    print(f"\n  ✓ {out.name} ({out.stat().st_size:,} bytes)")
    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Print 2 copies per saddle.")
    print("Hardware: 4× M4 × 30 mm socket caps + M4 nuts per saddle.")


if __name__ == "__main__":
    main()
