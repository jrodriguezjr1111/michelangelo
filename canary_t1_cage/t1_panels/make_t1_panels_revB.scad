// ============================================================================
// CANARY T1 CAGE — LOWER (CO) PANEL rev B                  (t1_panels family)
// 2026-09-28 · owner, verbatim: "let's redesign the CO panel as one panel with
// the same vented pattern. let's remove the canary icon and make both sides
// symmetrical. also, the dimensions of this panel should be 12 inches by 5.75
// inches to accommodate the gussets."
//
// NEW FILE (rev switch by file): rev A (make_t1_panels.scad, upper + lower) is
// untouched; this file `use`s its helpers (hex fill, strokes, V-grooves, accent
// fit, CO-tray reference) so the house geometry is not forked.
//
//   panel = "lower" (CO, rev B 2026-09-28) | "upper" (badge, rev B 2026-09-29)
//   placement (upper only) = "lowerbay" (front of the lower bay, over the case I/O) | "upperbay" (brow, mid -> top rail)
//   part = "half" | "half_mirror" | "cassette" | "accents" | "splice" (lower) ; "u_half" | "u_badge" | "u_accents" | "u_splice" (upper)
//   view = "none" | "front" | "back" | "exploded"                        (renders)
//
// 2026-09-29: frame numbers re-measured on photo 39 (straight-on; 20 mm gusset bolt pitch
// + 20 mm rail faces as rulers, keystone-corrected): deck->mid slot pitch 125.5, mid->top 86,
// long face ~442 (17.5 in = 444.5 taken), gussets L 62 x 60 / T 62 x +/-30.  All CONFIRM.
//
// Layout, strictly mirror-symmetric about the vertical centreline:
//   chevron | hex field | CO louver cassette (seam on its centreline) | hex field | chevron
// The panel sits FLAT on the rail faces BETWEEN the front-face corner gussets (no
// standoff).  Any overlap with a gusset outline is notched out (+1.5): on a 406 face
// the ends become arrowheads; on the measured ~444.5 face a 12 in panel clears the
// 62 mm gusset legs by 6.4 mm and only its 6 mm design corner chamfers remain.
// Two IDENTICAL MIRRORED HALVES (304.8 > 281 bed), joined on the centreline:
// loose printed spline in grooves in both halves + two rear splice bars on 4 x M3
// heat-set inserts; the cassette's single thumbscrew threads into an M4 insert in
// the TOP splice bar, so the cassette load crosses the seam through metal-backed
// print, never through the seam; two mirrored hooks (one per half) carry its weight.
// ============================================================================
use <make_t1_panels.scad>
panel = "lower";
placement = "lowerbay";
// 2026-09-28 owner decision: BOTH panels on the FRONT face — lower bay = this CO panel (vented, no brand), upper bay = badge brow
cassette = false;          // lower: false = plain louver insert over the rail-mounted CO node (default) | true = removable tray cassette
fix = "8ts";               // lower: "8ts" = 8 captive thumbscrews | "4ts_hooks" = 4 on the mid-rail row + 2 T-slot hooks in the deck rail
NODE_X = -5;               // EST photo 39: printed CO node centre 5 +/- 3 mm LEFT of the frame centreline (slides on its rod clamp)
NODE_SETBACK = 50;         // EST photo 39: node front ~50 behind the rail plane (at the case-face depth) — design minimum 10, CONFIRM
COMB = [1.6, 7.6, 8, 0.8];                 // tooth width, pitch, length, retaining hook
TS_SEAT = [11.6, 1.0];                     // captive thumbscrew head seat (knurled M5, head O11, O-ring behind = captive)
// SHARED MID RAIL (front pair): each panel owns half the mid-rail face (edge on the slot centreline) and reaches over
// with castellated bolt ears — the t1_faceplate rule (EAR_OV 18.5, notch = ear + 1 clearance per side).
EAR_W = 16; EAR_OV = 18.5; EAR_CLR = 1;
EAR_X_LO = [24, 66];          // lower panel's mid-row ears (its thumbscrew x), mirrored
EAR_X_UP = [45, 110];         // upper brow's mid-row ears (its bottom bolt x), mirrored
part = "half";
view = "none";
taglines = false;     // NOT APPROVED (R8) — no tagline is drawn on rev B either way
explode = 0;
$fn = 40;

// ---------------------------------------------------------------- frame — CONFIRM (same parameters as rev A)
FACE_L = 444.5;           // EST photo 39: 437 / 447 / 443 at top / mid / deck -> ~442 +/- 5; 17.5 in taken  (E model deck: 406 — CONFIRM)
DECK_SLOT_Z = 10;          // 20-2020 slot centreline
MID_SLOT_Z = 135.5;        // EST photo 39: deck->mid slot pitch 125.6 (L) / 125.3 (R) -> 125.5   (photo 38 had suggested ~110: foreshortened)
TOP_SLOT_Z = 221.5;        // EST photo 39: mid->top pitch 86.4 (L) / 84.9 (R) -> 86
W = 304.8;          // owner 12 in
H = 146.05;         // owner 5.75 in: flush over both rails only if the slot pitch is H - 20 = 126.05
X0 = (FACE_L - W) / 2;                     // 50.6 from each frame corner
NOTCH = [W / 2 - 76, 30];                  // I/O-face cable notch: from x 76 to W-76, 30 high (deck rail 0..20 + 10), clear of the louver bezel (z 30.75)
HOOK_TS = [[45, 20], [W - 45, 20]];        // 4ts_hooks: T-slot hooks in the deck-rail slot, x centre + width
ZC = (DECK_SLOT_Z + MID_SLOT_Z) / 2;       // module centre = centre of the bay opening between the rails
GUS_RL = 62; GUS_PL = 60; GUS_TH = 30; GUS_CLR = 1.5;   // EST photo 39: rail leg 62, L post leg 60, T +/-30 about the mid slot

