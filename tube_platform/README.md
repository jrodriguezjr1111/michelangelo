# tube_platform — SlimRig CHEESE PLATE (rev E)

`make_tube_platform.scad` (part selector). **94 x 134 x 8 plate** on two SlimRig
tubes (canon rev-B interface, Ø15.0+0.4 troughs, caps across each tube), with a
uniform **10.0 mm M3 heat-set grid** on the top face, a half-pitch-offset grid on
the underside, and the same grid on the upper deck. All caps interchange with the
printed rsd/lilygo/nano/orin spares (INS 4.4 family).

> **PRINTED PARTS THAT SURVIVE — DO NOT REPRINT:** `tp_clamps` and
> `tp_caps_spacers`. Verified this revision, not assumed (see *Clamp proof*).
> `tp_spacers_extra` is also unchanged.
>
> **STALE:** `make_system_assembly.scad` + `asm_shim_tp.scad` still reference
> `tower()`, `carrier()`, `TWR_*`, `BB`, `CAR*` — retired back in rev D. That
> scene was already broken before this revision and is not fixed here.

---

## rev E (CURRENT) — CHEESE PLATE, -30 mm, insert-ready grid

Two user calls: *"let's make a cheese plate instead with M3 inserts instead of
holes"* and *"let's remove the 30mm extra length."* Both are done, and the
component-specific hole layout is **retired entirely** — the plate and deck now
carry no board-specific feature at all.

| | rev D | rev E |
|---|---|---|
| plate | 94 x 164 x 7, y -97..67 | **94 x 134 x 8, y -67..67** |
| plate features | RTK/relay/EG25/deck-leg/fence/lashing bores | **grid only** |
| plate top bores | 20 named | **109 grid + 2 Ø8 pass-through** |
| plate underside | 4 WAGO inserts | **24 half-offset grid nodes** |
| deck | 4 mm, FC + proto bores | **6 mm, 87 grid nodes** |
| insert-ready total | ~28 | **220** (seat 33) |
| cantilever off the band | 56.6 S / 52.3 N | **26.6 S / 52.3 N** (back to rev A5) |

---

## THE PITCH DECISION — the arithmetic, not a preference

A cheese plate whose pitch matches none of the real board patterns holds
nothing. So this was brute-forced, not chosen: every pitch from 6.00 to 22.00 in
0.01 steps, scored against the ten distinct hole spans this box actually
contains. A Ø4.4 bore needs ≥ 2.5 mm of ligament, so the pitch floor is 6.9.

**Error to the nearest multiple, per span (mm):**

| span (source) | p=8 | **p=10** | p=12.5 | p=16 | p=20 |
|---|---|---|---|---|---|
| 19.77 (relay Y) | 3.77 | **0.23** | 5.23 | 3.77 | 0.23 |
| 24.21 (EG25 Y) | 0.21 | 4.21 | 0.79 | 7.79 | 4.21 |
| 37.60 (RTK, both) | 2.40 | 2.40 | **0.10** | 5.60 | 2.40 |
| 40.00 (sled Y, proto Y) | 0.00 | **0.00** | 2.50 | 8.00 | 0.00 |
| 40.77 (relay X) | 0.77 | **0.77** | 3.27 | 7.23 | 0.77 |
| 49.00 (FC Y) | 1.00 | **1.00** | 1.00 | 1.00 | 9.00 |
| 58.00 (FC X) | 2.00 | 2.00 | 4.50 | 6.00 | 2.00 |
| 60.00 (proto X) | 4.00 | **0.00** | 2.50 | 4.00 | 0.00 |
| 64.00 (sled X) | 0.00 | 4.00 | 1.50 | 0.00 | 4.00 |
| 70.80 (EG25 X) | 1.20 | **0.80** | 4.20 | 6.80 | 9.20 |

### What the sweep actually found
1. **No pitch in the whole viable range serves more than ONE complete pattern
   in both axes.** The spans are mutually irrational — 37.60 vs 40.77 vs 24.21
   vs 58 vs 64 share no useful common factor. Any claim that "a cheese plate
   makes everything bolt straight down" is false for this box.
2. **Pitch 10 serves the most distinct spans:** 6 of 10 within 1.0 mm
   (19.77, 40, 40.77, 49, 60, 70.80), three of them within 0.23 mm. It is also
   the family's prior art (`pelican_frame` `platform_blank`, 10 mm / 94 holes).
