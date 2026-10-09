# mti_mount — Xsens MTi AHRS mount on 2020 extrusion (2026-09-28)

**Owner, verbatim:** "let's design a plate or mount for the MTi AHRS. I will mount it to 2020 aluminum extrusions."
Then: "the MTi can straddle two members."

`make_mti_mount.scad`:
- `variant="bridge"` (**primary**: plate across two parallel members at `SPAN` c-c);
- `variant="saddle"` (fallback: straddles one member);
- `part = mount | stop | hood`.

Also here: `build_mti_mount.py` (STLs, renders, masses) and `mti_on_cage.scad` (placement (a) on the as-built back
face). The first brief's *corner* variant is superseded by the bridge and not built. **Nothing printed.** One PLA
fit-check slice is in the scratchpad (below).

## The board (photos 40/41): MTi 1-s DEV Rev 2.6 with the MTi-3 module
| item | value | tag |
|---|---|---|
| outline | **58.1 × 53.3**, a *trimmed* Arduino shield (Uno x 11.2-69.3, y 0-53.3) with a V-notch on the low-x edge | EST, photo 41 at 14.2 px/mm (board plane) |
| holes | **MEAS 2026-09-28 (Javi, caliper).** Viewed from the component side with USB-C at the bottom-left, origin at the upper-right hole: **UR (0, 0), LR (0, −47.75), UL (−47.95, −9.03)**. The left hole sits 9.03 mm *below* the right pair. This replaces the Uno-derived A/B/C (dx 52.1, dy 5.1) | MEAS |
| hole Ø | 3.2 (M3 clearance for the standoffs) | EST |
| pattern on the board | UR = Uno A, LR = B, UL = C (this frame is x = −x_uno, y = −y_uno). The measured pair is centred where photo 41 put A/B, at Uno (14.65, 2.775) / (14.65, 50.525), with UL at (62.6, 11.805). So UR sits ~3.5 from the right edge and ~2.8 from the top | hole-to-edge EST |
| Uno hole D (66.1, 35.5) | not on this board (the MTi socket); confirmed by the three-hole caliper report | MEAS |
| header tails under the board | **~10.5** (stacking headers; photographed end-on, so not scalable) | EST, CONFIRM |
| USB-C "COM" | high-x edge, Uno y 41-49. In the frame above its centre is at (−54.65, −42.2): left of the UL hole and below the pair midline, i.e. the **bottom-left corner**. The hood sits on it (asserted) | EST |
| sensor axes (silkscreen) | **X_s = −x_uno, Y_s = −y_uno, Z_s out of the component side**. With USB-C at the bottom-left this reads **X right, Y up**, which agrees with the brief. Photo 41 was simply taken rotated | photo 41 |

Manual MT0513P fig. 9 (43.5 × 34, M2.5 on 23 × 28) is the **older** DK, not this board. Recorded in
`../t1_params.py` (`MTI_DEV`; the `mti3_dk` tuple now uses 58.1 × 53.3).

**Standoff:** COTS **M3 × 12 male-female aluminium** hex, threaded into M3 heat-set inserts in the plate. That's
non-magnetic next to the magnetometer. Tail clearance:
- **Both variants:** 1.2 mm relief grooves run the full board length under both header rows. Each groove is broken
  by an 8 mm boss round each standoff insert. That gives 12 − 10.5 + 1.2 = **2.7 mm** (≥ 2, asserted).
- **Bridge:** there is also an **open window** under the board centre, at mount x −16 to +19.
- **Window margin:** the window keeps a ≥ 4 mm wall to every insert (asserted). The measured UL hole moved 3.5 mm
  inboard, so the window's −X edge moved from −20 to −16.

The board goes on and off from above with 3 M3 screws **without touching the datum**. Recalibrate after any board swap
(R3.2).

