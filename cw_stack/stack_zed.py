"""
CW-Stack instance — ZED-F9P box (standalone, saddle-mounted).

A single-component box: one ZED-F9P tray (bottom = saddle) + a flat lid.
The first real CW-Stack product; add a module above it later (IMU, LoRa, etc.)
and it becomes a stack.

ZED-F9P facts (from this project's make_gnss_enclosure.py):
  mounting holes 37.6 mm square, M2.5; board ~43 mm square.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from cw_stack import (Module, build_module, build_lid, stack_height,
                      FOOT_X, FOOT_Y, FLOOR_T, CAV_X, CAV_Y)
from build123d import export_stl

OUT = Path(__file__).parent

ZED_SQ = 37.6 / 2

ZED = Module(
    name="zed",
    height=16.0,                                   # board + USB-C / SMA connectors
    bottom="saddle",                               # M4 36.14 to the GNSS saddle
    standoffs=[(sx * ZED_SQ, sy * ZED_SQ) for sx in (-1, 1) for sy in (-1, 1)],
    standoff_od=6.0, standoff_h=6.0, standoff_pilot=2.5,   # M2.5 self-tap
    slots=[("-y", 12, 9, FLOOR_T + 1),             # USB-C cable bay (-Y wall)
           ("-y", 8, 6, FLOOR_T + 1)],             # SMA / u.FL antenna lead
    center_hole=20.0,                              # antenna up through the saddle's GNSS hole
)

if __name__ == "__main__":
    base = build_module(ZED)
    out = OUT / "stack_zed.stl"
    export_stl(base, str(out))
    print(f"  ✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)  — ZED-F9P tray, "
          f"{ZED.height} mm cavity, saddle bottom")

    lid = build_lid()
    out = OUT / "stack_zed_lid.stl"
    export_stl(lid, str(out))
    print(f"  ✓ {out.name}  ({out.stat().st_size/1024:.0f} KB)  — flat lid")

    H = stack_height([ZED])
    print(f"\n  Box:        {FOOT_X} x {FOOT_Y} x {H:.0f} mm; cavity {CAV_X} x {CAV_Y} x {ZED.height}")
    print(f"  ZED mount:  4x M2.5 standoffs at 37.6 sq; Ø20 antenna passthrough")
    print(f"  Saddle:     M4 36.14 x 36.1 in the floor; 4x M3 heat-set inserts for the lid clamp")
    print(f"  Cable:      USB-C bay + antenna slot on the -Y wall")
    print(f"  Print floor-down, no supports. Lid: 4x M3 (csk top) into the base inserts.")
