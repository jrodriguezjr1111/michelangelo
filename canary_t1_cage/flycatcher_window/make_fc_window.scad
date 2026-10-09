// ============================================================================
// FLYCATCHER WINDOW UNIT — Nooelec FlyCatcher v1.1b1 (dual 1090/978 tuner, Pi-HAT outline) in a
// stand-alone enclosure on a lever suction cup at the aircraft's back window
// (family canary_t1_cage/flycatcher_window, 2026-09-30).  Owner: "let's design a robust and clean
// looking enclosure for the FlyCatcher. We have decided to use a suction cup to place it near the back
// window of the aircraft."
//
//   part = "base" | "lid" | "hood" | "adapter" | "lens" | "label"     (print-oriented STLs)
//   view = "none" | "iso" | "exploded" | "glass" | "side"            (renders)
//
// FRAME: x right as seen from the CABIN, z UP, y from the cabin face (y = 0) toward the GLASS.
// The board stands VERTICAL, component face to the cabin (LEDs, LNA buttons visible), SMA edge UP
// (stubbies vertical — ADS-B / UAT are vertically polarised), micro-USB edge DOWN.
//   BASE (glass side) carries the board on its own brass standoffs (screws from the back into their
//        female ends — no heat-sets, no printed bosses), the stud + adapter screws, the tether tab and
//        the hood inserts.  LID (cabin side) carries the bezel, hex vents, LED lens, LNA button holes and
//        the CANARY TRAFFIC label seat.  They part on the board's mid-plane = the SMA axis plane, so the
//        TOP WALL is a split bulkhead round both SMA threads: the antenna nut + a 0.5 mm nylon washer
//        clamp the wall down onto the jack bodies — the wall takes the antenna cantilever, not the
//        board's edge joints.
//   HOOD (yellow, the one accent) traps both micro-USB overmolds (no latch exists) and zip-ties each
//        lead within 20 mm (R5.2).
//   ADAPTER keys the suction base's flange (eye-shaped pocket) so the unit cannot turn on the M6
//        screw; separate because a pocket on the base's bed face would be a 34 mm bridge.
// Secondary retention: a TETHER TAB on the base (lanyard to a seat-belt anchor / the cage) — a suction
// cup is not a restraint (R2.4).
// PRINT: base BACK face down; lid FRONT face down (house face-down; bezel, seat and vents on the bed);
// hood bottom down; adapter front down (pocket up); lens plate down; label face up.  No supports.
// Material: ASA flight — LIGHT GREY preferred (it sits in the sun at a window; black soaks), PLA fit-check.
// ============================================================================
use <../t1_panels/make_t1_panels.scad>     // house hex field: hex_cells(poly), hex_cm2(cells) — 5 AF / 1.6 web
part = "base";
view = "none";
$fn = 40;

// ---------------------------------------------------------------- board (t1_params "flycatcher" + photos 43/46)
BW = 56.03; BH = 64.93; BT = 1.6;                 // MEAS outline; long edge vertical (header on the right, front view)
HOLE_X = 24.5; HOLE_Z = [-3.47, -61.47];          // 49 x 58 MEAS, centred
SCREW_D = 2.9;                                    // M2.5 (Pi-HAT 2.75 holes) clearance; 3.4 if the standoffs are M3 — CONFIRM
STANDOFF = 11.0;                                  // EST brass standoff length behind the board (2x20 header is 8.5)
SMA_X = [13.25 - BW / 2, BW / 2 - 13.25];         // MEAS 2026-10-01: 13.25 from EACH side edge of the 56.03 SMA edge (mirror-symmetric) -> pitch 29.53
SMA_BASE = 1.45;                                  // MEAS 2026-10-01: jack body above the board's top edge
SMA_GAP = 6.16;                                   // MEAS 2026-09-30 (Javi): exposed thread, jack body -> antenna nut face, antenna fully seated
SMA_PITCH = 25.4 / 36;                            // 1/4-36 UNS-2A
WASHER = 0.5;                                     // nylon M6 washer the nut bites through
SMA_HOLE = 6.6; SPOT_D = 14.2;                    // 1/4-36 thread 6.35 + clearance; knurled nut 13.3 + 0.9
USB_X = [21.15 - BW / 2, BW / 2 - 21.15]; USB_AX = 1.3;   // MEAS 2026-10-01: ADS-B OUT 21.15 from the left edge, UAT OUT 21.15 from the right (pitch 13.73)
PLUG = [9.55, 7.45, 18.12];                       // MEAS 2026-10-01 micro-B plug body W x T x length (shell entry -> boot end)
CAB_D = 6.0;                                      // lead slot: lead 5.61 MEAS 2026-10-01 + 0.39
BTN_X = [23.1 - BW / 2, 33.7 - BW / 2]; BTN_Z = -4.46; BTN_D = 6.6; BTN_H = 16.93;   // LNA push-buttons: x EST (photo), z 4.46 + height 16.93 MEAS 2026-10-01, cap dia EST
LED_X = 28.10 - BW / 2; LED_Z = -18.61;           // MEAS 2026-10-01: cluster centre 28.10 from the left edge, 18.61 down from the top
LED_WIN = [[LED_X, LED_Z], [12, 9]];
LEDS = [for (l = [[-2.6, 1.6], [2.6, 1.8], [-1.8, -1.7], [2.0, -1.6]]) [LED_X + l[0], LED_Z + l[1]]];   // individual LEDs EST (photo)
MASS_BOARD = 48; MASS_ANT = 2 * 25; MASS_CUP = 180;               // g: PUB / EST / EST
ANT_L = 184; ANT_M = 25;                          // antenna length nut face -> tip MEAS 2026-10-01; mass EST

