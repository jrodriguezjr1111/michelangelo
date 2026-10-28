#!/usr/bin/env python3
"""Build the seat-rail bench fixture family (PROVISIONAL photo profile, 2026-10-28):
STLs, ray-cast checks on the exported meshes, previews, plate STLs, then PLA
slices through the house pipeline (plus4_print.py slice --check).

    python3 build_seat_rail_fixture.py            # everything
    python3 build_seat_rail_fixture.py --no-slice # geometry + checks + previews only
    python3 build_seat_rail_fixture.py --no-renders

Outputs in this directory:
  rail_seg1_node.stl          segment 1 (rev E base on its clamp deck), print orientation (plate down)
  rail_seg2_digiducer.stl     segment 2 (concept-B pair: sidecar deck + rev E deck)
  rail_gauge.stl              N417ER go/no-go caliper gauge v2
  rail_clamp_all100.stl       straddle clamp (deck 100 + 4 jaws) modelled in place — assembly renders
  rail_clamp_all48.stl        same, 48 deck (Digiducer sidecar)
  rail_clamp_print100.stl     the clamp in PRINT pose (deck top-face down, jaws on their outer faces)
  rail_clamp_print48.stl
  plate_fixture_set.stl       seg 1 + seg 2 + gauge arranged for the bed
  plate_clamps.stl            both clamp print sets on one plate
  plate_fitcheck_parts.stl    vib01e_base.stl + digiducer_sidecar_pla.stl (the fit-check parts, own plate)
  preview_*.png, profile_provisional.svg
  gcode/*.gcode               slices (git-ignored, regenerable)

The clamp jaw stations and the rev E / sidecar band stations are COPIED into
the instance files; this script re-derives them from the source models and
refuses to build if the copies drift.  Rail PROFILE numbers are never copied:
the lib and the clamp include ../digiducer_mount/rail_interface.scad.

NEVER sends anything to the printer.
"""
import argparse, re, struct, subprocess, sys
from pathlib import Path
import numpy as np

HERE   = Path(__file__).resolve().parent
REPO   = HERE.parent
PLUS4  = REPO / "plus4_print.py"
GCODE  = HERE / "gcode"
BED    = 305.0
ENVELOPE = 280.0                 # plus4_print.py check: any printing move past X/Y 280 is flagged (conservative vs the 305 bed)
BRIM   = 5.0
PLA_RHO = 1.24
PROC_OV = ["sparse_infill_density=30%", "wall_loops=4", "bottom_shell_layers=4", "top_shell_layers=5"]
BOTTOM_SHELL_CAP = 6             # vib01 warp postmortem 2026-08-19
assert int(next(v for v in PROC_OV if v.startswith("bottom_shell_layers")).split("=")[1]) <= BOTTOM_SHELL_CAP

SEGS  = {"rail_seg1_node": HERE / "rail_seg1_node.scad", "rail_seg2_digiducer": HERE / "rail_seg2_digiducer.scad"}
CLAMP = HERE / "make_rail_straddle_clamp.scad"
FIT_PARTS = {"vib01e_base": REPO / "vib01_node/vib01e_base.stl",
             "digiducer_sidecar_pla": REPO / "digiducer_mount/digiducer_sidecar_pla.stl"}


# ----------------------------------------------------------------- helpers
def openscad(scad, args, timeout=600, allow_empty=False):
    r = subprocess.run(["openscad", *args, str(scad)], capture_output=True, text=True, timeout=timeout)
    out = r.stdout + r.stderr
    bad = "ERROR" in out or ("Assert" in out and "failed" in out) or (r.returncode and not allow_empty)
    if bad:
        print(out[-3000:]); raise SystemExit(f"openscad failed: {scad.name} {' '.join(map(str, args))}")
    return out


def echoes(out):
    return [ln[6:].strip().strip('"') for ln in out.splitlines() if ln.startswith("ECHO:")]


