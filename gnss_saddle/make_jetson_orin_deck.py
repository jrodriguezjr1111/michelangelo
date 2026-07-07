"""
CyberWing Canary — Jetson ORIN deck (drone-frame, TOP of the stack).

Twin of the Nano deck. Holds the Orin in the middle on 4 self-tap standoffs
(91.86 × 58.37) and bolts DOWN to the Nano deck's 4 top M3 inserts at the
stepped inner pattern (150 × 90) via corner posts with an M3 clearance hole +
top counterbore. Top of the stack — no upward inserts.

Coordinate frame:
  X, Y = deck plane;  Z = up.  Deck underside at Z=0 (on the bed), features rise +Z.

Outputs:
  jetson_orin_deck.stl
"""

from build123d import *
import math
from pathlib import Path

# ---- corner down-mount (to Nano deck top inserts, 150 × 90) -----------------
CX = 75.0;  CY = 45.0

# ---- Orin board mount ------------------------------------------------------
ORIN_PAT = (91.86, 58.37)

# ---- fasteners -------------------------------------------------------------
M3_CLEAR = 3.4
CBORE_D  = 6.0;  CBORE_H = 3.2            # M3 cap-head counterbore (corner, top)
BOSS_OD  = 7.0;  BOSS_H = 6.0;  PILOT = 2.6   # Orin M3 self-tap standoff

# ---- deck / frame ----------------------------------------------------------
DECK_T   = 4.0
HUB_X    = ORIN_PAT[0] + 12               # ~104
HUB_Y    = ORIN_PAT[1] + 14              # ~72
ARM_W    = 12.0
CORNER_OD = 13.0;  CORNER_H = 6.0
ARM_ATTACH = (40.0, 30.0)

OUT_DIR = Path(__file__).parent

# ---- sanity ----------------------------------------------------------------
assert ORIN_PAT[0] / 2 < HUB_X / 2 - 1, "Orin standoffs exit the hub in X"
assert ORIN_PAT[1] / 2 < HUB_Y / 2 - 1, "Orin standoffs exit the hub in Y"
assert CBORE_H < DECK_T + CORNER_H - 1.0, "counterbore too deep for corner post"


def build_deck() -> Part:
    deck = Box(HUB_X, HUB_Y, DECK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))

    ax, ay = ARM_ATTACH
    for sx in (-1, 1):
        for sy in (-1, 1):
            hx, hy = sx * ax, sy * ay
            bx, by = sx * CX, sy * CY
            mx, my = (hx + bx) / 2, (hy + by) / 2
            ang = math.degrees(math.atan2(by - hy, bx - hx))
            L = math.hypot(bx - hx, by - hy) + 14
            arm = Box(L, ARM_W, DECK_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
            deck += Pos(mx, my, 0) * (Rot(0, 0, ang) * arm)
            deck += Pos(bx, by, 0) * Cylinder(CORNER_OD / 2, DECK_T + CORNER_H,
                                              align=(Align.CENTER, Align.CENTER, Align.MIN))

    # corner: M3 clearance through + top counterbore (bolt down to Nano inserts)
    top_z = DECK_T + CORNER_H
    for sx in (-1, 1):
        for sy in (-1, 1):
            bx, by = sx * CX, sy * CY
            deck -= Pos(bx, by, -0.2) * Cylinder(M3_CLEAR / 2, top_z + 0.4,
                                                 align=(Align.CENTER, Align.CENTER, Align.MIN))
            deck -= Pos(bx, by, top_z - CBORE_H) * Cylinder(CBORE_D / 2, CBORE_H + 0.1,
                                                            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Orin self-tap standoffs (top)
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = sx * ORIN_PAT[0] / 2, sy * ORIN_PAT[1] / 2
            deck += Pos(px, py, DECK_T) * Cylinder(BOSS_OD / 2, BOSS_H,
                                                   align=(Align.CENTER, Align.CENTER, Align.MIN))
            deck -= Pos(px, py, DECK_T + BOSS_H - 5.0) * Cylinder(PILOT / 2, 5.2,
                                                                  align=(Align.CENTER, Align.CENTER, Align.MIN))

    return deck


def main() -> None:
    print("CyberWing Jetson ORIN deck (drone-frame, top)")
    print(f"  down mount: 4× M3 clearance+cbore at (±{CX}, ±{CY}) = 150×90 -> Nano deck inserts")
    print(f"  Orin: 4× M3 self-tap standoffs {ORIN_PAT[0]}×{ORIN_PAT[1]}, {BOSS_H}mm")
    deck = build_deck()
    out = OUT_DIR / "jetson_orin_deck.stl"
    export_stl(deck, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes) — print flat (underside down), no supports")


if __name__ == "__main__":
    main()
