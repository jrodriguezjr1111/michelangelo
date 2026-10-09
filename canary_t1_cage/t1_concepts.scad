// ============================================================================
// CANARY T1 CAGE — THREE SWAP CONCEPTS, LOW-FIDELITY MASSING MODELS
// 2026-09-21 · concept study · INPUT KIT for the owner + Andrew, NOT a design
// of record.  No insert bores, no joints, no print features: these solids exist
// to make the SWAP MECHANISM and the SIZE CLASS legible, nothing else.
//
//   concept = "A"  CARTRIDGE RACK   Core chassis on the rod spine; peripherals
//                                   are keyed front-loading cartridges.
//   concept = "B"  OPEN BOOK        one visible plane on the 10 mm M3 cheese
//                                   grid; every component on its own carrier.
//   concept = "C"  ROD PODS         no shell; one faceted pod per function,
//                                   clamped to the rods, on a harness trunk.
//   concept = "D"  EXTRUSION FRAME  80/20 20-2020 (or Misumi HFS3-1515 via
//                                   series=15) T-slot frame; printed cartridges
//                                   ride DIRECTLY in the T-slot on ASA T-keys.
//   panel  = 0..1      concept D: how far the louvered side insert is slid out
//   labels = true      concept D: member labels M01-M14 (cut diagram render)
//   swap  = which module is shown leaving   ("TRAFFIC" | "RTK" | "LTE" |
//                                            "CABIN CO" | "BATTERY" | "IMU" | "CORE")
//   pull  = 0..1   how far it has travelled (0 = assembled)
//   lid   = 0..1   concept A core lid slides out rearward / concept B lid open
//
// Governing requirement (owner, 2026-09-21): "a solution that allows me to
// quickly swap components if they fail or need inspection."
// IMU RULE, all three: the IMU seats on a RIGID KEYED DATUM tied to the rod
// skeleton with captive screws — never on a sliding rail alone.
//
// Frame: X along the rods (fore-aft), Y lateral, Z up.  Sizes mirror
// t1_params.py / envelope_check.py; MEAS / EST provenance lives there.
// Colours: matte black structure, ONE accent = canary yellow, used only on
// things a hand touches or an eye must find (tabs, thumbscrews, caps, labels).
// ============================================================================
include <t1_mark.scad>

concept = "A";
swap = "TRAFFIC";
pull = 0;
lid = 0;
show_labels = true;
label_set = "product";      // "product" (patent pending -> real names) | "show"
labels = false;
series = 20;                // DECIDED 2026-09-21: 80/20 20-series (15 mm Misumi considered, rejected)
panel = 0;
$fn = 32;

BLK = [0.19, 0.19, 0.21];  BLK2 = [0.29, 0.29, 0.32];
YEL = [1.00, 0.80, 0.00];  ALU = [0.78, 0.80, 0.83];
PCB = [0.05, 0.32, 0.25];  MET = [0.35, 0.36, 0.40];  CBL = [0.30, 0.30, 0.32];

// ---- components (L along X, W along Y, H) — see t1_params.py for provenance
ORIN = [100, 81, 36];         // bare Jetson Orin dev kit, M3 91.86 x 58.37   MEAS/EST-H
HUB  = [139, 87, 35];         // EST_ Advantech UHR204 (PUB drawing)
BAT  = [74, 107, 64];         // EST_ V-mount 99 Wh
FLY  = [64.93, 56.03, 27];    // FlyCatcher                                    MEAS
COS  = [114, 20.92, 15.12];   // CO stick                                      MEAS
ZED  = [43.5, 43.5, 12];      // ZED-F9P                                       MEAS
LTE  = [80, 35, 12];          // EG25-G carrier (pattern 70.80 x 24.21 MEAS)
IMU  = [26, 24, 5];           // BNO085 (pattern 19.95 x 17.81 MEAS)
PDB  = [60, 40, 20];          // EST_ fuse / power distribution

TUBE_D = 15; TUBE_Y = 30;     // CANON rev B rod pair, 60 c-c

