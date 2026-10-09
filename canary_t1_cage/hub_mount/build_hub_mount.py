#!/usr/bin/env python3
"""UHR204 hub mount — STL exports (manifold backend, print-oriented) + renders + volume/mass.  No slicing here."""
import re, subprocess
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; SCAD = HERE / "make_hub_mount.scad"; OSC = "/opt/homebrew/bin/openscad"
RHO = {"PA12-CF": 1.06, "ASA": 1.07, "PLA": 1.24}; FILL = 0.85
PARTS = {"hub_dual_mount": {"variant": '"dual"', "part": '"mount"'},
         "hub_single_mount": {"variant": '"single"', "part": '"mount"'},
         "hub_comb": {"part": '"comb"'}}
VIEWS = {"hub_dual_iso": (SCAD, {"variant": '"dual"', "view": '"iso"'}, "-320,470,500,0,15,85"),
         "hub_dual_exploded": (SCAD, {"variant": '"dual"', "view": '"exploded"'}, "-420,660,640,0,60,110"),
         "hub_single_iso": (SCAD, {"variant": '"single"', "view": '"iso"'}, "-320,470,500,0,15,85"),
         "hub_on_cage_backface": (HERE / "hub_on_cage.scad", {}, "-60,-560,560,215,240,80")}
def run(a):
    r = subprocess.run([OSC, *a], capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if re.search(r"^WARNING:|^ERROR:|Assertion", l)]
    if r.returncode or bad: raise SystemExit(" ".join(a[-3:]) + "\n" + "\n".join(bad or r.stderr.splitlines()[-10:]))
    return r.stderr
def vol_bbox(p):
    v = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", p.read_text()), float); t = v.reshape(-1, 3, 3)
    return abs(np.einsum("ij,ij->i", t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6) / 1000, v.max(0) - v.min(0)
for v in ("dual", "single"):
    for l in run(["-D", f'variant="{v}"', "-o", "/tmp/_hub.stl", str(SCAD)]).splitlines():
        if l.startswith("ECHO"): print("  " + l[7:].strip('"'))
print("\n  %-18s %8s %16s %9s %6s %7s" % ("part", "CAD cm3", "print bbox mm", "PA12-CF g", "ASA g", "PLA g"))
for n, d in PARTS.items():
    f = HERE / "stl" / f"{n}.stl"; a = ["--backend=manifold"]
    for k, v in d.items(): a += ["-D", f"{k}={v}"]
    run(a + ["-o", str(f), str(SCAD)]); v, bb = vol_bbox(f)
    print("  %-18s %8.1f %16s %9.0f %6.0f %7.0f" % (n, v, "x".join("%.0f" % b for b in bb),
          v * FILL * RHO["PA12-CF"], v * FILL * RHO["ASA"], v * FILL * RHO["PLA"]))
for n, (src, d, cam) in VIEWS.items():
    a = ["--render", "--backend=manifold", "--colorscheme=Tomorrow", f"--camera={cam}", "--projection=p", "--imgsize=2000,1400"]
    for k, v in d.items(): a += ["-D", f"{k}={v}"]
    err = run(a + ["-o", str(HERE / "renders" / f"{n}.png"), str(src)])
    for l in err.splitlines():
        if l.startswith("ECHO") and "ON CAGE" in l: print("  " + l[7:].strip('"'))
    print(f"  PNG  renders/{n}.png")