3. **Pitch 8** is the *only* pitch that lands the family's **64 x 40 sled
   interface exactly** — genuinely tempting, because every `pelican_frame` sled
   would then drop straight on. Rejected: it serves fewer real *board* spans,
   needs 56% more bores, and leaves only 0.95x the solid-7 stiffness vs 1.08x
   at pitch 10. If you ever want pelican sleds on this plate, an 8-node sub-grid
   is a five-line change — say so and it goes in.
4. **Pitch 12.5** uniquely nails the ZED-F9P (37.60 = 3 x 12.533, err 0.10) and
   **nothing else**. Rejected.

### Which patterns need a provision — and why "dual pitch" and "slotted" are dead
- **DIRECT, no adapter:** ESP32-S3 protoboard **60 x 40** (exact) on Ø7x6 spacers.
- **DIRECT with a drill pass:** the **relay, 40.77 x 19.77 -> 40 x 20**, errors
  0.77 / 0.23, i.e. 0.39 and 0.12 mm per hole. Open its own holes from Ø3.2 to
  **Ø4.0** and an M3 at the grid node passes. (Precedent: rev D already
  contemplated opening these JQC3F holes.) A shoe is provided as the fallback.
- **SHOE required:** RTK (2.40 both axes), FC (2.00 / 1.00), EG25 (0.80 / 4.21).
- **Dual pitch / half-offset (quincunx) grid: arithmetically dead.** A
  rectangular 4-hole pattern needs all four corners in the *same* coset, so a
  quincunx grid still only reaches multiples of the base pitch — it buys exactly
  zero new spans. A true second family at 5 mm needs a 5 mm row pitch, which is
  a **0.6 mm** ligament. Impossible.
- **Slotted bores: impossible by definition.** A heat-set insert needs a round
  bore. Slots belong on the adapter, not the plate — which is what the shoes are.

### GRID SHOES — the adapter, sized so it does not cost you the layout
The obvious adapter is a square tile with the board pattern inside and grid
holes at the corners. It was **modelled and rejected**: an RTK tile needs
60 x 60 for a 43.5 mm board, and with that tile tax the five-board loadout no
longer nests on a 134 plate. The shipped adapter is a **pair of bars** instead —
one under each board-hole column — **6.0 mm thick so it replaces the Ø7x6
spacer** (board heights unchanged):

| shoe | board pattern | grid pattern | pair footprint | board envelope |
|---|---|---|---|---|
| RTK | 37.60 x 37.60 | 20 x 20 | 47.6 x 47.6 | 43.5 x 43.5 |
| RELAY (rot 90) | 19.77 x 40.77 | 20 x 20 | 32.0 x 50.8 | 26 x 50 |
| EG25 | 70.80 x 24.21 | 40 x 20 | 80.8 x 34.2 | 80 x 35 |
| FC (deck) | 58 x 49 | 40 x 40 | 68.0 x 59.0 | 73 x 54 |

Three of the four tuck **inside** the board's own envelope. Each bar: two M3
clearance holes with a **captive M3 nut pocket** in the top face (board screws,
M3x6 — no heat-sets in the shoe), and two counterbored M3 clearance holes
(M3x12 down into a grid insert). Board-hole-to-grid-hole separation is asserted
≥ 6.4 mm c-c on every shoe; the tightest is the relay at 10.4.

---

## THE 60-100 HEAT-SET PROBLEM — insert-READY, not insert-populated

A fully seated grid would be ~220 heat-sets: hours of work and real money. So
**every bore is printed insert-ready** — Ø4.4 x 6.0 with a 0.6 chamfered mouth
as the insertion funnel — and a brass insert goes in **only where a screw
actually lands.**

| where | insert-ready bores | seated for the reference loadout |
|---|---|---|
| plate top | 109 | 12 shoes + 4 deck legs + 5 fence = **21** |
| plate underside | 24 | 4 WAGO = **4** |
| deck | 87 | 4 FC shoe + 4 proto = **8** |
| **total** | **220** | **33** |

Everything is **one insert SKU** — Ø4.4 x 6.0, the same stock already in the
printed caps and rail tops. Do not introduce Ø4.0.

**Suppressed nodes (6):** x = ±40 at y = -10, -20, -30 — they sat inside the
Ø8 driver access cones of the rail bolts at (±40, -9/-19/-29). Asserted: every
surviving node clears a rail-bolt driver by ≥ 0.5 mm and its counterbore by
≥ 2.0 mm; the tightest surviving node is (40, 0) at 9.0 mm from a bolt.

---

## THE PRINTED CLAMPS STILL FIT — proof, not eyeball