LBL = label_set == "product"
  ? ["CANARY CORE", "TRAFFIC", "CABIN CO", "RTK", "LTE", "POWER", "IMU", "SPARE", "VIBRATION"]
  : ["T1-00 ALPHA", "T1-01 BRAVO", "T1-02 CHARLIE", "T1-03 DELTA", "T1-04 ECHO",
     "T1-05 FOXTROT", "T1-06 GOLF", "T1-07 HOTEL", "T1-08 INDIA"];
function lbl(n) = LBL[search([n], ["CORE","TRAFFIC","CABIN CO","RTK","LTE","BATTERY","IMU","SPARE","VIB"])[0]];
function P(n) = swap == n ? pull : 0;

// ---------------------------------------------------------------- primitives
module fbox(s, c = 2) {                 // faceted box: 45 deg chamfer on every edge
  hull() {
    translate([c, c, 0]) cube([s[0] - 2*c, s[1] - 2*c, s[2]]);
    translate([c, 0, c]) cube([s[0] - 2*c, s[1], s[2] - 2*c]);
    translate([0, c, c]) cube([s[0], s[1] - 2*c, s[2] - 2*c]);
  }
}
module thumb(d = 11, h = 7) {           // captive knurled thumbscrew, +Z
  color(YEL) { cylinder(d = d, h = h, $fn = 12); cylinder(d = d*0.55, h = h + 2, $fn = 24); }
}
module plate_label(txt, w, h = 9) {     // accent label plate, face +Z, centred
  color(YEL) translate([-w/2, -h/2, 0]) fbox([w, h, 1.6], 0.6);
  if (show_labels) color(BLK) translate([0, 0, 1.6])
    linear_extrude(0.4) text(txt, size = h*0.62, font = "DIN Condensed:style=Bold",
                             halign = "center", valign = "center", spacing = 1.08);
}
module xbrace(w, h, d = 1.6, b = 5) {   // recessed X-brace pocket (cutter), centred, +Z top
  difference() {
    translate([-w/2, -h/2, -d]) cube([w, h, d + 0.1]);
    for (s = [-1, 1]) rotate([0, 0, s * atan2(h, w)])
      translate([-(w + h), -b/2, -d - 0.1]) cube([2*(w + h), b, d + 0.3]);
  }
}
module rods(len, x0) {
  color(ALU) for (s = [-1, 1]) translate([x0, s*TUBE_Y, 0]) rotate([0, 90, 0])
    difference() { cylinder(d = TUBE_D, h = len); translate([0,0,-1]) cylinder(d = 11, h = len + 2); }
}
module canon_cap() {                    // canon cap massing, trough along X, rod axis z=0
  color(YEL) difference() {
    translate([-10, -17, -1]) cube([20, 34, 11]);
    rotate([0, 90, 0]) cylinder(d = 15.4, h = 30, center = true);
  }
}
module pigtail(len = 28) {              // short pigtail + LOCKING connector (yellow ring)
  color(CBL) rotate([-90, 0, 0]) cylinder(d = 5, h = len);
  translate([0, len, 0]) rotate([-90, 0, 0]) {
    color(MET) cylinder(d = 10, h = 14, $fn = 6);
    color(YEL) translate([0, 0, 3]) cylinder(d = 11.5, h = 3, $fn = 24);
  }
}
module comp(c, col) {                  // component massing: board + body, not a brick
  if (col == PCB) {
    color(PCB) cube([c[0], c[1], 2]);
    color(MET) translate([c[0]*0.14, c[1]*0.14, 2]) cube([c[0]*0.72, c[1]*0.72, max(c[2] - 2, 1)]);
  } else color(col) cube(c);
}
module imu_datum() {                    // the IMU rule, identical in A / B / C
  // rigid keyed block on the rod-tied member: 2 dowels (key) + 2 captive screws
  color(BLK2) translate([-20, -18, 0]) fbox([40, 36, 8], 1.5);
  translate([0, 0, 8 + 22*P("IMU")]) {
    color(PCB) translate([-13, -12, 0]) cube([26, 24, 3]);
    color(YEL) translate([-17, -15, 3]) difference() {
      fbox([34, 30, 9], 2); translate([3, 3, -1]) cube([28, 24, 7]);
    }
    for (p = [[-13, 0], [13, 0]]) translate([p[0], p[1], 12]) thumb(7, 4);
  }
  color(MET) for (p = [[-13, 9], [10, -9]])     // asymmetric dowels = the key
    translate([p[0], p[1], 8]) cylinder(d = 2.5, h = 5);
}

