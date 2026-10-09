// ============================================================================
// CANARY T1 STACK — tactical stacking system for the two repurposed aluminium
// cases (Orin + RTK/LTE), the UHR204 hub and the SmallRig V-mount plate, on a
// SmallRig cheese plate that bolts to the concept-E 2020 deck (2026-09-26).
//
// Family: canary_t1_cage/t1_stack/.  Self-contained (does not include the E /
// D / faceplate files).  Photos 33-36 are the reference for "the current setup".
//
// FRAME (stack coords): X across the case I/O faces (width), Y = SLIDE AXIS,
// +Y = out through the I/O face (case back end at y = 0, I/O face at y = CASE_D),
// Z up from the cheese-plate top.  On the E deck: stack +Y -> deck +X (I/O face
// toward the x = 406 end face), stack -X -> deck +Y (nose).  See README.md.
//
// PROVENANCE: MEAS / PUB / EST / DSN as t1_params.py.  EVERY case, V-plate,
// battery and cheese-plate number is EST from photos 33-35 (mat grid + the
// RJ45 / USB-A / DP / SMA bodies on the I/O face as rulers) -> measure_sheet.html.
//
// part = "assembly" | "exploded" | "io" | "swap"                 (views)
//      | "ladder_L" | "ladder_R" | "hub_cradle" | "vplate_bracket"
//      | "cable_bar" | "dog" | "imu_plate" | "imu_plate_2d" | "uusb_hood"   (printable / cut parts)
//      | "cheese_ref"                                            (reference solid only)
// ============================================================================
part = "assembly";
explode = 0;          // 0..1 for part="exploded"
pull = 70;            // mm the Orin case is pulled out in part="swap"
$fn = 40;

// ---------------------------------------------------------------- the two cases (EST, photos 33-35)
CASE_W  = 132;    // EST  I/O-face width (RJ45/USB-A/DP scaled: 128-140 -> 132)
CASE_D  = 106;    // EST  I/O face -> back end (top view W:D = 1.25, side view L:H = 2.2)
ORIN_H  = 47;     // EST  top case (Orin + fan)            photo 33/34
RTK_H   = 41;     // EST  bottom case (ZED-F9P + EG25-G)    photo 34 (160 vs 180 px)
ENDPL_T = 3;      // EST  end plates (4 corner screws each), inside CASE_D
// Side geometry (photo 34): the shells are extrusions with LONGITUDINAL grooves running
// along the slide axis + through vent slots in the mid band.  The key rides ONE groove.
GROOVE_Z = 6.0;   // EST  lowest side groove centre above the case bottom      CONFIRM
GROOVE_W = 3.0;   // EST  groove width                                          CONFIRM
GROOVE_D = 1.2;   // EST  groove depth                                          CONFIRM
KEY = "groove";   // "groove" = tongue in the side groove (Z both ways) | "lip" = ledge + top lip only (fallback if the groove is cosmetic)
VENT_Z  = [0.30, 0.75];   // EST  side vent band, fraction of case H (must stay OPEN)
FAN_D   = 45;     // EST  Orin top fan grille O (photo 35)
FAN_YC  = 38;     // EST  grille centre from the BACK end (photo 35: 36 % of D)

// ---------------------------------------------------------------- hub, V-plate, battery, cheese plate
HUB   = [139, 87, 35];   // PUB  UHR204 13.9 x 8.7 x 3.5 cm; 139 along X, downstream (long) face -> +Y
HUB_SET = 5;             // DSN  hub downstream face this far behind the case I/O plane
VPL   = [110, 20, 96];   // EST  SmallRig V-mount plate W x T x H (photo 34/35)  CONFIRM model
BATT  = [100, 86, 120];  // EST  V99 Pro as photographed W x D x H (t1_params says 107 x 74 x 64 — CONFLICT, measure)
CH    = [190, 210, 10];  // EST/DSN cheese plate X x Y x T  (CONFIRM SmallRig model — its hole pattern is not published)
CH_Y0 = -38;             // DSN  cheese plate starts 38 behind the case back end (spans deck x 194-404: centre-member slot x 203 + end-member slot x 396, 8 mm edge distance)
CH_P  = 20;              // CONFIRM 1/4-20 grid pitch (placeholder); every foot hole is a SLOT >= pitch, so any grid lands

