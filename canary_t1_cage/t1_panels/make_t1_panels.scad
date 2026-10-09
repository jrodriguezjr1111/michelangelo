// ============================================================================
// CANARY T1 CAGE — LONG-FACE PANELS for the lower bay       (t1_panels family)
// 2026-09-27 · owner: "2 panels, each 15.75 in by 4.75 in for the cage modeled
// after the snapshot" (concept render = styling reference, photo 38 = the fit).
//
//   panel   = "upper" (CANARY badge + two hex fields)  | "lower" (bird + CO louver cassette)
//   segment = "L" | "C" | "R" | "all"                  (400.05 > 281 bed -> three segments)
//   part    = "body" | "accents" | "badge" | "louver" | "splice"
//   view    = "none" | "front" | "back_seg" | "exploded" (renders; parts are print-oriented)
//
// Every feature earns its place (t1_faceplate rule):
//   face printed DOWN (bed finish outside); 45 deg bed-edge chamfers; every
//   face-side recess is a short roof -> MAXSPAN echoed for the slice guard (R6.3)
//   hex fields = bay ventilation (open area echoed per field, R4.2)
//   louver     = the REAL cabin-air intake of a removable CO cassette (R1, one thumbscrew)
//   yellow     = separate snap-in accents only (R7.3); brand = the tracked wordmark SVG
//   seams      = jogged polyline under the yellow bar/slash + V-groove panel lines,
//                tongue-and-groove for flush faces + printed splice plate on M3 inserts
//   NO fake bolts, NO cosmetic-only features.
//
// Coordinates: VIEWER frame — x right / y up as seen from OUTSIDE the cage, face
// at z = 0, body toward -z (into the bay), raised bezels toward +z.  Exports are
// rigid-rotated (rotate [0,180,0]) so the face lands on the bed; no mirroring.
// ============================================================================
panel = "lower";
segment = "all";
part = "body";
view = "none";
taglines = false;     // "SENSE FURTHER" / "MONITOR / PROTECT / ENDURE" — NOT APPROVED (R8): owner sign-off first
explode = 0;
$fn = 40;

// ---------------------------------------------------------------- frame (photo 38) — CONFIRM by calipers
FACE_L = 406;             // MEAS  long-face outer length of the owner's 2020 frame
L = 400.05;               // owner 15.75 in
DECK_SLOT_Z = 10;         // EST   deck-rail slot centreline above the frame bottom (20-2020: 10)
MID_SLOT_Z  = 120;        // EST   mid-rail slot centreline: photo 38 gusset-bolt scale (20 mm pitch) -> 107-117, take 110 pitch
EDGE    = 10;             // DSN   hole row to panel edge (= the rail's outer 10 mm: panel flush with rail outer edges)
OWNER_H = 120.65;         // owner 4.75 in: only fits if MID_SLOT_Z - DECK_SLOT_Z <= OWNER_H - 2*8 (8 = min M5 counterbore edge)
H = MID_SLOT_Z - DECK_SLOT_Z + 2 * EDGE;   // 130 with the photo estimate  (set H = OWNER_H once the pitch is measured <= 104.65)
X0 = (FACE_L - L) / 2;    // panel starts 2.975 in from the frame corner
RB = 20;                  // rail band on the panel (the rail is behind it)
GUS_L = 70; GUS_H = 70;   // EST   flat corner gusset legs (photo 38: on the FRONT faces at every corner)
GUS_T = 3.2; GUS_HEAD = 2.8;               // EST   gusset plate + M5 button head
STANDOFF = GUS_T + GUS_HEAD + 0.4;         // 6.4: the panel stands proud of the gussets and their heads
STRAP_X = [88, 318];      // DSN   cargo-strap loops round the deck rail (E rev B had 100 / 306 — each moved clear of a seam; bearing pads behind)

