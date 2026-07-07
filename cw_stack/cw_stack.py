"""
CW-Stack — CyberWing stackable encasing modules (build123d library).

Generalizes the flycatcher platform/lid family into a parametric vertical stack.
Each MODULE is a 101 x 65 tray that encases ONE component; modules nest via a
perimeter tongue-and-groove rim (the "stacking-tray" registration, matching the
Pelican-tray look) and clamp with 4 long M3 bolts on the 58 x 49 pattern. The
bottom module mounts to the GNSS saddle (M4 36.14 x 36.1); a flat LID caps the top.

  footprint   101 x 65    (CyberWing standard: saddle / flycatcher / carrier)
  cavity      96 x 60      (walls 2.5, floor 3)
  registration  1.5 mm wall-top tongue  +  matching 1.7 mm floor-underside groove
  clamp       4x M3 on 58 x 49 — long bolts run lid -> modules -> base inserts
  base mount  M4 36.14 x 36.1 to the saddle (decoupled from the M3 stack clamp)

ASSEMBLY (bottom -> top):
  saddle --M4--> BASE module (component 1, M3 heat-set inserts in its floor)
         --tongue--> MODULE (component 2) --tongue--> ... --tongue--> LID
  One length of M3 from the lid's csk top threads down into the base inserts and
  clamps everything; the tongue/groove keeps each layer registered.

This file is a LIBRARY — no parameters, no __main__ that builds. Instance files
(stack_<thing>.py) define component configs and call build_base/module/lid.
Every box in the family shares this geometry, so modules with matching heights
and the same footprint interchange.
"""

from build123d import *
from dataclasses import dataclass, field

# ---- footprint / shell ------------------------------------------------------
FOOT_X, FOOT_Y = 101.0, 65.0
WALL_T  = 2.5
FLOOR_T = 3.0
CAV_X   = FOOT_X - 2 * WALL_T      # 96
CAV_Y   = FOOT_Y - 2 * WALL_T      # 60

# ---- clamp bolts (flycatcher 58 x 49) ---------------------------------------
M3_PAT_X, M3_PAT_Y = 58.0, 49.0
M3_CLEAR  = 3.4
M3_CSK_D  = 6.0
M3_CSK_H  = 1.8
M3_INSERT_D = 4.0                  # M3 heat-set bore (base floor)
M3_INSERT_H = 5.0
M3_POS = [(sx * M3_PAT_X / 2, sy * M3_PAT_Y / 2) for sx in (-1, 1) for sy in (-1, 1)]

# ---- saddle mount (base only) ----------------------------------------------
M4_PAT_X, M4_PAT_Y = 36.14, 36.1
M4_CLEAR = 4.4
M4_POS = [(sx * M4_PAT_X / 2, sy * M4_PAT_Y / 2) for sx in (-1, 1) for sy in (-1, 1)]

# ---- registration tongue/groove (centered on the wall) ----------------------
TONGUE_W = 1.6
TONGUE_H = 1.5
FIT      = 0.20                    # groove clearance per side (PLA: snug press)

_C   = (Align.CENTER, Align.CENTER, Align.MIN)
_eps = 0.1

# tongue ring footprint (centered on the 2.5 mm wall)
_TO_X = FOOT_X - (WALL_T - TONGUE_W)     # 100.1
_TO_Y = FOOT_Y - (WALL_T - TONGUE_W)     # 64.1
_TI_X = CAV_X  + (WALL_T - TONGUE_W)     # 96.9
_TI_Y = CAV_Y  + (WALL_T - TONGUE_W)     # 60.9
# groove ring (floor underside) = tongue + FIT per side
_GO_X, _GO_Y = _TO_X + 2 * FIT, _TO_Y + 2 * FIT
_GI_X, _GI_Y = _TI_X - 2 * FIT, _TI_Y - 2 * FIT
GROOVE_DEPTH = TONGUE_H + FIT             # 1.7  (< FLOOR_T, leaves ~1.3 mm)


@dataclass
class Module:
    name: str
    height: float                                  # cavity clear height (component space)
    standoffs: list = field(default_factory=list)  # [(x, y), ...] interior coords, origin = center
    standoff_od: float = 6.0
    standoff_h: float = 6.0
    standoff_pilot: float = 2.5                     # M2.5 self-tap; 4.0 for M3 heat-set
    slots: list = field(default_factory=list)       # [(wall, w, h, z0)] centered wall slots
    ports: list = field(default_factory=list)       # [Port(...)] offset rect / round wall cuts
    bottom: str = "stack"                           # "stack" | "saddle"
    center_hole: float = 0.0                        # optional Ø passthrough in the floor