// =============================================================== CONCEPT A
AX = 285; AY = 175; AZ = 100; A_CD = 74;        // body; cartridge depth
A_BAYS = [ // name, x0, z0, w, h, depth, component
  ["TRAFFIC",   8,  8,  72, 42, A_CD, FLY],
  ["LTE",      84,  8,  80, 42, A_CD, [LTE[0], LTE[1], LTE[2]]],
  ["SPARE",   168,  8,  30, 42, A_CD, [0, 0, 0]],
  ["RTK",       8, 52,  60, 42, A_CD, ZED],
  ["CABIN CO", 72, 52, 126, 42, A_CD, COS],
  ["BATTERY", 203,  8,  78, 68, 112, [BAT[0], BAT[1], BAT[2]]]];

module a_cartridge(b) {
  n = b[0]; w = b[3]; h = b[4]; d = b[5]; c = b[6];
  translate([b[1], -2 - (d + 25) * P(n), b[2]]) {
    color(BLK) fbox([w - 1, 5, h - 1], 1.5);                         // faceted faceplate
    color(BLK2) translate([3, 5, 2]) cube([w - 7, d - 8, 3]);         // tray
    color(BLK2) translate([3 + (len(n) % 3) * 9, 5, 0]) cube([6, d - 8, 2]); // KEY rib (per-bay offset)
    if (c[0] > 0) translate([(w - 1 - c[0]) / 2, 8, 5])
      comp([c[0], min(c[1], d - 12), c[2]], n == "BATTERY" ? MET : PCB);
    translate([w - 12, 0, h / 2 - 1]) rotate([90, 0, 0]) thumb(10, 6);      // ONE captive thumbscrew
    color(YEL) translate([6, -7, h / 2 - 4]) fbox([10, 8, 7], 1);            // pull tab
    if (n != "SPARE") translate([w / 2 + 2, -0.4, h - 10]) rotate([90, 0, 0])
      plate_label(lbl(n), min(w - 28, 50), 10);
    if (P(n) > 0.2 && n != "BATTERY") translate([w / 2, d - 3, 12]) pigtail();
  }
}
module concept_A() {
  // ---- core chassis: rack cut, core bay cut, faceted pockets
  color(BLK) difference() {
    fbox([AX, AY, AZ], 4);
    for (b = A_BAYS) translate([b[1], -1, b[2]]) cube([b[3], b[5] + 1, b[4]]);
    translate([8, A_CD + 6, 6]) cube([190, AY - A_CD - 12, AZ]);        // core bay, open top
    translate([203, 118, 6]) cube([74, AY - 124, AZ]);                  // power-dist bay
    translate([AX / 2, AY, AZ / 2]) rotate([-90, 0, 0]) translate([0, 0, 0]) mirror([0,0,1])
      for (i = [-1, 0, 1]) translate([i * 90, 0, 0]) xbrace(80, 78);    // rear face X-braces
    for (s = [0, 1]) translate([s * AX, AY / 2, AZ / 2]) rotate([0, s ? 90 : -90, 0])
      xbrace(78, AY - 40);                                              // end-face X-braces
    for (i = [0 : 7]) translate([20 + i * 22, AY - 3, 70]) cube([14, 8, 5]);  // exhaust louvres
  }
  // ---- core internals (visible when the lid is lifted)
  translate([14, A_CD + 8, 6]) {
    color(MET) cube(HUB);
    translate([2, 3, HUB[2] + 6]) comp(ORIN, PCB);                      // bare dev kit, fan on top
  }
  color(MET) translate([210, 124, 6]) cube(PDB);
  // ---- core lid: 4 captive thumbscrews, fan intake grille.  FINDING: with the rods
  // on top a lid cannot lift clear (24.5 mm under the rods) -> it lifts 10 mm and
  // SLIDES OUT REARWARD under the rods.  The rods cost the design its top access.
  translate([0, 170 * max(lid, P("CORE")), 10 * min(1, 3 * max(lid, P("CORE")))]) {
    color(BLK) difference() {
      translate([4, A_CD + 2, AZ]) fbox([198, AY - A_CD - 6, 5], 1.5);
      translate([14 + 50, A_CD + 8 + 41, AZ - 1]) for (a = [0 : 60 : 300]) rotate([0, 0, a])
        translate([8, -5, 0]) cube([24, 10, 8]);                        // intake over the fan
      translate([160, A_CD + 50, AZ + 5]) xbrace(60, 70);
    }
    for (p = [[10, A_CD + 8], [196, A_CD + 8], [10, AY - 10], [196, AY - 10]])
      translate([p[0], p[1], AZ + 5]) thumb();
    translate([150, AY - 16, AZ + 5]) plate_label(lbl("CORE"), 70, 11);
  }
  for (b = A_BAYS) a_cartridge(b);
  // ---- rod spine ON TOP: yokes on the end frames, rods = handle + belt path + rail
  for (x = [14, AX - 14]) translate([x, AY / 2, AZ]) {
    color(BLK) translate([-14, -AY / 2 - 6, 0]) difference() {
      fbox([28, AY + 12, 32], 3);
      translate([-1, 22, -1]) cube([30, AY - 32, 14]);                  // bridge over the lid
      for (s = [-1, 1]) translate([-1, AY / 2 + 6 + s * TUBE_Y, 32]) rotate([0, 90, 0]) cylinder(d = 15.4, h = 30);
    }
    for (s = [-1, 1]) translate([0, s * TUBE_Y, 32]) canon_cap();
  }
  translate([0, AY / 2, AZ + 32]) rods(400, -70);
  translate([AX - 14, AY / 2, AZ + 32 + 10]) imu_datum();               // on the rear yoke, between the caps... see README
  // brand mark on the top-left of the service face
  color(YEL) translate([AX - 40, -0.2, AZ - 12]) rotate([90, 0, 0]) mark3d(18, 1);
}