// ---------------------------------------------------------------- body
T = 5.6;                  // 14 lines of 0.4
CH = 1.2;                 // bed-side 45 deg chamfer
M5B = 5.4; CB_D = 10.4; CB_H = 3.2; BOSS_D = 14;           // flush M5 BHCS into T-nuts (t1_faceplate numbers)
HOLE_X = [GUS_L + 12 - X0, L / 2, L - (GUS_L + 12 - X0)]; // corner holes just inboard of the gussets + one mid
HOLE_Y = [DECK_SLOT_Z - (DECK_SLOT_Z - EDGE), H - EDGE];   // = rail slot centrelines in panel coords
SKIRT = 2.4; RIB = 1.6;
XS = 112;                 // DSN   seam station (left); right seam at L - XS
M3B = 3.4; INS3_D = 4.4; INS3_DEP = 4.0;                    // M3 heat-set (short, 4 deep: 1.6 face skin)
M4B = 4.4; INS4_D = 5.6; INS4_DEP = 6.0;
TNG = [2.0, 1.6, 2.0];    // tongue: depth into the neighbour, thickness, face-skin above it
HEX_AF = 5.0; HEX_WEB = 1.6;                                // 5 AF cells, 4-line webs
ACC_D = 1.6; ACC_FIT = 0.1;                                 // accent pocket depth; accent oversize per side (0.2 press)
FIELD_GAP = 12;           // hex field to a SEAM accent edge (room for the splice inserts)
FIELD_GAP_ACC = 7;        // hex field to a plain accent edge
FONT = "DIN Condensed:style=Bold";

// ---------------------------------------------------------------- CO cassette (lower centre) — co_sensor rev 3 tray
CO_TRAY = [125.6, 26.22, 25.62];   // MEAS repo: make_co_tray.scad TRAY_L/W/H
CO_TAIL = [12, 16];                // zip/USB tail at +X
CO_EAR  = [[45, 17.11], [95, 17.11]];   // native M4-ear pattern (tray x from its -X end, +/-y)
CAS_IN  = [CO_TRAY[0] + CO_TAIL[0] + 2, 44, 0];   // box inner: tray + tail + 1/side ; ears need +/-21.1
CAS_W   = 2.0;
CAS_OUT = [CAS_IN[0] + 2 * CAS_W, CAS_IN[1] + 2 * CAS_W];
WIN_LO  = [CAS_OUT[0] + 2, CAS_OUT[1] + 2];       // body window, 1 mm clearance per side
BZ = 3.2;                          // raised bezel / badge flange thickness
CAS_BEZ = [WIN_LO[0] + 14, 84];    // cassette bezel octagon
CAS_DEPTH = 1.5 + CO_TRAY[2];      // bezel back -> tray base (ear plane): 1.5 air gap over the tray lid
EAR_T = 3;                         // EST  tray ear thickness at its base (CONFIRM on the printed co_tray)
HOOK = 2.6;                        // hook tab reach behind the window edge; the window is HOOK+0.4 wider on that side

// ---------------------------------------------------------------- badge (upper centre)
WIN_UP = [112, 50];  BADGE = [124, 62];  WM_W = 92;

// ================================================================ geometry helpers
function lerp(a, b, t) = a + (b - a) * t;
function seam_pts(p) = p == "upper"
  ? [[XS + 12, -1], [XS + 12, 30], [XS - 12, H - 30], [XS - 12, H + 1]]
  : [[XS - 8, -1], [XS - 8, RB + 4], [XS, RB + 12], [XS, H - RB - 12], [XS + 8, H - RB - 4], [XS + 8, H + 1]];
function seam_x(p, y, i = 0) = let(s = seam_pts(p)) i >= len(s) - 1 ? s[len(s) - 1][0] :
  (y <= s[i + 1][1] ? lerp(s[i][0], s[i + 1][0], (y - s[i][1]) / (s[i + 1][1] - s[i][1])) : seam_x(p, y, i + 1));
function mx(pts) = [for (q = pts) [L - q[0], q[1]]];               // mirror about the panel centre
function inside(pt, poly) = let(n = len(poly))                      // ray-cast point in polygon
  len([for (i = [0 : n - 1]) let(a = poly[i], b = poly[(i + 1) % n])
       if (((a[1] > pt[1]) != (b[1] > pt[1])) && (pt[0] < (b[0] - a[0]) * (pt[1] - a[1]) / (b[1] - a[1]) + a[0])) 1]) % 2 == 1;
HEX_R = HEX_AF / sqrt(3);                                          // circumradius
function hex_cells(poly) = let(px = HEX_AF + HEX_WEB, py = px * sqrt(3) / 2,
    xs = [for (q = poly) q[0]], ys = [for (q = poly) q[1]])
  [for (j = [0 : floor((max(ys) - min(ys)) / py)], i = [0 : floor((max(xs) - min(xs)) / px) + 1])
     let(c = [min(xs) + i * px + (j % 2) * px / 2, min(ys) + j * py])
     if (len([for (k = [0 : 5]) if (!inside(c + (HEX_R + HEX_WEB / 2) * [cos(30 + 60 * k), sin(30 + 60 * k)], poly)) 1]) == 0) c];
