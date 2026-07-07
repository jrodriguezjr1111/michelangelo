"""
CyberWing — Jetson Nano tube-clamp LOWER half (pairs with nano_tubeclamp.stl).

The bottom clamp half: captures the two GNSS tubes against the top plate
(make_nano_tubeclamp.py). Same tube scoops + same 4× M4 ±18 pattern so the two
halves bolt together around the tubes. No Nano standoffs / GNSS hole — just the
clamp, with M4 nut counterbores on the outer (bottom) face.

Frame: X = tube axis; Y = across tubes; Z = up. Scoops in the TOP (mating) face.
Print scoops-UP (as modeled) — the grooves are valleys, so NO supports needed.

Output: nano_tubeclamp_lower.stl
"""

from build123d import *
from pathlib import Path

# tubes (along X) at Y = ±30.085 — must match the top half
TUBE_OD, TUBE_SEP, CLR = 15.39, 60.17, 0.4
R_IN   = TUBE_OD / 2 + CLR / 2                   # 7.895
TUBE_Y = TUBE_SEP / 2                            # 30.085

# M4 clamp (matches the top half) — nut counterbore on the BOTTOM (outer) face
M4_P, M4_CLR, M4_CB_D, M4_CB_DEPTH = 18.0, 4.4, 8.5, 4.0

# lower clamp block
LOW_X, LOW_Y, LOW_H = 72.0, 84.0, 12.0          # covers tube scoops (Y±38) + margin

OUT_DIR = Path(__file__).parent

assert R_IN + 2.0 <= LOW_H, "lower half too short for scoop + wall"
assert M4_P + M4_CLR / 2 + 1.0 < TUBE_Y - R_IN, "M4 bolt clashes a tube scoop"


def build() -> Part:
    p = Box(LOW_X, LOW_Y, LOW_H, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # tube scoops in the TOP (mating) face, opening UP (no-support print)
    for sy in (-1, 1):
        bore = Cylinder(R_IN, LOW_X + 0.4, rotation=(0, 90, 0), align=(Align.CENTER,) * 3)
        p -= Pos(0.0, sy * TUBE_Y, LOW_H) * bore

    # 4× M4: clearance through + nut counterbore on the BOTTOM (z=0) face
    for sx in (-1, 1):
        for sy in (-1, 1):
            p -= Pos(sx * M4_P, sy * M4_P, -0.2) * Cylinder(
                M4_CLR / 2, LOW_H + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN))
            p -= Pos(sx * M4_P, sy * M4_P, -0.01) * Cylinder(
                M4_CB_D / 2, M4_CB_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MIN))

    return p


if __name__ == "__main__":
    part = build()
    out = OUT_DIR / "nano_tubeclamp_lower.stl"
    export_stl(part, str(out))
    print(f"✓ {out.name} ({out.stat().st_size / 1024:.0f} KB)")
    print(f"  lower clamp {LOW_X}×{LOW_Y}×{LOW_H}; scoops Ø{TUBE_OD} (mating face up) at Y=±{TUBE_Y:.2f}")
    print(f"  4× M4 at ±{M4_P}; nut counterbore Ø{M4_CB_D}×{M4_CB_DEPTH} on the bottom")
    print("  Print scoops-UP (as modeled) — NO supports. Pairs with nano_tubeclamp.stl.")
    print(f"  M4 length ≈ 14 (top) + {LOW_H} (lower) − counterbores ≈ use M4×30.")
