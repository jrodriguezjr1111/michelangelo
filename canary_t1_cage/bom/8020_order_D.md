# Canary T1 cage — Concept D, 80/20 order list (orderable, 8020.net)

Prices and part numbers read on **8020.net on 2026-09-21** (browser, product pages);
`8020_order_D.csv` is the same list one row per line item. **No purchase was placed —
Javi orders.** Frame layout = the FIXED layout of 2026-09-21 (see "what changed").

## Totals

| Build | Extrusion | Cuts | Brackets | Hardware + caps | **Total** |
|---|---|---|---|---|---|
| **Black anodized (decided)** — `20-2020-Black-FB` + `20-4119-Black` | $63.63 | $42.00 | $181.20 | $82.12 | **$368.95** |
| Plain clear (fit-check frame) — `20-2020` + `20-4119` | $25.41 | $42.00 | $123.60 | $82.12 | **$272.73** |
| Black-vs-plain delta | +$38.22 | — | +$57.60 | — | **+$95.82** |

Before tax and shipping. Black profile and black brackets carry 8020.net's
**"Products Requiring Additional Anodizing" longer lead time** (the plain
`20-2020` / `20-4119` pages say "shorter lead time"). 14 members, 1.94 m of profile (M03/M04 shortened to 130 on 2026-09-22 — see the cut table).

## Line items

| # | Part | Description | mm/pc | Qty | Unit | Line | Notes |
|---|---|---|---|---|---|---|---|
| 1 | `20-2020-Black-FB` | 20×20 T-slot, 4 open slots, full-black anodized, cut to **300** — M01, M02 | 300 | 2 | $9.84 | $19.68 | $0.0328/mm |
| 2 | `20-2020-Black-FB` | same, cut to **140** — M09, M10 (top end ties) | 140 | 2 | $4.59 | $9.18 | |
| 2b | `20-2020-Black-FB` | same, cut to **130** — M03, M04 (bottom end members): 5 mm short of each long so the Core / battery tray side walls pass through to the inner-slot track; the corner brackets span the gap | 130 | 2 | $4.26 | $8.53 | changed from 140 on 2026-09-22 |
| 3 | `20-2020-Black-FB` | same, cut to **100** — M05–M08 (corner posts), M11–M14 (mullions) | 100 | 8 | $3.28 | $26.24 | |
| 4 | cut charge | "*cut charge of $3.00" per piece, 14 pieces | — | 14 | $3.00 | $42.00 | **cut tolerance not printed on the product page — VERIFY on the order form** (80/20 commonly quotes a ±0.4 mm class); cut faces are bare aluminium |
| 5 | `20-4119-Black` | 20 Series 2-hole inside corner bracket, black, 6063-T6 | — | 24 | $7.55 | $181.20 | 4 bottom corners + 8 post feet (both planes) + 4 post-to-tie + 8 mullion feet (both sides); custom qty allowed |
| 6 | `75-3581` | Bolt assembly: M5×8 black BHSCS `11-5308` + M5 slide-in economy T-nut block `14122` | — | 53 | $0.90 | $47.70 | 2 per bracket = 48 + 10 % |
| 7 | `14122` | M5 slide-in economy T-nut block, 20 Series, steel, 9×9×3 | — | 30 | $0.37 | $11.10 | 20 needed (8 yoke plates, 5 cartridges, 2 Core, 1 battery, 2 louver, 2 IMU) + 10 % + **8 pre-loaded in the slots** before the end caps go on — see T-nut note |
| 8 | `11-5312` | M5×12 BHSCS, black zinc, full thread | — | 12 | $0.59 | $7.08 | cartridge / Core / battery / louver retention: 6 mm printed lug + 1 mm washer → 5 mm into the 3 mm nut. **Fallback only** — captive knurled thumbscrews are not an 80/20 item (buy generic M5×12 knurled + e-clip) |
| 9 | `11-5310` | M5×10 BHSCS, black zinc | — | 9 | $0.56 | $5.04 | 8 for the two 5 mm Al rod-yoke plates + 1 spare |
| 10 | `12305` | 20 Series 20×20 end cap, black ABS, push-in stem | — | 10 | $1.12 | $11.20 | 4 bottom-long ends + 4 mullion tops + 2 spare; every other member end abuts another member |
| | | | | | | **$368.95** | |

