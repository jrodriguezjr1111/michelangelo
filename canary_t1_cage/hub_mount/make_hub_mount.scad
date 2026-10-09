// ============================================================================
// UHR204 HUB MOUNT — Advantech B+B SmartWorx BB-UHR204 ("ULI-414I") industrial 4-port USB hub,
// PORTS UP, on 2020 extrusion  (family canary_t1_cage/hub_mount, 2026-09-29).
// Owner: "let's design an enclosure or method to strap down the USB hub to 1 or more aluminum
// extrusions. The hub has 4 holes on each side. The USB ports must point towards the sky to
// minimize strain for the traffic USB cables."
//
//   variant = "dual"   (RECOMMENDED: backplate across TWO parallel members at SPAN c-c; placement =
//                       inner faces of the BACK deck rail + mid rail, SPAN 125.5, see hub_on_cage.scad)
//           | "single" (hung from ONE member: 4 x M5 in one slot line — a cantilever, tap-test it)
//   part    = "mount" | "comb"                     (print-oriented STLs)
//   view    = "none" | "iso" | "exploded"          (renders; hub, plugs, cables, straps drawn)
//
// HUB (datasheet provenance, see README): case 138.24 x 86.92 x 35.00 (B&B UHRx04 2010 drawing; the
// 2018 Advantech sheet: 86.34 +/-0.51, 35 +/-0.51, ear holes 153.61 c-c).  The 4-port face is a
// 138 x 35 LONG face and carries the host USB-B too (at the terminal-block end); DC = 3-pole 5.08
// terminal block + locking barrel jack on one END face.  "4 holes on each side" = the two 86 x 35 END
// faces: four holes on the mid-thickness line; inner pair 51.33 c-c (DIMENSIONED, 2018 sheet), outer
// holes ~9.1 outboard of each (SCALED, EST).  The factory panel brackets use the pair nearest the port
// face.  Thread NOT in either datasheet (M3 or #4-40, CONFIRM) -> 3.4 clearance passes both.
//
// ORIENTATION: port face UP (+z).  The hub stands on its back face (opposite the ports) on two end
// ledges, its rail-side big face bears on the backplate, and it is held by:
//   PRIMARY  : two printed CHEEKS, 4 screws per end through 3.4 clearance into the hub's own end holes
//   SECONDARY: (independent of the hub's threads) end LEDGES (-z), a top LIP hooking 5 mm over the port
//              face's rail-side edge (+z), the backplate (+y), cheek bearing (+/-x) and TWO 25 mm straps
//              round hub + cheeks + backplate through slots in the plate (-y)  => R2.4 six directions twice.
// The backplate bolts to the member(s) with M5 BHCS into 14122 T-nuts (R6.6: 4.5 N.m, Loctite 243,
// torque stripe), heads flush in counterbores.  No tongues: the rail face is the bed face (see PRINT).
// CABLES: a separate COMB bar 4..10 mm above the plug overmolds grips every jacket within 20 mm (R5.2);
// tuners (p1 ADS-B, p2 UAT) go straight up to the antenna level; host / CO / vib turn down on the bay side.
// PRINT: mount RAIL FACE DOWN (flat bearing face on the bed; cheeks, ledges, lip rise off it; cheek
// screw holes teardropped; no supports).  Comb TOP FACE DOWN (engraved labels on the bed face).
// Material: PA12-CF flight (M5 preload on plastic, hot cabin), ASA acceptable for the comb, PLA fit-check.
// ============================================================================
variant = "dual";
SPAN = 125.5;          // member c-c (dual).  Back deck rail -> back mid rail on photo 39: 125.5 (CONFIRM)
part = "mount";
view = "none";
$fn = 40;

