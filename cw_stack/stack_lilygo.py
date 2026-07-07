"""
CW-Stack instance — LilyGo SX1262 module (sits on top of the FlyCatcher box).

bottom="stack" — its floor groove nests onto the FlyCatcher's tongue. The LilyGo
mount pattern (95.33 x 28.55, M2) is nearly footprint-wide, so the ±X standoffs
sit at the cavity walls and merge into them as bosses; the Y standoffs stand free.

Cable support (from the photographed board):
  -X end : USB-C connector  -> rectangular bay sized for a two-part clamshell that
           traps the cable (built in stack_lilygo_plugs.py).
  +X end : SMA antenna barrel -> round Ø7 bore + outside counterbore that seats a
           printed retainer ring (stack_lilygo_plugs.py).

NOTE — the connector OFFSETS / HEIGHTS below are read off the photos; confirm them
against calipers and nudge. Everything downstream (bays, plugs) keys off them.

Full stack:  saddle -> ZED -> FlyCatcher -> LILYGO -> lid
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from cw_stack import (Module, Port, build_module, build_skylid, build_radome,
                      stack_height, FOOT_X, FOOT_Y, FLOOR_T, CAV_X, CAV_Y, WALL_T,
                      M3_PAT_X)
from stack_zed import ZED
from stack_flycatcher import FLYCATCHER
from build123d import export_stl

OUT = Path(__file__).parent

# ---- LilyGo SX1262 mount (make_base_stacked.py: M2 95.33 x 28.55) -----------
LG_X, LG_Y = 95.33 / 2, 28.55 / 2                  # 47.665, 14.275
SO_H = 4.0                                          # standoff height
BOARD_TOP = FLOOR_T + SO_H + 1.6                    # 8.6  (board upper face)

# ---- connector locations on the ±X end walls  (CONFIRM vs calipers) ---------
# USB-C: rectangular bay on the -X end (offset along Y, sized for the clamshell)
USBC = Port(wall="-x", kind="rect", off=+7.0, z=6.0, w=13.0, h=8.0)
# SMA: round barrel bore on the +X end + outside counterbore for the retainer ring
SMA  = Port(wall="+x", kind="round", off=-7.0, z=BOARD_TOP + 1.9,   # ~10.5 centerline
            d=7.0, pocket_d=11.0, pocket_depth=1.6)

# ---- GPS ceramic patch (radiates +Z) — REORIENT board component-side UP ------
# The patch sits on the board's top face near the +X (SMA) end. It must see sky,
# so LilyGo is the crowning module and the lid carries an aperture right over it.
PATCH_X, PATCH_Y = +34.0, 0.0      # patch center on the board (CONFIRM vs caliper)
PATCH = 18.0                        # patch edge (typ. 18 sq active patch)
WIN   = PATCH + 3.0                 # sky aperture = patch + clearance
RADOME_T = 0.8                      # optional weather window (RF-transparent @ L1)

LILYGO = Module(
    name="lilygo",
    height=16.0,
    bottom="stack",                                # nests on the FlyCatcher tongue
    standoffs=[(sx * LG_X, sy * LG_Y) for sx in (-1, 1) for sy in (-1, 1)],
    standoff_od=4.5, standoff_h=SO_H, standoff_pilot=1.6,   # M2; ±X bosses fuse walls
    ports=[USBC, SMA],
)

if __name__ == "__main__":
    out = OUT / "stack_lilygo.stl"
    export_stl(build_module(LILYGO), str(out))
    print(f"  ✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)  — LilyGo module, "
          f"{LILYGO.height} mm cavity, stack bottom")

    sky = OUT / "stack_lilygo_skylid.stl"
    export_stl(build_skylid(PATCH_X, PATCH_Y, WIN), str(sky))
    print(f"  ✓ {sky.name}  ({sky.stat().st_size/1024:.0f} KB)  — top cap, "
          f"Ø-sky aperture {WIN} sq over the patch + radome ledge")

    rad = OUT / "lilygo_radome.stl"
    export_stl(build_radome(WIN, t=RADOME_T), str(rad))
    print(f"  ✓ {rad.name}  ({rad.stat().st_size/1024:.0f} KB)  — {RADOME_T} mm weather window (optional)")

    H = stack_height([ZED, FLYCATCHER, LILYGO])
    print(f"\n  Stack:      saddle -> ZED ({ZED.height}) -> flycatcher ({FLYCATCHER.height}) "
          f"-> lilygo ({LILYGO.height}) -> SKYLID  =  {H:.0f} mm")
    print(f"  Reorient:   board component-side UP; GPS patch faces +Z (sky)")
    print(f"  Sky window: {WIN} sq aperture @ ({PATCH_X:+.0f},{PATCH_Y:+.0f}) over the {PATCH} patch; "
          f"open, or drop in the {RADOME_T} mm radome")
    print(f"  USB-C bay:  -X end, Y{USBC.off:+.0f}, {USBC.w}x{USBC.h}  (clamshell)")
    print(f"  SMA bore:   +X end, Y{SMA.off:+.0f}, Ø{SMA.d} @ z {SMA.z:.1f}  (retainer ring)")
    print(f"  Plugs:      run stack_lilygo_plugs.py for the clamshell + retainer STLs")