// ---------------------------------------------------------------- stack (DSN)
CLR     = 0.5;           // house slide-in clearance (total, across)
IN_W    = HUB[0] + 1;    // 140 ladder inner span: set by the hub, the widest thing in the stack
LAD_T   = 6;             // ladder side plate (15 lines @ 0.4)
STILE   = 14;            // stile width along Y
FOOT_W  = 14;            // foot flange outboard of the ladder plane
FOOT_T  = 6;
LEDGE_T = 4;             // ledge under each case edge
LEDGE_IN = 4;            // ledge reach under the case bottom edge
RAIL_IN = (IN_W - CASE_W - CLR) / 2;   // 3.75: rail standoff from the ladder plane to the case side
CRADLE_T = 4;            // hub cradle floor
HUB_GAP  = 4.0;          // hub top -> RTK ledge underside: room for the ledge's 45 deg print chamfer; a 5 mm EPDM strip (squash to 4) holds the hub down
CASE_GAP = 4;            // RTK top -> Orin ledge underside: through-air channel between cases
CAP_T   = 8;             // top cap rail (IMU plate seat + insert bosses)
CAP_IN  = 4;             // cap reaches over the Orin top edge (a drawer lip: the case slides under it); 4 = a clean short overhang in print
IMU_T   = 3;             // IMU datum plate: 6061 Al 3 (flight) | PA12-CF 4 (alt)
PLUG_KEEP = 50;          // USB-A / RJ45 plug + boot ahead of the I/O face (t1_params PLUG_KEEPOUT 55, less the face recess)
BAR_T   = 4;             // cable-bar rows
CHAM    = 1.2;           // house chamfer
M4B = 4.4; M5B = 5.4; Q20 = 6.8;        // house clearances; 1/4-20 clearance 6.8
INS_M4 = 5.6; INS_M5 = 6.4;             // heat-set bores

// ---------------------------------------------------------------- derived Z stack
Z_HUB0  = CRADLE_T;                         // hub bottom
Z_L1    = Z_HUB0 + HUB[2] + HUB_GAP;        // RTK ledge underside  40.5
Z_RTK0  = Z_L1 + LEDGE_T;                   // RTK case bottom      44.5
Z_L2    = Z_RTK0 + RTK_H + CASE_GAP;        // Orin ledge underside 89.5
Z_ORIN0 = Z_L2 + LEDGE_T;                   // Orin case bottom     93.5
Z_CAP   = Z_ORIN0 + ORIN_H + 1;             // cap rail underside  141.5
Z_TOP   = Z_CAP + CAP_T;                    // ladder top          149.5
Z_IMU   = Z_TOP;                            // IMU plate underside
MTI     = [68.6, 53.3, 14];                 // PUB/photo Uno-shield board (t1_params mti3_dk)
MTI_SO  = 5;                                // standoffs
Z_STACK = Z_IMU + IMU_T + MTI_SO + MTI[2];  // stack top above the cheese plate
Y_BAR   = CASE_D + PLUG_KEEP;               // cable-bar front plane
X_LAD   = IN_W / 2;                          // ladder inner face
X_OUT   = X_LAD + LAD_T;                     // ladder outer face
LOOP    = [30, 34];                          // coax service-loop bay X x Y (outboard of the left ladder)
Y_VB    = -STILE - 6;                        // V-bracket face (behind the back stiles)

// ---------------------------------------------------------------- colours
C_ASA = [0.16, 0.16, 0.18]; C_AL = [0.12, 0.12, 0.13]; C_YEL = [1.0, 0.80, 0.0];
C_MET = [0.62, 0.64, 0.68]; C_PCB = [0.05, 0.32, 0.25]; C_GOLD = [0.85, 0.7, 0.3];
C_RED = [0.85, 0.15, 0.12]; C_BAT = [0.2, 0.2, 0.22];

// ============================================================ checks (echo the load-bearing numbers)
cases_levels = [["hub", Z_HUB0, HUB[2]], ["RTK/LTE", Z_RTK0, RTK_H], ["Orin", Z_ORIN0, ORIN_H]];
side_open = (CASE_D - 2 * STILE) / CASE_D;                       // fraction of each side face left open (Y)
vent_clear = VENT_Z[0] * RTK_H - (GROOVE_Z + GROOVE_W / 2);      // tongue top to the vent band (RTK, the lower one)
echo(str("T1 STACK: ladder inner ", IN_W, " (hub ", HUB[0], "), rail standoff ", RAIL_IN, ", case clearance ", CLR,
         " | Z: hub ", Z_HUB0, "-", Z_HUB0 + HUB[2], ", RTK ", Z_RTK0, "-", Z_RTK0 + RTK_H, ", Orin ", Z_ORIN0, "-", Z_ORIN0 + ORIN_H,
         ", ladder top ", Z_TOP, ", stack top (MTi) ", Z_STACK));
Y_MIN = Y_VB - VPL[1] - BATT[1];  Y_MAX = Y_BAR + BAR_T + 14;
echo(str("ENVELOPE (EST): X ", 2 * X_OUT + 2 * FOOT_W, " at the feet, ", 2 * X_OUT + LOOP[0], " at the cable bar (loop bay) | Y ", Y_MIN, " .. ", Y_MAX,
         " = ", Y_MAX - Y_MIN, " incl. battery (", Y_MAX - Y_VB + VB_T, " without) | Z ", Z_STACK, " above the cheese plate top"));