def load_stl(path):
    data = path.read_bytes()
    if data[:5] == b"solid" and b"facet" in data[:400]:
        v = np.array([[float(t) for t in ln.split()[1:4]] for ln in data.decode().splitlines()
                      if ln.strip().startswith("vertex")])
    else:
        n = struct.unpack("<I", data[80:84])[0]
        rec = np.frombuffer(data[84:84 + n * 50], dtype=np.dtype([("n", "<3f4"), ("v", "<9f4"), ("a", "<u2")]))
        v = rec["v"].reshape(-1, 3).astype(float)
    return v.reshape(-1, 3, 3)


def save_stl(path, tri):
    n = len(tri)
    normals = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(normals, axis=1); ln[ln == 0] = 1; normals /= ln[:, None]
    rec = np.zeros(n, dtype=np.dtype([("n", "<3f4"), ("v", "<9f4"), ("a", "<u2")]))
    rec["n"] = normals; rec["v"] = tri.reshape(n, 9)
    path.write_bytes(b"seat_rail_fixture plate".ljust(80, b"\0") + struct.pack("<I", n) + rec.tobytes())


def stl_volume(tri):
    return float(abs(np.einsum("ij,ij->i", tri[:, 0], np.cross(tri[:, 1], tri[:, 2])).sum() / 6.0))


def bbox(tri):
    v = tri.reshape(-1, 3); return v.min(0), v.max(0)


def ray_z_intervals(tri, x, y):
    """Material z-intervals along a vertical ray at (x, y): Möller–Trumbore, dir -Z, from above."""
    o = np.array([x, y, 1000.0]); d = np.array([0, 0, -1.0])
    v0, v1, v2 = tri[:, 0], tri[:, 1], tri[:, 2]
    e1, e2 = v1 - v0, v2 - v0
    p = np.cross(d, e2); det = np.einsum("ij,ij->i", e1, p)
    ok = np.abs(det) > 1e-12
    inv = np.zeros_like(det); inv[ok] = 1.0 / det[ok]
    tv = o - v0
    u = np.einsum("ij,ij->i", tv, p) * inv
    q = np.cross(tv, e1)
    w = np.einsum("j,ij->i", d, q) * inv
    tt = np.einsum("ij,ij->i", e2, q) * inv
    hit = ok & (u >= -1e-9) & (w >= -1e-9) & (u + w <= 1 + 1e-9) & (tt > 0)
    zs = np.sort(np.unique(np.round(1000.0 - tt[hit], 3)))[::-1]
    if len(zs) % 2: zs = zs[1:]
    return [(float(zs[i + 1]), float(zs[i])) for i in range(0, len(zs), 2)][::-1]


def scad_list(txt, name):
    m = re.search(rf"(?m)^\s*{name}\s*=\s*\[([^\]]*)\]", txt)
    return [float(t) for t in m.group(1).split(",")] if m else None


def scad_num(txt, name):
    m = re.search(rf"(?m)(?:^|;)\s*{name}\s*=\s*([-\d.]+)\s*;", txt); return float(m.group(1)) if m else None


def close(a, b, tol=1e-6):
    return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


