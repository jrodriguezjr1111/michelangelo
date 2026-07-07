"""
CyberWing — Jetson Nano saddle, derived from make_gnss_saddle.py.

Same Ø15.39 dual-tube clamp (central GNSS hole + 4× M4 clamp bolts), enlarged to
carry a Jetson Nano that sits centered OVER the GNSS cutout:
  - BLOCK_LEN grown in −X and +X  (50 → 110 mm).
  - 4× M3 Jetson Nano mounts centered on Y=0 (over the GNSS hole). The Nano's
    86 mm hole span runs ACROSS the tubes, so the two rows straddle the bores
    (Y = ±43.07, just outboard of each Ø15.8 bore); the 58 mm span runs along X.
  - Block stays SYMMETRIC in Y, sized to wrap the Nano rows (Y → ~101.5 mm).

Coordinate frame (model == print orientation):
  X = along tube axis, Y = across tubes (tubes at Y = ±TUBE_CENTER_SEP/2),
  Z = build. z=0 = BED (outer face), z=HALF_HT = SPLIT face (up).

Both halves identical (print two); the Nano mounts on the top half, over the hole.

Output:
  gnss_saddle_nano_half.stl
"""

from build123d import *
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================

# Tubes (from make_gnss_saddle.py)
TUBE_OD         = 15.39
TUBE_CENTER_SEP = 60.17
CLEARANCE       = 0.4

# GNSS antenna through-hole (centered, kept) — the Nano sits over this.
GNSS_HOLE_D = 30.0

# Block height (unchanged)
BLOCK_HT = 28.0

# X grown symmetrically (−X and +X): 50 → 110.
BLOCK_LEN = 110.0

# Clamp bolts (M4) — unchanged positions.
BOLT_X_OFFSET = 18.0
BOLT_Y_OFFSET = 18.0
SCREW_CLEAR_D  = 4.4
SCREW_HEAD_D   = 8.0
SCREW_HEAD_DEPTH = 4.5

# Jetson Nano mount holes (M3), centered over the GNSS hole. The 86 mm span runs
# ACROSS the tubes (rows straddle the bores); the 58 mm span runs along X.
NANO_PAT_X = 58.25         # along tube axis (X)
NANO_PAT_Y = 86.14         # across tubes (Y) — rows straddle the bores
M3_CLEAR_D = 3.4
EDGE_Y     = 6.0           # Nano hole → ±Y edge

OUT_DIR = Path(__file__).parent

# =============================================================================
# Derived
# =============================================================================

HALF_HT = BLOCK_HT / 2
R_IN    = TUBE_OD / 2 + CLEARANCE / 2
TUBE_Y  = TUBE_CENTER_SEP / 2
GNSS_R  = GNSS_HOLE_D / 2

# Nano rows straddle the tube bores, centered on Y=0 (over the GNSS cutout).
NANO_Y_CENTER = 0.0
NANO_ROW      = NANO_PAT_Y / 2          # ±43.07

# Symmetric block in Y, sized to wrap the Nano rows.
Y_HALF = NANO_ROW + M3_CLEAR_D / 2 + EDGE_Y
Y_POS, Y_NEG = Y_HALF, -Y_HALF
BLOCK_WID   = 2 * Y_HALF
BLOCK_Y_MID = 0.0

# =============================================================================
# Sanity
# =============================================================================
assert R_IN + 2.0 <= HALF_HT, "Half-height must clear tube bore radius + wall"
assert NANO_ROW - M3_CLEAR_D / 2 > TUBE_Y + R_IN, "Nano rows clash the tube bores"
assert Y_HALF >= TUBE_Y + R_IN + 2.0, "Block too narrow for tubes + wall"
assert GNSS_R + 2.0 < BOLT_X_OFFSET, "GNSS hole too close to clamp bolts in X"
assert abs(BOLT_Y_OFFSET) + SCREW_CLEAR_D / 2 + 1.0 < TUBE_Y - R_IN, "Clamp bolts clash with tube bores"
assert GNSS_R + SCREW_CLEAR_D / 2 + 1.0 < (BOLT_X_OFFSET**2 + BOLT_Y_OFFSET**2)**0.5, "GNSS hole too close to a clamp bolt"
assert NANO_PAT_X / 2 + M3_CLEAR_D / 2 + 0.5 < BLOCK_LEN / 2, "Nano holes exit block in X"
# Nano board (~100 × 80) centered over the GNSS hole → covers the Ø30 cutout.
assert NANO_PAT_Y / 2 > GNSS_R and NANO_PAT_X / 2 > GNSS_R, "Nano footprint does not span the GNSS hole"


# =============================================================================
# Build one half (both halves identical — print twice)
# =============================================================================

def build_half() -> Part:
    block = Pos(0.0, BLOCK_Y_MID, 0.0) * Box(
        BLOCK_LEN, BLOCK_WID, HALF_HT,
        align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Two tube half-bores scooped from the split face (z=HALF_HT).
    for sy in (-1, 1):
        bore = Cylinder(R_IN, BLOCK_LEN + 0.2,
                        rotation=(0, 90, 0),
                        align=(Align.CENTER, Align.CENTER, Align.CENTER))
        block -= Pos(0.0, sy * TUBE_Y, HALF_HT) * bore

    # Central GNSS through-hole.
    block -= Pos(0.0, 0.0, -0.2) * Cylinder(
        GNSS_R, HALF_HT + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× M4 clamp bolts + head/nut counterbore on the outer face (z=0).
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * BOLT_X_OFFSET, sy * BOLT_Y_OFFSET
            block -= Pos(cx, cy, -0.2) * Cylinder(
                SCREW_CLEAR_D / 2, HALF_HT + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN))
            block -= Pos(cx, cy, -0.05) * Cylinder(
                SCREW_HEAD_D / 2, SCREW_HEAD_DEPTH + 0.1, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 4× Jetson Nano M3 through-holes, centered over the GNSS hole.
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx = sx * NANO_PAT_X / 2
            cy = NANO_Y_CENTER + sy * NANO_PAT_Y / 2
            block -= Pos(cx, cy, -0.2) * Cylinder(
                M3_CLEAR_D / 2, HALF_HT + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN))

    return block


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("CyberWing Jetson Nano saddle — from make_gnss_saddle.py")
    print("=" * 60)
    print(f"Block:        {BLOCK_LEN} × {BLOCK_WID:.2f} × {BLOCK_HT} mm "
          f"(symmetric Y) — was 50 × 90")
    print(f"Tubes:        Ø{TUBE_OD} at Y = ±{TUBE_Y:.2f} (sep {TUBE_CENTER_SEP})")
    print(f"Bore ID:      Ø{2 * R_IN:.2f} ({CLEARANCE} mm clearance)")
    print(f"GNSS hole:    Ø{GNSS_HOLE_D} through, centered (Nano sits over it)")
    print(f"M4 bolts:     4× at (±{BOLT_X_OFFSET}, ±{BOLT_Y_OFFSET})")
    print(f"Nano mounts:  4× Ø{M3_CLEAR_D} at (±{NANO_PAT_X/2:.2f}, ±{NANO_ROW:.2f}) "
          f"— centered on the GNSS hole")
    print()

    half = build_half()
    out = OUT_DIR / "gnss_saddle_nano_half.stl"
    export_stl(half, str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)")
    print("\nPrint orientation: outer face on bed, split face UP. No supports.")
    print("Print 2 identical halves; the Jetson Nano mounts over the GNSS hole.")


if __name__ == "__main__":
    main()
