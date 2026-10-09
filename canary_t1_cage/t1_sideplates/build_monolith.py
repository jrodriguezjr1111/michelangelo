#!/usr/bin/env python3
"""Monolith wordmark-side plate (t1_sideplates, format="monolith"): STLs for both variants + letters/accents + splices, renders, volumes.
Run make_wordmark_layout.py first (it writes wm_layout_*.scad).  Times = CAD cm3 x 0.106 h (rate from the house slice of sp_r2_wordmark_L)."""
import re, subprocess
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; SCAD = HERE / "make_t1_sideplates.scad"; OSC = "/opt/homebrew/bin/openscad"
RATE = 0.106; FILL = 0.85; RHO = {"ASA": 1.07, "PLA": 1.24}
M = {"format": '"monolith"', "layout": '"twoline"'}
PARTS = {f"mono_{v}_{h}": {**M, "variant": f'"{v}"', "part": '"mono"', "half": f'"{h}"'} for v in ("stencil", "applique") for h in ("L", "R")}
PARTS.update({"mono_splices": {**M, "part": '"mono_splice"'}, "mono_splines": {**M, "part": '"mono_spline"'},
              "mono_stencil_chevron_yellow": {**M, "part": '"mono_chevron"'},
              "mono_applique_letters_yellow_plate": {**M, "variant": '"applique"', "part": '"letters_plate"'}})
VIEWS = {"mono_pair_straight": ({**M, "view": '"mono_pair"'}, "500,-1450,420,500,0,150"),
         "mono_pair_34": ({**M, "view": '"mono_pair"'}, "-500,-1150,820,520,140,140"),
         "mono_stencil_straight": ({**M, "variant": '"stencil"', "view": '"cage_wm"'}, "222,-1000,330,222,0,150"),
         "mono_applique_straight": ({**M, "variant": '"applique"', "view": '"cage_wm"'}, "222,-1000,330,222,0,150"),
         "mono_oneline_stencil_straight": ({"format": '"monolith"', "layout": '"oneline"', "variant": '"stencil"', "view": '"cage_wm"'}, "222,-1000,330,222,0,150"),
         "mono_applique_exploded": ({**M, "variant": '"applique"', "view": '"mono_exploded"'}, "0,-520,420,152,140,0")}
def run(a):
    r = subprocess.run([OSC, *a], capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if re.search(r"^WARNING:|^ERROR:|Assertion", l)]
    if r.returncode or bad: raise SystemExit(" ".join(a[-3:]) + "\n" + "\n".join(bad or r.stderr.splitlines()[-10:]))
    return r.stderr
def vol_bbox(p):
    v = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", p.read_text()), float); t = v.reshape(-1, 3, 3)
    return abs(np.einsum("ij,ij->i", t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6) / 1000, v.max(0) - v.min(0)
a = []; [a.extend(["-D", f"{k}={v}"]) for k, v in M.items()]
for l in run(a + ["-o", "/tmp/_m.stl", str(SCAD)]).splitlines():
    if "MONOLITH" in l: print("  " + l[7:].strip('"'))
print("\n  %-36s %7s %16s %6s %6s %6s" % ("part", "cm3", "print bbox mm", "ASA g", "PLA g", "h EST"))
V = {}
for n, d in PARTS.items():
    f = HERE / "stl" / f"{n}.stl"; a = ["--backend=manifold"]
    for k, v in d.items(): a += ["-D", f"{k}={v}"]
    run(a + ["-o", str(f), str(SCAD)]); v, bb = vol_bbox(f); V[n] = v
    print("  %-36s %7.1f %16s %6.0f %6.0f %6.1f" % (n, v, "x".join("%.0f" % b for b in bb), v * FILL * RHO["ASA"], v * FILL * RHO["PLA"], v * RATE))
for var, extra in (("stencil", ["mono_stencil_chevron_yellow", "mono_stencil_chevron_yellow"]), ("applique", ["mono_applique_letters_yellow_plate"])):
    keys = [f"mono_{var}_L", f"mono_{var}_R", "mono_splices", "mono_splines"] + extra
    tv = sum(V[k] for k in keys)
    print(f"  SET {var}: {tv:.0f} cm3 = {tv * FILL * RHO['ASA']:.0f} g ASA / {tv * FILL * RHO['PLA']:.0f} g PLA, ~{tv * RATE:.0f} h (EST)")
for n, (d, cam) in VIEWS.items():
    a = ["--render", "--backend=manifold", "--colorscheme=Tomorrow", f"--camera={cam}", "--projection=p", "--imgsize=2200,1300"]
    for k, v in d.items(): a += ["-D", f"{k}={v}"]
    run(a + ["-o", str(HERE / "renders" / f"{n}.png"), str(SCAD)]); print(f"  PNG  renders/{n}.png")