## Datum (R3.1 rigid, keyed, tied to metal, never a slide; R3.2 re-seat ≤ 0.2°)
| DOF | how | repeatability (EST) |
|---|---|---|
| Z, pitch, roll | the plate's flat underside on the member face(s), clamped by **2 × M5 per member into 14122 T-nuts** (R6.6: 4.5 N·m, Loctite 243, torque stripe) | face flatness, ≤ 0.05° |
| lateral + yaw | **one hard skirt face against a member side face.** Bridge: the *inner* face of member 1. Saddle: the −y face, with 2 crush ribs on the opposite skirt so it self-biases. Push it against the skirt face while torquing | extrusion face straightness over ~78 mm, ≈ 0.05° |
| (coarse) | 5.6 wide × 1.5 deep **tongue** in each 6.0 slot: location and anti-rotation only. Its 0.4 mm play alone would allow ~0.4°, which is why the skirt is the datum | — |
| axial | a separate **stop block** in the datum member's slot, **bolted once, torque-striped, never moved**. The mount's +X end face butts its flat face | contact, ~0.1 mm |
| keying | a rib on the stop face enters a notch at the mount's +X end only, so the mount **cannot seat reversed**. The board can't go on rotated 180° with 3 screws: the single hole would land **100.4 mm** from its insert, and it sits 14.8 mm off the pair midline (asserted). With only the 2 pair screws the pair is symmetric, but a reversed board visibly hangs ~29 mm past the +X end with USB-C away from the hood. **Fit all 3 screws** | — |

The **+X arrow is engraved** on the top face beside the board. The top face is the bed face (house rule: never raised
on the bed face), so it can't be embossed. On the flat bridge and the saddle it points to the nose. On the vertical
bridge (a) it points laterally; see the axes note below.

**USB-C strain relief (R5.2):** a printed **hood**, 2 × M3 into plate inserts.
- A tunnel over the overmold keeps the connector body unloaded, and a **zip-tie slot grips the jacket within 20 mm**.
- Thread the plug through the tunnel, plug in, then bolt the hood down.
- The cable leaves along −X_s, which is aft when X points to the nose.

## Where it goes, and which variant: **recommend the bridge, placement (a)**
| | **(a) vertical, back face: deck rail → mid rail** | (b) flat on two parallel members |
|---|---|---|
| SPAN | **125.5** (photo 39, the same rails, no new metal) | ≥ 73, so the 53 mm board sits inside the gap (render at 80) |
| on the as-built cage | inner faces of the **back** deck and mid rails, **centred at frame x 222**, board facing into the bay **~80 mm behind the case backs**. The back of the lower bay is free since both panels moved to the front. The datum skirt rests on the deck rail's **top face**, so gravity seats it on the datum | needs a **new member**. The antenna plate occupies the mid level. Behind the cases, a flat bridge needs SPAN ≥ 73, which puts a new 404 mm lateral member within ~3 mm of the case backs (EST), and the IMU would sit at that long member's **mid-span**, its least stiff point |
| stiffness | the braced back face: two rails, posts and front/back gussets. Stiffest place available | a long new member at mid-span |
| axes | board **vertical**: X_s lateral (+X world, toward the battery end), **Y_s up**, **Z_s → the front face**. The body frame needs a **fixed 90° sensor-to-body rotation** in the MTi config (Xsens alignment rotation, "RotSensor"). The **pitch-offset recal (T1 memo C2)** then measures only the small mounting residual. Redo it after install | board flat, no axis remap. The best *pure* datum if a stiff short member can be found |

**Attitude-quality reasoning for (a):**
- **Low:** board centre at z ~73, about the unit's CG height (EST ~70).
- **Laterally central:** frame x 222.
- **Stiff:** on the braced face.
- **Clear of heat:** out of the Orin's airflow. Its fan grille is an intake on the case *top*, and its side vents
  exhaust toward the end faces, not backward.
- **Clear of the battery:** ~170 mm from it (right end, x ≥ 392). The battery and its current loops are the
  magnetometer's worst neighbour.

**Magnetometer:**
- The mount keeps all fasteners within ~60 mm aluminium or non-magnetic except the 4 steel M5 + T-nuts. Use A2
  stainless M5 if available.
- After installing, run Xsens **MFM (magnetic field mapping)** in the cage, or run heading from GNSS.

**The saddle** is the fallback where only one member is reachable: 2 × M5, skirts on both side faces, the same stop and
keying.

