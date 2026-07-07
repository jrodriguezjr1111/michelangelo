"""
CyberWing Canary — IMU housing (ISM330DHCX + XIAO ESP32-S3) v1.

Two-part enclosure:
  - body: base + walls + interior features (cradle, standoffs, strain rib)
  - lid:  cap with M2 corner holes, light pipe, and XIAO down-force rib

Coordinate frame (model == print orientation):
  X = housing length.  -X face has the USB-C cable exit, +X face is IMU end
      (= aircraft "forward" when mounted to sub-panel).
  Y = housing width.
  Z = build direction.  Body: z=0 is the BOTTOM (sub-panel side), cavity
      opens upward.  Lid: z=0 is the OUTER top face; rib/bosses point down
      when installed but print upward (inside face up on the bed).

Print orientation:
  body: base-on-bed, interior up.   No supports needed.
  lid:  inside-face-up, rib points up.  No supports.

Outputs:
  housing_body.stl
  housing_lid.stl
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

# Outer envelope
OUTER_L = 88.0            # X, length (extra room for Qwiic cable bend
                          #         between XIAO and IMU)
OUTER_W = 40.0            # Y, width
OUTER_H = 18.0            # Z, total height (body + lid)

# Shell thicknesses
WALL    = 2.0
BASE_H  = 3.0
LID_H   = 2.0

# --- Sub-panel mount (4× M3 through-holes, countersunk from inside cavity) ---
PANEL_PATTERN_L = 65.0    # X spacing between M3 holes
PANEL_PATTERN_W = 30.0    # Y spacing between M3 holes
M3_CLEAR_D      = 3.4
M3_CSK_D        = 5.8     # socket-cap counterbore diameter
M3_CSK_DEPTH    = 3.0     # counterbore depth into cavity floor

# --- Lid attachment (4× M2 heat-set inserts in body corners) ---
LID_SCREW_INSET = 4.0     # distance from outer wall to screw center, both X and Y
M2_INSERT_D     = 3.2     # heat-set insert through-hole diameter (tapered OK)
M2_INSERT_DEPTH = 4.0     # insert cavity depth from top of boss
M2_CLEAR_D      = 2.4     # lid clearance for M2 shank

# --- Pure internal Qwiic wiring (no external Qwiic cable).
#     The ISM330DHCX has Qwiic / I²C connectors on BOTH −X and +X short
#     edges; both are wired to the XIAO inside the housing.
QWIIC_CONN_H        = 3.0   # JST-SH plug body height above PCB
QWIIC_PLUG_X        = 6.0   # plug body length along the cable axis (X)
# XIAO cradle opening on -X side (USB-C connector overhang clearance)
CRADLE_OPENING_W    = 10.0  # must be ≥ USBC_SLOT_W so plug can reach receptacle

# --- USB-C cutout in -X wall (for flashing / serial access to the XIAO) ---
USBC_SLOT_W   = 10.0    # Y, accepts a USB-C plug shroud (~9 mm + clearance)
USBC_SLOT_H   = 6.0     # Z, plug shroud height (~7 mm minus a bit, slot opens to lid seat
                        # if needed via the cavity above)
USBC_SLOT_Z   = 0.0     # bottom of slot above cavity floor; 0 = at floor

# --- XIAO ESP32-S3 clamp cradle ---
XIAO_L          = 21.17   # PCB length (USB-C edge to opposite edge, PCB only)
XIAO_W          = 17.93
XIAO_T          = 1.60    # PCB thickness
XIAO_USBC_OH    = 1.5     # USB-C connector overhang past PCB short edge
XIAO_FIT        = 0.30    # lateral fit
CRADLE_FENCE_H  = 2.0     # wall height around PCB
CRADLE_FENCE_W  = 1.0     # wall thickness
XIAO_LED_OFFSET = (4.0, -3.5)  # (dx, dy) from PCB center, for light-pipe alignment

# --- ISM330DHCX standoffs ---
IMU_PCB_L       = 25.53
IMU_PCB_W       = 25.42
IMU_HOLE_PAT_L  = 20.45
IMU_HOLE_PAT_W  = 20.45
IMU_STANDOFF_H  = 3.0     # brass standoff height (PCB sits this high above floor)
IMU_BOSS_OD     = 4.4     # boss outer diameter
IMU_BOSS_HOLE_D = 3.2     # for M2 heat-set insert (same as lid inserts)
IMU_BOSS_HOLE_DEPTH = 4.0

# --- Gasket groove on lid seating face (optional) ---
USE_GASKET_GROOVE = True
GASKET_GROOVE_W   = 1.5
GASKET_GROOVE_D   = 1.0
GASKET_GROOVE_INSET_FROM_WALL = 1.0

# --- Outer corner fillet (reduces base warping during print) ---
CORNER_FILLET_R = 5.0

# --- Lid features ---
LED_PIPE_D        = 3.0   # Ø3 mm hole through lid over XIAO LED
LID_RIB_H         = None  # auto-computed so it presses PCB top
LID_RIB_W         = 8.0   # rib width (along X)
LID_RIB_L         = 12.0  # rib length (along Y)

OUT_DIR = Path(__file__).parent


# =============================================================================
# Derived geometry
# =============================================================================

CAVITY_L = OUTER_L - 2 * WALL
CAVITY_W = OUTER_W - 2 * WALL
CAVITY_H = OUTER_H - BASE_H - LID_H  # interior clear height

# Body extends z = 0 .. (BASE_H + CAVITY_H) = OUTER_H - LID_H
BODY_H = OUTER_H - LID_H
# Cavity floor is at z = BASE_H.

# XIAO placement: 2 mm clearance between USB-C overhang tip and -X wall
XIAO_CENTER_X  = -OUTER_L / 2 + WALL + XIAO_USBC_OH + 2.0 + XIAO_L / 2
XIAO_CENTER_Y  = 0.0

# IMU placement: centered between the XIAO's +X edge and the +X inner
# wall, so equal clearance on both −X and +X sides of the IMU PCB. Both
# Qwiic plugs + their cables route in those gaps back to the XIAO.
_xiao_plus_x = XIAO_CENTER_X + XIAO_L / 2
_inner_plus_x = OUTER_L / 2 - WALL
IMU_CENTER_X   = (_xiao_plus_x + _inner_plus_x) / 2
IMU_CENTER_Y   = 0.0
IMU_LEFT_CLEAR  = IMU_CENTER_X - IMU_PCB_L / 2 - _xiao_plus_x
IMU_RIGHT_CLEAR = _inner_plus_x - (IMU_CENTER_X + IMU_PCB_L / 2)

# IMU PCB top Z (used by the preview to draw the Qwiic connector heights)
IMU_PCB_TOP_Z  = BASE_H + IMU_STANDOFF_H + 1.6           # 1.6 mm PCB thickness

# Sanity checks
assert XIAO_CENTER_X + XIAO_L / 2 < IMU_CENTER_X - IMU_PCB_L / 2, \
    "XIAO and IMU overlap in X — make OUTER_L larger or move components"
assert IMU_PCB_W + 2 * IMU_BOSS_OD < CAVITY_W, \
    "IMU + standoffs exceed cavity width"
assert PANEL_PATTERN_L + M3_CSK_D <= OUTER_L - 2 * WALL, \
    "Sub-panel X pattern too wide for base"
assert PANEL_PATTERN_W + M3_CSK_D <= OUTER_W - 2 * WALL, \
    "Sub-panel Y pattern too wide for base"

if LID_RIB_H is None:
    # Rib should contact PCB top: PCB top at z = BASE_H + XIAO_T
    # (PCB sits directly on cavity floor inside fence; fence is taller than PCB
    # by design so the rib lands on PCB, not fence)
    pcb_top_z = BASE_H + XIAO_T
    lid_inside_z = OUTER_H - LID_H
    # rib extends from lid inside face DOWN to pcb_top_z
    LID_RIB_H = lid_inside_z - pcb_top_z  # prints UP during lid print


# =============================================================================
# Body
# =============================================================================

def build_body() -> Part:
    # Solid outer block from z=0 to z=BODY_H, with vertical corners filleted
    body = Box(OUTER_L, OUTER_W, BODY_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    body = fillet(body.edges().filter_by(Axis.Z), CORNER_FILLET_R)

    # --- Cavity: subtract from z=BASE_H up to z=BODY_H ---
    cavity = Box(CAVITY_L, CAVITY_W, CAVITY_H + 1,
                 align=(Align.CENTER, Align.CENTER, Align.MIN))
    cavity = Pos(0, 0, BASE_H) * cavity
    body -= cavity

    # --- USB-C cutout through -X wall (XIAO programming / serial access) ---
    usbc_cut = Box(WALL + 0.4, USBC_SLOT_W, USBC_SLOT_H,
                   align=(Align.MIN, Align.CENTER, Align.MIN))
    usbc_cut = Pos(-OUTER_L / 2 - 0.1, 0,
                   BASE_H + USBC_SLOT_Z) * usbc_cut
    body -= usbc_cut

    # --- XIAO cradle fence (rectangular frame around PCB, 3 sides; open toward -X) ---
    fence_L = XIAO_L + 2 * XIAO_FIT + 2 * CRADLE_FENCE_W
    fence_W = XIAO_W + 2 * XIAO_FIT + 2 * CRADLE_FENCE_W
    fence_outer = Box(fence_L, fence_W, CRADLE_FENCE_H,
                      align=(Align.CENTER, Align.CENTER, Align.MIN))
    fence_outer = Pos(XIAO_CENTER_X, XIAO_CENTER_Y, BASE_H) * fence_outer
    fence_inner = Box(XIAO_L + 2 * XIAO_FIT, XIAO_W + 2 * XIAO_FIT, CRADLE_FENCE_H + 0.2,
                      align=(Align.CENTER, Align.CENTER, Align.MIN))
    fence_inner = Pos(XIAO_CENTER_X, XIAO_CENTER_Y, BASE_H - 0.1) * fence_inner
    fence = fence_outer - fence_inner
    # Open the -X fence segment so USB-C connector overhang is clear
    opening = Box(CRADLE_FENCE_W + 0.2, CRADLE_OPENING_W, CRADLE_FENCE_H + 0.2,
                  align=(Align.MIN, Align.CENTER, Align.MIN))
    opening = Pos(XIAO_CENTER_X - fence_L / 2 - 0.1, 0, BASE_H - 0.1) * opening
    fence -= opening
    body += fence

    # --- IMU standoffs: 4× bosses with M2 heat-set insert holes ---
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = IMU_CENTER_X + sx * IMU_HOLE_PAT_L / 2
            cy = IMU_CENTER_Y + sy * IMU_HOLE_PAT_W / 2
            boss = Cylinder(IMU_BOSS_OD / 2, IMU_STANDOFF_H,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            boss = Pos(cx, cy, BASE_H) * boss
            body += boss
            hole = Cylinder(IMU_BOSS_HOLE_D / 2, IMU_BOSS_HOLE_DEPTH + 0.1,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            hole = Pos(cx, cy, BASE_H + IMU_STANDOFF_H - IMU_BOSS_HOLE_DEPTH) * hole
            body -= hole

    # --- 4× lid heat-set insert bosses at corners ---
    # Boss merges into the outer walls naturally (they are within the wall envelope).
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = sx * (OUTER_L / 2 - LID_SCREW_INSET)
            cy = sy * (OUTER_W / 2 - LID_SCREW_INSET)
            # Boss sticks UP from cavity floor to just below lid seating face
            boss_h = CAVITY_H  # full cavity height
            boss = Cylinder(LID_SCREW_INSET * 0.9, boss_h,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            boss = Pos(cx, cy, BASE_H) * boss
            body += boss
            # Heat-set hole from TOP of boss (= lid seating face) going down
            insert = Cylinder(M2_INSERT_D / 2, M2_INSERT_DEPTH + 0.1,
                              align=(Align.CENTER, Align.CENTER, Align.MIN))
            insert = Pos(cx, cy, BODY_H - M2_INSERT_DEPTH) * insert
            body -= insert

    # --- Sub-panel mount: 4× M3 through-holes + counterbore on cavity floor ---
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = sx * PANEL_PATTERN_L / 2
            cy = sy * PANEL_PATTERN_W / 2
            thru = Cylinder(M3_CLEAR_D / 2, BASE_H + 0.2,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            thru = Pos(cx, cy, -0.1) * thru
            body -= thru
            csk = Cylinder(M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
                           align=(Align.CENTER, Align.CENTER, Align.MIN))
            csk = Pos(cx, cy, BASE_H - M3_CSK_DEPTH) * csk
            body -= csk

    # --- Gasket groove on top face of body (lid seating) ---
    if USE_GASKET_GROOVE:
        inset = GASKET_GROOVE_INSET_FROM_WALL + GASKET_GROOVE_W / 2
        outer = Box(OUTER_L - 2 * inset, OUTER_W - 2 * inset, GASKET_GROOVE_D + 0.1,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
        inner = Box(OUTER_L - 2 * inset - 2 * GASKET_GROOVE_W,
                    OUTER_W - 2 * inset - 2 * GASKET_GROOVE_W,
                    GASKET_GROOVE_D + 0.2,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
        groove = outer - inner
        groove = Pos(0, 0, BODY_H - GASKET_GROOVE_D) * groove
        body -= groove

    return body


# =============================================================================
# Lid
# =============================================================================

def build_lid() -> Part:
    lid = Box(OUTER_L, OUTER_W, LID_H,
              align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M2 clearance holes at corners
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = sx * (OUTER_L / 2 - LID_SCREW_INSET)
            cy = sy * (OUTER_W / 2 - LID_SCREW_INSET)
            hole = Cylinder(M2_CLEAR_D / 2, LID_H + 0.2,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            hole = Pos(cx, cy, -0.1) * hole
            lid -= hole

    # Light pipe hole over XIAO user LED
    led_x = XIAO_CENTER_X + XIAO_LED_OFFSET[0]
    led_y = XIAO_CENTER_Y + XIAO_LED_OFFSET[1]
    pipe = Cylinder(LED_PIPE_D / 2, LID_H + 0.2,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
    pipe = Pos(led_x, led_y, -0.1) * pipe
    lid -= pipe

    # Down-force rib pressing XIAO PCB top (prints upward when lid is
    # printed inside-face-up on the bed — no supports)
    rib = Box(LID_RIB_W, LID_RIB_L, LID_RIB_H,
              align=(Align.CENTER, Align.CENTER, Align.MIN))
    rib = Pos(XIAO_CENTER_X, XIAO_CENTER_Y, LID_H) * rib
    lid += rib

    return lid


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("CyberWing IMU housing — build123d generator")
    print("=" * 60)
    print(f"Outer:         {OUTER_L} × {OUTER_W} × {OUTER_H} mm")
    print(f"Cavity:        {CAVITY_L} × {CAVITY_W} × {CAVITY_H} mm")
    print(f"Panel mount:   4× M3 at {PANEL_PATTERN_L} × {PANEL_PATTERN_W} (counterbored from inside)")
    print(f"IMU mount:     4× M2 standoffs at {IMU_HOLE_PAT_L} × {IMU_HOLE_PAT_W} (board {IMU_PCB_L} × {IMU_PCB_W})")
    print(f"XIAO cradle:   {XIAO_L} × {XIAO_W} + {XIAO_FIT} fit, fence {CRADLE_FENCE_H} tall")
    xiao_to_imu = (IMU_CENTER_X - IMU_PCB_L / 2) - (XIAO_CENTER_X + XIAO_L / 2)
    imu_to_wall = OUTER_L / 2 - (IMU_CENTER_X + IMU_PCB_L / 2) - WALL
    print(f"Cable exit:    USB-C only ({USBC_SLOT_W} × {USBC_SLOT_H} mm in −X wall, for XIAO flashing)")
    print(f"IMU clearance: −X = {IMU_LEFT_CLEAR:.2f} mm  |  +X = {IMU_RIGHT_CLEAR:.2f} mm  (cable + plug)")
    print(f"Lid:           4× M2 heat-set at corners, rib height {LID_RIB_H:.1f} mm")
    print(f"Gasket groove: {'on' if USE_GASKET_GROOVE else 'off'}")
    print()

    body = build_body()
    body_path = OUT_DIR / "housing_body.stl"
    export_stl(body, str(body_path))
    print(f"  ✓ {body_path.name} ({body_path.stat().st_size:,} bytes)")

    lid = build_lid()
    lid_path = OUT_DIR / "housing_lid.stl"
    export_stl(lid, str(lid_path))
    print(f"  ✓ {lid_path.name} ({lid_path.stat().st_size:,} bytes)")

    print("\nPrint orientation (already set):")
    print("  body: base on bed, cavity opens upward → no supports")
    print("  lid:  inside-face-up (rib prints upward) → no supports")
    print("\nHardware BOM:")
    print("  - 4× M2 heat-set inserts + 4× M2 × 6 mm screws (lid)")
    print("  - 4× M2 heat-set inserts (IMU standoffs) + 4× M2 × 5 mm screws")
    print("  - 4× M3 socket-cap screws (to sub-panel from below)")
    print("  - 2× Qwiic JST-SH cables (IMU ↔ XIAO, both ports)")
    print("  - (optional) 1.5 mm Shore-40A silicone O-cord for gasket groove")


if __name__ == "__main__":
    main()
