# t1_sideplates — long-face side plates for the re-railed cage (2026-10-07)

**Owner:** new side plates "that elevate the look of the Cage".

The cage is rearranged (photos 47/48). The two aluminium cases are stacked, with their I/O on an **end** face. The
**long** faces now show:
- the case fins in row 2;
- the hub, the printed node and the MTi in row 1;
- the rods and clamps.

The dome and the V-mount battery sit outside the plates, at the top and the end.

**Files:**
- `make_t1_sideplates.scad`:
  - `side = "wordmark" | "plain"`
  - `row = 1 | 2 | 3`
  - `half = "L" | "R" | "full"` (`"full"` is row 3 only, 45° on the bed)
  - `part = plate | splice | spline | chevron`
  - `view = cage_wm | cage_plain | cage34 | exploded`
- `build_t1_sideplates.py`: STLs, renders, volumes. Pass the h/cm³ rate as an argument.

**Renders (`renders/`):**
- `sp_cage_wordmark_side` (photo 48's side, straight on)
- `sp_cage_plain_side`
- `sp_cage_34`
- `sp_row2_exploded`

## Frame — owner numbers, ROW ORDER ASSUMED

The owner gave "first row 92.56 mm in height, second row 81.86, third row 40.96". These are read as **bottom-up clear
openings between rail faces**, with 20 mm rails:

| row | clear opening | rails | slot centres z |
|---|---|---|---|
| 1 — deck → rail 2: hub, node, MTi | **92.56** | deck 0–20, rail 2 112.56–132.56 | 10 / 122.56 |
| 2 — rail 2 → rail 3: cases (fins), rods | **81.86** | rail 3 214.42–234.42 | 224.42 |
| 3 — rail 3 → top: short top bay | **40.96** | top 275.38–295.38 | 285.38 |

Overall height **295.38**. The old 125.5 / 86 pitches are dropped: he re-railed it.

**Check against photo 48:**
- **Row order:** the near-face rail centre pitches measure **316 : 284 : 156 px = 1 : 0.90 : 0.49**. These numbers give
  112.56 : 101.86 : 60.96 = **1 : 0.90 : 0.54**. **Bottom-up is the only order that fits**; top-down would invert it.
- **Vertical scale:** the rows give ~2.8 px/mm vertically, against ~3.9 px/mm horizontally from the gusset bolt pitch.
  That is consistent with the camera looking down ~44°: the rails' top faces are visible as extra band height.
- **Face width:** the gap between the gusset tips measures **316–320 mm** at the three rail levels. That matches
  444.5 − 2 × 62 = **320.5**, so the 444.5 face and the 12 in plate (6–8 mm clear at each end) are consistent.
- **Not taped yet.** Still CONFIRM below.

## Fastening — the t1_panels rev B scheme, three rows

- **Mounting:** the plates sit flat on the rail faces **between the corner gussets**: 304.8 wide (12 in class), plain
  chamfered ends, X0 = 69.85 from each frame corner.
- **Shared rails** (rails 2 and 3) are split on the slot centreline. Each plate owns half the rail face and reaches
  over with **castellated ears** (20 wide, 18.5 over, notch = ear + 1 per side) into the other plate's notches.
- **Bolts:** M5 into **14122 T-nuts** on the slot centrelines; 4.5 N·m, Loctite 243, torque stripe (R6.6).

**Ear pattern, the same on every shared rail: the LOWER plate owns set A, the UPPER plate owns set B.** Per half,
measured from the plate's outer end, mirrored:

| plate | bottom row | top row |
|---|---|---|
| row 1 | deck rail, plain bolts at **A [32, 100]** | rail 2, **up-ears at A** |
| row 2 | rail 2, **down-ears at B [66, 134]** | rail 3, **up-ears at A** |
| row 3 | rail 3, **down-ears at B** | top rail, plain bolts at **A** |

- **Fasteners:** 4 per half, so 8 per plate and **48 M5 + 48 T-nuts** for six plates.
- **Removal:** every plate comes off on its own fasteners; its neighbours' ears sit in its notches and do not trap it.
- **Ear section:** the ears are 20 wide, leaving ≥ 4.8 mm wall round a Ø 10.4 BHCS counterbore (asserted ≥ 2.4).
- **Fastener type:**
  - **Wordmark side, row 1** (over the hub and MTi, the tool-free one): **captive knurled M5 thumbscrews** in Ø 11.6
    seats.
  - **Everything else:** flush M5 BHCS.

## Function per side

| | wordmark side (photo 48) | plain side (other side) |
|---|---|---|
| row 1 | hub (left), printed node, MTi plate (right). Full hex. Thumbscrews. **No LED window:** the MTi board lies flat with its LED facing up, and the hub's LEDs face the I/O end | contents unknown. Full hex |
| row 2 | cases side-on, fins toward the plate (left half, EST u 30–119 = frame x 100–189). Hex over the fins; **CANARY wordmark in the right half**, off the fins | cases' other fin face (right half seen from that side). Full hex |
| row 3 | short top bay. **Five-row hex band** fits: 41 clear − 2 × 2 margin; notch keep-outs at set A | same |
| ends | dome on top and V-mount battery at the end are outside the plates. **What stays exposed:** both end faces (I/O end, battery end), the top, and the gusset corners (frame x 0–62 at each end) | same |
| cables | **none through the long faces:** the braided loom and the yellow tuner lead leave the I/O end (photos 47/48) | — |

## Open area (house hex 5 AF / 1.6 web, per plate)

| | row 1 | row 2 | row 3 |
|---|---|---|---|
| wordmark side | 98.5 cm² | 56.9 cm² (wordmark band solid) | 34.6 cm² |
| plain side | 98.5 cm² | 77.7 cm² | 34.6 cm² |

- **Over the row-2 case fins** (EST u 30–119, one half): **32.9 cm² on both sides** (R4.2 ≥ 32 **MET**, asserted by
  echo).
- **Why the wordmark sits in the right half:** a wordmark centred on the seam would cut the fin area to ~25 cm², which
  fails R4.2. The right half is clear of the fins and the wordmark never crosses the seam. The centred option is
  `WM_POS = "centre"`; its seam would run in the N|A letter gap.
- **Wordmark placement:** row 2 is recommended over row 1. Row 2 is eye level with the cases and the visual belt of
  the face. Note that row 1 is actually the larger bay (92.56 vs 81.86).

## Look and accents (one-accent rule)

- **Body:** black ASA. Hex fields in the house cell. 6 mm chamfered plate corners.
- **Wordmark side:**
  - the real `t1_panels/brand/canary-wordmark.svg`, scaled to 112 wide and **engraved 1.2** on the face;
  - **yellow snap-in chevrons** at both ends of every plate, the only colour: press-fit 1.6 inlays, 0.15 clearance, a
    dab of CA;
  - no bird mark (no vector exists; the slot is a placeholder only, not cut); taglines off.
- **Plain side:** vents only.

## Seam and print

- **Seam:** each plate (304.8) is wider than the bed, so it prints as **two halves** on the rev B centreline seam:
  - a loose spline (1.6 × 4.0) in grooves in both seam faces;
  - **one rear splice bar** per plate (32 × bay − 6 × 4), on 4 × M3 heat-sets (4.4 × 4) at ±8 from the seam.
  - Hex stops 18 from the seam.
- **Orientation: FACE DOWN.** The face gets the bed finish. Engraving, chevron seats, counterbores and thumbscrew seats
  are shallow bed-face recesses; the hex goes straight through.
- **MAXSPAN 10.4** (11.6 on the thumbscrew halves), so `max_bridge_length` is 15 / 16.
- **Row 3 can be ONE piece.** At 304.8 × 89.5 it does not fit straight (304.8 > 281), but **rotated 45° its footprint
  is 257 × 257**, inside the 281 house limit. `half="full"` gives `sp_r3_*_FULL45.stl`: no seam, no splice. Rows 1/2
  (≥ 139 tall) do not fit at 45° (315).

**House slice (done, NOT started):** `<scratchpad>/slice_side/sp_r2_wordmark_L_PLA.gcode`.
- **Preamble:** `PRINT_START BED=60 HOTEND=220`, M140 S60, M104 S220. The S0 shutdowns are untouched and there is no
  M109/M190.
- **Settings:** bottom shells 4, `max_bridge_length` 15, brim 6.
- **`gcode_check`:** PASS.
- **Result: 6 h 27 m, 20.2 m / 48.5 cm³ (~60 g PLA).**
- It sets the plan's rate: **0.106 h per CAD cm³**, and 0.79 cm³ of filament per CAD cm³.

**Print plan (times EST from that rate):**

| prints | contents | each | total |
|---|---|---|---|
| 4 | row-1 halves (wordmark L/R, plain L/R), one per bed | ~7.8 h, ~73 g PLA | ~31 h |
| 4 | row-2 halves | 6.4–7.6 h | ~27 h |
| 2 | row-3 plates: one-piece at 45° (or 4 halves, two per bed) | ~10.1 h | ~20 h |
| 1–2 | 6 splice bars + 6 splines + 6 yellow chevrons (separate yellow bed) | — | ~6 h |
| **11–12** | **full set (12 halves or 8 halves + 2 one-piece row 3)** | | **~85 h, ~790 g PLA fit-check** |

- **Installed mass:** ~730 g ASA plus ~150 g of hardware, so **~0.9 kg** added to the cage. Count it against the R7.2
  ceiling.
- **Hardware:**
  - 8 captive knurled M5 thumbscrews + O-rings;
  - 40 M5 × 10 BHCS;
  - 48 × 14122 T-nuts;
  - 24 M3 heat-sets + 24 M3 × 8;
  - Loctite 243.

## CONFIRM (before any flight print)

1. **Row order and meaning:** the rows are read as **bottom-up clear openings** (rail face to rail face). If they are
   centre-to-centre pitches, or top-down, re-cut `ROW_H`; everything regenerates.
2. **Face length** (444.5) and **the gusset-tip gap on each rail** (expect ~320; the plates are 304.8). Tape it.
3. **What is behind each side, at what depth** (tape from each rail's outer face to the nearest component, every row,
   both sides):
   - the case fin span along the face (EST frame x 100–189 from the I/O end) and their depth;
   - the hub, node and MTi;
   - that the rear splice bars (4 mm behind the plate at frame x ~206–238) clear everything.
4. **The other long side:** a photo, or the tape measures. Its contents are unknown.
5. **The MTi LED faces up** (no window cut); the hub's LEDs face the I/O end.
6. **Gussets on the long faces:** L at deck/top, T at rails 2/3, legs ≤ 62. Photo 48 shows T-plates at rails 2 and 3.

---
# MONOLITH option — "one plate that spells CANARY in large letters" (2026-10-07, wordmark side only)

**Settings:** `format="monolith"`, with `variant="stencil"|"applique"` and `layout="twoline"|"oneline"`. The plain side
keeps the three vented rows.

**Layout:** `make_wordmark_layout.py` builds it from the real `t1_panels/brand/canary-wordmark.svg`:
- parses the six glyphs;
- keeps the letter spacing;
- sizes and places the lines;
- finds the seam;
- lays the micro-hex;
- checks every web;
- writes `wm_layout_*.scad`.

**Build:** `build_monolith.py` makes the STLs, renders and volumes.

**Renders:**
- `renders/mono_pair_straight` and `mono_pair_34`: stencil left | applique right
- `mono_stencil_straight`
- `mono_applique_straight`
- `mono_oneline_stencil_straight`
- `mono_applique_exploded`

## Cap height — the 150–170 mm target is not reachable on this face

- **Width limit:** CANARY is ~9.6 : 1 wide-to-tall with its own spacing. On a 304.8 plate (12 margins) **one line caps
  at 30 mm**. A 160 mm cap would need a ~1.5 m wide face.
- **What is drawn — two lines, CAN over ARY, cap height 58.8 mm** (2.3 in, the maximum):
  - **CAN** sits in row 2 over the case fins; **ARY** sits in row 1.
  - Both stay ≥ 10.7 off the rail faces, so the solid rail bands carry all the bolts.
- **Legibility:** by the 1 in per 10 ft sign rule, 58.8 mm is best at ~7 m and legible to ~25 m. The 30 mm one-line
  version is best at ~3.5 m and legible to ~12 m.
- **Taller letters would need** the letterforms condensed (not the house vector), or the word stacked one letter per
  row, which does not fit three bays.

## Plate, fastening, seam

- **Plate:** 304.8 × **279.38**. The deck-row and top-row bolts sit 2 inside the bottom and top edges (the head
  overlaps the edge), so the plate covers 12 of the deck and top rails and **all of rails 2 and 3**; ≥ 10 overlap is
  asserted.
- **Height:** 279.38 is what makes a full-height half fit the **281 bed**. Full rail coverage (295.4) would not fit.
- **Fasteners:** no neighbours, so plain bolt rows on all four slot lines: **16 × M5 into 14122**.
  - Captive thumbscrews by default (`fix_mono="ts"`): the plate is now the access door for the hub/MTi row.
  - 8 fewer fasteners than the three-row set (24).
- **Seam (vertical):** it runs in a letter gap common to both lines, **u 202.7**: between A|N on line 1 and R|Y on line
  2, with a 5.2 web each side. The halves are **202.7 + 102.1 wide**, both 279.38 tall.
  - **It cannot be "CAN|ARY"** in the two-line layout, because the N|A break is the line break.
  - The one-line layout does put it in the N|A gap, but that gap leaves only **3.7 web each side** (< 4, flagged).
  - The seam is kept off the case-fin zone so the hex there stays whole.
- **Spline:** in three segments, only where no letter is near the seam.
- **Rear splice bars:** two, in **letter-free bands of the bays, never over a rail**:
  - row 3, 4 × M3 heat-sets;
  - row 1 below ARY, 2 × M3.

## Variants

| | **(A) STENCIL** | **(B) APPLIQUE** |
|---|---|---|
| letters | cut THROUGH as vents, 0.8 face bevel. **The house glyphs are single closed outlines with no enclosed counters (the A and R are open forms), so nothing falls out and no stencil bridges are needed** | yellow letters, 2.0 thick, standing **2.5 off the face on 3 × Ø7 standoff bosses with Ø4.2 pegs press-fit (0.2) into Ø4.0 holes** = 4.5 proud. All six fit one yellow plate (261 × 126). *Changed from "3 proud in shallow pockets": solid pocketed letters left only 23 cm² over the fins (R4.2 fail); standing them off lets the micro-hex run unbroken under them* |
| field | micro-hex (3.2 AF / 1.2 web) round the letters over the fin zone, ≥ 4 web from every letter, plus a row-3 band | micro-hex over all three bays |
| accent (one) | yellow chevrons at the row-3 ends | the letters |
| open area | letters **120.6** + hex **56.8** = **177.4 cm²** | **268.8 cm²** |
| over the case fins (EST u 30–119, row 2) | **33.3 cm²** (letters C/A + hex) — **R4.2 MET** | **34.1 plate, 33.1 effective** (flow under the letters capped at perimeter × 2.5 gap) — **R4.2 MET** |
| webs (stencil) | letter–letter ≥ 14.5; letter to a bolt seat ≥ 15.7 (≥ 6); letter–edge 12.0; letter–rail face 10.7; narrowest neck inside a letter 8.0 (≥ 4) | — |

## Print plan and mass (times EST at 0.106 h/cm³, from the row-2 house slice; nothing new sliced)

| | stencil | applique | three-row wordmark set it replaces |
|---|---|---|---|
| halves | L 239.6 + R 130.6 cm³ (25.4 h + 13.8 h) | L 208.8 + R 111.4 (22.1 + 11.8 h) | 6 halves, 377 cm³ |
| extras | 2 splice bars, 3 splines, 2 yellow chevrons | splices, splines, letters plate 26.6 cm³ (2.8 h, yellow) | 3 splices + 3 splines + 6 chevrons |
| total | **378 cm³ = 343 g ASA / 398 g PLA, ~40 h** | **354 cm³ = 322 g ASA / 373 g PLA, ~37 h** | ~393 cm³ = ~357 g ASA, ~42 h |
| fasteners | 16 | 16 | 24 |

**PRINT RISK:** each **L half is one ~22–25 h print** of ~165–190 cm³ of filament, i.e. **~69–79 m**. That exceeds
`gcode_check.py`'s 50 m total-extrusion heuristic, so the L half **will fail the house check as-is**. Options:
- the check's owner raises or waives that heuristic for this part; or
- split the L half again at the second common letter gap (u ≈ 113, between C|A of CAN and A|R of ARY, 5.2 web),
  giving three pieces. That gap crosses the fin zone, so the stencil fin area drops; re-run the layout before choosing
  it.

The R halves (37–43 m) pass.

## Recommendation

- **From across a hangar: APPLIQUE.** Yellow on black is the only high-contrast reading. The stencil's letters are
  black openings onto a dark interior: they read as texture up close and nearly vanish at distance.
- **Prints cleaner: STENCIL.** One material, no letters to press, no pegs to align, the letters ARE the vents, and it
  is more open overall.
- **Pick APPLIQUE for the look Javi asked for** ("spells CANARY in large letters"). It meets R4.2 over the fins only
  because the letters stand off the plate.

## CONFIRM (additions)

1. **Two-line CAN/ARY** at 58.8 mm caps is acceptable (vs one line at 30 mm with the seam in the N|A gap but a 3.7 mm
   web).
2. **Applique letters standing 4.5 proud on pegs** (not 3 mm in pockets). Check the 4.5 mm proud letters clear
   anything that passes the cage side (seat back, strap path).
3. **Case-fin zone behind row 2:** frame x 100–189 from the I/O end (EST). It decides both R4.2 results; tape it.
4. **The L half's 50 m extrusion overrun:** the gcode-check owner's call, or the three-piece split.
5. The 2.0 deck/top edge reveal (8 mm of each outer rail stays visible) is acceptable.

---
# CUTOUT option — row 2, black CANARY plate + yellow vented backer (2026-10-07, replaces the monolith for now)

**Owner:** "a single piece that is 12 inches wide and 80.80 mm tall with the word CANARY as cutouts, and then a single
yellow piece behind it, vented to make the CANARY pop out in yellow."

**Files:**
- **`format="cutout"`:** wordmark side only.
  - Row 2 is this plate.
  - Rows 1 and 3 on that side now cover rails 2 and 3 fully, with flat edges and no ears (`co_row*_wordmark_*`).
  - The plain side keeps its three vented rows.
- **`make_cutout_layout.py`:** sizes the lettering, adds the stencil bridges, lays the vents, checks the webs and open
  areas, and writes `cutout_layout_*.scad` and `cutout_common.scad`.
- **`build_cutout.py`:** STLs, renders, volumes.

**Renders:**
- `co_cage_straight` (condensed)
- `co_cage_straight_native`
- `co_pair_condensed_vs_native`
- `co_cage_34`
- `co_exploded`
- `co_inlay_closeup`

## Lettering — cap height, both options

| | **condensed** (DIN Condensed Bold, tracking +8 %, **off the case fins**) — RECOMMENDED | native (house wordmark, its own tracking) |
|---|---|---|
| cap height | **42.7 mm** (width-limited: the word sits right of the fin zone, u 125–280) | **30.2 mm** (width-limited, full width) |
| webs | letters 4.7 apart (≥ 4); letter to edge ≥ 18.9; letter to screw boss 9.5 (≥ 6) | 7.4; 11.0; 9.6 |
| counters | A and R have closed counters, so **4.5 mm stencil bridges** run up through the apex/bowl top. The island is held, nothing falls out | none (single-outline glyphs) |
| over the case fins (u 30–119, EST) | **34.4 cm² — R4.2 MET** (the fins see an unbroken black hex field) | 20.3 cm² — NOT MET |

**About the fonts:**
- The concept board's Saira Condensed is a web font and is not installed on this Mac. DIN Condensed Bold is the
  installed condensed sans of the same class.
- **Centring the condensed word gives cap 58.3 mm**, but it then covers the fins and leaves only 11.4 cm² there (R4.2
  fails). The 45–55 mm target is reachable only by giving up the fin rule on this face.
- Taller letters would need the fin zone relocated (CONFIRM it by tape: it is EST).

## Construction

- **Front** (black, 304.8 × 80.80 × 5.0):
  - CANARY is cut through, with a 0.4 face break.
  - A **rear rebate 3.2 deep** sits inside a 5 mm full-thickness rim, so the face skin is **1.8**.
  - **The yellow backer's face sits 1.8 behind the front face:** the letters read as an inlay with depth.
  - A house hex field (5 AF / 1.6) runs everywhere ≥ 4 from the letters, including into the rim.
  - Two Ø3 pegs on the rebate floor locate the backer.
- **Backer** (yellow, 3.0 thick, rebate outline − 0.3):
  - **Fine hex (1.6 AF / 0.8 web) under the letters.** 1.6 mm cells subtend ~1.8 arc-minutes at 3 m, so the letters
    read as near-solid yellow while still passing air.
  - **The trade:** that pattern is only ~20 % open across the letter area once whole cells and rims are counted
    (5.8 cm² through the condensed letters). The breathing is done by the black field, not the letters.
  - Elsewhere the backer has the field holes +0.3, aligned by the pegs, so the field reads dark through both plates.
    At a steep angle the yellow bore walls show.

## Fastening — (a) primary: inside the bay

The plate is **80.80 in the 81.86 bay: 0.53 to each rail**, with its front face flush with the rail faces.

**Retention:**
- **±z:** the two rails themselves.
- **±y and ±x:** **4 × M4** through front skin + backer into M4 heat-sets (5.6 × 6) in **4 printed L-brackets**.
  - Each bracket sits behind the plate and is bolted with **one M5 into a drop-in T-nut in the bay-facing slot** of
    rail 2 (bottom pair) or rail 3 (top pair).
  - The screw clamps backer, skin and bracket tab together. These are the same screws that hold the plate, as asked.

**Why not the face slots:** the brief's "M5 into the rails' face slots" cannot work for a plate inside the bay. The
face slots are at the rail centrelines, outside the plate's 80.8 height. The brackets use the bay-facing slots instead.

**Screws and access:**
- Screws sit at u 20 / 291.8, 9 mm from the top and bottom edges, outside the word.
- `co_fix="bhcs"` (M4 × 12 + washer) is the default: row 2 is the case bay, not the hub/MTi access row.
- `"ts"` gives captive M4 thumbscrews.

**(b) flagged, not drawn:** if 80.80 means the body between ears, use rev B castellated ears onto the rail faces (plate
~100 tall, M5 into the face slots) like the row plates.

## Print — one piece each, 45° on the bed

- **Footprint:** 304.8 × 80.8 at 45° is a **268.4 mm square** with the corner chamfers.
- **Brim:** the 3 mm corner chamfers trim the 272.7 estimate. With the house 6 mm brim it would be **280.4, just under
  281 (0.6 to spare)**. The slices use a **3 mm brim** for margin.
- **Checked from the gcode:** the front's extruded footprint is **277.9 × 277.9** (inside 281); the backer's is
  267.1 × 264.5.
- **No seam** on either part.
- **Orientation:** front FACE DOWN, rebate and pegs up; backer yellow face down. No bridges (MAXSPAN 2, so
  `max_bridge_length` is 7).

| part | cm³ | g ASA | slice (PLA, house way, NOT started) |
|---|---|---|---|
| `stl/co_condensed_front_45` | 40.1 | 36 | **`sp_cutout_front_PLA.gcode`: 4 h 22 m, 15.9 m / 38.2 cm³ (~47 g)**, gcode_check PASS |
| `stl/co_condensed_backer_yellow_45` | 39.5 | 36 | **`sp_cutout_backer_PLA.gcode`: 4 h 50 m, 14.6 m / 35.1 cm³ (~44 g)**, gcode_check PASS — print in YELLOW |
| `stl/co_brackets_x4` | 11.5 | 10 | not sliced (~1.2 h) |
| `stl/co_row1_wordmark_L/R`, `co_row3_wordmark_L/R` | 82.4 ×2, 55.6 ×2 | — | rows 1/3 re-cut for the cutout (flat edges on rails 2/3) |

**Both slices:**
- **Preamble:** `PRINT_START BED=60 HOTEND=220`, M140 S60, M104 S220. The S0 shutdowns are untouched and there is no
  M109/M190.
- **Settings:** bottom shells 4.

**Row-2 set (front + backer + 4 brackets): ~91 cm³ = ~83 g ASA, ~9.6 h.**
- **Hardware:**
  - 4 × M4 × 12 + washers;
  - 4 × M4 heat-sets;
  - 4 × M5 × 8 BHCS;
  - **4 × drop-in M5 T-nuts** for the bay-facing slots. Slide-in 14122s need the rail end open.

## CONFIRM (cutout)

1. **80.80** is the whole plate height, i.e. option (a) inside the bay. Otherwise use (b) with ears.
2. **Drop-in M5 T-nuts** for rails 2/3's bay-facing slots, and that those slots are free at x ≈ 90 and 360 (frame).
3. **Case-fin span** behind row 2 (EST frame x 100–189 from the I/O end). It is why the word sits right of centre; if
   the fins sit elsewhere, re-run `make_cutout_layout.py` with `FIN`.
4. **Lettering:** DIN Condensed (cap 42.7, recommended, R4.2 met) vs the house wordmark (cap 30.2, fails R4.2 here)
   vs centred condensed (cap 58.3, fails R4.2).
5. **Behind the plate:** ≥ 20 mm clear behind the plate's back face at the four bracket spots (the brackets reach
   15 mm into the frame).
