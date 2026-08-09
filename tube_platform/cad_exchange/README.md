# tube_platform rev B — CAD exchange (true B-rep STEP, positioned assembly)

STEP/STL for **SolidWorks** (or any B-rep CAD). These are *exchange* copies.
The **source of truth for printing remains the OpenSCAD files** one directory
up (`../make_tube_platform.scad`) and in `../../slimrig_mounts/`.

Same contract and the same generator pattern as
`slimrig_mounts/cad_exchange/` — in fact this generator **imports**
`slimrig_mounts/make_slimrig_brep.py` rather than re-implementing the canon cap,
spacer and tube plates, so the two directories cannot drift on the shared
interface. Seven `assert`s at import time check exactly that (tube Ø and
c-c, trough radius, cap body/pinch/bolt spacing, M3 clearance and counterbore,
heat-set bore, spacer OD/height).

## Files

| File | What it is |
|---|---|
| `tube_platform_assembly.step` | **the system**, 33 solids in true relative position: plate, fence, RTK tower, hanging carrier + 2 retainer bars, 2 rail clamps, 4 caps, 12 spacers, the Jetson Nano plate + its 2 caps + 4 spacers, and the 2 Ø15 tubes |
| `tube_platform_assembly_with_orin.step` | the same plus the Orin plate group at its earliest non-interfering station (centre y −142). **Needs a ≈330 mm tube pair** — see `../ASSEMBLY.md` §7 |
| `tp_plate.step` · `tp_fence.step` · `tp_tower.step` · `tp_carrier.step` · `tp_retainer_bar.step` · `tp_rail.step` · `tp_cap.step` · `tp_spacer.step` | the individual printed parts, **in the assembly (design) frame** |
| `*.stl` | mesh companions to each STEP (0.005 / 0.05 tolerance) |

`tp_rail.step` is the **west** rail; the east rail is its mirror about the YZ
plane (the assembly file contains both).

## Coordinate frame

The platform **design** frame, not a print frame:

* plate underside **z = 0**, plate top z = 7
* tubes run along **Y** at x = ±30 (60 c-c), tube axis **z = −61.7**
* **+Y = north** — the end the Jetson Nano inserts from
* corridor floor (tube top) z = −54.0, so the clear corridor is 54.0

Each part STEP is oriented **as it sits in the machine**, so dropping them into
one SolidWorks assembly at the origin reproduces the system. That is *not* the
print orientation — take print STLs from the `.scad`, never from here.

## Which file is authoritative for what

| Purpose | Authoritative file |
|---|---|
| **Printing / slicing** | `../make_tube_platform.scad` and the `../tp_*.stl` it emits |
| **Dimensions** | the `.scad` files — always |
| **SolidWorks / mating / downstream CAD** | the `.step` files here |
| Regenerating | `make_tube_platform_brep.py` |
| Checking | `verify_assembly.py` |

## Verification (2026-08-08)

`../../slimrig_mounts/verify_step.py`'s reader over every file here:

| File | Solids | Closed | BRepCheck | Faces (plane / cyl / cone) | Volume mm³ |
|---|---|---|---|---|---|
| `tp_plate.step` | 1 | yes | valid | 100 (36 / 40 / 24) | 83475.435 |
| `tp_fence.step` | 1 | yes | valid | 43 (22 / 21 / 0) | 11526.583 |
| `tp_tower.step` | 1 | yes | valid | 50 (22 / 24 / 4) | 14730.049 |
| `tp_carrier.step` | 1 | yes | valid | 64 (31 / 29 / 4) | 36540.304 |
| `tp_retainer_bar.step` | 1 | yes | valid | 12 (8 / 4 / 0) | 2755.586 |
| `tp_rail.step` | 1 | yes | valid | 39 (24 / 12 / 3) | 59874.901 |
| `tp_cap.step` | 1 | yes | valid | 14 (9 / 3 / 2) | 5737.039 |
| `tp_spacer.step` | 1 | yes | valid | 4 (2 / 2 / 0) | 176.432 |
| `tube_platform_assembly.step` | 33 | all yes | valid | 572 (295 / 223 / 54) | 462555.744 |