echo(str("THERMAL: ladder touches each case only on a ", LEDGE_IN, " mm ledge + the tongue (bottom ", GROOVE_Z + GROOVE_W / 2,
         " mm of the side); side windows leave ", round(side_open * 100), " % of each side's length open over the vent band; ",
         CASE_GAP, " mm through-air channel between the cases; Orin fan grille O", FAN_D, ": IMU plate notched O", FAN_D + 8,
         ", MTi board overhangs the grille's front edge by ", FAN_YC + FAN_D/2 - MTI_Y0, " mm at ", Z_IMU + IMU_T + MTI_SO - (Z_ORIN0 + ORIN_H), " mm above it"));
assert(RAIL_IN >= 3, "rail standoff too thin to carry the ledge");
assert(KEY != "groove" || GROOVE_D <= RAIL_IN + 1.5, "tongue cannot reach the groove");
assert(vent_clear >= 2, "tongue/ledge reach into the side vent band");
assert(Z_L1 - RAIL_IN + 0.5 >= Z_HUB0 + HUB[2] + 0.4, "RTK ledge print chamfer fouls the hub top edge");
assert(CASE_D - FAN_YC - FAN_D / 2 > 30, "fan too far forward for the IMU plate — move the plate to the back end");
assert(Y_BAR - CASE_D >= 45, "cable bar inside the plug keep-out");
assert(Z_ORIN0 - (Z_RTK0 + RTK_H) >= CASE_GAP, "no air channel between the cases");
assert(2 * X_OUT + 2 * FOOT_W <= CH[0] + 0.1, "ladder feet overhang the cheese plate");

// ============================================================ helpers
module cbox(s, c = CHAM) hull() {                 // chamfered box, min corner at origin
  translate([c, c, 0]) cube([s[0] - 2*c, s[1] - 2*c, s[2]]);
  translate([0, c, c]) cube([s[0], s[1] - 2*c, s[2] - 2*c]);
  translate([c, 0, c]) cube([s[0] - 2*c, s[1], s[2] - 2*c]);
}
module hexgrid(w, h, d, t, pitch = 9) {           // hex lightening/vent pattern in an XZ face, depth t along Y
  for (i = [0 : floor(w / pitch) - 1], j = [0 : floor(h / (pitch * 0.866)) - 1])
    translate([pitch/2 + i * pitch + (j % 2) * pitch / 2, -1, pitch/2 + j * pitch * 0.866])
      if (pitch/2 + i * pitch + (j % 2) * pitch / 2 + d/2 < w) rotate([-90, 0, 0]) rotate([0, 0, 30]) cylinder(d = d, h = t + 2, $fn = 6);
}
module thumbscrew(axis = [0, 1, 0], l = 12) {     // yellow knurled captive M5 thumbscrew, head at origin, shank along +axis
  rotate(axis == [0, 1, 0] ? [-90, 0, 0] : axis == [0, -1, 0] ? [90, 0, 0] : [0, 0, 0]) {
    color(C_YEL) translate([0, 0, -6]) difference() { cylinder(d = 12, h = 6, $fn = 18); for (a = [0 : 30 : 330]) rotate([0, 0, a]) translate([6, 0, -1]) cylinder(d = 1.6, h = 8, $fn = 6); }
    color(C_MET) cylinder(d = 5, h = l);
  }
}

