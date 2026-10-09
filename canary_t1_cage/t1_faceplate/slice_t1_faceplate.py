#!/usr/bin/env python3
"""t1_faceplate — PLA FIT-CHECK slice of one plate (default: fp_84_lte), OrcaSlicer
CLI direct via cw_mes/qidi_xplus4_brim.json, same harness as ../slice_coupon.py.
The PRINT_START preamble is forced and then verified LITERALLY in the gcode; the
two vib01 rev D guards apply (R6.3):
  GUARD 1  bottom_shell_layers <= 6
  GUARD 2  max_bridge_length derived from the model's own MAXSPAN echo
gcode_check.py runs on the result.  Output goes to --out (default: a scratch
dir), NOT to the printer.  Owner authorises every print.

    python3 slice_t1_faceplate.py --out /path/to/scratch [--plate fp_84_lte]
"""
import argparse, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ORCA = "/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer"
OPENSCAD = "/opt/homebrew/bin/openscad"
SYS = Path.home() / "Library/Application Support/OrcaSlicer/system/Qidi"
MACH = SYS / "machine/Qidi X-Plus 4 0.4 nozzle.json"
HERE = Path(__file__).resolve().parent
PROC = HERE.parent.parent / "cw_mes/qidi_xplus4_brim.json"
GCODE_CHECK = HERE.parent.parent / "gcode_check.py"
sys.path.insert(0, str(HERE))
from build_t1_faceplate import PLATES, COMMON, scad_def   # the same plate definitions as the build

PLA = dict(base=SYS / "filament/Qidi Generic PLA+ @Qidi X-Plus 4 0.4 nozzle.json", bed=60, hotend=220, chamber=0)
BOTTOM_SHELL_CAP = 6
# face-down flat plate: 4 walls (hex webs = 4 lines), 4 bottom / 4 top shells, 40 % gyroid core in the 4 mm skin,
# outer brim 6 (110 mm contraction length in PLA on a 60 C bed)
PROCESS = dict(wall_loops="4", bottom_shell_layers="4", top_shell_layers="4", sparse_infill_density="40%",
               sparse_infill_pattern="gyroid", brim_type="outer_only", brim_width="6", brim_object_gap="0.1")
assert int(PROCESS["bottom_shell_layers"]) <= BOTTOM_SHELL_CAP, "GUARD 1 (warp) — read vib01_node/README_revD.md"


def model_max_span(name, work):
    p = PLATES[name]
    defs = [x for k, v in {**COMMON, **p}.items() for x in ("-D", scad_def(k, v))]
    r = subprocess.run([OPENSCAD] + defs + ["-D", 'part="plate"', "--backend=manifold", "-o", str(work / "_span.stl"),
                       str(HERE / "make_t1_faceplate.scad")], capture_output=True, text=True, timeout=300)
    m = re.search(r"MAXSPAN=([\d.]+)", r.stdout + r.stderr)
    if not m:
        raise RuntimeError("model did not echo MAXSPAN — refusing to slice blind (GUARD 2)")
    return float(m.group(1))


def patched(path, upd, prefix, work):
    d = json.loads(Path(path).read_text()); d.update(upd)
    p = Path(tempfile.mktemp(suffix=".json", prefix=prefix, dir=work)); p.write_text(json.dumps(d)); return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", default="fp_84_lte", choices=sorted(PLATES))
    ap.add_argument("--out", required=True, help="output dir for the gcode (scratch — never the printer)")
    a = ap.parse_args()
    out_dir = Path(a.out); out_dir.mkdir(parents=True, exist_ok=True)
    work = out_dir / "_slice_work"; work.mkdir(exist_ok=True)
    stl = HERE / f"{a.plate}.stl"
    if not stl.exists():
        raise SystemExit(f"{stl} missing — run build_t1_faceplate.py first")

    span = model_max_span(a.plate, work)
    bridge = int(span) + 5
    assert bridge >= span
    print(f"model MAXSPAN = {span} mm  ->  max_bridge_length = {bridge}")

    fil = patched(PLA["base"], {
        "nozzle_temperature": [str(PLA["hotend"])], "nozzle_temperature_initial_layer": [str(PLA["hotend"])],
        "chamber_temperature": [str(PLA["chamber"])],
        **{f"{p}_temp{s}": [str(PLA["bed"])] for p in ("cool_plate", "eng_plate", "hot_plate", "textured_plate")
           for s in ("", "_initial_layer")}}, "fil_PLA_", work)
    proc = patched(PROC, PROCESS | {"max_bridge_length": str(bridge), "dont_filter_internal_bridges": "force"},
                   f"proc_{a.plate}_", work)
    for g in work.glob("*.gcode"):
        g.unlink()
    cmd = [ORCA, "--load-settings", f"{MACH};{proc}", "--load-filaments", str(fil),
           "--orient", "0", "--arrange", "1", "--slice", "0", "--outputdir", str(work), str(stl)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    gs = list(work.glob("*.gcode"))
    if r.returncode != 0 or not gs:
        print(f"FAIL rc={r.returncode}\n{(r.stderr or r.stdout)[-1500:]}"); return 1
    out = out_dir / f"{a.plate}_PLA.gcode"; shutil.move(str(gs[0]), out)
    txt = out.read_text(errors="ignore")
    ps = re.search(r"^PRINT_START .*$", txt, re.M)
    m104 = sorted(set(re.findall(r"^M104 S(\d+)", txt, re.M)))
    m140 = sorted(set(re.findall(r"^M140 S(\d+)", txt, re.M)))
    tm = re.search(r"; estimated printing time.*?= *(.+)", txt)
    fv = re.search(r"; filament used \[cm3\] *= *([\d.]+)", txt)
    mb = re.search(r"; max_bridge_length *= *(\d+)", txt)
    bs = re.search(r"; bottom_shell_layers *= *(\d+)", txt)
    sup = re.search(r"; enable_support *= *(\d+)", txt)
    good = (ps and f"BED={PLA['bed']}" in ps.group(0) and f"HOTEND={PLA['hotend']}" in ps.group(0)
            and set(m104) == {"0", str(PLA['hotend'])} and set(m140) == {"0", str(PLA['bed'])}
            and mb and int(mb.group(1)) == bridge and bs and int(bs.group(1)) <= BOTTOM_SHELL_CAP)
    print(f"\n{out}  [{'PREAMBLE + GUARDS OK' if good else '*** MISMATCH ***'}]")
    print(f"  {ps.group(0) if ps else 'NO PRINT_START'}")
    print(f"  M104={m104} M140={m140} max_bridge_length={mb.group(1) if mb else '?'} "
          f"bottom_shell_layers={bs.group(1) if bs else '?'} enable_support={sup.group(1) if sup else '?'}")
    vol = float(fv.group(1)) if fv else 0.0
    print(f"  time={tm.group(1) if tm else '?'}  vol={vol:.2f} cm3  mass~{vol * 1.24:.0f} g PLA (1.24 g/cm3)")
    chk = subprocess.run([sys.executable, str(GCODE_CHECK), str(out)], capture_output=True, text=True)
    print("\n--- gcode_check.py ---\n" + chk.stdout[-2500:] + chk.stderr[-500:])
    return 0 if (good and chk.returncode == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
