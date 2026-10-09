// ============================================================================
// MTi AHRS MOUNT — Xsens MTi 1-s DEV Rev 2.6 (MTi-3 module) on 2020 extrusion
// (family canary_t1_cage/mti_mount, 2026-09-28).  Owner: "let's design a plate or
// mount for the MTi AHRS. I will mount it to 2020 aluminum extrusions." ... "the MTi
// can straddle two members."
//
//   variant = "bridge" (PRIMARY: plate across two PARALLEL members, SPAN c-c)
//           | "saddle" (fallback: straddles one member)
//   part    = "mount" | "stop" | "hood"                (print-oriented STLs)
//   view    = "none" | "iso" | "exploded"              (renders; board drawn)
//
// DATUM (R3.1 rigid, keyed, tied to metal, never a slide; R3.2 <= 0.2 deg re-seat):
//   Z / pitch / roll : the plate's flat underside on the member face(s), clamped by
//                      2 x M5 per member into slide-in 14122 T-nuts (R6.6: 4.5 N.m, Loctite 243, stripe)
//   lateral + yaw    : ONE hard skirt face against a member's side face (extrusion face = the datum;
//                      push the mount against it while torquing); saddle adds 2 crush ribs on the
//                      opposite skirt so it self-biases.  Tongues (5.6 in the 6.0 slot) are coarse
//                      location + anti-rotation only — their 0.4 play alone would allow ~0.4 deg.
//   axial            : a separate STOP BLOCK in the datum member's slot, bolted ONCE, torque-striped,
//                      never moved; the mount's +X end face butts its flat face.
//   keying           : a rib on the stop face enters a notch in the mount's +X end only -> the mount
//                      cannot seat reversed; the board's 3-hole Uno-subset pattern is asymmetric ->
//                      the board cannot go on rotated 180 deg.
// Board on COTS M3 x 12 male-female ALUMINIUM standoffs (non-magnetic, near the magnetometer)
// threaded into M3 heat-set inserts in the plate; the board swaps from above with 3 screws and
// never disturbs the datum (recal after any board swap, R3.2 / T1 memo C2).
// PRINT: top face DOWN (bed finish up top once installed... i.e. the engraved face is the bed face);
// tongues, skirts and the hood/stop features rise off the bed; no supports.  Nothing stands on the
// top face, which is why the standoffs are COTS and the +X arrow is ENGRAVED, not embossed.
// Material: PA12-CF flight (preload hot), ASA acceptable, PLA fit-check only.
// ============================================================================
variant = "bridge";
SPAN = 125.5;          // member centre-to-centre (bridge).  (a) deck rail -> mid rail on the back face: 125.5
                       // (photo 39, CONFIRM); (b) flat on two members: >= 73 so the board sits inside the gap
part = "mount";
view = "none";
$fn = 36;

// ---------------------------------------------------------------- board: MTi 1-s DEV Rev 2.6 (photos 40/41)
// Uno coordinates (x along the header rows, y across; origin = Uno origin).
// MEAS 2026-09-28 (Javi, caliper), component side up, USB-C bottom-left, origin = upper-right hole:
//   UR (0, 0), LR (0, -47.75), UL (-47.95, -9.03).  Hole dia still EST 3.2 (M3 clearance for the standoffs).
//   Replaces the Uno-derived A/B/C (dx 52.1, dy 5.1).  In this frame x_j = -x_uno, y_j = -y_uno:
//   UR = A, LR = B, UL = C, and the silkscreen reads X_s right, Y_s up.
HOLES_J = [[0, 0], [0, -47.75], [-47.95, -9.03]];
HOLE_A = [14.65, 26.65 - 47.75 / 2];                      // EST anchor: the measured pair centred where photo 41 put A/B (hole-to-edge CONFIRM)
UNO_HOLES = [for (j = HOLES_J) [HOLE_A[0] - j[0], HOLE_A[1] - j[1]]];
HDR_X = [27.0, 64.0];                                     // EST header rows along x (Uno R3 span), y 2.54 / 50.8
UNO_D = [66.1, 35.5];                                     // Uno D: NOT on this board (the MTi socket sits there) — CONFIRM
BOARD_X = [11.2, 69.3];  BOARD_Y = [0, 53.3];             // EST photo 41 (14.2 px/mm at the board plane): 58.1 x 53.3
BOARD_T = 1.6;
PIN_TAIL = 10.5;         // EST stacking-header tails under the board (photographed end-on: not scalable) — CONFIRM
SOCK_H = 8.5;            // EST header sockets above the board
USB_Y = [41, 49]; USB_X = 69.3;                           // EST USB-C "COM" on the high-x edge (photo 41)
MODULE = [[48.5, 17.3], [66.5, 36.3]];                    // EST MTi-3 in its socket
// sensor axes (silkscreen, photo 41): X_s = -x_uno (toward the notched edge), Y_s = -y_uno, Z_s = +z (component side)
BCX = (BOARD_X[0] + BOARD_X[1]) / 2;  BCY = (BOARD_Y[0] + BOARD_Y[1]) / 2;
function b2m(p) = [-(p[0] - BCX), -(p[1] - BCY)];        // Uno -> mount (sensor X along mount +X)

