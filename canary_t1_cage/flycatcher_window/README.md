# flycatcher_window — FlyCatcher window unit on a suction cup (2026-09-30, measured re-cut 2026-10-01)

**Owner, verbatim:** "let's design a robust and clean looking enclosure for the FlyCatcher. We have decided to use a
suction cup to place it near the back window of the aircraft."

The FlyCatcher **leaves the cage**. It becomes a stand-alone window unit with its two stubby antennas, connected by
two micro-USB leads in one **0.9 m bundle** (owner: window-to-cage 2–3 ft) back to UHR204 ports 1 (ADS-B) and 2 (UAT). The cage's RF-3/4 coax runs are gone;
see `../LAYOUT_E.md`, rev B cable table.

**Files:**
- `make_fc_window.scad`:
  - `part = base | lid | hood | adapter | lens | label`
  - `view = iso | exploded | glass | side`
- `build_fc_window.py`: STLs, renders, masses.

**Renders:**
- `renders/fc_iso_closed.png`
- `renders/fc_exploded.png`
- `renders/fc_on_suction.png` (on the cup and the glass)
- `renders/fc_antenna_side.png` (glass standoff)

**Nothing printed.** One PLA fit-check slice of the base is in the scratchpad (see the slice section below).

## Architecture

- **Board orientation:** board **vertical**, with the component face to the cabin so the LEDs and LNA buttons are
  visible.
  - **SMA edge UP:** the stubbies stand vertical; 1090/978 are vertically polarised.
  - **Micro-USB edge DOWN.**
- **Frame used throughout:** x right as seen from the cabin, z up, y from the cabin face toward the glass.

| part | role | material / print |
|---|---|---|
| **base** (glass side) | carries the board on **its own brass standoffs**: 4 screws from the back into their female ends, so no heat-sets or printed bosses under the board. Also the cup's M6 screw, the adapter screws, the **tether tab** and the hood inserts | ASA, back face down |
| **lid** (cabin side) | chamfered bezel, house hex vents, LED lens window, two guarded LNA button holes (the caps rise into them), `CANARY TRAFFIC` label seat, engraved 1090 / 978 / LNA / ADS-B / UAT | ASA, front face down |
| **hood** (**yellow**, the accent) | traps both micro-USB overmolds (micro-USB has no latch) and zip-ties each lead **within 20 mm** (R5.2) | ASA, bottom down |
| **adapter** | an eye-shaped pocket keys the suction base's flange, so the unit **cannot turn on the stud** | ASA, pocket up |
| **lens** | clear plate in a 1.2 ledge + 4 light pipes toward the LEDs | clear PETG, plate down |
| **label** | house dovetail snap plate 44 × 11 × 1.8 (`make_style_coupon` seat) | yellow per the house label rule, or body grey if the hood should be the only yellow |

### The split SMA bulkhead (the main fix: the antennas no longer cantilever off the board)

- **Split:** the halves part on the board's mid-plane, which is also the SMA axis plane. The **top wall is therefore a
  split bulkhead** round both jack threads (6.6 holes).
- **Clamp:** each antenna nut, through a **0.5 mm nylon M6 washer**, clamps the wall (**5.6 thick**, 14 lines) down
  onto the jack bodies. The wall takes the antenna's bending, not the board's edge solder joints.
- **Nut seats:** Ø 14.2, recessed 3.8.
- **Jack positions (MEAS 2026-10-01):** 13.25 from each side edge of the 56.03 SMA edge (mirror-symmetric), so the jacks
  are 29.53 apart. The jack body stands 1.45 above the board edge; the wall's inner face sits on it.
- **Thickness rule:** Javi measured **6.16 mm of exposed thread** with an antenna fully seated (2026-09-30). Wall 5.6 +
  washer 0.5 = 6.1 sits inside it with 0.06 to spare. The RF interface therefore seats fully first, and the nut then
  bites the nylon washer; it compresses, so ±0.1 of print error still clamps.
  - The stack must never exceed the exposed thread, or the stubby could not mate (asserted: ≤ 6.16 and within 0.2).
  - **Nut engagement is not reduced by the wall.** The 6.16 is the thread the nut does *not* use when fully seated.
    The plug's own engagement (~4–5 mm, ~6 threads of the ¼-36 at 0.706 pitch, ≥ 3 required) stays the same.
  - Subtracting an engagement allowance from 6.16 would only open a gap and stop the nut biting.