@dataclass
class Port:
    """A located connector opening in a wall (origin = footprint center).
    rect:  (off along wall, z0 = bottom) sized w x h.
    round: (off along wall, z = centerline) bore Ø d; optional OUTSIDE counterbore
           (pocket_d x pocket_depth) seats a retainer ring / washer."""
    wall: str                                       # "+x" "-x" "+y" "-y"
    kind: str = "rect"                              # "rect" | "round"
    off: float = 0.0                                # offset along the wall axis
    z: float = 0.0                                  # rect: z0 (min);  round: centerline z
    w: float = 0.0
    h: float = 0.0
    d: float = 0.0
    pocket_d: float = 0.0
    pocket_depth: float = 0.0


# ---- shared geometry helpers ------------------------------------------------
def _ring(ox, oy, iz, h):
    return Box(ox, oy, h, align=_C) - Box(iz[0], iz[1], h + 1, align=_C)


def _tongue():
    return _ring(_TO_X, _TO_Y, (_TI_X, _TI_Y), TONGUE_H)


def _groove_cut(part):
    return part - Pos(0, 0, -_eps) * _ring(_GO_X, _GO_Y, (_GI_X, _GI_Y), GROOVE_DEPTH + _eps)


def _cut_slot(part, wall, w, h, z0):
    if wall in ("+x", "-x"):
        sx = 1 if wall == "+x" else -1
        return part - Pos(sx * FOOT_X / 2, 0, z0) * Box(
            WALL_T + 2, w, h, align=(Align.MAX if sx > 0 else Align.MIN, Align.CENTER, Align.MIN))
    sy = 1 if wall == "+y" else -1
    return part - Pos(0, sy * FOOT_Y / 2, z0) * Box(
        w, WALL_T + 2, h, align=(Align.CENTER, Align.MAX if sy > 0 else Align.MIN, Align.MIN))


def _wall_axis(wall):
    """(sign, normal_is_x) for a wall id."""
    return {"+x": (1, True), "-x": (-1, True),
            "+y": (1, False), "-y": (-1, False)}[wall]


def _cut_slot_off(part, wall, w, h, z0, off=0.0):
    """Rectangular wall cut offset by `off` along the wall axis."""
    s, nx = _wall_axis(wall)
    if nx:
        return part - Pos(s * FOOT_X / 2, off, z0) * Box(
            WALL_T + 2, w, h, align=(Align.MAX if s > 0 else Align.MIN, Align.CENTER, Align.MIN))
    return part - Pos(off, s * FOOT_Y / 2, z0) * Box(
        w, WALL_T + 2, h, align=(Align.CENTER, Align.MAX if s > 0 else Align.MIN, Align.MIN))


def _cut_round(part, wall, d, off, z, pocket_d=0.0, pocket_depth=0.0):
    """Round bore through a wall at (off, z), normal = wall. Optional OUTSIDE
    counterbore (pocket_d x pocket_depth) seats a retainer ring / washer."""
    s, nx = _wall_axis(wall)
    rot = Rotation(0, 90, 0) if nx else Rotation(90, 0, 0)
    if nx:
        cpos = Pos(s * (FOOT_X / 2 - WALL_T / 2), off, z)
    else:
        cpos = Pos(off, s * (FOOT_Y / 2 - WALL_T / 2), z)
    part -= cpos * rot * Cylinder(d / 2, WALL_T + 2, align=_C)
    if pocket_d > 0:
        if nx:
            xc = s * (FOOT_X / 2 - pocket_depth / 2 + _eps)
            ppos = Pos(xc, off, z)
        else:
            yc = s * (FOOT_Y / 2 - pocket_depth / 2 + _eps)
            ppos = Pos(off, yc, z)
        part -= ppos * rot * Cylinder(pocket_d / 2, pocket_depth + _eps, align=_C)
    return part


def _standoffs(part, m: Module):
    for x, y in m.standoffs:
        c = Pos(x, y, FLOOR_T)
        part += c * Cylinder(m.standoff_od / 2, m.standoff_h, align=_C)
        part -= c * Cylinder(m.standoff_pilot / 2, m.standoff_h + 0.1, align=_C)
    return part