// ============================================================ reference solids (not printed)
module case_solid(h, orin = true) {                // extrusion shell + end plates + grooves + ports + (Orin) fan grille
  color(C_AL) difference() {
    translate([-CASE_W/2, 0, 0]) cbox([CASE_W, CASE_D, h], 2);
    for (s = [-1, 1], zg = [GROOVE_Z, h * 0.5, h - GROOVE_Z])                                  // longitudinal grooves
      translate([s > 0 ? CASE_W/2 - GROOVE_D : -CASE_W/2 - GROOVE_D, ENDPL_T, zg - GROOVE_W/2]) cube([2 * GROOVE_D, CASE_D - 2 * ENDPL_T, GROOVE_W]);
    for (s = [-1, 1], k = [0, 1]) translate([s * CASE_W/2 - 1.5, 22 + k * 30, h * (VENT_Z[0] + 0.12 + k * 0.2)]) cube([3, 44 - k * 10, 2.2]);   // side vents
    if (orin) translate([0, FAN_YC, h - 1.2]) difference() { cylinder(d = FAN_D, h = 2); cylinder(d = FAN_D - 6, h = 2); }
  }
  color([0.08, 0.08, 0.09]) for (y = [0, CASE_D - ENDPL_T]) translate([-CASE_W/2 + 0.5, y, 0.5]) cube([CASE_W - 1, ENDPL_T, h - 1]);   // end plates
  io_ports(h, orin);
}
module io_ports(h, orin) {                           // I/O face as seen from +Y; u = mm from the face's LEFT edge (viewer's left = +X)
  function X(u) = CASE_W/2 - u;
  translate([0, CASE_D, 0]) {
    ants = orin ? [17, 116] : [17, 62, 115];
    for (u = ants) color(C_GOLD) translate([X(u), 0, h - 13]) rotate([-90, 0, 0]) { cylinder(d = 6.3, h = 9); cylinder(d = 9, h = 2, $fn = 6); }
    color([0.03, 0.03, 0.03]) {
      translate([X(21) - 5, -0.5, h * 0.28]) cube([10, 1, 9]);                                    // DC
      translate([X(49), -0.5, h * 0.28]) cube([18, 1, 7]);                                        // DP
      for (u = [68, 85]) translate([X(u), -0.5, h * 0.24]) cube([15, 1, orin ? 16 : 8]);          // USB-A pairs / pass-through
      translate([X(104), -0.5, h * 0.24]) cube([16, 1, 13]);                                      // ETH
      translate([X(115), -0.5, h * 0.3]) cube([9, 1, 3.5]);                                       // Type-C
    }
    color([0.4, 0.4, 0.42]) for (sx = [-1, 1], z = [4, h - 4]) translate([sx * (CASE_W/2 - 5), 0.2, z]) rotate([-90, 0, 0]) cylinder(d = 4, h = 0.8);
  }
}
module hub_solid() {                                   // UHR204: downstream long face -> +Y, host + DC on the -X short end (photo 29)
  color([0.15, 0.25, 0.55]) translate([-HUB[0]/2, CASE_D - HUB_SET - HUB[1], Z_HUB0]) cube(HUB);
  color([0.03, 0.03, 0.03]) for (i = [0 : 3]) translate([-HUB[0]/2 + 30 + i * 26, CASE_D - HUB_SET - 0.5, Z_HUB0 + 12]) cube([14, 1, 7]);
  color([0.2, 0.6, 0.2]) translate([-HUB[0]/2 - 0.5, CASE_D - HUB_SET - 40, Z_HUB0 + 8]) cube([1, 16, 10]);
}
module vplate_solid() {                                // SmallRig V-mount plate on the V-bracket, red release lever (photo 34)
  translate([-VPL[0]/2, Y_VB - VPL[1], 12]) {
    color([0.1, 0.1, 0.11]) cbox([VPL[0], VPL[1], VPL[2]], 2);
    color(C_RED) translate([VPL[0] - 6, 4, VPL[2] * 0.62]) cube([10, 8, 10]);
  }
}
module battery_solid() color(C_BAT) translate([-BATT[0]/2, Y_VB - VPL[1] - BATT[1], 2]) cbox(BATT, 5);
module cheese_ref() color([0.1, 0.1, 0.11]) difference() {
  translate([-CH[0]/2, CH_Y0, -CH[2]]) cube(CH);
  for (i = [-floor(CH[0] / CH_P / 2) + 0.5 : floor(CH[0] / CH_P / 2) - 0.5], j = [0 : floor(CH[1] / CH_P) - 1])
    translate([i * CH_P, CH_Y0 + CH_P/2 + j * CH_P, -CH[2] - 1]) cylinder(d = 6.35, h = CH[2] + 2, $fn = 16);
}
module mti_solid() {
  translate([MTI_X0, MTI_Y0, Z_IMU + IMU_T + MTI_SO]) {
    color(C_PCB) cube([MTI[0], MTI[1], 1.6]);
    color([0.1, 0.1, 0.1]) translate([MTI[0] - 14, MTI[1] - 14, 1.6]) cube([12, 12, 3]);
  }
}