function hex_cm2(cells) = len(cells) * (sqrt(3) / 2) * HEX_AF * HEX_AF / 100;
module stroke(pts, w) for (i = [0 : len(pts) - 2]) hull() { translate(pts[i]) square(w, center = true); translate(pts[i + 1]) square(w, center = true); }
module oct2d(s, c) polygon([[-s[0]/2 + c, -s[1]/2], [s[0]/2 - c, -s[1]/2], [s[0]/2, -s[1]/2 + c], [s[0]/2, s[1]/2 - c],
                            [s[0]/2 - c, s[1]/2], [-s[0]/2 + c, s[1]/2], [-s[0]/2, s[1]/2 - c], [-s[0]/2, -s[1]/2 + c]]);
module vgroove(pts, d = 1.0) for (i = [0 : len(pts) - 2]) hull() for (q = [pts[i], pts[i + 1]])
  translate([q[0], q[1], -d]) cylinder(h = d + 0.02, r1 = 0.01, r2 = d + 0.02, $fn = 8);
module face_cut(d) translate([0, 0, -d]) linear_extrude(d + 0.05) children();                  // pocket from the face
module thru_cham(ch = CH) {                                         // through-cut, 45 deg wider at the face
  translate([0, 0, -T - STANDOFF - 1]) linear_extrude(T + STANDOFF + 1 - ch + 0.01) children();
  hull() { translate([0, 0, -ch]) linear_extrude(0.01) children(); translate([0, 0, 0]) linear_extrude(0.05) offset(delta = ch) children(); }
}

// ================================================================ panel artwork (2D, viewer frame)
OUTLINE = [[6, 0], [L - 6, 0], [L, 6], [L, H - 6], [L - 6, H], [6, H], [0, H - 6], [0, 6]];
YF0 = RB + 6; YF1 = H - RB - 6;                                    // hex fields stay off the rail bands
module chevron_end2d() stroke([[26, H - 30], [14, H - 42], [14, 42], [26, 30]], 6);   // "<" bracket, left end
function slash_up() = [[XS + 12 - 4.5, 30], [XS + 12 + 4.5, 30], [XS - 12 + 4.5, H - 30], [XS - 12 - 4.5, H - 30]];
function bar_lo()   = [[XS - 4.5, RB + 12], [XS + 4.5, RB + 12], [XS + 4.5, H - RB - 12], [XS - 4.5, H - RB - 12]];
function slash_lo() = [[50 - 4, H - 28], [50 + 4, H - 28], [66 + 4, 28], [66 - 4, 28]];   // bird-side "\" slash
function field_L(p) = p == "upper"
  ? [[36, YF0], [seam_x(p, YF0) - 4.5 - FIELD_GAP, YF0], [seam_x(p, YF1) - 4.5 - FIELD_GAP, YF1], [36, YF1]]
  : [[lerp(66, 50, (YF0 - 28) / (H - 56)) + 4 + FIELD_GAP_ACC, YF0], [XS - 4.5 - FIELD_GAP, YF0],
     [XS - 4.5 - FIELD_GAP, YF1], [lerp(66, 50, (YF1 - 28) / (H - 56)) + 4 + FIELD_GAP_ACC, YF1]];
function field_R(p) = p == "upper" ? mx(field_L(p))
  : [[L - XS + 4.5 + FIELD_GAP, YF0], [L - 36, YF0], [L - 36, YF1], [L - XS + 4.5 + FIELD_GAP, YF1]];
module bird2d() {                                                   // PLACEHOLDER — not the Canary mark (no tracked vector exists)
  translate([26, H / 2 - 4]) scale(0.78) {
    scale([1.35, 0.9]) circle(r = 11);                              // body
    translate([10, 10]) circle(r = 6.5);                            // head
    translate([15.5, 11]) polygon([[0, 2.5], [7, 0], [0, -2.5]]);   // beak
    polygon([[-12, 2], [-25, -6], [-22, -9], [-10, -5]]);           // tail
    translate([-2, -10]) polygon([[0, 0], [-2, -8], [0, -8], [3, 0]]); // leg
  }
}