// =============================================================== CONCEPT B
BX = 300; BY = 262; B_FLOOR = 8; B_WALL = 28; B_LID = 58; B_T = 4;
B_CARRIERS = [ // name, x0, y0, w, d, component, comp-colour
  ["CABIN CO",  6,   6, 126,  32, COS, PCB],
  ["RTK",     140,   6,  56,  56, ZED, PCB],
  ["LTE",     204,   6,  84,  46, LTE, PCB],
  ["CORE",      6,  68, 112,  92, ORIN, PCB],
  ["TRAFFIC", 126,  68,  76,  68, [FLY[0], FLY[1], FLY[2]], PCB],
  ["POWER",   250,  68,  44,  66, [PDB[1], PDB[0], PDB[2]], MET],
  ["BATTERY",   6, 166, 116,  82, [BAT[1], BAT[0], BAT[2]], MET],
  ["HUB",     130, 160, 148,  96, HUB, MET]];

module b_carrier(c) {
  n = c[0];
  translate([c[1], c[2], B_FLOOR + 90 * P(n)]) {
    color(BLK2) fbox([c[3], c[4], 4], 1);
    translate([(c[3] - c[5][0]) / 2, (c[4] - c[5][1]) / 2, 4 + (c[6] == PCB ? 5 : 0)]) comp(c[5], c[6]);
    translate([6, 6, 4]) thumb(9, 6);
    translate([c[3] - 6, c[4] - 6, 4]) thumb(9, 6);                     // TWO captive thumbscrews
    translate([c[3] / 2, 5.5, 4]) plate_label(lbl(n == "HUB" ? "CORE" : n == "POWER" ? "BATTERY" : n),
                                                min(c[3] - 30, 44), 7);
    if (P(n) > 0.2) translate([c[3] - 10, c[4] - 2, 10]) pigtail(22);
  }
}
module concept_B() {
  color(BLK) difference() {                                             // tray
    fbox([BX, BY, B_WALL], 4);
    translate([B_T, B_T, B_FLOOR]) cube([BX - 2*B_T, BY - 2*B_T, B_WALL]);
  }
  color([0.45, 0.45, 0.5]) for (i = [1 : 28], j = [1 : 24])             // 10 mm M3 cheese grid (visual)
    translate([B_T + 1 + i * 10, B_T + 2 + j * 10, B_FLOOR - 0.3]) cylinder(d = 3.2, h = 0.5, $fn = 8);
  for (c = B_CARRIERS) b_carrier(c);
  translate([228, 104, B_FLOOR]) imu_datum();                           // on the rod-tied spine boss
  // lid: hinged on +Y, faceted, X-braced, mark
  translate([0, BY, B_WALL]) rotate([-112 * lid, 0, 0]) translate([0, -BY, 0]) {
    color(BLK) difference() {
      fbox([BX, BY, B_LID], 5);
      translate([B_T, B_T, -1]) cube([BX - 2*B_T, BY - 2*B_T, B_LID - 3]);
      for (i = [0, 1], j = [0, 1]) translate([80 + i * 140, 70 + j * 122, B_LID]) xbrace(124, 106);
    }
    color(YEL) translate([BX / 2, BY / 2, B_LID]) mark3d(40, 1.2);
    translate([BX / 2, 14, B_LID]) plate_label("CANARY T1", 90, 13);
    for (x = [30, BX - 30]) translate([x, -1, 14]) rotate([90, 0, 0]) thumb(13, 6);
  }
  // rod keel UNDER the tray (tube_platform lineage)
  for (x = [50, BX - 50]) for (s = [-1, 1]) translate([x, BY / 2 + s * TUBE_Y, -12]) rotate([180, 0, 0]) canon_cap();
  color(BLK) for (x = [50, BX - 50]) translate([x - 22, BY / 2 - 47, -12]) cube([44, 94, 12]);
  translate([0, BY / 2, -12]) rods(400, -50);
}