// ---------------------------------------------------------------- body (house numbers, as rev A)
T = 5.6; M5B = 5.4; CB_D = 10.4; CB_H = 3.2;
M3B = 3.4; INS3_D = 4.4; INS3_DEP = 4.0; M4B = 4.4; INS4_D = 5.6; INS4_DEP = 6.0;
ACC_D = 1.6;
SPL = [1.6, 2.0];               // loose spline thickness, depth into EACH half (groove +0.2)
SPL_Z = 2.0;                    // face skin above the spline groove
HOLE_X = [24, 66];              // panel x (mirrored): outboard of the cable notch; 2 per half per row
HX = concat(HOLE_X, [for (x = HOLE_X) W - x]);
HY = fix == "8ts" ? [DECK_SLOT_Z, MID_SLOT_Z] : [MID_SLOT_Z];     // thumbscrew rows (4ts_hooks: the deck row is the hooks)

// ---------------------------------------------------------------- CO cassette rev B (same co_sensor tray, same box)
CO_TRAY = [125.6, 26.22, 25.62];  CO_TAIL = [12, 16];  CO_EAR = [[45, 17.11], [95, 17.11]];  EAR_T = 3;
CAS_IN  = [CO_TRAY[0] + CO_TAIL[0] + 2, 44];  CAS_W = 2.0;
CAS_OUT = [CAS_IN[0] + 2 * CAS_W, CAS_IN[1] + 2 * CAS_W];     // 143.6 x 48
BZ = 3.2; CAS_BEZ = [159.6, 84]; CAS_DEPTH = 1.5 + CO_TRAY[2];
HOOK = 2.6; HOOK_X = 55; HOOK_W = 16;       // two hooks, mirrored, one per half
WIN_B = ZC - CAS_OUT[1] / 2 - 0.5;          // window bottom: box rests 0.5 above it, hooks 2.1 behind it
WIN_T = WIN_B + CAS_OUT[1] + HOOK + 0.9;    // window top: room to lift the box HOOK+0.4 on insertion
WIN_W = CAS_OUT[0] + 2;
TS_Z = ZC + 34;                              // the one thumbscrew: top centre of the bezel
LOUV = [116, 4.0, 7.2, 5];
SPLICE_BOT = [WIN_B - 2 - (NOTCH[1] + 2), NOTCH[1] + 2];           // [height, z0] between the cable notch and the window
SPLICE_TOP = [(MID_SLOT_Z - 12) - (WIN_T + 2), WIN_T + 2];
SPLICE_HW = 28;                              // splice bar half-width
INS_X = 12;                                  // M3 inserts at +/- this from the seam

// ---------------------------------------------------------------- 2D artwork (viewer frame: x right, y up = frame z)
// front-face gusset outlines in FRAME coords (x from the frame corner, z up) — measured on photo 39, CONFIRM
TT = TOP_SLOT_Z + 10;
function gus_L2d() = [[0, 0], [GUS_RL, 0], [GUS_RL, 20], [22, GUS_PL], [0, GUS_PL]];                              // deck-rail L
function gus_T2d() = [[0, MID_SLOT_Z - GUS_TH], [20, MID_SLOT_Z - GUS_TH], [GUS_RL, MID_SLOT_Z - 10],
                      [GUS_RL, MID_SLOT_Z + 10], [20, MID_SLOT_Z + GUS_TH], [0, MID_SLOT_Z + GUS_TH]];               // mid-rail T
function gus_Ltop2d() = [[0, TT], [GUS_RL, TT], [GUS_RL, TT - 20], [22, TT - GUS_PL], [0, TT - GUS_PL]];           // top-rail L
module gussets2d() { polygon(gus_L2d()); polygon(gus_T2d()); polygon(gus_Ltop2d()); }
module notches2d(zb = 0) for (m = [0, 1]) translate([m * W, -zb]) mirror([m, 0]) translate([-X0, 0]) offset(delta = GUS_CLR) gussets2d();
module outline2d(h = H, zb = 0) difference() {
  polygon([[6, 0], [W - 6, 0], [W, 6], [W, h - 6], [W - 6, h], [6, h], [0, h - 6], [0, 6]]);   // 6 mm design corner chamfers
  notches2d(zb);
}
END_CLR = X0 - GUS_RL;       // panel end to the gusset rail legs (negative = the notches do the work)
module chevron2d() stroke([[15, ZC + 24], [7, ZC + 16], [7, ZC - 16], [15, ZC - 24]], 5);
FIELD = [[20, DECK_SLOT_Z + 16], [W / 2 - CAS_BEZ[0] / 2 - 6, DECK_SLOT_Z + 16],
         [W / 2 - CAS_BEZ[0] / 2 - 6, MID_SLOT_Z - 16], [20, MID_SLOT_Z - 16]];
function mxw(p) = [for (q = p) [W - q[0], q[1]]];
cells = hex_cells(FIELD);                    // left field; the right field is its mirror (identical cell count)