## Material, print, hardware, mass
- **PA12-CF for flight** (the datum holds preload hot, R6.1), dried. ASA acceptable. PLA for fit-check only.
- **Mount:** top face **down**; the tongues, skirt(s) and ribs rise; no supports.
- **MAXSPAN = 10.4:** the counterbore annulus is the widest roof; the engraving is ≤ 2.5 mm.
- **Wall at the M5 counterbores:** the bridge plate is **flush with the members' outer faces**, so it never overhangs
  the frame bottom. That leaves 4.8 mm to the edge (asserted ≥ 4).
- **Stop:** top down. **Hood:** rear face down (export `rotate([0,90,0])`), tunnel vertical.
- **Walls ≥ 4 mm wherever a fastener passes:** plate 6.4 (16 lines).

| part | CAD cm³ | PA12-CF g | PLA g | print bbox |
|---|---|---|---|---|
| `stl/mti_bridge_mount.stl` (SPAN 125.5) | 81.2 | 73 | 86 | 108 × 146 × 13 |
| `stl/mti_saddle_mount.stl` | 50.0 | 45 | 53 | 108 × 69 × 13 |
| `stl/mti_stop.stl` | 2.3 | 2 | 2 | 17 × 20 × 10 |
| `stl/mti_usb_hood.stl` | 7.4 | 7 | 8 | 22 × 33 × 22 |

**Assembled bridge ≈ 80 g + the board (~25 g) + hardware ~25 g.**

**Hardware:**
- 4 × M5 × 12 BHCS + 4 × 14122 T-nuts for the mount;
- 1 × M5 × 12 + 1 × 14122 for the stop;
- 3 × M3 × 12 M-F aluminium hex standoffs;
- 3 × M3 × 6 screws (brass or aluminium preferred);
- 5 × M3 heat-set inserts (4.4 bore, 5 deep: 3 for the standoffs, 2 for the hood) + 2 × M3 × 8 for the hood;
- 1 × 2.5 mm zip tie;
- Loctite 243.

**Renders (`renders/`):** `mti_bridge_iso`, `mti_saddle_iso`, `mti_bridge_exploded`, `mti_bridge_flat_span80_iso`
(placement b), `mti_on_cage_backface` (placement a).

## PLA fit-check slice (MEAS holes, 2026-09-28; NOT started)
- **Contents:** one plate, **152 × 146**: bridge mount (SPAN 125.5) + stop + hood.
- **Method:** the house way (`<scratchpad>/slice_mti/slice_house_mti.sh`): OrcaSlicer CLI + machine profile +
  `cw_mes/qidi_xplus4_brim.json` + stock Bambu PLA.
- **Preamble:** the printer PRINT_START macro is kept. sed-patched from the CLI's `BED=35 HOTEND=200` to
  **`PRINT_START BED=60 HOTEND=220`**, `M140 S60`, `M104 S220`. Grep-verified.
- **Guards:** bottom shells 4, `max_bridge_length` 15 (MAXSPAN 10.4 + 5), brim 6. `gcode_check.py` passes.
- **Result: 7 h 01 m, 24.9 m / 59.9 cm³ PLA (~74 g).**
- **Gcode:** `<scratchpad>/slice_mti/mti_bridge_span125_MEAS_PLA.gcode`.
- **Superseded:** the earlier Uno-pattern slice was renamed `STALE_mti_bridge_span125_fitcheck_PLA.gcode`.

## CONFIRM
1. **Hole pattern:** calipered 2026-09-28 (done). Still open: hole Ø (3.2 EST) and the hole-to-edge offsets (UR to
   the right edge ~3.5, to the top edge ~2.8), which place the board outline and USB-C against the pattern.
2. **Header tail length** under the board (~10.5 EST). It sets the saddle's clearance; on the bridge the tails are over
   the open window.
3. **USB-C position** (Uno y 41-49 on the high-x edge) and the overmold size (12.4 × 6.4 EST) for the hood tunnel.
4. **Board outline** (58.1 × 53.3). The axes are settled: X right, Y up with USB-C at the bottom-left.
5. **SPAN 125.5** (deck → mid slot pitch, photo 39) and that the **back of the lower bay is free** at frame x 170-275.
6. **Tongue depth 1.5** against the 20-series slot lip and the 14122 T-nut, so the tongue never lands on the nut.
7. **Which face points to the nose.** This sets the fixed sensor-to-body rotation for placement (a).
