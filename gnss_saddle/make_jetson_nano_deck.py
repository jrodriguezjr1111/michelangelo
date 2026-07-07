"""
CyberWing Canary — Jetson NANO deck (drone-frame, stacks on the tube X-frame base).

A drone-frame plate that:
  - holds the Jetson Nano in the middle on 4 self-tap standoffs (86.14 × 58.25)
  - bolts DOWN to the base X-frame's 4 corner M3 inserts (172 × 104) via corner
    posts with an M3 clearance hole + top counterbore
  - presents 4 M3 heat-set inserts at an inner pattern (150 × 90) on top, so the
    Orin deck stacks above without colliding with the base screws (stepped tower)

Coordinate frame:
  X, Y = deck plane;  Z = up.  Deck underside at Z=0 (on the bed), features rise +Z.

Outputs:
  jetson_nano_deck.stl
"""

from build123d import *
import math
from pathlib import Path

# ---- corner base-mount (to base X-frame inserts) ---------------------------
CX = 86.0;  CY = 52.0                      # 172 × 104

# ---- Nano board mount ------------------------------------------------------
NANO_PAT = (86.14, 58.25)                  # Nano dev-kit mount pattern
NANO_BOARD = (100.0, 80.0)

# ---- Orin-mount inserts (stepped inner pattern, top) -----------------------
ORIN_CX = 75.0;  ORIN_CY = 45.0            # 150 × 90

# ---- fasteners -------------------------------------------------------------
M3_CLEAR  = 3.4
CBORE_D   = 6.0;  CBORE_H = 3.2            # M3 cap-head counterbore (corner, top)
INSERT_D  = 4.4;  INSERT_DEPTH = 6.0;  INSERT_CHAM = 0.6   # M3 heat-set (Orin)
BOSS_OD   = 7.0;  BOSS_H = 6.0;  PILOT = 2.6               # Nano M3 self-tap standoff

# ---- deck / frame ----------------------------------------------------------
DECK_T   = 4.0
HUB_X    = NANO_BOARD[0] + 4               # 104
HUB_Y    = NANO_BOARD[1] + 4               # 84
ARM_W    = 12.0
CORNER_OD = 13.0;  CORNER_H = 6.0          # base-mount corner post (above deck)
ORIN_OD   = 10.0;  ORIN_H   = 8.0          # Orin insert boss (above deck)
ARM_ATTACH = (44.0, 32.0)

OUT_DIR = Path(__file__).parent

# ---- sanity ----------------------------------------------------------------
assert INSERT_DEPTH < ORIN_H - 1.0, "Orin insert too deep for boss"
assert CBORE_H < DECK_T + CORNER_H - 1.0, "counterbore too deep for corner post"
assert ORIN_CX > NANO_BOARD[0] / 2 + 2, "Orin bosses clash the Nano board in X"


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
            # base-mount corner post (above deck)
            deck += Pos(bx, by, 0) * Cylinder(CORNER_OD / 2, DECK_T + CORNER_H,
                                              align=(Align.CENTER, Align.CENTER, Align.MIN))

    # corner: M3 clearance through + top counterbore (bolt down to base inserts)
    top_z = DECK_T + CORNER_H
    for sx in (-1, 1):
        for sy in (-1, 1):
            bx, by = sx * CX, sy * CY
            deck -= Pos(bx, by, -0.2) * Cylinder(M3_CLEAR / 2, top_z + 0.4,
                                                 align=(Align.CENTER, Align.CENTER, Align.MIN))
            deck -= Pos(bx, by, top_z - CBORE_H) * Cylinder(CBORE_D / 2, CBORE_H + 0.1,
                                                            align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Nano self-tap standoffs (top)
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = sx * NANO_PAT[0] / 2, sy * NANO_PAT[1] / 2
            deck += Pos(px, py, DECK_T) * Cylinder(BOSS_OD / 2, BOSS_H,
                                                   align=(Align.CENTER, Align.CENTER, Align.MIN))
            deck -= Pos(px, py, DECK_T + BOSS_H - 5.0) * Cylinder(PILOT / 2, 5.2,
                                                                  align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Orin-mount heat-set insert bosses (top, stepped inner pattern)
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = sx * ORIN_CX, sy * ORIN_CY
            deck += Pos(px, py, DECK_T) * Cylinder(ORIN_OD / 2, ORIN_H,
                                                   align=(Align.CENTER, Align.CENTER, Align.MIN))
            tz = DECK_T + ORIN_H
            deck -= Pos(px, py, tz - INSERT_DEPTH) * Cylinder(INSERT_D / 2, INSERT_DEPTH + 0.1,
                                                              align=(Align.CENTER, Align.CENTER, Align.MIN))
            deck -= Pos(px, py, tz - INSERT_CHAM) * Cone(
                INSERT_D / 2 + INSERT_CHAM, INSERT_D / 2, INSERT_CHAM + 0.01,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    return deck


def main() -> None:
    print("CyberWing Jetson NANO deck (drone-frame)")
    print(f"  base mount: 4× M3 clearance+cbore at (±{CX}, ±{CY}) = 172×104 -> base inserts")
    print(f"  Nano: 4× M3 self-tap standoffs {NANO_PAT[0]}×{NANO_PAT[1]}, {BOSS_H}mm")
    print(f"  Orin: 4× M3 inserts at (±{ORIN_CX}, ±{ORIN_CY}) = 150×90 (stepped, for Orin deck)")
    deck = build_deck()
    out = OUT_DIR / "jetson_nano_deck.stl"
    export_stl(deck, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes) — print flat (underside down), no supports")


if __name__ == "__main__":
    main()
