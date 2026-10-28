#!/usr/bin/env python3
"""Build the seat-rail bench fixture family: STLs, ray-cast checks on the
exported meshes, previews, plate STLs, then PLA slices through the house
pipeline (plus4_print.py slice --check).

    python3 build_seat_rail_fixture.py            # everything
    python3 build_seat_rail_fixture.py --no-slice # geometry + checks + previews only
    python3 build_seat_rail_fixture.py --no-renders

Outputs in this directory:
  rail_seg1_node.stl          segment 1 (rev E Feather-stack base), print orientation (plate down)
  rail_seg2_digiducer.stl     segment 2 (concept-B pair: rev E base + Digiducer sidecar)
  rail_gauge.stl              N417ER go/no-go caliper gauge
  plate_fixture_set.stl       seg 1 + seg 2 + gauge, arranged for the 305 x 305 bed
  plate_fitcheck_parts.stl    vib01e_base.stl + digiducer_sidecar_pla.stl (the fit-check parts, own plate)
  preview_*.png               renders
  gcode/*.gcode               slices (git-ignored, regenerable)

The band stations are COPIED into the instance files from make_vib01_revE.scad
and make_digiducer_sidecar.scad; this script re-derives both from the source
models and refuses to build if the copies drift.  Rail PROFILE numbers are not
copied at all — the lib includes ../digiducer_mount/rail_interface.scad.

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
BRIM   = 5.0                      # house: cw_mes/qidi_xplus4_brim.json = outer brim 5
PLA_RHO = 1.24
PROC_OV = ["sparse_infill_density=30%", "wall_loops=4", "bottom_shell_layers=4", "top_shell_layers=5"]
BOTTOM_SHELL_CAP = 6              # vib01 warp postmortem 2026-08-19
assert int(next(v for v in PROC_OV if v.startswith("bottom_shell_layers")).split("=")[1]) <= BOTTOM_SHELL_CAP

SEGS = {"rail_seg1_node": HERE / "rail_seg1_node.scad", "rail_seg2_digiducer": HERE / "rail_seg2_digiducer.scad"}
FIT_PARTS = {"vib01e_base": REPO / "vib01_node/vib01e_base.stl",
             "digiducer_sidecar_pla": REPO / "digiducer_mount/digiducer_sidecar_pla.stl"}


# ----------------------------------------------------------------- helpers
def openscad(scad, args, timeout=600):
    r = subprocess.run(["openscad", *args, str(scad)], capture_output=True, text=True, timeout=timeout)
    out = r.stdout + r.stderr
    if r.returncode or "ERROR" in out or ("Assert" in out and "failed" in out):
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
    m = re.search(rf"(?m)^\s*{name}\s*=\s*([-\d.]+)\s*;", txt); return float(m.group(1)) if m else None


def close(a, b, tol=1e-6):
    return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


# ----------------------------------------------------------- source checks
def check_copies():
    """The instance files copy the parts' band stations; re-derive them from the source models."""
    revE = (REPO / "vib01_node/make_vib01_revE.scad").read_text()
    node_tun = scad_list(revE, "tun_x")
    r = subprocess.run(["openscad", "-D", 'material="pla"', "-D", 'part="none"', "-o", str(GCODE / "_sc.stl"),
                        str(REPO / "digiducer_mount/make_digiducer_sidecar.scad")], capture_output=True, text=True, timeout=300)
    sc_out = r.stdout + r.stderr          # part="none" exports nothing (non-zero exit is expected); we only want the echoes
    m = re.search(r"bands at x=\[([\d., ]+)\]", sc_out); dg_tun = [float(t) for t in m.group(1).split(",")]
    sc = (REPO / "digiducer_mount/make_digiducer_sidecar.scad").read_text()
    node_gap = scad_num(sc, "node_gap")
    for name, scad in SEGS.items():
        txt = scad.read_text()
        n = scad_list(txt, "node_tun")
        if n is not None and not close(n, node_tun): raise SystemExit(f"{name}: node_tun {n} != make_vib01_revE.scad tun_x {node_tun}")
        d = scad_list(txt, "dg_tun")
        if d is not None and not close(d, dg_tun): raise SystemExit(f"{name}: dg_tun {d} != sidecar bands {dg_tun}")
        g = scad_num(txt, "node_gap")
        if g is not None and g != node_gap: raise SystemExit(f"{name}: node_gap {g} != sidecar node_gap {node_gap}")
    print(f"  copies OK: rev E tun_x {node_tun}; sidecar bands {dg_tun}, node_gap {node_gap}")
    (GCODE / "_sc.stl").unlink(missing_ok=True)
    return node_tun, dg_tun


