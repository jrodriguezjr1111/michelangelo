# T1 Cage Concepts — interactive concept board

`index.html` — one self-contained file. 3D comparison of the four Canary T1
cage swap concepts — **D Extrusion Frame (80/20 20-series, the DECIDED
structural direction, 2026-09-21)** plus A Cartridge Rack, B Open Book and
C Rod Pods as the printed-shell alternatives it was chosen over — built so
Javi and Andrew can pin the open design decisions before anything is handed to
CAD for hardening. The page opens on D.

**Owner decisions rendered as DECIDED (locked, 2026-09-21):** structure = 80/20
20-series black T-slot frame + printed ASA cartridges/bezels/panels; the UHR204
hub stays in the Core; Core access is a first-class swap (opened often in T0).
The Core removal path on D is shown as a **hardening gate**: as drawn the 80 mm
opening between the set-back top longs does not pass the 81 mm compute board
or the 87 mm hub, so the Core swap animation rises and stops (red BLOCKED tag)
and a red gate strip sits under the stage.

**Audience:** internal (founder + CAD/DFM lead). Not published, not shared.
Any external share — including clips from beauty mode — is the founder's call
and gets logged.

**Disclosure posture:** capability names only in the scene and on label plates
(no vendor part numbers in the scene or on plates; 80/20 part numbers appear
only in the D "BOM strip", labelled class); swap times are TARGETS; scores are judgments;
everything is labelled "massing — not hardened dimensions"; patent pending.

## Run
Open over http (module scripts): `python3 -m http.server 8791` in this folder,
or the `t1-cage-board` entry in canary `.claude/launch.json`. three.js r170 +
OrbitControls + RoomEnvironment load from jsDelivr and fonts from Google Fonts,
so the 3D view needs network; the swap / scorecard / decisions panels work
without it (a fallback notice replaces the stage).

## Interaction map
- Drag orbit, scroll/pinch zoom, double-click or RESET VIEW to refit. Canvas
  focused: arrow keys rotate, `+`/`-` zoom.
- Click a module (or its chip in the Swap tab): highlight, steps, tool count,
  target time, and the out-and-back animation. "Hold out" pauses it withdrawn.
- `1` `2` `3` `4` concept, `E` explode, `F` airflow, `B` beauty, `Esc` exit beauty.
- D swaps: peripherals drop out the TOP between the mullions; the battery slides
  out along X from the end; the Core rises 18 mm and is BLOCKED (the gate);
  louvered inserts lift like a cartridge; the IMU lifts off its dowel.
- Beauty mode: UI hidden, slow turntable, looping swaps — for screen recording.
- Decisions tab (41 items): options + notes persist in `localStorage`
  (`canary.t1cage.decisions.v2`, every access try/catch; a `v1` store is
  migrated by id on first load so nothing already pinned is lost); "Copy
  decisions" produces plain text with `[DECIDED 2026-09-21 owner]` and
  `[HARDENING GATE]` tags (also shown in a textarea if the clipboard is blocked).
  New D-side items: mass ceiling restatement, 20-2020 cavity confirm, Core
  removal path in D, T-key vs mini ball-bearing slide, black vs plain anodize
  for the fit-check frame, rods role, IMU seat material, battery latch+strap,
  insert retention, slot cable channels.
- Deep links: `#c=D&x=60&air=1&sel=traffic&beauty=1`.
- `prefers-reduced-motion`: no turntable, no tweens; a swap jumps to the
  withdrawn state and the button toggles pull / re-seat.

## Real vs placeholder
- **Mirrors CAD:** body/tray/pod sizes, bay layout, carrier layout, rod pair
  (Ø15, 60 c-c, 400 long), yokes, datum, trunk — from `../t1_concepts.scad`
  and `../t1_params.py` (MEAS / PUB / EST provenance lives there). Concept D
  member layout (300 × 180 × 140 frame, set-back top longs, mullion positions,
  bay widths 74/84/62 front and 30/30 rear, battery X-slide, louver inserts,
  rods on yoke plates) mirrors `concept="D"`; the T-key numbers come from
  `../t1_tkey_detail.scad`; the frame mass / gross / BOM / joint spec / load
  recompute come from `../README.md` §0, §5D, §10 and `../REQUIREMENTS.md`
  (R1.2, R1.6, R2.3, R6.4–R6.6, R7.2).
- **D, derived not stated:** the "80 mm opening" in the gate text is
  `2 × TOPY − E` from the SCAD (top longs at ±50, 20 mm members); the 81 / 87
  mm are the compute-board and hub widths as placed in the same file.
- **Added for the board (not in the SCAD):** louvres/grilles in B and C and the
  airflow overlay paths (illustrative, not CFD); the vibration port + external
  seat-rail node; the second IMU board on A's datum; the under-floor datum rib
  in B; translucent bench stands under C (display only, excluded from the
  envelope readout). On D: the 4 M5 tray bolts drawn as plain heads, corner
  brackets as simple L massing, the intake insert keyed into the corner posts
  (the SCAD leaves its keys floating), and the 2-hole bracket count reduced to
  what is visible.
- **Judgment / target, not data:** every scorecard pip and every swap time.