The rail band and its bolts are **absolute constants** (`BAND_S -40.4`,
`BAND_N 14.7`, bolts x ±40 at y -29/-19/-9); `west_rail()` reads none of
`PL_T`, `PL_Y0`, `PL_Y1`, so the plate could shrink 30 mm and thicken 1 mm
without touching the clamp.

Verified by **re-slicing the regenerated STL with the identical profile chain
and comparing toolpaths against the gcode that was actually printed** — a
stronger test than a vertex diff, because it compares the machine instructions:

| | tp_clamps | tp_caps_spacers |
|---|---|---|
| extrusion points | 6410 vs **6410** | 436 vs **436** |
| unique Z layers | 91 vs **91**, identical set | 18 vs **18**, identical set |
| max deviation (nearest point, same layer) | **0.0405 mm** | **0.0000 mm** |
| points deviating > 0.05 mm | **0 of 6410** | 0 of 436 |
| XY bounding box | bit-identical | bit-identical |
| filament | 17201.71 vs 17201.96 mm (+0.0015%) | identical |

0.0405 mm is **9% of one 0.45 mm bead** and is the STL triangulation phase of
the Ø15.4 trough facets — the same artifact rev D reported. **The printed
clamps and caps fit the rev-E plate.**

> The rev-D `tp_clamps.stl` was overwritten before the comparison (this
> directory is untracked, so there was no git copy). The printed **gcode**
> survived and is the better reference, so nothing was lost — but the STLs
> here are regenerated, not the exact bytes that were sliced in August.

---

## WHY 8 mm, AND THE STIFFNESS STORY

Perforating a plate on a 10 mm grid removes 44% of the ligament. Section
modulus through a bore row, computed in the model and echoed:

| plate | ligament | I (per unit width) | vs solid same-T | vs SOLID rev-D 7 mm | insert floor |
|---|---|---|---|---|---|
| solid 7 (rev D) | — | 28.58 | 1.000 | 1.000 | — |
| **7 perforated** | 0.56 | 19.61 | 0.686 | 0.686 | **1.0 mm** |
| **8 perforated (rev E)** | 0.56 | **30.81** | 0.722 | **1.078** | **2.0 mm** |

Going 7 -> 8 mm buys back everything the grid costs **and 8% more**. So:

- **NO underside ribs.** The 54 mm Nano corridor and the Nano's 52.3 mm
  insertion from the north are untouched, and nothing intrudes on the corridor
  anywhere (the underside bores are blind, 6 deep in 8 — no protrusion).
- The **1.0 mm floor at 7 mm was the real killer** independent of stiffness: a
  heat-set pressed into 109 blind bores each backed by 1.0 mm of PLA will punch
  through some of them. 2.0 mm is the fix, and it is asserted.
- The **half-offset underside family costs nothing in bending**: it is asserted
  to share no row and no column with the top family, so no section line ever
  cuts both. In-plane web between a top node and its nearest under node is
  **2.67 mm**. Shear/torsion in the 2..6 mm band is reduced; bending is not.
- Cost of the thickness change: the six plate-to-rail M3x12 now engage **4.0 mm**
  of brass instead of 5.0. The joint is plastic-limited (~300 N insert pull-out),
  not thread-limited, so M3x12 stands. **M3x14** gives the full 6.0 mm if you
  want belt and braces — that is the only BOM option this revision creates.

---

## THE UNDERSIDE GRID (24 nodes) — recovering what the -30 mm took

Removing 30 mm removed the area rev D grew for. Part of it comes back
underneath: a **half-pitch-offset family** at (10i+5, 10j+5), x ±25 (10 pitch),
y -55..+5 (20 pitch). It lives only where hanging hardware is already proven
safe — south of the Nano's stop face at y 14.7 and inboard of the rail blades —
both asserted. Duty: the **WAGO distribution rail**, and enough freedom to hang
a small board (the relay's 40 x 20 grid rectangle is reachable, 26 mm deep
leaves 28 mm of corridor). Two **Ø8 pass-throughs** at (-40, -40) and (-40, -60)
drop cables from the top face into the corridor on the west side, where the
photographed USB runs already exit.

---

## FENCE — does NOT survive unchanged

It was 164 long in rev D and must be re-cut for 134. The **SMA row is still
frozen** — y 44/16/-12, z 17, 2.5 mm panel — so bulkheads already installed
still fit and align. Everything else was re-sited into the windows a shorter
wall leaves, and asserted clear of each other:

- **DC feed-through survives** (the RSD PSU is still outside the box): Ø12 at
  **y -57**, z 12 — was y -60 on the longer wall.
- **Cable-clamp pad survives**, moved y -85 -> **y -30** (the only window that
  clears the SMA row, the ribs and the feed on a 134 wall). Printed clamp bar
  unchanged.