// ---------------------------------------------------------------- the full body (both halves), then the half
module body_full() difference() {
  union() {                                  // 45 deg bed-edge chamfer as 3 x 0.4 steps (the outline is concave)
    translate([0, 0, -T]) linear_extrude(T - 1.2) l_outline2d();
    for (i = [0 : 2]) translate([0, 0, -1.2 + 0.4 * i]) linear_extrude(0.4 + 0.01) offset(delta = -0.4 * (i + 1)) l_outline2d();
    if (fix == "4ts_hooks") for (h = HOOK_TS) translate([h[0] - h[1] / 2, 0, 0]) ts_hook(h[1]);   // T-slot hooks on the back
  }
  for (x = HX, y = HY) translate([x, y, 0]) {                                                  // captive M5 thumbscrews
    translate([0, 0, -T - 1]) cylinder(d = M5B, h = T + 2);
    translate([0, 0, -TS_SEAT[1]]) cylinder(d = TS_SEAT[0], h = TS_SEAT[1] + 1);
  }
  for (c = concat(cells, mxw(cells))) translate([c[0], c[1], -T - 1]) rotate([0, 0, 30]) cylinder(r = 5 / sqrt(3), h = T + 2, $fn = 6);
  translate([0, 0, -ACC_D]) linear_extrude(ACC_D + 0.05) { chevron2d(); translate([W, 0]) mirror([1, 0]) chevron2d(); }
  translate([W / 2 - WIN_W / 2, WIN_B, -T - 1]) cube([WIN_W, WIN_T - WIN_B, T + 2]);             // cassette window
  translate([W / 2, TS_Z, -T - 1]) cylinder(d = M4B, h = T + 2);                                 // thumbscrew passes the seam
  // design lines: the seam's visible runs (above / below the bezel) sit in 45 deg V-grooves on the centreline
  vgroove([[W / 2, NOTCH[1]], [W / 2, ZC - CAS_BEZ[1] / 2 + 0.5]]);  vgroove([[W / 2, ZC + CAS_BEZ[1] / 2 - 0.5], [W / 2, H + 1]]);
  vgroove([[24, MID_SLOT_Z - 10], [W - 24, MID_SLOT_Z - 10]], 0.8);                                  // rail-band edges
  for (m = [0, 1]) translate([m * W, 0, 0]) mirror([m, 0, 0]) vgroove([[24, DECK_SLOT_Z + 10], [NOTCH[0] - 4, DECK_SLOT_Z + 10]], 0.8);
  // splice inserts (from the back) + spline grooves on the centreline (both halves: the spline is loose)
  for (sx = [-1, 1], p = [[SPLICE_BOT[1] + SPLICE_BOT[0] / 2], [SPLICE_TOP[1] + SPLICE_TOP[0] / 2]])
    translate([W / 2 + sx * INS_X, p[0], -T - 0.01]) cylinder(d = INS3_D, h = INS3_DEP);
  for (r = [[NOTCH[1], WIN_B - 1], [WIN_T + 1, H + 1]]) translate([W / 2 - SPL[1] - 0.2, r[0], -SPL_Z - SPL[0] - 0.1]) cube([2 * (SPL[1] + 0.2), r[1] - r[0], SPL[0] + 0.2]);
}
module half() intersection() { body_full(); translate([-1, -1, -20]) cube([W / 2 + 1, H + 2, 40]); }   // LEFT half; right = mirror

// ---------------------------------------------------------------- splice bars + splines (print flat)
module splice_bar(which) {
  s = which == "top" ? SPLICE_TOP : SPLICE_BOT;
  difference() {
    union() {
      translate([W / 2 - SPLICE_HW, s[1], -T - 3.2]) cube([2 * SPLICE_HW, s[0], 3.2]);
      if (which == "top") translate([W / 2, TS_Z, -T - 3.2 - 4]) cylinder(d = 11, h = 4.01);      // M4 thumbscrew boss
    }
    for (sx = [-1, 1]) translate([W / 2 + sx * INS_X, s[1] + s[0] / 2, -T - 10]) cylinder(d = M3B, h = 11);
    if (which == "top") translate([W / 2, TS_Z, -T - 3.2 - 4 - 0.01]) cylinder(d = INS4_D, h = INS4_DEP);
  }
}
module splines() for (r = [[NOTCH[1] + 0.5, WIN_B - 1.5], [WIN_T + 1.5, H - 0.5]])
  translate([W / 2 - SPL[1], r[0], -SPL_Z - SPL[0]]) cube([2 * SPL[1], r[1] - r[0], SPL[0]]);

// ---------------------------------------------------------------- CO cassette rev B (one piece, spans the seam)
module cassette() difference() {
  union() {
    hull() { linear_extrude(BZ - 1.2) oct2d(CAS_BEZ, 12); translate([0, 0, BZ - 1.2]) linear_extrude(1.2) offset(delta = -1.2) oct2d(CAS_BEZ, 12); }
    translate([0, 0, -CAS_DEPTH]) linear_extrude(CAS_DEPTH + 0.01) difference() { square(CAS_OUT, center = true); square(CAS_IN, center = true); }
    for (s = [-1, 1]) translate([-CAS_IN[0] / 2, s > 0 ? CAS_IN[1] / 2 - 7 : -CAS_IN[1] / 2, -CAS_DEPTH + EAR_T]) cube([CO_TRAY[0], 7, 6]);
    for (sx = [-1, 1]) translate([sx * HOOK_X - HOOK_W / 2, -CAS_OUT[1] / 2 - HOOK, -T - 1.6]) cube([HOOK_W, HOOK + 0.01, 1.6]);   // mirrored hooks
  }
  for (i = [0 : LOUV[3] - 1]) translate([-LOUV[0] / 2 + 2, -(LOUV[3] - 1) * LOUV[2] / 2 + i * LOUV[2] - LOUV[1] / 2, 0])
    hull() { translate([0, 0, -1]) cube([LOUV[0] - 4, LOUV[1], 0.01]); translate([-1.2, -1.2, BZ + 0.01]) cube([LOUV[0] - 1.6, LOUV[1] + 2.4, 0.01]); }
  for (s = [-1, 1]) translate([s * (LOUV[0] / 2 + 9), 0, BZ - ACC_D]) linear_extrude(ACC_D + 0.1) mirror([s > 0 ? 1 : 0, 0]) cas_side2d();
  translate([0, 24, BZ - 0.6]) linear_extrude(1) text("CARBON MONOXIDE SENSOR", size = 4.4, font = "DIN Condensed:style=Bold", halign = "center", valign = "center", spacing = 1.15);
  translate([0, -27, BZ - 0.6]) linear_extrude(1) text("AIR IN · DETECT · STAY SAFE", size = 4.0, font = "DIN Condensed:style=Bold", halign = "center", valign = "center", spacing = 1.1);
  translate([0, 34, -1]) cylinder(d = M4B, h = BZ + 2);                                            // the one thumbscrew, on the centreline
  for (e = CO_EAR, sy = [-1, 1]) translate([-CAS_IN[0] / 2 + 1 + e[0], sy * e[1], -CAS_DEPTH + EAR_T - 0.01]) cylinder(d = INS3_D, h = 4.5);
  translate([CAS_IN[0] / 2 - 1, -CO_TAIL[1] / 2 - 1, -CAS_DEPTH - 1]) cube([CAS_W + 2, CO_TAIL[1] + 2, CAS_DEPTH - T - 2]);
}

