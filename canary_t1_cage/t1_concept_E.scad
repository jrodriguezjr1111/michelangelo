// ============================================================================
// CONCEPT E — SINGLE-LEVEL DECK on the owner's existing 2020 rectangle
// (2026-09-24 direction; supersedes the concept-D box for the T1 cage).
// Massing model.  Reuses t1_concepts.scad primitives without editing it.
//
// What exists on the floor: 406 x 279 outer (16 x 11 in) black 2020 frame, four
// flat corner gussets, one centre cross member on flat T-gussets -> two bays
// 173 x 239 clear.  Everything below is drawn ON that; the four 100 mm posts,
// the two yoke bridges and the rods are the added "antenna level".
//
// Frame: X = 406 (long, LATERAL in the aircraft = along the lap belt), Y = 279
// (fore-aft, +Y = nose), Z up, z = 0 deck underside, member tops at z = 20.
// view = "top" | "iso" | "lift" | "cables" | rev C: "elev" | "marker"
// ============================================================================
include <t1_concepts.scad>
concept = "none"; swap = "none"; pull = 0; lid = 0; panel = 0; labels = false; show_labels = true;
side_rails = false;              // rev C option: two side rails at antenna mid-height
view = "iso";
rev = "B";                       // "A" = 2026-09-25 first pass | "B" = connector-aware (photos 21-32) | "C" = B + full-height cage (top rectangle)
lift = 90;                        // mm the bay-R tray is lifted in view "lift"
mkid = 1;                         // view "marker": which elevation marker to draw alone
$fn = 32;

DXE = 406; DYE = 279;             // MEAS (owner's frame, cut from stock)
BAY = (DXE - 3*E) / 2;            // 173 clear per bay
CX0 = E + BAY;                    // centre member x = 193..213
T_SKIN = 4; T_RIB = 9;            // tray: 4 mm skin on the member tops, 9 mm ribs hanging into the bay
STD = 6;                          // component standoff
YOKE_T = 10;
YOKE_Z0 = 100;                    // yoke bridges at z = E + 3 + 100 in every rev (antenna level unchanged)
DOME_D = 150; DOME_H = 60; DOME_PC = 35;   // EST from photos 27/30: O150 x 60 survey dome, phase centre 35 above its base
PUCK_H = 30;                      // dome puck rod-mount (to design)
TOP_CLR = 15;                     // rev C: antenna tops at least this far below the top of the top rails
ROD_ZC = E + 3 + YOKE_Z0 + YOKE_T + 11 + 7.7;                       // 151.7 (E = 20)  == t1_params.ROD_Z
DOME_TOP = ROD_ZC + 7.7 + PUCK_H + DOME_H;                          // 249.4
// rev C post: the SHORTEST whole-mm post that keeps the dome top TOP_CLR under the top-rail top.
// Every extra mm of post raises the rails over the dome phase centre and worsens the GNSS mask
// (atan(h/d)), so no rounding up to 10: 221.4 -> 222 -> top rail top z 265.  (The 220/263 in the
// first rev C note came from a stale 148.7 rod-axis comment; 220 would leave the dome 13.6 under.)
POST_H = rev == "C" ? ceil(DOME_TOP + TOP_CLR - E - (E + 3)) : 100;   // rev C: 222
TOP_Z0 = E + 3 + POST_H;          // rev C top rectangle underside (245)
TOP_TOP = TOP_Z0 + E;             // rev C top-rail top (265); flat gussets on top -> 268 overall
ROD_Z = ROD_ZC;                  // rod axis (canon cap on the bridge), same in B and C
// ---- rev C rod level (mirrors t1_params.ROD_LEVEL_C / MA963 / DOME).  The real MA963 is NOT the
// 110 x 90 x 12 slab drawn in rev B: antenna 146.37 (along the rods) x 133.95 x 20.04 on the
// CW-ANT-005 rev C plate 173 x 180 x 7 (underside 12 above the rod axis, corner clamps 23.24 over
// the plate).  Dome 150 + plate 173 + CO tray 138 cannot share 326 mm of rod side by side, so rev C
// uses height: the dome and MA963 sit ON the rods, the CO tray hangs UNDER them.
MA_CX = 107;  MA_PL = [173, 180, 7];  MA_ANT = [146.37, 133.95, 20.04];  MA_CLH = 23.24;  MA_STD = 12;
MA_HALF = 90;                      // clamp outer corners, half length along the rods (plate 86.5)
DOME_CX = rev == "C" ? 277 : 120;
CO_CAP = 225;                      // CO tray tube plate cap station x (tray hangs below, tail +X)
WHIPS_C = [[374, 50], [374, 229]]; // 1090 / 978 stubbies on the RIGHT yoke bridge, clear of rods + dome
WHIP_H = 40; WHIP_BASE = E + 3 + YOKE_Z0 + YOKE_T + 8;                       // bridge top + SMA bracket = 141
MA_TOP = ROD_ZC + MA_STD + MA_PL[2] + MA_CLH;                                 // clamp tops 193.94
MA_ANT_TOP = ROD_ZC + MA_STD + MA_PL[2] + MA_ANT[2];                          // radome top 190.74
MA_RC = ROD_ZC + MA_STD + MA_PL[2] + MA_ANT[2] / 2;                          // radiating-element reference (mid-housing)
DOME_PCZ = ROD_ZC + 7.7 + PUCK_H + DOME_PC;                                  // 224.4
BAT_TOP = E + T_SKIN + 10 + 64;                                              // 98: battery on its V-plate
EXIT_LIFT = 12;                    // tray lift to clear the long member + ribs before sliding out a side window
BELT = [100, 172];                // lap-belt band, y range (the battery stands in it)
STRAP_X = [100, 306];             // fore-aft cargo-strap loops round the long members (tray cut-outs)

