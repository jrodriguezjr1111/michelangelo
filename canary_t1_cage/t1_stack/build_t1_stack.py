#!/usr/bin/env python3
"""
T1 stack — export the printable parts (STL / DXF) and the renders.  No slicing, no printing.

    python3 build_t1_stack.py            # everything
    python3 build_t1_stack.py --no-stl   # renders only

Printed parts are exported with the manifold backend; any "not 2-manifold" / CGAL warning fails the run.
"""
from __future__ import annotations
import argparse, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCAD = HERE / "make_t1_stack.scad"
DECK = HERE / "stack_on_deck.scad"
OSC = "/opt/homebrew/bin/openscad"
PARTS = ["ladder_L", "ladder_R", "hub_cradle", "vplate_bracket", "cable_bar", "dog", "uusb_hood", "imu_plate"]
VIEWS = {   # name: (file, defines, camera, projection, size)
    "stack_iso":        (SCAD, {"part": '"assembly"'}, "10,20,75,60,0,-138,1000", "p", (2000, 1500)),
    "stack_exploded":   (SCAD, {"part": '"exploded"', "explode": "1"}, "10,20,90,62,0,-132,1500", "p", (2000, 1500)),
    "stack_io_face":    (SCAD, {"part": '"io"'}, "-12,560,86,-12,0,86", "o", (2000, 1500)),
    "stack_swap":       (SCAD, {"part": '"swap"', "pull": "75"}, "10,40,80,62,0,-140,1050", "p", (2000, 1500)),
    "stack_on_E_deck":  (DECK, {"rev": '"C"'}, "203,139,120,58,0,-30,1250", "p", (2000, 1400)),
}


def run(args):
    r = subprocess.run([OSC, *args], capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if re.search(r"^WARNING:|^ERROR:|not 2-manifold|Assertion", l)
           and "Ignoring unknown module" not in l]
    if r.returncode or bad:
        raise SystemExit("openscad: " + " ".join(args[-3:]) + "\n" + "\n".join(bad or r.stderr.splitlines()[-15:]))
    return r.stderr


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--no-stl", action="store_true"); a = ap.parse_args()
    out = run(["-o", "/dev/null", "--export-format=echo", str(SCAD)])
    for l in out.splitlines():
        if l.startswith("ECHO"):
            print(" ", l[6:].strip('"'))
    if not a.no_stl:
        (HERE / "stl").mkdir(exist_ok=True)
        for p in PARTS:
            f = HERE / "stl" / f"{p}{'_pa12cf' if p == 'imu_plate' else ''}.stl"
            run(["--backend=manifold", "-D", f'part="{p}"', "-o", str(f), str(SCAD)])
            print(f"  STL  {f.relative_to(HERE)}  {f.stat().st_size // 1024} KB")
        f = HERE / "stl" / "imu_plate_al3.dxf"
        run(["-D", 'part="imu_plate_2d"', "-o", str(f), str(SCAD)])
        print(f"  DXF  {f.relative_to(HERE)}  (6061-T6 3 mm, waterjet/laser or hand-drilled from a 1:1 print)")
    (HERE / "renders").mkdir(exist_ok=True)
    for name, (src, defs, cam, proj, size) in VIEWS.items():
        args = ["--colorscheme=Tomorrow", f"--camera={cam}", f"--projection={proj}", f"--imgsize={size[0]},{size[1]}"]
        for k, v in defs.items():
            args += ["-D", f"{k}={v}"]
        f = HERE / "renders" / f"{name}.png"
        run(args + ["-o", str(f), str(src)])
        print(f"  PNG  {f.relative_to(HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
