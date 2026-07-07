"""
Drill-press template for the Orin platform hole pattern.

A thin plate (same XY outline) with pilot holes at every mounting location.
Clamp this template to your stock material and use a center punch or step
drill through the holes.

Hole types:
  - M3 Orin mounts:    Ø 3.4 mm  (4 holes, +X half)
  - 1/4"-20 railblock: Ø 6.8 mm  (4 holes, centered)

Outputs: orin_drill_template.stl
"""

from build123d import *
from pathlib import Path

# — Import geometry parameters from the platform script —
from make_platform import (
    PLATE_L, PLATE_W,
    orin_holes, rail_holes,
    M3_CLEAR_D, QUARTER_CLEAR_D,
)

TEMPLATE_T = 3.0  # thin enough to print fast, thick enough to guide a bit
PILOT_D = 2.5     # universal pilot hole for center-punching
LABEL_DEPTH = 0.6 # engraved text depth
OUT_DIR = Path(__file__).parent


def build_template() -> Part:
    # Base plate
    plate = Box(PLATE_L, PLATE_W, TEMPLATE_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Orin M3 holes — pilot size
    for x, y, _r, _tag in orin_holes:
        pilot = Pos(x, y) * Cylinder(
            PILOT_D / 2, TEMPLATE_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
        plate -= pilot

    # Rail 1/4" holes — full clearance (big enough to guide a step drill)
    for x, y, _r, _tag in rail_holes:
        hole = Pos(x, y) * Cylinder(
            QUARTER_CLEAR_D / 2, TEMPLATE_T,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        plate -= hole

    # Corner registration notches (small triangular cuts at each corner
    # so you can align the template flush against the workpiece edges)
    notch_size = 5.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = sx * PLATE_L / 2
            cy = sy * PLATE_W / 2
            tri = Pos(cx, cy) * Box(
                notch_size, notch_size, TEMPLATE_T,
                align=(
                    Align.MAX if sx > 0 else Align.MIN,
                    Align.MAX if sy > 0 else Align.MIN,
                    Align.MIN,
                ))
            plate -= tri

    # Engrave labels on top face
    labels = [
        (0, -PLATE_W / 2 + 8, "DRILL TEMPLATE"),
        (orin_holes[0][0], orin_holes[0][1] - 8, f"M3 x4 (Ø{M3_CLEAR_D})"),
        (rail_holes[0][0], rail_holes[0][1] - 8, f'1/4" x4 (Ø{QUARTER_CLEAR_D})'),
    ]
    for lx, ly, txt in labels:
        with BuildSketch(Plane.XY.offset(TEMPLATE_T)) as sk:
            with Locations([(lx, ly)]):
                Text(txt, font_size=4, align=(Align.CENTER, Align.CENTER))
        plate -= extrude(sk.sketch, amount=-LABEL_DEPTH)

    return plate


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()

    part = build_template()
    out = OUT_DIR / "orin_drill_template.stl"
    export_stl(part, str(out))
    print(f"✓ {out.name}  ({out.stat().st_size / 1024:.0f} KB)")
    print(f"  Plate: {PLATE_L:.2f} × {PLATE_W:.2f} × {TEMPLATE_T} mm")
    print(f"  Orin M3 pilots: Ø{PILOT_D} mm × 4")
    print(f"  Rail 1/4\" holes: Ø{QUARTER_CLEAR_D} mm × 4")

    if args.preview:
        show(part)
