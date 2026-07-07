"""
Stacked base — ZED-F9P + IMU carrier variant (was LILYGO SX1262 base).

Same 101 × 65 × 13 envelope, repurposed to carry a ZED-F9P breakout and an IMU
inside the cavity. Sits ON TOP of `flycatcher/imu_platform_saddle.stl` and is
fastened by 4× M4 through the floor at the saddle's 36.14 × 36.1 pattern.

  Outer:   101 × 65 × 27 mm
  Walls:   3 mm; floor: 4 mm
  Cavity:  95 × 59 × 23 mm (open top)

Stack (bottom → top):
  GNSS tube clamp → imu_platform_saddle → THIS BASE (ZED + IMU inside)
  → LILYGO board / top plate on the M2 bosses above the top face.

Current layout:
  - 4× M4 mount holes (Ø4.4) through the floor at 36.14 × 36.1, CENTERED —
    matches the saddle's M4 holes. Screws drop from inside the cavity (heads on
    the floor, UNDER the ZED board) down through the saddle into the tube clamp.
  - ZED-F9P on 4× Ø7 × 6 bosses (37.6 sq, M3 self-tap); the 6 mm boss height
    clears the M4 cap heads (≈4 mm) beneath the board.
  - IMU on 4× Ø4 × 4 standoffs (19.95 × 17.81, M2 self-tap).
  - EVEN X SPACING: wall → ZED (45) → IMU (22) → wall with three equal
    ~9.33 mm gaps (ZED at X ≈ -15.67, IMU at X ≈ +27.17).
  - M2 LILYGO bosses (95.33 × 28.55, Ø4.5 × 5) restored above the top face for
    the top plate; Ø2.4 clearance holes run all the way through.
  - 4× M3 corner bosses (Ø6, full cavity height, fused into the cavity
    corners) with Ø3.4 through-holes and csk on the TOP face.
  - M3 58 × 49 attach holes REMOVED (replaced by the M4 saddle mount).
"""

from build123d import *
from pathlib import Path

# =============================================================================
# Envelope
# =============================================================================
BASE_L = 101.0          # X — matches flycatcher saddle PLATE_L
BASE_W = 65.0           # Y — matches flycatcher saddle PLATE_W
BASE_H = 27.0           # Z

WALL_T  = 3.0
FLOOR_T = 4.0

CAV_L = BASE_L - 2 * WALL_T   # 95
CAV_W = BASE_W - 2 * WALL_T   # 59
CAV_H = BASE_H - FLOOR_T      # 9

# =============================================================================
# M4 saddle mount — 36.14 × 36.1 pattern, CENTERED (matches the M4 holes in
# flycatcher/make_imu_platform_saddle.py). Plain Ø4.4 through-holes in the
# floor; cap heads sit on the cavity floor under the ZED board.
# =============================================================================
M4_PAT_X   = 36.14
M4_PAT_Y   = 36.1
M4_CLEAR_D = 4.4
M4_HEAD_D  = 7.0        # cap head Ø (keep-out under the board)
M4_HEAD_H  = 4.0        # cap head height (sets min ZED boss height)

M4_POS = [(sx * M4_PAT_X / 2, sy * M4_PAT_Y / 2)
          for sx in (-1, 1) for sy in (-1, 1)]

# =============================================================================
# Board placement — EVEN SPACING along X: equal gaps wall → ZED board →
# IMU board → wall. Gap = (CAV_L − ZED_BOARD − IMU_BOARD) / 3.
# =============================================================================
ZED_BOARD = 45.0         # ZED envelope (keep-out) per side
IMU_BOARD = 22.0         # IMU envelope along X

X_GAP = (CAV_L - ZED_BOARD - IMU_BOARD) / 3            # 9.33
ZED_X_CENTER = -CAV_L / 2 + X_GAP + ZED_BOARD / 2      # -15.67
IMU_X_CENTER = ZED_X_CENTER + ZED_BOARD / 2 + X_GAP + IMU_BOARD / 2   # +27.17

# ZED-F9P bosses (cavity floor) — 37.6 mm square pattern, M3 self-tap.
ZED_PAT       = 37.6
ZED_SO_OD     = 7.0      # boss OD
ZED_SO_H      = 6.0      # boss height — clears the M4 cap heads under the board
ZED_SO_PILOT  = 2.5      # M3 self-tap

# IMU standoffs (cavity floor) — 19.95 × 17.81 pattern, M2 self-tap.
IMU_PAT_X     = 19.95
IMU_PAT_Y     = 17.81
IMU_SO_OD     = 4.0
IMU_SO_H      = 4.0
IMU_SO_PILOT  = 1.6      # M2 self-tap
IMU_ZED_GAP_MIN = 3.0    # required gap: ZED board envelope → IMU standoff