// ---- roster 2026-09-24 (MEAS / PUB / EST per t1_params.py)
MTI = rev != "A" ? [53.3, 68.6, 14] : [43.5, 34, 12];   // rev B: MTi-3 DEV BOARD = Arduino-Uno shield 68.6 x 53.3 (photo 32), long axis along deck Y (board +X -> nose)
LTEB = [90, 30, 14];              // rev B: EG25-G mini-PCIe->USB carrier ~90 x 30 (photo 22, scaled on the 30 mm mini-PCIe width), posts 70.80 x 24.21 MEAS
FLYC = [64.93, 56.03, 27];        // Nooelec FlyCatcher, Pi-HAT outline, holes 58 x 49 (MEAS); datasheet 76 x 57 x 19 incl. SMAs
VPL = [100, 80, 10];              // EST_ V-mount female plate with D-Tap (COTS)
PDBE = [60, 40, 20];              // EST_ fused PDB + INA219

// placement table: name, [x, y] min corner (deck coords), envelope [L, W, H], label, colour
PLACE = [
  ["BATTERY", [28, 99],  BAT[1] > BAT[0] ? [BAT[1], BAT[0], BAT[2]] : BAT, "POWER", MET],   // 107 x 74 x 64 lying on the V-plate
  ["VPLATE",  [32, 96],  VPL, "", ALU],
  ["PDB",     [30, 52],  PDBE, "PDB", MET],
  ["CO",      [40, 22],  COS, "CABIN CO", PCB],                                                // 114 x 21 at the FRONT edge (cabin air)
  ["LTE",     [90, 215], LTE, "LTE", PCB],                                                      // rear edge, under the LTE feed
  ["MTI",     [22, 225], MTI, "IMU", PCB],                                                      // on the rear-left CORNER PLATE (metal), not a tray
  ["HUB",     [216, 20], HUB, "CANARY CORE", MET],                                              // cable node, against the centre member
  ["RTK",     [216, 100], ZED, "RTK", PCB],
  ["FLYC",    [216, 176], FLYC, "TRAFFIC", PCB],
  ["ORIN",    [284, 176], ORIN, "", PCB],                                                       // fan up, nothing above it
];
// rev B: name, [x,y], env, label, colour, connector glyphs [[edge, tag], ...]  edge = N(+Y) S(-Y) E(+X) W(-X) NW/NE/SW/SE corner
PLACE_B = [
  ["BATTERY", [28, 99],  [107, 74, 64], "POWER", MET, [["S", "D-TAP"]]],                      // outputs on the pack's short end -> faces the PDB
  ["VPLATE",  [32, 96],  VPL, "", ALU, []],
  ["PDB",     [118, 42], PDBE, "PDB", MET, [["E", "DC OUT"], ["N", "IN"]]],                   // moved to the centre member: hub DC crosses it in 60 mm
  ["LTE",     [95, 222], LTEB, "LTE", PCB, [["E", "USB-A"], ["W", "u.FL"]]],                  // along X at the rear edge: USB end -> centre member, u.FL end -> rear-left post
  ["MTI",     [24, 198], MTI, "IMU", PCB, [["S", "uUSB"]]],                                    // Uno shield on the corner Al plate, board +X = deck +Y (nose), micro-USB on the board's -X end = deck S
  ["HUB",     [216, 20], HUB, "CANARY CORE", MET, [["W", "HOST+DC"], ["N", "P1 P2 P3 P4"]]],   // photo 29: host + green DC block on the SHORT end; downstream on the long face; p1 nearest the host end
  ["FLYC",    [216, 112], FLYC, "TRAFFIC", PCB, [["S", "uUSB x2"], ["N", "SMA x2"]]],          // micro-USBs face the hub's p1/p2, SMAs face the rear post  (edge assignment: CONFIRM)
  ["RTK",     [216, 200], ZED, "RTK", PCB, [["E", "USB-C"], ["NW", "u.FL"]]],                  // USB-C edge faces the Orin, antenna corner faces the rear-left slot run
  ["ORIN",    [284, 176], ORIN, "", PCB, [["S", "USB / DC / ETH"]]],                            // connector edge faces the hub channel (y 107-176)
];
function P_(n) = [for (p = (rev != "A" ? PLACE_B : PLACE)) if (p[0] == n) p][0];
function PL() = rev != "A" ? PLACE_B : PLACE;