// ---------------------------------------------------------------- suction base (photo 45, scaled on its own screw heads, EST)
FL_LOBE = 39.85 / 2; FL_R = (62.96 - 39.85) / 2; FL_C = 34; FL_T = 6.12;   // MEAS 2026-10-01: screws 39.85 c-c, overall 62.96, plate 6.12; centre width 34 EST
DISC_D = 27; DISC_H = 1.0;                        // raised centre disc: dia EST, height MEAS 2026-10-01
CUP_H = 62;                                       // glass -> flange top face
STUD_D = 6.4;                                     // M6 (owner 2026-09-30) close-fit clearance through the back wall + adapter
STUD_HEAD = [10.0, 6.0]; STUD_WASHER = [18, 1.6];  // M6 SHCS head dia x h (ISO 4762); fender washer inside the base
STUD_SUPPLIED = 19;                               // owner: the M6 screw supplied with the cup is 19 long — ASSUMED fully threaded under the head
STUD_LEN = STUD_SUPPLIED;                         // the supplied M6 x 19
STUD_PITCH = 1.0;                                 // M6 coarse
CUP_THREAD_DEPTH = STUD_SUPPLIED - 6.66;           // MEAS 2026-09-30 (Javi, case a): 6.66 of the M6 x 19 left showing when bottomed -> 12.34
CUP_THREAD = [0, CUP_THREAD_DEPTH];               // female thread assumed to start at the disc top