# =============================================================================
# USB-C cable opening + antenna hole — on the −Y wall, in front of the ZED.
# (Cannot live on a ±X wall: the M2 LILYGO channels at Y=±14.275 leave only
# ~26 mm clear, less than the 28 mm head.) Hole sits to the RIGHT of the slot
# when viewing the −Y wall from outside (+X direction).
# =============================================================================
USB_W   = 28.0           # along X (cable head width)
USB_H   = 13.0           # along Z (cable head height)
USB_XC  = ZED_X_CENTER   # centered on the ZED board
USB_Z0  = FLOOR_T        # slot bottom at the cavity floor

ANT_D   = 6.21           # antenna / cable passthrough
ANT_GAP = 3.0            # web between slot edge and hole
ANT_XC  = USB_XC + USB_W / 2 + ANT_GAP + ANT_D / 2     # +4.44
ANT_ZC  = USB_Z0 + USB_H / 2                            # 10.5

# IMU cable cutout — same (−Y) wall, centered on the IMU.
IMU_CUT_W  = 14.0        # along X (JST/Qwiic-class cable head)
IMU_CUT_H  = 10.0        # along Z
IMU_CUT_XC = IMU_X_CENTER                               # +27.17
IMU_CUT_Z0 = FLOOR_T     # bottom at the cavity floor

# =============================================================================
# M3 corner bosses — Ø6 columns fused into the 4 cavity corners, full cavity
# height, Ø3.4 through-hole with csk on the TOP face.
# =============================================================================
CB_OD        = 6.0
CB_CLEAR_D   = 3.4
CB_CSK_D     = 6.0
CB_CSK_DEPTH = 1.8
CB_EMBED     = 0.5      # boss center pushed into the corner for solid fusion
CB_POS = [(sx * (CAV_L / 2 - CB_OD / 2 + CB_EMBED),
           sy * (CAV_W / 2 - CB_OD / 2 + CB_EMBED))
          for sx in (-1, 1) for sy in (-1, 1)]

# =============================================================================
# M2 LILYGO bosses — above the top face, for the LILYGO board / top plate
# (restored from the original variant; matches make_top.py).
# =============================================================================
M2_PATTERN_X = 95.33
M2_PATTERN_Y = 28.55
M2_CLEAR_D   = 2.4
M2_BOSS_D    = 4.5      # boss OD
M2_BOSS_H    = 5.0      # boss height above the top face

OUT_DIR = Path(__file__).parent

# =============================================================================
# Sanity
# =============================================================================
assert M4_PAT_X / 2 + M4_CLEAR_D / 2 + 1 < CAV_L / 2, "M4 hole too close to cavity X wall"
assert M4_PAT_Y / 2 + M4_CLEAR_D / 2 + 1 < CAV_W / 2, "M4 hole too close to cavity Y wall"
assert ZED_SO_H > M4_HEAD_H + 1.0, "ZED bosses too short to clear M4 cap heads"

# ZED bosses inside cavity, clear of the M4 holes
for _sx in (-1, 1):
    for _sy in (-1, 1):
        _x, _y = ZED_X_CENTER + _sx * ZED_PAT / 2, _sy * ZED_PAT / 2
        assert abs(_x) + ZED_SO_OD / 2 < CAV_L / 2, "ZED boss hits cavity X wall"
        assert abs(_y) + ZED_SO_OD / 2 < CAV_W / 2, "ZED boss hits cavity Y wall"
        for _bx, _by in M4_POS:
            _d = ((_x - _bx) ** 2 + (_y - _by) ** 2) ** 0.5
            assert _d > ZED_SO_OD / 2 + M4_CLEAR_D / 2 + 0.8, "ZED boss covers an M4 hole"

# IMU standoffs inside cavity, spaced off the ZED board, clear of M4 holes
for _sx in (-1, 1):
    for _sy in (-1, 1):
        _x, _y = IMU_X_CENTER + _sx * IMU_PAT_X / 2, _sy * IMU_PAT_Y / 2
        assert abs(_x) + IMU_SO_OD / 2 < CAV_L / 2, "IMU standoff hits cavity X wall"
        assert abs(_y) + IMU_SO_OD / 2 < CAV_W / 2, "IMU standoff hits cavity Y wall"
        assert _x - IMU_SO_OD / 2 > ZED_X_CENTER + ZED_BOARD / 2 + IMU_ZED_GAP_MIN, \
            "IMU standoff too close to ZED board envelope"
        for _bx, _by in M4_POS:
            _d = ((_x - _bx) ** 2 + (_y - _by) ** 2) ** 0.5
            assert _d > IMU_SO_OD / 2 + M4_HEAD_D / 2 + 0.8, "IMU standoff clashes an M4 head"