- Ribs y **[60, 30, 0, -46]**; zip columns y **[60, 36, 24, 4, -4, -24, -40]**
  (8 -> 7 columns, pairs at z 21/27); top rail and 35 mm height unchanged.
- **Screw column now lands on GRID NODES** at x 40, y [60, 40, 10, -40, -60] —
  the wall needs no dedicated bores in the plate at all. Asserted.
- **Underside WAGO provisions carry over** onto the underside grid.

---

## Deck (rev E) — a cheese deck

83 x 132 x **6** (was 4), z 29..35 over the plate, on 4 legs at plate grid nodes
**(±30, ±60)**. 6 mm so a Ø4.4 heat-set sits **flush through**. 87 insert-ready
nodes on the same 10 mm grid (x ±30, y ±60). Deck underside clears a 26 mm-tall
level-1 stack by 3.0. Stiffness: 1.9x the old solid 4 mm deck even perforated.

## Reference loadout — NOT geometry any more

Nothing in the model depends on this. It exists so the assembly view and the
nesting check have something concrete; every position is a grid node, slide any
of it a node.

| level | item | at | mount |
|---|---|---|---|
| 1 (plate) | RTK ZED-F9P | (-20, 30) | RTK shoes |
| 1 | Relay | (20, 20), rotated 90° | relay shoes, **or** direct with Ø4.0 board holes |
| 1 | EG25 assembly | (0, -30) | EG25 shoes |
| 2 (deck) | FlyCatcher | (0, 30) | FC shoes |
| 2 | ESP32-S3 protoboard | (0, -30) | **DIRECT**, 4x Ø7x6 spacers |
| underside | WAGO rail | south field | 4 of the 24 under nodes |

All five fit, which took work — the honest nesting numbers are echoed by the
model. **RTK and RELAY abut with a 0.2 mm gap in X**: that is 10 mm grid
quantisation, not a fit problem, and it is layout, so move one a node if it
bothers you. **Service chain:** the EG25 shoe pair spans x ±40.4 and covers four
of the six rail-bolt counterbores — EG25 off before the plate comes off the
rails, as in every prior rev.

## Vertical stack (above plate top)
RTK / relay / EG25 top 26 · deck underside 29 (3.0 clear) · deck top 35 ·
FlyCatcher top 68 · protoboard top 66. Nano over tube tops 53.3 vs 54 corridor
(0.7, asserted).

---

## Print — PLA Tough+, OrcaSlicer CLI + `cw_mes/qidi_xplus4_brim.json`

Sliced with the machine profile `Qidi X-Plus 4 0.4 nozzle` + the repo brim
process + `Bambu PLA @Qidi X-Plus 4 0.4 nozzle`, **not** `plus4_print.py` (its
PLA temperatures are under separate review). The QIDI machine profile resolves
`PRINT_START` to the cool-plate defaults (BED=35 HOTEND=200); the preamble is
rewritten to the family's values and **verified literally**:
`PRINT_START BED=60 HOTEND=220 CHAMBER=0 EXTRUDER=0`, `M140 S60`, `M104 S220`.
The corrected preamble is byte-identical to the printed `tp_clamps_pla.gcode`
except for the timestamp. `gcode_check.py`: **all checks pass** on all four new
jobs.

| job | pieces | orientation | layers | time | cm³ |
|---|---|---|---|---|---|
| **tp_plate** | 94x134x8 cheese plate | cargo-face DOWN | 40 | **5h 21m** | 46.1 |
| **tp_deck** | cheese deck + 4 legs | deck-face DOWN, legs up | 175 | **4h 17m** | 34.9 |
| **tp_fence** | 134 cable wall + clamp bar + 6 clips | upright | 175 | **1h 58m** | 15.9 |
| **tp_shoes** | 4 shoe pairs (8 bars) | flat | 30 | **2h 31m** | 23.0 |
| tp_clamps | **SURVIVES — do not reprint** | — | — | — | — |
| tp_caps_spacers | **SURVIVES — do not reprint** | — | — | — | — |
| tp_spacers_extra | unchanged spare spacers | flat | — | 0h 12m | 1.6 |

**New print total ~14 h 07 m, 119.9 cm³.** Zero support throughout.

**The grid is not free:** the plate takes 5h21 despite being 30 mm *shorter*
than rev D's 3h33 — 135 bores is a lot of perimeter. That is the price of never
having to re-cut the plate again. `GRID_P` is one line if you want a coarser
grid; going to 12.5 would drop the plate to roughly 70 bores and raise stiffness
to 1.17x solid-7, at the cost of the 19.77 and 70.80 spans.

