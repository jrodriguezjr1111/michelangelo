"""
CyberWing Canary — Jetson sub-panel v1.

A rectangular mounting plate sized to carry a Jetson Orin Nano dev kit and a
Jetson Nano (B01) dev kit side-by-side, plus a half-circle notch on one short
edge for a GNSS antenna mount bolt.

Coordinate frame (print orientation):
  X = long axis (8.75 in)  — both Jetsons line up here
  Y = short axis (5.5 in)
  Z = build direction, thickness

Outputs:
  sub_panel.stl
"""

import argparse
import math
from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

# Plate (imperial in, converted once to mm)
INCH = 25.4
PLATE_L = 8.75 * INCH     # 222.25 mm (X)
PLATE_W = 5.50 * INCH     # 139.70 mm (Y)
PLATE_T = 4.0             # thickness (Z); bump to 5-6 mm if PLA feels too flexy

# --- Jetson mounting patterns (rectangular, centered on each Jetson's origin) ---
# Both are M3 with Ø3.4 mm clearance, counterbored from the BOTTOM so screw
# heads sit below the top mounting surface.
M3_CLEAR_D   = 3.4
M3_CSK_D     = 6.0        # socket-cap counterbore diameter
M3_CSK_DEPTH = 2.5        # counterbore depth from bottom face

# Jetson Orin Nano dev kit
ORIN_PCB_L     = 100.0
ORIN_PCB_W     = 78.79
ORIN_PATTERN_L = 92.12     # M3 hole spacing along PCB long axis
ORIN_PATTERN_W = 57.59     # M3 hole spacing along PCB short axis

# Jetson Nano dev kit B01
NANO_PCB_L     = 100.0
NANO_PCB_W     = 78.79
NANO_PATTERN_L = 88.65
NANO_PATTERN_W = 57.59

# Layout: place the two PCBs symmetrically along X with PCB_GAP between their
# nearest edges. Both centered on Y=0. End margins are derived (must be > 0).
PCB_GAP = 5.0             # gap between Orin PCB right edge and Nano PCB left edge
MIN_SCREW_EDGE_CLR = 5.0  # required clearance from any M3 hole to plate edge

# --- GNSS antenna bolt notch (semicircle on one LONG edge) ---
# This plate is one half of the Pelican-case floor; two mirrored halves butt
# together along this long edge, and the two semicircles combine into one full
# hole centered on the case for the GNSS antenna bolt.
# Default Ø20 fits a 5/8"-11 (15.9 mm) stud with clearance, or M16.
GNSS_NOTCH_D       = 20.0
GNSS_NOTCH_ON_PLUS_Y = True   # True: notch on +Y long edge; False: -Y long edge

# --- Hex honeycomb lightening pattern ---
# Through-hole hexes subtracted from the plate everywhere except keepout rings
# around screws, the GNSS notch, and the plate border.
USE_HEX_LATTICE       = True
HEX_FLAT              = 14.0   # flat-to-flat hex size (mm)
HEX_WALL              = 3.5    # rib thickness between hexes
HEX_EDGE_MARGIN       = 10.0   # keep solid within this distance of plate edge
HEX_SCREW_KEEPOUT_R   = 9.0    # keep solid within this radius of each M3 center
HEX_NOTCH_KEEPOUT_R   = GNSS_NOTCH_D / 2 + 10.0  # keep solid around notch

OUT_DIR = Path(__file__).parent


# =============================================================================
# Derived
# =============================================================================

# Layout driven by PCB_GAP (PCB edge to PCB edge), centered on plate.
# orin sits in -X half, nano in +X half.
orin_center_x = -(ORIN_PCB_L + PCB_GAP) / 2
nano_center_x = +(NANO_PCB_L + PCB_GAP) / 2

# Derived gaps and clearances
gap_between_patterns = (nano_center_x - NANO_PATTERN_L / 2) - \
                       (orin_center_x + ORIN_PATTERN_L / 2)
orin_left_screw_edge_clr  = (orin_center_x - ORIN_PATTERN_L / 2) - (-PLATE_L / 2)
nano_right_screw_edge_clr = (+PLATE_L / 2) - (nano_center_x + NANO_PATTERN_L / 2)

