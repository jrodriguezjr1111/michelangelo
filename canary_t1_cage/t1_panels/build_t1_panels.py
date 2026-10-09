#!/usr/bin/env python3
"""
T1 panels — export every printable part (STL, manifold backend, print-oriented) and the renders.

    python3 build_t1_panels.py            # STLs + renders + volume/mass/time table
    python3 build_t1_panels.py --no-stl

Fails on any OpenSCAD WARNING / ERROR / assertion.  No slicing here (see README: one PLA
fit-check slice via plus4_print.py); nothing is sent to the printer.
"""
from __future__ import annotations
import argparse, re, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
SCAD = HERE / "make_t1_panels.scad"
CAGE = HERE / "panels_on_cage.scad"
OSC = "/opt/homebrew/bin/openscad"
H_PER_CM3 = 37.85 / 359.39          # repo ratio (orin_tactical_case ASA): 0.105 h per sliced cm3
FILL = 0.85                         # sliced / CAD volume class (t1_params)
RHO = {"ASA": 1.07, "PLA": 1.24}

PARTS = [("upper", "body", s) for s in "LCR"] + [("lower", "body", s) for s in "LCR"] + \
        [("upper", "splice", "all"), ("lower", "splice", "all"), ("upper", "accents", "all"), ("lower", "accents", "all"),
         ("upper", "badge", "all"), ("lower", "louver", "all")]
VIEWS = {
    "upper_front":      (SCAD, {"panel": '"upper"', "view": '"front"'}, "200,65,0,0,0,0,540", "o", (2000, 700)),
    "lower_front":      (SCAD, {"panel": '"lower"', "view": '"front"'}, "200,65,0,0,0,0,540", "o", (2000, 700)),
    "seam_back_lower":  (SCAD, {"panel": '"lower"', "view": '"back_seg"'}, "170,65,-80,180,0,0,420", "p", (2000, 1100)),
    "accents_exploded_lower": (SCAD, {"panel": '"lower"', "view": '"exploded"'}, "200,65,20,58,0,-18,720", "p", (2000, 1200)),
    "accents_exploded_upper": (SCAD, {"panel": '"upper"', "view": '"exploded"'}, "200,65,20,58,0,-18,720", "p", (2000, 1200)),
    "panels_on_cage":   (CAGE, {"rev": '"C"'}, "-300,-800,520,203,139,105", "p", (2000, 1500)),
}


def run(args):
    r = subprocess.run([OSC, *args], capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if re.search(r"^WARNING:|^ERROR:|not 2-manifold|Assertion", l)]
    if r.returncode or bad:
        raise SystemExit("openscad " + " ".join(args[-4:]) + "\n" + "\n".join(bad or r.stderr.splitlines()[-12:]))
    return r.stderr


def stl_volume(p: Path) -> float:
    v = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", p.read_text()), float).reshape(-1, 3, 3)
    return abs(np.einsum("ij,ij->i", v[:, 0], np.cross(v[:, 1], v[:, 2])).sum() / 6) / 1000


def stl_bbox(p: Path):
    v = np.array(re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", p.read_text()), float)
    return v.max(0) - v.min(0)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--no-stl", action="store_true"); a = ap.parse_args()
    for pn in ("upper", "lower"):
        for l in run(["-D", f'panel="{pn}"', "-D", 'part="splice"', "-o", "/tmp/_t1p.stl", str(SCAD)]).splitlines():
            if l.startswith("ECHO"):
                print("  " + l[7:].strip('"'))
    if not a.no_stl:
        (HERE / "stl").mkdir(exist_ok=True)
        print("\n  %-28s %8s %20s %8s %8s %6s" % ("part", "CAD cm3", "print bbox mm", "ASA g", "PLA g", "h"))
        tot = {"upper": 0.0, "lower": 0.0}
        for pn, part, seg in PARTS:
            name = f"{pn}_{part}" + (f"_{seg}" if part == "body" else "")
            f = HERE / "stl" / f"{name}.stl"
            run(["--backend=manifold", "-D", f'panel="{pn}"', "-D", f'part="{part}"', "-D", f'segment="{seg}"', "-o", str(f), str(SCAD)])
            v = stl_volume(f); bb = stl_bbox(f); tot[pn] += v
            print("  %-28s %8.1f %20s %8.0f %8.0f %6.1f" % (name, v, "x".join("%.0f" % b for b in bb),
                  v * FILL * RHO["ASA"], v * FILL * RHO["PLA"], v * FILL * H_PER_CM3))
        for pn, v in tot.items():
            print("  %-28s %8.1f %20s %8.0f %8.0f %6.1f   (class estimate, not sliced)" % (f"TOTAL {pn}", v, "", v * FILL * RHO["ASA"],
                  v * FILL * RHO["PLA"], v * FILL * H_PER_CM3))
    (HERE / "renders").mkdir(exist_ok=True)
    for name, (src, defs, cam, proj, size) in VIEWS.items():
        args = ["--colorscheme=Tomorrow", f"--camera={cam}", f"--projection={proj}", f"--imgsize={size[0]},{size[1]}"]
        for k, v in defs.items():
            args += ["-D", f"{k}={v}"]
        f = HERE / "renders" / f"{name}.png"
        run(args + ["-o", str(f), str(src)])
        print(f"  PNG  renders/{f.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