// ============================================================ LADDER (x2, mirrored): open frame, stiles + rails, feet
// Printed STANDING, as installed, on its foot flange (149.5 tall, 34 x 120 footprint).  Every ledge / cap
// rail is continuous with the web's layers, so a case's weight bends each ledge ALONG its layer lines;
// 45 deg chamfers carry the rail standoffs, leaving <= 4 mm plain overhangs (ledge / cap lips).  No supports.
module ladder(side = 1) {                              // side = +1 right (+X), -1 left
  mirror([side < 0 ? 1 : 0, 0, 0]) color(C_ASA) difference() {
    union() {
      translate([X_LAD, -STILE, 0]) cube([LAD_T, STILE, Z_TOP]);                                   // back stile
      translate([X_LAD, CASE_D - STILE - 0.5, 0]) cube([LAD_T, STILE, Z_TOP]);                    // front stile (face 0.5 behind the case face: the dog bears on the case)
      translate([X_LAD, -STILE, 0]) cube([LAD_T, CASE_D + STILE - 0.5, 10]);                        // bottom rail
      translate([X_LAD, -STILE, 0]) cbox([LAD_T + FOOT_W, CASE_D + STILE - 0.5, FOOT_T], 1.2);      // foot flange (outboard)
      for (zl = [Z_L1, Z_L2]) {                                                                      // ledge rails
        translate([X_LAD - RAIL_IN - LEDGE_IN, 0, zl]) cube([RAIL_IN + LEDGE_IN + LAD_T, CASE_D - 0.5, LEDGE_T]);
        translate([X_LAD - RAIL_IN - LEDGE_IN, -3, zl]) cube([RAIL_IN + LEDGE_IN + LAD_T, 3, LEDGE_T + 6]);   // back stop
        translate([X_LAD - 0.01, -STILE, zl - 6]) cube([LAD_T, CASE_D + STILE - 0.5, LEDGE_T + 12]);  // rail web in the ladder plane
      }
      if (KEY == "groove") for (lv = [[Z_RTK0], [Z_ORIN0]]) {                                        // tongue into the lowest side groove
        translate([X_LAD - RAIL_IN - GROOVE_D + 0.3, ENDPL_T + 2, lv[0] + GROOVE_Z - (GROOVE_W - 0.6)/2]) cube([RAIL_IN + GROOVE_D - 0.3 + 0.01, CASE_D - 2 * ENDPL_T - 4, GROOVE_W - 0.6]);
        translate([X_LAD - RAIL_IN, 0, lv[0]]) cube([RAIL_IN + 0.01, CASE_D - 0.5, GROOVE_Z + GROOVE_W/2 + 1]);
      }
      translate([X_LAD - CAP_IN - RAIL_IN, -STILE, Z_CAP]) cube([CAP_IN + RAIL_IN + LAD_T, CASE_D + STILE - 0.5, CAP_T]);   // top cap rail
      for (zc = [Z_L1, Z_L2, Z_CAP]) hull() {                                                        // 45 deg print chamfer under the rail standoff (printed STANDING)
        translate([X_LAD - RAIL_IN, -STILE, zc - 0.01]) cube([RAIL_IN, CASE_D + STILE - 0.5, 0.01]);
        translate([X_LAD - 0.01, -STILE, zc - RAIL_IN]) cube([0.01, CASE_D + STILE - 0.5, RAIL_IN]); }
      translate([X_LAD, -STILE, Z_HUB0 + HUB[2] * 0.5]) cube([LAD_T, STILE, 1]);                    // (keeps the back stile continuous in STL)
    }
    // chamfer the outer vertical edges (bezel look, and a 45 deg lead into the I/O face)
    for (y = [-STILE, CASE_D - 0.5]) translate([X_OUT, y, -1]) rotate([0, 0, 45]) cube([3, 3, Z_TOP + 2], center = true);
    // hex lightening in the stiles (stiles only — the side WINDOW between them is fully open over the fins/vents)
    for (y0 = [-STILE, CASE_D - STILE - 0.5]) translate([X_LAD + LAD_T, y0 + STILE/2, 0])
      for (z = [22 : 12 : Z_TOP - 22]) translate([-LAD_T/2, 0, z]) rotate([0, 90, 0]) cylinder(d = 7.5, h = LAD_T + 2, center = true, $fn = 6);
    // foot slots (1/4-20 to the cheese plate) — slots >= CH_P long so ANY grid lands
    for (y = [10, CASE_D - 30]) hull() for (dy = [0, CH_P]) translate([X_OUT + FOOT_W/2 - 1, y + dy - CH_P/2, -1]) cylinder(d = Q20, h = FOOT_T + 2);
    // captive thumbscrew insert (M5) in the front stile face at each case + hub mid-height (right ladder carries the case dogs, left the hub dog)
    for (z = [Z_RTK0 + RTK_H/2, Z_ORIN0 + ORIN_H/2, Z_HUB0 + HUB[2]/2])
      translate([X_LAD + LAD_T/2, CASE_D - 0.5 - 7, z]) rotate([-90, 0, 0]) cylinder(d = INS_M5, h = 8);
    // cap-rail M4 inserts for the IMU plate + dowel holes (asymmetric: plate goes on one way only)
    for (y = [CASE_D - 12, CASE_D - 50]) translate([X_LAD - 1, y, Z_TOP - 7]) cylinder(d = INS_M4, h = 8);
    translate([X_LAD + 2.5, side > 0 ? CASE_D - 31 : CASE_D - 24, Z_TOP - 8]) cylinder(d = 3.0, h = 9);   // O3 dowel (press)
    // back stile: M4 inserts for the V-bracket
    for (z = [30, Z_TOP - 40]) translate([X_LAD + LAD_T/2, -STILE - 1, z]) rotate([-90, 0, 0]) cylinder(d = INS_M4, h = 8);
    // EPDM strip recess under the RTK ledge (takes up the hub gap)
    translate([X_LAD - RAIL_IN - LEDGE_IN + 0.5, 6, Z_L1 - 0.01]) cube([RAIL_IN + LEDGE_IN - 1, CASE_D - 20, 1.2]);
    // cable-bar arm seats (2 x M4 inserts in the front stile's outer face)
    for (z = [Z_L1 + 2, Z_L2 + 2]) translate([X_OUT + 1, CASE_D - 0.5 - 7, z]) rotate([0, -90, 0]) cylinder(d = INS_M4, h = 8);
  }
}

