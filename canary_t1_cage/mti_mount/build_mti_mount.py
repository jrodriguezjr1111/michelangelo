#!/usr/bin/env python3
"""MTi mount — STL exports (manifold backend, print-oriented) + renders + volume/mass.  No slicing here."""
import re, subprocess, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; SCAD = HERE / "make_mti_mount.scad"; OSC = "/opt/homebrew/bin/openscad"
RHO = {"PA12-CF": 1.06, "ASA": 1.07, "PLA": 1.24}; FILL = 0.85
PARTS = {"mti_bridge_mount": {"variant": '"bridge"', "part": '"mount"'},
         "mti_saddle_mount": {"variant": '"saddle"', "part": '"mount"'},
         "mti_stop": {"part": '"stop"'}, "mti_usb_hood": {"part": '"hood"'}}
VIEWS = {"mti_bridge_iso": (SCAD, {"variant": '"bridge"', "view": '"iso"'}, "0,0,10,55,0,-35,380"),
         "mti_saddle_iso": (SCAD, {"variant": '"saddle"', "view": '"iso"'}, "0,0,10,55,0,-35,330"),
         "mti_bridge_exploded": (SCAD, {"variant": '"bridge"', "view": '"exploded"'}, "0,0,40,62,0,-35,480"),
         "mti_bridge_flat_span80_iso": (SCAD, {"variant": '"bridge"', "SPAN": "80", "view": '"iso"'}, "0,0,10,55,0,-35,330"),
         "mti_on_cage_backface": (HERE / "mti_on_cage.scad", {}, "40,40,300,222,250,72")}
def run(a):
    r = subprocess.run([OSC, *a], capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if re.search(r"^WARNING:|^ERROR:|Assertion", l)]
    if r.returncode or bad: raise SystemExit(" ".join(a[-3:]) + "\n" + "\n".join(bad or r.stderr.splitlines()[-10:]))
    return r.stderr
def vol_bbox(p):
    v = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", p.read_text()), float); t = v.reshape(-1, 3, 3)
    return abs(np.einsum("ij,ij->i", t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6) / 1000, v.max(0) - v.min(0)
for v in ("bridge", "saddle"):
    for l in run(["-D", f'variant="{v}"', "-o", "/tmp/_mti.stl", str(SCAD)]).splitlines():
        if l.startswith("ECHO"): print("  " + l[7:].strip('"'))
print("\n  %-22s %8s %16s %9s %7s" % ("part", "CAD cm3", "bbox mm", "PA12-CF g", "PLA g"))
for n, d in PARTS.items():
    f = HERE / "stl" / f"{n}.stl"; a = ["--backend=manifold"]
    for k, v in d.items(): a += ["-D", f"{k}={v}"]
    run(a + ["-o", str(f), str(SCAD)]); v, bb = vol_bbox(f)
    print("  %-22s %8.1f %16s %9.0f %7.0f" % (n, v, "x".join("%.0f" % b for b in bb), v * FILL * RHO["PA12-CF"], v * FILL * RHO["PLA"]))
for n, (src, d, cam) in VIEWS.items():
    a = ["--render", "--backend=manifold", "--colorscheme=Tomorrow", f"--camera={cam}", "--projection=p", "--imgsize=2000,1400"]
    for k, v in d.items(): a += ["-D", f"{k}={v}"]
    run(a + ["-o", str(HERE / "renders" / f"{n}.png"), str(src)]); print(f"  PNG  renders/{n}.png")
