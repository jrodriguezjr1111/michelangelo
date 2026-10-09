# Concept E rev C (full-height cage): what to buy on top of the rev B order (2026-09-25)

This sheet lists only what rev C **adds** to `8020_order_E.md` (rev B, $140.44), with one substitution: the four
posts are cut to **222 instead of 100** (line 1 below is the extra length only). The rev B sheet and the D sheets
stay as they are. **80/20 delta for rev C: $220.74**, so rev B + rev C comes to **$361.18** before tax and shipping.
Prices are the verified 8020.net figures already used on the rev B sheet: 20-2020-Black-FB $0.0328/mm plus $3.00 per
cut, 20-4119-Black $7.55, 14122 $0.37, 75-3581 $0.90, 12305 $1.12, 12004 $5.40, and 20-4081 $11.23 as the
flat-plate class price. **No purchase has been placed.** Machine-readable copy: `8020_order_E_revC.csv`.

| # | part | what | qty | unit | line | notes |
|---|---|---|---|---|---|---|
| 1 | `20-2020-Black-FB` | cage **posts at 222** instead of 100 (E06-E09): +122 mm each. **Replaces rev B line 1**: order 4 × 222 | 4 | $4.00 | $16.00 | 222 is the shortest post that keeps the dome top 15 mm under the rail top. **Don't cut until the dome is measured**, because the post grows 1:1 with dome height |
| 2 | `20-2020-Black-FB` | **top long rails** E10-E11, 406, sitting on the posts | 2 | $13.32 | $26.64 | |
| 3 | `20-2020-Black-FB` | **top end rails** E12-E13, 239, between the top longs | 2 | $7.84 | $15.68 | |
| 4 | `CUT` | cut charge, 4 top rails (the post cut count is unchanged from rev B) | 4 | $3.00 | $12.00 | check the cut tolerance on the order form |
| 5 | `20-4119-Black` | inside corner bracket, 2 per post **top** (post to top long rail, post to top end rail) | 8 | $7.55 | $60.40 | same part as the post feet |
| 6 | `20-4081` | flat "L" corner plate 60 × 60 × 4, 5-hole, one per top corner | 4 | $11.23 | $44.92 | clear-anodize figure; `-Black` exists but its price needs checking. The owner's generic plates are fine if they are at least 3 mm thick and M5 |
| 7 | `75-3581` | M5 × 8 BHSCS + T-nut: bracket screws 16 + gusset screws 20 = 36, plus 10 % | 40 | $0.90 | $36.00 | |
| 8 | `14122` | spare T-nuts pre-loaded in the top rails for a future lid/radome frame and a carry strap | 10 | $0.37 | $3.70 | the yoke bridges' 4 T-nuts are already in rev B's 40; they now go in the **posts' inner slots** |
| 9 | `12004` | second 2 m slot-cover length for the taller posts (coax up both rear posts) | 1 | $5.40 | $5.40 | |
| 10 | `12305` | end caps: the 4 rev B post-top caps move to the 4 open ends of the top long rails | 0 | $1.12 | $0.00 | net 0 |
| 11 | `VERIFY: stubby 1090 / 978` | SMA stubby antennas, 40 mm or shorter, replacing the 100 mm whips | 2 | n/a | $0.00 | generic, needs pricing. Alternative: keep the straight 100 mm whips on the yoke bridge (tip at z ~241, 24 mm under the rail top), but the tip then sits about 12 mm from an aluminium rail |
| | **total** | 80/20 items, rev C **additional** | | | **$220.74** | rev B + C = **$361.18** |

## Notes
- **Cut list, rev C:** 4 × 222 (posts), 2 × 406 and 2 × 239 (top rectangle), 4 cuts on the top rails. That is 1.78 m
  more 20-2020 than rev B, or +784 g of extrusion. With the brackets, gussets and fasteners the frame gains **+1.26 kg**
  (see `envelope_check.py` §[4E-C]).
- **Order of assembly (T-nuts):** no 20-series drop-in T-nut exists, so load the slots first. Put the yoke-bridge T-nuts
  in the posts' inner slots, and the 10 spares in the top rails, **before** the top rectangle goes on.
- **Printed-part changes (not on this sheet):** the yoke bridges shorten from 279 to **239** (between the posts, ASA,
  fits the bed with margin). The dome puck mount is unchanged from rev B and still has to be designed. The CO tray
  tube plate is the existing `co_sensor` rev C part, now hung under the rods.
- **Not needed:** side rails. If the owner wants them anyway, they are 2 × 406 of 20-2020-Black-FB ($26.64 + $6.00 cuts),
  4 × 20-4119 ($30.20) and 8 × 75-3581 ($7.20), about $70 and +0.45 kg. See the LAYOUT_E rev C section for why they are not
  recommended.
