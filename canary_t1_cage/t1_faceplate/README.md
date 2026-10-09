# t1_faceplate — tactical face plate template for the T1 cage (concept D)

**2026-09-22 · concept-study part, not a design of record.** A parametric panel
that fills a clear opening `w × h` between 80/20 **20-2020** members (20 × 20,
6.0 slot, black anodized). Owner's brief, verbatim: *"design a tactical looking
face plate that i can use between extrusion, like a template that looks military
tough and tactical."* Everything on it is a working feature — no fake bolts, no
cosmetic-only geometry.

| File | Role |
|---|---|
| `make_t1_faceplate.scad` | The engine: `faceplate(w, h, ...)`, params block, design checks (`echo` + `assert`). |
| `t1_faceplate_render.scad` | Presentation wrapper: one plate in view orientation with its yellow label seated. |
| `t1_faceplate_on_frame.scad` | Assembled view on the concept-D frame — `use`s `../t1_concepts.scad` primitives, **nothing edited**. |
| `build_t1_faceplate.py` | Builds the four D plates + label plates (STL) and the renders; prints the echo record. |
| `slice_t1_faceplate.py` | PLA fit-check slice with the house guards; gcode to a scratch dir, never the printer. |
| `fp_*.stl`, `label_*.stl` | The four plates in **print orientation (face down)** + matching yellow label plates. |
| `renders/` | `fp_*_front/back/iso.png`, `assembled_front.png`, `assembled_rear.png`. |

## What it is

```
faceplate(w, h,                      // CLEAR opening, member face to member face
          mount     = "bolt",        // "bolt" = flight variant | "slot" = fit-check variant
          sides     = [0,1,1,1],     // a member behind [top, right, bottom, left]  (D bays: top open)
          neighbour = [0,1,0,1],     // another plate shares that member -> notches interleave its ears
          vent      = "hex",         // "hex" | "louver" | "none"
          vent_min_cm2 = 0,          // R4.2: 32 where the face is the intake / exhaust (asserted)
          grip      = "top",         // finger scallop edge | "none"
          label     = true,          // dovetail seat for the snap-in label plate
          mark      = true,          // Reticle Delta inlay, auto-off when it does not fit
          slot_edges = "lr",         // slot variant: tongues on left/right or top/bottom
          name      = "")            // tag for the echo line
```
`sides` / `neighbour` are as seen from **outside** the box. Top-level params
`part = "plate" | "label" | "set"` and `label_txt` drive the file directly
(`openscad -D w=84 -D 'vent="louver"' …`).

### Features, and why each one is there
- **45° outer bezel** — 2.0 chamfer on the face edge. Printed face-down that edge is a
  45° overhang, so it is free; it also reads as the concept's faceted language.
- **Castellated flange** (bolt variant) — 10 mm overlap on every member face = half the
  20 mm member, because the *neighbouring plate owns the other half*. The M5 bolts must
  sit on the slot centreline (T-nuts), i.e. right on the flange edge, so each bolt gets an
  **ear** reaching 18.5 mm over the member, and the flange carries a matching **notch**
  where the neighbour's ear lands. Ear slots alternate (left/bottom even, right/top odd),
  the pattern is 180°-symmetric, so **any plate interlocks with any plate** and a plate can
  go in either way up. Bolts per side = `max(2, ceil((L − 24)/60))`.
- **Plug** — 6 mm deep, +0.5 total clearance, enters the opening behind the flange so the
  members take ±X/±Z in **bearing**; the bolts only clamp (R2.4 six directions, R6.6 no
  structural preload on plastic).
- **Perimeter rib + X rib** on the back, 1.6 wide (2 × 0.4 walls per side, no infill),
  9 mm tall — the field skin is 4 mm, the ribs give it its stiffness. The rib wraps round
  the grip notch rather than being cut by it.