# ------------------------------------------------------------ verification
def verify_segment(name, tri, log):
    """Ray-cast the exported mesh against the model's own echoes."""
    e = " ".join(log)
    z = re.search(r"Z: plate 0\.\.([\d.]+) \| flange \.\.([\d.]+) \| body \.\.([\d.]+) = PAD PLANE \| head \.\.([\d.]+) \| band slot z ([\d.]+)\.\.([\d.]+)", e)
    plate_t, z_body0, z_bear, z_head, zs0, zs1 = map(float, z.groups())
    plate_w = float(re.search(r"plate [\d.]+ x ([\d.]+) x", e).group(1)); yc = plate_w / 2
    stations = [float(t) for t in re.search(r"BAND STATIONS x = \[([^\]]*)\]", e).group(1).split(",")]
    holes = [float(t) for t in re.search(r"x = \[([^\]]*)\] \(blind", e).group(1).split(",")]
    head_w = float(re.search(r"head ([\d.]+) x", e).group(1))
    hole_d = float(re.search(r"x Ø([\d.]+) at", e).group(1))
    bad = []

    def expect(label, x, y, want, tol=0.05):
        iv = ray_z_intervals(tri, x, y)
        ok = len(iv) == len(want) and all(abs(a - c) <= tol and abs(b - d) <= tol for (a, b), (c, d) in zip(iv, want))
        print(f"    {label:44s} ({x:6.1f},{y:5.1f}) -> {iv}  {'OK' if ok else '*** want ' + str(want)}")
        if not ok: bad.append((label, x, y, iv, want))

    print(f"  {name}: ray-cast (z intervals of material from the bed)")
    for s in stations:        # inside the body beside the hole line: plate+flange, then body above the slot crown
        expect("band slot crown, body line y=yc+15", s, yc + 15, [(0, z_body0), (zs1, z_bear)])
        expect("band slot, plate lip beyond the flange", s, 7.5, [(0, plate_t)])   # y 7.5: clear of the -Y label (y<5) and the flange step (y>=9.5)
        expect("band slot wall, 0.5 inside the slot edge", s + 8 - 0.5, yc + 15, [(0, z_body0), (zs0 + 0.9, z_bear)], tol=0.6)
    for h in holes:           # hole axis: nothing above the flange step
        expect("seat-stop hole axis", h, yc, [(0, z_body0)])
    slot_w = float(re.search(r"band slot z [\d.]+\.\.[\d.]+ \(([\d.]+) wide", e).group(1))
    mid = [(a + b) / 2 for a, b in zip(holes[:-1], holes[1:])]
    mid = [x for x in mid if all(abs(x - s) > slot_w / 2 + 1 for s in stations)]   # clear of every band slot
    for x in mid[:3]:         # head top between holes; pad plane outboard of the head
        expect("head top between holes", x, yc, [(0, z_head)])
        expect("pad plane outboard of the head (+Y pad)", x, yc + head_w / 2 + 4, [(0, z_bear)])
        expect("pad plane outboard of the head (-Y pad)", x, yc - head_w / 2 - 4, [(0, z_bear)])
    if bad: raise SystemExit(f"RAY-CAST FAIL {name}: {bad}")
    print(f"  {name}: slots open {zs0}..{zs1}, holes open to z {z_body0}, pad plane z {z_bear}, head z {z_head}: PASS")
    return dict(plate_t=plate_t, z_bear=z_bear, z_head=z_head, stations=stations, holes=holes, plate_w=plate_w)