### Orientation rationale
- **Plate cargo-face DOWN**: every blind grid bore opens at the bed and prints
  as a clean vertical hole closed by a 2 mm bridged ceiling; the chamfered
  mouths are the first layer. The underside family then prints as blind holes
  opening upward — no bridging at all. Load across layer lines is bending of a
  flat plate, which is the strong direction here. Zero support.
- **Deck deck-face DOWN, legs up**: the 4 legs print as vertical columns; the
  through-bores need no support.
- **Fence upright**: the SMA and zip bores are horizontal through a 2.5 mm
  panel (short bridges); the outboard fins have 45° tops.
- **Shoes flat**: nut pockets open upward, counterbores bridge over Ø3.4.

### Material
PLA Tough+ is fine for the bench rig this is. **If this box goes into an
aircraft or a hot cabin, reprint the plate, deck, fence and shoes in ASA/ABS**
(same files, no geometry change) — PLA's Tg ~60 °C creeps under a parked-in-SoCal
thermal load, and this plate is the structural member carrying every board.

---

## Hardware BOM (reference loadout)

**Heat-set inserts, Ø4.4 x 6.0 — 33 seated** (of 220 ready): 12 plate (3 shoe
pairs) + 4 plate (deck legs) + 5 plate (fence) + 4 plate underside (WAGO) +
8 deck (FC shoe + protoboard). Rail/cap inserts already in the printed parts.

**Screws:** 8x M3x25 (caps, unchanged) · 6x M3x12 plate->rail (M3x14 optional,
see above) · 4x M3x35 (deck legs) · 5x M3x10 (fence) · 16x M3x12 (shoes -> grid)
· 16x M3x6 + 16x M3 hex nuts (boards -> shoes) · 4x M3x12 (protoboard, direct).

**Printed:** 4 canon caps + 12 Ø7x6 spacers (have) · 8 more spacers
(`tp_spacers_extra`, have) · 4 shoe pairs · 2 clamp bars · 6 anchor clips.

---

## CONFIRM before hardware install
1. **ESP32-S3 protoboard 60 x 40 corner holes — UNMEASURED.** It is the one
   board mounting DIRECT to the grid, so it is the one assumption that costs a
   reprint of nothing but still wastes an evening. Measure it.
2. **Relay hole diameter.** Ø3.2 stock -> open to Ø4.0 for direct mounting, or
   use the relay shoes and leave the board alone.
3. **EG25 treated as ONE assembly** (module + USB/LTE carrier) on 70.80 x 24.21.
   If they are two boards, that is now purely a shoe-table edit.
4. **Tube lines x = ±30 (60 c-c)** and **TUBE_D 15.0** — unchanged assumptions
   from rev A2/A5.
5. **Nano envelope 36 mm** over its plate — the 0.7 mm corridor margin depends
   on it.

---

## Revision history (superseded)

- **rev D** — plate 94 x 164 (+30 south), component-specific inserts for
  RTK (-8,40) / relay (-8,-6) / EG25 (0,-70), one upper deck carrying
  FlyCatcher + ESP32 protoboard, DC feed moved into the cable wall, WAGO moved
  under the plate, hanging ESP32 carrier retired. Relay pattern MEASURED at
  40.77 x 19.77. Superseded by rev E: the +30 is gone and the named bores are
  gone. Spare/superseded prints: old plate, old fence, RTK tower, hanging
  ESP32 carrier.
- **rev C** — stiffened cable wall (outboard fins + top rail), zip columns
  5 -> 9, outboard cable-clamp pad + printed bar, pigtail anchor clips. The
  Ø25 round blank visible in the user's photo is **not** a feature of this
  design (`WALL_PORT_D = 0`); say what it is and it takes one line.
- **rev B** — level-1 layout on flush inserts, RTK tower, ESP32 hung under the
  plate on a carrier, breadboard tray retired, rail bolts moved to
  y -29/-19/-9 to clear the FlyCatcher's east hole column.
- **rev A5** — column keep-out band y [-40.4, +14.7]; one 55.1-long rail per
  tube, mirror pair, troughs inward, cap drivers outward; Nano tunnel south
  26.6 / north 52.3 with 54 mm clear; **rev E restores exactly these
  cantilevers.**
- **rev A4** — symmetric decoupled riser clamps, platform removable without
  unclamping the tubes.
- **rev A3** — 54 mm risers, DIN-rail two-phase engage, driver chimneys.
- **rev A2** — tubes rotated 90° to run along the 134 axis, lines x = ±30.
