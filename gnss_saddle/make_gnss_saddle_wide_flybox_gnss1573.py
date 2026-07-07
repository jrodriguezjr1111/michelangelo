"""
CyberWing Canary — GNSS dual-tube saddle, Y-WIDE, FLY_BOX wings.
VARIANT: GNSS through-hole Ø15.73 (was Ø30) and each wing's 4× M4 fly_box
group shifted 9.7 mm toward the center (FLY_EDGE 4.20 -> 13.90).

Same body as make_gnss_saddle_wide_flybox.py otherwise (two full tube tunnels,
4× M4 tube clamps, 180° wrap per half).

Outputs:
  gnss_saddle_wide_flybox_gnss1573_half.stl   (print 2 copies, mirror-identical)
"""

from build123d import *
from pathlib import Path

# ---- saddle body (identical to the wide saddle) ----------------------------
TUBE_OD         = 15.39
TUBE_CENTER_SEP = 60.17
CLEARANCE       = 0.4
GNSS_HOLE_D     = 15.73            # was 30.0
BLOCK_LEN = 50.0            # X
BLOCK_WID = 197.0          # Y
BLOCK_HT  = 28.0           # Z assembled
BOLT_X_OFFSET    = 18.0
BOLT_Y_OFFSET    = 18.0
SCREW_CLEAR_D    = 4.4
SCREW_HEAD_D     = 8.0
SCREW_HEAD_DEPTH = 4.5

# ---- fly_box wing mount: 8× M3 HEAT-SET INSERTS ----------------------------
FLY_PAT_X = 36.14          # = GNSS-saddle / FlyCatcher-box-bottom pattern
FLY_PAT_Y = 36.10
FLY_INSERT_D     = 4.4     # M3 heat-set insert bore (PLA recommended)
FLY_INSERT_DEPTH = 6.0     # blind bore depth (fits M3 inserts up to ~5.7mm)
FLY_INSERT_CHAM  = 0.6     # lead-in chamfer at the mouth
FLY_SHIFT = 9.7           # mm each wing group moved toward center
FLY_EDGE  = 4.20 + FLY_SHIFT   # outer row inset from the ±Y plate end (13.90)

OUT_DIR = Path(__file__).parent

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
TUBE_Y  = TUBE_CENTER_SEP / 2
GNSS_R  = GNSS_HOLE_D / 2

# ---- sanity ----------------------------------------------------------------
assert TUBE_Y + R_IN < BLOCK_WID / 2 - 1.0, "tube tunnel exits the block in Y"
assert R_IN + 2.0 <= HALF_HT, "half-height too small for tube bore + wall"
assert FLY_PAT_X / 2 + FLY_INSERT_D / 2 + 0.5 < BLOCK_LEN / 2, "fly_box holes exit block in X"
assert FLY_INSERT_DEPTH < HALF_HT - 1.0, "insert bore too deep for half thickness"
_fly_outer = BLOCK_WID / 2 - FLY_EDGE
_fly_inner = _fly_outer - FLY_PAT_Y
assert _fly_outer + FLY_INSERT_D / 2 < BLOCK_WID / 2, "fly_box outer holes exit block in Y"
assert _fly_inner - FLY_INSERT_D / 2 > TUBE_Y + R_IN + 1.0, "fly_box inner holes hit the tube tunnel"
assert GNSS_R + 1.0 < TUBE_Y - R_IN, "GNSS hole hits the tube tunnel"

# ---- build one half --------------------------------------------------------
def build_half() -> Part:
    block = Box(BLOCK_LEN, BLOCK_WID, HALF_HT,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # tube tunnels (full cylinders along X)
    for sy in (-1, 1):
        bore = Cylinder(R_IN, BLOCK_LEN + 0.2, rotation=(0, 90, 0), align=(Align.CENTER,)*3)
        block -= Pos(0.0, sy * TUBE_Y, HALF_HT) * bore

    # GNSS Ø15.73 through-hole
    block -= Pos(0.0, 0.0, -0.2) * Cylinder(GNSS_R, HALF_HT + 0.4,
                                            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M4 tube-clamp holes + outer-face head counterbore
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * BOLT_X_OFFSET, sy * BOLT_Y_OFFSET
            block -= Pos(cx, cy, -0.2) * Cylinder(SCREW_CLEAR_D / 2, HALF_HT + 0.4,
                                                  align=(Align.CENTER, Align.CENTER, Align.MIN))
            block -= Pos(cx, cy, -0.05) * Cylinder(SCREW_HEAD_D / 2, SCREW_HEAD_DEPTH + 0.1,
                                                   align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 8× M3 heat-set insert bores (4 per wing, 36.14 × 36.1), shifted 9.7 mm
    # toward center. Blind from the OUTER (bed, z=0) face, with a lead-in chamfer.
    for sw in (-1, 1):
        y_outer = sw * (BLOCK_WID / 2 - FLY_EDGE)
        y_inner = y_outer - sw * FLY_PAT_Y
        for sx in (-1, 1):
            for fy in (y_inner, y_outer):
                fx = sx * FLY_PAT_X / 2
                block -= Pos(fx, fy, -0.01) * Cylinder(
                    FLY_INSERT_D / 2, FLY_INSERT_DEPTH,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
                block -= Pos(fx, fy, -0.01) * Cone(
                    FLY_INSERT_D / 2 + FLY_INSERT_CHAM, FLY_INSERT_D / 2,
                    FLY_INSERT_CHAM, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return block


def main() -> None:
    print("CyberWing GNSS wide saddle — FLY_BOX wings (GNSS Ø15.73, wings -9.7mm)")
    print(f"  block {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT}, tubes Ø{TUBE_OD} at Y±{TUBE_Y:.2f}")
    print(f"  GNSS hole: Ø{GNSS_HOLE_D} (clears tube tunnel by {TUBE_Y-R_IN-GNSS_R:.2f}mm)")
    print(f"  fly_box mount: 4× M3 heat-set inserts Ø{FLY_INSERT_D}×{FLY_INSERT_DEPTH}mm blind "
          f"per wing ({FLY_PAT_X} × {FLY_PAT_Y}); "
          f"Y rows {abs(_fly_inner):.1f} / {abs(_fly_outer):.1f} (shifted {FLY_SHIFT} toward center)")
    half = build_half()
    out = OUT_DIR / "gnss_saddle_wide_flybox_gnss1573_half.stl"
    export_stl(half, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes) — print 2 copies, outer face on bed, no supports")


if __name__ == "__main__":
    main()
