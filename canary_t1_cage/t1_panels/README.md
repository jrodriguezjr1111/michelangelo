# t1_panels — long-face panels for the lower bay (2026-09-27)

**Owner, verbatim:** "let's design 2 panels, each 15.75 in by 4.75 in for the cage modeled after the snapshot."

- **Styling reference:** the AI concept render (image 37). It is not a drawing.
- **Fit reference:** photo 38, the cage as built.

**Not printed, not sent.** One segment was sliced for a PLA fit check (below); the gcode is in the session scratchpad.

| file | what |
|---|---|
| `make_t1_panels.scad` | family engine. `panel = upper\|lower`, `segment = L\|C\|R\|all`, `part = body\|accents\|badge\|louver\|splice`, `view = front\|back_seg\|exploded`, `taglines` (default **false**) |
| `panels_on_cage.scad` | both panels on the cage in photo 38's arrangement. Uses `t1_concept_E.scad`, `t1_stack` and this file **read-only**, and adds the as-built mid-rail rectangle |
| `build_t1_panels.py` | STL export on the manifold backend (fails on any warning or assert), renders, and the volume/mass/time table |
| `brand/canary-wordmark.svg` | the **tracked, public** CANARY wordmark, copied from `canary/baseline-service/public/brand/`. Glyph outlines only, with no enclosed counters, so the letters cut through with no islands |
| `stl/` | 6 body segments, 2 splice sets, 2 accent sets, badge, CO cassette. Every part is **print-oriented, face down** |
| `renders/` | `upper_front`, `lower_front`, `panels_on_cage`, `seam_back_lower` (seam joint + inserts), `accents_exploded_upper/_lower` |

## What photo 38 says, and why the panel is 130 tall, not 120.65
> **SUPERSEDED 2026-09-29 by the straight-on photo 39 measurement (section "Measured on photo 39" at the end):** deck->mid pitch is **125.5**, not ~110. Rev A's 130 mm height and z 120 hole row do not fit the frame as built; use rev B.

- **Faces:** the panels go on the **long faces of the lower bay, between the deck rail and the mid rail**. The front one
  faces the case I/O side, where the camera is. **Confirmed from the photo.**
- **Rail pitch:** the flat corner gussets sit **on the front faces** at every rail/post corner. Their bolts are on a
  20 mm pitch, which gives a scale of 55-70 px per 20 mm. That puts the **deck-rail to mid-rail slot-centre pitch at
  about 110 mm** (107-117 across both ends of the frame).
- **Height consequence:** holes on the slot centrelines, 10 mm from each edge, make the panel **130 mm (5.12 in)**,
  flush with the rails' outer edges. The owner's **4.75 in (120.65)** only works if the measured pitch is **104.65 or
  less**, keeping the 8 mm minimum edge for an M5 counterbore. So `H` is derived from `MID_SLOT_Z - DECK_SLOT_Z`,
  `OWNER_H` is kept, and the model asserts the edge distance.
- **Standoff:** the panel stands **6.4 mm** proud of the rail faces so it clears the gussets and their button heads.
  It bears on the rails only through Ø14 bosses at the bolts and the strap pads. The perimeter skirt is relieved at the
  gussets.

## Architecture
| | upper panel (front, I/O face) | lower panel (back face) |
|---|---|---|
| left | yellow "<" end bracket, hex field | bird plate (**PLACEHOLDER**), yellow "\\" slash, hex field |
| seam L (x 112) | hidden under the yellow "\\" slash | hidden under the yellow bar |
| centre | **CANARY badge**: black octagon flange, wordmark **cut through**, yellow backer pressed in behind, 4 snap catches | **CO cassette**: louver bezel + pocket box carrying the existing `co_sensor` tray |
| seam R (x 288) | under the "/" slash | under the bar |
| right | hex field, yellow ">" bracket | hex field, yellow ">" bracket |
| hex (5 AF, 1.6 web) | **22.9 + 21.9 = 44.8 cm²** | **8.4 + 24.0 = 32.5 cm²** (+ 22.4 cm² louver intake through the CO tray) |

Hex areas are echoed per field (R4.2). **The upper panel goes on the face nearer the Orin**, and the model asserts it
has ≥ 32 cm². The lower panel happens to clear 32 cm² as well. The Orin's own grille is on top of its case and its side
vents face the end faces, so these hex fields are **bay ventilation**, not a ducted fan intake.

