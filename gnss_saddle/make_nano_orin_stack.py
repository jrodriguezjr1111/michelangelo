"""
Modular ventilated stack: Jetson Nano (base) + Jetson Orin Nano (above),
mounted on top of the GNSS dual-tube saddle (make_gnss_saddle.py).

Parts (4 STLs):
  stack_base.stl    — SOLID floor; Nano standoffs; 4× M4 saddle mounts (±18);
                      central passthrough; 4 corner posts (Nano compartment).
  stack_middle.stl  — HEX-perforated deck; Orin standoffs on top; corner screw
                      holes; 4 corner posts (Orin compartment). Nano's ceiling,
                      Orin's floor.
  stack_top.stl     — HEX-perforated cap; corner screw holes.
  stack_wall.stl    — HEX-perforated side panel (long side, one compartment).

Stack join: 4 corner posts (Ø8 tube, M3 bore) on each deck; the deck above
bolts down onto the posts below with M3 screws (head recessed in the post bore,
nut/insert at the post top — exact hardware is the assembler's choice).

Frame: X across, Y = board long axis, Z = up. Boards oriented long-axis along Y.
Print each deck floor-down; no supports.
"""

from build123d import *
from math import sqrt
from pathlib import Path

# =============================================================================
# PARAMETERS
# =============================================================================
# Board mount-hole patterns (X, Y) in this frame (long axis along Y)
NANO_HX, NANO_HY = 58.25, 86.14      # Jetson Nano
ORIN_HX, ORIN_HY = 58.0, 92.0        # Jetson Orin Nano (from orin_box: 92 × 58)
STANDOFF_OD, STANDOFF_H, STANDOFF_PILOT = 6.0, 8.0, 2.5   # M3 self-tap

# Deck plate
DECK_X, DECK_Y, DECK_T = 100.0, 128.0, 3.0
BORDER = 6.0                          # solid border before perforation

# Corner posts (stack columns)
POST_X, POST_Y = 41.0, 58.0           # ± positions (beyond the board ends)
POST_OD, POST_BORE = 8.0, 3.4         # Ø8 tube, M3 clearance bore
NANO_GAP, ORIN_GAP = 34.0, 34.0       # board+heatsink / board+fan (post lengths)

# Saddle mount
M4_PAT, M4_CLEAR_D = 18.0, 4.4

# Hex (honeycomb) perforation
HEX_AF, HEX_WEB = 8.0, 2.2            # flat-to-flat, web between holes
HEX_R = HEX_AF / sqrt(3)             # circumradius
HEX_KEEPOUT = 2.0

WALL_T = 3.0

OUT_DIR = Path(__file__).parent
C = (Align.CENTER, Align.CENTER, Align.MIN)
POSTS = [(sx * POST_X, sy * POST_Y) for sx in (-1, 1) for sy in (-1, 1)]

# =============================================================================
# Sanity
# =============================================================================
assert POST_X + POST_OD / 2 < DECK_X / 2, "Corner posts exit deck in X"
assert POST_Y + POST_OD / 2 < DECK_Y / 2, "Corner posts exit deck in Y"
assert NANO_HY / 2 + STANDOFF_OD / 2 < POST_Y, "Nano standoffs clash corner posts"
assert ORIN_HY / 2 + STANDOFF_OD / 2 < POST_Y, "Orin standoffs clash corner posts"
assert STANDOFF_H > 5.0, "Standoff too short to clear an M4 cap head on the base"


# =============================================================================
# Helpers
# =============================================================================
def hex_holes(rx, ry, thickness, keepouts):
    """Honeycomb hole pattern (centered) as a solid to subtract, clear of keepouts."""
    R, D = HEX_R, HEX_AF + HEX_WEB
    dx, dy = D, D * sqrt(3) / 2
    xmax, ymax = rx / 2 - BORDER - R, ry / 2 - BORDER - R
    sk = None
    ny = int(ymax / dy) + 2
    nx = int(xmax / dx) + 2
    for j in range(-ny, ny + 1):
        y = j * dy
        if abs(y) > ymax:
            continue
        xoff = (dx / 2) if (j % 2) else 0.0
        for i in range(-nx, nx + 1):
            x = i * dx + xoff
            if abs(x) > xmax:
                continue
            if any((x - kx) ** 2 + (y - ky) ** 2 < (kr + R) ** 2 for kx, ky, kr in keepouts):
                continue
            poly = Pos(x, y) * RegularPolygon(R, 6, rotation=90)
            sk = poly if sk is None else sk + poly
    if sk is None:
        return None
    return Pos(0, 0, -0.2) * extrude(sk, amount=thickness + 0.4)


