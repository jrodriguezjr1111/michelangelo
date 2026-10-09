#!/usr/bin/env python3
"""Row-2 CUTOUT (t1_sideplates format="cutout"): STLs, renders, volumes.  Run make_cutout_layout.py first."""
import re, subprocess
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; SCAD = HERE / "make_t1_sideplates.scad"; OSC = "/opt/homebrew/bin/openscad"
RATE = 0.106; FILL = 0.85; RHO = {"ASA": 1.07, "PLA": 1.24}
C = {"format": '"cutout"'}
PARTS = {}
for lt in ("condensed", "native"):
    PARTS[f"co_{lt}_front_45"] = {**C, "lettering": f'"{lt}"', "part": '"co_front"'}
    PARTS[f"co_{lt}_backer_yellow_45"] = {**C, "lettering": f'"{lt}"', "part": '"co_backer"'}
PARTS["co_brackets_x4"] = {**C, "part": '"co_brackets"'}
for r in (1, 3):
    for h in ("L", "R"):
        PARTS[f"co_row{r}_wordmark_{h}"] = {**C, "row": str(r), "half": f'"{h}"', "part": '"co_row"'}
VIEWS = {"co_cage_straight": ({**C, "view": '"cage_wm"'}, "222,-1000,330,222,0,150"),
         "co_cage_34": ({**C, "view": '"cage34"'}, "-430,-720,560,222,140,140"),
         "co_cage_straight_native": ({**C, "lettering": '"native"', "view": '"cage_wm"'}, "222,-1000,330,222,0,150"),
         "co_exploded": ({**C, "view": '"co_exploded"'}, "-160,-470,380,222,20,175"),
         "co_inlay_closeup": ({**C, "view": '"co_detail"'}, "160,-150,230,262,0,172")}
def run(a):
    r = subprocess.run([OSC, *a], capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if re.search(r"^WARNING:|^ERROR:|Assertion", l)]
    if r.returncode or bad: raise SystemExit(" ".join(a[-3:]) + "\n" + "\n".join(bad or r.stderr.splitlines()[-10:]))
    return r.stderr
def vol_bbox(p):
    v = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", p.read_text()), float); t = v.reshape(-1, 3, 3)
    return abs(np.einsum("ij,ij->i", t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6) / 1000, v.max(0) - v.min(0)
for lt in ("condensed", "native"):
    a = []; [a.extend(["-D", f"{k}={v}"]) for k, v in {**C, "lettering": f'"{lt}"'}.items()]
    for l in run(a + ["-o", "/tmp/_c.stl", str(SCAD)]).splitlines():
        if "CUTOUT" in l: print("  " + l[7:].strip('"'))
print("\n  %-30s %7s %16s %6s %6s %6s" % ("part", "cm3", "print bbox mm", "ASA g", "PLA g", "h EST"))
V = {}
for n, d in PARTS.items():
    f = HERE / "stl" / f"{n}.stl"; a = ["--backend=manifold"]
    for k, v in d.items(): a += ["-D", f"{k}={v}"]
    run(a + ["-o", str(f), str(SCAD)]); v, bb = vol_bbox(f); V[n] = v
    print("  %-30s %7.1f %16s %6.0f %6.0f %6.1f" % (n, v, "x".join("%.0f" % b for b in bb), v * FILL * RHO["ASA"], v * FILL * RHO["PLA"], v * RATE))
for lt in ("condensed", "native"):
    k = [f"co_{lt}_front_45", f"co_{lt}_backer_yellow_45", "co_brackets_x4"]
    tv = sum(V[x] for x in k)
    print(f"  SET row-2 cutout ({lt}): {tv:.0f} cm3 = {tv * FILL * RHO['ASA']:.0f} g ASA, ~{tv * RATE:.1f} h (EST)")
for n, (d, cam) in VIEWS.items():
    a = ["--render", "--backend=manifold", "--colorscheme=Tomorrow", f"--camera={cam}", "--projection=p", "--imgsize=2200,1300"]
    for k, v in d.items(): a += ["-D", f"{k}={v}"]
    run(a + ["-o", str(HERE / "renders" / f"{n}.png"), str(SCAD)]); print(f"  PNG  renders/{n}.png")