**Segments and seams (R6.4: 400 > 281 bed).**
- **Split:** each panel is three pieces: L (120-126 wide), C (196-204 wide), R (120-126 wide), all 130 tall.
- **Seam path:** each seam is a **jogged polyline, never a straight line**. It is **hidden under the yellow
  bar/slash** (the accent is pressed across both halves and doubles as a key), and through the rail bands it sits in
  the root of a **45° V-groove panel line**.
- **Behind the face:**
  - a **2 mm tongue-and-groove** at mid-thickness keeps the faces flush;
  - a **printed splice plate** (3.2 mm) spans the seam with **4 × M3 into heat-set inserts** from the back (2 per
    side, 4 mm deep, leaving a 1.6 mm face skin). The model asserts the plate covers every insert.

**Mounting.** Six **M5 flush BHCS** (counterbore Ø10.4 × 3.2) go into T-nuts on the **rail slot centrelines**
(`DECK_SLOT_Z = 10`, `MID_SLOT_Z = 120`, both CONFIRM):
- two per rail at **frame x 82 and 324**, just inboard of the gussets;
- one per rail at **x 203**.

Strap-bearing pads behind the bottom band sit at **frame x 88 / 318**. The rev B cargo-strap loops at 100/306 are moved
clear of the seams, so a strap bears through the panel into the rail, not onto a floating skin.

**CO cassette: the louver is a real intake, and the stick swaps from outside (R1).**
- **Cassette:** the louver module is a removable cassette. A 159.6 × 84 bezel carries 5 louver slots with 45° lips,
  inlaid 0.6 text ("CARBON MONOXIDE SENSOR" / "AIR IN · DETECT · STAY SAFE"), and pockets for the yellow side brackets.
  Behind it, a **pocket box goes through a 145.6 × 50 window** in the C segment.
- **Tray mounting:** the box carries the **validated `co_sensor` rev 3 tray** (125.6 × 26.22 × 25.62, not a new CO
  holder).
  - It sits **lid toward the louvers** with a 1.5 mm air gap and is screwed **on its native ear pattern (45/95 × ±17.11)**.
  - The screws are M3, driven from the back into inserts in two ledges.
  - The USB tail exits the box's +X end.
- **Air path:** in through the louvers, over the cell, out through the tray's gills and floor vents into the bay.
- **Swap:** loosen **one yellow captive M4 thumbscrew** · slide the cassette 3 mm toward the thumbscrew, which releases
  the hook tab behind the window's opposite edge · pull it out and unplug the USB. The window is 3 mm oversize on the
  hook side so that slide exists. The bezel covers all of it.
- **Depth:** the cassette reaches **31 mm behind the face, 19 mm past the rail plane**. It is therefore on the back face,
  away from the I/O cables.

**Brand and accents.**
- Yellow appears **only as separate snap-in parts**, with a 0.2 mm press fit (0.1 per side) and a 0.4 lead-in step
  (R7.3): end brackets, slashes/bars, the bird, the cassette side brackets and the badge backer.
- The **wordmark is real** (the tracked SVG).
- The **bird is a PLACEHOLDER**. The only bird art is PNG, in the gitignored `canary/company/brand/`, and was
  deliberately not copied into this repo. Swap it for a vector when one exists.
- **Taglines** "SENSE FURTHER" (badge) and "MONITOR / PROTECT / ENDURE" (bird plate) are behind `taglines=true`,
  **default OFF**, pending owner approval under R8 (capability names only).