# M2 bosses on the rim
assert M2_PATTERN_X / 2 + M2_BOSS_D / 2 <= BASE_L / 2, "M2 boss hits X edge"
assert M2_PATTERN_Y / 2 + M2_BOSS_D / 2 <= BASE_W / 2, "M2 boss hits Y edge"

# USB-C slot + antenna hole on the −Y wall
assert USB_Z0 + USB_H + 2.0 < BASE_H, "USB slot leaves <2 mm of wall above (bridge band)"
_cb_inner_x = abs(CB_POS[0][0]) - CB_OD / 2     # corner boss inner X edge (42.0)
assert abs(USB_XC) + USB_W / 2 < _cb_inner_x - 1, "USB slot reaches a corner boss"
assert ANT_XC + ANT_D / 2 < _cb_inner_x - 1, "Antenna hole reaches a corner boss"
assert ANT_XC - ANT_D / 2 - (USB_XC + USB_W / 2) >= 2.0, "Antenna hole too close to USB slot"
assert ANT_ZC + ANT_D / 2 < BASE_H - 1 and ANT_ZC - ANT_D / 2 > FLOOR_T - 0.1, \
    "Antenna hole exits the wall in Z"

# IMU cutout on the −Y wall
assert IMU_CUT_Z0 + IMU_CUT_H + 2.0 < BASE_H, "IMU cutout leaves <2 mm of wall above"
assert IMU_CUT_XC - IMU_CUT_W / 2 - (ANT_XC + ANT_D / 2) >= 2.0, \
    "IMU cutout too close to the antenna hole"
assert IMU_CUT_XC + IMU_CUT_W / 2 < _cb_inner_x - 1, "IMU cutout reaches a corner boss"

# Corner bosses clear the boards, ZED bosses, IMU standoffs, and M2 holes
for _cbx, _cby in CB_POS:
    for _sx in (-1, 1):
        for _sy in (-1, 1):
            _zx, _zy = ZED_X_CENTER + _sx * ZED_PAT / 2, _sy * ZED_PAT / 2
            assert ((_cbx - _zx) ** 2 + (_cby - _zy) ** 2) ** 0.5 > CB_OD / 2 + ZED_SO_OD / 2 + 1, \
                "Corner boss clashes a ZED boss"
            _ix, _iy = IMU_X_CENTER + _sx * IMU_PAT_X / 2, _sy * IMU_PAT_Y / 2
            assert ((_cbx - _ix) ** 2 + (_cby - _iy) ** 2) ** 0.5 > CB_OD / 2 + IMU_SO_OD / 2 + 1, \
                "Corner boss clashes an IMU standoff"
            _mx, _my = _sx * M2_PATTERN_X / 2, _sy * M2_PATTERN_Y / 2
            assert ((_cbx - _mx) ** 2 + (_cby - _my) ** 2) ** 0.5 > CB_CSK_D / 2 + M2_CLEAR_D / 2 + 1, \
                "Corner boss csk clashes an M2 hole"
    # board envelopes (rectangular keep-outs)
    _dzx = abs(_cbx - ZED_X_CENTER) - ZED_BOARD / 2
    _dzy = abs(_cby) - ZED_BOARD / 2
    assert max(_dzx, _dzy) > CB_OD / 2, "Corner boss under the ZED board"