# ----------------------------------------------------------- source checks
def check_copies():
    """Instance files copy the clamp jaw stations and the parts' band stations; re-derive both."""
    revE = (REPO / "vib01_node/make_vib01_revE.scad").read_text()
    node_tun = scad_list(revE, "tun_x")
    r = subprocess.run(["openscad", "-D", 'material="pla"', "-D", 'part="none"', "-o", str(GCODE / "_sc.stl"),
                        str(REPO / "digiducer_mount/make_digiducer_sidecar.scad")], capture_output=True, text=True, timeout=300)
    sc_out = r.stdout + r.stderr
    dg_tun = [float(t) for t in re.search(r"bands at x=\[([\d., ]+)\]", sc_out).group(1).split(",")]
    node_gap = scad_num((REPO / "digiducer_mount/make_digiducer_sidecar.scad").read_text(), "node_gap")
    jaws = {}
    for L in (100, 48):
        o = openscad(CLAMP, ["-D", f"deck_L={L}", "-D", 'part="none"', "-o", str(GCODE / "_cl.stl")], allow_empty=True)
        m = re.search(r"JAWS: 4 x ([\d.]+) long at x \[([\d., ]+)\]", o)
        jaws[L] = (float(m.group(1)), [float(t) for t in m.group(2).split(",")])
    for name, scad in SEGS.items():
        txt = scad.read_text()
        for key, (L, jl_key) in {"jaw_x": (100, "jaw_L"), "dg_jaw_x": (48, "dg_jaw_L")}.items():
            jx = scad_list(txt, key)
            if jx is None: continue
            jl = scad_num(txt, jl_key)
            if not close(jx, jaws[L][1]) or jl != jaws[L][0]:
                raise SystemExit(f"{name}: {key}={jx}/{jl_key}={jl} != clamp deck_L={L} jaws {jaws[L]}")
        n = scad_list(txt, "node_tun")
        if n is not None and not close(n, node_tun): raise SystemExit(f"{name}: node_tun {n} != make_vib01_revE.scad tun_x {node_tun}")
        d = scad_list(txt, "dg_tun")
        if d is not None and not close(d, dg_tun): raise SystemExit(f"{name}: dg_tun {d} != sidecar bands {dg_tun}")
        g = scad_num(txt, "node_gap")
        if g is not None and g != node_gap: raise SystemExit(f"{name}: node_gap {g} != sidecar node_gap {node_gap}")
    print(f"  copies OK: clamp jaws {jaws}; rev E tun_x {node_tun}; sidecar bands {dg_tun}, node_gap {node_gap}")
    for f in ("_sc.stl", "_cl.stl"): (GCODE / f).unlink(missing_ok=True)


# ------------------------------------------------------------ verification
def verify_segment(name, tri, log):
    """Ray-cast the exported mesh against the model's own echoes (photo profile)."""
    e = " ".join(log)
    z = re.search(r"Z: plate 0\.\.([\d.]+) \| flange plate \.\.([\d.]+) \(= profile z 0\) \| lip underside ([\d.]+) \| crown ([\d.]+) \| head ([\d.]+) wide, web ([\d.]+), undercut ([\d.]+) @ ([\d.]+) deg \| flange plate ([\d.]+) wide", e)
    plate_t, z_fl1, z_lip, z_crown, head_w, web_w, undercut, lip_ang, flange_w = map(float, z.groups())
    plate_w = float(re.search(r"plate [\d.]+ x ([\d.]+) x", e).group(1)); yc = plate_w / 2
    bolts = re.search(r"at \[x, y from CL\] \[(.*?)\] \(mid-span", e).group(1)
    bolts = [[float(a), float(b)] for a, b in re.findall(r"\[([-\d.]+), ([-\d.]+)\]", bolts)]
    bolt_hh = float(re.search(r"FLANGE BOLTS \(hex [\d.]+ AF x ([\d.]+)\)", e).group(1))
    setback = float(re.search(r"head bar starts at x ([\d.]+)", e).group(1))
    rail_L = float(re.search(r"rail ([\d.]+) long", e).group(1))
    bad = []

    def expect(label, x, y, want, tol=0.05):
        iv = ray_z_intervals(tri, x, y)
        ok = len(iv) == len(want) and all(abs(a - c) <= tol and abs(b - d) <= tol for (a, b), (c, d) in zip(iv, want))
        print(f"    {label:46s} ({x:6.1f},{y:5.1f}) -> {iv}  {'OK' if ok else '*** want ' + str(want)}")
        if not ok: bad.append((label, x, y, iv, want))

    print(f"  {name}: ray-cast (z intervals of material from the bed)")
    xs = [setback + 20, rail_L / 2, rail_L - 20]
    r = head_w / 2  # crown radius = w/2 in the profile
    import math
    for x in xs:
        if any(abs(x - b[0]) < 8 for b in bolts): x += 12
        expect("crown on the CL", x, yc, [(0, z_crown)])
        expect("flange plate beyond the head (+Y)", x, yc + head_w / 2 + 6, [(0, z_fl1)])
        expect("flange plate beyond the head (-Y)", x, yc - head_w / 2 - 6, [(0, z_fl1)])
        # undercut: at y = web/2 + 2 the lip underside is (undercut - 2) * tan(angle) below the lip edge; crown top from the circle
        yu = web_w / 2 + 2
        z_under = z_lip - (head_w / 2 - yu) * math.tan(math.radians(lip_ang))
        z_top = (z_crown - r) + math.sqrt(max(r * r - yu * yu, 0))
        expect("undercut gap under the lip (+Y)", x, yc + yu, [(0, z_fl1), (z_under, z_top)], tol=0.1)
        expect("undercut gap under the lip (-Y)", x, yc - yu, [(0, z_fl1), (z_under, z_top)], tol=0.1)
    expect("web only in the head set-back", setback / 2, yc, [(0, z_lip)])
    for b in bolts:
        expect("flange bolt head top", b[0], yc + b[1], [(0, z_fl1 + bolt_hh)])
    expect("plate lip (clamp lip, no engraving)", rail_L / 2, 7.5, [(0, plate_t)])
    if bad: raise SystemExit(f"RAY-CAST FAIL {name}: {bad}")
    print(f"  {name}: crown z {z_crown}, flange plate z {z_fl1}, undercut open, bolt heads z {z_fl1 + bolt_hh}, set-back web-only: PASS")


