# seat_rail_fixture — N417ER seat-rail replica segments + straddle clamp (bench)

**Status 2026-10-28, rev 2 (photo).** Javi's photo of the real rail
(`reference/N417ER_rail_and_node_2026-10-28.webp`, the rev D box beside it
for scale) **falsified the profile every VIB-01 part was cut for** (rev B–E
node, Digiducer sidecar, rev 1 of this fixture): the head is a round-top
aluminium bar standing ~14 mm proud of a painted flange plate, with an
undercut lip over a web, hex flange bolts at the rail end and mid-span,
carpet cut around the plate, **no daylight under the rail** (no band path)
and **no seat-stop holes** on the photographed stretch. Rev 1 of this
family (a 2 mm head on a 45-wide flat, bands under the body) is kept
selectable for comparison; everything below is the rev 2 state.

What changed: `rail_interface.scad` (the one file node + sidecar + fixture
share) now carries a `rail_profile` switch with the PROVISIONAL photo
profile; the fixture segments replicate that profile (flange plate, head,
undercut, bolt heads, head set-back) with no band slots; a new
`make_rail_straddle_clamp.scad` is the candidate mounting interface; the
gauge is re-cut to the dimensions that now matter.

**Every rail number is a photo estimate with a ±. Nothing is measured.**
The fixture proves fit among our parts on the rail we *think* we saw;
section 5 is the gate to the aircraft.

## 1. Files

| File | What |
|---|---|
| `../digiducer_mount/rail_interface.scad` | shared rail numbers; `rail_profile = "photo_2026_10_28"` (provisional, default) or `"inferred_2026_08"` (falsified); `rail_section_2d()` = the photo profile |
| `seat_rail_fixture_lib.scad` | fixture engine: base plate + feet, flange plate, rail extrusion, bolt heads, head set-back, engraving, gauge v2, assembly scene; jaw-footprint-vs-bolt-head assert |
| `rail_seg1_node.scad` | **SEG 1 NODE** — rev E base on its 100 mm clamp deck, aft end at datum **E0** x = 40 (jaws 40..70 / 110..140 clear the end-pair bolts at x 6 and the mid-span bolt at x 150) |
| `rail_seg2_digiducer.scad` | **SEG 2 DG-B** — the concept-B pair: Digiducer sidecar on its 48 mm deck at **DG0** x = 44, rev E base at **E0** x = 100, node_gap 8; the mid-span bolt falls between the node's jaws |
| `make_rail_straddle_clamp.scad` | the candidate interface: deck + 4 lip-jaws, `deck_L = 100` (rev E) or `48` (sidecar); `part = deck | jaw | all | print | assembly` |
| `build_seat_rail_fixture.py` | copy-checks jaw/band stations against the source models, exports STLs, ray-casts the exported meshes (crown, flange plate, undercut gap, bolt heads, set-back, clamp pad), renders, plates, slices via `../plus4_print.py slice --check` |
| `rail_seg1_node.stl`, `rail_seg2_digiducer.stl`, `rail_gauge.stl` | print orientation (plate / card on the bed) |
| `rail_clamp_print100.stl`, `rail_clamp_print48.stl` | clamp sets in print pose (deck top-face down, jaws on their outer faces); `rail_clamp_all*.stl` = modelled in place (assembly renders) |
| `plate_fixture_set.stl`, `plate_clamps.stl`, `plate_fitcheck_parts.stl` | bed plates: segments + gauge; both clamp sets; the two already-printed fit-check parts |
| `profile_provisional.svg` | dimensioned cross-section with the clamp, every number from the model echo |
| `preview_*.png` | segments bare / with parts, end view, gauge, clamp assembly / end / print |
| `reference/` | the photo |
| `gcode/` | slices, git-ignored |

## 2. Provisional profile — every number, with its ±

z from the **flange-plate top**, y from the rail centreline. Scale in the
photo: the 45 mm box width and the ~10 mm hex heads; one oblique frame, so
vertical numbers are the softest.