- **Bending (antenna 184 long, MEAS 2026-10-01; 25 g EST):** with its centre of mass ~92 mm up, at 18 g (4.4 N) it puts
  **~408 N·mm** on the wall.
  - That is **~6.2 MPa** of bearing in the 5.6 hole: ASA bears ~40, so a safety factor of ~7. **The 5.6 wall passes.**
  - The brass jack neck sees ~29 MPa.
  - A 184 mm whip is soft, but its motion now loads the wall rather than the solder joints.
  - A load toward the cabin bears on the lid's half-wall and goes through the 4 lid screws; the other directions bear
    on both halves.
  - No extra rib is needed under the jack body.
- **Decided (owner 2026-09-30):** the stubbies stay on the board's jacks and this split bulkhead is the design. No
  pigtail or extension variant.

### Suction interface and secondary retention (R2.4)

- **The cup's own fastener: M6 (owner 2026-09-30).** It goes **from inside the base** through **6.4 mm clearance** (M6
  close fit) in the back wall and the adapter into the cup, on a Ø 18 fender washer.
  - Head 10 × 6 + washer leaves 3.4 mm under the board.
  - **Cup thread depth = 12.34 MEAS** (Javi 2026-09-30: 6.66 of the M6 × 19 left showing when bottomed).
  - **The supplied M6 × 19 is used**, assumed threaded the full 19 under the head.
  - **Stack-up under the head (re-run on the MEAS flange, 2026-10-01):**
    - Ø 18 × 1.6 fender washer + base floor 4.0 + adapter floor 3.4 = **9.0 grip**.
    - Adapter floor: the adapter's 7.6 less the 3.5 flange pocket less the **0.7 disc relief**. The disc is 1.0 MEAS,
      so it bears and the flange plate runs 0.3 clear.
  - **Engagement 10.0 (1.67 D), margin 2.34 to the bottom of the thread.** Both are asserted (≥ 1.5 D, ≥ 1 pitch).
  - **No thicker adapter or longer screw is needed.** The pocket only has to *key* the flange outline: it engages 3.2
    of the 6.12 flange edge, and the rest of the flange sits below the adapter face.
  - **The washer is needed:** under the bare Ø 10 head a hand-tight M6 (~1.5 kN) would bear ~33 MPa on the printed
    floor; the Ø 18 fender brings it to ~7 MPa. Do not drop it, and do not stack extra washers (each 1.6 mm costs
    engagement).
- **Adapter keying:** the adapter's pocket is the flange outline + 0.4. The **raised centre disc bears**; the lobes run
  0.3 clear, so the outline only keys. The adapter is fixed to the base by 2 × M3 from inside, at x ±17 diagonally, so
  they clear the eye pocket (≥ 1.6 wall asserted), the 2×20 header and the M6 fender washer.
- **Why a separate adapter:** a keyed pocket on the base's bed face would be a 34 mm bridge.
- **Flange, MEAS 2026-10-01:** screws **39.85** c-c, overall **62.96**, so the lobe radius is 11.56; plate **6.12**;
  disc height **1.0**. Still EST: the centre width (34) and the disc Ø (27). Lobes are oriented vertical.
- **Unit mass ≈ 388 g EST:** printed parts 95 g, board 48, antennas ~50, cup ~180, hardware ~15.
  - At 9 g forward that is **34 N**; at 18 g **69 N**.
  - A suction cup is **not** a restraint.
- **Tether:** the base carries a **tether tab** (top-left, in the back-wall plane, Ø 6.5 hole, edges broken). Its
  section is 2 × 4.75 × 6 mm, loaded in the layer plane, ~1.7 kN EST.
  - Lanyard: **2 mm Dyneema (≥ 1 kN) or 550 paracord** with a small locking carabiner, to a seat-belt anchor or the
    cage.
  - Keep ≤ ~100 mm of slack so a released unit cannot swing far.

### Glass, sun, vents

- **Glass standoff (EST):** the flange top is **62 mm** off the glass, so the antenna axis is **82 mm** from the glass
  and the antenna skin 76 mm.
