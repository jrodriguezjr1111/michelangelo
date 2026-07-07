"""
CyberWing — Jetson Nano tube-clamp plate + X-FRAME for the Orin mount.

Same as make_nano_tubeclamp.py (Nano plate that grips the two tubes) but adds
4 drone-style arms out to corner bosses with M3 heat-set inserts at the Orin
stack pattern (150 across tubes / Y × 90 along the tube axis / X), so the Orin
deck (or spacer standoffs) bolts on top, boards parallel.

Frame:  X = tube axis (Nano 58.25);  Y = across tubes (Nano 86.14);  Z = up.

Output: nano_tubeclamp_xframe.stl
"""

from build123d import *
import math
from pathlib import Path

# ---- Nano mount pattern (tube axis = X = 58.25; across = Y = 86.14) ----
NANO_X, NANO_Y = 58.25 / 2, 86.14 / 2
SO_OD, SO_H = 8.0, 7.0                          # standoff boss (wider for the insert)
SO_INS_D, SO_INS_H, SO_INS_CHAM = 4.0, 6.0, 0.6  # M3 heat-set insert (open UP, toward the Nano)

# ---- tubes (along X) at Y = ±30.085 ----
TUBE_OD, TUBE_SEP, CLR = 15.39, 60.17, 0.4
R_IN   = TUBE_OD / 2 + CLR / 2
TUBE_Y = TUBE_SEP / 2

GNSS_D = 30.0
M4_P, M4_CLR, M4_CB_D, M4_CB_DEPTH = 18.0, 4.4, 8.0, 4.5
HUB_X, HUB_Y, HUB_H = 72.0, 100.0, 14.0

ATT_INS_D, ATT_INS_H, ATT_CHAM = 4.0, 6.0, 0.6
ATT_Y = 20.0
ATT_Z = HUB_H / 2
SHORT_X = 20.0

# ---- NEW: Orin X-frame (150 across tubes / Y × 90 along X) ----
ORIN_CX, ORIN_CY = 45.0, 75.0          # corners at (±45 X, ±75 Y)
ARM_W   = 14.0
CORNER_OD = 13.0
ORIN_INS_D, ORIN_INS_H, ORIN_INS_CHAM = 5.6, 7.0, 0.6   # #8-32 heat-set, open UP (z=HUB_H)
ARM_ATTACH = (30.0, 44.0)              # hub anchor (inside hub ±36, ±50)

OUT_DIR = Path(__file__).parent

# ---- sanity ----
assert R_IN + 2.0 <= HUB_H, "hub too short for tube scoop + wall"
assert GNSS_D / 2 + 1.0 < TUBE_Y - R_IN, "GNSS hole clashes the tube scoops"
assert ORIN_CY - ARM_W / 2 > TUBE_Y + R_IN, "X-arm clashes a tube scoop"
assert ORIN_INS_H < HUB_H - 1.0, "Orin insert too deep for hub height"


def build() -> Part:
    p = Box(HUB_X, HUB_Y, HUB_H, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # tube scoops (bottom face, along X)
    for sy in (-1, 1):
        bore = Cylinder(R_IN, HUB_X + 0.4, rotation=(0, 90, 0), align=(Align.CENTER,) * 3)
        p -= Pos(0.0, sy * TUBE_Y, 0.0) * bore

    # central Ø30 GNSS pass-through
    p -= Pos(0, 0, -0.2) * Cylinder(GNSS_D / 2, HUB_H + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M4 clamp + top counterbore
    for sx in (-1, 1):
        for sy in (-1, 1):
            p -= Pos(sx * M4_P, sy * M4_P, -0.2) * Cylinder(M4_CLR / 2, HUB_H + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN))
            p -= Pos(sx * M4_P, sy * M4_P, HUB_H - M4_CB_DEPTH) * Cylinder(M4_CB_D / 2, M4_CB_DEPTH + 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # ---- NEW: 4 X-arms + corner bosses (added BEFORE Nano standoffs/side inserts) ----
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

    # Nano M3 heat-set insert standoffs on TOP (insert opens UP, toward the Nano)
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = sx * NANO_X, sy * NANO_Y
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
    out = OUT_DIR / "nano_tubeclamp_xframe.stl"
    export_stl(part, str(out))
    print(f"✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)")
    print(f"  hub {HUB_X}×{HUB_Y}×{HUB_H}; X-arms to Orin corners (±{ORIN_CX} X, ±{ORIN_CY} Y) = 90×150")
    print(f"  4× M3 inserts (Ø{ORIN_INS_D}×{ORIN_INS_H}) open UP at the corners for the Orin mount")
