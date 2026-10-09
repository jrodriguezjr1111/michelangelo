#!/usr/bin/env python3
"""t1_faceplate — build the concept-D plate set: STLs (print orientation, face
down), the matching yellow label plates, and the renders (front / back / iso
per plate + the assembled frame views).  Reads the model's own echoes
(OPEN_CM2, MAXSPAN, bolts) and prints them as the build record.

    python3 build_t1_faceplate.py            # everything
    python3 build_t1_faceplate.py --no-png   # STLs only

Nothing here talks to the printer.
"""
import argparse, re, subprocess, sys
from pathlib import Path

OPENSCAD = "/opt/homebrew/bin/openscad"
HERE = Path(__file__).resolve().parent
RENDERS = HERE / "renders"
H_FRONT = 100          # concept D: DZ - 2E (t1_concepts.scad); mullion top = 120, bottom long top = 20

# name -> faceplate() arguments.  neighbour[] is as seen from OUTSIDE the box.
PLATES = {
    "fp_74_traffic": dict(w=74,  h=H_FRONT, neighbour=[0, 1, 0, 0], vent="hex",    vent_min_cm2=0,  label_txt="TRAFFIC"),
    "fp_84_lte":     dict(w=84,  h=H_FRONT, neighbour=[0, 1, 0, 1], vent="hex",    vent_min_cm2=0,  label_txt="LTE"),
    "fp_62_rtk":     dict(w=62,  h=H_FRONT, neighbour=[0, 0, 0, 1], vent="none",   vent_min_cm2=0,  label_txt="RTK"),
    "fp_160_exhaust": dict(w=160, h=H_FRONT, neighbour=[0, 1, 0, 0], vent="louver", vent_min_cm2=32, label_txt="EXHAUST"),
}
COMMON = dict(mount="bolt", sides=[0, 1, 1, 1], grip="top", label=True, mark=True)
# view -> camera (eye xyz, centre xyz) on the render wrapper (view coords: face toward +z, y up)
VIEWS = {"front": "0,-1,700,0,0,0", "back": "160,-260,-420,0,0,-6", "iso": "-200,-320,520,0,0,0"}
FRAME_VIEWS = {"assembled_front": "-380,-620,420,150,0,70", "assembled_rear": "620,560,380,150,0,70"}


def scad_def(k, v):
    if isinstance(v, bool):
        return f"{k}={'true' if v else 'false'}"
    if isinstance(v, str):
        return f'{k}="{v}"'
    if isinstance(v, list):
        return f"{k}=[{','.join(str(x) for x in v)}]"
    return f"{k}={v}"


def run(args, timeout=600):
    r = subprocess.run([OPENSCAD] + args, capture_output=True, text=True, timeout=timeout)
    out = r.stdout + r.stderr
    if r.returncode != 0 or "ERROR" in out or "assert" in out.lower() and "failed" in out.lower():
        print(out[-3000:])
        raise SystemExit(f"openscad failed: {' '.join(args)}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-png", action="store_true")
    a = ap.parse_args()
    RENDERS.mkdir(exist_ok=True)
    record = []
    for name, p in PLATES.items():
        defs = [x for k, v in {**COMMON, **p}.items() for x in ("-D", scad_def(k, v))]
        out = run(defs + ["-D", scad_def("name", name), "-D", 'part="plate"', "--backend=manifold",
                          "-o", str(HERE / f"{name}.stl"), str(HERE / "make_t1_faceplate.scad")])
        echo = re.search(r'ECHO: "(FACEPLATE .*?)"', out).group(1)
        span = float(re.search(r"MAXSPAN=([\d.]+)", out).group(1))
        open_cm2 = float(re.search(r"OPEN_CM2=([\d.]+)", echo).group(1))
        bolts = int(re.search(r"bolts=(\d+)", echo).group(1))
        outline = re.search(r"outline (\S+)", echo).group(1)
        record.append((name, outline, bolts, p["vent"], open_cm2, span))
        print(f"{name:16s} {echo}\n{'':16s} MAXSPAN={span}")
        run(defs + ["-D", 'part="label"', "--backend=manifold",
                    "-o", str(HERE / f"label_{p['label_txt'].lower()}.stl"), str(HERE / "make_t1_faceplate.scad")])
        if a.no_png:
            continue
        for view, cam in VIEWS.items():
            run(defs + ["-D", scad_def("name", name), f"--camera={cam}", "--projection=o", "--imgsize=1600,1200",
                        "--colorscheme=Cornfield", "-o", str(RENDERS / f"{name}_{view}.png"),
                        str(HERE / "t1_faceplate_render.scad")])
    if not a.no_png:
        for view, cam in FRAME_VIEWS.items():
            run([f"--camera={cam}", "--projection=p", "--imgsize=2000,1300", "--colorscheme=Cornfield",
                 "-o", str(RENDERS / f"{view}.png"), str(HERE / "t1_faceplate_on_frame.scad")])
    print("\nname             outline        bolts vent    open cm2  MAXSPAN")
    for r in record:
        print(f"{r[0]:16s} {r[1]:14s} {r[2]:5d} {r[3]:7s} {r[4]:8.1f}  {r[5]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
