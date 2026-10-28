# seat_rail_fixture — C172 seat-rail replica segments (bench fixtures)

**Designed 2026-10-28** on Javi's "let's print 2 seat rails we can use to
mount the digiducer and feather to figure out the mounting configuration
before our next flight." Two 200 mm rail replicas on bolt-down base plates,
reproducing the N417ER seat rail **as the VIB-01 family currently models it**
(`../digiducer_mount/rail_interface.scad`, which this fixture *includes* —
one profile, three parts), plus a printed caliper gauge for the aircraft.

**What this fixture proves, and what it cannot.** Banding the rev E
Feather-stack base and the Digiducer sidecar to these segments checks fit
and handling **among our own parts** on the rail *we assumed* — pad seating
over the head, band routing through the tunnels, band size, node-to-sidecar
gap, wrench access, cable exits, torque feel in PLA. It says **nothing**
about the real rail: every rail number below is INFERRED and the flight
on 2026-10-27 flew with the production node on the co-pilot rail without
anyone closing the caliper gate. Section 5 is that gate.

## 1. Files

| File | What |
|---|---|
| `seat_rail_fixture_lib.scad` | the engine: rail profile, body, band slots, seat-stop holes, plate + feet, engraving, gauge, assembly scene. Holds **no** segment layout. |
| `rail_seg1_node.scad` | instance: **SEG 1 NODE** — rev E base centred (aft end at datum **E0** x = 50), band slots at its three tunnels |
| `rail_seg2_digiducer.scad` | instance: **SEG 2 DG-B** — the concept-B pair: rev E base at **E0** x = 22, Digiducer block at **DG0** x = 130 (node_gap 8), five band slots; the sidecar fits alone on its two |
| `build_seat_rail_fixture.py` | build: copy-checks the band stations against `make_vib01_revE.scad` / `make_digiducer_sidecar.scad`, exports STLs, ray-casts the slots/holes/pad plane on the exported meshes, renders, merges plate STLs, slices via `../plus4_print.py slice --check` |
| `rail_seg1_node.stl`, `rail_seg2_digiducer.stl` | print orientation (plate on the bed) |
| `rail_gauge.stl` | N417ER go/no-go caliper gauge (section 5) |
| `plate_fixture_set.stl` | seg 1 + seg 2 + gauge arranged for the 305 × 305 bed |
| `plate_fitcheck_parts.stl` | `vib01e_base.stl` + `digiducer_sidecar_pla.stl` on their own plate (both already printed once — optional second copies) |
| `profile_inferred.svg` | dimensioned cross-section as modelled (between stations / at a band station), every number from the model echo |
| `preview_*.png` | renders (bare segments, segments with the parts and bands, profile end view, gauge) |
| `gcode/` | slices, git-ignored (`*.gcode`), regenerable with the build script |

Render a segment by hand: `openscad -D 'part="seg"' -o rail_seg1_node.stl rail_seg1_node.scad`
(`part` = `seg` | `gauge` | `assembly` | `none`).

## 2. The rail as modelled — every dimension, with its provenance

Coordinates: x along the rail (0 = aft end of the rail body, +x = FWD, arrow
engraved), y across, z up from the bed. The **pad plane** (node z = 0) is the
body top at **z = 20**.