// ---------------------------------------------------------------- hub (mm)
HUB_L = 138.24;        // PUB 2010 drawing 5.442 in (2018 sheet scales 138.7) — CONFIRM by caliper
HUB_H = 86.92;         // PUB 2010 3.422 in (2018: 86.34 +/-0.51); port face <-> back face
HUB_T = 35.0;          // PUB 35.00 (+/-0.51)
END_HOLES = [8.4, 17.5, 68.83, 77.93];     // from the BACK face, on the mid-thickness line: inner 51.33 PUB, outer EST
TB_Z = [26, 42];       // EST terminal block along the end face, from the back face (2018 end view, scaled)
JACK_Z = [48, 58];     // EST locking barrel jack
SCREW_Z = [38, 48];    // EST slotted screw head on the far end face
// port face, from the TB end (2018 front view scaled at 6.43 px/mm, EST): host B, LED block, ports 1..4
HOST_X = 15.6; LED_X = [44.0, 60.4]; PORT_X = [71.1, 88.5, 105.7, 122.9];
PLUG_H = 30;           // EST overmold height above the port face (yellow flat + black round leads)
PLUG_A = [16, 8.5];    // EST USB-A overmold (along the hub, across it)
PLUG_B = [15, 13];     // EST USB-B overmold
MASS = 640;            // g, 2018 sheet (the 2010 sheet says 380 g for the older case) — weigh it

// ---------------------------------------------------------------- mount (house numbers)
PL_T = 6.4;                                   // backplate (16 lines): >= 4 wherever a fastener passes
CB_D = 10.4; CB_H = 3.2; M5B = 5.4;           // flush M5 BHCS
M3B = 3.4; INS3_D = 4.4; INS3_DEP = 5.0;      // M3 clearance / heat-set
CL = 0.4;                                     // per end: slide-in clearance (house +0.5 class)
CHK_T = 5.6;                                  // cheek (14 lines)
LEDGE_L = 20; LEDGE_T = 4;                    // end ledges under the hub
LIP = [5, 4];                                 // reach over the port face, thickness
STRAP_W = 25; STRAP_SLOT = [3.5, STRAP_W + 2];
Z0 = 26;                                      // hub bottom (deck bottom = 0; lower slot centre z 10)
HT = Z0 + HUB_H;                              // hub top = port face
XI = HUB_L / 2 + CL;  XO = XI + CHK_T;        // cheek inner / outer faces
YP = PL_T + HUB_T / 2;                        // port / hole centre line (ports centred in the 35)
CHK_Y = PL_T + HUB_T + 0.5;                   // cheeks reach the hub's bay face
PAD_LO = [Z0 - LEDGE_T, Z0 + END_HOLES[1] + M3B / 2 + 4];
PAD_HI = [Z0 + END_HOLES[2] - M3B / 2 - 4, HT + 0.5 + LIP[1]];
STRAPS_Z = [(PAD_LO[0] + PAD_LO[1]) / 2, (PAD_HI[0] + PAD_HI[1]) / 2];
BOLT_X = XO + CB_D / 2 + 1;
PLX = BOLT_X + CB_D / 2 + 4;
MZ = variant == "dual" ? [10, 10 + SPAN] : [10 + SPAN];
BOLTS = variant == "dual" ? [for (z = MZ, s = [-1, 1]) [s * BOLT_X, z]]
                          : [for (s = [-1, 1], x = [BOLT_X, 40]) [s * x, MZ[0]]];
PL_Z = variant == "dual" ? [0, MZ[1] + 10] : [Z0 - LEDGE_T - 6, MZ[0] + 10];
WINS = [[Z0 + 8, Z0 + 36], [Z0 + 50, Z0 + 76]];
WIN_X = XI - 8;
INS_C = [for (s = [-1, 1], z = [PAD_HI[1] + 7.5, PAD_HI[1] + 21.5]) [s * (XI - 3), z]];   // comb heat-sets
ANT_EDGE = 39.0;       // antenna plate back edge, mount y (abs y 220 on the cage, EST) — the comb must stay behind it
// comb
COMB_Z = [HT + PLUG_H + 4, HT + PLUG_H + 10];
BAR_Y = PL_T + 30;
CABLES = [["HOST", HOST_X, 6.0, 6.0], ["1 ADSB", PORT_X[0], 8.6, 3.0], ["2 UAT", PORT_X[1], 8.6, 3.0],
          ["3 CO", PORT_X[2], 5.2, 5.2], ["4 VIB", PORT_X[3], 5.2, 5.2]];        // label, x from TB end, slot w, cable t (EST)