// ---------------------------------------------------------------- mount (house numbers)
E = 20; SLOT = 6.0; TONGUE = [5.6, 1.5];                 // tongue 5.6 wide, 1.5 deep (stops above the T-nut) — CONFIRM lip
PL_T = 6.4;                                               // plate (16 lines of 0.4): >= 4 mm wherever a fastener passes
STANDOFF = 12;                                            // COTS M3 x 12 M-F Al hex standoff
PIN_CLR = STANDOFF - PIN_TAIL;                            // clearance under the tails (bridge: open window under the board)
M5B = 5.4; CB_D = 10.4; CB_H = 3.2;                       // flush M5 BHCS
INS3_D = 4.4; INS3_DEP = 5.0; M3B = 3.4;
SKIRT = [3.2, 6.5];                                       // thickness, depth (the land above the side slot)
RIB = [1.2, 0.45];                                        // crush rib O, interference (saddle opposite skirt)
BX = BOARD_X[1] - BOARD_X[0]; BY = BOARD_Y[1] - BOARD_Y[0];
HOOD = [20, 18.8, 22];                                    // hood block: along cable, width, length
X_NEG = -(BX / 2 + 1.5 + HOOD[2] + 4);                    // plate -X end (hood side)
X_POS = BX / 2 + 22;                                      // plate +X end (arrow beyond the board edge + stop side)
MEMBERS = variant == "saddle" ? [0] : [-SPAN / 2, SPAN / 2];
Y_HALF = variant == "saddle" ? BY / 2 + 8 : SPAN / 2 + E / 2;         // saddle: room for the hood ear insert | bridge: FLUSH with the members' outer faces (never below the frame bottom)
BOLT_X = [-30, 20];
HOLES_M = [for (h = UNO_HOLES) b2m(h)];
USB_M = b2m([USB_X, (USB_Y[0] + USB_Y[1]) / 2]);
DATUM_Y = MEMBERS[0];                                     // datum member (bridge: member 1 = deck rail in placement a)
WIN = variant == "bridge" ? [[-16, -(SPAN / 2 - E / 2 - 8)], [19, SPAN / 2 - E / 2 - 8]] : [[0, 0], [0, 0]];   // lightening window under the board

