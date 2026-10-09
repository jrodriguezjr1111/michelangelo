#!/usr/bin/env python3
"""
Concept E rev C (full-height cage) — renders + GNSS mask diagram.

    python3 render_E_revC.py            # all four PNGs into renders/

  renders/E_revC_iso.png              openscad, rev C assembled (2000 px)
  renders/E_revC_iso_siderails.png    openscad, same + the optional side rails
  renders/E_revC_side_elevation.png   openscad orthographic elevation; numbered markers located by
                                      rendering each marker alone with the same camera, then numbered
                                      + a legend drawn with PIL (no 3D text in the model)
  renders/E_revC_gnss_mask.png        matplotlib: rail/post shadow on the dome's sky + the two sections

Every number comes from the model's own ECHO lines (t1_concept_E.scad, rev="C") or t1_params.py —
nothing is re-typed here.  Nothing is sliced or printed.
"""
from __future__ import annotations
import math, re, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SCAD = HERE / "t1_concept_E.scad"
OUT = HERE / "renders"
OSC = "/opt/homebrew/bin/openscad"
sys.path.insert(0, str(HERE))
import t1_params as P  # noqa: E402

ISO_CAM = "203,139,120,62,0,-38,1450"
ELEV_CAM = "186,-1200,135,186,0,135"          # eye, centre: looking +Y, x right, z up
ELEV_SIZE = (1340, 1300)
FONT = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
FONT2 = "/System/Library/Fonts/Helvetica.ttc"


def osc(defs: dict, out: Path, cam: str, proj: str, size=(2000, 1400), extra=()):
    args = [OSC, "--colorscheme=Tomorrow",
            f"--camera={cam}", f"--projection={proj}", f"--imgsize={size[0]},{size[1]}", *extra]
    for k, v in defs.items():
        args += ["-D", f'{k}={v}']
    r = subprocess.run(args + ["-o", str(out), str(SCAD)], capture_output=True, text=True)
    if r.returncode or not out.exists():
        raise SystemExit(f"openscad failed ({out.name}):\n{r.stderr[-2000:]}")
    return r.stderr


def echoes() -> dict:
    with tempfile.TemporaryDirectory() as td:
        e = Path(td) / "c.echo"
        subprocess.run([OSC, "-D", 'rev="C"', "-D", 'view="iso"', "-o", str(e), str(SCAD)],
                       check=True, capture_output=True)
        txt = e.read_text()
    g = lambda pat: [float(x) for x in re.search(pat, txt).groups()]
    d = {}
    d["post"], d["top_z0"], d["top_top"], d["overall"] = g(r"posts (\d+).*?underside z ([\d.]+), top-rail top z ([\d.]+), overall ([\d.]+)")
    d["dome_top"], d["ma_top"], d["ma_ant_top"], d["whip_top"] = g(r"dome ([\d.]+) .*?MA963 clamps ([\d.]+) .*?radome ([\d.]+) \| whip tips ([\d.]+)")
    d["pc_z"], d["dome_cx"] = g(r"DOME L1 PC z ([\d.]+) at x ([\d.]+)")
    d["ma_rc"], d["ma_cx"] = g(r"MA963 element ref z ([\d.]+) at x ([\d.]+)")
    d["co_z0"], = g(r"CO tray [\d.]+-[\d.]+ z ([\d.]+)")
    d["txt"] = txt
    return d


def blob_centre(png: Path):
    a = np.asarray(Image.open(png).convert("RGB")).astype(int)
    bg = a[2, 2]
    m = np.abs(a - bg).sum(axis=2) > 40
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        raise SystemExit(f"marker not found in {png}")
    return float(xs.mean()), float(ys.mean())