// ------------------------------------------------------------------ frame that exists
module deck_frame() {
  for (y = [E/2, DYE - E/2]) translate([0, y, E/2]) extrusion(DXE);                    // long members (belt/strap members)
  for (x = [E/2, DXE - E/2]) translate([x, E, E/2]) ext_y(DYE - 2*E);                  // end members
  translate([CX0 + E/2, E, E/2]) ext_y(DYE - 2*E);                                     // centre member (on T-gussets)
  color([0.5, 0.51, 0.55]) for (c = [[0, 0], [DXE - 60, 0], [0, DYE - 60], [DXE - 60, DYE - 60]])   // owner's flat corner gussets, 60 x 60 L
    translate([c[0], c[1], E]) difference() { cube([60, 60, 3]); translate([20, 20, -1]) cube([40, 40, 5]); }
  color([0.5, 0.51, 0.55]) for (y = [0, DYE - 20]) translate([CX0 - 20, y, E]) cube([60, 20, 3]);   // flat T-gussets at the centre member
}
module posts_and_rods() {                                                                 // added antenna level
  if (rev == "C") cage_C(); else posts_and_rods_AB();
}
// ------------------------------------------------------------------ rev C: full-height cage
module cage_C() {
  for (x = [E/2, DXE - E/2], y = [E/2, DYE - E/2]) translate([x, y, E + 3]) ext_z(POST_H);  // 4 posts, 222
  for (y = [E/2, DYE - E/2]) translate([0, y, TOP_Z0 + E/2]) extrusion(DXE);              // top long rails 406 (on the posts)
  for (x = [E/2, DXE - E/2]) translate([x, E, TOP_Z0 + E/2]) ext_y(DYE - 2*E);            // top end rails 239 (between the longs)
  color([0.5, 0.51, 0.55]) for (c = [[0, 0], [DXE - 60, 0], [0, DYE - 60], [DXE - 60, DYE - 60]])
    translate([c[0], c[1], TOP_TOP]) difference() { cube([60, 60, 3]); translate([20, 20, -1]) cube([40, 40, 5]); }   // flat corner gussets, 20-4081 class
  color([0.5, 0.51, 0.55]) for (mx = [0, 1], my = [0, 1])                                  // 20-4119 at each post top, both planes
    translate([mx * DXE, my * DYE, 0]) mirror([mx, 0, 0]) mirror([0, my, 0]) {
      translate([E, 1, TOP_Z0 - 18]) cube([3, 18, 18]);  translate([E, 1, TOP_Z0 - 3]) cube([18, 18, 3]);   // post -> top long rail
      translate([1, E, TOP_Z0 - 18]) cube([18, 3, 18]);  translate([1, E, TOP_Z0 - 3]) cube([18, 18, 3]);   // post -> top end rail
    }
  if (side_rails) for (y = [E/2, DYE - E/2]) translate([0, y, ROD_Z + 50]) extrusion(DXE);   // OPTION: side rails at antenna mid-height
  // yoke bridges: printed ASA 40 x 239 x 10, BETWEEN each post pair, 2 x M5 + T-nut into each post's inner slot
  // (same z as rev B, so the antenna level and every coax length below it are unchanged)
  for (x = [0, DXE - 40]) translate([x, E, E + 3 + YOKE_Z0]) color(BLK) fbox([40, DYE - 2*E, YOKE_T], 2);
  for (x = [20, DXE - 20], y = [DYE/2 - 30, DYE/2 + 30]) translate([x, y, ROD_Z]) canon_cap();   // yoke caps ON the rod axis
  translate([0, DYE/2, ROD_Z]) rods(400, 3);
  // MA963 on the CW-ANT-005 rev C plate (left), cable tongue toward +Y (rear posts)
  translate([MA_CX, DYE/2, ROD_Z + MA_STD]) {
    color(BLK2) translate([-MA_PL[0]/2, -88, 0]) cube([MA_PL[0], MA_PL[1], MA_PL[2]]);
    color(BLK) translate([-MA_ANT[0]/2, -MA_ANT[1]/2, MA_PL[2]]) cube([MA_ANT[0], MA_ANT[1], MA_ANT[2]]);
    color(YEL) for (sx = [-1, 1], sy = [-1, 1]) translate([sx * (MA_HALF - 8) - 8, sy * (MA_ANT[1]/2 + 2) - 8, MA_PL[2]]) cube([16, 16, MA_CLH]);   // corner clamps
    color(BLK2) for (sx = [-1, 1], sy = [-1, 1]) translate([sx * 52 - 23, sy * 30 - 17, -MA_STD]) cube([46, 34, MA_STD]);                    // stations
  }
  for (sx = [-1, 1], sy = [-1, 1]) translate([MA_CX + sx * 52, DYE/2 + sy * 30, ROD_Z]) rotate([180, 0, 0]) canon_cap();                  // its caps UNDER the rods
  // GNSS dome on its puck (right)
  color(BLK) translate([DOME_CX, DYE/2, ROD_Z + 7.7]) cylinder(d = 40, h = PUCK_H);
  color([0.95, 0.95, 0.93]) translate([DOME_CX, DYE/2, ROD_Z + 7.7 + PUCK_H]) cylinder(d = DOME_D, h = DOME_H, $fn = 72);
  // CO tray tube plate (co_sensor rev C) hung UNDER the rods, tray below it, tail +X; its caps above the rods
  translate([CO_CAP, DYE/2, ROD_Z]) {
    color(BLK) translate([-32, -47.5, -19]) cube([64, 95, 7]);
    color(BLK2) translate([-70, -13.11, -19 - 25.62]) cube([125.6, 26.22, 25.62]);
    color(BLK2) translate([55.6, -8, -19 - 20]) cube([12, 16, 12]);
    for (sy = [-30, 30]) translate([0, sy, 0]) canon_cap();
  }
  // 1090 / 978 stubbies (<= 40) on the right yoke bridge
  color(BLK) for (q = WHIPS_C) translate([q[0], q[1], WHIP_BASE - 8]) { cube([14, 14, 8], center = false); translate([7, 7, 8]) cylinder(d = 10, h = WHIP_H); }
}
module posts_and_rods_AB() {
  for (x = [E/2, DXE - E/2], y = [E/2, DYE - E/2]) translate([x, y, E + 3]) ext_z(POST_H);
  for (x = [0, DXE - 40]) translate([x, 0, E + 3 + YOKE_Z0]) {                             // printed yoke bridges (ASA), canon cap stations
    color(BLK) difference() { fbox([40, DYE, YOKE_T], 2); for (y = [DYE/2 - 30, DYE/2 + 30]) translate([20, y, YOKE_T - 6]) cylinder(d = 15.4, h = 8); }
    for (y = [DYE/2 - 30, DYE/2 + 30]) translate([20, y, YOKE_T + 11 - 1]) canon_cap();
    for (y = [DYE/2 - 30, DYE/2 + 30]) translate([20, y, YOKE_T + 11 + 7.7]) {}
  }
  translate([0, DYE/2, ROD_Z]) rods(400, 3);
  if (rev != "A") {
    color(ALU) translate([205, DYE/2 - 45, ROD_Z + 7.7 + 6]) cube([110, 90, 12]);         // MA963 Guardian plate (taoglas_ma963, arrow = cable exit)
    color([0.95, 0.95, 0.93]) translate([120, DYE/2, ROD_Z + 7.7 + PUCK_H]) cylinder(d = DOME_D, h = DOME_H);   // white L1/L2 GNSS dome EST O150 x 60 on a NEW puck rod-mount
    color(BLK) translate([120, DYE/2, ROD_Z + 7.7]) cylinder(d = 40, h = PUCK_H);         // dome puck mount (5/8-11) - to design
    color(BLK) translate([322, DYE/2 - 20, ROD_Z - 22]) cube([40, 40, 60]);              // existing CO tray tube plate (co_sensor, photo 31), vents outboard
    color(BLK) for (q = [[20, DYE/2 - 30], [DXE - 20, DYE/2 + 30]]) translate([q[0], q[1], ROD_Z + 12]) cylinder(d = 10, h = 100);   // 1090 / 978 whips on the yoke bridges
  } else {
    color(ALU) translate([DXE/2 - 55, DYE/2 - 45, ROD_Z + 7.7 + 6]) cube([110, 90, 12]);
    color(BLK) for (x = [60, 346]) translate([x, DYE/2 - 30, ROD_Z + 7.7]) cylinder(d = 14, h = 30);
  }
}
// ------------------------------------------------------------------ trays (printed ASA, castellated ears)
module tray(x0, w, lifted = 0) {                                                          // full-bay tray: skin on the member tops + ribs
  translate([0, 0, lifted]) {
    color(BLK) difference() {
      union() {
        translate([x0 - 10, E - 10, E]) cube([w + 20, DYE - 2*E + 20, T_SKIN]);            // skin + 10 mm flange on every member (faceplate rule)
        for (i = [0 : 3]) translate([x0 + 6 + i * (w - 12) / 3 - 0.8, E, E - T_RIB]) cube([1.6, DYE - 2*E, T_RIB]);   // Y ribs
        for (j = [0 : 3]) translate([x0, E + 6 + j * (DYE - 2*E - 12) / 3 - 0.8, E - T_RIB]) cube([w, 1.6, T_RIB]);  // X ribs
      }
      for (sx = STRAP_X) if (sx > x0 && sx < x0 + w) translate([sx - 15, E - 12, E - 1]) cube([30, DYE - 2*E + 24, T_SKIN + 2]);  // strap slots
      for (y = [E, DYE - E - 10]) for (k = [0 : 2]) translate([x0 + 20 + k * (w - 40) / 2, y - 5 + (y > E ? 10 : -0) , E - 1]) cylinder(d = 5.4, h = 8);  // M5 ears (bolt line)
      translate([x0 + w/2, DYE/2, E + T_SKIN - 1]) for (i = [-1, 1]) rotate([0, 0, i * 45]) translate([-w * 0.7, -2.5, 0]) cube([w * 1.4, 5, 3]);  // X-brace pocket
    }
    for (k = [0 : 2], y = [E - 5, DYE - E + 5]) translate([x0 + 20 + k * (w - 40) / 2, y, E + T_SKIN]) thumb(9, 5);   // captive M5 thumbscrews -> T-nuts
  }
}
module component(p, dz = 0) {
  n = p[0]; o = p[1]; c = p[2]; lab = p[3]; col = p[4];
  z0 = (n == "MTI") ? E + 3 + 3 : E + T_SKIN;                                              // MTi on the 3 mm corner plate + 3 mm standoffs
  translate([o[0], o[1], z0 + dz]) {
    if (n == "BATTERY") color(col) cube(c);
    else if (n == "VPLATE") color(col) cube(c);
    else if (n == "MTI") { for (sx = [-1, 1], sy = [-1, 1]) translate([c[0]/2 + 8.5 - 43.5/2 + 23/2 + sx * 23/2, c[1]/2 + sy * 28/2, 0]) color([0.85,0.75,0.3]) cylinder(d = 5, h = 3, $fn = 6);
                          translate([0, 0, 3]) comp(c, col); color(YEL) translate([c[0]/2 - 4, c[1] - 4, 3 + 2.1]) rotate([0,0,90]) linear_extrude(0.6) polygon([[0,0],[6,3],[0,6]]); }   // arrow -> +Y (nose)
    else { for (sx = [0, 1], sy = [0, 1]) translate([4 + sx * (c[0] - 8), 4 + sy * (c[1] - 8), 0]) color([0.85,0.75,0.3]) cylinder(d = 5, h = STD, $fn = 6);
           translate([0, 0, STD]) comp(c, col); }
    if (lab != "") translate([c[0]/2, -0.5, min(c[2], 30)/2 + (n == "MTI" ? 3 : STD)]) rotate([90, 0, 0]) plate_label(lab, min(c[0] - 10, 60), 8);
    if (rev != "A" && len(p) > 5) for (g = p[5]) glyph(g[0], c);                          // connector-direction wedges
  }
}
module glyph(edge, c) {                                                                   // yellow wedge pointing OUT of the connector edge, drawn above the part
  zt = c[2] + STD + 4;
  pos = edge == "N" ? [c[0]/2, c[1], 0] : edge == "S" ? [c[0]/2, 0, 180] : edge == "E" ? [c[0], c[1]/2, -90] : edge == "W" ? [0, c[1]/2, 90]
      : edge == "NW" ? [0, c[1], 45] : edge == "NE" ? [c[0], c[1], -45] : edge == "SW" ? [0, 0, 135] : [c[0], 0, -135];
  color(YEL) translate([pos[0], pos[1], zt]) rotate([0, 0, pos[2]]) linear_extrude(2) polygon([[-6, 0], [6, 0], [0, 10]]);
}
module corner_imu_plate() { color(ALU) if (rev != "A") translate([E, DYE - E - 72, E]) cube([62, 72, 3]); else translate([E, DYE - E - 50, E]) cube([56, 50, 3]); }  // Al plate on the rear-left corner members' top slots (2 x M5 T-nuts + gusset bolts)

