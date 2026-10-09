# Canary T1 cage — requirements the cage must satisfy regardless of who draws it

One page. Each line carries its number and where the number comes from
(`envelope_check.py` section in brackets). MEAS/PUB/EST/DSN provenance as in
`t1_params.py`. This page is meant to survive any change of concept.

## R1 Swap (the governing requirement, owner 2026-09-21)
- **R1.1** Any peripheral (RTK, LTE, Traffic, Cabin CO, power monitor, battery) out and back in **≤ 3 hand steps, 0 tools, ≤ 2 min**, without disturbing any other module. [6]
- **R1.2** The Core (Orin + hub) out in **≤ 8 steps, ≤ 10 min, one driver at most**; every other module stays in place. **2026-09-21 (owner, T0 experience): the Core was opened OFTEN in T0** — Core access is a first-class swap, not the exception. Concept D must give the Core its own removal path (no neighbour out, no rod off); the concept-A `a_core` gap is now a hardening gate. [6]
- **R1.3** Every cable is a **separately replaceable, labelled, locking pigtail** — the T0 removal list includes a cable and a power monitor, not just boxes. [6]
- **R1.4** A swapped module cannot be seated in the wrong bay (**keyed**) or seated wrong-way-up.
- **R1.5** One blanking plate per empty bay; the unit manifest (T1 memo §2) says what is present.
- **R1.6** (added 2026-09-21, concept D) Swap-time targets: peripheral **≤ 2 min**, battery **≤ 1 min**, Core **≤ 10 min**, IMU **≤ 5 min + recal**; a swap must never require removing a neighbouring module. [6]

## R2 Restraint path — carry-on equipment, NOT an installation
- **R2.1** Load cases: flight **+3.8 / −1.52 g × 1.5**; emergency-landing **9 g fwd / 3 g up / 1.5 g side** (classic 23.561 items-of-mass); **18 g fwd** carried as the margin case. Design gross **≤ 3.7 kg** → 646 N at 18 g. [4]
- **R2.2** Belt/straps pass **around the Ø15 aluminium rods**, never round a printed lug. Rod bending at 18 g mid-span, 230 mm between yokes: **79 MPa vs 240 yield, MS 2.0**. [4a]
- **R2.3** **Positive axial stop in metal** on the rods (split shaft collars each side of one yoke, or M12 end hardware) — the canon clamp is friction-only and preload relaxes hot; fresh slip capacity 2000 N is not to be counted. [4b] **2026-09-21, concept D (80/20 20-series frame, DECIDED):** native — the belt goes round the frame's bottom long members; rods become handle + antenna rail only and leave the restraint path. R2.2 likewise native. [3b]
- **R2.2 (E, 2026-09-25)** lap belt over the battery in the y 100–172 band + two cargo straps round both 406 mm long members at x 100 / 306; strap bearing on 6063 0.65 MPa at 18 g (780 N). [4E]
- **R2.2 (E rev C, 2026-09-25)** unchanged restraint: belt + straps round the BOTTOM long members, never the top rails (a top-rail strap puts ~186 N·m at 18 g into the post-end joints). 18 g at 5.70 kg = 1006 N, strap bearing 0.84 MPa. Post feet under the 3.07 kg upper mass: MS 0.3 (cantilever bound) / 1.7 (portal) at 18 g. [4E-C]
- **R2.4** Every component **retained in all six directions**; nothing gravity-seated. The heaviest swappable item (battery, 0.74 kg with carrier) is held by a **latch AND a secondary strap, each good for 131 N (18 g) in any axis**. [4d]
- **R2.5** Printed bearing under any restraint load **≤ 1 MPa** (trough at 18 g: 0.54 MPa). Heat-set inserts in tension **≤ 50 N each** (carry case: 13.5 N). [4b, 4c]
- **R2.6** Nothing attaches to the airframe. Belt/strap only. Antennas external on the rod rail.

## R3 IMU (attitude quality is how the product is judged)
- **R3.1** BNO085 seats on a **rigid keyed datum tied to the rod skeleton** (two asymmetric dowels + two captive screws); **never on a sliding rail or a cartridge alone**.
- **R3.2** Datum repeatability ≤ 0.2° across a swap; the pitch-offset recal after any IMU swap is still mandatory (T1 memo C2), the datum makes it small.
- **R3.3** Soldered harness with a locking connector at the datum — no Dupont (house rule, two field failures).

## R4 Thermal — sealed is impossible
- **R4.1** Sustained dissipation **~24 W** (EST); a sealed shell of any concept reaches **76–90 °C interior at 35 °C ambient** (U ≈ 2.3 W/m²K) — over the battery limit. [5]
- **R4.2** Fan intake ducted to an exterior grille, **≥ 32 cm² intake and ≥ 32 cm² exhaust** (≥ 3 × fan throat), exhaust on a different face than intake, no recirculation. [5]
- **R4.2 (E)** open deck: no shell, the Orin fan exhausts to cabin air; the ≥ 32 cm² rule is met trivially and only the lid (if fitted on the rods) must keep ≥ 32 cm² over the fan. [4E]
- **R4.3** **Battery outside or upstream of the Orin exhaust**, behind a partition; Li-ion 45 °C charge / 60 °C discharge limits. [5]
- **R4.4** Parked-cabin soak 60–70 °C is an **unpowered survival case** for the material; design the operating case at 35 °C ambient + 8 K air rise. [5]