def verify_clamp(tri, log):
    """The printed clamp set: deck top (bed face) flat, channel + pad depths, counterbores, jaw lip wedge."""
    e = " ".join(log)
    z_br = float(re.search(r"bridge underside z ([\d.]+)", e).group(1)); z_deck = float(re.search(r"deck top z ([\d.]+)", e).group(1))
    pad = float(re.search(r"crown PAD ([\d.]+) proud", e).group(1)); deck_W = float(re.search(r"deck ([\d.]+) wide", e).group(1))
    ch = float(re.search(r"CHANNEL: half-width ([\d.]+)", e).group(1))
    deck_t = z_deck - z_br
    print("  clamp print set (deck top-face down): ray-cast")
    bad = []
    def expect(label, x, y, want, tol=0.05):
        iv = ray_z_intervals(tri, x, y)
        ok = len(iv) == len(want) and all(abs(a - c) <= tol and abs(b - d) <= tol for (a, b), (c, d) in zip(iv, want))
        print(f"    {label:46s} ({x:6.1f},{y:5.1f}) -> {iv}  {'OK' if ok else '*** want ' + str(want)}")
        if not ok: bad.append((label, x, y, iv, want))
    expect("deck slab (outboard of the channel)", 50, 20, [(0, deck_t)])
    expect("deck crown pad on the CL", 50, 0, [(0, deck_t + pad)])
    expect("deck over the channel, off the pad", 50, 6, [(0, deck_t)])
    if bad: raise SystemExit(f"RAY-CAST FAIL clamp: {bad}")
    print(f"  clamp: deck {deck_t} thick, pad {pad} proud on the CL, channel ±{ch}: PASS")


# ------------------------------------------------------------------ plates
def place(tri, dx, dy):
    t = tri.copy(); t[:, :, 0] += dx; t[:, :, 1] += dy; return t