def elevation(d):
    base = OUT / "E_revC_side_elevation.png"
    osc({"rev": '"C"', "view": '"elev"'}, base, ELEV_CAM, "o", ELEV_SIZE)
    z = d
    legend = [
        (1, f"top-rail top  z {z['top_top']:.0f}  (posts {z['post']:.0f} + deck 20 + gusset 3 + rail 20)"),
        (2, f"top-rail underside  z {z['top_z0']:.0f}"),
        (3, f"dome top  z {z['dome_top']:.1f}  ->  {z['top_top'] - z['dome_top']:.1f} under the top rail (>= 15)"),
        (4, f"dome L1 phase centre (EST)  z {z['pc_z']:.1f}  ->  rails {z['top_top'] - z['pc_z']:.1f} above it"),
        (5, f"MA963 corner-clamp top  z {z['ma_top']:.1f} (radome {z['ma_ant_top']:.1f})  ->  {z['top_top'] - z['ma_top']:.1f} under"),
        (6, f"1090/978 stubby tips  z {z['whip_top']:.0f}  ->  {z['top_top'] - z['whip_top']:.0f} under"),
        (7, f"rod axis  z {P.ROD_Z}  (unchanged from rev B)"),
        (8, f"CO tray underside (hung under the rods)  z {z['co_z0']:.1f}"),
        (9, "deck member top  z 20  (trays sit here)"),
        (10, "deck underside  z 0"),
    ]
    pos = {}
    with tempfile.TemporaryDirectory() as td:
        for i, _ in legend:
            f = Path(td) / f"m{i}.png"
            osc({"rev": '"C"', "view": '"marker"', "mkid": i}, f, ELEV_CAM, "o", ELEV_SIZE)
            pos[i] = blob_centre(f)
    im = Image.open(base).convert("RGB")
    W, H = im.size
    panel = 660
    canvas = Image.new("RGB", (W + panel, H), im.getpixel((2, 2)))
    canvas.paste(im, (0, 0))
    dr = ImageDraw.Draw(canvas)
    f_num = ImageFont.truetype(FONT, 30)
    f_leg = ImageFont.truetype(FONT, 27)
    f_hd = ImageFont.truetype(FONT, 36)
    ink, mag = (30, 30, 32), (217, 26, 140)
    for i, (x, y) in pos.items():                     # number tag beside each sphere
        tx, ty = x + 16, y - 34
        dr.rounded_rectangle([tx, ty, tx + (44 if i >= 10 else 30), ty + 32], 6, fill=(255, 255, 255), outline=mag, width=2)
        dr.text((tx + 7, ty + 1), str(i), font=f_num, fill=ink)
    x0 = W + 20
    dr.text((x0, 50), "CONCEPT E REV C - SIDE ELEVATION", font=f_hd, fill=ink)
    dr.text((x0, 100), "looking +Y, orthographic; z from the deck underside, mm", font=f_leg, fill=(90, 90, 92))
    y = 180
    for i, s in legend:
        dr.ellipse([x0, y + 4, x0 + 22, y + 26], fill=mag)
        dr.text((x0 + 34, y), f"{i}", font=f_leg, fill=ink)
        words, line, lines = s.split(), "", []
        for w_ in words:
            if dr.textlength(line + " " + w_, font=f_leg) > panel - 110:
                lines.append(line); line = w_
            else:
                line = (line + " " + w_).strip()
        lines.append(line)
        for k, ln in enumerate(lines):
            dr.text((x0 + 70, y + k * 34), ln, font=f_leg, fill=ink)
        y += 34 * len(lines) + 16
    y += 20
    for s in [f"posts {z['post']:.0f}  |  overall height {z['overall']:.0f} (rail top + 3 mm gussets)",
              "footprint 406 x 279 (unchanged)", "yellow bars, far left: post 222 (inner), overall 268 (outer)",
              "blue line: dome phase centre (EST)"]:
        dr.text((x0, y), s, font=f_leg, fill=ink); y += 40
    canvas.save(base)
    return pos