// ============================================================ DOG: swing clamp on the captive thumbscrew (one per case + hub)
// Loosen 1/2 turn, swing the dog up 90 deg, slide the case out.  Tightening drives the case onto the back stops.
module dog(swung = false) color(C_ASA) rotate([0, swung ? 90 : 0, 0]) difference() {
  hull() { cylinder(d = 14, h = 6); translate([-19, 0, 0]) cylinder(d = 10, h = 6); }
  translate([0, 0, -1]) cylinder(d = M5B, h = 8);
  translate([-19, 0, -1]) cylinder(d = 3, h = 1.6);                                 // EPDM dot seat on the bearing pad
}
module dog_at(z, side = 1, swung = false)                // at the front stile, bearing on the case end-plate edge
  translate([side * (X_LAD + LAD_T/2), CASE_D + 0.2, z]) rotate([90, 0, 0]) rotate([0, 0, side > 0 ? (swung ? 90 : 0) : 180 + (swung ? -90 : 0)]) {
    translate([0, 0, -6]) dog();
    translate([0, 0, -6]) mirror([0, 0, 1]) thumbscrew([0, 0, 1], 10);
  }

// ============================================================ HUB CRADLE: floor + back stop + side lips; hub slides in from +Y
module hub_cradle() color(C_ASA) difference() {
  union() {
    translate([-X_LAD + 0.3, CASE_D - HUB_SET - HUB[1] - 4, 0]) cbox([IN_W - 0.6, HUB[1] + 4 + HUB_SET - 1, CRADLE_T], 1);
    translate([-X_LAD + 0.3, CASE_D - HUB_SET - HUB[1] - 4, 0]) cube([IN_W - 0.6, 4, CRADLE_T + 10]);                 // back stop
    for (s = [-1, 1]) translate([s > 0 ? X_LAD - 3.3 : -X_LAD + 0.3, CASE_D - HUB_SET - HUB[1], 0]) cube([3, HUB[1] - 20, CRADLE_T + 4]);   // side lips
  }
  for (i = [-2 : 2], j = [0 : 2]) translate([i * 24, CASE_D - HUB_SET - HUB[1] + 18 + j * 24, -1]) cylinder(d = 14, h = CRADLE_T + 2, $fn = 6);   // hex lightening / drain
  for (x = [-50, 50], y = [CASE_D - HUB_SET - HUB[1] + 6, CASE_D - HUB_SET - 12]) hull() for (dy = [0, CH_P]) translate([x, y + dy - CH_P/2, -1]) cylinder(d = Q20, h = CRADLE_T + 2);   // 1/4-20 slots
  translate([-HUB[0]/2 - 2, CASE_D - HUB_SET - 44, CRADLE_T - 0.01]) cube([2.5, 22, 5]);    // host/DC end: cable relief
}

// ============================================================ V-MOUNT BRACKET (photo 34): L-bracket off the back stiles, carries the SmallRig plate
// Printed FACE DOWN (152 x 112 flat on the bed, base leg + gussets rising 12): the hanging-battery moment bends the
// face along its layers, and goes into the back stiles through 4 x M4 — the base leg only locates it on the plate.
VB_W = 2 * X_OUT;  VB_H = 112;  VB_T = 6;
module vplate_bracket() color(C_ASA) difference() {
  union() {
    translate([-VB_W/2, Y_VB, 0]) cbox([VB_W, VB_T, VB_H], 1.5);                                  // vertical face
    translate([-VB_W/2, Y_VB, 0]) cbox([VB_W, -Y_VB - STILE + VB_T, 6], 1.2);                      // base to the back stiles
    for (s = [-1, 1]) translate([s * (X_OUT - 3) - 3, Y_VB, 0]) hull() {                          // side gussets (45 deg)
      cube([6, VB_T, VB_H - 10]); cube([6, -Y_VB - STILE + 2, 8]); }
  }
  for (s = [-1, 1], z = [30, Z_TOP - 40]) if (z < VB_H) translate([s * (X_LAD + LAD_T/2), Y_VB - 1, z]) rotate([-90, 0, 0]) cylinder(d = M4B, h = 30);   // M4 to the back stiles
  for (dx = [-19, 19], z = [36, 66]) hull() for (dz = [0, 10]) translate([dx, Y_VB - 1, z + dz]) rotate([-90, 0, 0]) cylinder(d = Q20, h = VB_T + 2);   // 1/4-20 slots: V-plate (pattern CONFIRM)
  translate([0, Y_VB - 1, 51]) rotate([-90, 0, 0]) cylinder(d = 9.8, h = VB_T + 2);              // 3/8-16 centre clearance (ARRI-style, CONFIRM)
  for (s = [-1, 1]) translate([s * (VB_W/2 - 9) - 2.5, Y_VB - 1, VB_H - 30]) cube([5, VB_T + 2, 26]);   // secondary battery strap slots (R2.4)
  for (x = [-VB_W/2 + 14 : 16 : VB_W/2 - 20], z = [8]) hull() for (dy = [0, 10]) translate([x + 4, Y_VB + VB_T + 4 + dy, -1]) cylinder(d = Q20, h = 8);   // 1/4-20 slots to the cheese plate
  translate([-VB_W/2 + 10, Y_VB, 82]) hexgrid(VB_W - 20, 24, 7.5, VB_T, 9.5);                     // lightening above the plate
}