**Zero B-spline or tessellated faces in any file.** Schema **AP214**
(`AUTOMOTIVE_DESIGN`), length unit **millimetre** (`SI_UNIT(.MILLI.,.METRE.)`).
Analytic cylinder radii read back exactly as designed: `r=1.7` (M3 clearance
3.4), `r=2.2` (heat-set 4.4), `r=3.1` (counterbore 6.2), `r=3.25` (SMA 6.5),
`r=3.5` (spacer OD 7), `r=4.0` (lightening Ø8), `r=4.5` (tower leg / fence
flange Ø9), `r=5.0` (carrier wire pass Ø10), `r=7.5` (**the Ø15.0 tube**),
`r=7.7` (trough, Ø15.0 + 0.4), `r=12.0` (Ø24 passthrough in the Nano plate).

> `verify_step.py` prints `VERDICT: FAIL` for the two assembly files. That check
> is written for a single-solid part and asserts `solids == 1`; a 33-body
> assembly trips it by design. Every per-body result above is a pass.

### Volume cross-check vs. the printed OpenSCAD meshes

`make_tube_platform_brep.py` re-computes the mesh volume of each `../tp_*.stl`
and compares:

| Job | B-rep (analytic) | OpenSCAD mesh (`$fn=52`) | Δ |
|---|---|---|---|
| `tp_plate` | 83475.435 | 83486.843 | −11.408 (−0.014 %) |
| `tp_fence` | 11526.583 | 11527.809 | −1.226 (−0.011 %) |
| `tp_tower` | 14730.049 | 14716.057 | **+13.991 (+0.095 %)** |
| `tp_carrier` (+ 2 bars) | 42051.476 | 42046.606 | +4.870 (+0.012 %) |
| `tp_clamps` (2 rails) | 119749.803 | 119778.791 | −28.988 (−0.024 %) |
| `tp_caps_spacers` (4 + 12) | 25065.338 | 25078.712 | −13.374 (−0.053 %) |

Signs are the expected ones and confirm there is no dimensional error. `$fn=52`
inscribed polygons make every **bore** slightly undersized, so a bore-dominated
part reads *high* as a mesh (negative Δ). The **tower** is the one part whose
outer boundary is a hull of circles — an inscribed 52-gon shrinks that convex
outline, so its mesh reads *low* (positive Δ). Every part behaves accordingly.

### Assembly-level checks

`verify_assembly.py` (see `../ASSEMBLY.md` §9 for the full result table) runs
boolean interference over all 528 body pairs, exact OCCT solid-to-solid
distances on the load-bearing interfaces, a bore-proximity map of the 7 mm
plate, a fastener-stack audit and a Ø9 driver-access sweep. It **exits non-zero
today** — the findings are real and are documented in `../ASSEMBLY.md` §8; they
are defects in the parts, not in this rebuild.

## SolidWorks import notes

* **File → Open → STEP AP214.** Import the assembly as **multibody** (or let
  SolidWorks split it into an assembly of parts — the bodies carry names such as
  `tp_plate`, `tp_rail_west`, `tp_cap_W1`, `nano_tube_plate`, `tube_west`, and
  per-body colours).
* **Units are millimetres** and declared in the file. Open into an MMGS
  document; do **not** apply a unit scale.
* Bodies arrive as imported (dumb) solids, but every bore is a real cylindrical
  face and every insert chamfer a real cone, so **concentric / coincident mates
  work directly** and FeatureWorks has analytic geometry to recognise.
* `tube_west` / `tube_east` are Ø15.0 × 231.7 stock cylinders, not printed
  parts. Delete or suppress them if you are only after the plastic.
* **CSG epsilons are preserved, not cleaned.** The `.scad`'s +0.1 / +0.2 / +0.05
  overshoots on bores are reproduced exactly, as is the rail blade's 0.01 mm
  short-fall under the plate underside (`TZ+17-eps`). They exist in the printed
  parts, so they exist here.

## Regenerating

The repo `.venv` (Python 3.10) already has **build123d 0.10.0**:

```bash
cd /Users/sic_intel/Documents/GitHub/michelangelo
.venv/bin/python tube_platform/cad_exchange/make_tube_platform_brep.py   # STEP + STL
.venv/bin/python tube_platform/cad_exchange/verify_assembly.py           # all six checks
```

`make_tube_platform_brep.py` transcribes the `.scad` parameters verbatim,
including the CSG epsilons, and imports the canon geometry from
`slimrig_mounts/make_slimrig_brep.py`. **If a dimension changes, change the
`.scad` first and copy it here second** — the generator does not read the
`.scad`, so the two can drift if you edit only one. The `assert`s catch drift in
the *shared* canon; they cannot catch drift in a platform-only parameter.