## Parameters (`make_t1_panels.scad`)
| name | value | tag | note |
|---|---|---|---|
| `L` | 400.05 | owner | 15.75 in |
| `DECK_SLOT_Z / MID_SLOT_Z` | 10 / 120 | EST · CONFIRM | photo 38 pitch ~110 |
| `H` | 130 (derived) | — | owner 120.65 needs pitch ≤ 104.65 |
| `EDGE` | 10 | DSN | hole row to edge |
| `GUS_L / GUS_H / GUS_T / GUS_HEAD` | 70 / 70 / 3.2 / 2.8 | EST · CONFIRM | front-face corner gussets |
| `STANDOFF` | 6.4 | derived | gusset + head + 0.4 |
| `T` | 5.6 | DSN | 14 lines |
| `CH` | 1.2 | house | 45° bed-edge chamfer |
| `M5B / CB_D / CB_H / BOSS_D` | 5.4 / 10.4 / 3.2 / 14 | house (t1_faceplate) | |
| `XS` | 112 | DSN | seam station; right seam at L − 112 |
| `TNG` | 2.0 deep × 1.6, 2.0 below the face | DSN | tongue-and-groove, 0.2 clearance |
| `INS3_D / INS3_DEP` | 4.4 / 4.0 | house bore, short insert | M3 × 4 heat-set (CONFIRM part) |
| `INS4_D / INS4_DEP` | 5.6 / 6.0 | house | cassette thumbscrew, on a 3 mm back boss |
| `HEX_AF / HEX_WEB` | 5.0 / 1.6 | brief / 4 lines | |
| `ACC_D / ACC_FIT` | 1.6 / 0.1 per side | DSN | accent pocket depth / press fit |
| `FIELD_GAP / FIELD_GAP_ACC` | 12 / 7 | DSN | hex to seam accent (insert room) / to other accents |
| `STRAP_X` | 88 / 318 | DSN | strap bearing pads |
| `CO_TRAY, CO_EAR, EAR_T` | 125.6×26.22×25.62, 45/95 × ±17.11, 3 | MEAS / MEAS / EST | from `co_sensor/make_co_tray*.scad` |
| `BZ` | 3.2 | DSN | raised bezel/flange thickness |
| `HOOK` | 2.6 | DSN | cassette hook reach |
| `WIN_UP, BADGE, WM_W` | 112×50, 124×62, 92 | DSN | badge window, flange, wordmark width |
| `MAXSPAN` | 10.4 upper / 16 lower | echoed | widest face-side roof (counterbore annulus / bird pocket) |

## Print plan, mass, time
Every body segment prints **face down** for the bed finish, with no supports. Every face-side recess is a short roof
(MAXSPAN echoed). Bezel edges are 45° chamfers. There are no islands (the wordmark letters and hex cells are through-cuts).

| plate | parts | CAD cm³ | PLA fit-check | ASA flight (≈ 1.2×, EST) |
|---|---|---|---|---|
| 1 | upper L + upper R (black) | 144 | ~10.7 h | ~13 h |
| 2 | lower L + lower R (black) | 150 | ~11.2 h | ~13.5 h |
| 3 | upper C + upper splices (black) | 121 | ~9.0 h | ~11 h |
| 4 | **lower C** + lower splices (black) | 110 | **7 h 02 m for C alone (sliced)** + ~1.2 h | ~10 h |
| 5 | CO cassette + badge (black) | 88 | ~6.6 h | ~8 h |
| 6 | all yellow accents + badge backer (yellow) | 16 | ~1.2 h | ~1.5 h |
| **total** | both panels | **631** | **~47 h** | **~57 h** |

- Hours come from the **real slice ratio (0.074 h per CAD cm³ at these settings)**. Every plate is under the ~12 h
  cap (R6.4).
- **Mass (ASA):** upper panel ~277 g, lower ~297 g, excluding the CO tray. **~0.57 kg for the pair.**
- **ASA flight** also needs the house guards and the chamber profile.

**PLA fit-check slice (done, not started): `lower_body_C.stl`.** This uses the house PLA standard, the same pattern
as `vib01_node/slice_revD.py` / `t1_faceplate`:
- OrcaSlicer CLI with `--load-settings "Qidi X-Plus 4 0.4 nozzle;cw_mes/qidi_xplus4_brim.json"` and
  `--load-filaments "Bambu PLA @Qidi X-Plus 4 0.4 nozzle.json"`.
- The **printer's PRINT_START macro is kept**, because it does the homing, mesh and purge.
- Only the CLI's wrong preamble values are sed-patched. The CLI wrote `BED=35 HOTEND=200` and a mid-print `M104 S210`;
  these become `PRINT_START BED=60 HOTEND=220`, `M140 S60`, `M104 S220`. The `S0` shutdowns are untouched.

Process overrides:
- walls 4 (the hex webs are 4 lines), 4 top / **4 bottom** shells (**GUARD 1: ≤ 6**), gyroid 40 %, brim 6;
- **`max_bridge_length = 21`**, from the model's `MAXSPAN = 16` + 5 (**GUARD 2**).

Results:
- **7 h 02 m, 26.9 m / 64.7 cm³ PLA (~80 g)**, 60 layers.
- Checked by grep:
  - the only PRINT_START line is `PRINT_START BED=60 HOTEND=220 CHAMBER=0 EXTRUDER=0`;
  - every non-zero heater command is `M140 S60` / `M104 S220`;
  - there is no `M190`/`M109`.
- `gcode_check.py`: all checks pass.
- Gcode: `<session scratchpad>/slice_lowerC/lower_body_C_PLA.gcode`, made by `slice_house.sh` in the same folder.
  **Not sent. The owner authorises every print.**