# ---- builders ---------------------------------------------------------------
def build_module(m: Module) -> Part:
    """A stacking tray: floor + walls (cavity) + top tongue; bottom 'stack' gets
    the underside groove, bottom 'saddle' gets M4 holes + M3 heat-set inserts."""
    top_z = FLOOR_T + m.height
    part = Box(FOOT_X, FOOT_Y, top_z, align=_C)
    part -= Pos(0, 0, FLOOR_T) * Box(CAV_X, CAV_Y, m.height + 1, align=_C)

    part += Pos(0, 0, top_z) * _tongue()                 # registration tongue
    if m.bottom == "stack":
        part = _groove_cut(part)                         # mates the tongue below

    if m.bottom == "saddle":
        for x, y in M4_POS:                              # saddle clamp bolts
            part -= Pos(x, y, -_eps) * Cylinder(M4_CLEAR / 2, FLOOR_T + 0.4, align=_C)
        for x, y in M3_POS:                              # M3 heat-set inserts (from cavity side)
            part -= Pos(x, y, FLOOR_T - M3_INSERT_H) * Cylinder(M3_INSERT_D / 2, M3_INSERT_H + _eps, align=_C)
    else:
        for x, y in M3_POS:                              # M3 clamp clearance, full height
            part -= Pos(x, y, -_eps) * Cylinder(M3_CLEAR / 2, top_z + TONGUE_H + 0.4, align=_C)

    if m.center_hole > 0:
        part -= Pos(0, 0, -_eps) * Cylinder(m.center_hole / 2, FLOOR_T + 0.4, align=_C)

    part = _standoffs(part, m)
    for wall, w, h, z0 in m.slots:
        part = _cut_slot(part, wall, w, h, z0)
    for p in m.ports:
        if p.kind == "round":
            part = _cut_round(part, p.wall, p.d, p.off, p.z, p.pocket_d, p.pocket_depth)
        else:
            part = _cut_slot_off(part, p.wall, p.w, p.h, p.z, p.off)
    return part


def build_lid(cuts=None) -> Part:
    """Flat cap: nests onto the top module's tongue, M3 clamp holes csk on top."""
    part = Box(FOOT_X, FOOT_Y, FLOOR_T, align=_C)
    part = _groove_cut(part)
    for x, y in M3_POS:
        part -= Pos(x, y, -_eps) * Cylinder(M3_CLEAR / 2, FLOOR_T + 0.4, align=_C)
        part -= Pos(x, y, FLOOR_T - M3_CSK_H) * Cylinder(M3_CSK_D / 2, M3_CSK_H + 0.1, align=_C)
    for wall, w, h, z0 in (cuts or []):
        part = _cut_slot(part, wall, w, h, z0)
    return part


def build_skylid(win_x, win_y, win, ledge_w=2.0, ledge_d=1.2, cuts=None) -> Part:
    """Flat cap with a square SKY APERTURE over (win_x, win_y) for a GPS patch to
    radiate straight up. A recessed ledge on the top seats an optional radome
    (build_radome). Otherwise identical to build_lid (groove + M3 csk clamp)."""
    part = Box(FOOT_X, FOOT_Y, FLOOR_T, align=_C)
    part = _groove_cut(part)
    for x, y in M3_POS:
        part -= Pos(x, y, -_eps) * Cylinder(M3_CLEAR / 2, FLOOR_T + 0.4, align=_C)
        part -= Pos(x, y, FLOOR_T - M3_CSK_H) * Cylinder(M3_CSK_D / 2, M3_CSK_H + 0.1, align=_C)
    # open aperture (full through) + top ledge for the radome to drop into
    part -= Pos(win_x, win_y, -_eps) * Box(win, win, FLOOR_T + 0.4,
                                           align=(Align.CENTER, Align.CENTER, Align.MIN))
    part -= Pos(win_x, win_y, FLOOR_T - ledge_d) * Box(
        win + 2 * ledge_w, win + 2 * ledge_w, ledge_d + _eps,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    for wall, w, h, z0 in (cuts or []):
        part = _cut_slot(part, wall, w, h, z0)
    return part


def build_radome(win, ledge_w=2.0, t=0.8, fit=0.3) -> Part:
    """Thin RF-transparent window that drops into build_skylid's ledge (snap/glue).
    0.8 mm PLA is ~transparent at GNSS L1; omit it to leave the patch fully open."""
    s = win + 2 * ledge_w - fit
    return Box(s, s, t, align=(Align.CENTER, Align.CENTER, Align.MIN))


def stack_height(modules) -> float:
    """Assembled height: sum of (floor + cavity) per module + lid floor."""
    return sum(FLOOR_T + m.height for m in modules) + FLOOR_T
