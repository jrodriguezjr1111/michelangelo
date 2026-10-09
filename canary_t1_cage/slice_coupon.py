#!/usr/bin/env python3
"""Style coupon slicing — OrcaSlicer CLI direct via cw_mes/qidi_xplus4_brim.json.
Deliberately NOT plus4_print.py; the PRINT_START preamble is forced here and then
verified LITERALLY in the produced gcode.  Pattern: orin_tactical_case/slice_tactical.py.

Both vib01 rev D guards apply (vib01_node/README_revD.md):
  GUARD 1  bottom_shell_layers <= 6      (the 30-layer raft peeled off the bed)
  GUARD 2  max_bridge_length derived from the model's own MAXSPAN echo
           (spans over the limit are laid as infill into air — 2116 moves, silent)

Two plates: coupon_panel (black) and the two label plates (yellow filament).
Nothing is sent to the printer.
"""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ORCA = "/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer"
SYS = Path.home() / "Library/Application Support/OrcaSlicer/system/Qidi"
MACH = SYS / "machine/Qidi X-Plus 4 0.4 nozzle.json"
HERE = Path(__file__).resolve().parent
PROC = HERE.parent / "cw_mes/qidi_xplus4_brim.json"
SCAD = HERE / "make_style_coupon.scad"
WORK = HERE / "_slice_work"
WORK.mkdir(exist_ok=True)

PLA = dict(base=SYS / "filament/Qidi Generic PLA+ @Qidi X-Plus 4 0.4 nozzle.json",
           bed=60, hotend=220, chamber=0)
BOTTOM_SHELL_CAP = 6
BRIM = dict(brim_type="outer_only", brim_object_gap="0.1")
PLATES = {
    "coupon_panel": dict(stls=["coupon_panel.stl"], wall_loops="4", bottom_shell_layers="4",
                         top_shell_layers="5", sparse_infill_density="30%",
                         sparse_infill_pattern="gyroid", brim_width="6", **BRIM),
    "coupon_plates_yellow": dict(stls=["coupon_plate_yellow.stl", "coupon_plate_show_yellow.stl"],
                                 wall_loops="3", bottom_shell_layers="3", top_shell_layers="4",
                                 sparse_infill_density="100%", brim_width="3", **BRIM),
}
for n, ov in PLATES.items():
    assert int(ov["bottom_shell_layers"]) <= BOTTOM_SHELL_CAP, f"{n}: GUARD 1 (warp) — read the vib01 postmortem"


def model_max_span():
    r = subprocess.run(["openscad", "-D", 'part="none"', "-o", str(WORK / "_span.stl"), str(SCAD)],
                       capture_output=True, text=True, timeout=300)
    m = re.search(r"MAXSPAN=([\d.]+)", r.stdout + r.stderr)
    if not m:
        raise RuntimeError("model did not echo MAXSPAN — refusing to slice blind (GUARD 2)")
    return float(m.group(1))


MAX_SPAN = model_max_span()
BRIDGE_LIMIT = int(MAX_SPAN) + 5
assert BRIDGE_LIMIT >= MAX_SPAN
print(f"model MAXSPAN = {MAX_SPAN} mm  ->  max_bridge_length = {BRIDGE_LIMIT}")


def patched(path, upd, prefix):
    d = json.loads(Path(path).read_text()); d.update(upd)
    p = Path(tempfile.mktemp(suffix=".json", prefix=prefix, dir=WORK)); p.write_text(json.dumps(d)); return p


def main():
    fil = patched(PLA["base"], {
        "nozzle_temperature": [str(PLA["hotend"])], "nozzle_temperature_initial_layer": [str(PLA["hotend"])],
        "chamber_temperature": [str(PLA["chamber"])],
        **{f"{p}_temp{s}": [str(PLA["bed"])] for p in ("cool_plate", "eng_plate", "hot_plate", "textured_plate")
           for s in ("", "_initial_layer")}}, "fil_PLA_")
    ok_all = True
    for name, ov in PLATES.items():
        proc = patched(PROC, {k: v for k, v in ov.items() if k != "stls"} |
                       {"max_bridge_length": str(BRIDGE_LIMIT), "dont_filter_internal_bridges": "force"}, f"proc_{name}_")
        for g in WORK.glob("*.gcode"):
            g.unlink()
        cmd = [ORCA, "--load-settings", f"{MACH};{proc}", "--load-filaments", str(fil),
               "--orient", "0", "--arrange", "1", "--slice", "0", "--outputdir", str(WORK)] + \
              [str(HERE / s) for s in ov["stls"]]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        gs = list(WORK.glob("*.gcode"))
        if r.returncode != 0 or not gs:
            print(f"FAIL {name} rc={r.returncode}\n{(r.stderr or r.stdout)[-1500:]}"); ok_all = False; continue
        out = HERE / f"{name}_PLA.gcode"; shutil.move(str(gs[0]), out)
        txt = out.read_text(errors="ignore")
        ps = re.search(r"^PRINT_START .*$", txt, re.M)
        m104 = sorted(set(re.findall(r"^M104 S(\d+)", txt, re.M)))
        m140 = sorted(set(re.findall(r"^M140 S(\d+)", txt, re.M)))
        tm = re.search(r"; estimated printing time.*?= *(.+)", txt)
        fv = re.search(r"; filament used \[cm3\] *= *([\d.]+)", txt)
        fg = re.search(r"; filament used \[g\] *= *([\d.]+)", txt)
        mb = re.search(r"; max_bridge_length *= *(\d+)", txt)
        bs = re.search(r"; bottom_shell_layers *= *(\d+)", txt)
        good = (ps and f"BED={PLA['bed']}" in ps.group(0) and f"HOTEND={PLA['hotend']}" in ps.group(0)
                and set(m104) == {"0", str(PLA['hotend'])} and set(m140) == {"0", str(PLA['bed'])}  # S0 = end-gcode cool-down
                and mb and int(mb.group(1)) == BRIDGE_LIMIT and bs and int(bs.group(1)) <= BOTTOM_SHELL_CAP)
        ok_all &= bool(good)
        print(f"\n{out.name}  [{'PREAMBLE + GUARDS OK' if good else '*** MISMATCH ***'}]")
        print(f"  {ps.group(0) if ps else 'NO PRINT_START'}")
        print(f"  M104={m104} M140={m140} max_bridge_length={mb.group(1) if mb else '?'} "
              f"bottom_shell_layers={bs.group(1) if bs else '?'}")
        vol = float(fv.group(1)) if fv else 0.0
        print(f"  time={tm.group(1) if tm else '?'}  vol={vol:.2f} cm3  mass~{vol * 1.24:.0f} g PLA (profile reports 0 g; 1.24 g/cm3)")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