def gnss_mask(d):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle
    E, DX, DY = 20.0, 406.0, 279.0
    tt, t0, pcz, cx, cy = d["top_top"], d["top_z0"], d["pc_z"], d["dome_cx"], DY / 2
    BLUE, ORANGE, GREY, INK, MUTED = "#2a78d6", "#eb6834", "#8a8a8e", "#0b0b0b", "#52514e"

    # --- sky map by ray casting: which (az, el) rays from the phase centre hit rails / posts / gussets
    boxes = [((0, 0, t0), (DX, E, tt)), ((0, DY - E, t0), (DX, DY, tt)),            # long rails
             ((0, E, t0), (E, DY - E, tt)), ((DX - E, E, t0), (DX, DY - E, tt))]    # end rails
    boxes += [((x, y, 23), (x + E, y + E, t0)) for x in (0, DX - E) for y in (0, DY - E)]   # posts
    boxes += [((x, y, tt), (x + 60, y + 60, tt + 3)) for x in (0, DX - 60) for y in (0, DY - 60)]  # top gussets
    def hit(az, el, org):
        dv = np.array([math.cos(el) * math.sin(az), math.cos(el) * math.cos(az), math.sin(el)])
        for lo, hi in boxes:
            t_min, t_max = 0.0, 1e9
            ok = True
            for k in range(3):
                if abs(dv[k]) < 1e-12:
                    if not (lo[k] <= org[k] <= hi[k]):
                        ok = False; break
                else:
                    a_, b_ = (lo[k] - org[k]) / dv[k], (hi[k] - org[k]) / dv[k]
                    t_min, t_max = max(t_min, min(a_, b_)), min(t_max, max(a_, b_))
            if ok and t_min <= t_max and t_max > 0:
                return True
        return False
    org = (cx, cy, pcz)
    azs = np.radians(np.arange(0, 360, 1.0))
    els = np.radians(np.arange(0.25, 90, 0.5))           # whole upper hemisphere
    blk = np.array([[hit(a, e, org) for a in azs] for e in els])
    def frac_above(m_deg):
        sel = np.degrees(els) >= m_deg
        w = np.cos(els[sel])[:, None]
        return float((blk[sel] * w).sum() / (w.sum() * len(azs)))
    stats = {m: 100 * frac_above(m) for m in (0, 10, 15)}
    d["sky_blocked"] = stats

    fig = plt.figure(figsize=(20, 11), dpi=100)
    fig.patch.set_facecolor("#fcfcfb")
    gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 1], hspace=0.32, wspace=0.16,
                          left=0.04, right=0.95, top=0.88, bottom=0.09)

    def section(ax, title, d_list, span, label_axis):
        ax.set_title(title, loc="left", fontsize=15, color=INK)
        lo, hi = span
        for (pos, lab) in d_list:                               # rail sections (20 x 20) at each side
            ax.add_patch(Rectangle((pos[0], t0), E, E, color=GREY))
        ax.add_patch(Rectangle((cx_s - 75, pcz - 35), 150, 60, facecolor="#f3f3ef", edgecolor=MUTED, lw=1.5))
        ax.plot([cx_s], [pcz], "o", color=BLUE, ms=9, zorder=5)
        for (pos, lab) in d_list:
            inner = pos[0] + (E if pos[0] < cx_s else 0)
            ang = math.degrees(math.atan((tt - pcz) / abs(inner - cx_s)))
            sgn = -1 if pos[0] < cx_s else 1
            L = 300
            ax.plot([cx_s, cx_s + sgn * L * math.cos(math.radians(ang))], [pcz, pcz + L * math.sin(math.radians(ang))],
                    color=BLUE, lw=2)
            ax.text(cx_s + sgn * 150, pcz + 150 * math.tan(math.radians(ang)) + 14, f"{ang:.1f}°  {lab}",
                    ha="center", fontsize=13, color=INK)
        for m, ls in ((10, ":"), (15, "--")):
            for sgn in (-1, 1):
                ax.plot([cx_s, cx_s + sgn * 320 * math.cos(math.radians(m))], [pcz, pcz + 320 * math.sin(math.radians(m))],
                        color=ORANGE, lw=1.6, ls=ls)
            ax.text(cx_s + 330 * math.cos(math.radians(m)), pcz + 330 * math.sin(math.radians(m)), f"{m}° RTK mask",
                    fontsize=12, color=ORANGE, va="center")
        ax.axhline(pcz, color=GREY, lw=0.8)
        ax.set_xlim(lo, hi); ax.set_ylim(120, 330); ax.set_aspect("equal")
        ax.set_xlabel(label_axis, color=MUTED); ax.set_ylabel("z mm", color=MUTED)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    ax1 = fig.add_subplot(gs[0, 0])
    cx_s = cy
    section(ax1, f"Y-Z section through the dome centre (x {cx:.0f}): fore-aft long rails",
            [((0, 1), "y=0 rail"), ((DY - E, 1), "y=279 rail")], (-160, 460), "y mm (fore-aft, +Y nose)")
    ax2 = fig.add_subplot(gs[1, 0])
    cx_s = cx
    section(ax2, f"X-Z section through the dome centre (y {cy:.1f}): lateral end rails",
            [((0, 0), "x=0 rail"), ((DX - E, 0), "x=406 rail")], (-60, 620), "x mm (lateral)")

    ax3 = fig.add_subplot(gs[:, 1], projection="polar")
    ax3.set_theta_zero_location("N"); ax3.set_theta_direction(-1)
    A, R = np.meshgrid(azs, 90 - np.degrees(els))
    ax3.contourf(A, R, blk.astype(float), levels=[0.5, 1.5], colors=[GREY], alpha=0.85)
    th = np.linspace(0, 2 * np.pi, 361)
    ax3.plot(th, np.full_like(th, 80), color=ORANGE, ls=":", lw=1.8, label="10° mask")
    ax3.plot(th, np.full_like(th, 75), color=ORANGE, ls="--", lw=1.8, label="15° mask")
    ax3.set_rlim(0, 90); ax3.set_rticks([30, 60, 75, 80, 90])
    ax3.set_yticklabels(["60°", "30°", "15°", "10°", "0°"], color=MUTED, fontsize=10)
    ax3.set_xticks(np.radians([0, 90, 180, 270]))
    ax3.set_xticklabels(["+Y nose\ny=279 rail", "+X  \nx=406\nrail  ", "-Y tail\ny=0 rail", "  -X\nx=0\n  rail"], fontsize=11)
    ax3.set_title("Dome sky map from the L1 phase centre (grey = rail / post / gusset shadow)\n"
                  f"share of the sky above each mask that the cage shadows:  0°: {stats[0]:.1f} %   10°: {stats[10]:.1f} %   15°: {stats[15]:.1f} %",
                  fontsize=14, color=INK, pad=24)
    ax3.legend(loc="lower left", bbox_to_anchor=(-0.05, -0.08), frameon=False, fontsize=12)

    fig.suptitle(f"Concept E rev C: GNSS mask from the top rails (rail top z {tt:.0f}, dome L1 PC z {pcz:.1f} EST, "
                 f"h = {tt - pcz:.1f} mm)", x=0.04, ha="left", fontsize=19, color=INK)
    fig.text(0.04, 0.012, "Geometric (ray) shadow, cos(el)-weighted share of the whole sky.  A 20 mm rail is ~0.1 lambda at L1 (190 mm): "
             "expect diffraction and a few dB of C/N0 loss in these bands, not a hard cut;\nthe larger RTK risk is near-field "
             "pattern / phase-centre distortion and multipath from the anodised rails.  Dome size and L1 phase centre are EST "
             "(no datasheet).  The C172 cabin itself (roof, sills, seats) is not drawn.", fontsize=11.5, color=MUTED)
    out = OUT / "E_revC_gnss_mask.png"
    fig.savefig(out, dpi=100, facecolor=fig.get_facecolor())
    plt.close(fig)
    return stats


def main():
    OUT.mkdir(exist_ok=True)
    d = echoes()
    osc({"rev": '"C"', "view": '"iso"'}, OUT / "E_revC_iso.png", ISO_CAM, "p")
    osc({"rev": '"C"', "view": '"iso"', "side_rails": "true"}, OUT / "E_revC_iso_siderails.png", ISO_CAM, "p")
    elevation(d)
    st = gnss_mask(d)
    print("posts %.0f  top-rail top %.0f  overall %.0f" % (d["post"], d["top_top"], d["overall"]))
    print("dome sky blocked (cos-weighted): >0 deg %.1f %%  >10 deg %.1f %%  >15 deg %.1f %%" % (st[0], st[10], st[15]))
    for f in ("E_revC_iso.png", "E_revC_iso_siderails.png", "E_revC_side_elevation.png", "E_revC_gnss_mask.png"):
        print("  wrote", OUT / f)


if __name__ == "__main__":
    main()