module plate2d() difference() {
  offset(r = 3) offset(delta = -3) translate([X_NEG, -Y_HALF]) square([X_POS - X_NEG, 2 * Y_HALF]);
  translate([X_POS - 4, DATUM_Y + 6 - 2]) square([6, 4]);                                  // keying notch (rib on the stop)
  if (variant == "bridge") translate(WIN[0]) square(WIN[1] - WIN[0]);
}
// pin-row relief grooves (1.2 deep) the full board length, broken by an 8 mm boss round each standoff insert
module pin_reliefs() difference() {
  for (s = [-1, 1]) translate([-BX / 2, s * (BY / 2 - 2.5) - 3, PL_T - 1.2]) cube([BX, 6, 1.3]);
  for (h = HOLES_M) translate([h[0], h[1], PL_T - 1.5]) cylinder(d = BOSS_D, h = 2);
}
BOSS_D = INS3_D + 3.6;
module mount() difference() {
  union() {
    linear_extrude(PL_T) plate2d();
    for (my = MEMBERS) translate([X_NEG + 3, my - TONGUE[0] / 2, -TONGUE[1]]) cube([X_POS - X_NEG - 10, TONGUE[0], TONGUE[1] + 0.01]);   // tongues
    // hard datum skirt: saddle -> outer -y face of the member; bridge -> INNER face of member 1
    let(yf = variant == "saddle" ? DATUM_Y - E / 2 : DATUM_Y + E / 2)
      translate([X_NEG + 8, variant == "saddle" ? yf - SKIRT[0] : yf, -SKIRT[1]]) cube([X_POS - X_NEG - 22, SKIRT[0], SKIRT[1] + 0.01]);
    if (variant == "saddle") {                                                                   // opposite skirt + crush ribs (self-bias)
      translate([X_NEG + 8, E / 2 + 0.3, -SKIRT[1]]) cube([X_POS - X_NEG - 22, SKIRT[0], SKIRT[1] + 0.01]);
      for (x = [X_NEG + 16, X_POS - 20]) translate([x, E / 2 + 0.3 - RIB[1] + RIB[0] / 2, -SKIRT[1]]) cylinder(d = RIB[0], h = SKIRT[1]);
    }
  }
  for (my = MEMBERS, x = BOLT_X) translate([x, my, 0]) {                                         // 2 x M5 per member, flush from the top
    translate([0, 0, -TONGUE[1] - 1]) cylinder(d = M5B, h = PL_T + TONGUE[1] + 2);
    translate([0, 0, PL_T - CB_H]) cylinder(d = CB_D, h = CB_H + 1);
  }
  for (h = HOLES_M) translate([h[0], h[1], PL_T - INS3_DEP]) cylinder(d = INS3_D, h = INS3_DEP + 0.1);   // standoff inserts (from the top)
  for (s = [-1, 1]) translate([USB_M[0] - BX * 0 - 1.5 - HOOD[2] / 2 - 0, USB_M[1] + s * (HOOD[1] / 2 + 3.5), PL_T - INS3_DEP])
    cylinder(d = INS3_D, h = INS3_DEP + 0.1);                                                    // hood inserts
  pin_reliefs();                                                                                // pin-row reliefs (both variants)
  // engraved (0.8) on the top face = the bed face: +X arrow, "X", "MTi", "SPAN"
  translate([X_POS - 13, 0, PL_T - 0.8]) linear_extrude(1) {                                    // sensor +X (silkscreen X) arrow
    polygon([[-8, -2.2], [2, -2.2], [2, -5.5], [9, 0], [2, 5.5], [2, 2.2], [-8, 2.2]]);
    translate([0, 10]) text("+X", size = 5, font = "DIN Condensed:style=Bold", halign = "center", valign = "center");
  }
  translate([X_NEG + 16, variant == "saddle" ? -Y_HALF + 5 : -Y_HALF + 8, PL_T - 0.8]) linear_extrude(1)
    text(str("MTi  ", variant == "saddle" ? "SADDLE" : str("SPAN ", SPAN)), size = 3.2, font = "DIN Condensed:style=Bold", valign = "center");
}
// ---------------------------------------------------------------- stop block (bolted once, never moved) + hood
STOP = [14, E, 9];
module stop() difference() {
  union() {
    translate([0, -E / 2, 0]) cube(STOP);
    translate([0, -TONGUE[0] / 2, -TONGUE[1]]) cube([STOP[0], TONGUE[0], TONGUE[1] + 0.01]);
    translate([-3, 6 - 1.5, 0]) cube([3.01, 3, STOP[2]]);                                       // keying rib (enters the mount's notch)
  }
  translate([STOP[0] / 2 + 1.5, 0, -TONGUE[1] - 1]) cylinder(d = M5B, h = 20);
  translate([STOP[0] / 2 + 1.5, 0, STOP[2] - CB_H]) cylinder(d = CB_D, h = 5);
}
OVM = [12.8, 6.8];                                        // USB-C overmold 12.4 x 6.4 EST + 0.4
JKT = 4.6;                                                // cable jacket
module hood() let(zc = STANDOFF + BOARD_T + 1.6) difference() {          // in mount coords, z from the plate top
  union() {
    translate([-HOOD[2], -HOOD[1] / 2, 0]) cube([HOOD[2], HOOD[1], zc + OVM[1] / 2 + 3]);
    for (s = [-1, 1]) translate([-HOOD[2] / 2 - 5, s > 0 ? HOOD[1] / 2 - 0.01 : -HOOD[1] / 2 - 7, 0]) cube([10, 7.01, 4]);   // ears
  }
  translate([-HOOD[2] + 6, -OVM[0] / 2, zc - OVM[1] / 2]) cube([HOOD[2] - 5, OVM[0], OVM[1]]);   // overmold tunnel (front 16 mm)
  translate([-HOOD[2] - 1, 0, zc]) rotate([0, 90, 0]) cylinder(d = JKT, h = 8);                  // jacket exit
  translate([-HOOD[2] + 1.5, -HOOD[1] / 2 - 1, zc - 5]) cube([3, HOOD[1] + 2, 10]) ;            // zip-tie slot round the jacket (20 mm grip)
  for (s = [-1, 1]) translate([-HOOD[2] / 2, s * (HOOD[1] / 2 + 3.5), -1]) cylinder(d = M3B, h = 6);
}
// ---------------------------------------------------------------- reference board + standoffs (renders)
module board_ref() let(z0 = PL_T + STANDOFF) {
  color([0.1, 0.1, 0.12]) translate([0, 0, z0]) linear_extrude(BOARD_T) difference() {
    translate(b2m([BOARD_X[1], BOARD_Y[1]])) square([BX, BY]);
    translate(b2m([BOARD_X[0] + 8, BOARD_Y[0] + 41])) square([8.01, 26]);                        // top-edge notch
    for (h = HOLES_M) translate(h) circle(d = 3.2);
  }
  color([0.12, 0.12, 0.13]) for (y = [2.54, 50.8]) let(p = b2m([HDR_X[1], y])) translate([p[0], p[1] - 1.3, z0 + BOARD_T]) cube([HDR_X[1] - HDR_X[0], 2.6, SOCK_H]);
  color([0.8, 0.65, 0.3]) for (y = [2.54, 50.8]) let(p = b2m([HDR_X[1], y])) translate([p[0], p[1] - 0.3, z0 - PIN_TAIL]) cube([HDR_X[1] - HDR_X[0], 0.6, PIN_TAIL]);
  color([0.85, 0.45, 0.1]) let(a = b2m(MODULE[1])) translate([a[0], a[1], z0 + BOARD_T]) cube([18, 19, 3]);
  color([0.7, 0.7, 0.72]) translate([USB_M[0] - 7.4, USB_M[1] - 4.5, z0 + BOARD_T]) cube([7.5, 9, 3.2]);
  color([0.75, 0.76, 0.8]) for (h = HOLES_M) translate([h[0], h[1], PL_T - INS3_DEP]) cylinder(d = 5.5, h = STANDOFF + INS3_DEP, $fn = 6);   // Al standoffs
}
module usb_cable() color([0.1, 0.1, 0.1]) let(zc = PL_T + STANDOFF + BOARD_T + 1.6) translate([USB_M[0] - 1.5, USB_M[1], zc]) {
  translate([-20, -6.2, -3.2]) cube([20, 12.4, 6.4]); rotate([0, -90, 0]) cylinder(d = JKT, h = 70); }