// cable runs: [name, colour, [points...]] in deck coords (z = top of members unless noted)
ZC = E + T_SKIN + 2; ZS = E + 10;   // on-tray comb height / inside the outer side slot (member mid-height)
CABLES = [
  ["USB hub->Orin (A-B, hub side 15 N)",      [0.2, 0.6, 1.0], [[300, 105, ZC + 30], [300, 150, ZC + 20], [320, 176, ZC + 20]]],
  ["USB FlyCatcher x2 -> hub p1/p2",          [0.2, 0.6, 1.0], [[250, 176, ZC + 12], [250, 140, ZC + 12], [250, 107, ZC + 20]]],
  ["USB CO stick -> hub p3",                  [0.2, 0.6, 1.0], [[154, 32, ZC + 6], [200, 32, ZS], [216, 32, ZC + 12]]],
  ["USB vib bulkhead (front face) -> hub p4", [0.2, 0.6, 1.0], [[330, 8, ZS], [330, 20, ZC + 12]]],
  ["USB LTE -> Orin",                         [0.2, 0.6, 1.0], [[170, 232, ZC + 8], [200, 232, ZS], [284, 232, ZC + 14]]],
  ["USB RTK -> Orin",                         [0.2, 0.6, 1.0], [[238, 143, ZC + 8], [284, 200, ZC + 14]]],
  ["USB MTi-3 (micro) -> Orin",               [0.2, 0.6, 1.0], [[66, 242, ZC + 6], [130, 260, ZS], [284, 250, ZC + 14]]],
  ["DC V-plate D-Tap -> PDB",                 [1.0, 0.3, 0.2], [[80, 96, ZC + 8], [60, 92, ZC + 8]]],
  ["DC PDB -> Orin barrel (fused 3 A)",       [1.0, 0.3, 0.2], [[90, 60, ZC + 8], [193, 60, ZS], [213, 60, ZS], [284, 180, ZC + 8]]],
  ["DC PDB -> hub 10-30 V (fused 2 A)",       [1.0, 0.3, 0.2], [[90, 70, ZC + 8], [193, 70, ZS], [216, 70, ZC + 8]]],
  ["coax LTE -> rod level (SMA, loop)",       [0.9, 0.8, 0.1], [[100, 250, ZC + 8], [30, 265, ZS], [10, 265, E + 60], [10, DYE/2 - 30, ROD_Z + 8], [60, DYE/2 - 30, ROD_Z + 8]]],
  ["coax RTK -> rod level (SMA, loop)",       [0.9, 0.8, 0.1], [[238, 143, ZC + 10], [238, 265, ZS], [396, 265, E + 60], [396, DYE/2 + 30, ROD_Z + 8], [346, DYE/2 + 30, ROD_Z + 8]]],
  ["coax 1090 + 978 -> MA963 / whip (rear post)", [0.9, 0.8, 0.1], [[281, 200, ZC + 10], [281, 265, ZS], [396, 265, E + 60], [396, DYE/2, ROD_Z + 20]]],
];
CABLES_B = [
  ["USB-1 Orin -> hub HOST (W end)",         [0.2, 0.6, 1.0], [[292, 176, ZC + 20], [292, 140, ZC + 12], [214, 140, ZC + 12], [212, 60, ZC + 12]]],
  ["USB-2/3 FlyCatcher uUSB (S edge) -> p1/p2 (N face)", [0.2, 0.6, 1.0], [[240, 112, ZC + 12], [240, 108, ZC + 20]]],
  ["USB-4 CO tray (rod level, front-right) -> p3",  [0.2, 0.6, 1.0], [[340, DYE/2 - 30, ROD_Z - 10], [396, 14, ROD_Z - 20], [396, 14, E + 30], [330, 108, ZC + 20]]],
  ["USB-5 vib bulkhead (front face) -> p4",  [0.2, 0.6, 1.0], [[360, 8, ZS], [350, 108, ZC + 20]]],
  ["USB-6 LTE carrier USB-A (E end) -> Orin",[0.2, 0.6, 1.0], [[186, 237, ZC + 8], [200, 237, ZS], [212, 237, ZS], [292, 176, ZC + 14]]],
  ["USB-7 RTK USB-C (E edge) -> Orin",       [0.2, 0.6, 1.0], [[260, 222, ZC + 8], [300, 176, ZC + 14]]],
  ["USB-8 MTi uUSB (S edge) -> Orin",        [0.2, 0.6, 1.0], [[50, 196, ZC + 6], [50, 150, ZC + 6], [190, 150, ZS], [212, 150, ZS], [292, 176, ZC + 14]]],
  ["DC-1 battery D-Tap (S end) -> PDB IN",   [1.0, 0.3, 0.2], [[80, 99, ZC + 30], [118, 82, ZC + 8]]],
  ["DC-2 PDB -> Orin barrel (S edge)",       [1.0, 0.3, 0.2], [[178, 62, ZC + 8], [200, 62, ZS], [212, 62, ZS], [212, 150, ZS], [300, 176, ZC + 8]]],
  ["DC-3 PDB -> hub DC block (W end)",       [1.0, 0.3, 0.2], [[178, 50, ZC + 8], [212, 50, ZC + 8]]],
  ["RF-1 LTE u.FL (W end) -> rear-left post -> MA963 LTE", [0.9, 0.8, 0.1], [[95, 237, ZC + 8], [30, 265, ZS], [10, 265, E + 60], [10, DYE/2 - 30, ROD_Z + 8], [220, DYE/2 - 30, ROD_Z + 8]]],
  ["RF-2 RTK u.FL (NW corner) -> rear-left post -> GNSS dome", [0.9, 0.8, 0.1], [[216, 243, ZC + 10], [30, 265, ZS], [10, 265, E + 60], [10, DYE/2 + 30, ROD_Z + 8], [120, DYE/2 + 30, ROD_Z + 20]]],
  ["RF-3/4 FlyCatcher SMAs (N edge) -> rear-right post -> whips", [0.9, 0.8, 0.1], [[250, 170, ZC + 10], [250, 265, ZS], [396, 265, E + 60], [396, DYE/2 + 30, ROD_Z + 8]]],
];
module tube(pts, col) color(col) for (i = [0 : len(pts) - 2]) hull() { translate(pts[i]) sphere(2.2, $fn = 10); translate(pts[i + 1]) sphere(2.2, $fn = 10); }
module dim(txt, at, rot = 0) color(YEL) translate([at[0], at[1], E + 100]) rotate([0, 0, rot]) linear_extrude(0.6)
  text(txt, size = 7, font = "DIN Condensed:style=Bold", halign = "center", valign = "center");

