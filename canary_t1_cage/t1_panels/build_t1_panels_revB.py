#!/usr/bin/env python3
"""T1 panels — LOWER (CO) panel rev B: STL exports (manifold backend, print-oriented, face down) + renders + volume/mass.
No slicing here (see README rev B: one half sliced the house way).  Fails on any OpenSCAD WARNING / ERROR / assertion."""
from __future__ import annotations
import re, subprocess, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
SCAD = HERE / "make_t1_panels_revB.scad"; CAGE = HERE / "asbuilt_cage.scad"   # as-built frame, photo 39 (supersedes panels_on_cage_revB.scad)
OSC = "/opt/homebrew/bin/openscad"; FILL = 0.85; RHO = {"ASA": 1.07, "PLA": 1.24}; H_CM3 = 0.074   # real slice ratio (rev A lower C)
PARTS = {"lower_revB_half": "half", "lower_revB_half_mirror": "half_mirror", "lower_revB_cassette": "cassette", "lower_revB_louver_plain": "louver_plain",
         "lower_revB_accents": "accents", "lower_revB_splice": "splice"}
VIEWS = {   # full manifold render (--render) so the mirrored half shades correctly
    "lower_revB_front":    (SCAD, {"view": '"front"'}, "152.4,73,0,0,0,0,420", "o", (2000, 1000)),
    "lower_revB_back_seam": (SCAD, {"view": '"back"'}, "152.4,73,-60,180,0,0,560", "p", (2000, 1300)),
    "lower_revB_exploded": (SCAD, {"view": '"exploded"'}, "152.4,73,20,58,0,-18,560", "p", (2000, 1300)),
    "panels_on_cage_revB": (CAGE, {"bay": '"lowerbay"'}, "860,1000,420,222,140,105", "p", (2000, 1500)),   # rear 3/4: CO panel on the back
    "front_pair_front":   (CAGE, {"bay": '"pair"'}, "222,-820,125,222,0,115", "p", (2000, 1400)),
    "front_pair_front34": (CAGE, {"bay": '"pair"'}, "-330,-660,400,222,140,110", "p", (2000, 1400)),
    "lower_revB_front_4ts_hooks": (SCAD, {"view": '"front"', "fix": '"4ts_hooks"'}, "152.4,73,0,0,0,0,420", "o", (2000, 1000)),
    "upper_revB_front_lowerbay":   (CAGE, {"bay": '"lowerbay"'}, "222,-760,130,222,0,118", "p", (2000, 1300)),
    "upper_revB_front34_lowerbay": (CAGE, {"bay": '"lowerbay"'}, "-330,-640,380,222,140,105", "p", (2000, 1400)),
    "upper_revB_front_upperbay":   (CAGE, {"bay": '"upperbay"'}, "222,-760,150,222,0,130", "p", (2000, 1300)),
    "upper_revB_front34_upperbay": (CAGE, {"bay": '"upperbay"'}, "-330,-640,420,222,140,130", "p", (2000, 1400)),
}
UPARTS = {f"upper_revB_{pl}_{n}": (pl, part) for pl in ("lowerbay", "upperbay")
          for n, part in (("half", "u_half"), ("badge", "u_badge"), ("accents", "u_accents"), ("splice", "u_splice"))}
def run(args):
    r = subprocess.run([OSC, *args], capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if re.search(r"^WARNING:|^ERROR:|not 2-manifold|Assertion", l)]
    if r.returncode or bad:
        raise SystemExit("openscad " + " ".join(args[-4:]) + "\n" + "\n".join(bad or r.stderr.splitlines()[-12:]))
    return r.stderr
def vol_bbox(p):
    v = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", p.read_text()), float)
    t = v.reshape(-1, 3, 3)
    return abs(np.einsum("ij,ij->i", t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6) / 1000, v.max(0) - v.min(0)
def main():
    for l in run(["-D", 'part="accents"', "-o", "/tmp/_revb.stl", str(SCAD)]).splitlines():
        if l.startswith("ECHO"): print("  " + l[7:].strip('"'))
    print("\n  %-26s %8s %18s %7s %7s %6s" % ("part", "CAD cm3", "print bbox mm", "ASA g", "PLA g", "h"))
    tot = 0.0
    for name, part in PARTS.items():
        f = HERE / "stl" / f"{name}.stl"
        run(["--backend=manifold", "-D", f'part="{part}"', "-o", str(f), str(SCAD)])
        v, bb = vol_bbox(f)
        if part not in ("half_mirror", "cassette"): tot += v * (2 if part == "half" else 1)   # default build: plain louver (cassette optional)
        print("  %-26s %8.1f %18s %7.0f %7.0f %6.1f" % (name, v, "x".join("%.0f" % b for b in bb), v * FILL * RHO["ASA"], v * FILL * RHO["PLA"], v * H_CM3))
    print("  %-26s %8.1f %18s %7.0f %7.0f %6.1f   (DEFAULT: 2 halves + plain louver + accents + splice; class estimate)" % ("TOTAL panel", tot, "", tot * FILL * RHO["ASA"], tot * FILL * RHO["PLA"], tot * H_CM3))
    for pl in ("lowerbay", "upperbay"):
        for l in run(["-D", 'panel="upper"', "-D", f'placement="{pl}"', "-D", 'part="u_accents"', "-o", "/tmp/_revbu.stl", str(SCAD)]).splitlines():
            if l.startswith("ECHO"): print("  " + l[7:].strip('"'))
    utot = {"lowerbay": 0.0, "upperbay": 0.0}
    for name, (pl, part) in UPARTS.items():
        f = HERE / "stl" / f"{name}.stl"
        run(["--backend=manifold", "-D", 'panel="upper"', "-D", f'placement="{pl}"', "-D", f'part="{part}"', "-o", str(f), str(SCAD)])
        v, bb = vol_bbox(f); utot[pl] += v * (2 if part == "u_half" else 1)
        print("  %-34s %8.1f %18s %7.0f %7.0f %6.1f" % (name, v, "x".join("%.0f" % b for b in bb), v * FILL * RHO["ASA"], v * FILL * RHO["PLA"], v * H_CM3))
    for pl, v in utot.items():
        print("  %-34s %8.1f %18s %7.0f %7.0f %6.1f   (2 halves + badge + accents + splice)" % (f"TOTAL upper {pl}", v, "", v * FILL * RHO["ASA"], v * FILL * RHO["PLA"], v * H_CM3))
    for name, (src, defs, cam, proj, size) in VIEWS.items():
        args = ["--render", "--backend=manifold", "--colorscheme=Tomorrow", f"--camera={cam}", f"--projection={proj}", f"--imgsize={size[0]},{size[1]}"]
        for k, v in defs.items(): args += ["-D", f"{k}={v}"]
        run(args + ["-o", str(HERE / "renders" / f"{name}.png"), str(src)]); print(f"  PNG  renders/{name}.png")
if __name__ == "__main__":
    sys.exit(main())