// ---------------------------------------------------------------- lower outline with the I/O-face cable notch; T-slot hooks; plain louver
function mirrored(xs) = concat(xs, [for (x = xs) W - x]);
module l_outline2d() difference() {
  union() {
    intersection() { outline2d(); square([W, MID_SLOT_Z]); }                                          // body to the mid slot centreline
    for (x = mirrored(EAR_X_LO)) translate([x - EAR_W / 2, MID_SLOT_Z - 1]) square([EAR_W, (MID_SLOT_Z - 10) + EAR_OV - (MID_SLOT_Z - 1)]);   // ears
  }
  for (x = mirrored(EAR_X_UP)) translate([x - EAR_W / 2 - EAR_CLR, (MID_SLOT_Z + 10) - EAR_OV - EAR_CLR]) square([EAR_W + 2 * EAR_CLR, 30]);  // notches for the brow's ears
  cable_notch2d();
}
// T-slot hook (4ts_hooks): tongue 5.6 x 6 into the deck-rail slot on its centreline, head hooks UP 2.0 behind the upper
// slot lip.  Fit: offer the panel 2.5 mm low, push the tongues in, lift 2.5 -> heads behind the lip; 4 top thumbscrews.
module ts_hook(w) {
  translate([0, DECK_SLOT_Z - 2.8, -T - 6]) cube([w, 5.6, 6.01]);
  hull() { translate([0, DECK_SLOT_Z - 2.8, -T - 6]) cube([w, 5.6 + 2.0, 1.6]); translate([0, DECK_SLOT_Z - 2.8, -T - 4.4]) cube([w, 5.6, 0.01]); }
}
// plain louver (default): the cassette's bezel, louvers, text, side accents and single centreline thumbscrew over a
// 5.6-deep ring the size of the cassette box, with the same two hooks -> same body, same fitting; open behind to the node.
module louver_plain() difference() {
  union() {
    hull() { linear_extrude(BZ - 1.2) oct2d(CAS_BEZ, 12); translate([0, 0, BZ - 1.2]) linear_extrude(1.2) offset(delta = -1.2) oct2d(CAS_BEZ, 12); }
    translate([0, 0, -T]) linear_extrude(T + 0.01) difference() { square(CAS_OUT, center = true); square(CAS_IN, center = true); }
    for (sx = [-1, 1]) translate([sx * HOOK_X - HOOK_W / 2, -CAS_OUT[1] / 2 - HOOK, -T - 1.6]) cube([HOOK_W, HOOK + CAS_W, 1.6]);   // hook, tied to the ring wall
  }
  for (i = [0 : LOUV[3] - 1]) translate([-LOUV[0] / 2 + 2, -(LOUV[3] - 1) * LOUV[2] / 2 + i * LOUV[2] - LOUV[1] / 2, 0])
    hull() { translate([0, 0, -1]) cube([LOUV[0] - 4, LOUV[1], 0.01]); translate([-1.2, -1.2, BZ + 0.01]) cube([LOUV[0] - 1.6, LOUV[1] + 2.4, 0.01]); }
  for (s = [-1, 1]) translate([s * (LOUV[0] / 2 + 9), 0, BZ - ACC_D]) linear_extrude(ACC_D + 0.1) mirror([s > 0 ? 1 : 0, 0]) cas_side2d();
  translate([0, 24, BZ - 0.6]) linear_extrude(1) text("CARBON MONOXIDE SENSOR", size = 4.4, font = "DIN Condensed:style=Bold", halign = "center", valign = "center", spacing = 1.15);
  translate([0, -27, BZ - 0.6]) linear_extrude(1) text("AIR IN \u00b7 DETECT \u00b7 STAY SAFE", size = 4.0, font = "DIN Condensed:style=Bold", halign = "center", valign = "center", spacing = 1.1);
  translate([0, 34, -1]) cylinder(d = M4B, h = BZ + 2);
}
module co_node_ref() color([0.1, 0.1, 0.11]) translate([W / 2 + NODE_X - 24, ZC - 30, -T - NODE_SETBACK - 40]) cube([48, 70, 40]);   // photo-39 node (EST)

// ---------------------------------------------------------------- accents (yellow, rev A fit rule)
module accents() {
  accent() translate([-11, -ZC]) chevron2d();
  translate([18, 0, 0]) accent() mirror([1, 0]) translate([-11, -ZC]) chevron2d();
  for (i = [0, 1]) translate([36 + i * 14, 0, 0]) accent() mirror([i, 0]) cas_side2d();
}