// ================================================================ BODY (both panels)
cellsL = hex_cells(field_L(panel));  cellsR = hex_cells(field_R(panel));
module body_raw(p) difference() {
  union() {
    hull() { translate([0, 0, -CH]) linear_extrude(0.01) offset(delta = 0) polygon(OUTLINE);        // face chamfer
             translate([0, 0, -0.01]) linear_extrude(0.01) offset(delta = -CH) polygon(OUTLINE);
             translate([0, 0, -T]) linear_extrude(0.01) polygon(OUTLINE); }
    for (x = HOLE_X, y = HOLE_Y) translate([x, y, -T - STANDOFF]) cylinder(d = BOSS_D, h = STANDOFF + 0.01);    // bearing bosses
    for (sx = STRAP_X) translate([sx - X0 - 15, HOLE_Y[0] - 7, -T - STANDOFF]) cube([30, 14, STANDOFF + 0.01]);   // strap bearing pads
    difference() {                                                                                             // perimeter skirt
      translate([0, 0, -T - STANDOFF]) linear_extrude(STANDOFF + 0.01) difference() { polygon(OUTLINE); offset(delta = -SKIRT) polygon(OUTLINE); }
      gusset_relief();
    }
    for (y = [RB + 1.5, H - RB - 1.5]) translate([SKIRT, y - RIB / 2, -T - 5]) cube([L - 2 * SKIRT, RIB, 5.01]);  // back ribs at the band edges
    if (p == "lower") translate([L / 2 + CAS_BEZ[0] / 2 - 17, H / 2 - CAS_BEZ[1] / 2 + 9, -T - 3]) cylinder(d = 10, h = 3.01);   // boss behind the cassette thumbscrew insert
  }
  for (x = HOLE_X, y = HOLE_Y) translate([x, y, 0]) {                                                          // M5 flush counterbores
    translate([0, 0, -T - STANDOFF - 1]) cylinder(d = M5B, h = T + STANDOFF + 2);
    translate([0, 0, -CB_H]) cylinder(d = CB_D, h = CB_H + 1);
  }
  for (c = concat(hex_cells(field_L(p)), hex_cells(field_R(p)))) translate([c[0], c[1], -T - 1]) rotate([0, 0, 30]) cylinder(r = HEX_R, h = T + 2, $fn = 6);
  // accent pockets (yellow parts press in)
  face_cut(ACC_D) { if (p == "upper") chevron_end2d(); translate([L, 0]) mirror([1, 0]) chevron_end2d(); }   // lower: the bird plate owns the left end
  if (p == "upper") face_cut(ACC_D) { polygon(slash_up()); polygon(mx(slash_up())); }
  if (p == "lower") face_cut(ACC_D) { polygon(bar_lo()); polygon(mx(bar_lo())); polygon(slash_lo()); bird2d(); }
  // centre windows
  if (p == "upper") translate([L / 2, H / 2, 0]) thru_cham() oct2d(WIN_UP, 8);
  if (p == "lower") translate([L / 2, H / 2, 0]) {
    thru_cham() translate([-(HOOK + 0.4) / 2, 0]) oct2d(WIN_LO + [HOOK + 0.4, 0], 3);   // extra width on the hook side: insert shifted, slide over, lock
    translate([CAS_BEZ[0] / 2 - 17, -CAS_BEZ[1] / 2 + 9, -INS4_DEP]) cylinder(d = INS4_D, h = INS4_DEP + 0.1);   // cassette thumbscrew insert
  }
  // V-groove panel lines: rail-band edges + the seam jogs through the bands (the seam gap sits in the groove root)
  for (s = [0, 1]) let(sp = s == 0 ? seam_pts(p) : mx(seam_pts(p))) {
    vgroove([sp[0], sp[1]]); vgroove([sp[len(sp) - 2], sp[len(sp) - 1]]);
    if (p == "lower") { vgroove([sp[1], sp[2]]); vgroove([sp[3], sp[4]]); }
  }
  for (y = [RB, H - RB]) vgroove([[40, y], [L - 40, y]], 0.8);
  if (p == "lower") vgroove([[8, 26], [42, 26], [42, H - 26], [8, H - 26], [8, 26]], 0.8);   // bird plate outline
  if (taglines && p == "lower") translate([29, 30, -0.6]) linear_extrude(0.7) text("MONITOR / PROTECT / ENDURE", size = 2.6, font = FONT, halign = "center");
}
module gusset_relief() for (c = [[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [1, 1, 1, 1]])    // 4 corners of the lower-bay face
  translate([c[0] * L, c[1] * H, -T - STANDOFF - 1]) mirror([c[2], 0, 0]) mirror([0, c[3], 0])
    translate([-X0 - 2, -2, 0]) linear_extrude(STANDOFF + 1) polygon([[0, 0], [GUS_L + 4, 0], [GUS_L + 4, 24], [24, GUS_H + 4], [0, GUS_H + 4]]);

// ---------------------------------------------------------------- segments + seam joint
module region(seg, p) {
  sL = seam_pts(p); sR = mx(sL);
  if (seg == "L") polygon(concat([[-1, -1]], sL, [[-1, H + 1]]));
  if (seg == "R") polygon(concat([[L + 1, -1]], sR, [[L + 1, H + 1]]));
  if (seg == "C") difference() { translate([-1, -1]) square([L + 2, H + 2]); region("L", p); region("R", p); }
}
module tongue_band(p, grow) {                                       // the neighbour's side of each seam, within `grow` of it
  intersection() { offset(delta = grow) region("C", p); union() { region("L", p); region("R", p); } }
}
SPLICE_Y = [RB + 6, H - RB - 6];
function ins_pts(p, side) = [for (y = [H / 2 - 22, H / 2 + 22]) for (s = [0, 1])
  let(x = seam_x(p, y), xx = s == 0 ? x : L - x, dir = (s == 0 ? -1 : 1) * (side == "outer" ? 1 : -1)) [xx + dir * 9, y]];
module segment_body(seg, p) {
  difference() {
    union() {
      intersection() { body_raw(p); translate([0, 0, -50]) linear_extrude(100) region(seg, p); }
      if (seg == "C") intersection() { body_raw_solid(); translate([0, 0, -TNG[2] - TNG[1]]) linear_extrude(TNG[1]) tongue_band(p, TNG[0]); }
    }
    if (seg != "C") translate([0, 0, -TNG[2] - TNG[1] - 0.1]) linear_extrude(TNG[1] + 0.2) tongue_band(p, TNG[0] + 0.2);
    for (q = ins_pts(p, seg == "C" ? "inner" : "outer")) translate([q[0], q[1], -T - 0.01]) cylinder(d = INS3_D, h = INS3_DEP);   // M3 inserts from the back
  }
}
module body_raw_solid() translate([0, 0, -T]) linear_extrude(T) polygon(OUTLINE);
module splice(p, s) {                                               // printed splice plate, 3.2, behind each seam (s = 0 left, 1 right)
  sp = s == 0 ? seam_pts(p) : mx(seam_pts(p));
  difference() {
    translate([0, 0, -T - 3.2]) linear_extrude(3.2) intersection() {
      for (i = [0 : len(sp) - 2]) hull() for (q = [sp[i], sp[i + 1]]) translate(q) circle(r = 15);   // 15 mm band either side of the seam line
      translate([0, SPLICE_Y[0]]) square([L, SPLICE_Y[1] - SPLICE_Y[0]]);
    }
    for (q = concat(ins_pts(p, "outer"), ins_pts(p, "inner"))) if ((s == 0) == (q[0] < L / 2))
      translate([q[0], q[1], -T - 4]) cylinder(d = M3B, h = 5);
  }
}

// ================================================================ ACCENTS (yellow, snap-in: pocket outline + 0.1/side, 0.4 lead chamfer on the back)
module accent(h = ACC_D) {                                          // z 0 = visible face on the bed; 0.4 lead-in step on the back edge
  linear_extrude(h - 0.4) offset(delta = ACC_FIT) children();
  translate([0, 0, h - 0.4]) linear_extrude(0.4) offset(delta = ACC_FIT - 0.3) children(); }
module accents_list(p) {   // [name, 2D child index]; laid out flat for printing
  // printed face-down too: z = 0 is the visible face
  if (p == "upper") accent() translate([-20, -H / 2]) chevron_end2d();
  translate([22, 0, 0]) accent() mirror([1, 0]) translate([-20, -H / 2]) chevron_end2d();
  if (p == "upper") { translate([55, 0, 0]) accent() translate([-XS, -H / 2]) polygon(slash_up());
                      translate([90, 0, 0]) accent() translate([-(L - XS), -H / 2]) polygon(mx(slash_up())); }
  if (p == "lower") { translate([50, 0, 0]) accent() translate([-XS, -H / 2]) polygon(bar_lo());
                      translate([66, 0, 0]) accent() translate([-(L - XS), -H / 2]) polygon(mx(bar_lo()));
                      translate([95, 0, 0]) accent() translate([-58, -H / 2]) polygon(slash_lo());
                      translate([135, 0, 0]) accent() translate([-26, -H / 2]) bird2d();
                      for (i = [0, 1]) translate([170 + i * 16, 0, 0]) accent() cas_side2d(); }
  if (p == "upper") translate([168, 0, 0]) badge_backer();
}

// ================================================================ BADGE (upper centre) — black flange + ring, wordmark cut through; yellow backer shows through
RING = 3.0;
module wordmark2d() resize([WM_W, 0], auto = true) import("brand/canary-wordmark.svg", center = true);
module badge() difference() {
  union() {
    linear_extrude(BZ) offset(delta = -0.001) oct2d(BADGE, 10);                                     // flange on the face (z 0..BZ)
    translate([0, 0, -T]) linear_extrude(T) difference() { oct2d(WIN_UP - [0.4, 0.4], 7.8); offset(delta = -RING) oct2d(WIN_UP, 8); }   // ring in the window
    for (s = [-1, 1]) translate([s * (WIN_UP[0] / 2 - 0.2), 0, -T - 0.6]) rotate([0, 0, s > 0 ? 0 : 180])   // snap catches behind the body
      hull() { translate([-RING, -8, 0]) cube([RING, 16, 1.2]); translate([-RING, -8, 0]) cube([RING + 0.6, 16, 0.6]); }
  }
  translate([0, taglines ? 5 : 1, -1]) linear_extrude(BZ + 2) wordmark2d();                          // letters THROUGH the flange
  if (taglines) translate([0, -17, BZ - 0.6]) linear_extrude(1) text("SENSE FURTHER", size = 4, font = FONT, halign = "center", spacing = 1.3);
}
module badge_backer() linear_extrude(1.6) offset(delta = ACC_FIT) offset(delta = -RING) oct2d(WIN_UP, 8);   // yellow, presses into the ring against the flange

// ================================================================ CO CASSETTE (lower centre) — louver bezel + pocket box carrying the co_sensor tray
module cas_side2d() stroke([[0, 20], [-4, 16], [-4, -16], [0, -20]], 4);                          // "[" side accent
LOUV = [116, 4.0, 7.2, 5];                                                                         // slot L, slot h, pitch, count
module louver() difference() {
  union() {
    hull() { linear_extrude(BZ - CH) oct2d(CAS_BEZ, 12); translate([0, 0, BZ - CH]) linear_extrude(CH) offset(delta = -CH) oct2d(CAS_BEZ, 12); }   // bezel, face chamfer
    translate([0, 0, -CAS_DEPTH]) linear_extrude(CAS_DEPTH + 0.01) difference() {                    // pocket box through the body window
      square(CAS_OUT, center = true); square([CAS_IN[0], CAS_IN[1]], center = true); }
    for (s = [-1, 1]) translate([-CAS_IN[0] / 2, s > 0 ? CAS_IN[1] / 2 - 7 : -CAS_IN[1] / 2, -CAS_DEPTH + EAR_T]) cube([CO_TRAY[0], 7, 6]);   // ear ledges, in FRONT of the ear plane
    translate([-CAS_OUT[0] / 2 - HOOK, -10, -T - 1.6]) cube([HOOK + 0.01, 20, 1.6]);                  // hook tab behind the window's left edge
  }
  for (i = [0 : LOUV[3] - 1]) translate([-LOUV[0] / 2 + 2, -(LOUV[3] - 1) * LOUV[2] / 2 + i * LOUV[2] - LOUV[1] / 2, 0])
    hull() { translate([0, 0, -1]) cube([LOUV[0] - 4, LOUV[1], 0.01]); translate([-1.2, -1.2, BZ + 0.01]) cube([LOUV[0] - 1.6, LOUV[1] + 2.4, 0.01]); }   // louver slots, 45 deg lips
  for (s = [-1, 1]) translate([s * (LOUV[0] / 2 + 9), 0, BZ - ACC_D]) linear_extrude(ACC_D + 0.1) mirror([s > 0 ? 1 : 0, 0]) cas_side2d();   // yellow side pockets
  translate([-8, CAS_BEZ[1] / 2 - 12, BZ - 0.6]) linear_extrude(1) text("CARBON MONOXIDE SENSOR", size = 4.6, font = FONT, halign = "center", valign = "center", spacing = 1.15);
  translate([-10, -CAS_BEZ[1] / 2 + 10, BZ - 0.6]) linear_extrude(1) text("AIR IN · DETECT · STAY SAFE", size = 4.0, font = FONT, halign = "center", valign = "center", spacing = 1.1);
  translate([CAS_BEZ[0] / 2 - 17, -CAS_BEZ[1] / 2 + 9, -1]) cylinder(d = M4B, h = BZ + 2);            // captive thumbscrew
  for (e = CO_EAR, sy = [-1, 1]) translate([-CAS_IN[0] / 2 + 1 + e[0], sy * e[1], -CAS_DEPTH + EAR_T - 0.01]) cylinder(d = INS3_D, h = 4.5);   // M3 inserts: ears screwed from the BACK
  translate([CAS_IN[0] / 2 - 1, -CO_TAIL[1] / 2 - 1, -CAS_DEPTH - 1]) cube([CAS_W + 2, CO_TAIL[1] + 2, CAS_DEPTH - T - 2]);            // USB tail / cable exit
}
module co_tray_ref() color([0.25, 0.25, 0.27]) translate([-CAS_IN[0] / 2 + 1, -CO_TRAY[1] / 2, -CAS_DEPTH]) {
  cube(CO_TRAY); translate([CO_TRAY[0], (CO_TRAY[1] - CO_TAIL[1]) / 2, 4]) cube([CO_TAIL[0], CO_TAIL[1], 12]);
  for (e = CO_EAR, sy = [-1, 1]) translate([e[0], CO_TRAY[1] / 2 + sy * e[1], 0]) cylinder(d = 8, h = EAR_T); }

// ================================================================ checks
MAXSPAN = panel == "lower" ? 16 : max(9 + 2 * ACC_FIT, CB_D);   // widest face-side roof: bird pocket (lower) | counterbore / slash (upper)
edge_min = min(HOLE_Y[0], H - HOLE_Y[1]);
aL = hex_cm2(cellsL); aR = hex_cm2(cellsR);
louver_cm2 = LOUV[3] * (LOUV[0] - 4) * LOUV[1] / 100;
seg_w = [max([for (q = seam_pts(panel)) q[0]]) + TNG[0], L - 2 * min([for (q = seam_pts(panel)) q[0]]) + 2 * TNG[0]];
echo(str("PANEL ", panel, ": ", L, " x ", H, " x ", T, " (+", STANDOFF, " standoff over the gussets) | owner H ", OWNER_H,
         " vs rail-derived H ", H, " (slot pitch ", MID_SLOT_Z - DECK_SLOT_Z, ")"));
echo(str("HOLES M5 flush BHCS: x ", HOLE_X, " (frame x ", [for (x = HOLE_X) x + X0], ") on rows y ", HOLE_Y,
         " = frame z ", [DECK_SLOT_Z, MID_SLOT_Z], " (slot centrelines); edge distance ", edge_min));
echo(str("HEX 5 AF / 1.6 web: field L ", len(cellsL), " cells = ", round(aL * 10) / 10, " cm2, field R ", len(cellsR), " cells = ",
         round(aR * 10) / 10, " cm2, TOTAL ", round((aL + aR) * 10) / 10, " cm2", panel == "lower" ? str(" | louver intake ", louver_cm2, " cm2 (CO)") : ""));
echo(str("SEGMENTS: L ", seg_w[0], " | C ", seg_w[1], " | R ", seg_w[0], " wide x ", H, "  (bed usable 281)"));
echo(str("MAXSPAN=", MAXSPAN));
if (panel == "lower") echo(str("CO CASSETTE: bezel ", CAS_BEZ, ", box ", CAS_OUT, " through a ", WIN_LO, " window, depth behind the face ", CAS_DEPTH + 4,
         " (", CAS_DEPTH + 4 - T - STANDOFF, " past the rail plane); tray ", CO_TRAY, " + tail on its native ear pattern"));
assert(edge_min >= 8, "hole row too close to the panel edge — rail pitch vs panel height (see OWNER_H)");
assert(max(seg_w) <= 281, "segment longer than the bed allows (R6.4)");
assert(panel != "upper" || aL + aR >= 32, "upper panel hex open area < 32 cm2 (R4.2)");
assert(HOLE_X[0] - BOSS_D / 2 >= GUS_L - X0 + 2, "corner boss lands on the gusset");
assert(WIN_LO[0] + 2 * 6 <= L - 2 * (XS + 4.5), "cassette bezel overlaps the seam bars");
assert(CAS_IN[1] / 2 - 21.1 >= 0.5, "tray ears foul the cassette box");
assert(T - INS3_DEP >= 1.6 - 1e-6, "M3 insert breaks the face skin");
assert(T + 3 - INS4_DEP >= 2, "cassette thumbscrew insert breaks through its boss");
for (q = concat(ins_pts(panel, "outer"), ins_pts(panel, "inner"))) assert(abs(q[0] - (q[0] < L / 2 ? seam_x(panel, q[1]) : L - seam_x(panel, q[1]))) <= 15 - 4, "splice plate does not cover an insert");

// ================================================================ scenes / exports
module seg_colour(seg) color(seg == "C" ? [0.2, 0.2, 0.22] : [0.16, 0.16, 0.18]) children();
module panel_assembled(p, ex = 0) {
  for (seg = ["L", "C", "R"]) translate([ex * (seg == "L" ? -12 : seg == "R" ? 12 : 0), 0, 0]) seg_colour(seg) segment_body(seg, p);
  color([0.3, 0.3, 0.32]) for (s = [0, 1]) translate([0, 0, -ex * 20]) splice(p, s);
  color([1, 0.8, 0]) translate([0, 0, ex * 14]) {
    translate([0, 0, -ACC_D]) linear_extrude(ACC_D) { if (p == "upper") chevron_end2d(); translate([L, 0]) mirror([1, 0]) chevron_end2d();
      if (p == "upper") { polygon(slash_up()); polygon(mx(slash_up())); }
      if (p == "lower") { polygon(bar_lo()); polygon(mx(bar_lo())); polygon(slash_lo()); bird2d(); } }
  }
  if (p == "upper") translate([L / 2, H / 2, ex * 30]) { color([0.14, 0.14, 0.15]) badge(); color([1, 0.8, 0]) translate([0, 0, -1.6 - ex * 10]) badge_backer(); }
  if (p == "lower") translate([L / 2, H / 2, ex * 40]) {
    color([0.14, 0.14, 0.15]) louver(); translate([0, 0, -ex * 40]) co_tray_ref();
    color([1, 0.8, 0]) for (s = [-1, 1]) translate([s * (LOUV[0] / 2 + 9), 0, BZ - ACC_D + ex * 8]) linear_extrude(ACC_D) mirror([s > 0 ? 1 : 0, 0]) cas_side2d();
    color([1, 0.8, 0]) translate([CAS_BEZ[0] / 2 - 17, -CAS_BEZ[1] / 2 + 9, BZ]) cylinder(d = 11, h = 5, $fn = 18);   // yellow captive thumbscrew
  }
}
if (view == "front" || view == "exploded") panel_assembled(panel, view == "exploded" ? 1 : 0);
if (view == "back_seg") { seg_colour("C") segment_body("C", panel); color([0.3, 0.3, 0.32]) splice(panel, 0);
                          translate([-10, 0, 0]) seg_colour("L") segment_body("L", panel); }
// print-oriented parts (face on the bed)
module print_rot() rotate([0, 180, 0]) children();
if (view == "none") {
  if (part == "body" && segment != "all") print_rot() segment_body(segment, panel);
  if (part == "body" && segment == "all") print_rot() for (seg = ["L", "C", "R"]) segment_body(seg, panel);
  if (part == "splice") translate([0, 0, T + 3.2]) for (s = [0, 1]) translate([s == 0 ? -XS + 40 : -(L - XS) + 130, 0, 0]) splice(panel, s);   // laid side by side
  if (part == "accents") accents_list(panel);
  if (part == "badge" && panel == "upper") translate([0, 0, BZ]) print_rot() badge();
  if (part == "louver" && panel == "lower") translate([0, 0, BZ]) print_rot() louver();
}