// ---------------------------------------------------------------- enclosure (house numbers)
LID_T = 3.2;                                      // front panel (8 lines): label seat 1.8 leaves 1.4
FRONT_CLR = BTN_H - (LID_T - 0.5);               // the LNA caps rise INTO their lid holes and stop 0.5 under the face: guarded, finger-pressable
YB = LID_T + FRONT_CLR;                           // board front face
YP = YB + BT / 2;                                 // parting plane = board mid-plane = SMA axis
YW = YB + BT + STANDOFF;                          // base back wall, inner face
BACK_T = 4.0; YBK = YW + BACK_T;                  // back outer face
YUSB = YB - USB_AX;
WALL = 3.2; CW = BW / 2 + 0.6; XO = CW + WALL;
ZT_IN = SMA_BASE; T_SMA = 5.6; Z_SPOT = ZT_IN + T_SMA; ZT = ZT_IN + 9.4;
ZB_IN = -BH - 0.6; BOT_T = 9.0; ZB = ZB_IN - BOT_T;
CLIP = 4; EDGE = 1.5;
INS_D = 4.4; INS_DEP = 5.0; M3B = 3.4; CB_D = 6.2; CB_H = 3.0;
LID_SCREWS = [for (s = [-1, 1], z = [(ZT_IN + ZT) / 2, (ZB_IN + ZB) / 2]) [s * 26.0, z]];
STUD = [0, (ZT + ZB) / 2];
ADP_SCREWS = [[-17, STUD[1] + 20], [17, STUD[1] - 20]];          // diagonal: clear of the eye, the header and the stud washer
HOOD_INS = [[-18, YP + 7], [18, YP + 7]];                             // (x, y) on the base's bottom face
TAB_T = 6; TAB_Z = -6; TAB_R = 8; TAB_HOLE = 6.5;                 // tether tab (top-left, in the back-wall plane)
// adapter
AD_T = 7.6; AD_POCKET = 3.5; AD_W = 22; AD_H = FL_LOBE + FL_R + 3.5;
// hood
PLUG_OUT = PLUG[2] - (-BH - ZB);                  // overmold length below the bottom face
HOOD_Y = [YUSB - PLUG[1] / 2 - 3.5, HOOD_INS[0][1] + 5.5];
HOOD_X = 23; HOOD_H = PLUG_OUT + 0.3 + 12;
TIE_Z = ZB - PLUG_OUT - 0.3 - 6;
// label (house make_style_coupon plate)
LP_W = 44; LP_H = 11; LP_T = 1.8; LP_CLR = 0.15; LIP = 0.6; LABEL_Z = -32;
// hex fields on the lid front (x, z polygons)
F_SIDE = [[10.5, 0.5], [26.5, 0.5], [26.5, -24.5], [10.5, -24.5]];   // beside the LNA buttons + LED window (outlet, high)
F_LOW = [[-26.7, -40], [26.7, -40], [26.7, -64.5], [-26.7, -64.5]];  // over the tuners / USB end (inlet, low)
function mxp(p) = [for (q = p) [-q[0], q[1]]];
FIELDS = [F_SIDE, mxp(F_SIDE), F_LOW];
HEX_AF = 5.0; HEX_R = HEX_AF / sqrt(3);           // same cell as make_t1_panels (the cell centres come from its hex_cells)
SIDE_Z = [for (i = [0 : 7]) -10 - i * 6.6];       // side-wall hex row
CELLS = [for (f = FIELDS) each hex_cells(f)];

module ext_y(y0, y1) translate([0, y1, 0]) rotate([90, 0, 0]) linear_extrude(y1 - y0) children();
function clipped(x0, x1, z0, z1, c) = [[x0 + c, z0], [x1 - c, z0], [x1, z0 + c], [x1, z1 - c], [x1 - c, z1], [x0 + c, z1], [x0, z1 - c], [x0, z0 + c]];
module outline2d(d = 0) offset(delta = -d) polygon(clipped(-XO, XO, ZB, ZT, CLIP));
module body() hull() { ext_y(0, YBK) outline2d(EDGE); ext_y(EDGE, YBK - EDGE) outline2d(0); }
module eye2d(c = 0) hull() { circle(d = FL_C + 2 * c); for (s = [-1, 1]) translate([0, s * FL_LOBE]) circle(r = FL_R + c); }   // lobes along z

module common_cuts() {
  translate([-CW, LID_T, ZB_IN]) cube([2 * CW, YW - LID_T, ZT_IN - ZB_IN]);                     // cavity
  for (x = SMA_X) {
    translate([x, YP, ZT_IN - 1]) cylinder(d = SMA_HOLE, h = ZT - ZT_IN + 2);                   // split bulkhead hole
    translate([x, YP, Z_SPOT]) cylinder(d = SPOT_D, h = ZT - Z_SPOT + 1);                       // recessed nut seat
  }
  for (x = USB_X) translate([x - PLUG[0] / 2 - 0.2, YUSB - PLUG[1] / 2 - 0.2, ZB - 1]) cube([PLUG[0] + 0.4, PLUG[1] + 0.4, BOT_T + 2]);
}
module side_vents(up) for (s = [-1, 1], z = SIDE_Z) let(yc = up > 0 ? (LID_T + YP) / 2 : (YP + YW) / 2)
  translate([s * XO, yc, z]) rotate([0, 90, 0]) rotate([0, 0, up * 90]) cylinder(r = HEX_R, h = 3 * WALL, center = true, $fn = 6);   // vertex toward print-up