**Not ordered, by decision:**
- **Anchor / end fasteners** (`13184` 20-series M4 anchor assembly $4.57; `20-3681` end-fastener clip $1.32 + `20-3895` M5 end fastener $1.89): both need 80/20 machining (counterbore / end-tap + access hole) or our own drilling of every joint, and they cannot be repositioned if Andrew moves a member. **Brackets chosen**: no machining, black, reusable, and the CAD team can still slide a mullion.
- **Drop-in T-nuts**: 8020.net lists M5 standard drop-ins for 15/40 (`13116`), 30 (`13115`), 45 (`13127`) and 10/25 series M4 (`14164`) — **no 20-series drop-in was found**. Post-assembly additions therefore rely on the pre-loaded spare `14122`s (line 7) in each slot that will take a cartridge thumbscrew, yoke plate or louver. If a 20-series drop-in exists in the catalogue, it is VERIFY.
- **Drawer slides**: 80/20's start at 375 mm travel / 100 lb — wrong scale. Cartridges ride the slot itself.
- **Cheaper bracket for the plain fit frame**: `14059` die-cast 2-hole slotted inside corner with dual support, natural finish, **$1.31** (fits 10/20/25 series) — 24 × $1.31 = $31 instead of $124/$181; silver, not black. Fine for the PLA fit-check frame.

## Cut diagram — which member goes where

`../renders/D_extrusion_frame_cut_diagram.png` (labels on the render; M02 and M08 are the rear-face twins of M01 and M06). Frame 300 × 180 × 140, origin at the front-left-bottom corner, X along the rods.

```
                 M09 (top end tie, -X)                     M10 (top end tie, +X)
        z=140  ┌──────────────────────────────────────────────────────────┐
               │ M05 ║                    OPEN TOP                   ║ M06 │   front face (-Y)
   posts       │     ║   Core lifts out here (200 × 140 clear)        ║     │
               │ M07 ║   or slides out the -X end on M01/M02 slots    ║ M08 │   rear face (+Y)
        z=0    └──────────────────────────────────────────────────────────┘
                 M03 (bottom end, -X)                      M04 (bottom end, +X)
                 M01 = front bottom long (300)   M02 = rear bottom long (300)

   FRONT FACE (-Y), looking at it:            REAR FACE (+Y):
   ┌M05┐ TRAFFIC ┌M11┐  LTE  ┌M12┐ RTK ┌M06┐  ┌M07┐ CABIN CO ┌M13┐ SPARE ┌M14┐ EXHAUST louver ┌M08┐
   mullions M11, M12 (100) stand on M01;      mullions M13, M14 (100) stand on M02
   bays 74 / 84 / 62 between 20-wide mullions bays 30 / 30 / 160
```

| Label | Qty | Length | Role | Open ends (cap) |
|---|---|---|---|---|
| M01, M02 | 2 | 300 | bottom longs; **inner slots = the Core/battery track**; belt goes round these | 2 each |
| M03, M04 | 2 | **130** | bottom end members between the longs, 5 mm gap each end (tray walls pass here) | 0 |
| M05–M08 | 4 | 100 | corner posts | 0 |
| M09, M10 | 2 | 140 | top end ties; **rod yoke plates bolt on top** (rear plate carries the IMU datum) | 0 |
| M11, M12 | 2 | 100 | front mullions (cartridge slots) | 1 each (top) |
| M13, M14 | 2 | 100 | rear mullions | 1 each (top) |

Bracket map (24 × `20-4119-Black`): 4 at the M01/M02–M03/M04 corners (inside, bottom plane);
8 at the post feet (one in the X-Z plane, one in the Y-Z plane per post); 4 at the post
tops to M09/M10 (Y-Z plane); 8 at the mullion feet (one each side, X-Z plane).

## What changed for the Core path (owner: Core opened often in T0)

