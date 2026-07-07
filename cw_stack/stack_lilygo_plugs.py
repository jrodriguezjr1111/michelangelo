"""
CW-Stack — LilyGo cable plugs (print these alongside stack_lilygo.stl).

  usbc_clamshell.stl  — ONE half of a two-part clamshell that traps the USB-C
        cable in the -X bay. The cable channel is centered on the split plane, so
        the two halves are IDENTICAL — print this part x2, they mirror each other.
        Body passes through the 13x8 bay; the oversized flange stops it on the
        inside wall face so cable tension can't pull it out.

  sma_retainer.stl    — hex ring that seats in the +X Ø11 counterbore; the SMA
        barrel passes through its Ø7.2 bore and the antenna's coupling nut clamps
        the ring (and the wall), locking the bulkhead. Hex flats give a grip.

Dims key off the same connector ports as stack_lilygo.py — keep them in sync.
"""

from pathlib import Path
from build123d import *

OUT = Path(__file__).parent
_C = (Align.CENTER, Align.CENTER, Align.CENTER)

# ---- USB-C clamshell (one identical half) -----------------------------------
USBC_W, USBC_H = 13.0, 8.0          # the -X bay (must match stack_lilygo.py USBC)
DEPTH = 12.0                         # plug length into the box
FLANGE_T = 2.5                       # inner stop flange
CABLE_D = 5.0                        # USB-C cable / overmold neck (grips when halved)
FIT = 0.4                            # plug-in-bay clearance (total)


def usbc_clamshell_half() -> Part:
    bw, bh = USBC_W - FIT, USBC_H - FIT
    body = Box(DEPTH, bw, bh, align=_C)
    flange = Pos(-(DEPTH / 2 + FLANGE_T / 2), 0, 0) * Box(FLANGE_T, bw + 6, bh + 6, align=_C)
    plug = body + flange
    plug -= Rotation(0, 90, 0) * Cylinder(CABLE_D / 2, DEPTH + FLANGE_T + 2, align=_C)  # channel on z=0
    # keep the z >= 0 half; flat split face sits on the bed
    keep = Box(200, 200, 100, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return plug & keep


# ---- SMA retainer ring -------------------------------------------------------
SMA_BORE = 7.2                       # clearance over the SMA barrel (Ø6.35)
RING_AF  = 12.0                      # hex across-flats (grip)
RING_H   = 4.0
SEAT_D   = 10.8                      # register boss -> +X Ø11 counterbore
SEAT_H   = 1.5


def sma_retainer() -> Part:
    af = RING_AF / 2 / (3 ** 0.5 / 2)            # across-flats -> circumradius
    ring = extrude(RegularPolygon(af, 6), RING_H)               # z 0..4
    ring += Pos(0, 0, RING_H) * Cylinder(SEAT_D / 2, SEAT_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    ring -= Cylinder(SMA_BORE / 2, RING_H + SEAT_H + 2,
                     align=(Align.CENTER, Align.CENTER, Align.MIN))
    return ring


if __name__ == "__main__":
    a = usbc_clamshell_half()
    export_stl(a, str(OUT / "usbc_clamshell.stl"))
    print(f"  ✓ usbc_clamshell.stl  ({(OUT/'usbc_clamshell.stl').stat().st_size/1024:.0f} KB)  "
          f"— print x2; channel Ø{CABLE_D}, body {USBC_W-FIT:.1f}x{USBC_H-FIT:.1f}, flange stops pull-out")

    r = sma_retainer()
    export_stl(r, str(OUT / "sma_retainer.stl"))
    print(f"  ✓ sma_retainer.stl   ({(OUT/'sma_retainer.stl').stat().st_size/1024:.0f} KB)  "
          f"— hex AF{RING_AF}, bore Ø{SMA_BORE}, seat Ø{SEAT_D}x{SEAT_H} into the counterbore")