// ---------------------------------------------------------------- BASE (glass side)
module tether_tab() difference() {
  hull() { translate([-XO - TAB_R, YBK, TAB_Z]) rotate([90, 0, 0]) cylinder(r = TAB_R, h = TAB_T);
           translate([-XO + 1, YBK - TAB_T, TAB_Z - TAB_R]) cube([1, TAB_T, 2 * TAB_R]); }
  translate([-XO - TAB_R, YBK + 1, TAB_Z]) rotate([90, 0, 0]) cylinder(d = TAB_HOLE, h = TAB_T + 2);
  translate([-XO - TAB_R, YBK, TAB_Z]) rotate([90, 0, 0]) cylinder(d1 = TAB_HOLE + 2, d2 = TAB_HOLE - 0.01, h = 1, center = true);          // 0.5 x 45 edge breaks
  translate([-XO - TAB_R, YBK - TAB_T, TAB_Z]) rotate([90, 0, 0]) cylinder(d1 = TAB_HOLE - 0.01, d2 = TAB_HOLE + 2, h = 1, center = true);
}
module base() difference() {
  union() {
    intersection() { body(); translate([-100, YP, -200]) cube([200, 100, 400]); }
    tether_tab();
  }
  common_cuts();
  side_vents(-1);
  for (p = LID_SCREWS) translate([p[0], YP - 0.01, p[1]]) rotate([-90, 0, 0]) cylinder(d = INS_D, h = INS_DEP);
  for (s = [-1, 1], z = HOLE_Z) translate([s * HOLE_X, YW - 1, z]) rotate([-90, 0, 0]) cylinder(d = SCREW_D, h = BACK_T + 2);
  translate([STUD[0], YW - 1, STUD[1]]) rotate([-90, 0, 0]) cylinder(d = STUD_D, h = BACK_T + 2);
  for (p = ADP_SCREWS) translate([p[0], YW - 1, p[1]]) rotate([-90, 0, 0]) cylinder(d = M3B, h = BACK_T + 2);
  for (p = HOOD_INS) translate([p[0], p[1], ZB - 0.01]) cylinder(d = INS_D, h = INS_DEP);
}
// ---------------------------------------------------------------- LID (cabin side)
module label_seat() translate([0, -0.01, LABEL_Z]) rotate([-90, 0, 0])            // dovetail: wider at depth (45 deg overhang on the bed face)
  hull() { linear_extrude(0.01) square([LP_W + 2 * LP_CLR, LP_H + 2 * LP_CLR], center = true);
           translate([0, 0, LP_T]) linear_extrude(0.01) square([LP_W + 2 * LP_CLR + 2 * LIP, LP_H + 2 * LP_CLR + 2 * LIP], center = true); }
