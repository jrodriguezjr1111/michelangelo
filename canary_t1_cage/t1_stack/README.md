# t1_stack — tactical stacking system for the T1 compute block (2026-09-26)

**Owner, verbatim:** "let's design a tactical looking stacking system for the Orin, components, and USB hub, modeled
after the current setup. It will fasten to a SmallRig cheese board inside the cage."

The goal is to turn photo 36 into one keyed, swappable block. Today that photo shows cases stacked loose, the MTi-3
**taped** to the Orin lid, the hub lying loose on the frame bottom, and the cables hanging free. The block is:
- the two repurposed aluminium cases (**Orin** on top; **RTK + LTE** below, with the ZED-F9P and EG25-G inside);
- the **UHR204** hub;
- the **SmallRig V-mount plate** and V99 Pro battery;
- the **MTi-3** board.

It all sits on a SmallRig cheese plate that bolts to the concept-E 2020 deck.

**Nothing has been sliced or printed.** Every case, V-plate, battery and cheese-plate dimension is **EST from photos
33-35**. Fill in `measure_sheet.html` with calipers before printing the ladders.

| file | what |
|---|---|
| `make_t1_stack.scad` | the family engine: all geometry, echoes and asserts. `part=` selects the views and the per-part exports |
| `stack_on_deck.scad` | placement on the E deck, using `t1_concept_E.scad` read-only; **red = interference with the E antenna level** |
| `build_t1_stack.py` | exports the STLs/DXF with the manifold backend and renders the PNGs, failing on any warning or assert |
| `measure_sheet.html` | numbered-drawing caliper sheet that autosaves in the browser and exports CSV |
| `renders/stack_iso.png`, `stack_exploded.png`, `stack_io_face.png`, `stack_swap.png`, `stack_on_E_deck.png` | renders |
| `stl/*.stl`, `stl/imu_plate_al3.dxf` | the printable parts, plus the aluminium IMU plate outline |

## Architecture
Stack frame: X is across the I/O faces, Y is the **slide axis** (+Y points out through the I/O face), Z is up from
the cheese plate. From the bottom up:

1. **Cheese plate** (SmallRig, model **CONFIRM**). The model draws a 190 × 210 × 10 placeholder.
2. **Hub cradle**: printed floor, back stop and side lips. The UHR204 lies flat with its **downstream long face toward
   the I/O side**, 5 mm behind the case faces, and its host + DC end facing the left ladder's open window. It slides in
   from +Y. It is held in Z by a 5 mm EPDM strip under the RTK ledge and in Y by the left ladder's dog. Hub ports are
   the 15 N high-retention type, and the leads go straight up to the comb rows.
3. **Two side ladders**, left and right, mirrored. Each is an open frame: back stile, front stile, bottom rail with an
   outboard foot, a **ledge rail per case**, a **tongue that rides the case's lowest side groove**, and a top cap rail.
   - The side geometry comes from photo 34. The shells are extrusions with **longitudinal grooves along the slide axis**
     and through vent slots in the mid band, so the tongue gives Z retention both ways while the case slides in.
   - This is **CONFIRM**. If the groove is cosmetic, set `KEY="lip"`: the case then relies on the ledge and the
     4 mm cap lip only.
   - The stiles carry hex lightening. The **side window between the stiles is completely open**, which is where the
     fins and vents are.
4. **RTK/LTE case** on ledge 1 (z 47-88). **Orin case** on ledge 2 (z 96-143). There is a 4 mm through-air channel between them.
5. **One captive thumbscrew per case (and one for the hub).** Each is a yellow knurled M5 that works as a **swing dog**
   on the front stile. The dog pad bears on the right edge of the I/O end plate, between the corner screws and clear of
   the ANT SMA. Tightening it drives the case back onto its **back stops**.