def build_base() -> Part:
    body = Box(BASE_L, BASE_W, BASE_H,
               align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Hollow inner cavity (open top)
    body -= Pos(0, 0, FLOOR_T) * Box(
        CAV_L, CAV_W, CAV_H + 1.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # M4 saddle-mount holes through the floor (heads inside the cavity).
    for cx, cy in M4_POS:
        body -= Pos(cx, cy, -0.2) * Cylinder(
            M4_CLEAR_D / 2, FLOOR_T + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # ZED-F9P bosses on the cavity floor (M3 self-tap pilots).
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = ZED_X_CENTER + sx * ZED_PAT / 2, sy * ZED_PAT / 2
            body += Pos(cx, cy, FLOOR_T) * Cylinder(
                ZED_SO_OD / 2, ZED_SO_H,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= Pos(cx, cy, FLOOR_T) * Cylinder(
                ZED_SO_PILOT / 2, ZED_SO_H + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # IMU standoffs on the cavity floor (M2 self-tap pilots).
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = IMU_X_CENTER + sx * IMU_PAT_X / 2, sy * IMU_PAT_Y / 2
            body += Pos(cx, cy, FLOOR_T) * Cylinder(
                IMU_SO_OD / 2, IMU_SO_H,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= Pos(cx, cy, FLOOR_T) * Cylinder(
                IMU_SO_PILOT / 2, IMU_SO_H + 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # USB-C cable opening on the −Y wall (slot) + Ø6.21 antenna hole to its
    # right (viewed from outside the −Y wall).
    body -= Pos(USB_XC, -BASE_W / 2 - 0.2, USB_Z0) * Box(
        USB_W, WALL_T + 0.4, USB_H,
        align=(Align.CENTER, Align.MIN, Align.MIN))
    body -= Pos(ANT_XC, -BASE_W / 2 + WALL_T / 2, ANT_ZC) * Cylinder(
        ANT_D / 2, WALL_T + 0.4,
        rotation=(90, 0, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER))

    # IMU cable cutout on the −Y wall.
    body -= Pos(IMU_CUT_XC, -BASE_W / 2 - 0.2, IMU_CUT_Z0) * Box(
        IMU_CUT_W, WALL_T + 0.4, IMU_CUT_H,
        align=(Align.CENTER, Align.MIN, Align.MIN))

    # M3 corner bosses — full cavity height, csk on the top face.
    for cx, cy in CB_POS:
        body += Pos(cx, cy, FLOOR_T) * Cylinder(
            CB_OD / 2, CAV_H,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        body -= Pos(cx, cy, -0.2) * Cylinder(
            CB_CLEAR_D / 2, BASE_H + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        body -= Pos(cx, cy, BASE_H - CB_CSK_DEPTH) * Cylinder(
            CB_CSK_D / 2, CB_CSK_DEPTH + 0.1,
            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # M2 LILYGO bosses above the top face (top plate), clearance holes through.
    hx, hy = M2_PATTERN_X / 2, M2_PATTERN_Y / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * hx, sy * hy
            body += Pos(cx, cy, BASE_H) * Cylinder(
                M2_BOSS_D / 2, M2_BOSS_H,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            body -= Pos(cx, cy, -0.2) * Cylinder(
                M2_CLEAR_D / 2, BASE_H + M2_BOSS_H + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return body


if __name__ == "__main__":
    part = build_base()
    out = OUT_DIR / "lilygo_sx1262_base_stacked.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Base outer: {BASE_L} × {BASE_W} × {BASE_H} mm  (ZED-F9P + IMU carrier)")
    print(f"  Cavity:     {CAV_L} × {CAV_W} × {CAV_H} mm (open top)")
    print(f"  M4 mount:   4× Ø{M4_CLEAR_D} floor holes at {M4_PAT_X} × {M4_PAT_Y} CENTERED "
          f"(matches imu_platform_saddle M4); heads inside, under the ZED board")
    print(f"  ZED-F9P:    4× Ø{ZED_SO_OD}×{ZED_SO_H} bosses, {ZED_SO_PILOT} pilot "
          f"(M3 self-tap), {ZED_PAT} sq at X={ZED_X_CENTER:+.1f}")
    print(f"  IMU:        4× Ø{IMU_SO_OD}×{IMU_SO_H} standoffs, {IMU_SO_PILOT} pilot "
          f"(M2 self-tap), {IMU_PAT_X} × {IMU_PAT_Y} at X={IMU_X_CENTER:+.1f}")
    print(f"  Spacing:    even — wall | {X_GAP:.2f} | ZED {ZED_BOARD} | {X_GAP:.2f} "
          f"| IMU {IMU_BOARD} | {X_GAP:.2f} | wall")
    print(f"  USB-C slot: {USB_W} × {USB_H} mm on −Y wall at X={USB_XC:+.2f}, "
          f"z {USB_Z0}–{USB_Z0 + USB_H}")
    print(f"  Ant hole:   Ø{ANT_D} on −Y wall at X={ANT_XC:+.2f}, z={ANT_ZC} "
          f"(right of the slot, {ANT_GAP} mm web)")
    print(f"  IMU cutout: {IMU_CUT_W} × {IMU_CUT_H} mm on −Y wall at X={IMU_CUT_XC:+.2f}, "
          f"z {IMU_CUT_Z0}–{IMU_CUT_Z0 + IMU_CUT_H}")
    print(f"  M3 corner:  4× Ø{CB_CLEAR_D} through in Ø{CB_OD} corner bosses at "
          f"(±{abs(CB_POS[0][0]):.1f}, ±{abs(CB_POS[0][1]):.1f}), "
          f"csk Ø{CB_CSK_D}×{CB_CSK_DEPTH} on TOP face")
    print(f"  M2 LILYGO:  4× Ø{M2_CLEAR_D} at {M2_PATTERN_X}×{M2_PATTERN_Y}, "
          f"Ø{M2_BOSS_D}×{M2_BOSS_H} bosses above the top face (top plate)")
    print(f"  Sits on flycatcher/imu_platform_saddle.stl; M3 58×49 attach holes removed.")