// =============================================================== CONCEPT C
C_PODS = [ // name, side(+1 top / -1 bottom), x0, length, height, component
  ["CORE",      1,   0, 112, 50, ORIN],
  ["BATTERY",   1, 118,  82, 74, [BAT[0], BAT[1], BAT[2]]],
  ["TRAFFIC",   1, 206,  64, 40, [FLY[1], FLY[0], FLY[2]]],
  ["IMU",       1, 276,  40, 0,  IMU],
  ["HUB",      -1,   0, 148, 46, HUB],
  ["RTK",      -1, 154,  52, 26, ZED],
  ["LTE",      -1, 212,  44, 26, [LTE[1], LTE[0], LTE[2]]],
  ["CABIN CO", -1, 262,  30, 26, [COS[1], COS[0], COS[2]]]];
C_W = 120;

module c_pod(p) {
  n = p[0]; s = p[1]; L = p[3]; H = p[4];
  translate([p[2], 0, s * (9 + 70 * P(n))]) mirror([0, 0, s < 0 ? 1 : 0]) {
    color(BLK) translate([0, -48, 0]) cube([L, 96, 7]);                 // canon plate base
    if (n == "IMU") translate([L / 2, 0, 7]) imu_datum();
    else {
      color(BLK) translate([0, -C_W / 2, 7]) difference() {
        fbox([L, C_W, H], 3);
        translate([L / 2, C_W / 2, H]) xbrace(L - 16, C_W - 30);
      }
      translate([L / 2, -C_W / 2 + 12, 7 + H]) plate_label(lbl(n == "HUB" ? "CORE" : n), min(L - 12, 50), 8);
      for (e = [10, L - 10]) for (y = [-42.5, 42.5]) translate([e, y, 7]) thumb(8, 5); // knurled cap screws
    }
    for (e = [10, L - 10]) for (y = [-1, 1]) translate([e, y * TUBE_Y, -9]) rotate([180, 0, 0])
      translate([0, 0, -9]) canon_cap();
    if (n != "IMU") translate([L / 2, -C_W / 2, 7 + min(H, 26) / 2]) rotate([0, 0, 180]) pigtail(P(n) > 0.2 ? 20 : 8);
  }
}
module concept_C() {
  for (p = C_PODS) c_pod(p);
  rods(400, -60);
  color(BLK) translate([-10, -C_W / 2 - 34, -9]) fbox([320, 16, 18], 2);   // harness trunk
  color(YEL) for (p = C_PODS) if (p[0] != "IMU")
    translate([p[2] + p[3] / 2, -C_W / 2 - 18, p[1] * 9]) rotate([90, 0, 0]) cylinder(d = 11.5, h = 3, center = true);
  color(YEL) translate([-10.2, -C_W / 2 - 26, 0]) rotate([90, 0, -90]) mark3d(14, 1);
}