# ------------------------------------------------------------------ plates
def place(tri, dx, dy):
    t = tri.copy(); t[:, :, 0] += dx; t[:, :, 1] += dy; return t


def build_plates(meshes):
    """Arrange on the bed, origin at (0,0), brims included in the fit check."""
    gap = 2 * BRIM + 3
    out = {}
    s1, s2, g = meshes["rail_seg1_node"], meshes["rail_seg2_digiducer"], meshes["rail_gauge"]
    lo1, hi1 = bbox(s1); lo2, hi2 = bbox(s2); log, hig = bbox(g)
    w1 = hi1[1] - lo1[1]; w2 = hi2[1] - lo2[1]
    y2 = w1 + gap
    y3 = y2 + w2 + gap
    parts_set = [place(s1, -lo1[0], -lo1[1]), place(s2, -lo2[0], y2 - lo2[1]), place(g, -log[0], y3 - log[1])]
    out["plate_fixture_set"] = np.concatenate(parts_set)
    # fit-check parts on their own plate: with the set they make 290 x 239 (+ brims 300 x 249) — inside the 305 bed
    # but outside the 280 mm envelope plus4_print.py's check enforces, and a 25 h single job is a bad bet anyway.
    fb, dg = meshes["vib01e_base"], meshes["digiducer_sidecar_pla"]
    lob, hib = bbox(fb); lod, hid = bbox(dg)
    out["plate_fitcheck_parts"] = np.concatenate([place(fb, -lob[0], -lob[1]), place(dg, (hib[0] - lob[0]) + gap - lod[0], -lod[1])])
    for name, tri in out.items():
        lo, hi = bbox(tri); ext = hi - lo
        fit = ext[0] + 2 * BRIM <= ENVELOPE and ext[1] + 2 * BRIM <= ENVELOPE
        print(f"  {name:22s} footprint {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f} (+{BRIM} brim) -> check envelope {ENVELOPE:.0f}: {'FITS' if fit else '*** DOES NOT FIT ***'}")
        if not fit: raise SystemExit(f"{name} does not fit the bed")
        save_stl(HERE / f"{name}.stl", tri)
    return out


# ------------------------------------------------------------------- slice
def slice_one(stl, label):
    out = GCODE / (stl.stem + "_PLA.gcode")
    cmd = [sys.executable, str(PLUS4), "slice", str(stl), "--material", "pla", "--brim", str(BRIM), "--check", "--out", str(out),
           *sum([["--set", o] for o in PROC_OV], [])]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd=str(REPO))
    txt_out = r.stdout + r.stderr
    if r.returncode != 0 or not out.exists():
        print(txt_out[-3000:]); raise SystemExit(f"slice failed: {stl.name}")
    g = out.read_text(errors="ignore")
    tm = re.search(r"; estimated printing time \(normal mode\) = (.+)", g)
    fg = re.search(r"; filament used \[g\] = ([\d.]+)", g)
    fv = re.search(r"; filament used \[cm3\] = ([\d.]+)", g)
    head = g[:g.find(";LAYER_CHANGE")]
    # plus4_print.py replaces the QIDI PRINT_START macro with an explicit preamble (G28, M190, M109, M141)
    m190 = re.findall(r"^M190 S(\d+)", head, re.M); m109 = re.findall(r"^M109 S(\d+)", head, re.M)
    m104 = sorted(set(re.findall(r"^M104 S(\d+)", head, re.M))); m140 = sorted(set(re.findall(r"^M140 S(\d+)", head, re.M)))
    maxz = re.search(r"; max_z_height: ([\d.]+)", g)
    cm3 = float(fv.group(1)) if fv else 0.0
    grams = float(fg.group(1)) if fg and float(fg.group(1)) > 0 else cm3 * PLA_RHO   # Bambu PLA profile has filament_density 0
    issues = [ln.strip(" │") for ln in txt_out.splitlines() if ln.startswith("│") and "exceeds" in ln or "expected" in ln]
    known_fp = [i for i in issues if "max Y=290" in i]       # end-gcode park move (G0 Y290 after UNLOAD_FILAMENT); same on vib01c_set.gcode (printed OK)
    real = [i for i in issues if i not in known_fp]
    res = dict(label=label, gcode=out, time=tm.group(1).strip() if tm else "?", g=grams, cm3=cm3,
               preamble=f"G28 / M190 S{m190[0] if m190 else '?'} / M109 S{m109[0] if m109 else '?'}", m104=m104, m140=m140,
               maxz=maxz.group(1) if maxz else "?", issues=real, known_fp=known_fp)
    print(f"\n{label}  ->  {out.name}")
    print(f"  time {res['time']}   filament {cm3:.1f} cm3 = {grams:.0f} g PLA (1.24 g/cm3)   max z {res['maxz']}")
    print(f"  preamble {res['preamble']}   startup M104={m104} M140={m140}")
    for i in known_fp: print(f"  check (known false positive, end-gcode park): {i}")
    for i in real: print(f"  check ISSUE: {i}")
    ok = bool(m190) and bool(m109) and m140 == [m190[0]] and m104 == [m109[0]] and not real
    print(f"  [{'PREAMBLE + CHECK OK' if ok else '*** CHECK FAILED ***'}]")
    if not ok: raise SystemExit(f"slice check failed: {out.name}")
    return res