| Feature | Value | ± | Where it lives | What the photo shows |
|---|---|---|---|---|
| Head width | **16** | 3 | `ph_head_w` | round bar, ~60 px at ~3.7 px/mm |
| Head height above the flange plate (crown) | **14** | 4 | `ph_head_h` | clearly proud; foreshortened end face |
| Head thickness (lip underside → crown) | **9** | 3 | `ph_head_t` → `ph_lip_z` = 5 | the bar's end face vs the web below it |
| Crown radius | 8 (= w/2, fully round) | 3 | `ph_head_r` | round-topped end face; could be flatter |
| Web thickness | **8** | 3 | `ph_web_w` | grey strip under the head at the end |
| Undercut per side | 4 (= (16 − 8)/2) | 2 | `ph_undercut` | dark shadow band along ONE side only — **CONFIRM the other** |
| Lip underside angle | 45° | — | `ph_lip_angle` | **assumed** (printable upright); flat is likely — re-cuts the clamp lips |
| Flange plate width | **63** | 8 | `ph_flange_w` | carpet-to-carpet across the painted plate |
| Flange plate thickness | 2 | 1 | `ph_flange_t` | not visible edge-on; thin sheet |
| Flange bolts | hex **9.5 AF** × 4 high | 1.5 / 1 | `ph_bolt_af`, `ph_bolt_hh` | AN3-class; AN4 would be 11.1 |
| End pair | x 6 from the plate end, y ±12 | 3 / 3 | `ph_bolt_end` | one each side of the web at the rail end |
| Mid-span bolt | x 150, y +15, one side only | 30 / 4 | `ph_bolt_mid` | pitch read against the 144 mm box |
| Head set-back | the bar ends **18** before the plate end | 6 | `ph_head_setback` | the end bolts sit in a web-only stretch |
| Band path | **none** | — | — | no daylight under the rail |
| Seat-stop holes | **none seen** | — | (`hole_x0` only for the old profile) | ask for a photo of the other rail / the seat-stop stretch |

Fixture z: plate 0..4, flange plate ..6 (= profile 0), lip underside 11,
crown 20. Asserts (lib): flange plate inside the base-plate lips, bolt
heads on the plate and not under the head unless in the set-back, no clamp
jaw landing on a bolt head, no fit part starting inside the set-back.
`rail_interface.scad` asserts a usable undercut (lip underside ≥ 2 above
the plate) and web ≤ head.

## 3. The interface — what replaces pads + groove + bands

### (a) Straddle clamp — modelled, recommended (`make_rail_straddle_clamp.scad`)
Three-piece T-rail clamp, `preview_clamp_assembly.png` / `preview_clamp_end.png`:
- **Deck** 100 × 56 × 8 bridging the head (channel ±9, bridge 1 mm over
  the crown, a 6 mm **crown pad** on the centreline that bears on the
  round crown). Top face = the mounting deck, **z 23** above the flange
  plate = the node's pad plane. The rev E base bolts to it through its
  **existing interface-B holes** (M4 at x 22 / 93 on the centreline, into
  M4 × 5.7 inserts in the deck); pads flat on the deck.
- **Four jaws** 30 long (two per side, at x 15 / 85), 13.5 tall, each with a
  **45° lip** reaching from the channel wall to y = 6 (web + 2) under the
  head's lip (lip face 0.3 under the lip underside before preload). One
  **M4 × 18 button head** per jaw from the deck top, counterbored flush (the
  heads sit under the node's pads at |y| 16.7..24.3 → **torque the clamp
  before the node goes on**), into an **M4 × 8 insert** in the jaw (2 D).
- **Load path:** bolt tension → jaw lip UP into the undercut (45° wedge,
  self-centring) → head → crown pad DOWN → deck. The jaws float 1 mm above
  the flange plate: **plate and carpet are out of the path**; the rail head
  is in compression between pad and lips, like a vise. Lateral stiffness
  is wedge preload, not clearance.
- **Install:** deck on the crown, slide each jaw in from its side under the
  deck until the lip enters the undercut, run the four M4s down. No sliding
  on from the rail end, no seat removal. Works with a one-sided undercut
  (two jaws clamp, the other two locate).
- **Mass (solid):** deck 49 g ASA / 123 g 6061; jaws 34 / 87; hardware ~10
  → **~93 g ASA on top of the 65 g rev E enclosure** (W&B item; the 70 g
  gate is the enclosure). Sidecar deck 48: ~52 g ASA.
- **Material:** PLA for the bench clamp on this plate; **ASA for ground
  runs**; flight article = the same geometry in 6061 (structures call —
  plastic lips creep under preload; the reference sidecar spec already
  wants a metal-only path).
