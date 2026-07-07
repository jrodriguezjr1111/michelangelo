"""
Vented top cover for the dual-Jetson nano saddle (make_nano_saddle.py).

Mounts via the SAME 8× M3 Jetson hole pattern (4 per board) using tall
standoffs, so the cover stands as a canopy above both boards:

    cover (this part)        ← 8× M3 clearance holes
      ▲  standoffs (CLEAR_H)
    Orin / Nano boards
    ─── nano_saddle_top ───  ← M3 screws into saddle

Ventilation:
  • Orin (+Y): circular fan guard — open Ø FAN_D grille with a "+" spider
    and one concentric support ring (finger guard + airflow).
  • Nano (−Y): louvered slots over the passive heatsink — parallel slots
    (length along X) arrayed in Y for convection airflow.

Footprint matches the saddle top: BLOCK_LEN (X) × BLOCK_WID (Y).
Print flat on the bed, vents-up. No supports.
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS  (mirror make_nano_saddle.py where shared)
# =============================================================================

# Footprint — matches the saddle top
BLOCK_LEN = 70.0          # X
BLOCK_WID = 197.0         # Y
PLATE_T   = 3.0           # cover thickness

# Standoff height between board top and cover (hardware, BOM only)
CLEAR_H   = 30.0

# Jetson M3 mount patterns (identical to make_nano_saddle.py)
NANO_PATTERN_Y = 86.14
NANO_PATTERN_X = 58.25
ORIN_PATTERN_Y = 92.12
ORIN_PATTERN_X = 57.59
M3_CLEAR_D     = 3.4
M3_CB_D        = 5.3      # top counterbore Ø for screw head / standoff seat
M3_CB_DEPTH    = 1.6

ORIN_Y_CENTER =  BLOCK_WID / 4                                  # +49.25
NANO_Y_CENTER = -(BLOCK_WID / 2 - NANO_PATTERN_Y / 2 - 3.19)    # −52.24

# --- Orin fan guard ---------------------------------------------------------
FAN_D       = 50.0        # open grille diameter (Orin fan ≈ 40 mm)
FAN_RIB_W   = 3.0         # width of the "+" spider ribs
FAN_RING_R  = FAN_D / 4   # radius of the support ring
FAN_RING_W  = 2.5         # ring rib width

# --- Nano heatsink louvers --------------------------------------------------
HS_X      = 56.0          # slot length (along X)
HS_Y      = 56.0          # total louvered span (along Y)
SLOT_W    = 4.0           # slot width (along Y)
RIB_W     = 3.0           # rib between slots
SLOT_FILLET = SLOT_W / 2  # rounded slot ends

OUT_DIR = Path(__file__).parent

# =============================================================================
# Sanity
# =============================================================================
assert PLATE_T >= 2.0, "Cover too thin"
# Fan grille clears the Orin mount holes
assert FAN_D / 2 + 2.0 < ORIN_PATTERN_X / 2, \
    f"Fan grille Ø{FAN_D} too close to Orin M3 holes (X half {ORIN_PATTERN_X/2})"
# Heatsink louvers clear the Nano mount holes in X
assert HS_X / 2 + 2.0 < NANO_PATTERN_X / 2 + 0.01 or HS_X / 2 < BLOCK_LEN / 2 - 3, \
    "Heatsink slots exit plate / clash with Nano holes in X"
assert HS_X / 2 < BLOCK_LEN / 2 - 3, "Heatsink slots exit plate in X"
# Patterns fit on the plate in Y
for nm, py, yc in (("Nano", NANO_PATTERN_Y, NANO_Y_CENTER),
                   ("Orin", ORIN_PATTERN_Y, ORIN_Y_CENTER)):
    assert abs(yc) + py / 2 + M3_CB_D / 2 + 0.4 < BLOCK_WID / 2, f"{nm} holes exit plate in Y"

# Slot pitch / count
PITCH = SLOT_W + RIB_W
N_SLOTS = int(HS_Y // PITCH)
assert N_SLOTS >= 3, "Too few heatsink slots — adjust HS_Y / pitch"

# =============================================================================
# Geometry
# =============================================================================

def build_cover() -> Part:
    plate = Box(BLOCK_LEN, BLOCK_WID, PLATE_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # --- 8× M3 clearance holes + top counterbore (both board patterns) ---
    patterns = [
        (NANO_PATTERN_Y, NANO_PATTERN_X, NANO_Y_CENTER),
        (ORIN_PATTERN_Y, ORIN_PATTERN_X, ORIN_Y_CENTER),
    ]
    for py, px, yc in patterns:
        for sx in (-1, 1):
            for sy in (-1, 1):
                cx = sx * px / 2
                cy = yc + sy * py / 2
                plate -= Pos(cx, cy, -0.2) * Cylinder(
                    M3_CLEAR_D / 2, PLATE_T + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
                plate -= Pos(cx, cy, PLATE_T - M3_CB_DEPTH) * Cylinder(
                    M3_CB_D / 2, M3_CB_DEPTH + 0.2,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))

    # --- Orin fan guard: open circle minus "+" spider and a support ring ---
    fan_hole = Pos(0, ORIN_Y_CENTER, -0.2) * Cylinder(
        FAN_D / 2, PLATE_T + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Spider ribs (+): two thin bars kept as solid material
    rib_x = Pos(0, ORIN_Y_CENTER, -0.2) * Box(
        FAN_D + 1, FAN_RIB_W, PLATE_T + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    rib_y = Pos(0, ORIN_Y_CENTER, -0.2) * Box(
        FAN_RIB_W, FAN_D + 1, PLATE_T + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Support ring (annulus) kept as solid material
    ring_o = Pos(0, ORIN_Y_CENTER, -0.2) * Cylinder(
        FAN_RING_R + FAN_RING_W / 2, PLATE_T + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    ring_i = Pos(0, ORIN_Y_CENTER, -0.4) * Cylinder(
        FAN_RING_R - FAN_RING_W / 2, PLATE_T + 0.8,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    ring = ring_o - ring_i
    grille_solid = (rib_x + rib_y + ring) & fan_hole   # keep ribs only inside hole
    plate -= fan_hole
    plate += grille_solid

    # --- Nano heatsink louvers: parallel slots (length along X) ---
    y0 = NANO_Y_CENTER - (N_SLOTS - 1) * PITCH / 2
    for i in range(N_SLOTS):
        cy = y0 + i * PITCH
        slot_sk = SlotOverall(HS_X, SLOT_W)            # length along X, rounded ends
        slot = extrude(slot_sk, amount=PLATE_T + 0.4)
        plate -= Pos(0, cy, -0.2) * slot

    return plate


def main() -> None:
    cover = build_cover()
    out = OUT_DIR / "nano_cover.stl"
    export_stl(cover, str(out))
    print("=" * 62)
    print("Dual-Jetson nano saddle — vented top cover")
    print("=" * 62)
    print(f"Footprint:    {BLOCK_LEN} × {BLOCK_WID} × {PLATE_T} mm")
    print(f"Mount:        8× Ø{M3_CLEAR_D} M3 (Nano + Orin patterns), "
          f"Ø{M3_CB_D}×{M3_CB_DEPTH} c'bore on top")
    print(f"Standoffs:    {CLEAR_H} mm (hardware) board-top → cover")
    print(f"Orin fan:     Ø{FAN_D} grille at Y={ORIN_Y_CENTER:+.2f} "
          f"(+ spider {FAN_RIB_W} mm, ring r={FAN_RING_R:.1f})")
    print(f"Nano heatsink:{N_SLOTS}× louver slots {HS_X}×{SLOT_W} mm "
          f"(pitch {PITCH}) at Y={NANO_Y_CENTER:+.2f}")
    print(f"  ✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)")
    print("\nPrint flat on bed, vents-up. No supports.")
    print("Hardware: 8× M3 screws + 8× M3 standoffs (≈{:.0f} mm) board→cover."
          .format(CLEAR_H))


if __name__ == "__main__":
    main()