- **Antenna angle:** the stubbies run **parallel to the glass**. On the C172's slanted rear window they tilt with it:
  a 30° tilt costs ~1.2 dB on vertical polarisation.
- **Window frame clearance:** the antennas are **184 long** (MEAS), so the tips are **~223 mm above the cup centre**.
  The whole unit, hood to tip, is ~287 tall.
  - Keep the cup centre **≥ ~230 mm below the top of the glass**, measured along the glass. Otherwise the swivels must
    fold, which costs polarisation.
  - **CONFIRM** this fits the C172 rear window at the spot Javi picks.
- **Vents:** **33 front + 32 side hex cells (5 AF, house field from `make_t1_panels.scad`) = 14.1 cm² open**.
  - Inlet: low, over the tuners and the USB end. Outlet: high, beside the LNA buttons, plus side rows.
  - The board draws ~2.8 W (250 + 315 mA at 5 V, PUB).
  - **The glass-side back face is solid:** that is the sunlit face.
- **Colour:** a **black ASA unit at a sunlit window soaks** to roughly 70–80 °C surface (EST), close to the tuners'
  ratings. **Print the flight unit in LIGHT-GREY ASA** (the renders use it). Black is acceptable only for a
  shaded/north window.

### Board, standoffs, cables

- **Standoffs:** the existing **brass standoffs** stay on the board. 4 × M2.5 screws come from the back of the base
  into their female ends; the holes are 2.9, or 3.4 if they turn out to be M3.
  - They set the 11 mm (EST) gap the 2×20 female header (8.5) needs.
  - The front-side brass hexes are assumed to be nuts, inside the 14.2 front clearance.
- **Micro-USB (MEAS 2026-10-01):**
  - Receptacles 21.15 from each side edge (mirror-symmetric), so x ±6.865, 13.73 apart. ADS-B OUT is on the left,
    UAT OUT on the right (front view).
  - Plug body 9.55 × 7.45 × 18.12 long; lead Ø 5.61.
  - **Openings 9.95 × 7.85** (+0.4).
  - Each plug body protrudes **8.5** into the yellow hood's pocket (pocket 8.8 deep). The pocket floor traps the boot
    end, so the plug cannot back out.
  - **Lead slots 6.0**, open to the cabin with a 1.2 mouth chamfer. A zip-tie path runs round each lead **6 mm below
    the plug** (R5.2 ≤ 20). The hood is 20.8 tall.
- **LNA buttons — LID DECISION (2026-10-01):** the caps measure **16.93** above the board (EST was 9.5), which broke
  the old lid. The caps now **rise into their own holes** and stop 0.5 under the lid face.
  - Holes Ø 8.4, chamfered: cap 6.6 EST + 0.9 radial, which absorbs the EST x positions.
  - The buttons are **guarded but finger-pressable**: no pen, no protruding cap to knock.
  - **The lid grows 3.7 deeper** (front clearance 10.5 → 14.2; enclosure 30.3 → 34.0 deep). The front is still one
    flat bezel.
  - **The base is unchanged in shape.** The split stays on the board mid-plane = the SMA axis, so the base's
    side-wall half is the same height; only the lid's half grows.
  - Positions: 4.46 down from the top edge MEAS; x 23.1 / 33.7 EST.
- **LEDs:** a 12 × 9 window centred on the cluster at **28.10 from the left / 18.61 from the top** (MEAS 2026-10-01).
  The cluster is round the airplane icon (Red power, Blue LNA on, Green GPIO). The clear lens has 4 light pipes,
  13.2 long, at the EST individual LED positions.

## Hardware

- 4 × M2.5 × 6 (board standoffs; M3 × 6 if they are M3);
- 4 × M3 heat-set (4.4 × 5) + 4 × M3 × 20 SHCS, flush from the front (lid, now 18.2 deep);
- 2 × M3 heat-set + 2 × M3 × 12 from below (hood);
- 2 × M3 heat-set in the adapter + 2 × M3 × 8 from inside the base;
- the cup's supplied **M6 × 19** + **one** Ø 18 × 1.6 fender washer;
- 2 × 0.5 mm nylon M6 washers (SMA);
- 2 × 2.5 mm zip ties;
- lanyard + locking carabiner.

