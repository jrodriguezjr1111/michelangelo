"""
CW-Stack instance — FlyCatcher module (sits on top of the ZED box).

The flycatcher is this project's IMU platform; here it's a CW-Stack module with
bottom="stack", so its floor groove nests onto the ZED box's tongue. Carries the
IMU pattern (19.95 x 17.81) and the flycatcher's signature cable slots on the
±X walls (cables exit parallel to the tubes). The existing stack_zed_lid.stl
caps it — no new lid needed.

Full assembly:  saddle --M4--> ZED box --tongue--> FLYCATCHER --tongue--> lid
One length of M3 (lid csk -> flycatcher floor -> ZED base inserts) clamps it.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from cw_stack import (Module, build_module, build_lid, stack_height,
                      FOOT_X, FOOT_Y, FLOOR_T, CAV_X, CAV_Y)
from stack_zed import ZED                          # reuse the ZED for stack math
from build123d import export_stl

OUT = Path(__file__).parent

IMU_X, IMU_Y = 19.95 / 2, 17.81 / 2

FLYCATCHER = Module(
    name="flycatcher",
    height=18.0,                                    # IMU + sensor headroom
    bottom="stack",                                 # nests on the ZED box's tongue
    standoffs=[(sx * IMU_X, sy * IMU_Y) for sx in (-1, 1) for sy in (-1, 1)],
    standoff_od=4.0, standoff_h=4.0, standoff_pilot=1.6,   # M2 self-tap (IMU)
    slots=[("+x", 38, 7.8, FLOOR_T + 2),            # flycatcher cable slots, ±X walls
           ("-x", 38, 7.8, FLOOR_T + 2)],
)

if __name__ == "__main__":
    out = OUT / "stack_flycatcher.stl"
    export_stl(build_module(FLYCATCHER), str(out))
    print(f"  ✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)  — FlyCatcher module, "
          f"{FLYCATCHER.height} mm cavity, stack bottom (nests on the ZED tongue)")

    stack = [ZED, FLYCATCHER]
    H = stack_height(stack)
    print(f"\n  Stack:      saddle -> ZED ({ZED.height}) -> flycatcher ({FLYCATCHER.height}) -> lid")
    print(f"  Assembled:  {H:.0f} mm tall  (M3 clamp length >= {H:.0f} mm — was 22 for ZED alone)")
    print(f"  IMU mount:  4x M2 standoffs at 19.95 x 17.81")
    print(f"  Cables:     38 x 7.8 slots on both ±X walls (parallel exits, flycatcher-style)")
    print(f"  Reuses:     stack_zed_lid.stl as the cap — print only this module to add it.")