// ---------------------------------------------------------------- checks
open_hex = 2 * hex_cm2(cells);
louver_cm2 = LOUV[3] * (LOUV[0] - 4) * LOUV[1] / 100;
edge_top = H - MID_SLOT_Z; edge_bot = DECK_SLOT_Z;
if (panel == "lower") echo(str("LOWER rev B: ", W, " x ", H, " x ", T, " flat on the rails between the gussets (end clearance to the gusset rail legs ", END_CLR,
         ", notched where negative) | H implies a flush slot pitch of ", H - 20, "; measured pitch ", MID_SLOT_Z - DECK_SLOT_Z,
         " -> the panel stands ", H - (MID_SLOT_Z + 10), " above the mid-rail top"));
if (panel == "lower") echo(str("HOLES (captive M5 thumbscrews): panel x ", HX, " = frame x ", [for (x = HX) x + X0], " on rows ", HY, " (slot centrelines); edges ", edge_bot, " / ", edge_top));
if (panel == "lower") echo(str("OPEN AREA: hex ", len(cells), " + ", len(cells), " cells = ", round(open_hex * 10) / 10, " cm2 (R4.2 >= 32: ", open_hex >= 32 ? "MET" : "NOT MET",
         ") + louver intake ", louver_cm2, " cm2 through the CO tray"));
if (panel == "lower") echo(str("FIX ", fix, ": ", fix == "8ts" ? "8 captive yellow M5 thumbscrews (rows z 10 / 135.5)" : "4 captive thumbscrews on the mid-rail row + 2 T-slot hooks in the deck-rail slot",
         " at panel x ", HX, " | cable notch x ", NOTCH[0], "..", W - NOTCH[0], " to z ", NOTCH[1], " (", floor((W - 2 * NOTCH[0]) / COMB[1]), " comb gaps)"));
if (panel == "lower") echo(str("LOUVER: ", cassette ? "removable CO cassette (co_sensor tray)" : "plain louver insert over the rail-mounted node",
         " centred on the panel centreline; node at ", NODE_X, " mm (photo 39) -> inside the louver span +/-", (LOUV[0] - 4) / 2,
         "; louver back at the rail plane, node front ~", NODE_SETBACK, " behind it (design minimum 10, CONFIRM)"));
if (panel == "lower") echo(str("SHARED MID RAIL: body to z ", MID_SLOT_Z, " (slot centreline), ears to z ", MID_SLOT_Z - 10 + EAR_OV, " at x ", mirrored(EAR_X_LO),
         "; notches for the brow's ears at x ", mirrored(EAR_X_UP), " (t1_faceplate castellation)"));
if (panel == "lower") echo(str("HALF: ", W / 2, " x ", H, " (bed usable 281) | window ", WIN_W, " x ", WIN_T - WIN_B, " | splice bars ", 2 * SPLICE_HW, " x ", SPLICE_BOT[0], " / ", SPLICE_TOP[0]));
echo(str("MAXSPAN=", max(CB_D, 5 + 0.2, (panel == "upper" && placement == "lowerbay") || panel == "lower" ? TS_SEAT[0] : 0)));
assert(min(edge_bot, edge_top) >= 8, "hole row too close to the panel edge");
assert(W / 2 <= 281, "half longer than the bed allows");
assert(HX[0] - CB_D / 2 >= GUS_RL + GUS_CLR - X0 + 2, "corner counterbore lands in the gusset notch");
assert(SPLICE_BOT[0] >= 10 && SPLICE_TOP[0] >= 12, "splice bar too short between rail and window");
assert(TS_Z > WIN_T + 3 && TS_Z < MID_SLOT_Z - 10 - 3, "thumbscrew not between the window and the mid rail");
assert(ZC + CAS_BEZ[1] / 2 <= MID_SLOT_Z - CB_D / 2 - 1 && ZC - CAS_BEZ[1] / 2 >= DECK_SLOT_Z + CB_D / 2 + 1, "bezel fouls a hole row");
assert(HOOK_X - HOOK_W / 2 > SPLICE_HW + 2, "hook tab fouls the bottom splice bar");
assert(ZC - CAS_BEZ[1] / 2 >= NOTCH[1], "louver bezel hangs over the cable notch");
assert((MID_SLOT_Z - 10) + EAR_OV - MID_SLOT_Z - TS_SEAT[0] / 2 >= 2.5, "ear wall round the thumbscrew seat < 2.5");
assert(EAR_OV + EAR_CLR <= 20, "ear + clearance exceeds the 20 mm rail");
for (a = mirrored(EAR_X_LO), b = mirrored(EAR_X_UP)) assert(abs(a - b) >= EAR_W + EAR_CLR + 2, "castellated ears too close");
assert(ZC + CAS_BEZ[1] / 2 <= (MID_SLOT_Z + 10) - EAR_OV - EAR_CLR - 1, "louver bezel runs into the brow-ear notches");
assert(abs(NODE_X) + 24 <= (LOUV[0] - 4) / 2, "CO node not behind the louver span");
assert(NODE_SETBACK >= 10, "CO node closer than the 10 mm louver standoff");
assert(HOLE_X[1] + TS_SEAT[0] / 2 + 2 <= NOTCH[0], "thumbscrew seat breaks into the cable notch");
assert(fix != "4ts_hooks" || HOOK_TS[0][0] + HOOK_TS[0][1] / 2 + 2 <= NOTCH[0], "T-slot hook under the cable notch");
assert(CAS_IN[1] / 2 - 21.1 >= 0.5, "tray ears foul the cassette box");