// ============================================================ CABLE BAR: rows at the inter-level gaps (the cases slide THROUGH it)
// Two arms off the front stiles, a comb row at each gap (hub/RTK, RTK/Orin, top), label column + coax loop bay outboard left.
ROWS = [Z_L1, Z_L2, Z_CAP];
LABEL_Z = [26, 74, 122];            // three standing 44-tall labels on the loop-bay front, level with hub / RTK-LTE / Orin
module cable_bar() color(C_ASA) difference() {
  union() {
    for (s = [-1, 1]) translate([s > 0 ? X_LAD : -X_OUT, CASE_D - 0.5, Z_L1 - 4]) cube([LAD_T, Y_BAR - CASE_D + BAR_T + 0.5, Z_CAP + CAP_T - Z_L1 + 4]);   // arms
    for (z = ROWS) translate([-X_OUT, Y_BAR, z]) cbox([2 * X_OUT, BAR_T + 14, BAR_T], 0.8);       // comb rows (teeth outward)
    translate([-X_OUT - LOOP[0], Y_BAR - LOOP[1] + BAR_T + 14, 2]) cube([LOOP[0], LOOP[1], Z_CAP + CAP_T - 2]);   // loop bay + label column (to the plate)
  }
  for (z = ROWS, i = [0 : 19]) translate([-X_OUT + 8 + i * 7.6, Y_BAR + BAR_T + 2, z - 1]) cube([3.4, 20, BAR_T + 2]);   // comb slots (O3-3.4 leads/RG174), 20 mm jacket grip depth
  for (z = ROWS, x = [-X_OUT + 4, X_OUT - 7]) translate([x, Y_BAR + 4, z - 1]) cube([3, 6, BAR_T + 2]);                     // zip-tie eyes
  translate([-X_OUT - LOOP[0] + 3, Y_BAR - LOOP[1] + BAR_T + 17, 1]) cube([LOOP[0] - 6, LOOP[1] - 6, Z_CAP + CAP_T + 2]);   // loop bay void (open top + bottom)
  translate([-X_OUT - LOOP[0] - 1, Y_BAR - LOOP[1] + BAR_T + 22, Z_L1 + 6]) cube([5, 14, Z_CAP - Z_L1 - 12]);            // coax exit slot, outboard face
  for (lz = LABEL_Z)                                                                                                          // label seats on the bay FRONT (house 44 x 11 plate, standing, faces +Y)
    translate([-X_OUT - LOOP[0]/2 - 5.65, Y_BAR + BAR_T + 14 - 1.95 + 0.01, lz - 22.15]) cube([11.3, 2, 44.3]);
  for (s = [-1, 1], z = [Z_L1 + 2, Z_L2 + 2]) translate([s * (X_LAD + LAD_T/2) + s * 10, CASE_D - 0.5 - 7, z]) rotate([0, 90, 0]) cylinder(d = M4B, h = 30, center = true);
  for (s = [-1, 1], zz = [[Z_L1 + BAR_T + 5, Z_L2 - 5], [Z_L2 + BAR_T + 5, Z_CAP - 5]])                                      // arm windows (weight, and a hand-hold)
    translate([(s > 0 ? X_LAD : -X_OUT) - 1, CASE_D + 12, zz[0]]) cube([LAD_T + 2, Y_BAR - CASE_D - 20, zz[1] - zz[0]]);
}