| Feature | Value | Provenance | Where it lives |
|---|---|---|---|
| Head width | **18.0** | INFERRED — rev B/D note "rail head 16–19 wide"; 18 = the sidecar's scene module; leaves 1.0 per side in the node's 20 mm groove | `seat_rail_fixture_lib.scad` `head_w` (the only rail number set here — change it when measured) |
| Head height above the bearing surface | **2.0** | INFERRED — `rail_head_h` in `rail_interface.scad`; the node's groove is 3.0 deep, so 1.0 air over the head | `rail_interface.scad` |
| Groove the head drops into | 20.0 wide × 3.0 deep | INFERRED (same file) — the node/sidecar side of the fit | `rail_interface.scad` |
| Bearing surface (what the 2 × 12.5 pads sit on) | **45 wide** flat, = node width W | INFERRED — *no ledge, shoulder or carpet is modelled*; the pads simply land on a flat 12.5 mm either side of the head, 2 mm below its top | `rail_interface.scad` `W`, `pad_w` |
| Body ("web") | 45 wide × 14 tall solid | FIXTURE ONLY — the sidecar scene module draws a 45 × 6 body; the fixture makes it 14 so there is 8 mm of body in the band loop above the slot | lib `body_h` |
| Flange | 65 wide × 2 step | FIXTURE ONLY — copied from the sidecar scene module (`rail()`: 65 × 2 base) | lib `flange_w/h` |
| Seat-stop holes | **Ø 9.5 at 25.4 pitch**, 8 per segment, blind from the head top to the flange step | INFERRED from literature: 1 in seat-adjust increments; AD 2011-10-09 wear limit 0.42 in (10.7) implies a nominal well under it, 3/8 in assumed. Nobody has put a caliper on N417ER's holes | lib `hole_d`, `hole_pitch`; `hole_x0` per instance |
| Band path | a 16 × 6 slot **under the bearing surface**, floor on the flange step, at each part tunnel station; the band loops part + 10 mm of rail (8 body + 2 head) | **ASSUMPTION** — how a band gets round the real rail (under a raised head? through the web? not at all?) is unknown. Photo it (section 5, item 6) | lib `slot_*` |
| Band stations | seg 1: 63.3 / 98.3 / 133.3 · seg 2: 35.3 / 70.3 / 105.3 / 140 / 168 | COPIED from `make_vib01_revE.scad` `tun_x` [13.3, 48.3, 83.3] and the sidecar's bands [10, 38] + `node_gap` 8; the build script fails if the copies drift | instance files |
| Holes vs bands | seg 1: band 1 **over a hole** (1.8 off), band 2 **between holes** (11.4), band 3 over a hole edge (4.4) · seg 2: 0.8 / 8.8 / 7.0 / 2.3 / 4.9 | chosen so both placements the bank argues about ("clamp over a rail hole" vs "avoid the seat-pin holes under the band") can be felt on the bench | echoed by the model |

The lib asserts the fit it was built for: head + 2 × 0.5 ≤ groove, head ≤
groove depth − 0.5, head within 16–19, slot crown ≤ 6 (self-supporting),
slot ≥ tunnel + 2, ≥ 6 mm of body over the slot, ≥ 10 mm of body between
slots, no slot or hole off the rail end, band loop ≤ an SAE #36 band, plate
not engraved below 2 mm. Seven more come with `rail_interface.scad`.

## 3. Print — PLA, plate on the bed, no support

- **Material: PLA.** A bench fixture that never sees the aircraft or a hot
  cabin; the node's PLA fit-check pieces are the same class. (Anything that
  flies in this family is ASA — not this.)
- **Orientation: as modelled, base plate down.** The pad bearing surface and
  the head top are then top faces (flat, no layer-line steps across the
  pads); the seat-stop holes are vertical bores; the band slots are gabled
  45° from a 0.9 mm wall to a **5.8 mm crown — the only bridge, inside the
  house 6 mm self-supporting limit** (same pattern as the node tunnels after
  the 2026-08-19 bridging postmortem). Feet and lips are in the first layer.
- **Slicer:** `plus4_print.py slice --material pla --brim 5 --check` with
  `sparse_infill_density=30%`, `wall_loops=4`, `bottom_shell_layers=4`,
  `top_shell_layers=5` (bottom shells capped at 6 per the warp postmortem).
  Preamble as written by the house pipeline: `PRINT_START BED=70 HOTEND=215
  CHAMBER=0` — verified by the build script on every file (the vib01 scripts
  use 60/220; both are PLA-sane, the pipeline is the authority here).
- **Elephant foot:** none designed in; the Ø6.5 foot holes and the 16 mm
  slot mouths have ~0.3 mm first-layer squish margin. If the feet bind on a
  1/4 in bolt, ream.

Slice results — see section 7.

## 4. Using the fixture

