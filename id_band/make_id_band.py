"""
Newborn identification wristband.

A flat, flexible strip (print in TPU) with raised/embossed text and a row of
tie-holes at each end so a thin ribbon or suture thread can be used to close
it at any circumference. No snap pegs — safer for an infant.

Text (4 lines, centered on the strip):
    NICOLAS XAVIER RODRIGUEZ
    DOB: 05/08/23   SEX: M
    MOTHER: PERLA HUIZAR
"""

from build123d import *
from pathlib import Path

# Strip (keepsake size — legibility over wearability)
STRIP_L = 160.0     # X  (scaled up for legibility; 3 mm thick keeps it stuck)
STRIP_W = 32.0      # Y  (band width)
STRIP_T = 3.0       # Z  (thickness that worked)
END_R   = STRIP_W / 2   # rounded ends

# Text (sized so NICOLAS XAVIER RODRIGUEZ fits within STRIP_L with margins)
TEXT_H_NAME = 5.5   # mm cap height for the name line
TEXT_H_INFO = 4.5   # mm cap height for info lines
TEXT_EMBOSS = 1.2   # raised height above the strip
FONT        = "Arial"
LINE_SPACE  = 8.0   # mm between line baselines

LINES = [
    ("NICOLAS XAVIER RODRIGUEZ", TEXT_H_NAME, True),
    ("DOB: 05/08/23    SEX: M",  TEXT_H_INFO, False),
    ("MOTHER: PERLA HUIZAR",     TEXT_H_INFO, False),
]

# Tie-holes: row at each end for adjustable fastening / ribbon
TIE_D       = 4.0           # hole diameter
TIE_COUNT   = 2             # per end
TIE_PITCH   = 8.0           # spacing between holes along X
TIE_EDGE    = 8.0           # distance from strip end to first hole center

OUT_DIR = Path(__file__).parent


def build_band() -> Part:
    # Rounded-rectangle base: two end semicircles + center rectangle
    core_l = STRIP_L - STRIP_W      # length between end circle centers
    base = (
        Box(core_l, STRIP_W, STRIP_T,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        + Pos(-core_l / 2, 0, 0) * Cylinder(
            END_R, STRIP_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
        + Pos(+core_l / 2, 0, 0) * Cylinder(
            END_R, STRIP_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )

    # Tie holes at both ends
    for sx in (-1, 1):
        x_first = sx * (STRIP_L / 2 - TIE_EDGE)
        for i in range(TIE_COUNT):
            x = x_first - sx * i * TIE_PITCH
            base -= Pos(x, 0, -0.2) * Cylinder(
                TIE_D / 2, STRIP_T + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Text block: stack lines vertically, centered overall
    total_h = (len(LINES) - 1) * LINE_SPACE
    y_top = total_h / 2
    text_part = None
    for i, (line, h, bold) in enumerate(LINES):
        y = y_top - i * LINE_SPACE
        sk = Text(line, font_size=h, font=FONT,
                  font_style=FontStyle.BOLD if bold else FontStyle.REGULAR,
                  align=(Align.CENTER, Align.CENTER))
        ext = extrude(sk, amount=TEXT_EMBOSS)
        ext = Pos(0, y, STRIP_T) * ext
        text_part = ext if text_part is None else text_part + ext

    return base + text_part


if __name__ == "__main__":
    part = build_band()
    out = OUT_DIR / "id_band.stl"
    export_stl(part, str(out))
    kb = out.stat().st_size / 1024
    print(f"✓ {out.name}  ({kb:.0f} KB)")
    print(f"  Strip: {STRIP_L} × {STRIP_W} × {STRIP_T} mm (rounded ends)")
    print(f"  Emboss: {TEXT_EMBOSS} mm, font: {FONT}")
    print(f"  Tie holes: {TIE_COUNT} per end, Ø{TIE_D} @ {TIE_PITCH} mm pitch")
    for line, h, bold in LINES:
        tag = "bold" if bold else "reg"
        print(f"    [{tag} {h} mm]  {line}")