// ============================================================ IMU DATUM PLATE: Al 6061 3 mm (or PA12-CF 4), on both ladder caps, 2 x M4 + 1 dowel per side
MTI_X0 = -MTI[0]/2;  MTI_Y0 = CASE_D - 6 - MTI[1];
UNO = [[13.97, 2.54], [15.24, 50.8], [66.04, 7.62], [66.04, 35.56]];     // PUB Arduino Uno hole pattern (board frame)
IMU_Y0 = CASE_D - 66;
module imu_plate_2d() difference() {
  translate([-X_OUT + 1, IMU_Y0]) offset(r = 3) offset(delta = -3) square([2 * X_OUT - 2, 66]);
  translate([0, FAN_YC]) circle(d = FAN_D + 8);                                                   // fan notch: nothing over the grille
  for (s = [-1, 1], y = [CASE_D - 12, CASE_D - 50]) translate([s * (X_LAD - 1), y]) circle(d = M4B);
  for (s = [-1, 1]) translate([s * (X_LAD + 2.5), s > 0 ? CASE_D - 31 : CASE_D - 24]) circle(d = 3.05);   // dowels: asymmetric = keyed
  // board holes: board +X (its silkscreen arrow) along STACK -X = DECK +Y (nose) -> board frame rotated 180 about Z
  for (h = UNO) translate([MTI_X0 + MTI[0] - h[0], MTI_Y0 + MTI[1] - h[1]]) circle(d = 3.2);
  for (i = [-2 : 2]) translate([i * 22, IMU_Y0 + 8]) circle(d = 8, $fn = 6);                       // hex lightening row
  // arrow "NOSE" cut through (reads from above, points stack -X)
  translate([-X_LAD + 16, CASE_D - 30]) polygon([[0, 0], [12, 7], [12, 3], [26, 3], [26, -3], [12, -3], [12, -7]]);
}
module imu_plate() color([0.72, 0.74, 0.78]) translate([0, 0, Z_IMU]) linear_extrude(IMU_T) imu_plate_2d();

// ============================================================ micro-USB HOOD (tuner end; the FlyCatcher is not in the stack)
UH = [12.5, 8.0, 20];      // EST micro-USB overmold W x H x L (+0.4 clearance built in below)
module uusb_hood() color(C_ASA) difference() {
  union() { cbox([UH[0] + 6, UH[2] + 14, UH[1] + 5], 1); translate([-8, UH[2] + 2, 0]) cbox([UH[0] + 22, 10, 4], 1); }
  translate([3, -1, 2]) cube([UH[0] + 0.4, UH[2] + 1, UH[1] + 0.4]);                                // overmold pocket (plug seated = pocket bottom)
  translate([(UH[0] + 6)/2 - 2.5, UH[2] - 1, 2]) cube([5, 16, 4]);                                   // cable exit + 20 mm jacket grip (zip over)
  for (x = [-4, UH[0] + 10]) translate([x, UH[2] + 7, -1]) cylinder(d = 3.4, h = 6);                 // M3 to the tuner standoffs / tray
}

// ============================================================ scenes
module stack(ex = 0, pull_orin = 0, swung = false) {
  cheese_ref();
  translate([0, 0, 6 * ex]) hub_cradle();
  translate([0, 40 * ex, 6 * ex]) hub_solid();
  for (s = [-1, 1]) translate([s * 60 * ex, 0, 12 * ex]) ladder(s);
  translate([0, 60 * ex, 12 * ex]) translate([0, 0, Z_RTK0]) case_solid(RTK_H, false);
  translate([0, 90 * ex + pull_orin, 12 * ex]) translate([0, 0, Z_ORIN0]) case_solid(ORIN_H, true);
  translate([0, -50 * ex, 12 * ex]) { vplate_bracket(); translate([0, -30 * ex, 0]) { vplate_solid(); translate([0, -40 * ex, 0]) battery_solid(); } }
  translate([0, 130 * ex, 12 * ex]) cable_bar();
  translate([0, 0, 50 * ex]) { imu_plate(); mti_solid(); }
  translate([60 * ex, 20 * ex, 12 * ex]) { dog_at(Z_RTK0 + RTK_H/2, 1); dog_at(Z_ORIN0 + ORIN_H/2, 1, swung); }
  translate([-60 * ex, 20 * ex, 6 * ex]) dog_at(Z_HUB0 + HUB[2]/2, -1);
  color(C_YEL) for (lz = LABEL_Z)                                                                  // yellow label plates: HUB / RTK-LTE / CORE
    translate([-X_OUT - LOOP[0]/2 - 5.5, Y_BAR + BAR_T + 14 - 1.8 + 130 * ex, lz - 22 + 12 * ex]) cube([11, 1.8, 44]);
}
module stack_part(p) {
  if (p == "ladder_R") ladder(1);                                                          // standing, foot on the bed
  if (p == "ladder_L") ladder(-1);
  if (p == "hub_cradle") hub_cradle();
  if (p == "vplate_bracket") translate([0, 0, -Y_VB]) rotate([90, 0, 0]) vplate_bracket();   // FACE DOWN: flat 152 x 112 on the bed
  if (p == "cable_bar") rotate([-90, 0, 0]) translate([0, -Y_BAR - BAR_T - 14, 0]) cable_bar();
  if (p == "dog") dog();
  if (p == "imu_plate") linear_extrude(4) imu_plate_2d();                                  // PA12-CF alt (4 mm); Al: cut from imu_plate_2d
  if (p == "imu_plate_2d") imu_plate_2d();
  if (p == "uusb_hood") uusb_hood();
  if (p == "cheese_ref") cheese_ref();
}
if (part == "assembly") stack();
if (part == "exploded") stack(ex = explode > 0 ? explode : 1);
if (part == "io") stack();
if (part == "swap") stack(pull_orin = pull, swung = true);
stack_part(part);