6. **IMU datum plate**: 6061 Al, 3 mm (PA12-CF 4 mm is the alternative).
   - It bolts across both ladder caps with 2 × M4 per side and **one Ø3 dowel per side at different Y**, so it fits one
     way only.
   - Its back edge is **notched Ø53 round the Orin fan grille**.
   - The MTi-3 Uno shield sits on 4 × M3 standoffs, 5 mm, on the Uno pattern. The board's +X arrow points **stack -X,
     which is deck +Y (the nose)**. An arrow and "NOSE" are cut through the plate. Nothing is taped.
7. **V-mount bracket** off the back stiles (4 × M4) and the plate (1/4-20 slots), as in photo 34. It carries the
   SmallRig V-plate on 1/4-20 slots and a 3/8-16 centre (pattern **CONFIRM**). The battery hangs 86 mm behind it.
   **Secondary strap slots** are built in, because R2.4 needs a latch and a strap.
8. **Cable bar** across the I/O face, **50 mm ahead of it** to clear the plug keep-out.
   - Two windowed arms off the front stiles, with a **comb row at each inter-level gap** (hub/RTK, RTK/Orin, top).
     Slots are 3.4 mm at a 7.6 mm pitch and **20 mm deep for the jacket grip**, with zip-tie eyes at the row ends.
   - The rows sit **only in the gaps**, flush with the ledges, **so each case slides out through the cable bar** and
     rides out on the row below it. Its cables stay dressed in the combs.
   - Outboard left is a **coax service-loop bay**, 30 × 34, open top and bottom, with a coax exit slot. Its front face
     carries **three yellow label seats** (the house 44 × 11 plate from `make_style_coupon`): HUB, RTK-LTE, CORE.
9. **micro-USB hood** (`uusb_hood`) for the tuner end of hub ports 1-2. The FlyCatcher is not in the stack.

**Tactical look, with each feature doing a job.** The chamfers are print chamfers or insertion lead-ins. The hex
cut-outs are lightening in the stiles and the cradle, and each drains or vents. The side windows are the fin airflow.
The single yellow accent marks only what a hand touches (thumbscrews) or an eye must find (labels).

### Swap (R1)
| item | steps | tools |
|---|---|---|
| **Orin case (Core)** | 1. unplug at the I/O face (cables stay in the combs) · 2. loosen the dog ½ turn and swing it · 3. slide out +Y through the cable bar | 0 |
| RTK/LTE case | same | 0 |
| hub | 1. unplug · 2. dog · 3. slide out (both cases can stay in) | 0 |
| battery | V-lock release, plus the secondary strap | 0 |
| IMU board | 4 × M3 (plate stays, datum unchanged) · RE-CAL | driver |

A Core swap **never disturbs the IMU plate**: the case slides out under it (`renders/stack_swap.png`).

### Six-direction retention
- **Cases:** ±X ladder rails (0.25 per side) · −Y back stops · +Y dog under thumbscrew preload · ±Z ledge + groove tongue (cap lip as backup).
- **Hub:** ±X ladders · −Y cradle stop · +Y dog · +Z EPDM under the ledge.
- **Battery:** V-lock + strap.
- **IMU plate:** 4 × M4 + 2 dowels.
- **Stack to plate:** 1/4-20 through the foot, cradle and bracket slots.
- **Plate to deck:** 4 × M5 into 14122 T-nuts.

## Thermal: the fins stay open
- **Ladder contact:** each ladder touches a case only on a **4 mm ledge and the tongue, in the bottom 7.5 mm of each
  side**. The window between the stiles leaves **74 % of each side's length open** over the vent band (asserted:
  tongue top ≥ 2 mm below the vent band).
- **Airflow:** there is a **4 mm through-air channel** between the cases, open front and back. At the **Orin fan grille**, the IMU plate
  is notched Ø53, so nothing sits on the grille. The MTi board, 17 mm above the case top, still overhangs the grille's
  front edge by **~14 mm**, shadowing about 26 % of the grille footprint. The rest of the grille is open to the sky, and
  the covered part draws sideways through the 17 mm gap. If the fan measures further forward, the assert fails and the
  plate moves to the back end.