// ------------------------------------------------------------------ scenes
module assembly(lift_R = 0, with_rods = true) {
  deck_frame(); corner_imu_plate();
  tray(E, BAY); tray(CX0 + E, BAY, lift_R);
  for (p = PL()) component(p, (p[1][0] > CX0) ? lift_R : 0);
  if (with_rods) posts_and_rods();
  // front-face bulkheads on the bay-R front member: vib USB + DC service (panel-mount, locking)
  color(MET) for (x = [330, 360]) translate([x, -3, E + 10]) rotate([-90, 0, 0]) cylinder(d = 12, h = 3);
  color(YEL) translate([DXE - 14, -0.2, E - 4]) rotate([90, 0, 0]) mark3d(12, 1);
}
if (view == "iso") assembly();
if (view == "lift") assembly(lift_R = lift);
if (view == "cables") { assembly(with_rods = true); for (c = (rev != "A" ? CABLES_B : CABLES)) tube(c[2], c[1]); }
if (view == "top") {
  assembly(with_rods = false);
  if (rev != "A") for (c = CABLES_B) tube([for (q = c[2]) [q[0], q[1], E + 92]], c[1]);   // runs drawn on the top view
  color(YEL) for (y = BELT) translate([0, y - 1, E + 95]) cube([DXE, 2, 1]);                                 // lap-belt band edges
  color(YEL) for (sx = STRAP_X, dx = [-15, 13]) translate([sx + dx, 0, E + 95]) cube([2, DYE, 1]);            // strap loop edges
  dim(str(DXE, " x ", DYE, " OUTER   BAYS ", BAY, " x ", DYE - 2*E), [DXE/2, -16]);
  dim("BELT BAND y100-172", [DXE/2, BELT[0] - 8]);
  dim("STRAP", [STRAP_X[0], DYE + 10]); dim("STRAP", [STRAP_X[1], DYE + 10]);
  dim("+Y = NOSE", [DXE + 24, DYE/2], 90);
  if (rev != "A") dim("REV B - CONNECTOR-AWARE; WEDGE = CONNECTOR EDGE; BLUE USB / RED DC / YELLOW COAX", [DXE/2, -30]);
  for (p = PL()) if (p[0] != "VPLATE") dim(str(p[0], " ", p[2][0], "x", p[2][1], " @", p[1][0], ",", p[1][1]), [p[1][0] + p[2][0]/2, p[1][1] + p[2][1] + 6]);
}