function hx(d) = -HUB_L / 2 + d;             // TB end at mount -x

module teardrop2d(d) union() { circle(d = d); polygon([[-d / 2 / sqrt(2), d / 2 / sqrt(2)], [0, d / 2 * sqrt(2)], [d / 2 / sqrt(2), d / 2 / sqrt(2)]]); }

// ---------------------------------------------------------------- backplate + cheeks + ledges + lip
module plate2d() difference() {                       // in (x, z)
  offset(r = 4) offset(delta = -4) translate([-PLX, PL_Z[0]]) square([2 * PLX, PL_Z[1] - PL_Z[0]]);
  for (w = WINS) offset(r = 4) offset(delta = -4) translate([-WIN_X, w[0]]) square([2 * WIN_X, w[1] - w[0]]);
  for (s = [-1, 1], z = STRAPS_Z) translate([s > 0 ? XO : -XO - STRAP_SLOT[0], z - STRAP_SLOT[1] / 2]) square(STRAP_SLOT);
  for (b = BOLTS) translate(b) circle(d = M5B);
}
module mount() difference() {
  union() {
    translate([0, PL_T, 0]) rotate([90, 0, 0]) linear_extrude(PL_T) plate2d();
    for (s = [-1, 1], p = [PAD_LO, PAD_HI]) translate([s > 0 ? XI : -XO, PL_T - 0.01, p[0]]) cube([CHK_T, CHK_Y - PL_T, p[1] - p[0]]);
    for (s = [-1, 1]) translate([s > 0 ? XI - LEDGE_L : -XI, PL_T - 0.01, Z0 - LEDGE_T]) cube([LEDGE_L + 0.01, CHK_Y - PL_T, LEDGE_T]);
    translate([-XI - 0.01, PL_T - 0.01, HT + 0.5]) cube([2 * XI + 0.02, LIP[0], LIP[1]]);
  }
  for (b = BOLTS) translate([b[0], PL_T - CB_H, b[1]]) rotate([-90, 0, 0]) cylinder(d = CB_D, h = CB_H + 1);
  for (s = [-1, 1], h = END_HOLES) translate([s * (XI + CHK_T / 2), YP, Z0 + h]) rotate([0, 90, 0]) linear_extrude(CHK_T + 2, center = true) teardrop2d(M3B);
  for (i = INS_C) translate([i[0], PL_T - INS3_DEP, i[1]]) rotate([-90, 0, 0]) cylinder(d = INS3_D, h = INS3_DEP + 0.1);
  // strap bends: 45 deg x 2.5 on the rail-face edge inboard of each slot, and on each cheek's outer bay-side edge
  for (s = [-1, 1], z = STRAPS_Z) translate([s * XO, 0, z]) rotate([0, 0, 45]) cube([3.5, 3.5, STRAP_SLOT[1]], center = true);
  for (s = [-1, 1], p = [PAD_LO, PAD_HI]) translate([s * XO, CHK_Y, (p[0] + p[1]) / 2]) rotate([0, 0, 45]) cube([2.2, 2.2, p[1] - p[0] + 1], center = true);
  translate([0, PL_T - 1.2, Z0 + 5]) rotate([-90, 0, 0]) cylinder(d = 12, h = 2);           // relief: case screw near the back edge (EST)
}
// ---------------------------------------------------------------- comb (strain relief, R5.2)
module comb() difference() {
  union() {
    translate([-XO, PL_T, PAD_HI[1] + 0.3]) cube([2 * XO, 4, COMB_Z[1] - PAD_HI[1] - 0.3]);         // leg on the plate face
    translate([-XO, PL_T, COMB_Z[0]]) cube([2 * XO, BAR_Y - PL_T, COMB_Z[1] - COMB_Z[0]]);           // bar over the plugs
  }
  for (c = CABLES) translate([hx(c[1]), 0, COMB_Z[0] - 1]) linear_extrude(COMB_Z[1] - COMB_Z[0] + 2) {
    translate([-c[2] / 2, YP - c[3] / 2 - 0.4]) square([c[2], BAR_Y - YP + c[3] / 2 + 1.4]);           // slot, open to the bay
    translate([0, BAR_Y]) polygon([[-c[2] / 2 - 1.2, 0.01], [-c[2] / 2, -1.2], [c[2] / 2, -1.2], [c[2] / 2 + 1.2, 0.01]]);   // 1.2 mouth chamfer
    translate([c[2] / 2 + 1.6, YP - 1.7]) square([1.8, 3.4]);                                            // zip-tie eye
  }
  translate([hx(LED_X[0]) - 2, YP - 7, COMB_Z[0] - 1]) cube([LED_X[1] - LED_X[0] + 4, 14, 10]);    // LED window
  for (i = INS_C) translate([i[0], PL_T + 5, i[1]]) rotate([90, 0, 0]) linear_extrude(6) rotate(180) teardrop2d(M3B);
  for (c = CABLES) translate([hx(c[1]), PL_T + 8.6, COMB_Z[1] - 0.6]) linear_extrude(1) rotate(180)
    text(c[0], size = 2.8, font = "DIN Condensed:style=Bold", halign = "center", valign = "center");
}
// ---------------------------------------------------------------- reference hub, plugs, cables, straps, members (renders)
module hub_ref() {
  color([0.13, 0.28, 0.72]) difference() {
    translate([-HUB_L / 2, PL_T, Z0]) hull() for (y = [1.5, HUB_T - 1.5], z = [1.5, HUB_H - 1.5]) translate([0, y, z]) rotate([0, 90, 0]) cylinder(r = 1.5, h = HUB_L);
    for (s = [-1, 1], h = END_HOLES) translate([s * HUB_L / 2, YP, Z0 + h]) rotate([0, 90, 0]) cylinder(d = 3, h = 6, center = true);
  }
  color([0.18, 0.2, 0.3]) translate([-HUB_L / 2 + 3, PL_T + 3, HT - 0.3]) cube([HUB_L - 6, HUB_T - 6, 0.5]);
  color([0.75, 0.75, 0.78]) for (d = PORT_X) translate([hx(d) - 7.6, YP - 3.6, HT - 6]) cube([15.2, 7.2, 6.3]);
  color([0.75, 0.75, 0.78]) translate([hx(HOST_X) - 6.3, YP - 5.7, HT - 6]) cube([12.6, 11.4, 6.3]);
  color([0.2, 0.9, 0.3]) for (i = [0:3]) translate([hx(LED_X[0] + 5 + (i % 2) * 7), YP - 3 + floor(i / 2) * 6, HT]) cylinder(d = 2.4, h = 0.6);
  color([0.2, 0.7, 0.3]) translate([-HUB_L / 2 - 11, YP - 8, Z0 + TB_Z[0]]) cube([11, 16, TB_Z[1] - TB_Z[0]]);     // terminal block + plug
  color([0.55, 0.55, 0.58]) translate([-HUB_L / 2, YP - 3, Z0 + (JACK_Z[0] + JACK_Z[1]) / 2]) rotate([0, -90, 0]) cylinder(d = 10, h = 9);
  color([0.55, 0.55, 0.58]) translate([HUB_L / 2, PL_T + 8, Z0 + (SCREW_Z[0] + SCREW_Z[1]) / 2]) rotate([0, 90, 0]) cylinder(d = 8, h = 2.5);
}
module plugs_ref(ex = 0) {
  for (i = [0:3]) let(d = PORT_X[i]) {
    color(i < 2 ? [0.95, 0.8, 0.1] : [0.1, 0.1, 0.1]) translate([hx(d) - PLUG_A[0] / 2, YP - PLUG_A[1] / 2, HT]) cube([PLUG_A[0], PLUG_A[1], PLUG_H]);
    if (ex == 0) color(i < 2 ? [0.95, 0.8, 0.1] : [0.1, 0.1, 0.1]) {
      if (i < 2) translate([hx(d) - 3.75, YP - 1.25, HT + PLUG_H]) cube([7.5, 2.5, 95]);          // tuners: straight up to the antenna level
      else cable_down(hx(d), 4.6);
    }
  }
  color([0.72, 0.72, 0.7]) translate([hx(HOST_X) - PLUG_B[0] / 2, YP - PLUG_B[1] / 2, HT]) cube([PLUG_B[0], PLUG_B[1], PLUG_H]);
  if (ex == 0) color([0.72, 0.72, 0.7]) cable_down(hx(HOST_X), 5.5);
}
module cable_down(x, d, R = 16) let(zt = COMB_Z[1] + 6) {
  translate([x, YP, HT + PLUG_H]) cylinder(d = d, h = zt - HT - PLUG_H);
  translate([x, YP + R, zt]) rotate([0, 90, 0]) rotate([0, 0, 90]) rotate_extrude(angle = 180) translate([R, 0]) circle(d = d);
  translate([x, YP + 2 * R, Z0]) cylinder(d = d, h = zt - Z0);
}
module straps_ref() color([0.05, 0.05, 0.06]) for (z = STRAPS_Z) translate([0, 0, z - STRAP_W / 2]) {
  translate([-XO - 1.5, CHK_Y, 0]) cube([2 * XO + 3, 1.5, STRAP_W]);
  for (s = [-1, 1]) translate([s > 0 ? XO : -XO - 1.5, -1.5, 0]) cube([1.5, CHK_Y + 3, STRAP_W]);
  translate([-XO - 1.5, -1.5, 0]) cube([2 * XO + 3, 1.5, STRAP_W]);
}
module screws_ref(ex = 0) color([0.7, 0.7, 0.72]) {
  for (s = [-1, 1], h = END_HOLES) translate([s * (XO + ex * 30), YP, Z0 + h]) rotate([0, s * 90, 0]) cylinder(d = 5.5, h = 2.2);
  for (b = BOLTS) translate([b[0], PL_T - CB_H + ex * 90, b[1]]) rotate([-90, 0, 0]) cylinder(d = 9.5, h = 2.75);
}
module members_ref() color([0.15, 0.15, 0.17]) for (z = MZ) translate([-PLX - 30, -20, z - 10]) difference() {
  cube([2 * PLX + 60, 20, 20]);
  translate([-1, 18.2, 7]) cube([2 * PLX + 62, 2, 6]); translate([-1, 12.2, 4.5]) cube([2 * PLX + 62, 6, 11]);
  translate([-1, 7, 18.2]) cube([2 * PLX + 62, 6, 2]);
}
module hub_assembly(ex = 0) {
  members_ref();
  color([0.2, 0.2, 0.22]) mount();
  color([0.3, 0.3, 0.33]) translate([0, 0, ex * 70]) comb();
  translate([0, ex * 75, ex * 20]) { hub_ref(); translate([0, 0, ex * 40]) plugs_ref(ex); }
  screws_ref(ex);
  if (ex == 0) straps_ref();
}
// ---------------------------------------------------------------- checks
maxspan = M3B;             // no bridges in either print orientation; the teardropped M3 holes are the widest horizontal openings
strap_n = MASS / 1000 * 9.81 * 18;                              // R2.4: 18 g in any axis
strap_p = strap_n / 2 * sqrt(2) / (STRAP_W * 2.5 * sqrt(2));    // per side, 90 deg bend over the 2.5 x 45 chamfer
echo(str("HUB MOUNT ", variant, variant == "dual" ? str(" SPAN ", SPAN) : " (one member)", ": plate ", 2 * PLX, " x ", PL_Z[1] - PL_Z[0], " x ", PL_T,
         " | hub bottom z ", Z0, ", port face z ", HT, " | ", len(BOLTS), " x M5 BHCS into 14122 at ", BOLTS));