module lid() difference() {
  intersection() { body(); translate([-100, -1, -200]) cube([200, YP + 1, 400]); }
  common_cuts();
  side_vents(1);
  for (p = LID_SCREWS) translate([p[0], -1, p[1]]) rotate([-90, 0, 0]) { cylinder(d = M3B, h = YP + 2); cylinder(d = CB_D, h = CB_H + 1); }
  for (c = CELLS) translate([c[0], -1, c[1]]) rotate([-90, 0, 0]) rotate([0, 0, 30]) cylinder(r = HEX_R, h = LID_T + 2, $fn = 6);
  // LED window: 45 deg bezel on the face, 1.2 ledge from inside for the clear lens
  translate([LED_WIN[0][0], 0, LED_WIN[0][1]]) {
    translate([0, -0.01, 0]) rotate([-90, 0, 0]) linear_extrude(1.21, scale = [LED_WIN[1][0] / (LED_WIN[1][0] + 2.4), LED_WIN[1][1] / (LED_WIN[1][1] + 2.4)])
      square([LED_WIN[1][0] + 2.4, LED_WIN[1][1] + 2.4], center = true);
    translate([0, -1, 0]) rotate([-90, 0, 0]) linear_extrude(LID_T + 2) square(LED_WIN[1], center = true);
    translate([0, LID_T - 1.2, 0]) rotate([-90, 0, 0]) linear_extrude(2) square([LED_WIN[1][0] + 2.4, LED_WIN[1][1] + 2.4], center = true);
  }
  for (x = BTN_X) translate([x, -1, BTN_Z]) rotate([-90, 0, 0]) { cylinder(d = BTN_D + 1.8, h = LID_T + 2); translate([0, 0, 0.99]) cylinder(d1 = BTN_D + 4.2, d2 = BTN_D + 1.8, h = 1.2); }
  label_seat();
  for (t = [["LNA", 0, BTN_Z - 6.5], ["1090", SMA_X[0], 5], ["978", SMA_X[1], 5], ["ADS-B", USB_X[0], -69], ["UAT", USB_X[1], -69]])
    translate([t[1], 0.6, t[2]]) rotate([90, 0, 0]) linear_extrude(1)
      text(t[0], size = 2.6, font = "DIN Condensed:style=Bold", halign = "center", valign = "center");
}
// ---------------------------------------------------------------- HOOD (yellow): traps both micro-USB overmolds + ties the leads
module hood() difference() {
  hull() {
    translate([-HOOD_X, HOOD_Y[0] + 3, ZB - HOOD_H]) cube([2 * HOOD_X, HOOD_Y[1] - HOOD_Y[0] - 3, HOOD_H]);
    translate([-HOOD_X, HOOD_Y[0], ZB - HOOD_H + 3]) cube([2 * HOOD_X, HOOD_Y[1] - HOOD_Y[0], HOOD_H - 3]);   // 45 deg chamfer, bottom-front edge
  }
  for (x = USB_X) {
    translate([x - PLUG[0] / 2 - 0.3, HOOD_Y[0] - 1, ZB - PLUG_OUT - 0.3]) cube([PLUG[0] + 0.6, YUSB + PLUG[1] / 2 + 0.3 - HOOD_Y[0] + 1, PLUG_OUT + 1.3]);   // overmold pocket
    translate([x - CAB_D / 2, HOOD_Y[0] - 1, ZB - HOOD_H - 1]) cube([CAB_D, YUSB + CAB_D / 2 - HOOD_Y[0] + 1, HOOD_H + 1]);            // lead slot, open to the cabin
    translate([x, HOOD_Y[0] - 0.01, ZB - HOOD_H / 2]) rotate([-90, 0, 0]) linear_extrude(1.2, scale = [CAB_D / (CAB_D + 2.4), 1]) square([CAB_D + 2.4, HOOD_H + 4], center = true);
    for (s = [-1, 1]) translate([x + s * (CAB_D / 2 + 2.4) - 1, HOOD_Y[0] - 1, TIE_Z - 0.9]) cube([2, YUSB + CAB_D / 2 + 2.6 - HOOD_Y[0] + 1, 1.8]);   // tie tunnels
    translate([x - CAB_D / 2 - 3.4, YUSB + CAB_D / 2 + 0.6, TIE_Z - 0.9]) cube([CAB_D + 6.8, 2, 1.8]);                                        // behind the lead
  }
  for (p = HOOD_INS) translate([p[0], p[1], ZB - HOOD_H - 1]) { cylinder(d = M3B, h = HOOD_H + 2); cylinder(d = CB_D, h = HOOD_H - 8 + 1); }
}
// ---------------------------------------------------------------- ADAPTER: keys the suction base's flange
module adapter() difference() {
  translate([0, YBK, STUD[1]]) hull() for (sx = [-1, 1], sz = [-1, 1]) translate([sx * (AD_W - 4), 0, sz * (AD_H - 4)]) rotate([-90, 0, 0]) {
    cylinder(r = 4, h = AD_T - 1); translate([0, 0, AD_T - 1]) cylinder(r1 = 4, r2 = 3, h = 1); }
  translate([0, YBK + AD_T - AD_POCKET, STUD[1]]) rotate([-90, 0, 0]) linear_extrude(AD_POCKET + 1) eye2d(0.4);       // flange pocket
  translate([0, YBK + AD_T - AD_POCKET - (DISC_H - 0.3), STUD[1]]) rotate([-90, 0, 0]) cylinder(d = DISC_D + 0.8, h = DISC_H + 1);  // disc relief (the disc bears)
  translate([STUD[0], YBK - 1, STUD[1]]) rotate([-90, 0, 0]) cylinder(d = STUD_D, h = AD_T + 2);
  for (p = ADP_SCREWS) translate([p[0], YBK - 0.01, p[1]]) rotate([-90, 0, 0]) cylinder(d = INS_D, h = INS_DEP);
}
// ---------------------------------------------------------------- LENS (clear PETG): plate in the ledge + light pipes toward the LEDs
module lens() translate([LED_WIN[0][0], 0, LED_WIN[0][1]]) {
  translate([0, LID_T - 1.2 + 0.1, 0]) rotate([-90, 0, 0]) linear_extrude(1.1) square([LED_WIN[1][0] + 2.2, LED_WIN[1][1] + 2.2], center = true);
  for (l = LEDS) translate([l[0] - LED_WIN[0][0], LID_T, l[1] - LED_WIN[0][1]]) rotate([-90, 0, 0]) cylinder(d = 2.2, h = YB - LID_T - 1.0);
}
module label() {
  hull() { linear_extrude(0.01) square([LP_W + 2 * LIP, LP_H + 2 * LIP], center = true); translate([0, 0, LIP]) linear_extrude(LP_T - LIP) square([LP_W, LP_H], center = true); }
  translate([0, 0, LP_T - 0.01]) linear_extrude(0.6) text("CANARY TRAFFIC", size = 4.6, font = "DIN Condensed:style=Bold", halign = "center", valign = "center");
}
// ---------------------------------------------------------------- references (renders)
GLASS_Y = YBK + AD_T - AD_POCKET + 0.3 + CUP_H;   // flange top face = pocket floor + 0.3 (disc bears)
module board_ref() {
  color([0.05, 0.3, 0.55]) translate([-BW / 2, YB, -BH]) cube([BW, BT, BH]);
  color([0.95, 0.94, 0.9]) for (x = BTN_X) translate([x, YB, BTN_Z]) rotate([90, 0, 0]) { translate([-3.8, -3.8, 0]) cube([7.6, 7.6, 3.5]); cylinder(d = BTN_D, h = BTN_H); }
  color([0.75, 0.75, 0.78]) for (x = USB_X) translate([x - 4, YB - 2.6, -BH]) cube([8, 2.6, 5]);
  color([0.1, 0.1, 0.1]) translate([BW / 2 - 5.2, YB + BT, -BH + 6]) cube([5, 8.5, 52]);
  color([0.85, 0.7, 0.3]) for (s = [-1, 1], z = HOLE_Z) translate([s * HOLE_X, YB + BT, z]) rotate([-90, 0, 0]) cylinder(d = 5, h = STANDOFF, $fn = 6);
  color([0.85, 0.7, 0.3]) for (x = SMA_X) { translate([x - 3.25, YP - 3.25, 0]) cube([6.5, 6.5, SMA_BASE]); translate([x, YP, SMA_BASE]) cylinder(d = 6.35, h = SMA_GAP + 4); }
  color([0.2, 1, 0.3]) for (l = LEDS) translate([l[0], YB - 0.5, l[1]]) cube(0.9, center = true);
}
module antennas_ref() color([0.08, 0.08, 0.09]) for (x = SMA_X) translate([x, YP, Z_SPOT + WASHER]) {
  cylinder(d = 13.3, h = 8, $fn = 24); translate([0, 0, 8]) cylinder(d = 12, h = ANT_L - 14); translate([0, 0, ANT_L - 6]) sphere(d = 12); }
