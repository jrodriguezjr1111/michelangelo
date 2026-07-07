"""
CyberWing Canary — GNSS QUAD-tube saddle clamp.

Extension of make_gnss_saddle.py from 2 tubes to FOUR parallel tubes (one added
on each side at the same 60.17 mm pitch), with the block widened in Y and 8 extra
M4 clamp bolts (4 left, 4 right) added in the outer webs between adjacent tubes.

Geometry:
  Two rectangular blocks split along Z=HALF_HT.  Each half is identical (print
  two copies).  Each half has:
    - four half-cylinder scoops on its split face (one per tube)
    - a full Ø GNSS_HOLE_D through-hole on the Z axis (for the antenna bolt)
    - 12× M4 clamp bolt holes with head/nut counterbore on the outer face

Coordinate frame (model == print orientation):
  X = along tube axis (tubes run parallel in +X / -X)
  Y = across tubes (tube centers symmetric about 0 at 60.17 mm pitch)
  Z = build direction.  z=0 = BED (outer face), z=HALF_HT = SPLIT face (up).

Printability: tube scoops open UPWARD at the split face (no overhang); the
GNSS through-hole is a vertical cylinder (no overhang).  No supports needed.

Outputs:
  gnss_saddle_quad_half.stl    (print 2 copies, mirror-identical)
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

# Tubes (MEASURE WITH CALIPERS)
TUBE_OD         = 15.39      # mm, all tubes
TUBE_CENTER_SEP = 60.17      # mm, ADJACENT center-to-center across Y
N_TUBES         = 4          # was 2 — added one left, one right
CLEARANCE       = 0.4        # total diametral clearance

# GNSS antenna bolt through-hole (centered on block)
# Set to 15.73 to match the saddle_quad preview (per user). Note this differs
# from make_gnss_saddle.py (30.0) — the 2-tube generator was not changed.
GNSS_HOLE_D     = 15.73      # Ø, goes fully through both halves

# Block (assembled, both halves combined)
BLOCK_LEN   = 50.0          # X, along tube axis — clamp grip length
BLOCK_HT    = 28.0          # Z, total height assembled
EDGE_MARGIN = 7.0           # plastic beyond outermost bore (Y) — sets BLOCK_WID

# Clamp bolts (M4 stainless socket cap). Central pair flanks the GNSS hole;
# two more columns sit in each outer web between adjacent tubes.
BOLT_X_OFFSET = 18.0         # ±X from center (along tube axis), all bolts
BOLT_Y_OFFSET = 18.0         # central pair Y (flanking GNSS hole)
WEB_BOLT_HALF = 15.0         # outer-web columns offset from web center
SCREW_CLEAR_D  = 4.4
SCREW_HEAD_D   = 8.0
SCREW_HEAD_DEPTH = 4.5       # counterbore depth on outer face (M4 cap head or M4 nut)

OUT_DIR = Path(__file__).parent


# =============================================================================
# Derived
# =============================================================================

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
GNSS_R  = GNSS_HOLE_D / 2

# Tube Y centers, symmetric about 0 at uniform pitch
TUBE_YS = [(i - (N_TUBES - 1) / 2) * TUBE_CENTER_SEP for i in range(N_TUBES)]
TUBE_Y_MAX = max(TUBE_YS)

BLOCK_WID = 2 * (TUBE_Y_MAX + R_IN + EDGE_MARGIN)   # Y, across tubes

# Bolt Y columns: central pair + two columns in each outer web.
# Outer webs are centered between adjacent tubes, at ±TUBE_CENTER_SEP.
BOLT_YS = [-BOLT_Y_OFFSET, BOLT_Y_OFFSET]
for wc in (-TUBE_CENTER_SEP, TUBE_CENTER_SEP):
    BOLT_YS += [wc - WEB_BOLT_HALF, wc + WEB_BOLT_HALF]
BOLT_XS = [-BOLT_X_OFFSET, BOLT_X_OFFSET]

# =============================================================================
# Sanity checks
# =============================================================================

assert TUBE_Y_MAX + R_IN + 3.0 <= BLOCK_WID / 2, \
    f"Block too narrow ({BLOCK_WID:.2f} mm) for outer tube centers ±{TUBE_Y_MAX:.2f}"
assert R_IN + 2.0 <= HALF_HT, \
    "Half-height must clear tube bore radius + wall"

# every bolt clears every tube bore (Y separation)
_min_bolt_tube = min(abs(by - ty) - R_IN - SCREW_CLEAR_D / 2
                     for by in BOLT_YS for ty in TUBE_YS)
assert _min_bolt_tube > 1.0, \
    f"Clamp bolt clashes a tube bore (min {_min_bolt_tube:.2f} mm)"

# every bolt clears the GNSS hole (diagonal)
_min_bolt_gnss = min((bx**2 + by**2) ** 0.5 - GNSS_R - SCREW_CLEAR_D / 2
                     for bx in BOLT_XS for by in BOLT_YS)
assert _min_bolt_gnss > 1.0, \
    f"Clamp bolt too close to GNSS hole (min {_min_bolt_gnss:.2f} mm)"

# outer bolt heads stay inside the block edge
_bolt_edge = BLOCK_WID / 2 - (max(abs(b) for b in BOLT_YS) + SCREW_HEAD_D / 2)
assert _bolt_edge > 1.0, f"Outer bolt head exits block edge ({_bolt_edge:.2f} mm)"


# =============================================================================
# Build one half (both halves are identical — print twice)
# =============================================================================

def build_half() -> Part:
    block = Box(BLOCK_LEN, BLOCK_WID, HALF_HT,
                align=(Align.CENTER, Align.CENTER, Align.MIN))

    # --- Tube half-bores scooped from split face (z=HALF_HT) ---
    for ty in TUBE_YS:
        bore = Cylinder(R_IN, BLOCK_LEN + 0.2,
                        rotation=(0, 90, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        bore = Pos(0.0, ty, HALF_HT) * bore
        block -= bore

    # --- GNSS center through-hole (Z axis) ---
    gnss = Cylinder(GNSS_R, HALF_HT + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
    gnss = Pos(0.0, 0.0, -0.2) * gnss
    block -= gnss

    # --- 12× clamp-bolt through-holes + outer-face counterbore ---
    for cx in BOLT_XS:
        for cy in BOLT_YS:
            thru = Cylinder(SCREW_CLEAR_D / 2, HALF_HT + 0.4,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            thru = Pos(cx, cy, -0.2) * thru
            block -= thru
            head = Cylinder(SCREW_HEAD_D / 2, SCREW_HEAD_DEPTH + 0.1,
                            align=(Align.CENTER, Align.CENTER, Align.MIN))
            head = Pos(cx, cy, -0.05) * head
            block -= head

    return block


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("CyberWing GNSS QUAD-tube saddle — build123d generator")
    print("=" * 60)
    print(f"Block:          {BLOCK_LEN} × {BLOCK_WID:.2f} × {BLOCK_HT} mm assembled")
    print(f"Tubes:          {N_TUBES}× Ø{TUBE_OD} at Y = "
          f"{', '.join(f'{y:.2f}' for y in TUBE_YS)} (adjacent C-C {TUBE_CENTER_SEP} mm)")
    print(f"Bore ID:        Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"GNSS hole:      Ø{GNSS_HOLE_D} through, centered")
    print(f"Clamp bolts:    {len(BOLT_XS) * len(BOLT_YS)}× M4 at X=±{BOLT_X_OFFSET}, "
          f"Y = {', '.join(f'{y:.2f}' for y in BOLT_YS)}")
    print()

    half = build_half()
    out = OUT_DIR / "gnss_saddle_quad_half.stl"
    export_stl(half, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)")

    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Print 2 copies. Assemble with 12× M4 × 30 mm socket caps + M4 nuts.")
    print("Hardware BOM:")
    print("  - 12× M4 × 30 mm socket-cap screws (stainless)")
    print("  - 12× M4 nuts (standard, fits Ø8 counterbore)")
    print("  - 12× M4 washers (optional)")


if __name__ == "__main__":
    main()