assert orin_left_screw_edge_clr  >= MIN_SCREW_EDGE_CLR, (
    f"Orin leftmost screw too close to plate edge "
    f"({orin_left_screw_edge_clr:.2f} mm < {MIN_SCREW_EDGE_CLR} mm). "
    "Shrink PCB_GAP or enlarge PLATE_L."
)
assert nano_right_screw_edge_clr >= MIN_SCREW_EDGE_CLR, (
    f"Nano rightmost screw too close to plate edge "
    f"({nano_right_screw_edge_clr:.2f} mm < {MIN_SCREW_EDGE_CLR} mm)."
)
assert gap_between_patterns > 0, \
    f"Screw patterns overlap by {-gap_between_patterns:.2f} mm — increase PCB_GAP"

# Where the GNSS notch sits (centered on the chosen LONG edge). Notch center
# is at X=0, Y=±PLATE_W/2. When two mirrored panels butt together along this
# edge, the two semicircles form one full hole.
notch_edge_y = (+PLATE_W / 2) if GNSS_NOTCH_ON_PLUS_Y else (-PLATE_W / 2)

# Make sure the notch does not clash with the nearest Jetson screw (both
# patterns are at Y = ±29, notch reaches Y = ±PLATE_W/2 - GNSS_NOTCH_D/2).
_notch_inner_y = abs(notch_edge_y) - GNSS_NOTCH_D / 2
_jetson_max_y  = max(ORIN_PATTERN_W, NANO_PATTERN_W) / 2
assert _notch_inner_y - _jetson_max_y > 5.0, (
    f"GNSS notch too close to Jetson screws: "
    f"{_notch_inner_y - _jetson_max_y:.1f} mm clearance"
)


# =============================================================================
# Build
# =============================================================================