- **Battery:** the battery hangs off the back end, away from the side-vent exhaust (R4.3).
- **Hub:** the hub is a 2 W metal IP30 box on a hex-vented cradle.

## Parameters (`make_t1_stack.scad`)
| name | value | tag | note |
|---|---|---|---|
| `CASE_W / CASE_D` | 132 / 106 | EST | I/O-face width (scaled on the RJ45, USB-A, DP and SMA bodies) / face-to-back |
| `ORIN_H / RTK_H` | 47 / 41 | EST | photo 34 heights |
| `ENDPL_T` | 3 | EST | end plate thickness, inside `CASE_D` |
| `GROOVE_Z / _W / _D`, `KEY` | 6 / 3.0 / 1.2, "groove" | EST · CONFIRM | the tongue's groove; set `KEY="lip"` if there isn't one |
| `VENT_Z` | 0.30-0.75 H | EST | side vent band that must stay open |
| `FAN_D / FAN_YC` | 45 / 38 from the back | EST | Orin grille |
| `HUB` | 139 × 87 × 35 | PUB | UHR204; ear pattern unknown |
| `VPL` | 110 × 20 × 96 | EST · CONFIRM | SmallRig V-plate (model unknown) |
| `BATT` | 100 × 86 × 120 | EST | **conflicts** with `t1_params` 107 × 74 × 64. Measure. |
| `CH, CH_Y0, CH_P` | 190 × 210 × 10, −38, 20 | EST/DSN · CONFIRM | cheese plate; the pitch is a placeholder and every foot hole is a slot ≥ 1 pitch |
| `CLR` | 0.5 total | house | slide-in clearance |
| `IN_W` | 140 | DSN | ladder inner span, set by the hub |
| `LAD_T / STILE / FOOT_W` | 6 / 14 / 14 | DSN | 6 = 15 lines of 0.4 |
| `LEDGE_T / LEDGE_IN / RAIL_IN` | 4 / 4 / 3.75 | DSN | |
| `HUB_GAP / CASE_GAP` | 4 / 4 | DSN | hub gap is set by the ledge print chamfer; case gap is the air channel |
| `CAP_T / CAP_IN` | 8 / 4 | DSN | cap rail (M4 inserts for the IMU plate) / drawer lip |
| `IMU_T / MTI_SO` | 3 / 5 | DSN | |
| `PLUG_KEEP` | 50 | DSN | cable bar ahead of the I/O face |
| clearances | M4 4.4, M5 5.4, 1/4-20 6.8; heat-set M4 5.6 / M5 6.4; chamfer 1.2; label seat +0.15/side | house | |

Model echo:
- **Z:** hub 4-39, RTK 47-88, Orin 96-143, ladder top 152, IMU plate 152-155, **MTi top 174 above the plate top**.
- **Envelope (EST):** **180 wide at the feet** (182 at the loop bay) × **300 along the slide axis including the
  battery** (200 without) × **174 tall** above the cheese plate, which is about 212 above the deck underside on the
  risers.

## Material, print orientation, hardware
| part | material | orientation | CAD cm³ |
|---|---|---|---|
| `ladder_L`, `ladder_R` | **PA12-CF for flight** (they carry the IMU datum and the thumbscrew preload hot, R6.1); ASA is acceptable; PLA for fit-check only | **standing on the foot flange as installed** (34 × 120 footprint, 152 tall). Ledges bend along their layers; 45° chamfers under every rail standoff; ≤ 4 mm plain overhangs; no supports | 78 each |
| `vplate_bracket` | PA12-CF (a hanging 640 g battery on a hot preload) or ASA | **face down** (152 × 112 flat); moment within layers, into the stiles by 4 × M4 | 96 |
| `hub_cradle` | ASA | floor down | 50 |
| `cable_bar` | ASA | comb tips and the loop-bay front face down; ≤ 34 mm bridges over the arm windows | 115 |
| `dog` ×3 | ASA | flat | 2 each |
| `uusb_hood` | ASA | floor down | 6 |
| IMU plate | **6061-T6 Al 3 mm** from `stl/imu_plate_al3.dxf` (PA12-CF 4 mm STL as the alternative) | — | — |

