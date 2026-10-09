# canary_t1_cage — CONCEPT STUDY / input kit (2026-09-21)

**Status: concept study, not a design of record.** The owner and Andrew McGlynn
are designing the T1 cage; this directory is an **input kit** for them: the
arithmetic, three low-fidelity massing concepts with the swap mechanism made
legible, the requirements page, the STEP envelopes, one printable style coupon.
Everything here is an option with its trade-off stated. **Nothing was sent to
the printer.**

| File | Role |
|---|---|
| `REQUIREMENTS.md` | **Read first.** The one page that survives any concept change — every requirement with its number. |
| `envelope_check.py` · `t1_params.py` | The arithmetic: inventory, size class, print class, load cases, thermal, swap steps. `exit 0` = every hard check closes. |
| `t1_concepts.scad` · `t1_mark.scad` | Four massing concepts in one file: `concept="A"|"B"|"C"|"D"`, `swap=<module>`, `pull=0..1`, `lid=0..1`, `panel=0..1`, `label_set="product"|"show"`. |
| `t1_tkey_detail.scad` | **Concept D's load-bearing detail**: printed T-key in the 20-2020 slot, thumbscrew into a T-nut, pull tab, pigtail (`view="plan"|"iso"`). |
| `renders/` | Hero and mid-swap renders of A / B / C / D, black + canary yellow; `D_tkey_detail_*` for the slot detail. |
| `cad_exchange/` | True analytic B-rep STEP envelopes (measured components, `EST_` placeholders, `PERCH_` stack, `CANON_` rod interface) + their README. |
| `make_style_coupon.scad` · `coupon_*.stl` · `*_PLA.gcode` · `slice_coupon.py` | The **style coupon** — the only thing in here meant to be printed (after the owner's go-ahead). |
| `t1_faceplate/` | **Tactical face plate template** (2026-09-22): `faceplate(w, h, mount="bolt"\|"slot", vent="hex"\|"louver"\|"none", …)` fills any opening between 20-2020 members; castellated interlocking bolt flange (M5 BHCS → drop-in T-nuts, the flight variant), 6 mm plug in bearing, X-ribbed back, hex/louver field with the open area echoed, coupon label seat, grip notch. Four D plates (74 / 84 / 62 front, 160 rear exhaust louver ≥ 32 cm²) as face-down STLs + renders; its README has the parameter list and the CONFIRM items. |

---

## 0. What should change the owner's mind before ~100 print hours go in

**2026-09-21 update — concept D, 80/20 20-series black extrusion frame, is the DECIDED structural direction.** The two things it changes and the one thing it costs:

- It makes R2.2 / R2.3 native: the belt goes round anodized 6105-T5 members (241 MPa yield); nothing structural depends on printed preload any more (§5D). The 281 mm bed rule and the 12 h plate rule stop applying to the structure.
- **It costs ~1.2 kg.** The frame as drawn is **1.67 kg** (2.58 m of 20-2020 at 0.4411 g/mm = 1.14 kg, plus 24 brackets, 40 T-nuts, ~64 M5) against A's 0.90 kg printed shell — gross **~4.5 kg vs the 3.7 kg of R7.2**, and still 3.9 kg without the UHR204 hub. R7.2 was the heaviest *printed* concept, not an aircraft limit; the owner should restate it knowing D is a 4–4.5 kg unit. Every load case still closes at 4.52 kg (18 g fwd = 798 N, rod MS 1.5).
- **The T-slot is a track along its member**, so front-loading drawers would need Y-direction runners per bay (+0.6 kg). D therefore drops its peripheral cartridges in **from the top between vertical mullions** (Z-direction track, keys in the mullions' facing slots), and slides the battery in **along X from the end** on the bottom longs' inner slots. That decision shapes the whole frame (§5D) and is the first thing to argue with.


1. **The UHR204 hub is 30 % of the electronics mass and the largest footprint in the box.** 139 × 87 × 35, 10–30 VDC, datasheet weight 0.64 kg (line shared with the 7-port model — probably high, still heavy). It buys 15 N high-retention USB ports. The same retention is available as **screw-lock USB cables into the Orin's own ports** or a **panel-mount locking USB bulkhead** at a fraction of the mass and volume. Decide whether the hub is a requirement or a T0 expedient before sizing a bay for it. [`envelope_check.py` §1]
2. **Strength is not the discriminator; creep is.** Every printed stress in the load cases is 1–2 orders under allowables. What fails hot (parked SoCal cabin, 60–70 °C) is *preload*: clamped rods, thumbscrews into heat-sets, snap fits. The cage needs **metal in the axial rod path** (shaft collars / M12 end hardware) and a latch **plus** strap on the battery — those are the two places friction is currently doing structural work. [§4b, §4d]
3. **The rods on top cost you top access.** Concept A as drawn has 24.5 mm under the rods; a lift-off Core lid does not clear — it has to slide out under the rods. If the owner's T0 experience says "the Core must open from the top", the rods go to the bottom (B) or the middle (C), and the belt path changes with them. This is the first "open to T0 experience" question below.
4. **Sealed is impossible, again.** ~24 W in any of the three shells reaches 76–90 °C interior at 35 °C ambient. The airflow has to be designed, and the battery must sit outside the Orin's exhaust. [§5]
5. **Nothing fits the bed in one piece except C.** A needs one designed seam (285 > 281), B needs one (300 > 281). Seams go at frames, never mid-panel. [§2]
6. **The IMU rule is non-negotiable in all four**: a rigid keyed datum on the rod-tied member with captive screws — never a cartridge, never a rail. Attitude quality is the product. [R3]

---

## 1. Envelope / feasibility (the arithmetic first)

`python3 envelope_check.py` — full tables. Summary:

| | A CARTRIDGE RACK | B OPEN BOOK | C ROD PODS |
|---|---|---|---|---|
| body X × Y × Z (mm) | 285 × 175 × 100 | 300 × 262 × 86 | 316 × 154 × 150 (8 pods) |
| overall incl. rods | 400 × 187 × 143 | 400 × 262 × 110 | 400 × 154 × 150 |
| longest part vs 281 bed | **285 — seam** | **300 — seam** | 148 — fits |

**D EXTRUSION FRAME (added 2026-09-21):** body 300 × 180 × 140, overall 400 × 180 × 174 incl. rods; longest *printed* part 134 mm; printed parts ~420 g / ~41 h / 5 plates; **frame 1.67 kg**; gross **~4.5 kg**. Full numbers in `envelope_check.py` §3b.
| print class (ASA g / h / plates) | ~900 g / ~89 h / 9 | ~1230 g / ~121 h / 13 | ~1060 g / ~104 h / 11 |
| gross incl. electronics, rods, hardware | ~3.3 kg | ~3.7 kg | ~3.5 kg |
| sealed interior @ 35 °C (must vent) | 90 °C | 76 °C | 79 °C (no shell) |

Electronics + harness ~2.13 kg (hub 640 g EST, battery 640 g EST, bare Orin 250 g
EST); rods 2 × 400 mm Ø15 × 2 Al ~176 g. Pelican build for comparison ~3.1 kg.
C172: baggage door 387 × 559, baggage limit 54 kg — none of this is size- or
mass-critical in the aircraft; **the printer bed is the binding size constraint.**

Print-effort figures are class estimates (skin area × thickness × solidity,
scaled by the repo's own sliced ratio 0.105 h/cm³ from `orin_tactical_case`),
±30 %. Nothing in the concepts was sliced — deliberately: they are massing
models without insert bores or joints.

## 2. Load cases and the restraint path

Design gross 3.66 kg (heaviest concept). Flight +3.8 g × 1.5 → 205 N; 9 g fwd →
323 N; **18 g fwd margin case → 646 N**. Carry-on restrained by belt/straps,
nothing attaches to the airframe.

- **Rods (metal) carry the belt.** 18 g as a mid-span load between yokes 230 mm
  apart: 79 MPa in a Ø15 × 2 6061 tube vs 240 yield — MS 2.0. Belt webbing
  (≥ 6.7 kN) is not the limit.
- **Rod → print, transverse:** 4 canon stations, 0.54 MPa bearing at 18 g. Fine.
- **Rod → print, axial (the 9 g direction): friction only.** Fresh, 8 × M3 at
  0.6 N·m gives ~2000 N slip capacity vs 323 N; hot and aged the preload cannot
  be relied on → **requirement: positive axial stop in metal** (Ø15 split
  collars against a yoke face: 0.75 MPa at 18 g; or M12 end screws if the
  SmallRig rods are M12-threaded — CONFIRM).
- **Carry by the rods (3 g swing):** 13.5 N per cap insert in tension vs ~150 N
  hot pull-out — MS 10.
- **Heaviest swappable: battery + carrier 0.74 kg → 131 N at 18 g.** In A the
  fore-aft load goes into bay walls in bearing (0.019 MPa) *if* the unit is
  belted rods-fore-aft; a CFI will turn it 90° one day, so the **latch and a
  secondary strap must each hold 131 N in any axis** (one M4 captive
  thumbscrew into a heat-set ≈ 250 N hot: MS 0.9 alone — hence the strap).
- Allowables used (hot, aged, FDM knock-down): ASA 5 MPa interlayer tension /
  10 MPa bearing; PA12-CF ~3× that. Everything above is 1–2 orders under.

## 3. Thermal

~24 W sustained (EST: Orin 15, Traffic 2.5, hub 2, LTE 2, rest < 3). Sealed:
76–90 °C interior. Vented: dev-kit fan throat ~10.6 cm² → **≥ 32 cm² each of
intake and exhaust** (house ≥ 3×); at ~5 CFM the bulk air rise is 8 K →
interior ~43 °C at 35 °C ambient. Rules: intake ducted to an exterior grille,
exhaust on a different face, **battery upstream of or outside the Orin exhaust
behind a partition**, nothing printed in the fan keep-out. Parked-cabin soak is
an unpowered survival case for the material, not an operating case.

## 4. Material recommendation

**ASA for the shells and cartridges** (Tg ~100 °C, heated-chamber warp control,
this repo's most-printed hot-cabin material, matte by construction).
**PA12-CF for the parts that hold preload hot**: rod yokes, IMU datum, battery
latch — HDT > 150 °C, ~3× ASA strength, and it has printed successfully here once
dried (`slimrig_mounts` rear antenna mount). Its cost is hygroscopy (dry, print,
recondition) and a 280 °C nozzle; use it on the few small parts, not the shells.
**Li-ion bay:** the QIDI profile set includes **PC-ABS-FR**; print the battery
bay (or its liner) in it, or line an ASA bay with 0.5 mm aluminium sheet. The
argument: the bay is the one printed part that could see a cell vent, and a
partition that chars rather than drips buys the seconds a pilot needs. **PLA
only for the style coupon and fit checks — it never flies** (FLEDGE rule).

## 5. The four concepts — options with trade-offs (D is the decided structural direction)

Renders in `renders/`. Same file, `concept="A"|"B"|"C"`; `swap="TRAFFIC"`,
`pull=0.75` shows a module leaving.

### A — CARTRIDGE RACK (`A_cartridge_rack_*.png`)
Core chassis on the two-rod spine (rods on top = handle, belt path, antenna
rail). Canary Core (bare Orin on the hub, power distribution) inside; RTK / LTE
/ TRAFFIC / CABIN CO / SPARE are **front-loading keyed cartridges on rails, one
captive thumbscrew + one pull tab each**, a short locking pigtail to a patch
point inside; the battery is a larger cartridge on the same face. Core lid
slides out rearward under the rods (finding: a lift-off lid does not clear).

### B — OPEN BOOK (`B_open_book_*.png`)
A shallow tray on the rod keel (`tube_platform` lineage), hinged faceted lid,
**everything on one visible plane on the 10 mm M3 cheese grid, each component on
its own carrier held by two captive thumbscrews**. Best inspection; largest
plate; the lid is the whole top so cable discipline is by carrier layout only.

### C — ROD PODS (`C_rod_pods_*.png`)
No shell. **One faceted pod per function, each a canon tube plate clamped to
the rods with the validated cap**, plugged into a harness trunk by one locking
connector. Every part fits the bed; most reconfigurable; but a pod swap is four
cap screws with a driver, and every pod has the axial-friction problem
individually.

### D — EXTRUSION FRAME (`D_extrusion_frame_*.png`, `D_tkey_detail_*.png`) — DECIDED direction
**FIXED LAYOUT 2026-09-21 (Core path):** the two set-back top longs and the IMU cross are deleted — 17 → **14 members, 1.96 m, frame 1.40 kg, gross ~4.25 kg**. The top plane is the two full-width end ties only, so the Core has a 200 × 140 lift-out once the rod-yoke plates are off, and a zero-tool path: the Core tray is an end-loading cartridge on the bottom longs' inner slots from the −X end (its faceted end bezel is the intake louver) — one thumbscrew, pull, unplug (`D_extrusion_frame_swap_core.png`). The IMU datum moved into the rear aluminium yoke plate on the rear end tie. Details and the cut diagram: `bom/8020_order_D.md`. The paragraph below describes the superseded 17-member draft where it says otherwise.

**80/20 20-series, black anodized** (`20-2020-Black-FB`; plain `20-2020` for the fit-check frame). Draft: 17 members, 2.58 m: bottom rectangle 300 × 180, four corner posts, two full-width top end ties, two **top longs set back 30 mm** behind each face (so the top plane closes behind the cartridge line and the Core is reached through the open top between the rods), one IMU cross member, four 100 mm **mullions** (two front, two rear) cantilevered off the bottom rails. Printed parts shrink to: 5 cartridges, the battery carrier, 2 louvered inserts, the Core tray, 2 rod-yoke plates, the IMU seat, faceted bezels/label plates.

**The T-slot cartridge (the load-bearing element — `t1_tkey_detail.scad`, `envelope_check.py` §3b):**
- **Key:** printed with the cartridge on each side wall; neck **5.6 wide** (6.0 slot − 0.4) = 14 lines of 0.4, head **10.4 × 2.0** in the 11.0 cavity (cavity to be read from the 80/20 CAD before cutting), **88 mm engaged** over the 96 mm cartridge, **1.0 mm lead chamfer** both ends, layer lines *along* the neck (the shear plane never crosses layers). Worst load 131 N per pair (battery class at 18 g): 0.13 MPa shear, 0.12 MPa lip bearing — 40× under the ASA allowables. Why 6 mm: a 5.6 neck carries a lead chamfer and survives a dropped cartridge; a 3.0 neck (15-series) is 7 lines and chips.
- **Six directions:** keys in two facing slots give ±X and ±Y; the bottom rail gives −Z; **+Z is the one captive M5 thumbscrew** through the faceplate return into a slide-in T-nut in the mullion's front slot (metal-to-metal preload, washer face on the plastic). Keyed by a bay-specific rib on the tray floor so the wrong cartridge bottoms out 4 mm proud and the thumbscrew cannot reach its T-nut.
- **Pull tab** (yellow, 10 × 8) on the faceplate; **one locking pigtail** per cartridge to a patch point on the Core tray, ≥ 20 mm jacket grip before the connector.
- **vs mini ball-bearing slides** (Accuride / Sugatsune 100–150 mm class): +40–80 g and +4 screws per bay, a 10–13 mm side gap, steel in a hot cabin, rattle unless detented; they earn their place only for a full-extension drawer over ~1 kg. Nothing here is. The slot is already the rail: zero added parts, zero gap. 80/20's own drawer slides start at 375 mm travel / 100 lb — wrong scale, not used.

**IMU datum (best of the four):** a machined-Al (or PA12-CF + washers) seat on the rear top cross member, **2 × M5 into T-nuts + one dowel into a drilled hole in the extrusion** — the reference is a straight, anodized, ±0.1 mm extrusion face tied by four M5 joints to the whole frame, not a printed rib. Repeatability is set by the dowel, not by print tolerance. Re-cal after a swap is still mandatory.

**Hot preload in plastic — what remains:** nothing structural. Belt → frame members (metal); cartridge → M5 thumbscrew into a steel T-nut (the ASA faceplate is only clamped, 0.2 MPa under a washer); keys carry bearing, not preload; battery latch → T-nut, strap → frame member; the IMU seat is metal or washered PA12-CF; the canon rod caps still clamp the rods, but the rods are now handle + antenna rail only and are outside the restraint path. Creep can loosen a label plate and nothing else.

**Bolted joints under vibration:** M5 8.8 into steel T-nuts, **4.5 N·m + Loctite 243 + torque stripe**, re-check at 10 h and every 50 h; a corner sees ≤ 162 N at 18 g against ~2 kN per joint. 15-series M3 sheet brackets (160 N allowable) would be *at* their allowable at one corner — one of the three reasons 20-series won (with the 6 mm slot and the SolidWorks-native 80/20 CAD library).

**Thermal:** open top between the set-back longs = fan intake straight down onto the Orin; **exhaust = a printed louvered insert** (160 × 96, 6 mm louvres, ≥ 32 cm² open) dropped into the rear mullion slots on its own T-keys; a second louvered insert in the −X end feeds the hub/battery level; the battery bay at +X is upstream of the Orin. Panels come out the same way as a cartridge.

**Look:** black extrusion reads as the tactical frame by itself; the printed faceted bezels (cartridge faceplates, end bezel, yoke plates) and the yellow thumbscrews / pull tabs / rod caps / label plates carry the accent. Renders: assembled, `swap="TRAFFIC"` and `swap="BATTERY"` mid-swap, rear with the exhaust panel lifted, top view of the Core.

### E — FLAT DECK 406 × 279 (`E_*.png`, `LAYOUT_E.md`) — owner's direction 2026-09-24, the current build path
Everything on ONE level on the owner's existing 2020 rectangle (406 × 279, centre member, two 173 × 239 bays): two
full-bay printed ASA trays (castellated ears, M5 T-nuts, thumbscrews on the Core bay), the battery on a V-mount plate
in the lap-belt band, MTi-3 on an aluminium corner plate, the hub as the cable node, the Orin fan open to the sky;
four 100 mm 2020 posts + two printed yoke bridges carry the SmallRig rods = handle, antenna rail (MA963, LTE/GNSS
patches), lid carrier. Layout rules, cable table and the trays' structural role: `LAYOUT_E.md`. Gross ~4.4 kg
(`envelope_check.py` §[4E]); 80/20 delta `bom/8020_order_E.md` ($140.44 + COTS V-plate).

**E rev C — full-height cage (option, 2026-09-25, `LAYOUT_E.md` rev C, `render_E_revC.py`):** the posts go to 222 and
carry a top 406 × 279 ring (top-rail top z 265, overall 268), so the dome, MA963 and stubbies sit 15.6 / 71 / 84 mm under
the top. The trays are unchanged. The rod level is rearranged because the real MA963 (146 × 134 on a 173 × 180 plate)
never fitted rev B's rod budget. Cost: +1.26 kg (5.70 kg gross), +$221 of 80/20, and a 4-20° rail shadow on the GNSS
dome (13 % of the sky above a 10° mask). Restraint stays on the bottom longs; the top rails are the carry handle only.
Recommendation: build 222 posts and the rev C rod level now, and bolt the ring on only after a static RTK A/B test.

### Scorecard (honest, class judgements)

| criterion | A CARTRIDGE RACK | B OPEN BOOK | C ROD PODS | D EXTRUSION FRAME | **E FLAT DECK (current)** |
|---|---|---|---|---|
| peripheral swap: steps / tools | **3 / 0** | 4 / 0 | 6 / 1 (hex key) | **3 / 0** (thumbscrew, lift, unlock) | 4 / 0 (unlock, 4 screws, lift) — or the whole tray on 6 thumbscrews |
| Core swap: steps | 8 (lid slides under rods) | 4 | 6 | **3 / 0** (end-loading tray: thumbscrew, pull out the −X end, unplug) | **3 / 0** — it is on the open top level; unplug, unscrew, lift |
| inspection visibility | bays only; Core needs the lid out | **everything at once** | good per pod, no overview | Core visible through the open top; bays by pulling a cartridge | **everything visible at once** (B's virtue without B's lid) |
| IMU datum rigidity | on the rear yoke, rod-tied: very good | on a spine boss bolted through to the keel: good | on its own canon plate, rod-tied: good, but a 4-screw clamp is the datum | **best**: bolted + dowelled to an anodized extrusion face tied by M5 joints to the whole frame | Al corner plate bolted to two members: as good as D, cheaper |
| thermal path | designed duct: intake top grille → fan → side louvres; battery in its own bay | lid off = open; lid on needs a full grille lid | free — no shell | open top intake → rear louvered insert; battery upstream at +X end; inserts swap like cartridges | **free**: open deck, fan exhausts into cabin air; battery two bays upwind |
| mass / size class | 3.3 kg, 5.0 L body | 3.7 kg, 6.8 L | 3.5 kg, long | **4.5 kg** (3.9 without the hub), 7.6 L — the cost of metal | ~4.4 kg, 406 × 279 × 190 — the largest footprint |
| print effort | ~89 h, one seam | ~121 h, one seam, 300 mm lid | ~104 h, no seams, 30+ parts | **~41 h, no seams**, nothing over 134 mm; + 2.58 m of extrusion to cut and 48 joints to torque | ~40 h (2 trays + 2 yokes), frame already built |
| cable discipline | **best**: patch points per bay, one trunk | by layout; lid-open cables are the show | trunk on the outside; most exposed | as A: patch points on the Core tray; T-slots double as cable channels with snap-in covers | star at the hub, runs in the outer slots under `12004` covers, combs on the trays — most exposed, most inspectable |
| looks (owner's brief: drawer tower, faceted bezels, one accent) | **strongest** — the reference image, literally | flight-case; the lid mark is the hero | tactical, "system on rails"; busiest | black frame + faceted printed faces: the most credible to a CFI, the least "printed" | open tray: honest, technical; needs a lid to look finished (the rods carry one) |
| restraint (belt round rods) | rods on top: belt over the top, unit sits on feet | rods below: belt under, unit sits on the rods | rods mid: belt round the rod ends | **belt round the frame's bottom members** — native metal path, no printed clamp anywhere in it | lap belt over the battery + straps round both long members — native, and the belt holds the heaviest item directly |

### Recommendation for the human CAD team to harden: **D frame + A cartridges + bolted-and-dowelled IMU**

D wins on the axes that matter to a senior CFI and to the T0 removal history: the restraint path is metal end to end, nothing structural rides on printed preload, the IMU datum is the best of the four, the peripheral swap is 3 steps / 0 tools, and the print effort halves with no seams. A's contribution survives inside it: the keyed, labelled, one-thumbscrew-one-tab-one-pigtail cartridge is the same object, only its rail changed from a printed slide to the extrusion slot. What D gives up and the owner should accept knowingly: **~1.2 kg** over the printed shell (restate R7.2), the top-loading rack instead of front-loading drawers (a consequence of T-slots being tracks along their member), and a frame with 48 torqued joints that need a torque-stripe discipline. Two things could still overturn it: if T0 says the Core is the module opened most, the set-back top longs must widen (or the rods move) so the Orin lifts straight out; and if the owner's rod inventory or the CFI's restraint preference wants the belt on the rods, the rods must be bolted to the frame through metal (yoke plates in Al, not print) — cheap, but decide it before the CAD team draws the yokes.

The 15 mm Misumi HFS3-1515 alternative (0.34 kg/m, I = 2800 mm⁴, 3.4 mm slot, M3 sheet brackets rated 160 N) was considered and rejected: it saves ~0.5 kg of frame but gives 41 % of the stiffness, a 3.0 mm printed key neck, and corner brackets at their allowable at 18 g.

## 6. Style, labels, coupon

Language (from the owner's references): faceted 45° bezel round every opening;
matte black with **one** accent, canary yellow, only on thumbscrews, pull tabs,
rod caps, label plates; recessed X-brace pockets that are real stiffening;
recessed label plates in stencil caps; the Reticle Delta mark embossed
(`t1_mark.scad` transcribes the brand SVG to native geometry — 11 ring segments
+ dot, four-facet delta at two heights).

**Label sets** (`label_set`): `product` = CANARY CORE / TRAFFIC / CABIN CO / RTK
/ LTE / POWER / IMU / SPARE (patent pending, filed 2026-08-17 — usable);
`show` = T1-00 ALPHA … T1-08 INDIA, kept as an **option** because the
disclosure ledger stays strict and anything beyond the provisional's content is
not covered. Plates snap in, so the set is a two-minute swap.

**Style coupon** (`renders/style_coupon_set.png`): 90 × 70 × 5 panel with a
faceted bezel opening, X-brace pocket, dovetail snap seat, embossed mark,
recessed fastener well and chamfered slot mouth; plus two yellow label plates
(TRAFFIC, T1-01 BRAVO). Print face-up, zero supports, PLA.
Sliced `slice_coupon.py` (OrcaSlicer CLI, `cw_mes/qidi_xplus4_brim.json`, NOT
`plus4_print.py`): **panel 2 h 25 m / 16.0 cm³ (~20 g)**; **plates 18 m /
1.9 cm³** in yellow. Verified literally in both gcodes: `PRINT_START BED=60
HOTEND=220 CHAMBER=0`, `M104 S220`, `M140 S60`, `max_bridge_length=8` (from the
model's `MAXSPAN=3.6` echo), `bottom_shell_layers` 4 / 3 (cap 6). `gcode_check.py`
passes both. The snap lip (`LIP = 0.6`, `LP_CLR = 0.15`) is the thing the coupon
exists to tune. **Not printed — owner authorises every print.**

## 7. Carry-over from earlier printed parts

| From | Carries over | Note |
|---|---|---|
| `slimrig_mounts` | canon rev-B rod interface (Ø15.0+0.4 troughs, 60 c-c, caps with 2 × M3×25 into cap-face inserts), all printed cap spares, the whole antenna-mount family on the rods | untouched; every concept clamps with it |
| `orin_tactical_case` | the **Perch's** enclosure — a ground unit, no flight loads, not bound by PLA-never-flies. Shared with the T1 only: the sealed-box thermal method (U ≈ 2.3 W/m²K), the lug-capture idea (bearing takes lateral load so screws only hold down), the M2-washer creep finding (→ washers under every thumbscrew), the slice-harness guards | its keel prints the Perch, not the T1 |
| `skidframe` | the rod-tax lesson (28 mm of height to the rod interface), the closed-ring stiffness argument, the "one 26 h hull is one 20 h failure" warning → nothing over ~12 h here | |
| `tube_platform` / `cheese_plate_106x90` | the 10 mm M3 grid pitch (brute-forced against the real hole spans) — B is built on it | |
| `vib01_node` rev D | the two print guards, applied in `slice_coupon.py` | |
| `co_sensor` | vented tray + the Ø4.216 hole correction for the CO stick | the CABIN CO cartridge inherits it |

## 8. Open to T0 experience — decisions most likely to be overturned by someone who has flown the box

Not guessed here; these are the questions for the owner and Andrew.

1. **What was opened most in T0, and from which side?** Decides rods-top (A) vs rods-bottom (B) vs mid (C), and whether the Core needs top access.
2. **Which connectors actually walked out or failed** (USB-A, barrel, SMA, JST)? Decides whether the UHR204 stays, and the locking-connector standard per pigtail.
3. **What needed in-flight access** (power switch, status LEDs, SD, a reset)? Decides the I/O face content and whether any indicator must be visible with the belt on.
4. **What failed mechanically** (a strap, a foam block, a standoff, a cable tie)? Decides the retention hardware class.
5. **Cable strain**: which cable was replaced and why (the vibration cable is on record) — sets the strain-relief and service-loop rule per pigtail.
6. **Heat**: was anything hot to the touch after a flight; did the Orin throttle; how hot was the box after a parked afternoon? Calibrates §3.
7. **How is it carried to the aircraft and where does it ride** (rear seat, baggage 1, footwell)? Sets the belt geometry and whether the rods should protrude as a handle.
8. **Does the LTE modem live inside the Orin housing or as its own cartridge?** (EG25-G pattern is measured; its home is not.)
9. **Battery: is a V-lock plate wanted** (tool-free, positive) or a strap-and-tray bay?
10. **Is the Vibration node's cable stowage on the cage, and how long is the cable?** (external node, locking connector per the T1 memo.)

## 9. CONFIRM list (ranked)

0. **Concept D specifics (2026-09-21):** the 20-2020 slot cavity width (11.0 assumed — read from the 80/20 CAD model), whether `20-2020-Black-FB` lead time fits the FLEDGE build week (plain `20-2020` for the fit frame), and the owner's restated mass ceiling (R7.2) now that D reads ~4.5 kg.
1. **Bare Orin dev-kit height with heatsink and fan, fan diameter and position** (EST 36 tall, Ø44 fan). Sets every Core bay.
2. **UHR204 keep / drop** (§0.1). If kept: port face, mounting-ear pattern (not in the datasheet), real mass.
3. **V-mount battery** outline and mass calipered; V-lock plate or tray.
4. **Rod lengths owned** and whether the ends are M12-threaded (axial stop design).
5. **EG25-G home** (inside the Core housing or a cartridge).
6. **Connector standard per pigtail** (JST-GH / screw-lock USB / SMA) — harness spec v0 (T1 memo C5) must exist before any bay is dimensioned.
7. **Board outlines** for BNO085 and EG25-G (patterns are measured, outlines are not); CO stick hole position.
8. **FlyCatcher, CO stick, power-distribution masses and dissipation** (EST).
9. **Print material**: ASA stock on hand; PA12-CF dried; PC-ABS-FR availability for the battery bay.
10. **Where the unit rides in the C172** and the belt/strap it will use (sets the yoke spacing, 230 mm assumed).

## 10. Rough totals for a full build (class, from `envelope_check.py` §3)

| | parts (printed) | print hours | ASA filament | hardware class |
|---|---|---|---|---|---|
| A CARTRIDGE RACK | ~22 (chassis in 2, lid, 6 cartridges, 2 yokes, 4 caps, IMU datum, label plates) | ~89 h, 9 plates | ~0.9 kg | ~40 M3 heat-sets, 8 M3×25, ~12 captive M3/M4 thumbscrews, 2 Ø15 collars, 1 strap, ~10 locking pigtails |
| B OPEN BOOK | ~23 (tray in 2, lid in 2, 8 carriers, keel, 4 caps, IMU boss, plates) | ~121 h, 13 plates | ~1.2 kg | ~60 heat-sets (grid), 8 M3×25, 16 thumbscrews, 2 lid latches, hinge pin |
| C ROD PODS | ~41 (8 pods × body + plate, 16 caps, trunk, IMU plate, plates) | ~104 h, 11 plates | ~1.1 kg | 32 M3×25 + 32 heat-sets (caps), 8 collars/keys, trunk connectors |
| **D EXTRUSION FRAME** | ~18 printed (5 cartridges, battery carrier, 2 louver inserts, Core tray, 2 yoke plates, IMU seat, ~6 bezels/plates) + 17 cut members | **~41 h, 5 plates** | ~0.4 kg + 1.67 kg frame | see the 80/20 BOM below |

### Concept D — 80/20 BOM: **orderable list in `bom/8020_order_D.csv` + `bom/8020_order_D.md`** (8020.net-verified part numbers and prices, 2026-09-21; black total **$368.95**, plain $272.73, 14 members / 1.94 m; mechanism renders `renders/D_mechanism_*.png` + `renders/D_mechanism_README.md`). The class table below is superseded by that file.

| Item | 80/20 part | Qty | Class cost |
|---|---|---|---|
| Profile 20 × 20, four open T-slots, 6063-T6 per 8020.net, full-black anodized | `20-2020-Black-FB` (0.4411 g/mm, A 159 mm², I 6826 mm⁴, slot 6.0) — plain `20-2020` for the PLA fit-check frame | **1.94 m** in 14 cuts: 2 × 300, 2 × 140, 2 × 130, 8 × 100 (fixed layout 2026-09-21/22) | $64 black / $25 plain + 14 × $3 cuts |
| 2-hole inside corner bracket, 20-series, black | `20-4119-Black` | 24 (8 bottom corners, 8 top, 4 mullion feet ×2) | ~$70 |
| M5 slide-in economy T-nut | `14122` class (20-series M5) | 40 (48 bracket joints partly shared + 5 cartridge + 4 IMU/tray + spares) | ~$40 |
| M5 × 10 BHCS 8.8 black + M5 washers | 80/20 20-series bolt assemblies or generic | ~64 | ~$20 |
| End caps 20-series (17 members × 2 faces where open) | 80/20 20-series end cap (verify number in the catalog) | ~20 | ~$15 |
| Captive M5 thumbscrews (cartridges, battery, yoke plates) | generic knurled, yellow-anodized or printed cap | 11 | ~$25 |
| Ø15 rod hardware: 4 canon caps (printed spares), 8 M3×25 | existing | — | — |
| Loctite 243, torque-stripe marker | — | 1 each | ~$15 |
| **Frame + hardware class total** | | | **~$270 black / ~$230 plain** |

Not in the 80/20 catalog by intent: drawer slides (theirs start at 375 mm / 100 lb — wrong scale). Cartridge rails are the slots themselves.

**Face plates (`t1_faceplate/`, 2026-09-22):** any bay not holding a cartridge takes a bolted face plate — blanking (R1.5), vent, or fixed panel — on ~6–7 M5 × 16 BHCS into drop-in T-nuts per plate (~25 for the four D plates; add to the T-nut line above). The 84-wide plate slices at **7 h 03 m / ~53 g PLA** for the fit check; ASA for anything that flies. Not printed.

Plus, any concept: 6 SMA + 1 USB + 1 DC bulkheads, fuses, labels. Style coupon
first: 2 h 43 m PLA total.

## Verification performed

- `openscad` renders of all four concepts, the T-key detail and the coupon: no errors; coupon
  STLs `NoError`, genus 0.
- `python3 envelope_check.py` → exit 0 (one WARN: D gross 4.52 kg vs the pre-D R7.2 ceiling of 3.7 kg — owner to restate).
- `../.venv/bin/python make_t1_brep.py && ../.venv/bin/python verify_step.py`
  → 12 STEP files PASS (single closed valid solid, mm, zero tessellated faces).
- `python3 slice_coupon.py` → both PLA gcodes, preamble and guards verified
  literally; `gcode_check.py` passes both.
- **Nothing was sent to the printer.**
