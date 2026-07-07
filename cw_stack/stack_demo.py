"""
CW-Stack instance — demo 2-component stack.

Bottom: ZED-F9P module (mounts the GNSS saddle via M4).
Middle: IMU module.
Top:    flat lid.

Each box in the family is a file like this: pick components, set heights/standoffs/
slots, build. cw_stack.py supplies all the joint geometry.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from cw_stack import (Module, build_module, build_lid, stack_height,
                      FOOT_X, FOOT_Y, FLOOR_T, CAV_X, CAV_Y)
from build123d import export_stl

OUT = Path(__file__).parent

# --- component standoff patterns (interior coords, origin = footprint center) ---
ZED_SQ  = 37.6 / 2                                  # ZED-F9P 37.6 mm square
IMU_X, IMU_Y = 19.95 / 2, 17.81 / 2                 # IMU 19.95 x 17.81

ZED = Module(
    name="zed",
    height=16.0,                                    # board + connectors
    bottom="saddle",                                # mounts the GNSS saddle
    standoffs=[(sx * ZED_SQ, sy * ZED_SQ) for sx in (-1, 1) for sy in (-1, 1)],
    standoff_pilot=2.5,                             # M2.5 self-tap
    slots=[("-y", 28, 13, FLOOR_T + 1),             # USB-C bay on the -Y wall
           ("-y", 8, 8, FLOOR_T + 1)],
    center_hole=20.0,                               # antenna cable up from the saddle hole
)

IMU = Module(
    name="imu",
    height=10.0,
    standoffs=[(sx * IMU_X, sy * IMU_Y) for sx in (-1, 1) for sy in (-1, 1)],
    standoff_pilot=1.6,                             # M2 self-tap
    slots=[("-y", 12, 8, FLOOR_T + 1)],             # IMU cable
)

MODULES = [ZED, IMU]

if __name__ == "__main__":
    for m in MODULES:
        out = OUT / f"stack_{m.name}.stl"
        export_stl(build_module(m), str(out))
        print(f"  ✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)  — {m.name} module, "
              f"{m.height} mm cavity, {'saddle' if m.bottom=='saddle' else 'stack'} bottom")
    lid = build_lid()
    out = OUT / "stack_lid.stl"
    export_stl(lid, str(out))
    print(f"  ✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)  — flat lid")

    H = stack_height(MODULES)
    print(f"\n  Footprint:  {FOOT_X} x {FOOT_Y} mm; cavity {CAV_X} x {CAV_Y}")
    print(f"  Stack:      {' -> '.join(m.name for m in MODULES)} -> lid")
    print(f"  Assembled:  {H:.1f} mm tall  (M3 clamp length >= {H:.0f} mm)")
    print(f"  Clamp:      4x M3 lid(csk) -> module floors -> ZED base heat-set inserts")
    print(f"  Saddle:     ZED base M4 36.14 x 36.1; antenna passthrough Ø20")