module plugs_ref() for (x = USB_X) {
  color([0.1, 0.1, 0.1]) translate([x - PLUG[0] / 2, YUSB - PLUG[1] / 2, -BH - PLUG[2]]) cube([PLUG[0], PLUG[1], PLUG[2]]);
  color([0.1, 0.1, 0.1]) translate([x, YUSB, -BH - PLUG[2] - 40]) cylinder(d = 3.5, h = 40);
}
module cup_ref() {
  yf = GLASS_Y - CUP_H;
  color([0.12, 0.12, 0.13]) {
    translate([0, yf, STUD[1]]) rotate([-90, 0, 0]) { translate([0, 0, -DISC_H]) cylinder(d = DISC_D, h = DISC_H); linear_extrude(FL_T) eye2d(); }
    translate([0, yf + FL_T, STUD[1]]) rotate([-90, 0, 0]) { cylinder(d = 46, h = 28); translate([0, 0, 28]) cylinder(d1 = 46, d2 = 86, h = CUP_H - FL_T - 28); }
    translate([20, yf + FL_T + 6, STUD[1] - 8]) cube([22, 9, 16]);                       // lever
  }
  color([0.75, 0.75, 0.78]) translate([STUD[0], YW - STUD_WASHER[1] - STUD_HEAD[1], STUD[1]]) rotate([-90, 0, 0]) cylinder(d = STUD_HEAD[0], h = STUD_HEAD[1]);  // M6 SHCS head inside
}
module glass_ref() color([0.6, 0.8, 0.9]) translate([-120, GLASS_Y, -150]) cube([240, 5, 300]);
module unit(ex = 0) {
  color([0.62, 0.64, 0.66]) base();
  translate([0, -ex * 45, 0]) { color([0.55, 0.57, 0.6]) lid(); color([0.85, 0.9, 0.95]) lens();
                                color([0.95, 0.8, 0.1]) translate([0, LP_T - ex * 15, LABEL_Z]) rotate([90, 0, 0]) label(); }
  translate([0, -ex * 22, 0]) board_ref();
  color([0.95, 0.8, 0.1]) translate([0, 0, -ex * 30]) hood();
  color([0.4, 0.42, 0.45]) translate([0, ex * 25, 0]) adapter();
  translate([0, 0, ex * 40]) antennas_ref();
  translate([0, 0, -ex * 15]) plugs_ref();
}
// ---------------------------------------------------------------- checks
cells_front = len(CELLS); cells_side = 4 * len(SIDE_Z);
open_cm2 = (cells_front + cells_side) * (sqrt(3) / 2) * HEX_AF * HEX_AF / 100;
glass_ant = GLASS_Y - YP;
maxspan = part == "lid" ? LP_H + 2 * LP_CLR + 2 * LIP : part == "hood" ? CB_D : part == "base" ? INS_D : 2.2;
echo(str("FC WINDOW: enclosure ", 2 * XO, " x ", YBK, " x ", ZT - ZB, " (w x d x h), +adapter ", AD_T, " | board on its own standoffs ", STANDOFF,
         " (screws from the back, d ", SCREW_D, ") | parting = SMA axis plane y ", YP));