def build_panel() -> Part:
    panel = Box(PLATE_L, PLATE_W, PLATE_T,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # --- 8× M3 clearance holes (through) + counterbores from bottom face ---
    hole_centers: list[tuple[float, float]] = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            hole_centers.append((orin_center_x + sx * ORIN_PATTERN_L / 2,
                                 sy * ORIN_PATTERN_W / 2))
            hole_centers.append((nano_center_x + sx * NANO_PATTERN_L / 2,
                                 sy * NANO_PATTERN_W / 2))

    for cx, cy in hole_centers:
        thru = Cylinder(M3_CLEAR_D / 2, PLATE_T + 0.2,
                        align=(Align.CENTER, Align.CENTER, Align.MIN))
        thru = Pos(cx, cy, -0.1) * thru
        panel -= thru
        # Skip counterbore on thin test prints (would punch through)
        if M3_CSK_DEPTH + 0.4 < PLATE_T:
            csk = Cylinder(M3_CSK_D / 2, M3_CSK_DEPTH + 0.1,
                           align=(Align.CENTER, Align.CENTER, Align.MIN))
            csk = Pos(cx, cy, -0.05) * csk
            panel -= csk

    # --- GNSS semicircle notch on the chosen LONG edge (centered X=0) ---
    # Subtract a full cylinder whose center sits ON the edge line.
    notch = Cylinder(GNSS_NOTCH_D / 2, PLATE_T + 0.4,
                     align=(Align.CENTER, Align.CENTER, Align.MIN))
    notch = Pos(0.0, notch_edge_y, -0.2) * notch
    panel -= notch

    # --- Hex honeycomb lightening pattern ---
    if USE_HEX_LATTICE:
        panel = _apply_hex_lattice(panel, hole_centers)

    return panel


def _apply_hex_lattice(panel: Part, screw_centers: list[tuple[float, float]]) -> Part:
    """Subtract a hex grid from the plate, keeping solid rings around screws,
    the GNSS notch, and the plate border."""
    # "Pointy-top" hex: flat-to-flat = HEX_FLAT, circumscribed radius = HEX_FLAT/sqrt(3)
    circ_r  = HEX_FLAT / math.sqrt(3)
    pitch_x = HEX_FLAT + HEX_WALL                       # between hex centers in a row
    pitch_y = (HEX_FLAT + HEX_WALL) * math.sqrt(3) / 2  # row spacing (staggered)

    # Grid extent: cover full plate minus margin, in a staggered pattern
    half_L = PLATE_L / 2 - HEX_EDGE_MARGIN
    half_W = PLATE_W / 2 - HEX_EDGE_MARGIN
    n_rows = int(half_W / pitch_y) + 1
    n_cols = int(half_L / pitch_x) + 1

    notch_cx, notch_cy = 0.0, notch_edge_y
    cuts: list[Part] = []

    for i in range(-n_rows, n_rows + 1):
        y = i * pitch_y
        x_off = (pitch_x / 2) if (i % 2) else 0.0
        for j in range(-n_cols, n_cols + 1):
            x = j * pitch_x + x_off
            # Hex must fit entirely within [-half_L, +half_L] x [-half_W, +half_W]
            if abs(x) + circ_r > half_L or abs(y) + circ_r > half_W:
                continue
            # Screw keepout (Euclidean distance to any M3 center)
            if any(math.hypot(x - sx, y - sy) < HEX_SCREW_KEEPOUT_R
                   for sx, sy in screw_centers):
                continue
            # GNSS notch keepout
            if math.hypot(x - notch_cx, y - notch_cy) < HEX_NOTCH_KEEPOUT_R:
                continue
            hex_sk = RegularPolygon(circ_r, 6)
            hex3d  = extrude(hex_sk, amount=PLATE_T + 0.4)
            cuts.append(Pos(x, y, -0.2) * hex3d)

    if cuts:
        combined = cuts[0]
        for c in cuts[1:]:
            combined += c
        panel -= combined
    print(f"  lattice: {len(cuts)} hex cutouts")
    return panel


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    global PLATE_T
    ap = argparse.ArgumentParser(description="Jetson sub-panel generator")
    ap.add_argument("--test", action="store_true",
                    help="Generate a thin (1.2 mm) test print for fit verification.")
    ap.add_argument("--thickness", type=float, default=None,
                    help="Override plate thickness in mm.")
    args = ap.parse_args()

    if args.test:
        PLATE_T = 1.2
        out_name = "sub_panel_test.stl"
    elif args.thickness is not None:
        PLATE_T = args.thickness
        out_name = f"sub_panel_{PLATE_T:g}mm.stl"
    else:
        out_name = "sub_panel.stl"

    print("=" * 60)
    print("Jetson sub-panel — build123d generator")
    if args.test:
        print("  TEST PRINT MODE  (thin, no counterbores)")
    print("=" * 60)
    print(f"Plate:         {PLATE_L:.2f} × {PLATE_W:.2f} × {PLATE_T} mm "
          f"(5.50 × 8.75 in)")
    print(f"Orin:          PCB {ORIN_PCB_L} × {ORIN_PCB_W}, holes "
          f"{ORIN_PATTERN_L} × {ORIN_PATTERN_W}, center X = {orin_center_x:+.2f}")
    print(f"Nano:          PCB {NANO_PCB_L} × {NANO_PCB_W}, holes "
          f"{NANO_PATTERN_L} × {NANO_PATTERN_W}, center X = {nano_center_x:+.2f}")
    print(f"PCB-to-PCB gap:        {PCB_GAP:.1f} mm")
    print(f"Screw-pattern gap:     {gap_between_patterns:.2f} mm")
    print(f"Orin screw-edge clr:   {orin_left_screw_edge_clr:.2f} mm")
    print(f"Nano screw-edge clr:   {nano_right_screw_edge_clr:.2f} mm")
    print(f"Screws:        8× M3 Ø{M3_CLEAR_D} clearance, "
          f"Ø{M3_CSK_D}×{M3_CSK_DEPTH} counterbore from bottom")
    print(f"GNSS notch:    Ø{GNSS_NOTCH_D} mm on "
          f"{'+Y' if GNSS_NOTCH_ON_PLUS_Y else '-Y'} long edge "
          f"(mates with mirrored panel for full circle)")
    if USE_HEX_LATTICE:
        print(f"Hex lattice:   flat={HEX_FLAT} mm, wall={HEX_WALL} mm, "
              f"edge margin={HEX_EDGE_MARGIN} mm")
    print()

    panel = build_panel()
    out = OUT_DIR / out_name
    export_stl(panel, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)")

    print("\nPrint orientation: already flat on bed (+Z up). No supports.")
    print("Recommended settings: 0.2 mm layers, 4 walls, 30-40% gyroid infill.")
    print("If you want a stiffer panel, bump PLATE_T to 5 or 6 mm.")


if __name__ == "__main__":
    main()