def build_plates(meshes):
    gap = 2 * BRIM + 3
    out = {}
    s1, s2, g = meshes["rail_seg1_node"], meshes["rail_seg2_digiducer"], meshes["rail_gauge"]
    lo1, hi1 = bbox(s1); lo2, hi2 = bbox(s2); log, hig = bbox(g)
    y2 = (hi1[1] - lo1[1]) + gap; y3 = y2 + (hi2[1] - lo2[1]) + gap
    out["plate_fixture_set"] = np.concatenate([place(s1, -lo1[0], -lo1[1]), place(s2, -lo2[0], y2 - lo2[1]), place(g, -log[0], y3 - log[1])])
    c1, c2 = meshes["rail_clamp_print100"], meshes["rail_clamp_print48"]
    loc1, hic1 = bbox(c1); loc2, hic2 = bbox(c2)
    out["plate_clamps"] = np.concatenate([place(c1, -loc1[0], -loc1[1]), place(c2, -loc2[0], (hic1[1] - loc1[1]) + gap - loc2[1])])
    fb, dg = meshes["vib01e_base"], meshes["digiducer_sidecar_pla"]
    lob, hib = bbox(fb); lod, hid = bbox(dg)
    out["plate_fitcheck_parts"] = np.concatenate([place(fb, -lob[0], -lob[1]), place(dg, (hib[0] - lob[0]) + gap - lod[0], -lod[1])])
    for name, tri in out.items():
        lo, hi = bbox(tri); ext = hi - lo
        fit = ext[0] + 2 * BRIM <= ENVELOPE and ext[1] + 2 * BRIM <= ENVELOPE
        print(f"  {name:22s} footprint {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f} (+{BRIM} brim) -> check envelope {ENVELOPE:.0f}: {'FITS' if fit else '*** DOES NOT FIT ***'}")
        if not fit: raise SystemExit(f"{name} does not fit the envelope")
        save_stl(HERE / f"{name}.stl", tri)
    return out


# ------------------------------------------------------------------- slice
def slice_one(stl, label, maxspan=0.0):
    out = GCODE / (stl.stem + "_PLA.gcode")
    ov = list(PROC_OV) + ([f"max_bridge_length={int(maxspan) + 5}"] if maxspan > 0 else [])
    cmd = [sys.executable, str(PLUS4), "slice", str(stl), "--material", "pla", "--brim", str(BRIM), "--check", "--out", str(out),
           *sum([["--set", o] for o in ov], [])]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd=str(REPO))
    txt_out = r.stdout + r.stderr
    if r.returncode != 0 or not out.exists():
        print(txt_out[-3000:]); raise SystemExit(f"slice failed: {stl.name}")
    g = out.read_text(errors="ignore")
    tm = re.search(r"; estimated printing time \(normal mode\) = (.+)", g)
    fg = re.search(r"; filament used \[g\] = ([\d.]+)", g)
    fv = re.search(r"; filament used \[cm3\] = ([\d.]+)", g)
    head = g[:g.find(";LAYER_CHANGE")]
    m190 = re.findall(r"^M190 S(\d+)", head, re.M); m109 = re.findall(r"^M109 S(\d+)", head, re.M)
    m104 = sorted(set(re.findall(r"^M104 S(\d+)", head, re.M))); m140 = sorted(set(re.findall(r"^M140 S(\d+)", head, re.M)))
    maxz = re.search(r"; max_z_height: ([\d.]+)", g)
    cm3 = float(fv.group(1)) if fv else 0.0
    grams = float(fg.group(1)) if fg and float(fg.group(1)) > 0 else cm3 * PLA_RHO   # Bambu PLA profile has filament_density 0
    issues = [ln.strip(" │") for ln in txt_out.splitlines() if ln.startswith("│") and ("exceeds" in ln or "expected" in ln)]
    known_fp = [i for i in issues if "max Y=290" in i]       # end-gcode park move (G0 Y290 after UNLOAD_FILAMENT); same on vib01c_set.gcode (printed OK)
    real = [i for i in issues if i not in known_fp]
    res = dict(label=label, gcode=out, time=tm.group(1).strip() if tm else "?", g=grams, cm3=cm3,
               preamble=f"G28 / M190 S{m190[0] if m190 else '?'} / M109 S{m109[0] if m109 else '?'}", m104=m104, m140=m140,
               maxz=maxz.group(1) if maxz else "?", issues=real, known_fp=known_fp)
    print(f"\n{label}  ->  {out.name}")
    print(f"  time {res['time']}   filament {cm3:.1f} cm3 = {grams:.0f} g PLA (1.24 g/cm3)   max z {res['maxz']}" + (f"   max_bridge_length {int(maxspan)+5}" if maxspan else ""))
    print(f"  preamble {res['preamble']}   startup M104={m104} M140={m140}")
    for i in known_fp: print(f"  check (known false positive, end-gcode park): {i}")
    for i in real: print(f"  check ISSUE: {i}")
    ok = bool(m190) and bool(m109) and m140 == [m190[0]] and m104 == [m109[0]] and not real
    print(f"  [{'PREAMBLE + CHECK OK' if ok else '*** CHECK FAILED ***'}]")
    if not ok: raise SystemExit(f"slice check failed: {out.name}")
    return res