- **Vent field** — `hex` 5 AF / 1.6 web honeycomb (no fingertip passes), or `louver`
  = 6 mm straight-through slats on a 12 pitch (the concept's louver; true angled louvres
  do not print face-down and a cabin-interior box does not need rain shedding). Cells /
  slats are omitted where they would cross a rib, the label seat, the mark or the grip, so
  the X reads through the field **because the rib is really there**. Open area is
  computed analytically and echoed (`OPEN_CM2`), asserted against `vent_min_cm2`.
- **Label seat** — the coupon's dovetail pocket, identical numbers
  (`LP_W 44, LP_H 11, LP_T 1.8, LP_CLR 0.15, LIP 0.6`), with a 1.0 back pad so 3.0 mm of
  skin remains behind it; the yellow plate is `make_style_coupon.scad`'s `plate()` (R7.3, R8).
- **Grip** — 24 × 7 stadium scallop through the edge, chamfered. On the D bays the top is
  open (the top long is set back 30 mm), so a finger really goes behind the plate.
- **Mark** — Reticle Delta **inlaid** 0.6 (a raised mark would lift the face off the bed).
- **Counterbores** — Ø10 × 3.0 for a flush M5 BHCS, roofed by a 1.0 flat ring and a 45°
  cone to the Ø5.4 bore so the upside-down counterbore prints without a bridge.

### Which variant flies, and why
**`mount="bolt"` flies.** M5 × 16 BHCS 8.8 (black) through the ears into **drop-in
T-nuts** (20-series, M5, spring/ball type) in the members' front slots — drop-in, so a
plate comes off and goes back **without loosening any frame joint** (R1 swap; a fixed-
panel swap is bolts only, no neighbour disturbed, R1.6). Metal-to-metal preload, plate
clamped under the head, plug in bearing: nothing on it relies on plastic preload hot
(R6.6). Torque per R6.6 (4.5 N·m + Loctite 243 + stripe).
**Sourcing note (2026-09-22, from the 80/20 BOM check):** 8020.net lists **no 20-series
M5 drop-in T-nut** (drop-ins exist for 10/25 M4, 15/40, 30 and 45 only). Two ways to
keep the "no frame joint loosened" property: (a) buy the drop-in from a third party —
generic "2020 M5 drop-in / spring-loaded T-nut" (Misumi HNTT5-5 class) — and confirm
its thread height against the `BOLT_L` assert; or (b) **pre-load slide-in `14122`
nuts** in every face-plate member before the brackets and end caps go on (the BOM
already pre-loads 8 spares this way; add ~25 for the four D plates). The plate geometry
is identical either way. Javi decides at order time; `bom/8020_order_D.md` carries
the same note.
**`mount="slot"` is bench-only.** 5.6 mm tongues (6.0 slot − 0.4, as the T-key neck) ride
the two facing slots, 5.0 engaged, 1.0 lead chamfer; the tongue's underside is a 45°
wedge so it prints face-down. It is retained in ±X and ±Y by the slot lips but **not in
+Z** (it slides out the way it went in) and the sloped underside is line contact — fine
for checking an opening, not for anything that flies (R2.4).

## The four concept-D plates (`build_t1_faceplate.py`)

Concept D (`t1_concepts.scad`, `concept="D"`): frame 300 × 180 × 140, front mullions at
x 104 / 208 → bays **74 / 84 / 62** wide; rear mullions at 60 / 110 → 30 / 30 / **160**.
Opening height **100** = `DZ − 2E` (bottom long top face z 20 → mullion top z 120).

| STL | opening | outline (print) | bolts | vent | open cm² | label |
|---|---|---|---|---|---|---|
| `fp_74_traffic.stl` | 74 × 100 | 94 × 110 × 13 | 6 | hex | 17.3 | TRAFFIC |
| `fp_84_lte.stl` | 84 × 100 | 104 × 110 × 13 | 6 | hex | 19.9 | LTE |
| `fp_62_rtk.stl` | 62 × 100 | 82 × 110 × 13 | 6 | none | 0 | RTK |
| `fp_160_exhaust.stl` | 160 × 100 | 180 × 110 × 13 | 7 | louver | **43.8** (≥ 32, R4.2) | EXHAUST |

