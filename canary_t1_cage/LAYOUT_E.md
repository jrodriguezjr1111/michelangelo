# LAYOUT_E — component layout + cable plan on the owner's 406 × 279 deck (concept E, rev B 2026-09-25)

> **Rev B (connector-aware, from Javi's 12 photos) is the current layout — see the rev B section at the end.**
> Rev A below is kept as the record of what moved and why.
> **Rev C (full-height cage option, 2026-09-25) is the last section**: same trays, a top 406 × 279 ring on 222 posts, rearranged rod level.

Massing-level input for Javi + Andrew. Drawn in `t1_concept_E.scad` (`view="top"|"iso"|"lift"|"cables"`),
renders `renders/E_*.png`. Numbers: `envelope_check.py` §[4E]. **Nothing sliced, nothing printed.**
Roster re-verified in the canary memory bank 2026-09-24: **MTi-3 replaces the BNO085** (removed 2026-09-22),
**rf-node retired 2026-09-17**, the **FlyCatcher dual tuner stays** (its two tuners are UHR204 ports 1–2, CO stick
port 3, vib node port 4), EG25-G installed, ZED-F9P, V-mount pack, MA963 on the rod level.

## Axes and the belt
X = 406 (long axis, **lateral in the aircraft — along the lap belt**), Y = 279 (fore-aft, **+Y = nose**), members 20 tall,
bays **173 × 239** clear each side of the centre member (x 193–213). Lap-belt band **y 100–172** across the whole deck;
two fore-aft cargo-strap loops round **both long members** at **x = 100 and 306** (30 mm tray cut-outs so the strap
never bears on plastic). The rods (400 long, y 110/170, axis z 148.7) are handle, antenna rail and lid carrier — **not
in the restraint path**.

## Placement (deck coordinates, mm, min corner; standoff 6 unless noted) and the rule behind each

| item | envelope | at | rule applied |
|---|---|---|---|
| **Battery** V99-class 107 × 74 × 64 on its **V-plate** (100 × 80 × 10 EST, flat on the tray) | bay L | 28, 99 | heaviest item **in the belt band**, back-down so the CG is 42 mm up; V-lock latch + belt over it + secondary strap = R2.4 three ways |
| **PDB** + INA219 (60 × 40 × 20 EST) | bay L | 30, 52 | shortest raw-rail run (D-Tap → PDB 100 mm); fuses 3 A Orin / 2 A hub |
| **Cabin CO** stick 114 × 21 × 15 | bay L, **front edge** | 40, 22 | cabin air: the front tray edge is louvred over it; USB to hub p3 through the centre-member slot |
| **LTE** EG25-G carrier 80 × 35 | bay L, rear edge | 90, 215 | under the LTE SMA feedthrough on the rear-left post; coax 450 |
| **IMU** MTi-3 DK 43.5 × 34, M2.5 on 23.00 × 28.00 (PUB) | **rear-left corner Al plate 56 × 50 × 3** on the members' top slots | 22, 225 | R3.1: metal datum bolted to two members, **not a tray**; board flat, arrow → +Y (nose); 3 mm spacers; micro-USB hood |
| **UHR204 hub** 139 × 87 × 35 | bay R, front half, **against the centre member** | 216, 20 | cable node: 4 downstream + 1 upstream + DC all within 150 mm; tuners' micro-USB on the tray side |
| **RTK** ZED-F9P 43.5 sq | bay R | 216, 100 | 12 tall inside the belt band (belt rides the battery, clears it); SMA up the rear-right post |
| **Traffic** FlyCatcher 64.93 × 56.03 × 27 (holes 58 × 49) | bay R | 216, 176 | beside the hub (USB-2/3 = 140 mm); SMAs to the rear post |
| **Orin** dev kit 100 × 81 × 36, fan up | bay R, rear-right | 284, 176 | **nothing above the fan but rods**; battery is two bays away and upstream of the exhaust; heatsink exhaust radial into the open bay |
| Bulkheads: vib USB (threaded IP67), DC service | bay R **front face** (front long member's outer slot line) | x 330 / 360 | the only cabin-facing connectors, both locking |

Not on the deck: antennas (rod level), the vibration node (external, on the vib bulkhead cable), the Perch.

## Trays — what they are and what they add
Two **full-bay printed ASA trays** (`fp` castellated-ear rule from `t1_faceplate`: 10 mm flange on every member,
M5 ears on the slot line into `14122` T-nuts; **bay R on six captive thumbscrews** because that is the bay opened most —
T0 lesson; bay L on M5 BHCS). Skin 4 mm on the member tops, 9 mm ribs into the bay, an X pocket on top,
component standoffs printed in (heat-set M3 on each board's **measured** pattern; the V-plate bolts through on its
1/4-20 / M4 threads). **Structural role:** a bare 2020 picture frame racks about its four bracket joints (each member
J ≈ 13.7 × 10³ mm⁴); each 4 mm ASA skin adds in-plane shear stiffness G·t ≈ 2.8 kN/mm per mm of width, so the deck
becomes a shear panel — an order-of-magnitude class gain in racking stiffness, which is why the trays are full-bay
and bolted on all four sides. **Keep the centre member:** it halves the tray span (173, not 366), gives the mid-line
bolt row, and both trays print under 281 mm (239 × 193 outline). Tray class: ~158 cm³, ~17 h each, ASA (PLA sags a
173 mm span under the 640 g hub at 60 °C — never flies). Label plates: snap-in yellow (`make_style_coupon` seat) on
each component's front standoff rail; POWER / PDB / CABIN CO / LTE / IMU / CANARY CORE / RTK / TRAFFIC.

## Six-direction retention, per item
battery: V-lock (±X ±Y −Z by the plate, +Z by the latch) + belt + strap · boards: 4 × M3 into heat-sets (all six) ·
hub: 4 × M4 through its ears (VERIFY ear pattern) · V-plate: 4 × M4 into the tray · trays: ears in bearing on the
members (±X ±Y), bolts (±Z) · IMU: 4 × M2.5 into the Al plate · rods: canon caps · cables: below.

## Does a different deck length lay out cleaner?
406 works: bay L holds battery (107) + PDB with 27 mm to spare in X; bay R holds hub (139) + 34 mm. **420** (bays 180)
would give both bays 7 mm of breathing room per side and a round number; **not worth re-cutting** the frame he has —
keep 406 for the prototype, cut 420 only if the frame is ever rebuilt in black. Do **not** go shorter.

## Cable-management plan
**Topology: star at the hub for USB (5 legs), a 3-leg power harness from the PDB, coax point-to-point to the rod level.**
No trunk — every run is its own labelled, replaceable pigtail (T0: a cable was among the five things pulled).
- **In the T-slots:** the long members' **inner top slots are under the trays** (unusable); runs go in the **outer side
  slots** of the front/rear long members and the centre member's side slots, under **80/20 `12004` 20-series reduction
  T-slot cover** (polypropylene, black, $5.40 per 2 m — one length covers the deck: 2 × 406 + 2 × 239 + 239 = 1.53 m
  plus posts). Marked "slot" in the table.
- **On the trays:** printed cable combs (4 mm ASA, 6 mm slots, zip-tie eyes) every ≤ 80 mm; **20 mm jacket grip
  before every connector** (comb or hood), so connector bodies carry zero load.
- **Coax to the rod level:** up the rear-left post (LTE) and rear-right post (GNSS, 1090/978) in the post's outer
  slot under cover, with a **60 mm service loop** at the post top before the SMA.
- **Power:** V-plate D-Tap → PDB (100 mm) → Orin barrel / hub DC as two fused legs; INA219 in the PDB on the raw rail.
- **Retention rule:** no friction-only connector anywhere: hub ports are 15 N high-retention; screw-lock USB-A/USB-C
  cables at the Orin and F9P; **micro-USB (FlyCatcher ×2, MTi-3) has no latch → printed hood + comb within 20 mm**;
  barrel → hood; D-Tap → printed keeper; JST-VH latches; SMA torqued 0.45 N·m; threaded bulkheads.

| # | run (A -> B) | connectors | retention | route | drawn path mm | order length mm (+2x20 grip +loop, rounded) |
|---|---|---|---|---|---|---|
| USB-1 | UHR204 upstream (B) -> Orin USB-A | USB-A / USB-B | hub B port = 15 N high-retention; Orin end: screw-lock USB-A cable (or printed hood on the tray) | star-hub | 79 | **150** |
| USB-2/3 | FlyCatcher 1090 + 978 -> hub p1 / p2 | micro-USB / USB-A | hub A = 15 N; micro-USB end = printed micro-USB hood + cable comb on the tray within 20 mm (no latch exists) | star-hub | 70 | **140** |
| USB-4 | CO stick (CP2102) -> hub p3 | USB-A / USB-A | hub A = 15 N; stick end = the stick's own tray clamp (co_sensor tray) + comb | slot | 64 | **140** |
| USB-5 | front-face vib bulkhead -> hub p4 | panel USB-A bulkhead (IP67, threaded) / USB-A | threaded bulkhead outside; hub A = 15 N inside | slot | 14 | **90** |
| USB-6 | EG25-G carrier -> Orin USB-A | USB-A / USB-A (carrier) | screw-lock USB-A at the Orin; carrier end: comb + hood | slot | 115 | **190** |
| USB-7 | ZED-F9P -> Orin USB-A | USB-C / USB-A | USB-C latching (screw-lock C) at the F9P; screw-lock A at the Orin | comb | 73 | **150** |
| USB-8 | MTi-3 DK (micro) -> Orin USB-A | micro-USB / USB-A | micro hood + comb on the corner plate; screw-lock A at the Orin | slot | 221 | **300** |
| DC-1 | V-plate D-Tap -> PDB input (14.4 V raw, INA219 shunt) | D-Tap / JST-VH 2-pin (locking) | D-Tap is a friction fit: printed D-Tap keeper on the V-plate frame; VH latches | comb | 20 | **100** |
| DC-2 | PDB -> Orin barrel 5.5x2.5 (9-20 V, 3 A fuse) | JST-VH / barrel (locking: threaded barrel bulkhead or hood) | VH latches; Orin barrel = printed hood clamping the plug body | slot | 263 | **340** |
| DC-3 | PDB -> UHR204 DC (10-30 V, 2 A fuse) | JST-VH / hub terminal block (screw) | screw terminal; VH latches | slot | 126 | **200** |
| RF-1 | EG25-G u.FL -> SMA bulkhead on the rod-level yoke -> LTE patch | u.FL / SMA | u.FL: adhesive + comb; SMA torqued (0.45 N.m) | slot+post | 349 | **450** |
| RF-2 | ZED-F9P SMA -> GNSS patch on the rods | SMA / SMA | torqued SMA both ends; service loop at the post top | slot+post | 460 | **570** |
| RF-3/4 | FlyCatcher 1090 + 978 SMA -> MA963 / whip on the rods | SMA / SMA | torqued SMA; loop at the post top | slot+post | 344 | **450** |

Lengths are measured from the drawn paths (`CABLES` in `t1_concept_E.scad`): drawn path + 2 × 20 mm jacket grip
+ 30 mm slack (60 mm loop on coax), rounded up to 10. Re-measure after the first dry fit.

## Open CONFIRMs (E-specific)
1. **MTi-3 DK outline** — 43.5 × 34.0 with M2.5 on 23.00 × 28.00 is from the Xsens DK manual (MT0513P.C fig. 9); the
   height, mass and which micro-USB end it exits are EST. Caliper before the corner plate is drilled.
2. **FlyCatcher status** — still in T1 (memory bank 2026-09-23/24: tuners on hub ports 1–2, ForeFlight validated on
   them). Its USB is **micro-USB ×2**, unlatched: the hood/comb is mandatory. Board 64.93 × 56.03 MEAS; datasheet
   76 × 57 × 19 with SMAs, 48 g.
3. **Deck length** — 406 as built; 420 only on a rebuild.
4. UHR204 mounting-ear pattern; V-mount plate part (COTS with D-Tap, see `bom/8020_order_E.md`); post height 100
   vs the rods' clearance over the battery (64 + 10 + 4 + 20 = 98 → rods at 141 underside: 43 mm clear — fine).


---
# REV B — connector-aware placement (2026-09-25, photos 21–32)

Renders: `renders/E_top_layout_revB.png` (yellow wedge = connector edge, pointing out; blue USB / red DC / yellow coax
drawn on the plan), `renders/E_cable_routing_revB.png`, `renders/E_iso_assembled_revB.png`. `t1_concept_E.scad`
with `rev="B"`. Three-minute-swap rule kept: every connector edge faces open tray or the hub channel, never a neighbour.

## What the photos settled
| photo | fact used |
|---|---|
| 21 | SparkFun ZED-F9P: **USB-C on one short edge** (with the GND/3V3/RX2/TX2 header), **u.FL antenna at the diagonally opposite corner**, PPS/RTK/FENCE and I²C headers on the left edge, SPI on the right. |
| 22 | EG25-G on a mini-PCIe→USB carrier: **USB receptacle at the top short end** (metal shroud proportions read as **USB-A female — CONFIRM**), 2 + 2 mounting posts (repo MEAS 70.80 × 24.21), module zip-tied, **u.FL→SMA pigtail from the module's near (bottom) end**. Carrier outline **≈ 90 × 30** scaled on the module's 30 mm mini-PCIe width (the mat grid was not used — the module is the better ruler). |
| 26 + 29 | UHR204: four downstream USB-A on the **long face**, numbered **4-3-2-1 from the far end** (port 1 nearest the host); **USB Host receptacle + green DC terminal block together on ONE short end**. Ports 1–2 = yellow flat leads to the tuners, 3–4 black. |
| 32 | MTi-3 **dev board is an Arduino-Uno shield** (≈ 68.6 × 53.3, Uno hole pattern): micro-USB on a short edge, PSEL DIP, module at the corner with the axes silkscreened — **+X along the long axis away from the USB end, +Y across the board, +Z out**. |
| 27 + 30 | Rod level today: MA963 Guardian on the printed plate (arrow = cable exit) **plus a white Ø~150 L1/L2 GNSS dome** beside it. |
| 31 | Printed black node with the canon rod clamp and vent slots on one end = the **`co_sensor` CO tray tube plate** (vented lid) — the CO stick already has a validated rod-level home. |
| 24 + 25 | T0 discipline: all bulkheads on **one face**, cables dressed down and zip-tied → E puts its two bulkheads on the bay-R front face. |

## What moved, and the connector edge that drove it
| item | rev A → rev B | driving edge |
|---|---|---|
| **UHR204** | same spot (216,20), now **rotated: host + DC short end faces the centre member (W)**, downstream long face faces +Y | photo 29: host and DC block share a short end → they meet the PDB and the Orin lead at the centre-member corner; p1/p2 (tuners) sit nearest that end, so the FlyCatcher goes directly above them |
| **FlyCatcher** | 216,176 → **216,112**, micro-USB edge S (4 mm from the hub's downstream face), SMAs N | its two unlatched micro-USB leads become 80 mm right-angle jumpers straight into p1/p2; the SMAs face the rear slot to the rear-right post |
| **ZED-F9P** | 216,100 → **216,200**, USB-C edge E toward the Orin, u.FL corner NW | photo 21: USB-C and antenna on opposite corners — USB-C now looks at the Orin's connector edge (61 mm), the coax leaves at the rear slot |
| **Orin** | same (284,176), **connector edge S** into the y 107–176 channel | one channel between hub and Orin carries USB-1/6/7/8 and DC-2 under one comb row; the fan stays open above |
| **EG25-G carrier** | 90,215 (80 × 35) → **95,222 as 90 × 30 along X**, USB end E, u.FL end W | photo 22: USB at one short end, antenna pigtail at the other — USB end points at the centre member (crosses in its top slot to the Orin, 200 mm), u.FL end points at the rear-left post (LTE feed) |
| **MTi-3 DK** | 43.5 × 34 at 22,225 → **Uno shield 53.3 × 68.6 at 24,198 on a 62 × 72 × 3 Al corner plate**, board +X = deck +Y (nose), **micro-USB on the board's −X end = deck S**, so the lead leaves toward the tray interior | photo 32: arrow-to-nose fixes the long axis along Y; the USB then exits away from the corner, not into it |
| **PDB** | 30,52 → **118,42**, OUT edge E at the centre member, IN edge N at the battery | both fused outputs cross the centre member in ≤ 60 mm; the D-Tap lead from the pack's S end is 47 mm |
| **Battery** | same, pack outputs (D-Tap) on its S end toward the PDB | V99 outputs are on the short end |
| **CO stick** | deck front edge → **the existing rod-level CO tray (photo 31) at x 322–362** on the front rod | zero new print, real cabin-air exposure; USB down the front-right post to p3 |
| **Rod level** | dome added | **dome Ø150 at x 45–195 over bay L, MA963 plate at x 205–315, CO tray at x 322–362 — 326 mm clear between the yoke bridges, 7 mm to spare; the 1090/978 whips move to the two yoke bridges.** The dome needs a **new puck rod-mount (5/8-11 stud)** — no michelangelo family has one; ~400 g EST at the rod level. |

## Rev B cable table (re-measured from `CABLES_B`; + 2 × 20 grip + 30 slack, 60 loop on post runs; rounded up to 10)
| # | run (A -> B) | connectors | retention / route notes | route | drawn mm | order mm |
|---|---|---|---|---|---|---|
| USB-1 | Orin USB-A (S edge) -> hub HOST (W short end) | USB-A / USB-A (hub host receptacle, photo 29) | screw-lock A at the Orin; hub host = 15 N; comb in the y107-176 channel | comb | 195 | **270** |
| USB-2/3 | ~~FlyCatcher uUSB x2 (S edge) -> hub p1/p2 (N long face)~~ **2026-09-30: the FlyCatcher LEAVES the deck** (window unit, `flycatcher_window/`): two micro-USB leads in ONE bundled run window -> cage -> hub p1 (ADS-B OUT) / p2 (UAT OUT) | micro-USB / USB-A | yellow hood traps both overmolds + ties each lead within 20 mm at the window unit; hub A = 15 N; secure the bundle along the run (no strain on the window unit) | window -> cage | 600–900 (owner: 2–3 ft) | **0.9 m** (buy length, both leads) |
| USB-4 | CO tray on the rods (front-right) -> hub p3 | USB-A / USB-A | down the front-right post's outer slot under 12004 cover, 60 mm loop at the post top; hub A = 15 N | slot+post | 305 | **410** |
| USB-5 | front-face vib bulkhead (x 360) -> hub p4 | threaded IP67 USB-A bulkhead / USB-A | threaded bulkhead; hub A = 15 N | comb | 102 | **180** |
| USB-6 | EG25-G carrier USB-A (E end) -> Orin USB-A (S edge) | USB-A / USB-A (carrier receptacle type: CONFIRM from photo 22) | hood + comb at the carrier; screw-lock A at the Orin; crosses the centre member in its top slot | slot | 128 | **200** |
| USB-7 | ZED-F9P USB-C (E edge) -> Orin USB-A | USB-C / USB-A | screw-lock C; screw-lock A | comb | 61 | **140** |
| USB-8 | MTi-3 DK micro-USB (S edge of the Uno board) -> Orin USB-A | micro-USB / USB-A | hood + comb on the corner plate; crosses the centre member; screw-lock A | slot | 293 | **370** |
| DC-1 | battery D-Tap (pack's S end) -> PDB IN | D-Tap / JST-VH | printed D-Tap keeper; VH latches | comb | 47 | **120** |
| DC-2 | PDB OUT (E edge, 3 A fuse) -> Orin barrel (S edge) | JST-VH / 5.5x2.5 barrel + hood | VH; barrel hood clamps the plug body; centre-member slot then the channel comb | slot | 214 | **290** |
| DC-3 | PDB OUT (E edge, 2 A fuse) -> hub DC terminal block (W end) | JST-VH / screw terminal | VH; screw terminal + ferrules | direct | 34 | **110** |
| RF-1 | EG25-G u.FL (W end) -> rear-left post -> MA963 LTE SMA | u.FL->SMA pigtail / SMA | u.FL adhesive + comb; SMA 0.45 N.m; 60 mm loop at the post top; rear slot under cover | slot+post | 508 | **610** |
| RF-2 | ZED-F9P u.FL (NW corner) -> rear-left post -> GNSS dome (TNC/SMA) | u.FL->SMA / dome connector (CONFIRM TNC vs SMA) | as RF-1 | slot+post | 474 | **580** |
| RF-3/4 | ~~FlyCatcher SMA x2 (N edge) -> rear-right post -> whips on the yoke bridges~~ **GONE from the cage 2026-09-30** — the stubbies screw straight onto the window unit's SMA bulkhead wall (no coax) | — | — | — | — | — |

Retention rule unchanged: hub ports 15 N; screw-lock USB-A/C at the Orin and F9P; **micro-USB ×3 (FlyCatcher ×2, MTi-3) has no latch → printed hood + comb within 20 mm**; barrel → hood; D-Tap → keeper; JST-VH latches; SMA 0.45 N·m; threaded bulkheads. Slot runs under 80/20 `12004` cover: rear long member (RF-1, RF-2, RF-3/4), front-right and rear-left/right posts, centre member top slot (USB-6, USB-8, DC-2 cross it).

## CONFIRM (rev B)
1. **MTi-3 DK**: Uno 68.6 × 53.3 with the Uno hole pattern is read from photo 32 (not measured); which short edge the micro-USB is on relative to the module axes — the photo says the USB is at the board's −X end; caliper the board and the hole pattern before the corner plate is drilled.
2. **EG25-G carrier**: outline ≈ 90 × 30 from photo scale; receptacle type (A/B) at the USB end.
3. **FlyCatcher**: which long edge carries the micro-USBs vs the SMAs (assumed opposite edges); if they share an edge the board turns 90° and USB-2/3 become 120 mm.
4. **UHR204**: confirmed from photos — host + DC on one short end, ports 1→4 from that end. Ear/mount pattern still unknown.
5. **GNSS dome**: diameter (~150), mass, connector (TNC vs SMA), thread (5/8-11) → puck mount to design.
6. Rod level fit: 326 mm clear vs 150 + 110 + 40 + 3 × 10 gaps = 330 → **4 mm short as drawn; the dome overlaps the yoke bridge by ~4 mm or the MA963 shifts 4 mm — fine, but if the rods are shorter than 400 something moves to the yoke bridges.**


---
# REV C — full-height cage (2026-09-25)

> Owner, verbatim: *"making the box twice as high so that the GNSS and LTE/WIFI antennas rise halfway above the bottom
> of the box and below the top of the box so that they have protection sitting below the top of the box."*

Drawn in `t1_concept_E.scad` with `rev="C"`. The model echoes every number below and asserts the clearances. Renders
come from `render_E_revC.py`: `renders/E_revC_iso.png`, `E_revC_iso_siderails.png` (option), `E_revC_side_elevation.png`
(numbered markers + legend) and `E_revC_gnss_mask.png`. Mass, loads and exit path are in `envelope_check.py` §[4E-C].
BOM delta: `bom/8020_order_E_revC.md/.csv`. **Nothing sliced, nothing printed.** The rev B tray layout is **unchanged**:
rev C draws `PLACE_B` as it is. A gate bug that would have given rev C the old 43.5 × 34 MTi board was fixed
(`MTI = rev != "A"`).

## Geometry (as modelled)
| item | value | note |
|---|---|---|
| posts | **4 × 222** 20-2020 (rev B: 100) | the shortest whole-mm post that keeps the dome top ≥ 15 under the rail top. The earlier "220 → z 263" note came from a stale 148.7 rod-axis comment: with E = 20 the rod axis is **z 151.7**, and 220 would leave the dome only 13.6 under. Every extra mm of post worsens the GNSS mask, so the length is not rounded up to 230 |
| top rectangle | 2 × 406 on the posts + 2 × 239 between them; 20-4119 × 2 at each post top; 20-4081-class flat L plate on each top corner | top-rail underside z 245, **top-rail top z 265** |
| **overall height** | **268** (rail top + 3 mm gussets) × 406 × 279 | rev B as drawn already stood **249** at the dome and **264** at the 100 mm whips, so rev C is **+4 mm** over rev B's tallest point. It is a cage around what already stuck up, not a taller unit |
| C172 baggage door 387 × 559 | **passes**, long axis first: 279 × 268 section through 387 × 559, with 108 / 291 mm spare | |
| antenna tops vs the rail top (z 265) | dome **249.4 → 15.6 under** · MA963 corner clamps 193.9 → 71.1 (radome 190.7) · 1090/978 stubbies 181 → 84 | all asserted ≥ 15 in the model |
| rod axis | z 151.7, **same as rev B** | coax lengths below the rod level do not change |

**Rod yokes: kept on the posts, not moved to the top rails.** Each printed ASA bridge (now 40 × **239** × 10) spans
**between** a post pair at the rev B height (z 123-133), with 2 × M5 into T-nuts in each post's inner slot. Why:
- It braces each front/rear post pair at mid-height, which halves the posts' free length in that plane.
- It keeps the 1.6 kg of antennas low (lower CG, higher sway mode).
- It keeps the antenna level exactly where rev B has it.

Hanging the rods from the top rails would put about 1.8 kg on ~100 mm printed hangers in tension, which means plastic
creep in the load path and the antennas no lower.

## Rod level: the real MA963 forced a rearrangement (applies to rev B too)
Rev B drew the MA963 as a 110 × 90 × 12 slab. The part is `taoglas_ma963` CW-ANT-005 rev C: antenna
**146.37 (along the rods) × 133.95 × 20.04, 730 g**, on a **173 × 180 × 7** plate whose underside is 12 above the rod axis,
with corner clamps 23.24 above the plate. Dome 150 + plate 173 + CO tray tube plate (tray 137.6 along the rods) does
not fit in the 326 mm between the yoke bridges side by side. It is **37 mm over**, not the 4 mm rev B's CONFIRM 6
estimated. Rev C uses height instead:

| item | x along the rods | z | why here |
|---|---|---|---|
| MA963 on its plate, cable tongue toward +Y (the rear posts) | centre **107** (clamps 17-197) | plate 163.7-170.7, clamps to 193.9 | the plate overhangs the left yoke's canon cap with 2 mm to spare, and its stations clear that cap by 2 mm (asserted). LTE is TX, so it goes at the opposite end from the GNSS dome, and RF-1 gets shorter |
| GNSS dome on the (still to design) puck | centre **277** (dome 202-352) | base 189.4, **L1 PC 224.4 (EST)**, top 249.4 | 5 mm clear of the MA963 clamps and 34 mm clear of the x=406 end-rail face |
| CO tray (existing `co_sensor` rev C tube plate), **hung under the rods**, tail +X | cap station **225**, tray 155-292.6 | 107.1-139.7 | under the dome, clear of the MA963 caps, 20 mm clear of the battery's lift path, cabin air on all sides. USB-4 drops 85 mm to hub p3 (was 305 via the post) |
| 1090 / 978 **stubbies ≤ 40** | on the **right** yoke bridge at (374, 50) / (374, 229) | tips 181 | off the rods, away from the MA963 (LTE TX) and from the dome footprint. The rev B whip spots are now under the MA963 plate |

Changed runs (same rule as rev B: drawn length + 2 × 20 grip + 60 loop, rounded up to 10):
- **RF-1** LTE u.FL → rear-left post → MA963: drawn 338, order **440** (was 610).
- **RF-2** ZED-F9P u.FL → **rear-right** post → dome: drawn 579, order **680** (was 580).
- **RF-3/4** FlyCatcher → rear-right post → stubbies: near 500 / far **680** (was 480).
- **USB-4** CO tray → hub p3: drawn 85, order **160** (was 410). About 45 mm of it is free span, so zip it to the CO plate rung.

Re-measure all of these at dry fit.

## GNSS masking (item 2) — `renders/E_revC_gnss_mask.png`
Mask angle to each top rail = atan(height of the rail's top inner edge above the reference point / horizontal distance
to the rail's inner face). The sides are open, so each rail shadows a **band**. The band's lower edge is the ray to the
rail's bottom outer edge.

| reference | rail top above it | y=0 long (tail side) | y=279 long (nose side) | x=0 end (lateral) | x=406 end (lateral) |
|---|---|---|---|---|---|
| **dome L1 PC** (EST), x 277, z 224.4 | 40.6 | **18.8°** (band 8.4-18.8) | **18.8°** (8.4-18.8) | 9.0° (4.3-9.0) | **20.4°** (9.1-20.4) |
| **MA963** mid-housing, x 107, z 180.7 | 84.3 | 35.2° | 35.2° | 44.1° | 16.8° |

Posts add four ~7° wedges up to ~14°. The corner gussets sit above the rails at the corners. Ray-cast over the whole
sky (cos-weighted), the cage shadows **16.7 %** of the dome's hemisphere above 0°, **13.2 % of the sky above a 10°
mask** and **5.8 % above 15°**.
- **Against a 10-15° RTK mask:** the rail bands rise above 15° in three of four directions, so the cage costs sky
  that RTK would otherwise use. **No rev C geometry fixes this.** h can't fall below (dome H − PC) + 15 = 40 mm. The
  279 deck caps the fore-aft distance at 119.5, and it would need ≥ 149 to get 15°. Moving the dome to mid-deck would only
  trade the end-rail angle for an impossible MA963 fit.
- **Against the C172 cabin (assumption, EST, no survey):** the unit rides on the rear bench or in baggage. The metal roof
  blocks the zenith above roughly 45-55°, except through the rear window (1963+ Omni-Vision) and any overhead skylights.
  The side windows see roughly 5-40°. Forward, the front seats, occupants and panel block below roughly 25-30°. The
  cabin's usable sky is therefore a **5-45° window band plus the rear window**, and that is exactly where the rail bands
  (4-20°) fall. In the cabin the cage takes a larger share of the *usable* sky than the 13 % whole-sky figure suggests.
  The cabin still masks far more than the cage does.
- **This is a geometric shadow, not a hard cut.** A 20 mm rail is about 0.1 λ at L1 (190 mm), so expect diffraction
  and a few dB of C/N0 loss across those bands. **The larger RTK risk is multipath and near-field coupling:** anodised
  aluminium rails and gussets within ~0.6-1 λ of the phase centre alter the pattern and the phase-centre variation.
  Because the cage is rigid with the antenna the effect is repeatable, but it is not in any antenna calibration.
- **MA963 has no GNSS element.** Seen from altitude, LTE towers are at or below the horizon and Wi-Fi is in the cabin,
  so its 17-44° rail angles do not matter. At 600 MHz-6 GHz a 20 mm rail is a small scatterer.
- **Any lid over the dome must be RF-transparent:** ASA / PC / PETG sheet ≤ 3 mm with ≥ 10-15 mm air over the dome.
  **Not** PA12-CF or any carbon-filled print, metal mesh, perforated aluminium, metallic paint or ACM panel. Carbon
  fibre is a lossy conductor at L1. Keep it drained so a water film can't form.

## Protection, honestly (item 3)
**The top rectangle does protect against:**
- setting the unit down upside down: it lands on the 4 gussets and rails, with the dome 15.6 mm clear;
- a flat or large object set on top (a bag, a case, a seat cushion) that spans the 366 × 239 opening;
- the cabin roof or baggage-bay ceiling contacting the top when the unit is tilted through the door;
- flat-wall and seat-back contact. The posts, long members and top rails define all four face planes, and nothing
  protrudes: the MA963 plate edge is 49.5 mm inboard of the face plane and the dome 64.5 mm.

It also gives an **all-metal carry handle** (168 N at 3 g through the posts in tension, with no printed part in the
path, whereas rev B carried by the rods through printed canon caps), and a frame for a lid.

**It does not protect against:**
- anything smaller than the 366 × 239 top opening. A boot, a headset, a water bottle or a hand reaches the dome from
  above.
- anything entering the side windows between the posts: **366 × 225 on each long face** and 239 × 225 on each end face
  above the yoke bridge. A bag corner, a foot or a buckle can reach the MA963 plate edge or the dome.
- a load on a top rail at mid-span. 1 kN (a knee) gives ~150 MPa in 6063-T6 (yield 172), so the rail survives, but
  only just.

**Side rails at antenna height (the `side_rails=true` option, z ~192-212):**
- **In favour:** they sit below the dome's phase centre, so they add **no** GNSS mask. They do not block the tray exit
  path.
- **Against:** they only split each long-face window into two ~95 mm slots, so a boot still gets in.
- **Against:** +0.45 kg and ~$70.
- **Against:** they put aluminium at the MA963's element height 30-50 mm from its plate, which is near-field at LTE low
  bands.

**Not recommended** for the belted rear-seat carry. If baggage-bay carriage shows loose items reaching the antennas,
fit a printed ASA/PC side guard (RF-transparent, clipped to the posts' slots) instead of metal rails.

## Restraint and mass (item 4) — `envelope_check.py` §[4E-C]
- **Pick: lap belt + 2 cargo straps round the BOTTOM long members, unchanged from rev B. Never belt the top rails.** At
  rev C gross, 18 g gives 1006 N, and the strap bears on the 6063 long members at 0.84 MPa. A strap on the top rails
  would act ~185 mm above the CG (z ~70, EST). That is 186 N·m at 18 g, taken by eight post-end bracket joints in bending
  at ~2.3 kN per foot, over the ~2 kN class of a 20-4119 joint. It would also lay the belt across the dome's sky. The
  top rails are the carry handle and the protection, not a tie-down.
- **The posts now carry 3.07 kg** (the top ring, half of each post, and the rod level with antennas). At 18 g that is
  136 N per post. The post-foot moment is 30 N·m as a cantilever (upper bound), giving 1.5 kN bolt tension, MS 0.3; as a
  portal it is 15 N·m, MS 1.7. At the classic 9 g case the figures are MS 1.7 / 4.3. It closes, but torque stripes and
  the 10 h re-check (R6.6) now matter on the post feet.
- **Vibration flag:** the upper mass on four 222 posts sways at an estimated **~66-131 Hz** before joint compliance
  (rev B's 100 mm posts: ~282 Hz). That brackets the C172's ~80 Hz blade-pass and firing frequency at 2400 rpm. The
  seat cushion and belt isolate well below that, but put the vib node on a top rail for one ground run before flight
  (structures-engineer check).
- **Mass delta +1.26 kg:**
  - +1.78 m of 20-2020: +784 g;
  - 4 top gussets: +172 g;
  - 8 brackets: +72 g;
  - 36 screw/T-nut sets: +234 g.

  **Gross 4.43 → 5.70 kg.** That is over the 5 kg bound the concept table is held to; the script flags it as a WARN, and
  the R7.2 ceiling is still the owner's to restate. Neither gross includes the 1.6 kg rod-level payload: MA963 730,
  plate 250, dome 400 EST, puck 40, CO tray 120, whips 60.
- **Trays: "lift out through the open top" is not true in rev C, and was not true in rev B with the rods fitted.** The
  top opening is 366 × 239, but a tray with its 10 mm member flanges is 193 × 259. In rev B the rod pair already spans
  both bays at z 144 with only 44.6 mm between the rods.

  **The real path, both revs:**
  1. Undo the straps, the tray bolts and the pigtails.
  2. Lift the tray 12 mm.
  3. Slide it out a **long-face side window between the posts** (366 wide × 225 tall).

  Clearances on that path:
  - bay-L tray + battery top out at z 110 against the lowest rod-level part over it, z 141.7 (the MA963 caps);
  - bay-R tray's tallest item (Orin) tops out at z 78 against the CO tray underside, z 107.1;
  - side rails, if fitted, sit above this path.

  **Bay R goes out the rear (y=279) face**, because the two bulkheads are on its front face. **CONFIRM at dry fit:**
  - the trays' outer-corner flanges sit under the post feet and deck gussets, so the flight trays need 20 × 20 corner
    notches, and bay L also needs an IMU-plate cut-out;
  - bay L shifts ~12 mm toward the centre member before sliding, so its end-member flange clears the posts. This is the
    same in rev B.

## BOM delta (item 6) — `bom/8020_order_E_revC.md/.csv`
**+$220.74** of 80/20, for **$361.18** with rev B's $140.44:
- post extra length 4 × 122 (+$16.00);
- top rails 2 × 406 + 2 × 239 ($42.32) + 4 cuts ($12.00);
- 8 × 20-4119-Black ($60.40);
- 4 × 20-4081 ($44.92);
- 40 × 75-3581 ($36.00);
- 10 spare 14122 ($3.70);
- 1 more 12004 ($5.40);
- end caps net 0.

Stubby 1090/978 antennas still need pricing.

## Recommendation — rev B open deck vs rev C cage
**Fly rev B's open deck, but build it the rev C way underneath, so the top ring is a bolt-on decision rather than a
rebuild.** That means 222 mm posts (+$21 with the extra slot cover), yoke bridges between the posts, and rev C's rod
level. The rod level is needed in any case, because the real MA963 does not fit rev B's rod level.

**What rev C buys:** real protection from being set down upside down, from a bag on top and from roof contact. It also
gives an all-metal carry handle and a frame for an RF-transparent lid. It adds only 4 mm to rev B's height.

**What it costs:**
- +1.26 kg (5.70 kg gross);
- +$221;
- the upper structure's sway mode drops into the ~80 Hz engine band;
- the aluminium rails shadow a 4-20° band all round the dome (13 % of the sky above a 10° mask), inside the window band
  a C172 cabin actually leaves for GNSS. The rails are also near-field reflectors next to an RTK antenna.

It still does not stop anything smaller than 366 × 239 from reaching the dome, or anything entering from the sides.

The deciding evidence should be measured, not argued. Run a 1-hour static RTK A/B on the ramp with the top ring on and
off (it is 8 bolts plus 4 gussets): compare fix rate, time-to-fix and C/N0 against elevation. Fit the ring only if the
degradation is negligible **and** handling damage is a real problem in T0/T1 use. If it is fitted, add an RF-transparent
lid rather than side rails.

## CONFIRM (rev C)
1. **GNSS dome:** height (60 EST), phase centre (35 EST), mass (400 EST), connector. **The post length follows the dome
   height 1:1, so don't cut the posts until it is measured.** Also design the 5/8-11 puck (30 tall is a DSN guess).
2. MA963 clearances to the left yoke cap are **2 mm** in both X (stations) and Z (plate overhang). Check them at dry fit.
   If they are tight, move the yoke caps under the rods.
3. Post-foot detail: the 20-4119 brackets land on the deck's flat corner gussets. Use the gusset holes or M5 × 12 through
   the plate.
4. Tray outer-corner notches (20 × 20) and bay-L's IMU-plate cut-out, which is needed in rev B too.
5. The ~80 Hz vib check on the top rail, and the static RTK A/B, both before committing to the ring.