The 17-member draft had two top longs set back 30 mm (±50 mm → 80 mm opening — the
board caught it: Orin 81, hub 87 do not pass) and an IMU cross member. Fixed layout:
**the two 260 mm top longs and the 100 mm IMU cross are deleted** (17 → 14 members,
2.58 → 1.94 m, frame 1.67 → 1.40 kg, gross ~4.25 kg). The top plane is the two
full-width end ties only, so the Core has a **200 × 140 clean lift-out** between them
once the two rod-yoke plates are off, **and** a zero-tool path: the Core tray is an
end-loading cartridge on M01/M02's inner slots from the −X end (its faceted end bezel
is the intake louver), one thumbscrew, pull, unplug — the same track the battery uses
at +X. The IMU datum moved into the **rear aluminium yoke plate** (bolted to M10 with
4 × M5 T-nuts + a dowel into the tie). The set-back longs would also have blocked the
cartridge drop-in (a cartridge deeper than 29 mm hits them) — deleting them fixes both.
Frame envelope stays 300 × 180 × 140. Racking stiffness without top longs: 800 N at
18 g over four post feet = 20 N·m per foot, ~1 kN across the 20 mm couple vs ~1.1 kN
slip per M5 at 4.5 N·m × 4 bolts per foot — MS ≈ 3, plus the tray/faceplates as shear panels.

**End-loading detail found while drawing the mechanism (2026-09-22):** a tray riding the bottom longs' *inner* slots cannot pass a full-length end member — M03/M04 abut the longs exactly where the slot opening is. Hence M03/M04 are cut **130**, leaving a 5 mm gap at each end for the 4 mm tray wall; `20-4119` brackets (18 mm legs) span the gap. The tray floor sits at z 20–23, above M03; only the wall foot and the key are below it. Renders: `../renders/D_mechanism_core_tray.png`.

## Before you click buy

1. **Slot cavity width** — open the `20-2020` CAD (product page → CAD Files) and read the cavity behind the 6.0 slot; the printed T-key head (10.4 wide) assumes 11.0. If it is narrower, the key head shrinks, nothing else changes.
2. **Core opening** — 200 × 140 between M09/M10 and the posts; hub 139 × 87 and the Orin 100 × 81 pass with the yoke plates off. Confirm the hub really is 139 × 87 × 35 (datasheet drawing, unmeasured) before the tray is printed.
3. **Anodize choice** — black adds $96 and the extended anodizing lead time. If the FLEDGE build week is fixed, order the **plain** set now for the fit frame (with `14059` brackets, −$150) and the black set in parallel.
4. **Cut tolerance** — read it on the order form; if 80/20 quotes worse than ±0.5 mm, the 100 mm posts and mullions are the ones that matter (they set the cartridge height); the 140/300 members do not.
5. **Material** — 8020.net lists 20-2020 as **6063-T6, yield 172 MPa**; the distributor sheets say 6105-T5 / 241 MPa. The load checks were re-run mentally at 172: rod/frame margins stay > 1.0 (worst member stress is far below either).
6. `20-4119-Black` at $7.55 is 49 % of the order. If that stings, `20-4119` plain at $5.15 on the hidden joints (post feet, mullion feet) and black only on the 8 visible corners saves ~$38.
7. Thumbscrews: the 11-5312 line is the fallback; the real captive knurled M5×12 thumbscrews are a generic buy (McMaster / Misumi), 11 off.

## Face-plate T-nuts (added 2026-09-22)

The `t1_faceplate/` plates (blanking / vent / fixed panels, R1.5) bolt with M5 × 16 BHCS
into T-nuts in the members' front slots — ~25 nuts for the four D plates. 8020.net has
**no 20-series M5 drop-in T-nut**, so either (a) source a generic 2020 M5 drop-in
(Misumi HNTT5-5 class) separately and confirm its thread height against the plate's
`BOLT_L` assert, or (b) add **+25 `14122` slide-in nuts** to line 6 above and pre-load
them in the face-plate members before brackets and end caps go on. The plate geometry
is the same either way. Decide before ordering; option (b) adds ~$9.25 to the total.