// ---------------------------------------------------------------- scenes / exports
module panel_revB(ex = 0) {
  color([0.16, 0.16, 0.18]) half();
  color([0.2, 0.2, 0.22]) translate([ex * 14, 0, 0]) translate([W, 0, 0]) mirror([1, 0, 0]) half();
  color([0.3, 0.3, 0.32]) translate([0, 0, -ex * 20]) { splice_bar("top"); splice_bar("bottom"); }
  color([0.5, 0.5, 0.52]) translate([0, 0, -ex * 10]) splines();
  color([1, 0.8, 0]) translate([0, 0, ex * 14 - ACC_D]) linear_extrude(ACC_D) { chevron2d(); translate([W, 0]) mirror([1, 0]) chevron2d(); }
  color([1, 0.8, 0]) for (x = HX, y = HY) translate([x, y, -TS_SEAT[1]]) cylinder(d = 11, h = 7, $fn = 18);   // captive thumbscrews
  translate([W / 2, ZC, ex * 40]) {
    if (cassette) { color([0.14, 0.14, 0.15]) cassette(); translate([0, 0, -ex * 40]) co_tray_ref(); }
    else color([0.14, 0.14, 0.15]) louver_plain();
    color([1, 0.8, 0]) for (s = [-1, 1]) translate([s * (LOUV[0] / 2 + 9), 0, BZ - ACC_D + ex * 8]) linear_extrude(ACC_D) mirror([s > 0 ? 1 : 0, 0]) cas_side2d();
    color([1, 0.8, 0]) translate([0, 34, BZ]) cylinder(d = 11, h = 5, $fn = 18);                  // the one yellow thumbscrew
  }
}
if (panel == "lower" && (view == "front" || view == "exploded")) panel_revB(view == "exploded" ? 1 : 0);
if (panel == "lower" && view == "back") panel_revB(0);
if (panel == "lower" && view == "none") {
  if (part == "half") rotate([0, 180, 0]) half();                                    // face on the bed
  if (part == "half_mirror") rotate([0, 180, 0]) mirror([1, 0, 0]) half();           // convenience copy of the mirror
  if (part == "cassette") translate([0, 0, BZ]) rotate([0, 180, 0]) cassette();
  if (part == "louver_plain") translate([0, 0, BZ]) rotate([0, 180, 0]) louver_plain();
  if (part == "accents") accents();
  if (part == "splice") {                                                         // body-side face down, M4 boss rising
    rotate([180, 0, 0]) translate([-W / 2, -SPLICE_TOP[1], T]) splice_bar("top");
    translate([70, 0, 0]) rotate([180, 0, 0]) translate([-W / 2, -SPLICE_BOT[1], T]) splice_bar("bottom");
    for (i = [0, 1]) translate([110 + i * 10, -60, 0]) cube([2 * SPL[1], i == 0 ? WIN_B - 2 : H - WIN_T - 2, SPL[0]]);   // loose splines, flat
  }
}

// ============================================================================
// UPPER (CANARY badge) panel — rev B format (2026-09-29).  Same family rules as the
// lower rev B: 12 in wide, flush over both rails of ITS bay, between the gussets,
// strictly symmetric, two mirrored halves on a centreline seam hidden under the badge
// flange + V-groove design line, loose spline + 2 rear splice bars on 4 x M3 inserts.
//   placement = "lowerbay": 146.05 tall over the deck + mid rails, in front of the case
//               I/O faces.  8 CAPTIVE YELLOW THUMBSCREWS (every cable + Core swap is
//               behind it) and a CABLE-EXIT NOTCH along the bottom edge with comb teeth:
//               the panel goes on over dressed cables, they leave downward past the deck rail.
//   placement = "upperbay": the brow over the antenna level, sized to the measured
//               mid->top pitch (86 + 20 = 106 tall), flush M5 BHCS (nothing behind it
//               needs service).
// ============================================================================
function U_ZB(p)   = p == "lowerbay" ? DECK_SLOT_Z - 10 : MID_SLOT_Z - 10;          // frame z of the panel bottom
function U_ROWS(p) = p == "lowerbay" ? [DECK_SLOT_Z, MID_SLOT_Z] : [MID_SLOT_Z, TOP_SLOT_Z];
function U_H(p)    = p == "lowerbay" ? H : TOP_SLOT_Z - MID_SLOT_Z + 20;
function U_ZC(p)   = (U_ROWS(p)[0] + U_ROWS(p)[1]) / 2 - U_ZB(p);                   // bay-opening centre, panel coords
function U_RT(p)   = U_ROWS(p)[1] - 10 - U_ZB(p);                                    // underside of the upper rail, panel coords
function U_WIN(p)  = p == "lowerbay" ? [112, 50] : [112, 40];                         // badge window (wordmark 92 x 9.6)
function U_FL(p)   = U_WIN(p) + [12, 12];                                             // badge flange
function U_HXh(p)  = p == "lowerbay" ? [24, 66] : [24, 100];                          // lowerbay: holes outboard of the cable notch
function U_HX(p)   = concat(U_HXh(p), [for (x = U_HXh(p)) W - x]);
function U_HY(p)   = [for (r = U_ROWS(p)) r - U_ZB(p)];
// NOTCH / COMB / TS_SEAT: defined with the parameters at the top (shared with the lower panel)
function U_FIELD(p) = let(xr = p == "lowerbay" ? NOTCH[0] - 4 : W / 2 - U_FL(p)[0] / 2 - 6)
  [[20, 26], [xr, 26], [xr, U_RT(p) - 6], [20, U_RT(p) - 6]];