if (concept == "A") concept_A();
if (concept == "B") concept_B();
if (concept == "C") concept_C();
if (concept == "D") concept_D();

// =============================================================== CONCEPT D
// 80/20 20-2020 (0.4411 g/mm, 6105-T5, I = 6826 mm4, slot 6.0 — FPE/AHP spec
// sheets) or Misumi HFS3-1515 (0.34 kg/m, AW-6061, I = 2800 mm4, slot 3.4 —
// Misumi catalogue p.659).  Members cut to length: the 281 mm bed rule and the
// 12 h plate rule no longer touch the structure.
//
// THE T-SLOT FINDING (why the rack looks like this): a T-slot is a track ALONG
// its member.  A front-loading drawer (sliding in Y) would need Y-direction
// runners per bay (+0.6 kg of 20-series for 5 bays) — so here the peripherals
// DROP IN FROM THE TOP between vertical MULLIONS, their side T-keys riding the
// mullions' facing slots (Z-direction track), retained by ONE captive M5
// thumbscrew into a T-nut in the mullion (metal-to-metal preload).  The battery
// slides in along X from the +X end on the bottom long members' inner slots.
// The rack face therefore has NO top rail (mullions cantilever 100 mm from the
// bottom rail: 0.045 mm at 65 N — the extrusion does not care); the frame's top
// plane closes 30 mm behind the faceplates.
E   = series == 20 ? 20 : 15;                     // profile
SLT = series == 20 ? 6.0 : 3.4;                   // slot opening
SLD = series == 20 ? 6.0 : 3.6;                   // slot depth
CAV = series == 20 ? 11.0 : 5.7;                  // cavity width (verify in the vendor CAD)
DX = 300; DY = 180; DZ = 140;                     // frame outer envelope (rods excluded)
TOPY = DY/2 - E/2 - 30;                           // top long members set back 30 behind each face
ANO = [0.15, 0.15, 0.17];
CART_H = DZ - 2*E - 4;                            // 96: drop-in cartridge height
D_FRONT = [["TRAFFIC", 74, [FLY[0], FLY[1], FLY[2]]], ["LTE", 84, [LTE[0], LTE[1], LTE[2]]], ["RTK", 62, ZED]];
D_REAR  = [["CABIN CO", 30, [COS[1], COS[0], COS[2]]], ["SPARE", 30, [0, 0, 0]]];   // + 160 exhaust louver
function bay_x(list, i) = E + (i == 0 ? 0 : bay_x(list, i - 1) - E + list[i - 1][1] + E);

