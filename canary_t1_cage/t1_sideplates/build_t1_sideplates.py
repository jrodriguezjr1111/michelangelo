#!/usr/bin/env python3
"""T1 side plates — STL exports (manifold, print-oriented: halves FACE DOWN) + renders + volumes.  No slicing here.
Print-time column = volume x the rate measured on the house slice of row 2 / wordmark / L (RATE_H_PER_CM3, EST for the rest)."""
import re, subprocess, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; SCAD = HERE / "make_t1_sideplates.scad"; OSC = "/opt/homebrew/bin/openscad"
RHO = {"ASA": 1.07, "PLA": 1.24}; FILL = 0.85
RATE_H_PER_CM3 = float(sys.argv[1]) if len(sys.argv) > 1 else 0.11
PARTS = {}
for side in ("wordmark", "plain"):
    for r in (1, 2, 3):
        for h in ("L", "R"):
            PARTS[f"sp_r{r}_{side}_{h}"] = {"side": f'"{side}"', "row": str(r), "half": f'"{h}"', "part": '"plate"'}
    PARTS[f"sp_r3_{side}_FULL45"] = {"side": f'"{side}"', "row": "3", "half": '"full"', "part": '"plate"'}
for r in (1, 2, 3):
    PARTS[f"sp_r{r}_splice"] = {"row": str(r), "part": '"splice"'}
    PARTS[f"sp_r{r}_spline"] = {"row": str(r), "part": '"spline"'}
    PARTS[f"sp_r{r}_chevron_yellow"] = {"row": str(r), "part": '"chevron"'}
VIEWS = {"sp_cage_wordmark_side": ({"view": '"cage_wm"'}, "222,-1050,260,222,0,150"),
         "sp_cage_plain_side": ({"view": '"cage_plain"'}, "222,1330,260,222,279,150"),
         "sp_cage_34": ({"view": '"cage34"'}, "-430,-720,560,222,140,140"),
         "sp_row2_exploded": ({"view": '"exploded"'}, "40,-330,520,152,173,0")}
def run(a):
    r = subprocess.run([OSC, *a], capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if re.search(r"^WARNING:|^ERROR:|Assertion", l)]
    if r.returncode or bad: raise SystemExit(" ".join(a[-3:]) + "\n" + "\n".join(bad or r.stderr.splitlines()[-10:]))
    return r.stderr
def vol_bbox(p):
    v = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", p.read_text()), float); t = v.reshape(-1, 3, 3)
    return abs(np.einsum("ij,ij->i", t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6) / 1000, v.max(0) - v.min(0)
for l in run(["-o", "/tmp/_sp.stl", str(SCAD)]).splitlines():
    if l.startswith("ECHO"): print("  " + l[7:].strip('"'))
print("\n  %-26s %7s %16s %6s %6s %7s" % ("part", "cm3", "print bbox mm", "ASA g", "PLA g", "h EST"))
tot = {"v": 0, "h": 0}
for n, d in PARTS.items():
    f = HERE / "stl" / f"{n}.stl"; a = ["--backend=manifold"]
    for k, v in d.items(): a += ["-D", f"{k}={v}"]
    run(a + ["-o", str(f), str(SCAD)]); v, bb = vol_bbox(f)
    h = v * RATE_H_PER_CM3
    if "FULL45" not in n:        # the build set = 12 halves + per-plate splice/spline (x2 sides) + chevrons (wordmark side, x2 ends)
        mult = 2 if any(k in n for k in ("splice", "spline", "chevron")) else 1
        tot["v"] += v * mult; tot["h"] += h * mult
    print("  %-26s %7.1f %16s %6.0f %6.0f %7.1f" % (n, v, "x".join("%.0f" % b for b in bb), v * FILL * RHO["ASA"], v * FILL * RHO["PLA"], h))
print("  BUILD SET (12 halves + 6 splice bars + 6 splines + 6 chevrons): %.0f cm3 = %.0f g ASA / %.0f g PLA, ~%.0f h (EST)"
      % (tot["v"], tot["v"] * FILL * RHO["ASA"], tot["v"] * FILL * RHO["PLA"], tot["h"]))
for n, (d, cam) in VIEWS.items():
    a = ["--render", "--backend=manifold", "--colorscheme=Tomorrow", f"--camera={cam}", "--projection=p", "--imgsize=2000,1300"]
    for k, v in d.items(): a += ["-D", f"{k}={v}"]
    run(a + ["-o", str(HERE / "renders" / f"{n}.png"), str(SCAD)]); print(f"  PNG  renders/{n}.png")
