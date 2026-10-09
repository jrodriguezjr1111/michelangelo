#!/usr/bin/env python3
"""FlyCatcher window unit — STL exports (manifold backend, print-oriented) + renders + volume/mass.  No slicing here."""
import re, subprocess
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; SCAD = HERE / "make_fc_window.scad"; OSC = "/opt/homebrew/bin/openscad"
RHO = {"ASA": 1.07, "PETG": 1.27, "PLA": 1.24}; FILL = 0.85
PARTS = {"fc_base": "ASA", "fc_lid": "ASA", "fc_hood": "ASA", "fc_adapter": "ASA", "fc_lens": "PETG", "fc_label": "ASA"}
VIEWS = {"fc_iso_closed": ({"view": '"iso"'}, "-330,-520,260,0,15,40", "p"),
         "fc_exploded": ({"view": '"exploded"'}, "-400,-600,330,0,10,40", "p"),
         "fc_on_suction": ({"view": '"glass"'}, "-460,-380,300,0,45,30", "p"),
         "fc_antenna_side": ({"view": '"side"'}, "420,45,40,0,45,40", "o")}
EXTRA_G = {"board": 48, "antennas (EST, 2 x 25)": 50, "suction cup (EST)": 180, "hardware": 15}
def run(a):
    r = subprocess.run([OSC, *a], capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if re.search(r"^WARNING:|^ERROR:|Assertion", l)]
    if r.returncode or bad: raise SystemExit(" ".join(a[-3:]) + "\n" + "\n".join(bad or r.stderr.splitlines()[-10:]))
    return r.stderr
def vol_bbox(p):
    v = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", p.read_text()), float); t = v.reshape(-1, 3, 3)
    return abs(np.einsum("ij,ij->i", t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6) / 1000, v.max(0) - v.min(0)
for l in run(["-o", "/tmp/_fc.stl", str(SCAD)]).splitlines():
    if l.startswith("ECHO") and "MAXSPAN" not in l: print("  " + l[7:].strip('"'))
print("\n  %-11s %7s %16s %5s %7s %7s" % ("part", "CAD cm3", "print bbox mm", "mat", "g", "PLA g"))
tot = 0
for n, mat in PARTS.items():
    f = HERE / "stl" / f"{n}.stl"
    span = re.search(r"MAXSPAN=([\d.]+)", run(["--backend=manifold", "-D", f'part="{n[3:]}"', "-o", str(f), str(SCAD)])).group(1)
    v, bb = vol_bbox(f); g = v * FILL * RHO[mat]; tot += g
    print("  %-11s %7.1f %16s %5s %7.0f %7.0f   MAXSPAN %s" % (n, v, "x".join("%.0f" % b for b in bb), mat, g, v * FILL * RHO["PLA"], span))
print("  printed parts %.0f g + %s = UNIT %.0f g (EST)" % (tot, " + ".join(f"{k} {v}" for k, v in EXTRA_G.items()), tot + sum(EXTRA_G.values())))
for n, (d, cam, proj) in VIEWS.items():
    a = ["--render", "--backend=manifold", "--colorscheme=Tomorrow", f"--camera={cam}", f"--projection={proj}", "--imgsize=2000,1400"]
    if proj == "o": a.append("--viewall")
    for k, v in d.items(): a += ["-D", f"{k}={v}"]
    run(a + ["-o", str(HERE / "renders" / f"{n}.png"), str(SCAD)]); print(f"  PNG  renders/{n}.png")