module extrusion(len) {                            // T-slot member massing, along +X, centred on the axis
  color(ANO) difference() {
    translate([0, -E/2, -E/2]) cube([len, E, E]);
    for (r = [0, 90, 180, 270]) rotate([r, 0, 0]) {
      translate([-1, -SLT/2, E/2 - SLD]) cube([len + 2, SLT, SLD + 1]);
      translate([-1, -CAV/2, E/2 - SLD - 2.5]) cube([len + 2, CAV, 2.5]);
    }
    rotate([0, 90, 0]) translate([0, 0, -1]) cylinder(d = series == 20 ? 4.2 : 2.5, h = len + 2);
  }
}
module ext_y(len) rotate([0, 0, 90]) extrusion(len);     // along +Y
module ext_z(len) rotate([0, -90, 0]) extrusion(len);    // along +Z
module bracket() { color([0.5, 0.51, 0.55]) { cube([E - 2, E - 2, 3]); cube([E - 2, 3, E - 2]); } }  // 20-4119 class
module tkey(L) {                                   // printed ASA T-key along +Z: neck through the slot, head in the cavity
  color(BLK2) { translate([0, -(SLT - 0.4)/2, 0]) cube([SLD + 0.5, SLT - 0.4, L]);
                translate([SLD + 0.5 - 0.01, -(CAV - 0.6)/2, 0]) cube([2.0, CAV - 0.6, L]); }
}
module louver(w, h, txt) {                         // printed louvered insert: T-keys on its sides, drops into the mullion slots
  color(BLK) difference() {
    translate([-w/2, 0, 0]) cube([w, 4, h]);
    for (i = [1 : floor(h / 12) - 1]) translate([-w/2 + 8, -1, i * 12]) cube([w - 16, 6, 6]);
  }
  translate([-w/2, 2, 4]) rotate([0, 0, 180]) tkey(h - 8);
  translate([w/2, 2, 4]) tkey(h - 8);
  translate([0, -0.4, h - 9]) rotate([90, 0, 0]) plate_label(txt, min(w - 30, 44), 7);
}
module d_cartridge(b, x0, face) {                  // face = -1 front / +1 rear ; drop-in between mullions
  n = b[0]; w = b[1]; c = b[2]; d = 44; h = CART_H;
  translate([x0, face * (DY/2 - 1), E + 2 + (h + 30) * P(n)]) mirror([0, face > 0 ? 1 : 0, 0]) {
    color(BLK) fbox([w - 1, 5, h], 1.5);                                  // faceted faceplate (flush with the face)
    color(BLK2) translate([2, 5, 0]) cube([w - 5, d - 4, 3]);              // tray
    translate([0.5, 12, 4]) rotate([0, 0, 180]) tkey(h - 8);               // side T-keys -> mullion slots
    translate([w - 1.5, 12, 4]) tkey(h - 8);
    color(BLK2) translate([2 + (len(n) % 4) * 8, 5, 3]) cube([5, d - 8, 2]); // KEY rib (bay-specific)
    if (c[0] > 0) translate([(w - 1 - c[0]) / 2, 8, 3]) comp([c[0], min(c[1], d - 10), c[2]], PCB);
    translate([w - 10, 0, h - 14]) rotate([90, 0, 0]) thumb(10, 6);        // captive M5 -> T-nut in the mullion
    color(YEL) translate([6, -7, h - 18]) fbox([10, 8, 7], 1);            // pull tab
    if (n != "SPARE") translate([w/2, -0.4, h/2]) rotate([90, 0, 0]) plate_label(lbl(n), min(w - 20, 50), 9);
    if (P(n) > 0.2) translate([w/2, d, 20]) pigtail();
  }
}
module mlabel(txt, pos) { if (labels) color(YEL) translate(pos) rotate([90, 0, 0])
  linear_extrude(1) text(txt, size = 9, font = "DIN Condensed:style=Bold", halign = "center", valign = "center"); }