echo(str("SMA BULKHEAD: wall ", T_SMA, " (14 lines) + ", WASHER, " nylon washer = ", T_SMA + WASHER, " in the MEAS ", SMA_GAP, " exposed thread (", SMA_GAP - T_SMA - WASHER,
         " left: the RF interface seats fully, then the nut bites the washer); the nut's own engagement is unchanged = all of the jack thread above the 6.16 (",
         "an SMA plug engages ~4-5 mm = ", round(4.5 / SMA_PITCH), " threads); holes ", SMA_HOLE, ", nut seats ", SPOT_D, " recessed ", ZT - Z_SPOT));
ant_f = ANT_M / 1000 * 9.81 * 18; ant_m = ant_f * (ANT_L / 2 + WASHER); ant_p = ant_m / (T_SMA * 2 / 3) / (6.35 * T_SMA / 2);
ant_tube = PI / 64 * (pow(6.0, 4) - pow(4.6, 4)) / 3.0;                      // EST jack neck section modulus (OD 6.0 root, ID 4.6)
echo(str("SMA BENDING: ", ANT_M, " g antenna (EST), ", ANT_L, " long (MEAS), CG ~", ANT_L / 2, " up, 18 g -> ", round(ant_f * 100) / 100, " N, ", round(ant_m), " N.mm at the wall -> hole bearing ~",
         round(ant_p * 10) / 10, " MPa in the ", T_SMA, " wall (ASA bearing ~40: SF ", round(40 / ant_p), "), jack neck ~", round(ant_m / ant_tube), " MPa brass; -y load on the lid half-wall, through the 4 lid screws"));
assert(ant_p <= 10, "SMA wall bearing > 10 MPa");
echo(str("VENTS: ", cells_front, " front + ", cells_side, " side hex cells (5 AF) = ", round(open_cm2 * 10) / 10, " cm2 open; back (sun/glass) face solid"));
echo(str("GLASS: flange top ", CUP_H, " off the glass (EST) -> antenna axis ", round(glass_ant * 10) / 10, " mm, antenna skin ", round((glass_ant - 6.5) * 10) / 10, " mm from the glass"));
stud_grip = STUD_WASHER[1] + BACK_T + (AD_T - AD_POCKET - (DISC_H - 0.3));    // washer + back wall + adapter floor under the disc
stud_tip = STUD_LEN - stud_grip;                                  // screw length past the disc top
stud_engage = stud_tip - CUP_THREAD[0];
stud_margin = CUP_THREAD[0] + CUP_THREAD[1] - stud_tip;            // to the bottom of the cup's thread
echo(str("STUD STACK (M6 x ", STUD_LEN, ", clearance ", STUD_D, "): fender washer ", STUD_WASHER[1], " + base floor ", BACK_T, " + adapter floor ", AD_T - AD_POCKET - (DISC_H - 0.3),
         " = grip ", stud_grip, " -> ", stud_tip, " past the disc top = ", stud_engage, " engaged (", round(stud_engage / 6 * 10) / 10, " D), ", stud_margin, " to the thread bottom (MEAS depth 12.34, >= 1 pitch)"));
assert(stud_engage >= 1.5 * 6, "M6 engagement < 1.5 D");