# ---------------------------------------------------------- profile SVG
def profile_svg(log):
    """Dimensioned cross-section of the PROVISIONAL profile with the clamp, every number from the model echoes."""
    e = " ".join(log)
    z = re.search(r"Z: plate 0\.\.([\d.]+) \| flange plate \.\.([\d.]+) \(= profile z 0\) \| lip underside ([\d.]+) \| crown ([\d.]+) \| head ([\d.]+) wide, web ([\d.]+), undercut ([\d.]+) @ ([\d.]+) deg \| flange plate ([\d.]+) wide", e)
    plate_t, z_fl1, z_lip, z_crown, head_w, web_w, undercut, lip_ang, flange_w = map(float, z.groups())
    plate_w = float(re.search(r"plate [\d.]+ x ([\d.]+) x", e).group(1)); yc = plate_w / 2
    import math
    S = 5.0; ox, oy = 60.0, 230.0
    X = lambda y: ox + y * S; Y = lambda zz: oy - zz * S
    def poly(pts, fill="#cfd8e3", dash=""): return f'<polygon points="{" ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in pts)}" fill="{fill}" stroke="#223" stroke-width="1.2" {dash}/>'
    def dim(x1, y1, x2, y2, label, off=0, vert=False):
        if vert:
            xx = x1 + off
            return (f'<line x1="{xx}" y1="{y1}" x2="{xx}" y2="{y2}" stroke="#b00" stroke-width="0.8"/>'
                    f'<text x="{xx+3}" y="{(y1+y2)/2+3}" font-size="10" fill="#b00">{label}</text>')
        yy = y1 + off
        return (f'<line x1="{x1}" y1="{yy}" x2="{x2}" y2="{yy}" stroke="#b00" stroke-width="0.8"/>'
                f'<text x="{(x1+x2)/2}" y="{yy-3}" font-size="10" fill="#b00" text-anchor="middle">{label}</text>')
    hw, ww = head_w / 2, web_w / 2; r = hw; zc = z_crown - r
    lipdrop = undercut * math.tan(math.radians(lip_ang))
    # rail section: web, lips, crown (semicircle approximated)
    arc = [(yc + r * math.cos(math.radians(a)), zc + r * math.sin(math.radians(a))) for a in range(0, 181, 10)]
    rail = [(yc + ww, z_fl1), (yc + ww, z_lip - lipdrop), (yc + hw, z_lip), (yc + hw, zc)] + arc + [(yc - hw, zc), (yc - hw, z_lip), (yc - ww, z_lip - lipdrop), (yc - ww, z_fl1)]
    g = ['<g>',
         poly([(0, 0), (plate_w, 0), (plate_w, plate_t), (0, plate_t)], "#e8e8e8"),                                   # fixture base plate
         poly([(yc - flange_w/2, plate_t), (yc + flange_w/2, plate_t), (yc + flange_w/2, z_fl1), (yc - flange_w/2, z_fl1)], "#d9cfae"),
         poly(rail, "#b8bcc2"),
         # clamp: deck (56 wide, 8 thick, bridge 1 over the crown, pad on the CL) + jaws (9..28, lip to 6)
         poly([(yc-28, z_crown+1), (yc+28, z_crown+1), (yc+28, z_crown+9), (yc-28, z_crown+9)], "#a9b4c2", 'stroke-dasharray="4,2"'),
         poly([(yc-3, z_crown), (yc+3, z_crown), (yc+3, z_crown+1), (yc-3, z_crown+1)], "#a9b4c2"),
         ]
    for s in (-1, 1):
        lip_tip_z = z_lip - (hw - (ww + 2)) * math.tan(math.radians(lip_ang)) - 0.3
        jaw = [(yc + s*(ww+2), z_fl1+1), (yc + s*28, z_fl1+1), (yc + s*28, z_crown+0.5), (yc + s*9, z_crown+0.5), (yc + s*9, z_lip - 0.3 + (9-hw)*math.tan(math.radians(lip_ang))), (yc + s*hw, z_lip-0.3), (yc + s*(ww+2), lip_tip_z)]
        g.append(poly(jaw, "#8fa3b8", 'stroke-dasharray="4,2"'))
    g += [dim(X(yc-hw), Y(z_crown), X(yc+hw), Y(z_crown), f"head {head_w:g} ±3", off=-16),
          dim(X(yc-ww), Y(z_fl1), X(yc+ww), Y(z_fl1), f"web {web_w:g} ±3", off=40),
          dim(X(yc-flange_w/2), Y(0), X(yc+flange_w/2), Y(0), f"flange plate {flange_w:g} ±8 wide, {z_fl1-plate_t:g} ±1 thick", off=22),
          dim(X(yc+hw)+70, Y(z_crown), 0, Y(z_fl1), f"head {z_crown-z_fl1:g} ±4 above the plate", vert=True),
          dim(X(yc+hw)+70, Y(z_crown), 0, Y(z_lip), f"head thick {z_crown-z_lip:g} ±3 (lip underside)", off=90, vert=True),
          dim(X(yc-hw)-30, Y(z_lip), 0, Y(z_fl1), f"undercut {undercut:g} ±2 @ {lip_ang:g}° (45 assumed)", off=-150, vert=True),
          f'<text x="{ox}" y="{oy+70}" font-size="11" fill="#223">PROVISIONAL rail section from the 2026-10-28 photo (rail_interface.scad "photo_2026_10_28"), 5 px/mm, fixture base plate in grey, clamp deck + jaws dashed.</text>',
          f'<text x="{ox}" y="{oy+86}" font-size="11" fill="#223">Clamp load path: jaw lip UP into the undercut ↔ crown pad DOWN. Flange plate and carpet out of the path. Every ± is a caliper item (README §5).</text>',
          "</g>"]
    W = int(X(plate_w) + 200); H = int(oy + 100)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica">'
           f'<rect width="100%" height="100%" fill="#fff"/>' + "\n".join(g) + "</svg>")
    (HERE / "profile_provisional.svg").write_text(svg)