1. Bolt each segment to the bench through the four Ø6.5 feet (1/4 in or M6
   bolts; M4 with a washer). The plate lips (9.5 mm flat outside the flange
   step) also take an F-clamp. Both segments bolt side by side at any pitch;
   they are independent.
2. **Seg 1:** rev E base, aft end on the **E0** tick (+Y lip), USB exit aft.
   Feed three 5/16 in-wide mini worm-drive bands through the base's
   tunnels and the fixture's slots and tighten. Loop around the closed box
   + rail section is ~46 × 45 → **Ø ~58 mm → SAE #32 (40–64 mm)**; the
   open base (34 tall) is Ø ~57, same band. (The sidecar README already
   corrected the "SAE #8" in the vib01 comments — #8 tops out near 25 mm.)
3. **Seg 2:** Digiducer block, aft end on **DG0**, two bands (loop Ø ~46 →
   SAE #24/#28); optionally the rev E base at **E0** too — that is the
   concept-B pair at the designed 8 mm gap: check the 1 in wrench ring
   (r 30 from the stud), the 48.7 mm stud-to-fwd-IMU-row distance (REQ-1.1
   ≤ 60) and the cable saddle.
4. Record what you learn here or in the part READMEs: band size that
   actually closes, torque feel before PLA creaks (PLA fixture — do not
   torque to the flight number), whether the pads sit flat with the head in
   the groove (a rocking node = the head is proud or the groove is tight),
   USB-C plug reach past the clamp bar, Digiducer cable loop.
5. Nothing learned here transfers to the aircraft until section 5 is done.

## 5. Caliper card — what Javi must measure on N417ER (the real gate)

Print `rail_gauge.stl` (110 × 30 × 5 card): three notches **16 / 18 / 20
wide × 3.0 deep** (= the node's groove) on one edge, pins **Ø 9.0 / 9.5 /
10.0 go + Ø 10.7 no-go** (the AD 2011-10-09 wear limit) and a **Ø8 pair at
25.4 c-c** on the other. Then the caliper. Pilot *and* co-pilot rail, at
the stations actually used (co-pilot rail = production node, pilot rail =
Digiducer on 2026-10-27).

| # | Measure | Fixture assumes | Decides |
|---|---|---|---|
| 1 | **Head width** across the top, at a hole and between holes (gauge: which notch drops over?) | 18 (16–19) | `groove_w` 20 → 16? (the bridging postmortem wants the groove narrower; 20 was sized for an unmeasured 19) |
| 2 | **Head height above the surface the pads would bear on**, and *what that surface is* (rail shoulder / lip / floor skin / carpet) and how wide it is each side of the head (gauge: does the 3 mm notch bottom touch the head before the card lands on the shoulder?) | 2.0 over a 45-wide flat | the whole rev B–E underside: pads at z 0, head 2 under the 3 groove. If the head stands 15–20 mm proud of the floor (a real T-rail), the pads ride on nothing and interface A needs a re-design, not a tweak |
| 3 | **Rail cross-section**: overall height floor-to-head-top, web thickness, flange width, head underside shape (is there a lip a band or a hook could bear under?) | 45 × 14 body on a 65 × 2 flange (fixture only) | band loop size; whether a band can go round the rail at all; the sidecar block depth |
| 4 | **Seat-stop hole Ø** (pins), **depth** (through the head into the web? blind?), edge condition | Ø 9.5 blind | hole-in-the-band-path question; AD compliance note for the logbook if a hole gauges over 10.7 |
| 5 | **Hole pitch** (Ø8 pair) and the **x of the nearest floor-attach rivets/screws** relative to the holes | 25.4; no floor attach modelled | lets the band stations be put over a floor-attach point (bank hygiene rule: never mid-span) and tells which holes end up under a band |
| 6 | **Band path photo**: side view at floor level at the station — is there daylight under the head? under the rail? what did the 2026-10-27 bands actually loop? | slot under the bearing surface | the one assumption this fixture cannot test |
| 7 | **Material** (magnet on the rail: sticks = steel; bank says likely aluminium) and carpet/trim at the station | bare, rigid | magnet-base option dead or alive; carpet in the load path |

Write the numbers into `rail_interface.scad` first (node + sidecar follow),
then `head_w` here; re-run `build_seat_rail_fixture.py` — if the measured
head does not satisfy the lib's asserts the fixture refuses to build, which
is the point.

## 6. Hardware

- 4 × 1/4-20 × 3/4 in (or M6 × 20) bench bolts + washers per segment, or two F-clamps on the lips.
- Bands: 5/16 in (7.94 mm)-wide stainless worm-drive, **SAE #32** × 3 for the rev E box, **#24–#28** × 2 for the Digiducer block (loop numbers above; buy after the bench check closes them).
- Nothing else; the fixture is one piece per segment.

## 7. Slice results (2026-10-28, PLA, `plus4_print.py`)

| Job | gcode | Time | Filament | Check |
|---|---|---|---|---|
| Segment 1 (NODE) alone | `gcode/rail_seg1_node_PLA.gcode` | **9 h 25 m** | 113.0 cm³ ≈ **140 g** | preamble G28 / M190 S70 / M109 S215 OK; only the end-gcode park flag |
| Segment 2 (DG-B) alone | `gcode/rail_seg2_digiducer_PLA.gcode` | **9 h 28 m** | 113.6 cm³ ≈ **141 g** | same |
| Gauge alone | `gcode/rail_gauge_PLA.gcode` | 1 h 13 m | 13.0 cm³ ≈ 16 g | same |
| Fixture set: seg 1 + seg 2 + gauge (230 × 224 plate) | `gcode/plate_fixture_set_PLA.gcode` | **20 h 06 m** | 239.5 cm³ ≈ **297 g** | same |
| Fit-check parts: rev E base + Digiducer sidecar (167 × 45) | `gcode/plate_fitcheck_parts_PLA.gcode` | 5 h 33 m | 56.2 cm³ ≈ 70 g | same |

Grams are cm³ × 1.24 (the Bambu PLA profile carries `filament_density 0`,
so the gcode header says 0 g). 0.20 mm layers, 30 % infill, 4 walls,
4/5 bottom/top shells, 5 mm outer brim, no support. Max z 22 (set) / 34
(fit-check plate). Model MAXSPAN 5.8 (slot crowns) — no true bridge, so
`max_bridge_length` was left at the profile default.

Plate layout (`plate_fixture_set.stl`): seg 1 at the front, seg 2 behind
it, gauge in a third row, 13 mm between objects (two 5 mm brims + 3) —
230 × 224 mm. **Everything on one plate does not pass the house check:**
set + rev E base + Digiducer sidecar makes 290 × 239 (300 × 249 with brims),
inside the 305 bed but outside the 280 mm move envelope
`plus4_print.py check` enforces, and a 25 h single job is a poor bet. So:
the fixture set is one plate (20 h), the two fit-check parts another
(`plate_fitcheck_parts.stl`) — and those two STLs are **the same pieces
already printed 2026-10-24/25** (`vib01e_base`) and sliced 2026-10-22
(`digiducer_sidecar_pla`); print them again only if a second copy is wanted.

Time lever if 9.5 h per segment is too long: 15 % gyroid + 3 walls slices
seg 1 at 7 h 49 m / 84.8 cm³ (tested, not the default) — the body carries
only band compression, so it is acceptable for a bench fixture; the plate
and feet still get 4 bottom shells. The house check's "Print exceeds Y bed
(max Y=290.0)" on every file is the end-gcode park move (`G0 Y290` after
`UNLOAD_FILAMENT`); `vib01c_set.gcode`, which printed on 2026-07-10,
carries the same flag.

## 8. Open questions

- Everything in section 5. The fixture is a replica of an inference.
- Fixture body height (14) and the band slot under the bearing surface are
  fixture choices, not rail knowledge; if the real rail lets a band pass
  only *through* a hole, the fixture's through-holes-into-slot geometry
  already allows threading a band down a hole — try it on the bench.
- `rail_interface.scad` still carries its rev D `--check-rail` note; rev E
  and this fixture both `include` it, so one edit moves all three parts.