- **Asserts:** channel roof ≤ MAX_BRIDGE, lip tip ≥ 1 mm above the jaw
  float, wedge rises, jaw top under the bridge (lip touches first), insert
  bore + floor, 2 D engagement, counterbore leaves ≥ 4 mm, deck inside the
  flange plate, jaws on the deck, bolt does not bottom.
- **Uncertainty drivers:** head height ±4 moves the deck height (and the
  node's CG); head width ±3 moves the channel and lip reach; lip angle
  re-cuts the lips; web ±3 moves the lip tip. The clamp is a shape, not a
  part, until section 5 is filled.

### (b) Flange-bolt mount — not modelled, A&P-gated
Replace the rail's end-pair / mid-span flange bolts with longer ones
through a plate (the rev E interface-B clamp plate pattern). Those bolts
are the seat rail's own floor attachment: removing them is maintenance on
a primary occupant restraint (14 CFR 43, A&P + logbook entry), and the
pitch (150 ± 30 to the end pair, one side only) does not match anything on
the node. Keep as the fallback if the undercut turns out unusable (lip too
thin, no undercut on either side, or a lip the AD cares about).

### What changes for the existing parts
| Part | Change | Size |
|---|---|---|
| **VIB-01 rev E base** | **Tweak, zero geometry change for the bench:** sit it on the clamp deck via interface B (the two M4 holes already there), pads on the deck. Flight article: delete the dead interface A (groove + 3 tunnels), which also drops mass; consider merging the deck into the slab once the profile is measured. | small |
| **Digiducer sidecar** | **Redesign of the underside:** its 6 mm slab *is* the rail interface (pads + groove + 2 band tunnels) → replace with two M4 holes at x 10 / 38 (where the tunnels were) and bolt it to the 48 mm deck; the stud axis stays over the rail centreline, the Ø7 stud relief now opens onto the deck (make the deck's centre insert-free there or move the relief). The 6061 flight version becomes a one-piece block with the lips machined in. | moderate |
| **This fixture** | done (rev 2) | — |

## 4. Print — PLA, no support

- **Segments:** plate on the bed. Flange plate and base plate are flat
  first layers; the head's 45° lip undersides are self-supporting; the
  crown prints as a dome; bolt heads are vertical hex prisms. MAXSPAN 0.
  If the real lip underside is flat, print the rail on its side or support
  the lips.
- **Clamp:** deck **top-face down** (flat deck from the first layer; the
  bridge underside over the channel is the one true bridge, 18 mm ≤
  MAX_BRIDGE 20 → the build script passes `max_bridge_length = 23` to the
  slicer); jaws on their **outer faces, lip up** (the 45° lip face is
  self-supporting). Counterbores open downward in print pose (2.5 mm, fine
  at 0.2 layers).
- **Slicer:** `plus4_print.py slice --material pla --brim 5 --check`, 30 %
  infill, 4 walls, 4/5 shells (bottom shells capped at 6). Preamble as
  written by the pipeline: G28 / M190 S70 / M109 S215, verified per file.

## 5. Caliper card — ordered by what moves the design most

Print `rail_gauge.stl` (gauge v2, 130 × 40 × 5): head-width notches
**13 / 16 / 19 × 12 deep** (drop over the crown), **height ladder 10 / 14 /
18** (stand the card on the flange plate beside the head, read which step
the crown reaches), **undercut feelers 2 / 4 / 6 wide × 2 thick** (slide
under the lip), **bolt-AF notches 9.5 / 11.1**, hole pins Ø9.5 / 10.7 kept
for seat-stop holes found elsewhere. Then the caliper, both rails, at the
stations used 2026-10-27 (co-pilot = production node, pilot = Digiducer).

| # | Measure | Provisional | Decides |
|---|---|---|---|
| 1 | **Head height above the flange plate** (crown), and **head thickness** lip-underside → crown | 14 ± 4, 9 ± 3 | deck height / node CG; whether the lips have anything to grab (lip underside must sit ≥ 2 mm above the plate) |
| 2 | **Head width** and **undercut** on BOTH sides: lip overhang beyond the web, lip underside shape (flat / angled / radiused), web thickness | 16 ± 3, 4 ± 2 each side (one seen), 45° assumed, web 8 ± 3 | channel width, lip reach, lip angle — the clamp's whole working geometry; one-sided undercut = two-jaw clamp |
| 3 | **Flange plate width and thickness**, carpet edge gap, paint/bare | 63 ± 8, 2 ± 1 | deck width limit (jaws must stay on the plate), no carpet under anything |
| 4 | **Bolt pattern**: AF, head height, x/y of every head along the usable stretch, pitch to the next, which side | 9.5 AF × 4; end pair x 6 y ±12; mid x 150 y +15 one side | where jaws may sit (30 mm jaws need 30 mm clear per station); alternative (b) |
| 5 | **Seat-stop holes**: present on this rail? where (x from the rail end), Ø, through the head or into the web? | none seen | hole-in-the-clamp-footprint rule; AD note if any gauges > 10.7 |
| 6 | **Head set-back** from the plate end and what the end looks like (end cap? web only?) | 18 ± 6 | how close to the rail end a deck can sit |
| 7 | Material (magnet), rail end accessibility, seat travel over the chosen stretch | aluminium | magnet-base option; install clearance |

Write the numbers into `rail_interface.scad` (the `ph_*` block), rebuild —
the clamp and the fixture refuse to build if the lips cannot engage.

## 6. Hardware

- Fixture: 4 × 1/4-20 × 3/4 in (or M6 × 20) bench bolts + washers per
  segment, or two F-clamps on the lips.
- Clamp (per deck): 4 × M4 × 18 ISO 7380 button head, 4 × M4 × 8 heat-set
  insert (OD 6.0), 2 × M4 × 5.7 insert in the deck for the node's
  interface-B bolts (rev E already specifies those bolts). Sidecar deck:
  same count.
- No bands. The SAE #32 note from rev 1 is void.

## 7. Slice results (2026-10-28, PLA, `plus4_print.py`)

| Job | gcode | Time | Filament | Check |
|---|---|---|---|---|
| Segment 1 (NODE) alone | `gcode/rail_seg1_node_PLA.gcode` | **5 h 55 m** | 77.6 cm³ ≈ **96 g** | preamble G28 / M190 S70 / M109 S215 OK; only the end-gcode park flag |
| Segment 2 (DG-B) alone | `gcode/rail_seg2_digiducer_PLA.gcode` | **5 h 54 m** | 77.5 cm³ ≈ **96 g** | same |
| Gauge v2 alone | `gcode/rail_gauge_PLA.gcode` | 1 h 41 m | 18.1 cm³ ≈ 22 g | same |
| Fixture set: seg 1 + seg 2 + gauge (230 × 252 plate) | `gcode/plate_fixture_set_PLA.gcode` | **13 h 33 m** | 173.3 cm³ ≈ **215 g** | same |
| Straddle clamps: deck 100 + deck 48 + 8 jaws (138 × 170) | `gcode/plate_clamps_PLA.gcode` | **6 h 22 m** | 68.5 cm³ ≈ **85 g** | same; `max_bridge_length 23` for the 18 mm channel roof |

(Rev 1, the falsified profile, was 9 h 25 m / 140 g per segment — the proud
head carries far less plastic than the old 45-wide body.) 0.20 mm layers,
30 % infill, 4 walls, 4/5 shells, 5 mm outer brim, no support.

Grams are cm³ × 1.24 (the Bambu PLA profile carries `filament_density 0`).
The house check's "Print exceeds Y bed (max Y=290.0)" on every file is the
end-gcode park move (`G0 Y290` after `UNLOAD_FILAMENT`); `vib01c_set.gcode`
(printed 2026-07-10) carries the same flag. The two fit-check parts
(`plate_fitcheck_parts.stl`, 5 h 33 m / 70 g from rev 1) are the pieces
already printed 2026-10-24/25 and are not re-sliced here.

## 8. Open questions

- Everything in section 5; in particular the undercut on the second side
  and the lip underside shape, which the clamp lips are cut to.
- Seat-stop holes: none on the photographed stretch. If they exist where
  the node must sit, the deck pad and the jaw lips must avoid them.
- Whether a plastic-lipped clamp is acceptable even for ground runs
  (structures); the 6061 version is the same model.
- The node's CG rises ~9 mm (deck 23 vs the old pad plane 6 above the rail
  foot) — fn proxy unchanged (the clamp is stiff), but the tap test decides.