# ---------------------------------------------------------- profile SVG
def profile_svg(log):
    """Dimensioned cross-section at a band station and between stations, 2:1, every number from the model echo."""
    e = " ".join(log)
    z = re.search(r"Z: plate 0\.\.([\d.]+) \| flange \.\.([\d.]+) \| body \.\.([\d.]+) = PAD PLANE \| head \.\.([\d.]+) \| band slot z ([\d.]+)\.\.([\d.]+) \(([\d.]+) wide, crown ([\d.]+)\)", e)
    plate_t, z_body0, z_bear, z_head, zs0, zs1, slot_w, crown = map(float, z.groups())
    plate_w = float(re.search(r"plate [\d.]+ x ([\d.]+) x", e).group(1))
    pr = re.search(r"head ([\d.]+) x ([\d.]+) \(groove ([\d.]+) x ([\d.]+).*bearing ([\d.]+) wide \(pads 2 x ([\d.]+)\); body [\d.]+ x ([\d.]+); flange ([\d.]+) x ([\d.]+)", e)
    head_w, head_h, groove_w, groove_d, body_w, pad_w, body_h, flange_w, flange_h = map(float, pr.groups())
    hole_d = float(re.search(r"x Ø([\d.]+) at ([\d.]+) pitch", e).group(1)); pitch = float(re.search(r"x Ø[\d.]+ at ([\d.]+) pitch", e).group(1))
    S = 4.0; ox, oy = 40.0, 170.0           # 4 px/mm, origin of the section (x = -Y edge, y = bed) in each panel
    def X(y): return ox + y * S
    def Y(z): return oy - z * S
    yc = plate_w / 2
    def poly(pts, fill="#cfd8e3"): return f'<polygon points="{" ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in pts)}" fill="{fill}" stroke="#223" stroke-width="1.2"/>'
    def dim(x1, y1, x2, y2, label, off=0, vert=False):
        if vert:
            xx = x1 + off
            return (f'<line x1="{xx}" y1="{y1}" x2="{xx}" y2="{y2}" stroke="#b00" stroke-width="0.8"/>'
                    f'<text x="{xx+3}" y="{(y1+y2)/2+3}" font-size="10" fill="#b00" font-family="Helvetica">{label}</text>')
        yy = y1 + off
        return (f'<line x1="{x1}" y1="{yy}" x2="{x2}" y2="{yy}" stroke="#b00" stroke-width="0.8"/>'
                f'<text x="{(x1+x2)/2}" y="{yy-3}" font-size="10" fill="#b00" text-anchor="middle" font-family="Helvetica">{label}</text>')
    # section polygon (outline, -Y to +Y), between stations (solid) — then the slot drawn as a hole in panel 2
    outline = [(0, 0), (plate_w, 0), (plate_w, plate_t), (yc + flange_w/2, plate_t), (yc + flange_w/2, z_body0),
               (yc + body_w/2, z_body0), (yc + body_w/2, z_bear), (yc + head_w/2, z_bear), (yc + head_w/2, z_head),
               (yc - head_w/2, z_head), (yc - head_w/2, z_bear), (yc - body_w/2, z_bear), (yc - body_w/2, z_body0),
               (yc - flange_w/2, z_body0), (yc - flange_w/2, plate_t), (0, plate_t)]
    W = int(X(plate_w) + 190); H = 230
    panels = []
    for k, title in enumerate(["BETWEEN band stations (solid body)", f"AT a band station: slot {slot_w:g} x {zs1-zs0:g}, 45 deg gable to a {crown:g} crown"]):
        g = [f'<g transform="translate({k*W},0)">', poly(outline)]
        if k == 1:
            sp = (zs1 - zs0) - 0.9
            slot = [(yc - body_w/2 - 1, z_body0), (yc + body_w/2 + 1, z_body0)]
            g.append(f'<rect x="{X(yc-body_w/2-1):.1f}" y="{Y(zs1):.1f}" width="{(body_w+2)*S:.1f}" height="{(zs1-zs0)*S:.1f}" fill="#fff" stroke="none"/>')
            # gable: the slot polygon (wall 0.9 then 45 deg to the crown) drawn at the section plane
            g.append(poly([(yc - slot_w/2, z_body0), (yc + slot_w/2, z_body0), (yc + slot_w/2, zs0 + 0.9), (yc + crown/2, zs1), (yc - crown/2, zs1), (yc - slot_w/2, zs0 + 0.9)], fill="#fff"))
            g.append(f'<text x="{X(yc):.1f}" y="{Y(z_body0)+12:.1f}" font-size="9" text-anchor="middle" fill="#555" font-family="Helvetica">band passes here, on the flange step</text>')
        else:
            g.append(f'<rect x="{X(yc-hole_d/2):.1f}" y="{Y(z_head):.1f}" width="{hole_d*S:.1f}" height="{(z_head-z_body0)*S:.1f}" fill="#fff" stroke="#223" stroke-dasharray="3,2" stroke-width="0.8"/>')
            g.append(f'<text x="{X(yc):.1f}" y="{Y(z_body0)+12:.1f}" font-size="9" text-anchor="middle" fill="#555" font-family="Helvetica">seat-stop hole Ø{hole_d:g} @ {pitch:g} (blind to the flange step)</text>')
        g += [dim(X(yc-head_w/2), Y(z_head), X(yc+head_w/2), Y(z_head), f"head {head_w:g} (INFERRED 16-19)", off=-12),
              dim(X(yc-body_w/2), Y(z_head), X(yc+body_w/2), Y(z_head), f"bearing {body_w:g} = pads 2 x {pad_w:g} either side of the head (INFERRED: a flat 2 mm below the head top)", off=-30),
              dim(X(yc-flange_w/2), Y(0), X(yc+flange_w/2), Y(0), f"flange step {flange_w:g} x {flange_h:g} (fixture only)", off=22),
              dim(X(yc+body_w/2)+8, Y(z_head), 0, Y(z_bear), f"head {head_h:g} (INFERRED)", vert=True),
              dim(X(yc+body_w/2)+8, Y(z_bear), 0, Y(z_body0), f"body {body_h:g} (fixture)", off=60, vert=True),
              dim(X(plate_w)+8, Y(plate_t), 0, Y(0), f"plate {plate_t:g}", vert=True),
              f'<text x="{ox}" y="{H-12}" font-size="11" font-family="Helvetica" fill="#223">{title}</text>', "</g>"]
        panels.append("\n".join(g))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{2*W}" height="{H}" viewBox="0 0 {2*W} {H}" font-family="Helvetica">'
           f'<rect width="100%" height="100%" fill="#fff"/>'
           f'<text x="{ox}" y="16" font-size="12" font-weight="bold" fill="#223">seat_rail_fixture — rail cross-section AS MODELLED (rail_interface.scad + lib), 4 px/mm, -Y on the left. Every INFERRED number is a caliper item (README section 5).</text>'
           + "\n".join(panels) + "</svg>")
    (HERE / "profile_inferred.svg").write_text(svg)


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
    o = openscad(SEGS["rail_seg1_node"], ["-D", 'part="gauge"', "-o", str(HERE / "rail_gauge.stl")])
    meshes["rail_gauge"] = load_stl(HERE / "rail_gauge.stl")
    lo, hi = bbox(meshes["rail_gauge"]); v = stl_volume(meshes["rail_gauge"]) / 1000
    print(f"  {'rail_gauge':22s} {len(meshes['rail_gauge']):6d} tris  {hi[0]-lo[0]:.1f} x {hi[1]-lo[1]:.1f} x {hi[2]-lo[2]:.1f}  {v:6.1f} cm3 solid")
    for name, p in FIT_PARTS.items():
        meshes[name] = load_stl(p); lo, hi = bbox(meshes[name])
        print(f"  {name:22s} (existing) {hi[0]-lo[0]:.1f} x {hi[1]-lo[1]:.1f} x {hi[2]-lo[2]:.1f}")

    print("\n== model echoes")
    for name in SEGS:
        print(f"  [{name}]")
        for ln in logs[name]:
            if not ln.startswith("GAUGE") or name == "rail_seg1_node": print("    " + ln)

    print("\n== ray-cast verification on the exported meshes")
    for name in SEGS: verify_segment(name, meshes[name], logs[name])

    print("\n== plates")
    build_plates(meshes)

    if not a.no_renders:
        print("\n== renders")
        R = [("rail_seg1_node", "seg", "100,42,12,50,0,25,520", "preview_seg1.png"),
             ("rail_seg1_node", "assembly", "100,42,20,55,0,35,520", "preview_seg1_assembly.png"),
             ("rail_seg2_digiducer", "seg", "100,42,12,50,0,25,520", "preview_seg2.png"),
             ("rail_seg2_digiducer", "assembly", "100,42,20,55,0,35,540", "preview_seg2_assembly.png"),
             ("rail_seg1_node", "seg", "100,42,11,90,0,90,130", "preview_profile_end.png"),
             ("rail_seg1_node", "gauge", "55,15,5,45,0,20,280", "preview_gauge.png")]
        for name, part, cam, png in R:
            ortho = png == "preview_profile_end.png"
            openscad(SEGS[name], ["-D", f'part="{part}"', "--camera=" + cam, "--projection=" + ("o" if ortho else "p"),
                                  "--imgsize=1600,1000", "--colorscheme=Tomorrow", "-o", str(HERE / png)])
            print(f"  {png}")
        profile_svg(logs["rail_seg1_node"]); print("  profile_inferred.svg")

    if a.no_slice: return
    print("\n================ PLA SLICES via plus4_print.py (nothing is sent) ================")
    results = [slice_one(HERE / "rail_seg1_node.stl", "SEG 1 NODE alone"),
               slice_one(HERE / "rail_seg2_digiducer.stl", "SEG 2 DG-B alone"),
               slice_one(HERE / "rail_gauge.stl", "gauge alone"),
               slice_one(HERE / "plate_fixture_set.stl", "PLATE: seg 1 + seg 2 + gauge"),
               slice_one(HERE / "plate_fitcheck_parts.stl", "PLATE: rev E base + Digiducer sidecar (fit-check parts, already printed once)")]
    print("\n== summary")
    for r in results:
        print(f"  {r['label']:62s} {r['time']:>12s}  {r['cm3']:6.1f} cm3  {r['g']:4.0f} g  {r['gcode'].name}")
    print(f"\ngcode in {GCODE} (git-ignored) — NOT sent to the printer.")


if __name__ == "__main__":
    main()