**Assembly order:**
1. Fit the heat-sets.
2. Fix the adapter to the base (2 × M3 from inside).
3. Fix base + adapter to the cup (the supplied M6 × 19 + one fender washer, from inside, hand-tight ~1.5 N·m; the pocket keys the flange).
4. Fit the board on its standoffs. The jack threads drop into the base half-holes. Fit 4 × M2.5 from the back; they
   reach past the adapter edge with ~0.3 mm to spare.
5. Fit the lens and snap in the label.
6. Fit the lid (4 × M3 from the front).
7. Fit the washers, then the antennas, hand-tight.
8. Plug ADS-B and UAT, then fit the hood (2 × M3) and zip-tie each lead.
9. Attach the tether lanyard.

## Print, mass, slice

- **Walls ≥ 4 at fasteners:** the SMA bulkhead is 5.6 and the back wall 4.0. Insert walls ≥ 1.6 are asserted.
- **Look:** chamfered 1.5 × 45° bezels, 4 mm clipped corners, flush counterbored screws, recessed nut seats.
- **No supports:** every overhang is ≤ 45° or a short bridge.

| part | CAD cm³ | ASA g | PLA g | print bbox | MAXSPAN |
|---|---|---|---|---|---|
| `stl/fc_base.stl` | 38.0 | 35 | 40 | 80 × 85 × 16 | 4.4 (horizontal insert holes) |
| `stl/fc_lid.stl` | 32.5 | 30 | 34 | 64 × 85 × 18 | 12.5 (label-seat floor) |
| `stl/fc_hood.stl` | 16.1 | 15 | 17 | 46 × 22 × 21 | 6.2 (counterbores) |
| `stl/fc_adapter.stl` | 16.7 | 15 | 18 | 44 × 70 × 8 | — |
| `stl/fc_lens.stl` (PETG) | 0.4 | 0.4 | — | 14 × 11 × 14 | — |
| `stl/fc_label.stl` | 1.0 | 1 | 1 | 45 × 12 × 2 | — |

**PLA fit-check slice of the base (house way, NOT started):** `<scratchpad>/slice_fc/fc_base_fitcheck_MEAS1001_PLA.gcode`.
- **Superseded slices** are renamed `STALE_fc_base_fitcheck_PLA.gcode` (¼-20), `STALE_fc_base_fitcheck_M6_PLA.gcode`
  (SMA wall 6.8) and `STALE_fc_base_fitcheck_M6_SMA616_PLA.gcode` (EST jack, button and USB positions).
- **Method:** `slice_house_fc.sh`: OrcaSlicer CLI + `cw_mes/qidi_xplus4_brim.json` + stock Bambu PLA.
- **Preamble:** **`PRINT_START BED=60 HOTEND=220`**, M104 S220, M140 S60, verified. The S0 shutdowns are untouched and
  there is no M109/M190.
- **Settings:** bottom shells 4, `max_bridge_length` 9 (MAXSPAN 4.4 + 5), brim 6.
- **`gcode_check`:** PASS.
- **Result: 3 h 08 m, 11.9 m / 28.65 cm³ (~36 g).**

## CONFIRM (rows still open after the 2026-10-01 bench sheet)

1. **F4 / F5 standoffs:** M2.5 vs M3 (holes 2.9 / 3.4), and the length behind the board (11 EST). It sets the
   board-to-back-wall gap and the M6 head clearance.
2. **F16 flange centre width (34 EST) and F18 disc Ø (27 EST):** the pocket width and the disc relief.
3. **F20 cup height**, glass to flange top (62 EST): the 82 mm glass standoff.
4. **F21 cup screw:** threaded the full 19? It needs ≥ 10 of thread at the tip. Also: does the cup's thread start at
   the disc top?
5. **F8 LNA button x** from the left edge (23.1 / 33.7 EST), and the **cap Ø** (6.6 EST). The Ø 8.4 holes absorb
   ±0.9.
6. **Individual LED positions** inside the cluster: the light pipes. The window centre is MEAS.
7. **Antenna fit at the window:** 184 mm antennas need the cup ≥ ~230 mm below the top of the glass. Also the antenna
   mass (25 g EST): it sizes the wall check, which has SF ~7 so is not critical.
8. **F24 lanyard anchor** point and distance.
