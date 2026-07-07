"""
CyberWing Canary — GNSS dual-tube saddle, Y-WIDE, FLY_BOX wings.

Same body as make_gnss_saddle_wide.py (Ø30 GNSS through-hole, 4× M4 tube
clamps, two full tube tunnels, 180° wrap per half) but each ±Y wing carries a
4× M4 fly_box mount at the GNSS / FlyCatcher-box-bottom pattern (36.14 × 36.1),
with the outer row 4.20 mm in from the plate end. (Replaces the ZED/M2 mounts.)

Outputs:
  gnss_saddle_wide_flybox_half.stl   (print 2 copies, mirror-identical)
"""

from build123d import *
from pathlib import Path

# ---- saddle body (identical to the wide saddle) ----------------------------
TUBE_OD         = 15.39
TUBE_CENTER_SEP = 60.17
CLEARANCE       = 0.4
GNSS_HOLE_D     = 30.0
BLOCK_LEN = 50.0            # X
BLOCK_WID = 197.0          # Y
BLOCK_HT  = 28.0           # Z assembled
BOLT_X_OFFSET    = 18.0
BOLT_Y_OFFSET    = 18.0
SCREW_CLEAR_D    = 4.4
SCREW_HEAD_D     = 8.0
SCREW_HEAD_DEPTH = 4.5

# ---- fly_box wing mount (NEW) ----------------------------------------------
FLY_PAT_X = 36.14          # = GNSS-saddle / FlyCatcher-box-bottom pattern
FLY_PAT_Y = 36.10
FLY_M4    = 4.4            # M4 clearance through-hole (no counterbore: 4.20 edge)
FLY_EDGE  = 4.20          # outer row inset from the ±Y plate end

OUT_DIR = Path(__file__).parent

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
TUBE_Y  = TUBE_CENTER_SEP / 2
GNSS_R  = GNSS_HOLE_D / 2

# ---- sanity ----------------------------------------------------------------
assert TUBE_Y + R_IN < BLOCK_WID / 2 - 1.0, "tube tunnel exits the block in Y"
assert R_IN + 2.0 <= HALF_HT, "half-height too small for tube bore + wall"
assert FLY_PAT_X / 2 + FLY_M4 / 2 + 0.5 < BLOCK_LEN / 2, "fly_box holes exit block in X"
_fly_outer = BLOCK_WID / 2 - FLY_EDGE
_fly_inner = _fly_outer - FLY_PAT_Y
assert _fly_outer + FLY_M4 / 2 < BLOCK_WID / 2, "fly_box outer holes exit block in Y"
assert _fly_inner - FLY_M4 / 2 > TUBE_Y + R_IN + 1.0, "fly_box inner holes hit the tube tunnel"

# ---- build one half --------------------------------------------------------
def build_half() -> Part:
    block = Box(BLOCK_LEN, BLOCK_WID, HALF_HT,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # tube tunnels (full cylinders along X)
    for sy in (-1, 1):
        bore = Cylinder(R_IN, BLOCK_LEN + 0.2, rotation=(0, 90, 0), align=(Align.CENTER,)*3)
        block -= Pos(0.0, sy * TUBE_Y, HALF_HT) * bore

    # GNSS Ø30 through-hole
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

    # 4× M4 fly_box mount per wing (36.14 × 36.1), outer row 4.20 from the ±Y end
    for sw in (-1, 1):
        y_outer = sw * (BLOCK_WID / 2 - FLY_EDGE)
        y_inner = y_outer - sw * FLY_PAT_Y
        for sx in (-1, 1):
            for fy in (y_inner, y_outer):
                fx = sx * FLY_PAT_X / 2
                block -= Pos(fx, fy, -0.2) * Cylinder(FLY_M4 / 2, HALF_HT + 0.4,
                                                      align=(Align.CENTER, Align.CENTER, Align.MIN))
    return block


def main() -> None:
    print("CyberWing GNSS wide saddle — FLY_BOX wings")
    print(f"  block {BLOCK_LEN} × {BLOCK_WID} × {BLOCK_HT}, tubes Ø{TUBE_OD} at Y±{TUBE_Y:.2f}")
    print(f"  fly_box mount: 4× M4 {FLY_PAT_X} × {FLY_PAT_Y} per wing; "
          f"Y rows {abs(_fly_inner):.1f} / {abs(_fly_outer):.1f} (outer {FLY_EDGE} from end)")
    half = build_half()
    out = OUT_DIR / "gnss_saddle_wide_flybox_half.stl"
    export_stl(half, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes) — print 2 copies, outer face on bed, no supports")


if __name__ == "__main__":
    main()