Printed total **424 cm³ CAD → ~360 sliced → ~385 g ASA, ~38 h** (class estimate using the repo's 0.105 h/cm³; not
sliced). Every part fits the QIDI Plus 4 bed, the largest being 182 × 150. **Never PLA in the aircraft.**

**Hardware:**
- 3 × M5 × 16 knurled captive thumbscrews (yellow) + 6 M5 heat-sets;
- 12 × M4 heat-sets + 12 × M4 × 12 BHCS (IMU plate, V-bracket, cable bar);
- 2 × Ø3 × 8 steel dowels;
- ~16 × 1/4-20 × 12 BHCS (feet, cradle, bracket, V-plate);
- 4 × M3 × 5 standoffs + screws (MTi);
- 5 × 10 EPDM strip (hub) and EPDM dots on the dogs;
- 25 mm cam strap for the battery;
- 3 × yellow label plates;
- **deck:** 4 × M5 × 25 BHCS + 4 × `14122` T-nuts + 4 × 8 mm Al risers.

## Mass estimate (all EST until weighed, measure sheet row 15)
| item | g |
|---|---|
| Orin in its Al case | 750 |
| RTK/LTE case (ZED-F9P, EG25-G inside) | 480 |
| UHR204 hub | 640 (EST-high) |
| SmallRig V-mount plate | 190 |
| cheese plate (depends on the model; a 190 × 210 × 6 Al plate with holes ≈ 450) | 300-450 |
| printed parts | 385 |
| IMU plate (Al) + MTi-3 | 95 |
| hardware + EPDM + strap | 100 |
| **stack without battery** | **~2.9-3.1 kg** |
| V99 Pro battery | 640 |
| **stack with battery** | **~3.6-3.7 kg** |

Compared with concept E rev B (bare Orin 250 on a tray, ZED and EG25 on trays, battery on a tray), the stack adds the
two aluminium cases (~0.9 kg of enclosure) and the cheese plate (~0.4 kg), less the trays it replaces. **E gross rises
roughly +1.0-1.3 kg**, to about 5.5-5.7 kg on the rev B frame. Recompute in `envelope_check.py` once the cases are
weighed; I have not added a stack block there.

## On the concept-E deck — `stack_on_deck.scad`, `renders/stack_on_E_deck.png`
**Placement: bay R (the Core bay), with the slide axis along deck +X.** The I/O face and cable bar point at the
**x = 406 end face**, which becomes the service face, and the stack's −X is deck +Y (the nose), so the IMU arrow is
correct.
- The cheese plate spans **deck x 194-404** and bolts with **4 × M5 into 14122 T-nuts in the centre member (x 203) and
  the end member (x 396)** on **8 mm Al risers**.
- If the owner's SmallRig plate is shorter than ~210 mm, add one 239 mm 20-2020 cross member in bay R at the plate's
  far bolt line (2 × 20-4119, 4 T-nuts, ~$20).
- The cable bar stops at the x = 406 end-face plane.
- The battery hangs over the centre member into bay L at deck x 106-192, y 90-190, bottom z ~40.

**What changes in the E layout (rev B):**
1. **The rev B Core placement is superseded.**
   - Orin, hub, ZED-F9P and EG25-G leave the trays (they are in the stack now). So do the battery and V-plate.
   - The MTi-3 corner plate goes unused, because the IMU is on the stack.
   - The **bay R tray** stays as the deck's shear panel, with four holes for the risers.
   - **Bay L keeps the PDB** at (118, 42), which is clear of the hanging battery.
   - Bay L **takes the FlyCatcher** (e.g. at 30, 30), with ~450 mm hooded micro-USB leads to hub ports 1-2.
   - The bay-R front-face bulkheads (vib USB, DC) are unaffected.
