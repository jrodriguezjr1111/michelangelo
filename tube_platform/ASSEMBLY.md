# tube_platform rev B — system assembly, BOM and build order

> ## ⚠ STALE AS OF rev E — DO NOT BUILD FROM THIS FILE
> This document describes the **rev-B** platform: the RTK tower, the hanging
> ESP32 carrier, the breadboard tray and a 94 x 134 x 7 plate with
> component-specific bores. All of that is retired.
> **`README.md` is the current authority** (rev E: cheese plate, 94 x 134 x 8,
> 10 mm insert grid, grid shoes, cheese deck).
> Still accurate here and worth reading: the **rail-clamp + cap install order**,
> the **Nano corridor / insertion procedure**, and the **Orin-not-co-mounted**
> discussion — none of which rev E changed. The **BOM and the loadout sections
> are wrong**; use the rev-E BOM in `README.md`.
> `make_system_assembly.scad` + `asm_shim_tp.scad` do not render (they still
> call `tower()` / `carrier()`, retired in rev D).

Covers the **whole tube-mounted system**, not just this directory: the rev-B
platform, the two mirror rail clamps and their caps, the hanging ESP32 carrier,
and the **Jetson Nano on its own `slimrig_mounts/nano_tube_plate`** sliding into
the 54 mm under-plate corridor. The Jetson Orin plate is covered as a *separate
group* — see [Orin](#the-orin-is-not-co-mounted).

| | |
|---|---|
| Geometry authority | `make_tube_platform.scad`, `../slimrig_mounts/make_nano_tube_plate.scad`, `../slimrig_mounts/make_orin_tube_plate.scad` |
| Assembly scene (OpenSCAD) | `make_system_assembly.scad` + `asm_shim_*.scad` |
| Assembly B-rep / STEP | `cad_exchange/make_tube_platform_brep.py` |
| Verification | `cad_exchange/verify_assembly.py` |
| Renders | `renders/` |
| Datum | plate underside **z 0**, plate top z 7, tube axes z **−61.7** at x ±30, **+Y = north** (the end the Nano enters from) |

Nothing in the assembly files re-derives a dimension: the OpenSCAD scene reads
every number back out of the part files through the shims, and the B-rep script
transcribes them verbatim and then cross-checks its volume against the printed
`.stl`. **If a part changes, change its `.scad` and re-run both.**

---

## 1. Vertical stack (all heights above the plate top, z 7 absolute)

```
  z 66  ────────────  ZED-F9P top                       (RTK env 20)
  z 46  ────────────  RTK spacers Ø7×6 on the deck
  z 40  ══════════════  RTK TOWER DECK 48×50, 4 thick    (x −40..8, y 13..63)
  z 36  ─┬──────────  deck underside │ 5.0 CLEAR over the EG25
  z 31   │            EG25-G top                          (env 18)
  z 13  ─┴──────────  EG25 / FlyCatcher board undersides (spacers Ø7×6)
  z  7  ══════════════  PLATE TOP  94 × 134 × 7          fence rises to z 42
  z  0  ══════════════  PLATE UNDERSIDE — corridor ceiling
  z −4  ────────────  carrier backer
  z −13 ────────────  breadboard face / retainer bars
  z −30 ────────────  ESP32 + jumpers, bottom of the hanging assembly
  z −42.7 ──────────  Jetson Nano plate TOP  ┐ 53.3 mm stack over the tube top,
  z −49.7 ──────────  Jetson Nano plate BOT  ┘ 0.7 mm under the platform
  z −54.0 ══════════  TUBE TOP — corridor floor  (54.0 clear)
  z −61.7 ────────────  tube axis, Ø15.0, 60 c-c
  z −78.7 ────────────  rail clamp bottom
```

FlyCatcher is **not** under the deck (board north edge y 6.5 vs deck south
y 13) — it is 33 tall over the plate, above the 29 deck seat.

---

## 2. Printed parts — jobs, time, material

PLA **Tough+**, OrcaSlicer CLI, brim profile, BED 60 / HOTEND 220 (the profile
in the existing `*_pla.gcode`). Times and volumes below are read straight out of
those gcode headers, not estimated.

| job | pieces | print orientation | time | cm³ | ≈ g (PLA 1.24) |
|---|---|---|---|---|---|
| `tp_plate` | 1 × plate | cargo face **down**, flat | 2 h 56 m 12 s | 36.22 | 45 |
| `tp_clamps` | 2 × mirror rail clamp | on the outboard face, troughs up | 3 h 47 m 11 s | 41.37 | 51 |
| `tp_tower` | 1 × RTK tower | deck face **down**, legs up | 1 h 09 m 36 s | 9.99 | 12 |
| `tp_carrier` | 1 × carrier + 2 × retainer bar | backer **down**, walls up | 2 h 10 m 05 s | 24.16 | 30 |
| `tp_fence` | 1 × cable wall | upright | 1 h 04 m 35 s | 10.45 | 13 |
| `tp_caps_spacers` | 4 × cap + 12 × spacer | insert face up / upright | 1 h 34 m 01 s | 14.26 | 18 |
| **platform subtotal** | | | **12 h 41 m 40 s** | **136.45** | **169** |
| `nano_tube_plate` (set) | 1 × plate + 2 × cap + 4 × spacer | outboard face down | 3 h 38 m 24 s | 36.15 | 45 |
| **system total** | | | **16 h 20 m 04 s** | **172.60** | **214** |
| `orin_tube_plate` (set, only if the Orin is built) | 1 × plate + 2 × cap + 4 × spacer | outboard face down | 4 h 10 m 54 s | 44.23 | 55 |

Zero supports in every job. All caps are the **canon SlimRig cap** and
interchange across the rsd / lilygo / nano / orin / platform spares pool —
verified numerically: identical 20 × 34 × 11 body, 1.0 pinch, Ø15.4 trough,
bolts at ±12.5.

**Material call.** This platform belongs to the **Pelican 1400 ground-station**
family (same validated Ø15.0 / 60 c-c SlimRig tube set), so PLA Tough+ is
appropriate and is what has been printed. If any of it is ever moved into the
aircraft or a hot cabin, **reprint in ASA/ABS/PC** — PLA's Tg (~60 °C) creeps
in a parked airframe. Keep the chamber under 40 °C on back-to-back PLA runs.

---

## 3. Heat-set inserts — M3, Ø4.4 × 6.0 bore, 0.6 chamfer

Counted off the model, not the old README (**the rev-A5 figure of 28 in
`README.md` is stale — rev B needs 46 in the platform alone**).

| part | inserts | where |
|---|---:|---|
| `tp_plate` — top face | 16 | 4 EG25, 4 FlyCatcher, 4 tower legs, 4 fence hold-downs |
| `tp_plate` — underside | 8 | hanging carrier |
| `tp_tower` deck | 4 | ZED-F9P |
| `tp_carrier` end-wall tops | 4 | 2 retainer bars |
| rail clamps (3 each) | 6 | plate lands on these |
| caps (2 each × 4) | 8 | cap clamp bolts |
| **platform total** | **46** | |
| `nano_tube_plate` | 4 | Jetson Nano |
| nano caps (2 each × 2) | 4 | |
| **system total** | **54** | (+8 more if the Orin plate is built) |

---

## 4. Fasteners — **read the length column, it is not the old BOM**

Every counterbore in this family is **CB_H = 3.5 deep**. The screw length has to
be measured from the *counterbore floor*, not from the part's top face; the
lengths in `README.md` were computed as "material + insert depth" and therefore
run **3.5 mm long wherever the head is recessed**. A screw longer than the
available depth bottoms in the brass and the joint never clamps.

| joint | qty | material under the head | + insert | available | **use** | old BOM | engagement |
|---|---:|---:|---:|---:|---|---|---:|
| rail cap bolts (through the 19 rail → cap) | 8 | 15.5 | 6.0 | 21.5 | **M3×20** | M3×25 ✗ | 4.5 |
| plate → rail top (through the 7 plate) | 6 | 3.5 | 6.0 | 9.5 | **M3×8** | M3×12 ✗ | 4.5 |
| RTK tower legs (deck 4 + leg 29) | 4 | 29.5 | 6.0 | 35.5 | **M3×35** ✓ | M3×35 ✓ | 5.5 |
| cable-wall hold-downs (3.0 flange) | 4 | (see note) | 6.0 | 9.0 | **M3×8 + Ø9 penny washer** | M3×10 ✗ | 5.0 |
| carrier → plate underside (4 backer) | 8 | 0.5 | 6.0 | 6.5 | **M3×6** | M3×12 ✗ | 5.5 |
| retainer bars → carrier walls (4 bar) | 4 | 0.5 | 6.0 | 6.5 | **M3×6** | M3×10 ✗ | 5.5 |
| EG25-G + FlyCatcher cargo (board 1.6 + spacer 6) | 8 | 7.6 | 6.0 | 13.6 | **M3×12** ✓ | M3×12 ✓ | 4.4 |
| ZED-F9P on the tower deck | 4 | 7.6 | 6.0 | 13.6 | **M3×12** ✓ | M3×12 ✓ | 4.4 |
| nano plate cap bolts (station 12 + plate 7) | 4 | 15.5 | 6.0 | 21.5 | **M3×20** | M3×25 ✗ | 4.5 |
| Jetson Nano board | 4 | 7.6 | 6.0 | 13.6 | **M3×12** ✓ | M3×12 ✓ | 4.4 |

All M3 socket-head cap screws (head Ø5.5 ≤ CB Ø6.2, head height 3.0 ≤ CB 3.5).
4.4 mm of thread in a brass heat-set is 1.47 × D — adequate; anything longer
bottoms (M3×14 would need 6.4 of a 6.0 bore).

**Fence washer note:** the 4 cable-wall hold-down counterbores are 3.5 deep in a
**3.0 thick** flange, so they cut the flange through — there is no head seat at
all (verified as material volume: 0.000 mm³ inside Ø6.2 over the full flange
height). Use a **DIN 9021 M3 penny washer, Ø9 OD** — it matches the Ø9 flange
and bears on the full remaining ring (r 3.1 → 4.5, 33.4 mm²). A DIN 125 Ø7
washer is **not** enough: it would bear on a 0.4 mm-wide ring, 8.3 mm², which an
M3 preload crushes straight into the PLA. Do not fit these screws bare.

**Other hardware**

| item | qty | note |
|---|---:|---|
| printed spacer Ø7 × 6 (Ø3.4 bore) | 12 platform + 4 Nano = **16** | EG25 ×4, FlyCatcher ×4, ZED-F9P ×4, Nano ×4 |
| SMA bulkhead jack, Ø6.5 panel hole | 3 | fence, y 44 / 16 / −12, z 17 above the plate top; 2.5 panel < 4.0 max |
| zip ties | 10 pairs | 5 zip columns in the fence at y 52/34/2/−26/−52, holes z 21 and 27 |
| Ø12 washer (or omit the bolt) | 1 | **west middle plate→rail bolt (−40,−19)** — see Findings #1 |
| SlimRig tube, Ø15.0 | 2 | **≥ 190 mm** for platform + Nano — the tube-engaging features only span 115 mm (rail south −40.4 → nano station north 74.7), but the Nano must be pressed on **north of the platform** (centre y ≥ 105) and slid in, so the tube has to reach ≈ y +132. **≥ 320 mm** if the Orin joins |
| M3 penny washer Ø9 (DIN 9021) | 4 | fence hold-downs |

---

## 5. Build order

Insert every heat-set **before** anything is bolted together (46 in the
platform, 8 in the Nano plate). Canon: tubes clamp first, cargo last.

1. **Rail clamps onto the tubes.** Each rail is a free body: push it sideways
   onto its tube (troughs open inboard) and slide it to the keep-out band
   **y −40.4 … +14.7**. Fit the two caps per rail *inboard* of the tube and draw
   them up with **4 × M3×20 per rail, driven from OUTBOARD** — west rail from
   the west, east rail from the east, both open air. The 1.0 mm pinch gap
   between cap face and rail face is the clamp; it must still exist when
   torqued.
2. **Plate onto the rails.** 6 × M3×8 from above into the rail-top inserts,
   flush in the counterbores. *Fit the west (−40,−19) bolt with a Ø9 washer* —
   its counterbore is destroyed by a lightening hole (Findings #1).
3. **Cable wall (fence).** 4 × M3×8 + Ø7 washers at x 42, from above.
   Do this **before** the FlyCatcher — the two south screws (42,−52) and
   (42,−38) end up under the FlyCatcher board with only 6.5 mm of driver room.
4. **Hanging carrier**, from below: 8 × M3×6 into the plate-underside inserts
   (heads sit inside the pocket). Then drop the breadboard onto its adhesive
   back into the 56 × 84 pocket, then the **2 retainer bars**, 4 × M3×6. The
   bars are the positive retention — the adhesive alone is not (house rule).
5. **EG25-G**, landscape at (0, 38): 4 spacers + 4 × M3×12. **Before the
   tower** — the tower bridges over it and its two west screws end up with only
   21.4 mm of headroom under the deck.
6. **FlyCatcher**, portrait at (14, −30): 4 spacers + 4 × M3×12. **After steps
   2 and 3** (it covers the east plate→rail bolts and the two south fence
   screws).
7. **RTK tower**: legs over the EG25, 4 × M3×35 from the deck top into the
   plate inserts.
8. **ZED-F9P** on the deck: 4 spacers + 4 × M3×12. Do this **last** on the
   platform — it covers all four tower-leg heads.
9. **Jetson Nano** — the one sequence that cannot be reordered:
   1. Press the nano plate down onto the tube pair **north of the platform**
      (its troughs open downward, so it cannot be pressed on at its final
      station — the platform is above it there).
   2. Fit its 2 caps and 4 × M3×20 **finger tight only**.
   3. Slide the whole plate **south** along the tubes until its south edge
      lands on the rail north faces at **y = 14.7**. That is the mechanical
      stop — the full 52.3 mm insertion, putting ~54 mm of the 80 mm board
      under the platform.
   4. Torque the 4 cap bolts. Their heads are flush in the nano plate's top
      face at **y = 52.7, x = ±17.5 / ±42.5**, now 42.7 mm below the platform —
      use a short-arm 2.5 mm hex L-key working up through the corridor from the
      north. **The Nano board must not be fitted yet.**
   5. Fit the 4 spacers and the Nano board, 4 × M3×12 (open sky from above,
      north of the platform edge only for the outer pair — plan on the L-key).
10. **Cables.** 3 SMA bulkheads through the fence, u.FL runs tied at the 5 zip
    columns. The corridor keeps the full 54 mm everywhere except under the
    carrier footprint (x −31…31, y −91…9), where 24 mm remains.

---

## 6. Service chains — measured, not guessed

`verify_assembly.py` sweeps a Ø9 driver column up from every top-driven head and
reports the first obstruction. Result:

| fastener | clear above the head | blocked by | to service it |
|---|---:|---|---|
| rail cap bolts (8) | open air, outboard | — | always reachable, platform and Nano fitted |
| plate → rail, west column (−40, −29/−19/−9) | open sky | — | free |
| plate → rail, east column (+40, −29/−19/−9) | **9.5 mm** | FlyCatcher board | FlyCatcher off |
| fence hold-downs (42, +20) and (42, +57) | open sky | — | free |
| fence hold-downs (42, −52) and (42, −38) | **6.5 mm** | FlyCatcher board | FlyCatcher off |
| tower legs (4) | **9.5 mm** | ZED-F9P board | ZED-F9P off |
| EG25 east screws (+35.4, ·) | open sky | — | free |
| EG25 west screws (−35.4, ·) | 21.4 mm | tower deck | stubby/ball driver, or tower off |
| FlyCatcher (4) | open sky | — | free |
| ZED-F9P (4) | open sky | — | free |
| carrier → plate (8) | heads inside the pocket | breadboard | retainer bars off, breadboard out |
| nano plate caps (4) | 42.7 mm, under the platform | Nano board | Nano board off, short-arm L-key |

**Full teardown order:** ZED-F9P → tower → FlyCatcher → EG25 → fence →
retainer bars → breadboard → carrier → plate off the rails → rail caps → rails
off the tubes. The Nano comes off independently at any time (board off → caps
loose → slide north).

---

## 7. The Orin is not co-mounted

The Orin plate is 102 mm on the tube axis. Everything from y +14.7 (rail north
face) down to y −91 (carrier south edge) is occupied, and under the carrier the
corridor is 24 mm — less than the Orin's own 17.3 mm seat stack plus a board.
The first station that does not interfere is **north edge on y = −91, centre
y = −142**, which needs a tube run of **283.7 mm** from the Orin's south edge to
the Nano's north edge, plus end margin — call it a **330 mm rail pair**. No repo
file states the tube length, so:

* the default assembly scene and STEP **leave the Orin out**;
* `part="orin_option"` / `tube_platform_assembly_with_orin.step` draw exactly
  that co-mounted case with the tubes extended (render:
  `renders/asm_orin_option_plan.png`). Interference-checked clean at that
  station.

Treat it as a separate group until someone measures the actual rails.

---

## 8. Findings this assembly exposed

Cross-revision drift between parts designed at different times. **None of these
is fixed here** — no part `.scad` or gcode was touched.

1. **A Ø8 lightening hole destroys a plate→rail bolt.** `LIGHTEN` has a hole at
   **(−40, −20)**; rev B moved the rail bolts to y −29/−19/−9, putting one at
   **(−40, −19)** — 1.0 mm away. The Ø3.4 bolt hole is entirely inside the Ø8
   hole (web −4.7) and the Ø6.2 counterbore is swallowed too (web −6.1). That
   bolt has **no head seat**: 1 of the 3 west plate→rail bolts. The east column
   is unaffected (asymmetric — a clear oversight, the lightening hole is a
   leftover from the pre-rev-B bolt column). *Field fix: Ø9 washer. Proper fix:
   move the hole to (−40, −44) or delete it, plate reprint 2 h 56 m.*
   The `.scad` assert suite checks insert-to-insert and insert-to-bolt spacing
   but never checks the lightening holes against anything.
2. **The fence hold-down counterbores cut through the flange.**
   `cylinder(d=CB_D, h=CB_H+2)` starting at `3 - CB_H = −0.5` removes the full
   3 mm flange over Ø6.2 at all four screws. Measured: 0.000 mm³ of material
   inside Ø6.2. *The fence is on the printer now — fit Ø7 washers rather than
   reprinting.*
3. **Screw lengths run 3.5 mm long wherever the head is counterbored** — see
   §4. Worst case is the carrier: M3×12 into 6.5 mm of available depth would
   drive 5.5 mm of screw into a plate that only has 1.0 mm of material above
   the insert bore.
4. **The FlyCatcher's SE spacer touches the fence's south flange.** Ø7 spacer at
   (38.5, −59) vs the Ø9 fence flange at (42, −52): centres 7.826 apart,
   radii sum 8.0 → **0.174 mm interference, 0.573 mm³** shared volume. The only
   solid-on-solid interference in the whole assembly. The `.scad` assert that
   should catch it compares **insert** diameters (Ø4.4), not the installed
   Ø7 spacer and Ø9 flange, so it passes with 3.43 mm to spare. *Fix: chamfer
   or scallop one spacer, or move the fence screw to y −50.*
5. **A FlyCatcher insert has a 1.23 mm web to a lightening hole.** Insert at
   (−10.5, −1.0) vs the Ø8 hole at (−8, −8). Under the house minimum of 1.5 mm
   around a heat-set — the brass will likely break into the hole when it is
   pressed in. Watch it during insert installation.
6. **`make_tube_platform.scad`'s own `assembly()` view mis-places the 4 caps.**
   `rotate([0,0,90]) rotate([90,0,0]) rotate([0,90,0])` resolves to
   (x,y,z)→(−x,z,y): the cap's trough runs *across* the tube instead of along
   it, and the cap lies flat 11 mm north of its bolt line. Display only —
   `part="clamps"` and `part="caps_spacers"` are unaffected and the printed caps
   are correct — but it hides the fact that the mated cap reaches z −44.7,
   9.3 mm up into the Nano corridor, and that its north face lands **exactly**
   on the Nano's stop plane (y 14.7, 0.000 mm margin). The correct placement is
   `translate([TUBE_X−PINCH, cy, TZ]) rotate([−90,0,90])`; the assembly scene
   uses that, and OpenSCAD and OCCT independently agree on the result.
7. **The Nano board overhangs its plate 2 mm to the south**, i.e. 2 mm past the
   rail stop face at y 14.7, down to y 12.7. It clears because the board
   underside sits 8.0 mm above the rail top. `make_tube_platform.scad`'s ghost
   draws that board 2 mm *north* of the plate edge instead of centred, so the
   overhang does not appear in the part file's own view.
8. **Soft CONFIRMs inherited, still open:** the Nano board+SoM+heatsink envelope
   of **36 mm** (the memory bank has "Orin heatsink 36" measured, not the
   Nano's) — the whole 0.7 mm corridor margin rides on it; the EG25 board
   estimate 76 × 30 around its measured 70.80 × 24.21 holes; the breadboard
   assumed half-size 400-point 83 × 55 × 9; the relay module, still deleted and
   unplaced.

---

## 9. Verification (2026-08-08)

`.venv/bin/python cad_exchange/verify_assembly.py`

| check | result |
|---|---|
| B-rep sanity | 8/8 parts: one closed, `BRepCheck`-valid solid, **zero non-analytic faces** |
| volume vs the printed OpenSCAD meshes | worst deviation **0.095 %**, sign and magnitude fully explained by `$fn=52` faceting |
| interpenetration, 528 body pairs | **1** hit: the 0.573 mm³ spacer/fence touch (Finding #4) |
| Nano corridor | stack 53.3 over the tube top vs 54.0 → **0.700 mm**, measured solid-to-solid |
| Nano insertion stop | 0.000 to both rails and both north caps — flush by construction |
| tube vs every trough | 0.200 mm (Ø15.4 trough over Ø15.0 stock) everywhere |
| RTK deck over the EG25 | **5.000 mm** vertical; legs straddle at 2.500 in Y, by design |
| plate bore proximity | 2 breaches, 1 thin web (Findings #1, #5) |
| fastener stacks | 5 joints over-length, 1 with no head seat (Findings #2, #3) |
| driver access | 4 blocked heads → the service chains in §6 |

---

## 10. Regenerating everything

```bash
cd /Users/sic_intel/Documents/GitHub/michelangelo/tube_platform

# renders
openscad -o renders/asm_iso.png       -D 'part="assembled"' --imgsize=2200,1650 \
  --camera=0,4,-4,60,0,240,700 --projection=o --colorscheme=Tomorrow make_system_assembly.scad
openscad -o renders/asm_exploded_iso.png -D 'part="exploded"' --imgsize=2200,1800 \
  --camera=0,10,4,62,0,240,900 --projection=o --colorscheme=Tomorrow make_system_assembly.scad
openscad -o renders/asm_elevation.png -D 'part="elevation"' --imgsize=2400,1300 \
  --camera=0,6,-8,90,0,270,480 --projection=o --colorscheme=Tomorrow make_system_assembly.scad
openscad -o renders/asm_plan.png      -D 'part="plan"' --imgsize=1500,2000 \
  --camera=0,8,0,0,0,0,620 --projection=o --colorscheme=Tomorrow make_system_assembly.scad
openscad -o renders/asm_orin_option_plan.png -D 'part="orin_option"' --imgsize=1300,2400 \
  --camera=0,-40,0,0,0,0,880 --projection=o --colorscheme=Tomorrow make_system_assembly.scad

# STEP assembly + per-part analytic STEP/STL
../.venv/bin/python cad_exchange/make_tube_platform_brep.py
# every check above
../.venv/bin/python cad_exchange/verify_assembly.py
```

No printing is triggered by any of this. The `*_pla.gcode` in this directory is
untouched.