All four: `sides=[0,1,1,1]` (top open), `MAXSPAN = 12.5` (the label seat's short side —
the largest face-side roof), M5 × 16 engages the full 4.5 mm of the T-nut thread with the
tip 12 mm past the member face (inside the profile's centre bore, asserted). Every STL:
`Status: NoError`, edge-manifold, face on z = 0.

## Print
- **Orientation: flat, face down** — the outside face gets the bed finish; the bezel,
  ears, notches and grip are 45° bed-edge chamfers; the label seat, mark and counterbore
  roofs are the only face-side recesses (spans ≤ 12.5, bridged). Ribs and plug stand up
  from the skin. **No islands, no supports** (`enable_support=0` verified in the gcode).
- **Material:** **ASA** for the flight plates (R6.1 — a parked SoCal cabin is 60–70 °C;
  PLA sags). **PLA only for the fit check.** Label plates in canary-yellow filament.
- **Process (fit check, `slice_t1_faceplate.py`):** 4 walls, 4 bottom / 4 top shells,
  40 % gyroid, outer brim 6, `max_bridge_length = 17` (= int(MAXSPAN) + 5),
  `bottom_shell_layers = 4` (cap 6). Both vib01 rev D guards enforced.
- **Slice result, `fp_84_lte` PLA (2026-09-22):** **7 h 03 m, 42.71 cm³ (~53 g)**,
  65 layers, 13.0 mm. Preamble verified literally: `PRINT_START BED=60 HOTEND=220
  CHAMBER=0`, `M104 S220`, `M140 S60`. `gcode_check.py`: all pass. **Not printed —
  the owner authorises every print.** (A `vent="none"` fit check would be markedly
  shorter: the 92 hex cells are 92 × 4 perimeters.)

## Tolerances used (house)
M5 clearance 5.4 (house step 3.4 / 4.4 / 5.4) · counterbore Ø10 × 3.0 (BHCS 9.5 × 2.75)
· plug / slide-in clearance +0.5 total · ear-to-notch clearance 1.0 per side · tongue
5.6 in the 6.0 slot, 1.0 lead · label seat +0.15 per side, lip 0.6 (the coupon's
tune-me numbers) · walls 1.6 = 4 × 0.4 · skins 4.0 (≥ 4 mm under every fastener, R6.2).

## Assembly hardware (per plate)
`bolts` × M5 × 16 BHCS 8.8 black + drop-in T-nut 20-series M5 (6 or 7 per plate; ~25 for
the four) · 1 label plate (yellow) · Loctite 243, torque stripe.

## Assumed, not measured (CONFIRM before ASA)
1. **Slot geometry** as already used in `t1_tkey_detail.scad`: opening 6.0, depth 6.0,
   cavity 11.0 — the cavity does not touch this part, the depth sets the tongue (5.0) and
   the bolt tip check. Read from the 80/20 CAD.
2. **Drop-in T-nut thread height 4.5 mm and nut face at the slot floor** (EST): sets
   `BOLT_L = 16`. If the actual nut sits deeper, go to M5 × 20 and re-run the assert.
3. **Front opening height 100** and **no top member** on the D bays (mullions cantilever
   to z 120, top longs set back 30) — so the D plates have three bolted sides. A four-sided
   opening just sets `sides=[1,1,1,1]`.
4. The 84 plate's slice time was taken at 4 walls / 40 % infill; ASA will differ.
5. **Rear exhaust plate vs the SPARE cartridge:** they share the rear mullion at x 100–120.
   The cartridge's thumbscrew return lug in `t1_tkey_detail.scad` (22 tall, full member
   width) is wider than this plate's notch (18): the two must be hardened together — either
   the cartridge lug shrinks to an ear that fits the notch, or it takes the plate's half.
6. A bay holds **either** a cartridge **or** a face plate: this is the blanking / vent /
   fixed-panel object (R1.5), not the cartridge faceplate.
