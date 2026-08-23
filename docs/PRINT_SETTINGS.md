# Print settings — QIDI X-Plus 4

Reference settings for this repo, anchored to prints that actually succeeded.
Written 2026-08-22 after the MA963 antenna plate — the best-quality article
produced so far.

---

## 1. The reference print

`taoglas_ma963/ma963_plate_pla.gcode` — 173 × 180 × 19 mm plate, 95 layers,
88.24 cm³. Estimated 8 h 41 m, **actual 8 h 47 m**. Zero defects.

| setting | value |
|---|---|
| printer profile | `Qidi X-Plus 4 0.4 nozzle` |
| print profile | `0.20mm Standard @Qidi XPlus4 BRIM5` |
| filament profile | `Bambu PLA @Qidi X-Plus 4 0.4 nozzle` |
| layer height | 0.20 (first layer 0.20) |
| wall loops | 2 |
| bottom / top shells | **3 / 4** |
| sparse infill | 20 %, crosshatch |
| brim | `outer_only`, width 5, object gap 0.1 |
| support | **off** |
| `max_bridge_length` | 10 |
| bridge speed | 25 mm/s |
| outer wall / infill speed | 60 / 100 mm/s |
| first-layer speed | 30 mm/s |
| fan | 20–100 % |

**Temperatures as actually run** (see §2 — this is not what the preamble says):

| | first layer | rest of print |
|---|---|---|
| nozzle | 200 °C | **210 °C** |
| bed | 60 °C | **35 °C** |

Chamber sat at **34–36 °C** throughout.

---

## 2. The temperature trap — read this before trusting any gcode

The QIDI OrcaSlicer profile emits `PRINT_START BED=35 HOTEND=200`, which is
wrong for PLA Tough+, so every slice in this repo gets patched. **The patch is
easy to under-apply.** There are *two* places temperature is set:

1. The `PRINT_START` macro line, plus the `M140`/`M104` pair right after it —
   these govern the **first layer**.
2. A second `M104 ... ; set nozzle temperature` / `M140 ... ; set bed
   temperature` pair at **layer 2**, which governs the **entire rest of the
   print**.

Patching only (1) leaves the job running at the profile's stock 210 / 35 for
99 % of its duration while the header claims 220 / 60. Two of this repo's best
prints ran that way without anyone noticing.

**Verify both.** A preamble check alone is not verification:

```bash
grep -m1 '^PRINT_START' file.gcode
grep -m1 '^M104 S[0-9]* ; set nozzle temperature' file.gcode
grep -m1 '^M140 S[0-9]* ; set bed temperature'    file.gcode
```

### Which temperatures do we actually want?

Evidence as of 2026-08-22 is that **the stock 210 / 35 is not a defect to fix —
it may be the better profile**, for a specific reason: a 60 °C bed for the first
layer buys adhesion, and dropping to 35 °C afterwards keeps the enclosed chamber
cool. Prints that held bed 60 all the way ran the chamber at 39–40 °C, which is
where PLA heat-creeps and jams the hotend — a failure this repo has hit
repeatedly and has been mitigating by propping the door open.

| print | bed after layer 1 | chamber observed | outcome |
|---|---|---|---|
| MA963 plate | 35 °C | 34–36 °C | best print produced |
| tube_platform plate | 35 °C | ~37 °C | good |
| VIB-01 base | 60 °C | 39–40 °C | (failed for other reasons) |
| saddle / clamps | 60 °C | 37–39 °C | good |

Not a controlled experiment, and the failures had unrelated causes — but the
mechanism is sound and the correlation is consistent. **Recommended default:
first layer 60 °C bed / 200 °C nozzle, then 35 °C bed / 210 °C nozzle.**

---

## 3. Settings that have caused failures here

| setting | safe | what went wrong |
|---|---|---|
| `bottom_shell_layers` | **3–5** | 30 was applied globally on the VIB-01 base (a *local* solidity requirement misread as a global one). 6 mm of solid PLA on the plate; the part peeled. |
| `max_bridge_length` vs model spans | limit **≥** longest span | VIB-01 had 16 mm tunnel roofs and a 20 mm groove roof against a limit of 10. Over-limit spans are **not bridged** — they are laid down as ordinary sparse infill into open air (2 116 such moves in one layer). Spaghetti, dragged by the nozzle. |
| brim width on long parts | 12 mm over ~150 mm | 5 mm is fine for compact parts; widen it as contraction length grows. |

### The rule that prevents both

**The model must declare its longest unsupported span, and the slicer's bridge
limit must be checked against it at slice time.** Where this is implemented
(`vib01_node/slice_revD.py`) the script parses the model's `MAXSPAN=` echo and
refuses to slice on a mismatch, so model and profile cannot silently disagree.

Prefer self-supporting geometry over bridging at all: 45° gables and teardropped
bores need no bridge and no support. See the skidframe keel and the VIB-01 rev D
tunnel crowns for the house treatment.

### Verifying a slice actually prints what you think

Beyond span-vs-limit, the strongest check is to classify every extrusion move
against the model's void map and count **non-bridge extrusion over open air** —
the target is 0. Used on the MA963 files before printing; all four returned 0.
Two traps when re-running it: layer 1 reads as 100 % over-air because it sits on
the bed, and object alignment must be taken from an outer wall **above** the brim
layer (the purge line corrupts a bbox-based offset). Keep an alignment self-test
as the gate on whether the check can be believed at all.

---

## 4. Materials

| material | first layer | rest | chamber | notes |
|---|---|---|---|---|
| PLA Tough+ (bench) | 60 / 200 | 35 / 210 | keep < 40 °C | above ~40 °C the hotend heat-creeps and jams; crack the door on long runs |
| ASA (field/outdoor) | 95 / 255 | 95 / 255 | 50 °C | required for anything outdoors or near heat — PLA Tg ≈ 60 °C |
| PA12-CF | 80 / 280 | 80 / 280 | 60 °C | must be dried 8–12 h at 70 °C or it prints fuzzy and stringy |

**Material choice is not cosmetic.** Parts in sun, on a case exterior, or bolted
near a warm PSU must be ASA. A black PLA part in direct sun exceeds its own glass
transition.

---

## 5. Bed preparation

After any failed or warped print: **wash the plate with soap and water.** IPA
does not lift accumulated glue residue, and residue is a recurring cause of
adhesion loss. Do not add fresh glue on top of old.

---

## 6. Slicing command

Use the OrcaSlicer CLI with the repo's brim profile — **not** `plus4_print.py`,
whose PLA temperature table diverges from the fleet (under review as of
2026-08-22).

```bash
S="$HOME/Library/Application Support/OrcaSlicer/system/Qidi"
/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer --slice 0 \
  --load-settings "$S/machine/Qidi X-Plus 4 0.4 nozzle.json;cw_mes/qidi_xplus4_brim.json" \
  --load-filaments "$S/filament/Bambu PLA @Qidi X-Plus 4 0.4 nozzle.json" \
  --arrange 1 --outputdir . part.stl        # emits plate_1.gcode
```

Then patch **both** temperature sites and verify per §2.