function U_SPB(p) = [(p == "lowerbay" ? NOTCH[1] : 20) + 2, U_ZC(p) - U_WIN(p)[1] / 2 - 2];   // bottom splice bar z range
function U_SPT(p) = [U_ZC(p) + U_WIN(p)[1] / 2 + 2, U_RT(p) - 2];                               // top splice bar z range
module u_chevron2d(p) let(zc = U_ZC(p)) stroke([[15, zc + 24], [7, zc + 16], [7, zc - 16], [15, zc - 24]], 5);
module cable_notch2d() difference() {
  translate([NOTCH[0], -1]) square([W - 2 * NOTCH[0], NOTCH[1] + 1]);
  for (x = [NOTCH[0] + COMB[1] : COMB[1] : W - NOTCH[0] - COMB[1] / 2])                              // comb teeth hang from the notch top
    translate([x - COMB[0] / 2, NOTCH[1] - COMB[2]]) { square([COMB[0], COMB[2] + 0.01]); translate([0, 0]) square([COMB[0] + COMB[3], 1.2]); }
}
module u_outline2d(p) difference() {
  union() {
    intersection() { outline2d(U_H(p), U_ZB(p)); if (p == "upperbay") translate([0, 10]) square([W, U_H(p)]); else square([W, U_H(p)]); }   // brow: body from the mid slot centreline
    if (p == "upperbay") for (x = mirrored(EAR_X_UP)) translate([x - EAR_W / 2, 20 - EAR_OV]) square([EAR_W, EAR_OV - 9]);   // ears down over the mid rail
  }
  if (p == "lowerbay") cable_notch2d();
  if (p == "upperbay") for (x = mirrored(EAR_X_LO)) translate([x - EAR_W / 2 - EAR_CLR, -1]) square([EAR_W + 2 * EAR_CLR, EAR_OV - 10 + 10 + EAR_CLR + 1]);  // notches for the CO panel's ears
}
function u_rows_x(p, i) = (p == "upperbay" && i == 0) ? mirrored(EAR_X_UP) : U_HX(p);
module u_body_full(p) let(h = U_H(p), zc = U_ZC(p), cells = hex_cells(U_FIELD(p)), fl = U_FL(p)) difference() {
  union() {
    translate([0, 0, -T]) linear_extrude(T - 1.2) u_outline2d(p);
    for (i = [0 : 2]) translate([0, 0, -1.2 + 0.4 * i]) linear_extrude(0.4 + 0.01) offset(delta = -0.4 * (i + 1)) u_outline2d(p);
  }
  for (i = [0, 1], x = u_rows_x(p, i)) let(y = U_HY(p)[i]) translate([x, y, 0]) {
    translate([0, 0, -T - 1]) cylinder(d = M5B, h = T + 2);
    if (p == "lowerbay") translate([0, 0, -TS_SEAT[1]]) cylinder(d = TS_SEAT[0], h = TS_SEAT[1] + 1);   // thumbscrew seat
    else translate([0, 0, -CB_H]) cylinder(d = CB_D, h = CB_H + 1);                                   // flush BHCS
  }
  for (c = concat(cells, mxw(cells))) translate([c[0], c[1], -T - 1]) rotate([0, 0, 30]) cylinder(r = 5 / sqrt(3), h = T + 2, $fn = 6);
  translate([0, 0, -ACC_D]) linear_extrude(ACC_D + 0.05) { u_chevron2d(p); translate([W, 0]) mirror([1, 0]) u_chevron2d(p); }
  translate([W / 2, zc, 0]) thru_cham() oct2d(U_WIN(p), 8);                                           // badge window (split by the seam)
  vgroove([[W / 2, p == "lowerbay" ? NOTCH[1] : 10], [W / 2, zc - fl[1] / 2 + 0.5]]);  vgroove([[W / 2, zc + fl[1] / 2 - 0.5], [W / 2, h + 1]]);
  for (y = [20, U_RT(p)]) vgroove([[24, y], [p == "lowerbay" ? NOTCH[0] - 4 : W - 24, y]], 0.8);
  if (p == "lowerbay") vgroove([[W - NOTCH[0] + 4, 20], [W - 24, 20]], 0.8);
  if (p == "lowerbay") vgroove([[NOTCH[0] - 4, U_RT(p)], [W - 24, U_RT(p)]], 0.8);
  for (sx = [-1, 1], b = [U_SPB(p), U_SPT(p)]) translate([W / 2 + sx * INS_X, (b[0] + b[1]) / 2, -T - 0.01]) cylinder(d = INS3_D, h = INS3_DEP);
  for (r = [[p == "lowerbay" ? NOTCH[1] : 10, zc - U_WIN(p)[1] / 2 - 1], [zc + U_WIN(p)[1] / 2 + 1, h + 1]])
    translate([W / 2 - SPL[1] - 0.2, r[0], -SPL_Z - SPL[0] - 0.1]) cube([2 * (SPL[1] + 0.2), r[1] - r[0], SPL[0] + 0.2]);
}
module u_half(p) intersection() { u_body_full(p); translate([-1, -1, -20]) cube([W / 2 + 1, U_H(p) + 2, 40]); }
module u_splice_bar(p, b) difference() {
  translate([W / 2 - SPLICE_HW, b[0], -T - 3.2]) cube([2 * SPLICE_HW, b[1] - b[0], 3.2]);
  for (sx = [-1, 1]) translate([W / 2 + sx * INS_X, (b[0] + b[1]) / 2, -T - 5]) cylinder(d = M3B, h = 6);
}
module u_splines(p) let(zc = U_ZC(p)) for (r = [[(p == "lowerbay" ? NOTCH[1] : 10) + 0.5, zc - U_WIN(p)[1] / 2 - 1.5], [zc + U_WIN(p)[1] / 2 + 1.5, U_H(p) - 0.5]])
  translate([W / 2 - SPL[1], r[0], -SPL_Z - SPL[0]]) cube([2 * SPL[1], r[1] - r[0], SPL[0]]);