module members_ref(len = 170) color([0.15, 0.15, 0.17]) for (my = MEMBERS) translate([X_NEG - 20, my - E / 2, -E]) difference() {
  cube([len, E, E]); translate([-1, E / 2 - SLOT / 2, E - 1.8]) cube([len + 2, SLOT, 2]); translate([-1, E / 2 - 5.5, E - 7.8]) cube([len + 2, 11, 6]); }
module assembly(ex = 0) {
  members_ref();
  color([0.2, 0.2, 0.22]) translate([0, 0, ex * 25]) mount();
  color([0.55, 0.3, 0.1]) translate([X_POS + ex * 20, DATUM_Y, 0]) stop();
  translate([0, 0, ex * 60]) { board_ref(); usb_cable(); }
  color([0.3, 0.3, 0.33]) translate([USB_M[0] - 1.5, USB_M[1], PL_T + ex * 45]) hood();
}
// ---------------------------------------------------------------- checks
open_under = variant == "bridge";
PAIR_MID = (HOLES_M[0] + HOLES_M[1]) / 2;
KEY_MISS = 2 * norm(HOLES_M[2] - PAIR_MID);               // 180 deg about the pair midpoint: where the single hole would have to be
KEY_DY = abs(HOLES_J[2][1] - (HOLES_J[0][1] + HOLES_J[1][1]) / 2);   // single hole off the pair midline (breaks the Y flip)
HOOD_J = [-(USB_X - HOLE_A[0]), -((USB_Y[0] + USB_Y[1]) / 2 - HOLE_A[1])];   // USB-C centre in Javi's frame (UR hole origin)
echo(str("HOLES MEAS (Javi frame, UR origin) ", HOLES_J, " -> Uno ", UNO_HOLES, " -> mount ", HOLES_M));
echo(str("KEYING: board rotated 180 deg puts the single hole ", KEY_MISS, " mm from its insert; single hole ", KEY_DY, " mm off the pair midline; USB-C centre at ", HOOD_J, " in Javi's frame (bottom-left: x < UL hole x, y below the pair midline)"));
assert(KEY_MISS >= 10 && KEY_DY >= 5 && abs(HOLES_J[2][0]) >= 10, "hole pattern not keyed against 180 deg / flip");
assert(HOOD_J[0] < HOLES_J[2][0] && HOOD_J[1] < (HOLES_J[0][1] + HOLES_J[1][1]) / 2, "USB-C hood not at the bottom-left of the measured pattern");
assert((BOSS_D - INS3_D) / 2 >= 1.5, "insert boss wall at a relief groove < 1.5");
maxspan = CB_D;
echo(str("MTi MOUNT ", variant, variant == "bridge" ? str(" SPAN ", SPAN) : "", ": plate ", X_POS - X_NEG, " x ", 2 * Y_HALF, " x ", PL_T,
         " | board 3-hole MEAS pattern at mount ", HOLES_M, " | standoff ", STANDOFF, " (COTS M3 M-F Al) -> ",
         open_under ? str("open window under the board + ", PIN_CLR + 1.2, " mm over the 1.2 relief grooves beyond it") : str(PIN_CLR + 1.2, " mm under the pin tails (1.2 relief grooves)")));