- The earlier `plus4_print.py` gcode (hand-written M190 S70 / M109 S215 preamble) is renamed
  `SUPERSEDED_plus4print_preamble_DO_NOT_PRINT.gcode`.

## Stiffness: they are a shear skin, not structure
Per panel, `G·t·L/H` is ≈ 0.7 GPa × 5.6 × 366 / 110 ≈ **13 kN/mm** for the skin itself. The joint cannot deliver that:
six M5 on 6.4 mm standoff bosses in ASA bring it down to roughly **2-5 kN/mm of racking stiffness** (EST), a secondary
path in parallel with the metal corner gussets the frame already has. Panels **stiffen and quiet** the lower bay. They
are **not** in the restraint path: belt and straps stay on metal, and the strap pads only stop a strap crushing the skin.

## CONFIRM (measure / decide)
1. **Rail slot pitch** (deck to mid rail). ~110 from the photo sets **H = 130**. If calipers say ≤ 104.65, set
   `H = OWNER_H` (4.75 in).
2. **`DECK_SLOT_Z` / `MID_SLOT_Z`** absolute, and whether the mid rail is 20-2020 like the deck.
3. **Corner gussets:** leg lengths, thickness, button-head height, and their bolt positions. These set `STANDOFF` and
   the corner-hole x (82 / 324).
4. **Mark source:** the bird is a PLACEHOLDER. A vector (SVG) of the Canary bird is needed; the PNGs in `company/` stay
   there.
5. **Taglines** "SENSE FURTHER" and "MONITOR / PROTECT / ENDURE": owner approval (R8). They are off until then.
6. **Which face gets which panel.** The model puts the badge on the I/O face and the CO cassette on the back face. The
   back face needs **≥ 25 mm clear** behind its centre.
7. **Core access (R1).** The panels close the lower bay's long faces, so a case swap means taking the front panel off
   (6 × M5). If the Core is opened as often as in T0, switch that panel to **captive knurled thumbscrews** (Ø13
   counterbores). This is not yet modelled.
8. **Strap loops moved to frame x 88 / 318**, if the long-member straps from rev B are still the restraint.
9. **Heat-set parts:** M3 × 4 short inserts (4.4 bore) and M4 × 6. Also the CO-tray ear thickness (`EAR_T` 3 EST).
10. **`t1_stack` vs the as-built frame.** The as-built lower bay is only ~90 mm clear between rails, and photo 38 shows
    the two cases **side by side**. The 174 mm vertical `t1_stack` does not fit under the mid rail. The stack needs a
    single-level variant, or the owner decides the arrangement.

## Verification performed
- Every part and view renders with **all asserts passing**:
  - hole edge distance;
  - segment ≤ 281;
  - upper hex ≥ 32 cm²;
  - corner boss clear of the gusset;
  - bezel clear of the seam bars;
  - tray ears inside the box;
  - M3/M4 insert skins;
  - splice covers every insert.
- **Manifold backend** exports all 14 STLs cleanly (`build_t1_panels.py`). Volumes, bboxes and masses come from the STLs.
- One PLA slice with the guards applied and the preamble verified literally (above). **No prints.**

---
# LOWER (CO) panel — rev B (2026-09-28)

> **Updated 2026-09-29:** rail numbers re-measured on photo 39 (see "Measured on photo 39" below). The model now uses rows z 10 / 135.5 (flush: 0.55 proud), gussets cleared by 7.85 (no notches on a 444.5 face), hex 42.4 cm², ~227 g. The figures in this section are the 2026-09-28 values, and its gcode is **stale**.

> Owner, verbatim: "let's redesign the CO panel as one panel with the same vented pattern. let's remove the canary
> icon and make both sides symmetrical. also, the dimensions of this panel should be 12 inches by 5.75 inches to
> accommodate the gussets."