// badge (rev A logic, sized per placement): black flange with the tracked wordmark cut through, ring + 4 catches in the window
module u_badge(p) let(win = U_WIN(p), fl = U_FL(p)) difference() {
  union() {
    linear_extrude(BZ) oct2d(fl, 10);
    translate([0, 0, -T]) linear_extrude(T) difference() { oct2d(win - [0.4, 0.4], 7.8); offset(delta = -3) oct2d(win, 8); }
    for (s = [-1, 1]) translate([s * (win[0] / 2 - 0.2), 0, -T - 0.6]) rotate([0, 0, s > 0 ? 0 : 180])
      hull() { translate([-3, -8, 0]) cube([3, 16, 1.2]); translate([-3, -8, 0]) cube([3.6, 16, 0.6]); }
  }
  translate([0, WM_DY, -1]) linear_extrude(BZ + 2) wordmark2d();
}
WM_DY = -12;                 // import(center=true) centres the SVG viewBox, not the glyphs: measured +12 mm high in rev A -> recentre
module u_backer(p) linear_extrude(1.6) offset(delta = 0.1) offset(delta = -3) oct2d(U_WIN(p), 8);   // yellow, shows through the letters
// ---------------------------------------------------------------- checks (upper)
if (panel == "upper") {
  cellsU = hex_cells(U_FIELD(placement));
  echo(str("UPPER rev B (", placement, "): ", W, " x ", U_H(placement), " x ", T, " | frame z ", U_ZB(placement), "..", U_ZB(placement) + U_H(placement),
           " | rows ", U_ROWS(placement), " = panel y ", U_HY(placement), " | holes x ", U_HX(placement), " (", placement == "lowerbay" ? "8 x captive yellow M5 thumbscrews" : "8 x M5 flush BHCS", ")"));
  echo(str("UPPER OPEN AREA: hex ", len(cellsU), " + ", len(cellsU), " = ", round(2 * hex_cm2(cellsU) * 10) / 10, " cm2",
           placement == "lowerbay" ? str(" + cable notch ", round((W - 2 * NOTCH[0]) * (NOTCH[1] - 20) / 100 * 10) / 10, " cm2 above the deck rail") : ""));
  echo(str("UPPER splice bars ", U_SPB(placement), " / ", U_SPT(placement), " | badge window ", U_WIN(placement), ", flange ", U_FL(placement), " | end clearance to gussets ", END_CLR));
  assert(min(U_HY(placement)[0], U_H(placement) - U_HY(placement)[1]) >= 8, "upper: hole row too close to the edge");
  assert(U_SPB(placement)[1] - U_SPB(placement)[0] >= 8 && U_SPT(placement)[1] - U_SPT(placement)[0] >= 8, "upper: splice bar too short");
  assert(U_ZC(placement) + U_FL(placement)[1] / 2 <= U_HY(placement)[1] - CB_D / 2, "upper: badge flange fouls the top hole row");
  assert(placement != "lowerbay" || U_HXh(placement)[1] + TS_SEAT[0] / 2 + 2 <= NOTCH[0], "upper: thumbscrew seat breaks into the cable notch");
  assert(placement != "lowerbay" || 2 * hex_cm2(cellsU) >= 32, "upper (lower bay, closes the compute bay): hex open area < 32 cm2 (R4.2)");
}
module upper_revB(p, ex = 0) {
  color([0.16, 0.16, 0.18]) u_half(p);
  color([0.2, 0.2, 0.22]) translate([ex * 14 + W, 0, 0]) mirror([1, 0, 0]) u_half(p);
  color([0.3, 0.3, 0.32]) translate([0, 0, -ex * 20]) { u_splice_bar(p, U_SPB(p)); u_splice_bar(p, U_SPT(p)); }
  color([0.5, 0.5, 0.52]) translate([0, 0, -ex * 10]) u_splines(p);
  color([1, 0.8, 0]) translate([0, 0, ex * 14 - ACC_D]) linear_extrude(ACC_D) { u_chevron2d(p); translate([W, 0]) mirror([1, 0]) u_chevron2d(p); }
  translate([W / 2, U_ZC(p), ex * 30]) { color([0.14, 0.14, 0.15]) u_badge(p); color([1, 0.8, 0]) translate([0, 0, -1.6 - ex * 10]) u_backer(p); }
  if (p == "lowerbay") color([1, 0.8, 0]) for (x = U_HX(p), y = U_HY(p)) translate([x, y, -TS_SEAT[1]]) cylinder(d = 11, h = 7, $fn = 18);   // captive thumbscrews
}
if (panel == "upper" && (view == "front" || view == "exploded")) upper_revB(placement, view == "exploded" ? 1 : 0);
if (panel == "upper" && view == "back") upper_revB(placement);
if (panel == "upper" && view == "none") {
  if (part == "u_half") rotate([0, 180, 0]) u_half(placement);
  if (part == "u_badge") translate([0, 0, BZ]) rotate([0, 180, 0]) u_badge(placement);
  if (part == "u_accents") { accent() translate([-11, -U_ZC(placement)]) u_chevron2d(placement);
                             translate([18, 0, 0]) accent() mirror([1, 0]) translate([-11, -U_ZC(placement)]) u_chevron2d(placement);
                             translate([100, 0, 0]) u_backer(placement); }
  if (part == "u_splice") { rotate([180, 0, 0]) translate([-W / 2, -U_SPB(placement)[0], T]) u_splice_bar(placement, U_SPB(placement));
                            translate([70, 0, 0]) rotate([180, 0, 0]) translate([-W / 2, -U_SPT(placement)[0], T]) u_splice_bar(placement, U_SPT(placement));
                            for (i = [0, 1]) translate([140 + i * 10, -60, 0]) cube([2 * SPL[1], 40, SPL[0]]); }
}