echo(str("DATUM: hard skirt on member y=", DATUM_Y, variant == "saddle" ? " (-y face, crush ribs opposite)" : " (inner face)",
         " | tongues ", TONGUE, " in ", len(MEMBERS), " slot(s) | ", 2 * len(MEMBERS), " x M5 into 14122 | stop block at +X, keying rib"));
echo(str("MAXSPAN=", maxspan));
assert(PIN_CLR + 1.2 >= 2, "pin-tail clearance over the relief grooves < 2 mm");
assert(variant != "bridge" || WIN[0][0] >= max([for (h = HOLES_M) h[0] < 0 ? h[0] : -99]) + INS3_D / 2 + 4 && WIN[1][0] <= min([for (h = HOLES_M) h[0] > 0 ? h[0] : 99]) - INS3_D / 2 - 4, "insert wall to the window < 4");
assert(PL_T - INS3_DEP >= 1.2, "insert breaks through the plate");
assert(variant != "bridge" || Y_HALF - (SPAN / 2) - CB_D / 2 >= 4, "M5 counterbore wall to the plate edge < 4");
assert(X_POS - X_NEG <= 281 && 2 * Y_HALF <= 281, "plate exceeds the bed");
// ---------------------------------------------------------------- exports
if (view == "iso") assembly();
if (view == "exploded") assembly(1);
if (view == "none") {
  if (part == "mount") translate([0, 0, PL_T]) rotate([180, 0, 0]) mount();      // top face on the bed
  if (part == "stop") translate([0, 0, STOP[2]]) rotate([180, 0, 0]) stop();     // top on the bed, tongue + rib up
  if (part == "hood") rotate([0, 90, 0]) hood();                                 // rear face on the bed, tunnel vertical
}