// ------------------------------------------------------------------ rev C design checks (echo + assert)
// Mask angle to a top rail = atan(height of the rail's TOP inner edge above the reference point /
// horizontal distance to the rail's inner face).  The rail's bottom outer edge gives the lower edge
// of its shadow band (the sides are open, so a rail shadows a band, not everything below it).
function mask(h, d) = atan(h / d);
RAILS_C = [["y=0 long (front face)", DYE/2 - E], ["y=279 long (rear face)", DYE/2 - E],
           ["x=0 end", 0], ["x=406 end", 0]];
function d_in(i, cx) = i < 2 ? DYE/2 - E : (i == 2 ? cx - E : DXE - E - cx);
if (rev == "C") {
  echo(str("REV C CAGE: posts ", POST_H, " (4 x 20-2020), top rectangle underside z ", TOP_Z0, ", top-rail top z ", TOP_TOP,
           ", overall ", TOP_TOP + 3, " incl. flat gussets; footprint ", DXE, " x ", DYE));
  echo(str("TOPS vs top-rail top ", TOP_TOP, ": dome ", DOME_TOP, " (", TOP_TOP - DOME_TOP, " under) | MA963 clamps ", MA_TOP,
           " (", TOP_TOP - MA_TOP, ") radome ", MA_ANT_TOP, " | whip tips ", WHIP_BASE + WHIP_H, " (", TOP_TOP - WHIP_BASE - WHIP_H, ")"));
  echo(str("DOME L1 PC z ", DOME_PCZ, " at x ", DOME_CX, "; rail top ", TOP_TOP - DOME_PCZ, " above it; masks (top inner edge / band bottom): ",
           [for (i = [0 : 3]) [RAILS_C[i][0], round(mask(TOP_TOP - DOME_PCZ, d_in(i, DOME_CX)) * 10) / 10,
                                round(mask(TOP_Z0 - DOME_PCZ, d_in(i, DOME_CX) + E) * 10) / 10]]));
  echo(str("MA963 element ref z ", MA_RC, " at x ", MA_CX, "; masks: ",
           [for (i = [0 : 3]) [RAILS_C[i][0], round(mask(TOP_TOP - MA_RC, d_in(i, MA_CX)) * 10) / 10]]));
  echo(str("ROD LEVEL x: MA963 clamps ", MA_CX - MA_HALF, "-", MA_CX + MA_HALF, " | dome ", DOME_CX - DOME_D/2, "-", DOME_CX + DOME_D/2,
           " (gap ", DOME_CX - DOME_D/2 - MA_CX - MA_HALF, ") | CO tray ", CO_CAP - 70, "-", CO_CAP + 67.6, " z ", ROD_Z - 44.62, "-", ROD_Z - 12));
  echo(str("SIDE EXIT WINDOW (each long face, between posts): ", DXE - 2*E, " wide x ", TOP_Z0 - E, " tall; bay-L tray + battery at +",
           EXIT_LIFT, " lift tops out at z ", BAT_TOP + EXIT_LIFT, " vs lowest rod-level part over it z ", ROD_Z - 10,
           "; top opening ", DXE - 2*E, " x ", DYE - 2*E, " vs tray ", BAY + 20, " x ", DYE - 2*E + 20));
  assert(TOP_TOP - DOME_TOP >= TOP_CLR, "dome top within TOP_CLR of the top rails");
  assert(TOP_TOP - MA_TOP >= TOP_CLR, "MA963 within TOP_CLR of the top rails");
  assert(TOP_TOP - WHIP_BASE - WHIP_H >= TOP_CLR, "whips within TOP_CLR of the top rails");
  assert(DOME_CX - DOME_D/2 >= E + 5 && DOME_CX + DOME_D/2 <= DXE - E - 5, "dome under an end rail (it rises above the rail underside)");
  assert(DOME_CX - DOME_D/2 - (MA_CX + MA_HALF) >= 5, "dome fouls the MA963 clamps");
  assert(MA_CX - 52 - 23 >= 20 + 10 + 2, "MA963 station fouls the left yoke cap");
  assert(MA_STD - 10 >= 2, "MA963 plate overhang fouls the yoke cap top");
  assert(CO_CAP + 10 + 2 <= DOME_CX - 20, "CO cap fouls the dome puck");
  assert(CO_CAP - 10 - 2 >= MA_CX + MA_HALF, "CO cap (above the rods) fouls the MA963 plate");
  assert(CO_CAP - 32 >= MA_CX + 52 + 10 + 2, "CO plate fouls the MA963 under-rod caps");
  assert(CO_CAP - 70 >= 28 + 107 + 10, "CO tray hangs over the battery's lift path");
  assert(CO_CAP + 67.6 <= DXE - 40 - 2, "CO tray fouls the right yoke bridge");
  assert(BAT_TOP + EXIT_LIFT <= ROD_Z - 10 - 10, "battery cannot pass under the rod level in the side exit");
  for (q = WHIPS_C) assert(abs(q[1] - DYE/2) - 5 >= 30 + 17 + 2 && q[0] - 5 >= DOME_CX + DOME_D/2 + 5 && q[0] + 5 <= DXE - E - 5, "whip placement");
}

