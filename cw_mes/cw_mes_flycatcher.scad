/* ======================================================================
   CW-MES instance — NOOELEC FLYCATCHER box (ADS-B / UAT SDR)
   Same modular 6-panel bolted design as the Jetson Nano box; only the
   parameters differ. Geometry comes from cw_mes_lib.scad.
   ----------------------------------------------------------------------
   The FlyCatcher is TWO radios (ADS-B + UAT), each with its own SMA RF
   input (board's far/back edge) and micro-USB (near/front edge). We route
   each radio's pair out ITS OWN side wall via CW-Link cable glands:
       LEFT  wall = ADS-B chain  (1 SMA gland + 1 USB gland)
       RIGHT wall = UAT  chain  (1 SMA gland + 1 USB gland)   -> 4 total
   Board sits on bottom-plate riser bosses (heat-set inserts).

   ⚠ DIMENSIONS BELOW ARE PHOTO ESTIMATES — confirm with calipers:
     FC board size, mount-hole pattern, gland heights, insert size.
   The CW-Link gland is M18 (Ø18.4 bore); it is generous for this board.
   Shrinking GLAND_D shrinks the whole box (gland nut sets the X clearance).
   ====================================================================== */

view = "assembled";   // assembled | plate | bottom top front back left right | fittest

/* ---------- board + gland (CONFIRM) ---------- */
FC      = [73, 54, 1.6];   // ADS-B↔UAT × USB↔SMA × thickness  (USB↔SMA = 54 → inner.y 66)
GLAND_D = 12.0;            // Ø12 bore for a single-cable CLAMSHELL gland (was 18.4 M18)
gx      = 15.5;            // wall↔board gap for the gland body

/* ---------- 1 · Core dimensions ---------- */
inner = [FC[0] + 2*gx, FC[1] + 12, 51];   // [104, 66, 51]; -8mm height (top card guide at 48 → ~3mm headroom)
t     = 3.0;
rim   = 2.5;
clr   = 0.10;                       // PLA / Bambu PLA — coupon-verified
fit_tests = [0.10, 0.15, 0.20];

/* ---------- 2 · Fastener system (M3, DIN 562 square nuts) ---------- */
bolt_d  = 3.4;
bolt_l  = 12;
nut_w   = 5.8;
nut_t   = 2.1;
cbore_d = 6.4;
cbore_h = 0;

/* ---------- 3 · Joint pattern ---------- */
nx = 3;
ny = 3;
nz = 2;

/* ---------- 4 · Board mounting — FULL RACK (no bottom bosses) ---------- */
// Bosses removed: the FlyCatcher (and other components) mount on slide-in/drop-in
// plates instead. The freed floor lets shelves pack lower.
mount_holes = [];
boss_d   = 8;
boss_h   = 14;
insert_d = 4.0;
insert_h = 5;

// GNSS-saddle mount: M4 36.14 x 36.1 pattern, centered on the bottom plate
saddle_d     = 4.4;   // M4 clearance
sad_cx = inner[0]/2;  sad_cy = inner[1]/2;
saddle_holes = [[sad_cx - 36.14/2, sad_cy - 36.1/2], [sad_cx + 36.14/2, sad_cy - 36.1/2],
                [sad_cx - 36.14/2, sad_cy + 36.1/2], [sad_cx + 36.14/2, sad_cy + 36.1/2]];

/* ---------- 5 · Vents & cutouts ---------- */
vent_top   = [22, 16, 60, 34];
vent_pitch = 7;
vent_slot  = 3;
cut_front  = [];   // USB edge faces the gland walls, not this one
cut_back   = [];   // SMA edge likewise
cut_left   = [];
cut_right  = [];

/* ---------- 6 · Cable-gland bores  [along-wall y, height z, Ø] ---------- */
gz     = 15;       // gland centerline lowered so the cage shelves clear it above
gy_usb = 18;       // toward the USB (front) edge — fits the 66 mm wall
gy_sma = 48;       // toward the SMA (back) edge
cut_left_round  = [[gy_usb, gz, GLAND_D], [gy_sma, gz, GLAND_D]];   // ADS-B chain
cut_right_round = [[gy_usb, gz, GLAND_D], [gy_sma, gz, GLAND_D]];   // UAT chain

/* ---------- 7 · Card-cage rack — slide-in plates on L/R wall guides ---------- */
// Guides on the FRONT/BACK (XZ-plane) walls: plates slide in along X (remove a
// left/right panel). Shelves sit above the gland row (z 9..21); two levels fit.
card_plate_t   = 2.0;
// 5 shelf levels running along the LONG (front/back) walls. z=24 is the lowest
// that clears the gland band (z 9..21); 48 stays under the z 51..59 top joint.
card_guides_fb = [24, 30, 36, 42, 48];   // long (front/back) walls — 5 levels
card_guides    = [24, 30, 36, 42, 48];   // short (left/right) walls -> 4-sided
rail_frac_lr   = 0.75;                    // green (L/R) rails span 75% (centered), clears corners
rail_chamfer_lr = 0;                      // green (L/R) rails square (no taper); orange keep the funnel

// FlyCatcher mount plate (view="cardboss"): 4x M3 standoffs, 10 mm, 58 x 49 centered
plate_bosses    = [[-29, -24.5], [29, -24.5], [-29, 24.5], [29, 24.5]];
plate_boss_h    = 10;
plate_boss_d    = 7;     // standoff OD around the Ø3.4 bore
plate_boss_bore = 3.4;   // M3 clearance

include <cw_mes_lib.scad>