## R5 Connectors
- **R5.1** Every connector positively retained: locking (JST-GH class, screw-lock USB, threaded barrel/SMA) or the UHR204's 15 N high-retention ports. **No friction-fit USB-A anywhere.**
- **R5.2** Connector bodies carry **zero mechanical load**; strain relief grips the jacket ≥ 20 mm from the connector.
- **R5.3** Bulkheads (6 × SMA, USB, DC) on one I/O face, each in a recessed bezel so a plug cannot be side-loaded.

## R6 Material and print
- **R6.1** **PLA never flies** (FLEDGE rule). Flight article: **ASA** default; **PA12-CF** where a clamped/threaded joint must hold preload hot (yokes, IMU datum, battery latch) — dried and reconditioned. Li-ion bay: **PC-ABS-FR** (profile exists on this machine) or a 0.5 mm aluminium liner in the ASA bay.
- **R6.2** Walls in multiples of 0.4; skins ≥ 4 mm (10 lines) on any face carrying a fastener; 45° chamfers instead of supports; no floating islands in the stated orientation.
- **R6.3** **Print guards, every slice**: `bottom_shell_layers ≤ 6`; `max_bridge_length` derived from the model's `MAXSPAN` echo; `PRINT_START` temperatures verified literally in the gcode. (`vib01_node/README_revD.md`.)
- **R6.4** No part longer than **281 mm** (305 bed − 2 × 12 margin) — concepts A (285) and B (300) need a **designed seam** at a frame, never mid-panel. No plate over ~12 h. [2] **2026-09-21, concept D:** no longer binds the *structure* (members cut to length, ≤ 300 mm); still binds every printed part (longest 134 mm). 
- **R6.5** (added 2026-09-21, concept D) **Printed T-key** riding a 20-series slot: neck 5.6 wide (slot 6.0 − 0.4), ≥ 14 lines, engagement ≥ 88 mm, head ≤ 10.4 × 2.0 in the 11.0 cavity (verify cavity in the 80/20 CAD), 1.0 mm lead chamfer, printed with layer lines **along** the neck; worst load 131 N per pair → 0.13 MPa shear. [3b]
- **R6.6** (added 2026-09-21) **Bolted T-slot joints:** M5 8.8 into steel T-nuts, **4.5 N·m + Loctite 243 + torque stripe**; re-check at 10 h and every 50 h. No preload on plastic anywhere structural: thumbscrews bear on washers, seat plastic is only clamped. [3b]

## R7 Size, mass, handling
- **R7.1** Fits the C172 baggage door (387 × 559) and a rear-seat lap-belt span; every concept does — the bed, not the aircraft, binds size. [2]
- **R7.2 (E)** gross ~4.42 kg (deck + posts 1.49 kg, V-plate 0.15, trays/yokes 0.42) — same restatement request as D. [4E]
- **R7.2 (E rev C)** gross ~5.70 kg (+1.26 kg: top ring 406/239 + 222 posts, gussets, brackets, fasteners), over the 5 kg bound; 406 × 279 × 268 passes the 387 × 559 door. Antennas ≥ 15 mm under the top rails (dome 15.6). [4E-C]
- **R7.2** Gross ≤ 3.7 kg incl. rods and battery; the rods are the carry handle (3 g swing case, 108 N). [3, 4] **2026-09-21:** the 3.7 kg was the heaviest *printed* concept, not an aircraft limit (C172 baggage 54 kg). Concept D reads **~4.5 kg** (frame 1.67 kg: 2.58 m of 20-2020 + brackets + T-nuts + screws); without the UHR204 hub ~3.9 kg — moot, **UHR204 DECIDED kept (owner 2026-09-21)**, so 4.5 kg is the number. **Owner to restate the ceiling** — the load cases below are recomputed at 4.52 kg (18 g fwd = 798 N, rod MS 1.5, all still closing). [3b, 4]
- **R7.3** One accent colour (canary yellow) only on things a hand touches or an eye must find: thumbscrews, pull tabs, rod caps, label plates.

## R8 Labels and disclosure
- **R8.1** Provisional filed 2026-08-17 (USPTO 64/135,338) → "patent pending" and the real module names **Canary Core / Traffic / Cabin CO / Vibration** are usable on label plates.
- **R8.2** A non-revealing "show" label set stays available as an **option**: the disclosure ledger is still strict, and anything beyond the provisional's content is not covered. Plates are snap-in, so the set is a two-minute swap.