assert(stud_margin >= STUD_PITCH, "M6 bottoms in the cup (< 1 thread margin)");
echo(str("MAXSPAN=", maxspan));
assert(T_SMA >= 4, "SMA wall < 4 at the bulkhead");
assert(T_SMA + WASHER <= SMA_GAP && SMA_GAP - T_SMA - WASHER <= 0.2, "SMA wall + washer must sit inside the exposed thread and leave <= 0.2 so the nut bites");
assert(ZT - Z_SPOT >= 1.5, "nut seat too shallow");
assert(min([for (p = LID_SCREWS, x = SMA_X) abs(p[0] - x) - INS_D / 2 - SPOT_D / 2]) >= 0 || min([for (p = LID_SCREWS) p[1] + INS_D / 2]) <= Z_SPOT, "lid insert cuts a nut seat");
assert(XO - abs(LID_SCREWS[0][0]) - INS_D / 2 >= 1.6, "lid insert wall to the side < 1.6");
assert(min([for (p = LID_SCREWS) min(abs(p[1] - ZT_IN), abs(p[1] - ZT), abs(p[1] - ZB_IN), abs(p[1] - ZB))]) - INS_D / 2 >= 1.6, "lid insert wall in the top/bottom wall < 1.6");
assert(YP - INS_D / 2 >= 0 && YBK - (YP + INS_DEP) >= 1.2, "lid insert depth");
assert(min([for (x = USB_X) abs(x)]) - PLUG[0] / 2 - 0.2 >= 1.2, "USB openings merge");
assert(abs(HOOD_INS[0][0]) - INS_D / 2 - (max([for (x = USB_X) abs(x)]) + PLUG[0] / 2 + 0.3) >= 1.6, "hood insert breaks into a USB opening");
assert(HOOD_INS[0][1] - INS_D / 2 >= YP + 1.6 && HOOD_INS[0][1] + INS_D / 2 <= YBK - EDGE - 1.2, "hood insert not inside the base's bottom wall");
assert(abs(ADP_SCREWS[0][0]) + 5.5 / 2 <= BW / 2 - 5.2 - 0.5, "adapter screw head under the 2x20 header");
assert(STANDOFF - STUD_HEAD[1] - STUD_WASHER[1] >= 2, "M6 head + washer touches the board back");
assert(AD_T - AD_POCKET - DISC_H >= 2, "adapter floor under the disc < 2");
function eye_hw(dz) = max(sqrt(max(0, FL_C * FL_C / 4 - dz * dz)), sqrt(max(0, FL_R * FL_R - pow(abs(dz) - FL_LOBE, 2))),
                         abs(dz) <= FL_LOBE ? FL_C / 2 + (FL_R - FL_C / 2) * abs(dz) / FL_LOBE : 0);
assert(min([for (p = ADP_SCREWS) abs(p[0]) - INS_D / 2 - (eye_hw(p[1] - STUD[1]) + 0.4)]) >= 1.6, "adapter insert wall to the flange pocket < 1.6");
assert(AD_W - eye_hw(0) - 0.4 >= 3 && AD_H - (FL_LOBE + FL_R + 0.4) >= 3, "adapter rim round the pocket < 3");
assert(BTN_H - FRONT_CLR >= 0 && BTN_H <= YB - 0.3, "LNA cap must sit in its hole and stay >= 0.3 under the face");
assert(TIE_Z - 0.9 - (ZB - HOOD_H) >= 2, "tie tunnel too near the hood bottom");
assert(TIE_Z + 0.9 >= ZB - PLUG_OUT - 0.3 - 20, "lead grip > 20 mm from the plug (R5.2)");
assert(2 * XO + 2 * TAB_R + 2 <= 281, "bed");
// ---------------------------------------------------------------- exports
if (view == "iso") unit();
if (view == "exploded") unit(1);
if (view == "glass") { unit(); cup_ref(); glass_ref(); }
if (view == "side") { unit(); cup_ref(); glass_ref(); }
if (view == "none") {
  if (part == "base") translate([0, 0, YBK]) rotate([-90, 0, 0]) base();              // back face on the bed
  if (part == "lid") rotate([90, 0, 0]) lid();                                         // front face on the bed
  if (part == "hood") translate([0, 0, -(ZB - HOOD_H)]) hood();                        // bottom on the bed
  if (part == "adapter") translate([0, 0, -YBK]) rotate([90, 0, 0]) adapter();         // front on the bed, pocket up
  if (part == "lens") translate([0, 0, -(LID_T - 1.1)]) rotate([90, 0, 0]) lens();    // plate on the bed, pipes up
  if (part == "label") label();
}