# -------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-slice", action="store_true"); ap.add_argument("--no-renders", action="store_true")
    a = ap.parse_args()
    GCODE.mkdir(exist_ok=True)

    print("== source-copy checks")
    check_copies()

    print("\n== STL export")
    meshes, logs = {}, {}
    for name, scad in SEGS.items():
        out = HERE / f"{name}.stl"
        o = openscad(scad, ["-D", 'part="seg"', "-o", str(out)])
        logs[name] = echoes(o); meshes[name] = load_stl(out)
        lo, hi = bbox(meshes[name]); v = stl_volume(meshes[name]) / 1000
        print(f"  {name:22s} {len(meshes[name]):6d} tris  {hi[0]-lo[0]:.1f} x {hi[1]-lo[1]:.1f} x {hi[2]-lo[2]:.1f}  {v:6.1f} cm3 solid = {v*PLA_RHO:.0f} g PLA solid")
    openscad(SEGS["rail_seg1_node"], ["-D", 'part="gauge"', "-o", str(HERE / "rail_gauge.stl")])
    meshes["rail_gauge"] = load_stl(HERE / "rail_gauge.stl")
    lo, hi = bbox(meshes["rail_gauge"]); print(f"  {'rail_gauge':22s} {hi[0]-lo[0]:.1f} x {hi[1]-lo[1]:.1f} x {hi[2]-lo[2]:.1f}")
    clamp_log = {}
    for L in (100, 48):
        for part in ("all", "print"):
            out = HERE / f"rail_clamp_{part}{L}.stl"
            o = openscad(CLAMP, ["-D", f"deck_L={L}", "-D", f'part="{part}"', "-o", str(out)])
            meshes[out.stem] = load_stl(out)
            if part == "print": clamp_log[L] = echoes(o)
            lo, hi = bbox(meshes[out.stem]); v = stl_volume(meshes[out.stem]) / 1000
            print(f"  {out.stem:22s} {hi[0]-lo[0]:.1f} x {hi[1]-lo[1]:.1f} x {hi[2]-lo[2]:.1f}  {v:6.1f} cm3 solid = {v*1.07:.0f} g ASA solid")
    for name, p in FIT_PARTS.items():
        meshes[name] = load_stl(p)

    print("\n== model echoes")
    for name in SEGS:
        print(f"  [{name}]")
        for ln in logs[name]: print("    " + ln)
    print("  [rail_clamp deck 100]")
    for ln in clamp_log[100]: print("    " + ln)

    print("\n== ray-cast verification on the exported meshes")
    for name in SEGS: verify_segment(name, meshes[name], logs[name])
    verify_clamp(meshes["rail_clamp_print100"], clamp_log[100])
    maxspan_clamp = float(re.search(r"MAXSPAN=([\d.]+)", " ".join(clamp_log[100])).group(1))

    print("\n== plates")
    build_plates(meshes)

    if not a.no_renders:
        print("\n== renders")
        R = [(SEGS["rail_seg1_node"], "seg", "100,42,12,50,0,25,520", "p", "preview_seg1.png"),
             (SEGS["rail_seg1_node"], "assembly", "100,42,20,55,0,35,520", "p", "preview_seg1_assembly.png"),
             (SEGS["rail_seg2_digiducer"], "seg", "100,42,12,50,0,25,520", "p", "preview_seg2.png"),
             (SEGS["rail_seg2_digiducer"], "assembly", "100,42,20,55,0,35,540", "p", "preview_seg2_assembly.png"),
             (SEGS["rail_seg1_node"], "seg", "100,42,11,90,0,90,130", "o", "preview_profile_end.png"),
             (SEGS["rail_seg1_node"], "gauge", "65,20,5,45,0,20,330", "p", "preview_gauge.png"),
             (CLAMP, "assembly", "50,0,15,60,0,30,330", "p", "preview_clamp_assembly.png"),
             (CLAMP, "all", "50,0,10,90,0,90,110", "o", "preview_clamp_end.png"),
             (CLAMP, "print", "70,40,8,50,0,20,360", "p", "preview_clamp_print.png")]
        for scad, part, cam, proj, png in R:
            openscad(scad, ["-D", f'part="{part}"', "--camera=" + cam, "--projection=" + proj, "--imgsize=1600,1000",
                            "--colorscheme=Tomorrow", "-o", str(HERE / png)])
            print(f"  {png}")
        profile_svg(logs["rail_seg1_node"]); print("  profile_provisional.svg")

    if a.no_slice: return
    print("\n================ PLA SLICES via plus4_print.py (nothing is sent) ================")
    results = [slice_one(HERE / "rail_seg1_node.stl", "SEG 1 NODE alone"),
               slice_one(HERE / "rail_seg2_digiducer.stl", "SEG 2 DG-B alone"),
               slice_one(HERE / "rail_gauge.stl", "gauge v2 alone"),
               slice_one(HERE / "plate_fixture_set.stl", "PLATE: seg 1 + seg 2 + gauge"),
               slice_one(HERE / "plate_clamps.stl", "PLATE: straddle clamps (deck 100 + 48, 8 jaws) — PLA bench; ASA for ground runs", maxspan_clamp)]
    print("\n== summary")
    for r in results:
        print(f"  {r['label']:78s} {r['time']:>12s}  {r['cm3']:6.1f} cm3  {r['g']:4.0f} g  {r['gcode'].name}")
    print(f"\ngcode in {GCODE} (git-ignored) — NOT sent to the printer.")


if __name__ == "__main__":
    main()
