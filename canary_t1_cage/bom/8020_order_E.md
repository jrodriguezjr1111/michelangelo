# Concept E — "what to buy" delta for the existing 406 × 279 deck (2026-09-25)

The deck (2 × 406 + 3 × 239 of 2020, 4 corner gussets, 2 T-gussets) **already exists**; this sheet is only what is
added for concept E. The D sheet (`8020_order_D.*`) is kept for reference, not superseded in place.
**80/20 delta total: $140.44** before tax/shipping, + the two VERIFY COTS items. No purchase placed.

| # | part | what | qty | unit | line | notes |
|---|---|---|---|---|---|---|
| 1 | `20-2020-Black-FB` | antenna-level POSTS, cut to 100 (E06-E09) — the deck itself is already built from stock | 4 | $3.28 | $13.12 | $0.0328/mm; +4 cut charges; verified 8020.net 2026-09-21 |
| 2 | `CUT` | cut charge per piece | 4 | $3.00 | $12.00 | cut tolerance not on the product page - VERIFY on the order form |
| 3 | `20-4119-Black` | 2-hole inside corner bracket: 2 per post foot (both planes) = 8 | 8 | $7.55 | $60.40 | verified 8020.net; the owner's existing corner gussets look like GENERIC 2020 flat corner plates (3 holes/leg) - 80/20's own are 20-4081 'L' flat plate $11.23 and 20-4080 'T' flat plate $12.05 (60 x 60, 5-hole, 4 mm) - keep his if the bolts are M5 and the plate is >= 3 mm |
| 4 | `12004` | 20 Series reduction T-slot cover, black PP, 2 m length - cable runs in the outer side slots + posts | 1 | $5.40 | $5.40 | verified 8020.net; deck perimeter + centre + posts = 1.93 m -> one length; 80/20 has NO 20-series ECONOMY cover (economy covers exist for 10/25, 15/40, 45 only) |
| 5 | `14122` | M5 slide-in economy T-nut block - 2 trays x 6 + IMU plate 4 + V-plate frame 2 + yokes 4 + post brackets 16 + 10 % = 40 | 40 | $0.37 | $14.80 | verified 8020.net; PRE-LOAD the tray rows before the posts/end caps go on (no 20-series drop-in exists on 8020.net) |
| 6 | `75-3581` | M5 x 8 black BHSCS + 14122 assembly - post brackets 16 + 10 % | 18 | $0.90 | $16.20 | verified 8020.net |
| 7 | `11-5312` | M5 x 12 BHSCS black - tray ears through 7 mm flange + washer (bay L), yokes, IMU plate | 20 | $0.59 | $11.80 | verified 8020.net; bay R tray uses 6 captive knurled M5 x 12 thumbscrews (generic, not 80/20) |
| 8 | `12305` | 20 Series end cap, black - 4 post tops | 6 | $1.12 | $6.72 | verified 8020.net; +2 spare |
| 9 | `VERIFY: V-mount plate` | V-mount FEMALE plate with D-Tap out (COTS): SmallRig 3203B class (D-Tap 14.8 V + 8 V/12 V DC, 1/4-20 + rod-clamp threads) or a bare V-lock plate + own D-Tap pigtail | 1 | $0.00 | $0.00 | not an 80/20 item; SmallRig 3203B verified to exist with D-Tap + DC outputs (smallrig.com), price/dims not shown - VERIFY; bare plates (SmallRig 2988, $~40) have no power port |
| 10 | `VERIFY: threaded USB-A bulkhead` | panel-mount IP67 threaded USB-A bulkhead (vib node port) + threaded DC bulkhead | 2 | $0.00 | $0.00 | generic (Bulgin/Amphenol class) - VERIFY |

## Notes
- **Gussets:** the owner's flat corner gussets with 3 screws per leg look like **generic 2020 flat corner plates** (80/20's 20-series flat corner plates are the 5-hole `20-4081` "L" and `20-4080` "T", 60 × 60 × 4 mm, $11–12 each, clear anodize; black versions `-Black` exist). Keep the generic ones for the prototype if the plate is ≥ 3 mm and the bolts are M5 into steel T-nuts; replace with `20-4081-Black` ×4 + `20-4080-Black` ×2 (~$70) for the flight article if the generic ones are < 3 mm or use M4.
- **Slot covers:** `12004` is the only 20-series cover on 8020.net (reduction type, 6.25 wide, 5 mm deep channel — takes two Ø2.5 USB leads or one RG174 coax per slot). One 2 m length does the deck; order 2 if the posts are covered too.
- **T-nuts:** no 20-series drop-in on 8020.net → pre-load `14122` in every tray bolt row **before** the posts and end caps close the slots; the trays then come off and on without touching a frame joint.
- **V-mount plate:** the owner's "modified V-mount insert" = a female V-lock plate bolted to bay L's tray with a D-Tap pigtail to the PDB. SmallRig 3203B-class plates carry D-Tap + regulated DC outs on the plate (verified on smallrig.com; dims/price not displayed — VERIFY); a bare 2988 plate is cheaper but has no power port, so the D-Tap then comes from the battery itself (V99 Pro has D-Tap) — either works; the PDB is the same.
- **Not needed for E:** mullions, cartridges, T-key rack hardware, louvered inserts (all D).