echo(str("HUB HOLES: 4 per end at ", END_HOLES, " from the back face, mid-thickness; 3.4 clearance (M3 or #4-40, CONFIRM) through ", CHK_T,
         " cheeks -> screw = removed factory bracket screw + ", CHK_T - 1.6, " mm"));
echo(str("RETENTION (R2.4): primary 8 screws | secondary ledges -z, lip +z (", LIP[0], " over the port face), plate +y, cheeks +/-x, 2 x ", STRAP_W,
         " mm straps -y; 18 g = ", round(strap_n), " N; strap bend bearing ", round(strap_p * 100) / 100, " MPa (R2.5 <= 1)"));
echo(str("CABLES: comb bar z ", COMB_Z, " = ", COMB_Z[0] - HT - PLUG_H, "..", COMB_Z[1] - HT - PLUG_H, " mm above the plug overmolds (R5.2 <= 20); bar edge y ", BAR_Y, " vs antenna plate ", ANT_EDGE));
echo(str("MAXSPAN=", maxspan));
assert(PAD_LO[1] - (Z0 + END_HOLES[1] + M3B / 2) >= 4 && (Z0 + END_HOLES[0] - M3B / 2) - PAD_LO[0] >= 4, "cheek wall at the lower screws < 4");
assert((Z0 + END_HOLES[2] - M3B / 2) - PAD_HI[0] >= 4 && PAD_HI[1] - (Z0 + END_HOLES[3] + M3B / 2) >= 4, "cheek wall at the upper screws < 4");
assert(Z0 + TB_Z[0] >= PAD_LO[1] + 1 && Z0 + JACK_Z[1] <= PAD_HI[0] - 1 && Z0 + SCREW_Z[1] <= PAD_HI[0] - 1, "terminal block / jack / end screw not inside the cheek gap");
assert(PAD_LO[1] - PAD_LO[0] >= STRAP_W + 1 && PAD_HI[1] - PAD_HI[0] >= STRAP_W + 1, "strap wider than the cheek pad it wraps");
assert(min([for (b = BOLTS, z = STRAPS_Z) abs(b[1] - z) - STRAP_SLOT[1] / 2 - CB_D / 2]) >= 2, "strap slot runs into an M5 counterbore");
assert(variant != "dual" || (STRAPS_Z[0] - STRAP_SLOT[1] / 2 >= MZ[0] + 10 && STRAPS_Z[1] + STRAP_SLOT[1] / 2 <= MZ[1] - 10), "strap cannot pass behind the plate between the members");
assert(PLX - BOLT_X - CB_D / 2 >= 4, "M5 counterbore wall to the plate edge < 4");
assert(min([for (i = INS_C, b = BOLTS) abs(i[0] - b[0]) - INS3_D / 2 - CB_D / 2]) >= 4 || min([for (i = INS_C, b = BOLTS) abs(i[1] - b[1])]) >= 10, "comb insert wall to an M5 counterbore < 4");
assert(PL_T - INS3_DEP >= 1.2, "insert breaks through the plate");
assert(max([for (i = INS_C) i[1]]) + INS3_D / 2 + 2 <= PL_Z[1], "comb insert too near the plate top");
assert(PL_T + max(LIP[0], 4) <= YP - PLUG_B[1] / 2 - 2, "lip / comb leg hits a plug overmold");
assert(COMB_Z[0] - HT - PLUG_H >= 2 && COMB_Z[1] - HT - PLUG_H <= 20, "comb grip not within 20 mm of the plug tops (R5.2)");
assert(BAR_Y <= ANT_EDGE - 2, "comb bar reaches the antenna plate edge");
assert(2 * PLX <= 281 && PL_Z[1] - PL_Z[0] <= 281, "plate exceeds the bed");
// ---------------------------------------------------------------- exports
if (view == "iso") hub_assembly();
if (view == "exploded") hub_assembly(1);
if (view == "none") {
  if (part == "mount") rotate([90, 0, 0]) mount();                                    // rail face (y = 0) on the bed
  if (part == "comb") translate([0, 0, COMB_Z[1]]) rotate([180, 0, 0]) comb();       // top face on the bed
}