// ------------------------------------------------------------------ rev C views
// Elevation markers: numbered in the legend by render_E_revC.py (no 3D text).  [id, x, z, colour]
MK_X = DXE + 16;
MARKS_C = [
  [1, MK_X, TOP_TOP],        [2, -24, TOP_Z0],   [3, DOME_CX, DOME_TOP],  [4, DOME_CX, DOME_PCZ],
  [5, MA_CX, MA_TOP],        [6, WHIPS_C[0][0], WHIP_BASE + WHIP_H],         [7, MK_X, ROD_Z],
  [8, CO_CAP - 70, ROD_Z - 44.62], [9, -24, E],  [10, MK_X, 0]];
module mk(m) translate([m[1], -60, m[2]]) color([0.85, 0.1, 0.55]) sphere(4.5, $fn = 24);
if (view == "elev") {                                                                        // side elevation, looking +Y, orthographic
  assembly();
  color(YEL) for (m = MARKS_C) if (m[0] != 4) translate([min(m[1], 0) - 30, -58, m[2] - 0.6]) cube([max(m[1], DXE) + 30 - min(m[1], 0) + 30 + (m[1] > DXE ? 0 : 0), 1, 1.2]);
  color([0.2, 0.47, 0.84]) translate([DOME_CX - 90, -58, DOME_PCZ - 0.6]) cube([180, 1, 1.2]);   // phase-centre line
  for (m = MARKS_C) mk(m);
  color(YEL) translate([-44, -58, E + 3]) cube([1.2, 1, POST_H]);                            // post length bar
  color(YEL) translate([-54, -58, 0]) cube([1.2, 1, TOP_TOP + 3]);                           // overall height bar
}
if (view == "marker") { m = MARKS_C[mkid - 1]; mk(m); }                                      // one marker alone (pixel locator)