**Rev switch = a new file.** `make_t1_panels_revB.scad` `use`s the rev A helpers (hex fill, strokes, V-grooves,
accent fit, CO-tray reference), so `make_t1_panels.scad`, the upper panel and every rev A output are untouched. Also
new: `panels_on_cage_revB.scad` and `build_t1_panels_revB.py`. Parts: `stl/lower_revB_half.stl` (plus a convenience
`lower_revB_half_mirror.stl`), `lower_revB_cassette.stl`, `lower_revB_accents.stl`, `lower_revB_splice.stl` (2 splice
bars + 2 loose splines). Renders: `lower_revB_front`, `lower_revB_back_seam`, `lower_revB_exploded`,
`panels_on_cage_revB` (rear three-quarter view: rev B replaces rev A's lower panel on the back face).

## Size, gussets, rails
- **304.8 × 146.05 × 5.6**, sitting **flat on the rail faces, between the front-face corner gussets**. With no
  standoff, the face lands about level with the gussets' button heads.
- 304.8 is wider than the ~266 clear between 70 mm gusset legs, so the **four ends are notched round the gusset
  outlines** (+1.5 clearance): the L gusset at the deck rail, the T gusset at the mid rail, following their 45°
  hypotenuses. The ends become arrowheads. At full width the panel spans the rail gap between z 41.5 and 88.5 (frame).
- **Height:** 146.05 overlaps **both rails fully**. It is flush over both only if the **slot pitch is 126.05**
  (146.05 − 20). Photo 38 estimates **~110**, which leaves the panel **16.05 above the mid-rail top**. The panel is
  bottom-aligned at the frame bottom so it never drops below the seat plane. The height stays parametric, and the
  pitch is still CONFIRM.

## Holes, open area
- **8 × M5 flush BHCS** (Ø10.4 × 3.2 counterbores) into T-nuts on the slot centrelines:
  - rows at frame z **10 / 120**, with edge distances 10 / 26.05;
  - x at frame **82, 153, 253, 324**, which is **4 per half**, so each half bolts to both rails by itself and the seam
    carries no mounting load.
- **Hex** (5 AF / 1.6 web): **85 + 85 cells = 36.8 cm²**, which meets R4.2 (≥ 32).
- **Louver:** **22.4 cm²** through the CO tray.

## Layout (strictly mirror-symmetric)
chevron | hex field | CO louver cassette | hex field | chevron.
- **No bird, no badge.** Yellow is only the two end chevrons, the two cassette side brackets and the **one
  thumbscrew**, which sits **on the centreline** at the top of the bezel.
- The cassette text is inlaid as before. **Taglines stay OFF.**

## Two identical mirrored halves (152.4 × 146.05 each)
- **Seam:** on the centreline, through the middle of the louver module.
  - Between z 23 and 107 it sits **under the one-piece cassette bezel**.
  - Above and below that it runs in the root of a **45° V-groove on the axis of symmetry**, so it reads as the design's
    centre line.
- **Joint:**
  - a **loose printed spline** (1.6 × 4) in grooves in *both* halves, which is what makes them true mirror images;
  - two **rear splice bars** (56 wide), below and above the window, on **4 × M3 heat-set inserts** (2 per bar,
    ±12 from the seam).
- **Cassette:** it spans the seam without depending on it.
  - **Two mirrored hooks** (x ±55, one on each half) carry its weight behind the window's bottom edge.
  - The **single M4 thumbscrew** passes the seam and threads into an **M4 insert in a boss on the top splice bar**, so
    the lock load crosses the seam through the splice.
  - To fit it: insert raised, drop 3 mm onto the hooks, tighten the thumbscrew.
  - The window is 145.6 × 51.5.
  - The same `co_sensor` rev 3 tray is carried the same way, on its native ears, lid to the louvers.

## Mass, print, slice
- **Mass:** 2 halves + cassette + accents + splice = **233 cm³ CAD, ~212 g ASA** (~245 g PLA). That is lighter than
  rev A's ~297 g.
- **Print plan:**
  - **half ×2**, one mirrored (slicer mirror-X, or use `_half_mirror.stl`), one per plate;
  - cassette on its own plate;
  - accents in yellow;
  - splice bars and splines together.
- **PLA fit-check slice (done, NOT started):** `lower_revB_half.stl`, run the house way by
  `<scratchpad>/slice_lowerRevB/slice_house_revB.sh`.
  - OrcaSlicer CLI with the machine profile + `cw_mes/qidi_xplus4_brim.json` + stock Bambu PLA.
  - The printer PRINT_START macro is kept. sed-patched from the CLI's `BED=35 HOTEND=200` / mid-print `M104 S210` to
    **`PRINT_START BED=60 HOTEND=220`, `M140 S60`, `M104 S220`**, with the S0 shutdowns untouched.
  - Guards: `bottom_shell_layers = 4` (≤ 6), `max_bridge_length = 15` (MAXSPAN 10.4 + 5),
    `dont_filter_internal_bridges = nofilter`, 4 walls / 4 top, gyroid 40 %, brim 6.
  - **6 h 54 m, 23.6 m / 56.8 cm³ PLA (~70 g)**, 28 layers.
  - Grep-verified. `gcode_check.py` passes.
  - Gcode: `<scratchpad>/slice_lowerRevB/lower_revB_half_PLA.gcode`.

## CONFIRM (rev B additions)
1. **Slot pitch: 126.05 (flush at 5.75 in) vs ~110 (photo).** This decides whether the panel stands 16 mm above the
   mid rail.
2. **Gusset outlines:** L at the deck rail and T at the mid rail, 70 legs with 45° hypotenuses (EST). The end notches
   follow them.
3. **Hole x positions** (frame 82 / 153 / 253 / 324) against the gusset bolts and the T-nuts that are free in the slots.

---
# Measured on photo 39 (2026-09-29): the as-built frame, straight on

Photo 39 is near-orthographic. The rulers were the flat gussets' **20 mm bolt pitch**, checked against the **20 mm
rail faces**, which agree within ~0.5 mm. The image has a clear vertical keystone: bolt pitch runs from 75-79 px at the
deck rail through 85-87 px at the mid rail to 94-96 px at the top rail. So each span was measured between bolt-row
centrelines and divided by the mean of the local vertical scales at its two ends.

| quantity | left end | right end | **taken** | earlier estimate |
|---|---|---|---|---|
| deck → mid slot pitch | 501 px / 3.99 = 125.6 | 517 / 4.13 = 125.3 | **125.5 ± 1.5 mm** | ~110 (photo 38, oblique: the verticals were foreshortened) |
| mid → top slot pitch | 389 / 4.50 = 86.4 | 383 / 4.51 = 84.9 | **86 ± 2 mm** | not measured before |
| long face, gusset edge to gusset edge | 437 (top) · 447 (mid) · 443 (deck) | | **~442 ± 5 → 17.5 in (444.5) taken** | 406 in the E model |
| gusset outlines | L: 62 along the rail × 60 up the post, legs ~20-22, hypotenuse (62,20)→(22,60) · T at the mid rail: 62 × ±30 about the slot, hypotenuses (62,±10)→(20,±30) | | **CONFIRM** | 70 × 70 at 45° |

What follows from these numbers:
- **The owner's 5.75 in is right.** 125.5 + 20 = 145.5, so a 146.05 panel lies flush over the deck and mid rails,
  standing 0.55 mm proud. The ~110 estimate was the error.
- **The owner's 12 in fits.** On a ~444.5 face a 304.8 panel clears 62 mm gusset legs by **7.85 mm** at each end. That
  is what "to accommodate the gussets" means, and on the measured frame the rev B end notches vanish, leaving 6 mm
  design corner chamfers. On a 406 face the notch logic would still cut arrowheads.
- **Frame width conflicts with the E study.** If the as-built long face is ~444.5, it differs from the 406 deck in the
  E study. That affects `LAYOUT_E` / rev C numbers too (CONFIRM).

`make_t1_panels_revB.scad` now carries these as `FACE_L 444.5`, `MID_SLOT_Z 135.5`, `TOP_SLOT_Z 221.5`, `GUS_RL 62`,
`GUS_PL 60`, `GUS_TH 30`, all CONFIRM. **The lower (CO) rev B was regenerated to them:**
- hole rows z 10 / 135.5 at panel x 24 / 100 / 204.8 / 280.8;
- hex **98 + 98 = 42.4 cm²**;
- ~227 g ASA.

**Its 2026-09-28 fit-check gcode is stale** (rails at z 120) and has been renamed
`STALE_rails-at-120_DO_NOT_PRINT_...gcode`. Re-slicing is one command (`slice_house_revB.sh`) once approved.

Rev A's wordmark sits ~12 mm high in its badge, because `import(center=true)` centres the SVG viewBox rather than the
glyphs. Rev A is left untouched; rev B recentres it (`WM_DY`).

---
# UPPER (CANARY badge) panel — rev B (2026-09-29)

This uses the same format as the lower rev B and lives in the same file (`panel="upper"`,
`placement="lowerbay"|"upperbay"`):
- 12 in wide, strictly symmetric, flush over both rails of its bay, sitting between the gussets;
- chevrons, hex fields and the **CANARY wordmark badge** (tracked SVG, cut through, yellow backer). No taglines;
- **two mirrored halves** with the centreline seam under the badge flange and in V-groove design lines;
- a loose spline and 2 rear splice bars on 4 × M3 inserts.

Renders on the as-built frame (`asbuilt_cage.scad`): `renders/upper_revB_{front,front34}_{lowerbay,upperbay}.png`.
STLs: `stl/upper_revB_{lowerbay,upperbay}_{half,badge,accents,splice}.stl`. **Nothing sliced, nothing printed.**

| | **(a) front of the lower bay** (over the case I/O faces) | **(b) front of the upper bay** (brow over the antenna level) |
|---|---|---|
| size | 304.8 × **146.05** (deck + mid rails) | 304.8 × **106** (mid + top rails, 86 pitch + 20) |
| fixing | **8 captive yellow M5 thumbscrews** on the rail rows (panel x 24 / 66 / 238.8 / 280.8), O-ring-captive, no tools | 8 × M5 flush BHCS (x 24 / 100 / 204.8 / 280.8): nothing behind it needs service |
| swap access | every cable and Core/case swap is behind it: loosen 8 thumbscrews, lift the panel off over the cable comb. That is ~40 s, but 8 hand steps, so it is on the edge of R1. Option: top row thumbscrews + bottom hook tabs to reach 4 steps (not yet modelled) | none needed |
| cable exit | **notch along the bottom edge**, 152.8 wide from the deck rail face to 14 mm above it, with **19 comb gaps** (6 mm at a 7.6 mm pitch, hooked teeth). The panel drops on over dressed cables, which leave downward past the deck rail | none (the coax stays inside) |
| what the vents do | **bay air only**, 45.5 cm² (+ 21.3 cm² through the notch). The case fans are on the **case tops**, not behind this panel, so the hex fields exchange lower-bay air around the I/O ends and are not fan intakes. R4.2 is met regardless | 31.2 cm². The upper bay is open top and sides, so these vents have **no thermal job**; they are look and weight |
| SMA / plug clearance | the panel back sits on the rail plane and nothing protrudes into the bay beyond the badge ring (≤ 1 mm). The case I/O faces are **~70 mm behind the front plane (EST, photo 39)**, and SMA plus right-angle plugs need ~25-35 mm, so **they clear**. CONFIRM with a ruler | n/a |
| RF | out of the antenna near field: the MA963 plate and dome are above the mid rail | **ASA in the dome's near field on one side.** The dome's front edge is ~70 mm behind the panel (≈ 0.37 λ at L1), and the brow reaches z 231.5, above the dome's phase centre (~z 170 EST). From the phase centre it covers the forward sector up to **~40° elevation**. 5.6 mm ASA (εr ~2.8, low loss) costs ~0.1 dB but adds a few degrees of carrier-phase delay and pattern ripple in that sector: an RTK bias the antenna calibration does not model. The metal top rail is already there |
| mass (ASA) | ~185 g (2 halves + badge + accents + splice) | ~152 g |
| print time (PLA class, 0.074 h/cm³) | ~15 h: halves 5.9 h each, badge 2 h, accents + splice 1 h | ~12 h |

> **Superseded 2026-09-28 by the owner's decision (section "FRONT PAIR" below): the lower bay gets the vented CO panel and the badge becomes the upper-bay brow.**

**Recommendation: (a), the badge panel on the front of the lower bay.**
- It covers what photo 39 shows needs covering: the cable nest and the I/O ends.
- It vents the right air, with no RF cost.
- The captive thumbscrews and the drop-on cable comb keep service tool-free.
- With the CO rev B on the back of the same bay, the lower bay is fully skinned and the antenna level stays open to the sky.

**(b) is not recommended.** It puts a dielectric slab in the GNSS antenna's near field on one side and protects
nothing that needs protecting. If the upper bay needs a face for looks, use an open frame there, not a skin.

## CONFIRM (upper rev B)
1. Frame long face ~444.5 (17.5 in) vs 406. This sets `FACE_L`, the end clearance, and whether notches are cut.
2. Gusset outlines (L 62 × 60, T 62 × ±30) and the deck→mid / mid→top pitches (125.5 / 86): caliper them.
3. Case I/O face setback from the front rail plane (~70 EST), for the SMA and plug clearance behind panel (a).
4. Captive thumbscrew part: knurled M5 × 16 with an O-ring or e-clip behind the panel. Or the 4-step hook variant.

---
# FRONT PAIR: the decided placement (owner, 2026-09-28)

> "the carbon monoxide sensor sits right behind the lower panel; I'm thinking remove Canary from the bottom panel,
> make it vented and leave the top panel with the Canary on it."

**Both panels go on the FRONT face.** Renders: `renders/front_pair_front.png` (photo 39's straight-on angle) and
`front_pair_front34.png`, via `asbuilt_cage.scad` with `bay="pair"`.

| | lower bay (deck → mid, pitch 125.5) | upper bay (mid → top, pitch 86) |
|---|---|---|
| panel | **CO rev B**: vented (hex **42.4 cm²** + louver **22.4 cm²**), **no wordmark, no bird**, symmetric | **CANARY badge brow** (`upper_revB_upperbay`): hex 31.2 cm², chevrons, badge |
| size | 304.8 wide; body to the mid slot centreline (135.5), ears to 144 (5.67 in) | 304.8 wide; body from the mid slot centreline to the top-rail top (231.5), ears down to 127 |
| fixing | `fix="8ts"` (default): **8 captive yellow M5 thumbscrews** · `fix="4ts_hooks"`: 4 on the mid-rail row + **2 T-slot hooks** in the deck-rail slot (render `lower_revB_front_4ts_hooks.png`) | 8 × M5 flush BHCS (nothing behind it needs service) |
| cable exit | **comb notch along the bottom edge**, x 76-228, deck rail + 10 mm, 20 gaps at 6 mm. The panel drops on over dressed cables | none |
| RF | none | ASA in the dome's near field, one side (see the table above). **Accepted by the owner; the ramp GNSS test covers it.** |

**The shared mid rail uses castellated ears.** Both panels land on the mid rail, which can't carry two full-height
skins. So each owns half its face (the edge sits on the slot centreline), and they interleave bolt ears that reach
18.5 mm over it: the `t1_faceplate` castellation.
- CO panel ears at x 24 / 66 (+ mirrors) carry its thumbscrews.
- Brow ears at x 45 / 110 (+ mirrors) carry its BHCS.
- Notches are ear + 1 mm per side.
- Thumbscrew seats are Ø11.6, leaving a 2.7 mm ear wall. All of this is asserted.

**Louver and the printed CO node.**
- Photo 39 puts the node's centre **5 ± 3 mm left of the frame centreline**. Its body spans image x 911-1051 against
  a frame centre of ~997 px, at the case-face depth where 132 mm = 388 px.
- The louver stays **centred**, which keeps the hex fields symmetric. The louver slots span ±56 mm, so the 48 mm node
  sits fully behind them either way. **Slide the node 5 mm right on its rod clamp** to centre it.
- The louver's back is at the rail plane. The node's front is **~50 mm behind it (EST)**; the design minimum is 10 mm.
  **CONFIRM with a ruler.**

**The cassette is optional.** `cassette=false` (default) fits a **plain louver insert**: the same bezel, louvers, text,
yellow side brackets and **single centreline thumbscrew**, on a 5.6 mm ring the size of the cassette box, with the same
two hooks. It is open behind to the rail-mounted node. `cassette=true` keeps the removable-tray version. Both use the
**same body, window and fitting**.

**Mass (ASA):** lower ~164 g (2 halves + plain louver + accents + splice), upper brow ~136 g. **~0.30 kg for the pair.**

**PLA fit-check slices (done, NOT started).** Both were run by `<scratchpad>/slice_pair/slice_house_pair.sh`:
- OrcaSlicer CLI + machine profile + `cw_mes/qidi_xplus4_brim.json` + stock Bambu PLA.
- The printer PRINT_START macro is kept. sed-patched from the CLI's `BED=35 HOTEND=200` to
  **`PRINT_START BED=60 HOTEND=220`**, `M140 S60`, `M104 S220`, with the S0 shutdowns untouched. Grep-verified.
- `gcode_check.py` passes both.

| part | guards | time | filament |
|---|---|---|---|
| `lower_revB_half.stl` (`fix="8ts"`; the body is the same with or without the cassette) | bottom shells 4, `max_bridge_length` 16 (MAXSPAN 11.6 + 5) | **6 h 12 m** | 20.5 m / 49.3 cm³ (~61 g) |
| `upper_revB_upperbay_half.stl` | bottom shells 4, `max_bridge_length` 15 (MAXSPAN 10.4 + 5) | **5 h 15 m** | 17.4 m / 41.9 cm³ (~52 g) |

Gcode: `<scratchpad>/slice_pair/{lower_revB_half_8ts,upper_revB_upperbay_half}_PLA.gcode`. Each half prints twice, with
the second one mirrored.

**Open CONFIRMs:**
1. **Frame long face:** ~444.5 (17.5 in) from photo 39, against 406 in the E model.
2. **Gusset outlines:** L 62 × 60, T 62 × ±30.
3. Also the node setback (≥ 10, EST ~50) and the captive thumbscrew part (knurled M5, Ø11 head, O-ring).
