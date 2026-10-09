# hub_mount — UHR204 USB hub, ports up, on 2020 extrusion (2026-09-29)

**Owner, verbatim:** "let's design an enclosure or method to strap down the USB hub to 1 or more aluminum extrusions.
The hub has 4 holes on each side. The USB ports must point towards the sky to minimize strain for the traffic USB
cables."

**Files:**
- `make_hub_mount.scad`:
  - `variant="dual"` (**recommended**: a backplate across two parallel members at `SPAN`)
  - `variant="single"` (hung from one member)
  - `part = mount | comb`
  - `view = iso | exploded`
- `hub_on_cage.scad`: placement on the as-built back face (photo 39).
- `build_hub_mount.py`: exports the STLs and renders and prints the masses.

**Nothing printed.** Two PLA fit-check slices are in the scratchpad (see the slice section below).

## The hub: Advantech B+B BB-UHR204 ("ULI-414I", photos 26/29)

| item | value | source |
|---|---|---|
| case | **138.24 × 86.92 × 35.00** (2018 sheet: 86.34 ± 0.51, 35 ± 0.51; length scales 138.7) | **PUB**: B&B `UHRx04_3210ds` (2010) dimensioned drawing, and the Advantech `BB-UHRx04 & BB-UHRx07_1819ds` (2018) mechanical diagram |
| port face | a **138 × 35 long face** carrying **host USB-B** at one end, then the LED block, then ports 1–4 (port 1 nearest the LEDs). *Correction to the brief: host USB-B is on the port face, not the short end.* | 2018 front view + photos 26/29 |
| port positions from the TB end | host B 15.6, LEDs 44–60, **p1 71.1, p2 88.5, p3 105.7, p4 122.9**; ports centred in the 35 | EST (2018 drawing scaled at 6.43 px/mm) |
| DC | 3-pole 5.08 terminal block + locking 5.5 mm barrel jack on the **end face at the host-B end** | PUB spec + 2018 end view |
| **"4 holes on each side"** | the two **86 × 35 END faces**, four holes each on the **mid-thickness line**, at **8.4 / 17.5 / 68.83 / 77.93 mm from the back face** (the face opposite the ports) | see the next row |
| … which parts are published | the **inner pair is 51.33 c-c (dimensioned)**; the outer holes sit ~9.1 outboard of each (**scaled, EST**). The factory panel brackets use the pair nearest the port face; the other pair lets the bracket move to the back edge | 2018 end views |
| hole thread | **not published** (M3 or #4-40, **CONFIRM**). The cheeks use 3.4 clearance, which passes either | — |
| mass | 0.64 kg (2018 sheet); the 2010 sheet says 0.38 kg for the older case. Loads are sized at 0.64 | PUB, weigh it |
| ears (not used) | factory panel-bracket holes 153.61 × 25.40, 168.19 overall | PUB 2018 |

The same facts are recorded in `../t1_params.py` as `UHR204`, and the `EST_uhr204_hub` note is corrected.

## Orientation: port face UP

- **Cable exits:** all five plugs point up, which is +z.
  - Tuners (p1 ADS-B, p2 UAT, yellow flat) rise straight to the antenna level with no bend at the plug.
  - Host (B), CO (p3) and vib (p4) rise 20 mm through the comb, then turn down on the bay side (R ≥ 16).
- **Hub labels and LEDs:**
  - The port-face legends ("Industrial USB Hub", port numbers, Bus/Local Power, 100/500 mA) face the sky.
  - Seen from inside the bay, with host B on your right, they read **upside-down**, exactly as in photo 26. They read
    the right way from the back of the cage.
  - **The LEDs stay visible from above** through a window in the comb.
  - The big blue faces carry no information: one bears on the backplate and the other sits under the two straps.

## Retention (R2.4, six directions, twice)

| path | ±x | ±y | ±z | depends on the hub's threads? |
|---|---|---|---|---|
| **Primary: cheeks + 8 screws** through 3.4 clearance into the 4 end holes per end | cheek bearing + screws | screws in shear | screws in shear | yes |
| **Secondary: cradle + 2 straps** | cheeks in bearing (0.4 clearance per end) | **+y** backplate; **−y** two 25 mm straps round hub + cheeks + backplate | **−z** end ledges (20 × 36); **+z** top lip 5 mm over the port face's rail-side edge (clear of the plugs by 4.5) | **no** |

- **18 g load:** 0.64 kg → **113 N**.
- **Strap bearing:** each strap bends 90° over a 2.5 × 45° chamfer at the slot and at the cheek corner, giving
  **0.90 MPa (R2.5 ≤ 1)**.
- **Strap routing:** the straps pass behind the plate in the open back face between the deck rail and the mid rail
  (z 23–48 and 90–117). They also cover the cheek screws, so the screws cannot back out.
- **Insertion:**
  1. Tilt the hub's rail-side top edge under the lip.
  2. Swing the bottom onto the ledges.
  3. Fit the screws.
  4. Fit the straps.
- **Removal (R1.2 Core access):** unplug 5 USB + the TB plug, remove the straps, remove 8 screws, tilt the hub out.
  The comb stays on.

## Cable strain relief (R5.2): the comb

- **Grip height:** a separate bar at z 146.9–152.9, **4–10 mm above the plug overmolds**. It grips every jacket within
  20 mm, so no connector body carries load. The ports are 15 N high-retention (R5.1).
- **Slots:** each slot is open to the bay side with a 1.2 mouth chamfer (house funnel), plus a zip-tie eye.

| slot | width | cable (EST) |
|---|---|---|
| HOST | 6.0 | round Ø5.5 |
| 1 ADSB, 2 UAT | 8.6 | yellow flat ~8 × 2.5 |
| 3 CO, 4 VIB | 5.2 | round Ø4.6 |

- **Labels:** the slot names are engraved on the bar's top face (the bed face), readable from the bay side.
- **Fixing:** 4 × M3 into heat-sets on the backplate's top band. Fit the comb before plugging in, because it covers
  the screws of the single variant's inboard bolts.

## Recommendation: **DUAL, SPAN 125.5, on the inner faces of the BACK deck rail + back mid rail**

- **Position:** hub centred at **frame x 295**, TB end toward the battery / V-mount (+x). Rendered in
  `renders/hub_on_cage_backface.png`.
- **Why the back face:**
  - It uses existing rails and the stiff braced face.
  - The ports-up plug column rises *inside* the back mid rail (15.9 mm clear of its inner face) and *behind* the
    antenna plate's back edge (7.1 mm clear, EST). The tuner leads go straight up to the antenna level with no bend.
  - Case I/O stays untouched (both cases face the front).
  - It is far from the CO panel (the front pair) and the CO node.
- **Why not the lower bay floor, the first candidate:**
  - A ports-up hub on the floor needs 87 mm of case + ~30 mm of plug + a bend under the antenna plate (z 145.5).
    Between the cases that leaves ~13 mm, so the cable must bend hard at the plug unless the antenna plate is
    slotted.
  - In front of the cases it blocks the Orin and RTK I/O.
- **Why DUAL rather than SINGLE:** single is a cantilever off one slot line; dual clamps both ends 125.5 apart.
  Estimated first modes: plate alone ~160 Hz (dual) vs ~30–40 Hz as a bare single-rail cantilever, in the engine and
  prop bands (the cheeks/hub box stiffens both). **Tap-test the single** if it is ever used.

### Consequences
1. **The MTi bridge (printing now) slides left** along the same two rails, from x 222 to **x 83** (plate x 26.5–134).
   - The back face then holds both.
   - MTi board to hub case is **114 mm**. MTi board to battery grows from ~170 to ~280 mm, better for the
     magnetometer.
   - The MTi's own placement argument (braced face, low) still holds. Laterally it is now ~140 mm off centre, which
     is negligible for attitude in a C172.
   - Re-do the alignment and pitch-offset recal at install as already planned.
   - *`../mti_mount/README.md` still says x 222. It is not edited here (family rule); update it when Javi confirms.*
2. **Cargo-strap stations on the back deck rail** must avoid x 26–134 (MTi) and x 204–386 (hub), i.e. stations at
   x ≈ 140–200 or ≥ 390. **CONFIRM** against the belt/strap layout (R2.2).
3. **Cable lengths (EST, drawn path + 2 × 20 grips + slack):**

| run | route | length |
|---|---|---|
| host B (x 348) → Orin front USB-A | up 44, turn down, floor, through the case gap, along the Orin front | **~0.7 m screw-lock A-B** (0.6 m if the hub is flipped, TB left, but then the DC runs 200 mm toward the MTi) |
| tuners p1/p2 (x 293/276) → FlyCatcher | **2026-09-30: the FlyCatcher moved to a window unit** (`../flycatcher_window/`): p1/p2 rise through the comb, then run as one bundle to the window | **0.9 m** bundled (owner: window-to-cage 2–3 ft) |
| CO p3 (x 258) → CO node (front centre) | down, then forward through the case gap | **~0.5 m** |
| vib p4 (x 241) → front-face bulkhead | down, then forward | **~0.5–0.6 m** |
| DC (TB at x 364) → V-mount 12 V out (right end) | 2 A fuse per LAYOUT_E | **~0.2 m** |

4. **Clash checks:**
   - back mid rail: 15.9 clear;
   - antenna plate edge: 7.1 plugs / **2.6 comb bar (EST, tight)**;
   - TB plug end ~x 384 vs battery x 392;
   - hub bay face to the case backs (y 176): 41 mm aisle for the downward cables;
   - E rev B CO panel / front pair: on the other face, no interaction;
   - `t1_stack`: not built on the as-built cage. This family replaces the stack's hub cradle there.

## Material, print, hardware, mass

- **Material:**
  - **Mount in PA12-CF for flight** (4 × M5 preload on plastic in a hot cabin, R6.1/R6.6). ASA is acceptable for the
    comb. PLA is for the fit check only.
  - The UHR204 itself is rated −40…80 °C.
- **Mount print orientation: RAIL FACE DOWN.**
  - The flat bearing face goes on the bed. Cheeks, ledges and lip rise off it. The cheek screw holes are
    teardropped. No supports, no bridges.
  - **No tongues:** they would sit on the bed face. The backplate is located by the bolts and by bearing on the
    rails. It needs no datum, unlike the MTi.
- **Comb print orientation: TOP FACE DOWN,** with the labels on the bed face.
- **MAXSPAN = 3.4,** so `max_bridge_length` = 8.
- **Walls ≥ 4 at every fastener (asserted):**
  - cheek wall at the M3s ≥ 4;
  - M5 counterbore to the plate edge 4.0;
  - comb insert to the M5 ≥ 7;
  - insert skin 1.4.
  - Plate 6.4 (16 lines), cheeks 5.6 (14 lines).

| part | CAD cm³ | PA12-CF g | ASA g | PLA g | print bbox |
|---|---|---|---|---|---|
| `stl/hub_dual_mount.stl` | 151.6 | 137 | 138 | 160 | 181 × 146 × 42 |
| `stl/hub_single_mount.stl` | 133.0 | 120 | 121 | 140 | 181 × 130 × 42 |
| `stl/hub_comb.stl` | 39.4 | 36 | 36 | 42 | 150 × 30 × 35 |

**Hardware (dual):**
- 4 × M5 × 10 BHCS + 4 × 14122 T-nuts (4.5 N·m, Loctite 243, torque stripe);
- 8 × M3 (or #4-40) pan head + 8 washers, each **as long as the factory bracket screw + 4 mm** (cheek 5.6 vs bracket
  1.6). Never longer: the hole depth is unknown;
- 4 × M3 heat-sets (4.4 × 5) + 4 × M3 × 8 for the comb;
- 2 × 25 mm hook-and-loop or cam-buckle straps, ≥ 500 mm;
- 5 × 2.5 mm zip ties.

**Single variant:** 4 × M5 in one slot line (x ±81.3, ±40). Fit the comb after the bolts.

## Parameters (top of `make_hub_mount.scad`)

| param | value | meaning |
|---|---|---|
| `SPAN` | 125.5 | member c-c (dual); single hangs from the member at z 10 + SPAN |
| `Z0` | 26 | hub bottom above the deck bottom; 2 mm above the deck rail top plus the 4 mm ledge |
| `HUB_L / HUB_H / HUB_T` | 138.24 / 86.92 / 35 | case |
| `END_HOLES` | 8.4, 17.5, 68.83, 77.93 | end-face holes from the back face |
| `CL` | 0.4 per end | slide-in clearance between the cheeks |
| `LIP` | 5 × 4 | top lip reach × thickness |
| `STRAP_W` | 25 | strap; slots 3.5 × 27 |
| `PLUG_H` | 30 | overmold height; sets the comb height |
| `ANT_EDGE` | 39 (mount y) | antenna plate back edge (abs y 220, EST); the comb bar must stay 2 mm behind it |

## PLA fit-check slices (house way, NOT started)

- **Method:** `<scratchpad>/slice_hub/slice_house_hub.sh`: OrcaSlicer CLI + `cw_mes/qidi_xplus4_brim.json` + stock
  Bambu PLA, with the printer's PRINT_START macro kept.
- **Preamble:** sed-patched from the CLI's `BED=35 HOTEND=200` to **`PRINT_START BED=60 HOTEND=220`**, M104 S220,
  M140 S60. The S0 shutdowns are untouched and there is no M109/M190.
- **Settings:** bottom shells 4, `max_bridge_length` 8, brim 6.

| gcode | time | filament | `gcode_check` |
|---|---|---|---|
| `hub_dual_mount_fitcheck_PLA.gcode` | **11 h 34 m** | 42.5 m / 102.3 cm³ (~127 g) | PASS |
| `hub_comb_fitcheck_PLA.gcode` | **3 h 06 m** | 13.1 m / 31.5 cm³ (~39 g) | PASS |

A combined mount + comb plate (14 h 41 m, 55.6 m) failed `gcode_check`'s total-extrusion heuristic (≤ 50 m). It is
kept as `REJECTED_gcodecheck_hub_dual_plate_PLA.gcode` and must not be printed. The two parts are therefore sliced
separately.

## CONFIRM (before the flight print)

1. **End-hole thread** (M3 × 0.5 or #4-40) and **depth**. Measure the factory bracket screw length and the hole
   depth; the screw = bracket screw + 4 mm.
2. **End-hole positions:** the outer holes at 8.4 / 77.93 are scaled. The inner 51.33 c-c is published.
3. **Case length** (138.24 PUB vs 138.7 scaled) and height (86.92 vs 86.34). The cheek pocket is 139.04.
4. **Mass** (0.64 vs 0.38 kg): weigh it.
5. **TB / jack / end-screw heights** on the end faces (26–42 / 48–58 / ~43 EST). They must sit in the cheek gap
   (z 23.2–63.1 above the back face).
6. **Case features on the big faces and the back face** (DIN-clip holes, a case screw near the back edge). The
   backplate has a Ø12 relief at the centre.
7. **Plug overmold height (30) and cable sections** (yellow flat ~8 × 2.5; round Ø4.6 / 5.5): they set the comb
   slots and height.
8. **Antenna plate back edge (EST y 220):** the comb bar is 2.6 mm from it.
9. **Back band free** at x 204–390, y 212–259, z 0–160, including the rod clamps. **MTi slide to x 83** OK with Javi.
10. **Where the FlyCatcher sits** on the antenna level (sets the tuner run), and the vib bulkhead location.
11. **Cargo-strap stations** vs the two back-face mounts.