def add_corner_posts(part, height):
    for px, py in POSTS:
        part += Pos(px, py, DECK_T) * Cylinder(POST_OD / 2, height, align=C)
        part -= Pos(px, py, -0.2) * Cylinder(POST_BORE / 2, DECK_T + height + 0.4, align=C)
    return part


def standoffs(part, hx, hy):
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Pos(sx * hx / 2, sy * hy / 2, DECK_T)
            part += c * Cylinder(STANDOFF_OD / 2, STANDOFF_H, align=C)
            part -= c * Cylinder(STANDOFF_PILOT / 2, STANDOFF_H + 0.1, align=C)
    return part


# =============================================================================
# Parts
# =============================================================================
def build_base() -> Part:
    p = Box(DECK_X, DECK_Y, DECK_T, align=C)
    p = standoffs(p, NANO_HX, NANO_HY)
    for sx in (-1, 1):
        for sy in (-1, 1):
            p -= Pos(sx * M4_PAT, sy * M4_PAT, -0.2) * Cylinder(M4_CLEAR_D / 2, DECK_T + 0.4, align=C)
    p = add_corner_posts(p, NANO_GAP)
    return p


def build_middle() -> Part:
    p = Box(DECK_X, DECK_Y, DECK_T, align=C)
    keep = [(px, py, POST_OD / 2 + HEX_KEEPOUT) for px, py in POSTS]
    keep += [(sx * ORIN_HX / 2, sy * ORIN_HY / 2, STANDOFF_OD / 2 + HEX_KEEPOUT)
             for sx in (-1, 1) for sy in (-1, 1)]
    holes = hex_holes(DECK_X, DECK_Y, DECK_T, keep)
    if holes is not None:
        p -= holes
    for px, py in POSTS:
        p -= Pos(px, py, -0.2) * Cylinder(POST_BORE / 2, DECK_T + 0.4, align=C)
    p = standoffs(p, ORIN_HX, ORIN_HY)
    p = add_corner_posts(p, ORIN_GAP)
    return p


def build_top() -> Part:
    p = Box(DECK_X, DECK_Y, DECK_T, align=C)
    keep = [(px, py, POST_OD / 2 + HEX_KEEPOUT) for px, py in POSTS]
    holes = hex_holes(DECK_X, DECK_Y, DECK_T, keep)
    if holes is not None:
        p -= holes
    for px, py in POSTS:
        p -= Pos(px, py, -0.2) * Cylinder(POST_BORE / 2, DECK_T + 0.4, align=C)
    return p


def build_wall() -> Part:
    WALL_W = 2 * POST_Y - POST_OD        # long-side span between posts
    WALL_H = NANO_GAP
    p = Box(WALL_W, WALL_H, WALL_T, align=C)
    mh = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            hx, hy = sx * (WALL_W / 2 - 5), sy * (WALL_H / 2 - 5)
            p -= Pos(hx, hy, -0.2) * Cylinder(POST_BORE / 2, WALL_T + 0.4, align=C)
            mh.append((hx, hy, POST_BORE / 2 + HEX_KEEPOUT))
    holes = hex_holes(WALL_W, WALL_H, WALL_T, mh)
    if holes is not None:
        p -= holes
    return p


# =============================================================================
# Main
# =============================================================================
def main() -> None:
    print("=" * 60)
    print("Modular Nano + Orin stack on the GNSS saddle")
    print("=" * 60)
    total_h = DECK_T + NANO_GAP + DECK_T + ORIN_GAP + DECK_T
    print(f"Deck:         {DECK_X} × {DECK_Y} × {DECK_T} mm")
    print(f"Compartments: Nano {NANO_GAP} mm, Orin {ORIN_GAP} mm  (stack ~{total_h:.0f} mm tall)")
    print(f"Corner posts: 4× Ø{POST_OD} at (±{POST_X}, ±{POST_Y}), M3 bore")
    print(f"Nano mounts:  4× standoff at ±{NANO_HX/2:.2f} × ±{NANO_HY/2:.2f}")
    print(f"Orin mounts:  4× standoff at ±{ORIN_HX/2:.2f} × ±{ORIN_HY/2:.2f}")
    print(f"Saddle mount: 4× M4 at (±{M4_PAT}, ±{M4_PAT})")
    print(f"Perforation:  hex AF {HEX_AF}, web {HEX_WEB}")
    print()
    for name, fn in (("stack_base", build_base), ("stack_middle", build_middle),
                     ("stack_top", build_top), ("stack_wall", build_wall)):
        part = fn()
        out = OUT_DIR / f"{name}.stl"
        export_stl(part, str(out))
        print(f"  ✓ {out.name} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
