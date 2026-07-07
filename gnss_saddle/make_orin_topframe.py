"""
CyberWing — Jetson ORIN top-frame.

A version of make_nano_tubeclamp_xframe.py WITHOUT the tube scoops and the M4
clamp holes (the Orin sits on top of the stack, it doesn't grip tubes). Same
72×100×14 hub, X-arms to corner M3 inserts at (±45 X, ±75 Y), GNSS Ø30 pass-
through, and side M3 inserts. Board standoffs use the Orin pattern (58.37 ∥ X,
91.86 across Y) so it sits parallel to the Nano below.

Frame:  X = tube axis;  Y = across tubes;  Z = up.

Output: orin_topframe.stl
"""

from build123d import *
import math
from pathlib import Path

# ---- Orin mount pattern (58.37 ∥ X, 91.86 across Y) ----
ORIN_X, ORIN_Y = 58.37 / 2, 91.86 / 2          # ±29.185, ±45.93
SO_OD, SO_H = 8.0, 7.0                          # standoff boss (wider for the insert)
SO_INS_D, SO_INS_H, SO_INS_CHAM = 4.0, 6.0, 0.6  # M3 heat-set insert (open UP, toward the Orin)

GNSS_D = 30.0
HUB_X, HUB_Y, HUB_H = 72.0, 100.0, 14.0

ATT_INS_D, ATT_INS_H, ATT_CHAM = 4.0, 6.0, 0.6
ATT_Y = 20.0
ATT_Z = HUB_H / 2

# ---- Orin X-frame corners (90 X × 150 Y) ----
ORIN_CX, ORIN_CY = 45.0, 75.0
ARM_W   = 14.0
CORNER_OD = 13.0
ORIN_INS_D, ORIN_INS_H, ORIN_INS_CHAM = 5.6, 7.0, 0.6   # #8-32 heat-set
ARM_ATTACH = (30.0, 44.0)

OUT_DIR = Path(__file__).parent

# ---- sanity ----
assert GNSS_D / 2 + 2.0 < ORIN_Y, "GNSS hole clashes the Orin standoffs in Y"
assert ORIN_INS_H < HUB_H - 1.0, "Orin insert too deep for hub height"
assert ORIN_X + SO_OD / 2 < HUB_X / 2, "Orin standoffs exit the hub in X"
assert ORIN_Y + SO_OD / 2 < HUB_Y / 2, "Orin standoffs exit the hub in Y"


def build() -> Part:
    p = Box(HUB_X, HUB_Y, HUB_H, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # central Ø30 pass-through (no tube scoops, no M4 holes)
    p -= Pos(0, 0, -0.2) * Cylinder(GNSS_D / 2, HUB_H + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4 X-arms + corner bosses
    ax, ay = ARM_ATTACH
    for sx in (-1, 1):
        for sy in (-1, 1):
            hx, hy = sx * ax, sy * ay
            bx, by = sx * ORIN_CX, sy * ORIN_CY
            mx, my = (hx + bx) / 2, (hy + by) / 2
            ang = math.degrees(math.atan2(by - hy, bx - hx))
            L = math.hypot(bx - hx, by - hy) + 12
            arm = Box(L, ARM_W, HUB_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
            p += Pos(mx, my, 0) * (Rot(0, 0, ang) * arm)
            p += Pos(bx, by, 0) * Cylinder(CORNER_OD / 2, HUB_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # corner #8-32 THROUGH-holes + head counterbore on TOP and BOTTOM faces
    C832_CLR, C832_CB_D, C832_CB_H = 4.5, 8.0, 4.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            bx, by = sx * ORIN_CX, sy * ORIN_CY
            p -= Pos(bx, by, -0.2) * Cylinder(C832_CLR / 2, HUB_H + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN))
            p -= Pos(bx, by, HUB_H - C832_CB_H) * Cylinder(C832_CB_D / 2, C832_CB_H + 0.1, align=(Align.CENTER, Align.CENTER, Align.MIN))   # top head space
            p -= Pos(bx, by, -0.1) * Cylinder(C832_CB_D / 2, C832_CB_H + 0.1, align=(Align.CENTER, Align.CENTER, Align.MIN))               # bottom head space

    # Orin M3 heat-set insert standoffs on TOP (insert opens UP, toward the Orin)
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = sx * ORIN_X, sy * ORIN_Y
            p += Pos(px, py, HUB_H) * Cylinder(SO_OD / 2, SO_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
            tz = HUB_H + SO_H
            p -= Pos(px, py, tz - SO_INS_H) * Cylinder(SO_INS_D / 2, SO_INS_H + 0.1, align=(Align.CENTER, Align.CENTER, Align.MIN))
            p -= Pos(px, py, tz - SO_INS_CHAM) * Cone(SO_INS_D / 2, SO_INS_D / 2 + SO_INS_CHAM, SO_INS_CHAM + 0.01, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # side M3 inserts (+X long edge — for the RSD flange)
    for sy in (-1, 1):
        c = Pos(HUB_X / 2 + 0.01, sy * ATT_Y, ATT_Z)
        p -= c * (Rot(0, 90, 0) * Cylinder(ATT_INS_D / 2, ATT_INS_H, align=(Align.CENTER, Align.CENTER, Align.MAX)))
        p -= c * (Rot(0, 90, 0) * Cone(ATT_INS_D / 2, ATT_INS_D / 2 + ATT_CHAM, ATT_CHAM, align=(Align.CENTER, Align.CENTER, Align.MAX)))

    # short-side M3 inserts (±Y faces — for the side component plates)
    SHORT_X = 20.0
    for sx in (-1, 1):
        cp = Pos(sx * SHORT_X, HUB_Y / 2 + 0.01, ATT_Z)        # +Y face, bore -Y
        p -= cp * (Rot(-90, 0, 0) * Cylinder(ATT_INS_D / 2, ATT_INS_H, align=(Align.CENTER, Align.CENTER, Align.MAX)))
        p -= cp * (Rot(-90, 0, 0) * Cone(ATT_INS_D / 2, ATT_INS_D / 2 + ATT_CHAM, ATT_CHAM, align=(Align.CENTER, Align.CENTER, Align.MAX)))
        cm = Pos(sx * SHORT_X, -HUB_Y / 2 - 0.01, ATT_Z)       # -Y face, bore +Y
        p -= cm * (Rot(90, 0, 0) * Cylinder(ATT_INS_D / 2, ATT_INS_H, align=(Align.CENTER, Align.CENTER, Align.MAX)))
        p -= cm * (Rot(90, 0, 0) * Cone(ATT_INS_D / 2, ATT_INS_D / 2 + ATT_CHAM, ATT_CHAM, align=(Align.CENTER, Align.CENTER, Align.MAX)))

    return p


if __name__ == "__main__":
    part = build()
    out = OUT_DIR / "orin_topframe.stl"
    export_stl(part, str(out))
    print(f"✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)")
    print(f"  hub {HUB_X}×{HUB_Y}×{HUB_H}; NO tube scoops, NO M4 holes")
    print(f"  Orin: 4× Ø{SO_OD}×{SO_H} standoffs at (±{ORIN_X:.2f}, ±{ORIN_Y:.2f})")
    print(f"  X-arms to corner M3 inserts at (±{ORIN_CX} X, ±{ORIN_CY} Y); GNSS Ø{GNSS_D} pass-through kept")