2. **Belt-band logic, rechecked and restated.**
   - The battery no longer stands in the y 100-172 belt band on bay L's tray. It hangs off the stack end. A lap belt
     laid across the deck at the old height would now ride over a 212 mm stack and its IMU plate, which is wrong.
   - **New rule: the lap belt runs at deck level through a tunnel.** It passes over the tray skin (z 24) and under the
     cheese plate: the risers give 4 mm, clear of the risers at y 70 / 210. It also passes under the hanging battery,
     with 16 mm clearance.
   - So the belt holds the **deck members**, and the stack is held to the deck by its 4 M5 bolts. At 18 g on 3.7 kg
     that is 650 N, about 210 N tension and 160 N shear per M5 into steel T-nuts, which is small against the ~2 kN
     class.
   - The cargo straps at x 100 / 306 also pass under the battery and through the tunnel.
   - The **battery's secondary strap is now mandatory**, because the belt no longer rides the battery.
3. **Antenna level: hard conflict in rev B and rev C** (red in the render).
   - The stack top is at **z ~212** (MTi), but the E rods sit at **axis z 151.7 (underside 144)**. The rods, MA963,
     dome and CO tray all pass through the stack. The rev C right yoke bridge (z 123-133) also blocks the end face that
     the cases slide out through.
   - Fitting the stack **requires the antenna level to rise to a rod axis of about z 230 or more**, which is +78 mm.
     In rev C that means **posts ~300** instead of 222, a rail top of ~342 and **overall ~346**, at about +140 g.
   - That still passes the 387 × 559 baggage door (279 × 346 section, 41 mm spare). The GNSS mask angles are unchanged,
     because they depend only on h and d.
   - The raised yoke bridges (z ~201-211) then clear the whole end-face swap path.
   - Moving the hub out of the stack saves only 39 mm, which is not enough. **This is the owner's call**; the E files
     have not been edited.
4. **R3.1 (IMU datum) is weaker than rev B's aluminium corner plate.** The MTi now sits ~190 mm up on printed ladders.
   That is why the ladders are PA12-CF, the plate is aluminium with dowels, and the cases are preloaded into the frame
   (so they act as shear webs). **Tap-test or vib-node the stack top before trusting attitude.** If it rings, the
   fallback is the rev B corner plate on the deck.

## CONFIRM — measure first (the P1 rows of `measure_sheet.html`)
1. **Case outer L × W × H**, both cases. Does the lower case really measure ~10 % narrower, as photo 33 suggests?
2. **Side groove**: height, width and depth, or "none". This decides `KEY`.
3. **I/O end plate**: thickness and how far it is proud; the dog bears on it.
4. **Orin fan grille** position and diameter; this drives the IMU plate notch.
5. **Cheese plate model**, outline, hole grid and clearance holes. SmallRig's product pages do not publish hole
   drawings, so we need the model number or calipers. If it spans less than ~210, add a cross member.
6. **V-mount plate model** and back-face hole pattern; **battery outline** (conflicts with the repo table).
7. UHR204 body and any ears / DIN clip; port positions.
8. MTi-3 Uno-shield outline and hole pattern.
9. Case masses, for the 18 g check.

## Verification performed
- `openscad` renders every part and view with no warnings, and **all asserts pass**. The asserts cover: rail
  standoff, tongue reach, the vent band left open, the hub/ledge chamfer, the fan-vs-IMU plate, the plug keep-out, the
  air channel, and the feet on the plate.
- The **manifold backend** exports all 8 printable parts cleanly (`build_t1_stack.py` fails on any warning).
- Volumes come from the STLs. `measure_sheet.html` was checked headlessly: tags balanced, JS syntax OK, 32 rows.
- **Not sliced, not printed** (house rule for this task).