module concept_D() {
  // FIXED LAYOUT 2026-09-21: no top longs, no IMU cross -> the Core lifts straight out
  // between the two end ties (200 x 140) or slides out the -X end on the bottom longs'
  // inner slots (same track the battery uses at +X).  14 members.
  for (y = [-1, 1]) translate([0, y * (DY - E)/2, E/2]) extrusion(DX);                       // M01 M02
  for (x = [E/2, DX - E/2]) translate([x, -(DY - E)/2 + E, E/2]) ext_y(DY - 2*E);            // M03 M04
  for (x = [E/2, DX - E/2], y = [-1, 1]) translate([x, y * (DY - E)/2, E]) ext_z(DZ - 2*E);  // M05..M08
  for (x = [E/2, DX - E/2]) translate([x, -(DY - E)/2 + E, DZ - E/2]) ext_y(DY - 2*E);       // M09 M10 top end ties
  for (f = [-1, 1]) { L = f < 0 ? D_FRONT : D_REAR;                                          // M11..M14 mullions
    for (i = [1 : len(L) - (f < 0 ? 1 : 0)]) translate([bay_x(L, i) - E/2, f * (DY - E)/2, E]) ext_z(DZ - 2*E);
  }
  mlabel("M01", [DX/2, -DY/2 - 2, -14]); mlabel("M02", [DX/2, DY/2 + 22, -14]);
  mlabel("M03", [-16, -DY/2 - 2, E/2]); mlabel("M04", [DX + 16, -DY/2 - 2, E/2]);
  mlabel("M05", [-16, -DY/2 - 2, DZ/2]); mlabel("M06", [DX + 16, -DY/2 - 2, DZ/2]);
  mlabel("M07", [-16, DY/2 + 22, DZ/2]); mlabel("M08", [DX + 16, DY/2 + 22, DZ/2]);
  mlabel("M09", [-16, -DY/2 - 2, DZ + 12]); mlabel("M10", [DX + 16, -DY/2 - 2, DZ + 12]);
  mlabel("M11", [bay_x(D_FRONT, 1) - E/2, -DY/2 - 2, DZ + 6]); mlabel("M12", [bay_x(D_FRONT, 2) - E/2, -DY/2 - 2, DZ + 6]);
  mlabel("M13", [bay_x(D_REAR, 1) - E/2, DY/2 + 22, DZ + 6]); mlabel("M14", [bay_x(D_REAR, 2) - E/2, DY/2 + 22, DZ + 6]);
  for (x = [E, DX - E], y = [-1, 1]) translate([x, y * (DY/2 - E), E])
    mirror([x > E ? 1 : 0, 0, 0]) mirror([0, y > 0 ? 1 : 0, 0]) bracket();
  // ---- Core: END-LOADING tray from -X on the bottom longs' inner slots (T-keys), 2 x M5 into T-nuts in the posts
  translate([E + 2 - (HUB[0] + 60) * P("CORE"), -HUB[1]/2 - 4, E + 4]) {
    color(BLK2) translate([0, 0, -2]) cube([HUB[0] + 12, HUB[1] + 8, 2]);
    color(BLK) translate([-6, -4, -4]) fbox([6, HUB[1] + 16, 96], 1.5);                     // faceted end bezel = intake louver frame
    translate([6, 4, 0]) { color(MET) cube(HUB); translate([12, 4, HUB[2] + 6]) comp(ORIN, PCB); }
    translate([-6, HUB[1]/2 + 4, 80]) rotate([0, -90, 0]) thumb(11, 6);
    translate([-6.2, HUB[1]/2 + 4, 20]) rotate([90, 0, -90]) plate_label(lbl("CORE"), 60, 9);
  }
  color(MET) translate([DX - E - 70, -20, E + 4]) cube(PDB);
  // ---- battery: slides in along X from the +X end on the same track; latch + strap
  translate([DX - E - 2 + (BAT[0] + 40) * P("BATTERY"), -BAT[1]/2, E + 4]) {
    color(BLK) translate([0, -4, -2]) fbox([6, BAT[1] + 8, BAT[2] + 14], 1.5);
    color(BLK2) translate([-BAT[0] - 4, -2, -2]) cube([BAT[0] + 4, BAT[1] + 4, 2]);
    color(MET) translate([-BAT[0], 0, 0]) cube(BAT);
    translate([6, BAT[1]/2, BAT[2]/2]) rotate([0, 90, 0]) thumb(11, 6);
    color(YEL) translate([-BAT[0] - 2, 10, BAT[2] + 1]) cube([BAT[0] + 8, 14, 3]);
    translate([6.2, BAT[1]/2, BAT[2] - 4]) rotate([90, 0, 90]) plate_label(lbl("BATTERY"), 50, 9);
  }
  for (i = [0 : len(D_FRONT) - 1]) d_cartridge(D_FRONT[i], bay_x(D_FRONT, i), -1);
  for (i = [0 : len(D_REAR) - 1]) d_cartridge(D_REAR[i], bay_x(D_REAR, i), 1);
  // ---- louvered exhaust insert (rear, drops into the last rear bay); intake = the Core end bezel + open top
  translate([bay_x(D_REAR, 2) + 80, DY/2 - 1, E + 2 + (DZ + 20) * panel]) mirror([0, 1, 0]) louver(160 - 2, CART_H, "EXHAUST");
  // ---- rods: Al yoke plates ON the end ties (M09/M10), canon caps; rear plate carries the IMU datum
  for (x = [E/2, DX - E/2]) translate([x, 0, DZ]) {
    color([0.55, 0.56, 0.6]) translate([x > E ? -50 : -14, -DY/2 + E, 0]) cube([64, DY - 2*E, 5]);   // Al plate, rear one 64 wide
    for (y = [-1, 1]) { translate([0, y * TUBE_Y, 5 + 11]) canon_cap(); translate([0, y * (DY/2 - E - 6), 5]) thumb(9, 5); }
  }
  translate([0, 0, DZ + 5 + 11 + 7.7]) rods(400, -50);
  translate([DX - E/2 - 30, 0, DZ + 5]) imu_datum();                                          // keyed pocket in the rear Al yoke plate
  color(YEL) translate([DX - 14, -DY/2 - 0.2, DZ - E - 8]) rotate([90, 0, 0]) mark3d(14, 1);
}
