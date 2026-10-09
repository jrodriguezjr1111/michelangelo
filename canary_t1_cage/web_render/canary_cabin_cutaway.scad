// ============================================================================
// canary_cabin_cutaway.scad — CONCEPT cut-away: the Canary unit sitting on the baggage
// floor of a GENERIC high-wing single-engine piston cabin (2026-10-09).  Not a part.
//
// Rules of the scene (hard):
//   * ORIGINAL simplified fuselage shell — a rounded-rectangle tube with invented, round
//     proportions.  No type badge, no registration, no manufacturer geometry, no real
//     cabin dimension reproduced.  Proportions are "plausible generic high-wing single", nothing more.
//   * The unit is a PLAIN SILHOUETTE: outer box + deck, plain case block, plain dome on a
//     pedestal, battery block.  No vents, no dome detail, no wordmark.  Rendered ghosted.
//   * NOTHING else in the bay: no restraint, strap, tie-down, cable, antenna, sensor or
//     mount anywhere; nothing on or under the seats or floor other than the unit.
//   * 2026-10-09 rev: grp="ghost" is a whole-airframe locator hull (fuselage, wing, empennage,
//     gear, prop disc) — an ORIGINAL simple hull whose side proportions are traced from the
//     public site's generic high-wing line art (company-site/explorations/c-aircraft), plan
//     proportions invented round numbers.  No badge, no registration, no glazing, no doors.
//
// grp = "cabin" | "tail" | "unit" | "ghost" | "ghost_wing" | "all"   (render_cabin.py exports the groups)
// cut = "iso" | "section" | "plan" | "none"           (which cut-away is applied to the shell)
// ghost_fit = true pulls the tailcone end section inside the ghost hull (the _ghost renders)
//
// Aircraft axes: +X forward (nose), +Y left, +Z up.  Origin: rear face of the seat backs
// on the cabin floor, aircraft centreline.
// ============================================================================
grp = "all";
cut = "iso";
ghost_fit = false;

// ---- invented generic cabin proportions (mm) ---------------------------------------
CAB_W   = 1050;   CAB_H = 1180;  CAB_R = 200;   WALL = 30;   // inner width / height, corner radius, shell
BELLY   = 150;                                              // inner floor-line sits this far above the shell bottom
X_FWD   = 620;    X_BULK = -920; X_TAIL = -2050;            // forward cut plane, aft bulkhead, tailcone end
FLOOR_T = 30;     SHELF_H = 90;  BULK_T = 25;               // cabin floor slab, baggage-floor step, bulkhead
SEAT    = [120, 470, 620];  SEAT_GAP = 60;  SEAT_RAKE = 12; // seat back block, centre gap, rake (deg, top aft)
CUSH    = [430, 470, 230];                                  // seat cushion block ahead of the back
DOOR    = [560, 470];  DOOR_X1 = -190;  DOOR_Z0 = 140;  DOOR_R = 45;  GROOVE = [6, 2.5];   // baggage door outline (RIGHT wall, -Y)
TAIL_W  = 540;    TAIL_H = ghost_fit ? 580 : 640;  TAIL_RISE = ghost_fit ? -110 : 260;  TAIL_SLANT = 0.55;  // tailcone end section + how the fade cut leans
// cut planes
ISO_Y   = -250;   ISO_SILL = 150;   // iso: near (+Y) wall removed above the sill, roof kept only for y <= ISO_Y (far quarter, so it never hides the far wall)
PLAN_Z  = 800;                      // plan: everything above this removed
// ---- the unit, silhouette only (envelope matches canary_unit_web.scad) ---------------
U  = [406, 279, 274];  U_BAT = [51, 95, 150];  U_BAT_Z0 = 70;
U_CASE = [160, 120, 56];  U_CASE_C = [130, U[1] / 2];
U_DOME_D = 110;  U_DOME_C = [U[0] - 76, U[1] / 2];  U_PED_D = 50;  U_PED_H = 22;
U_POS = [-720, -U[1] / 2, SHELF_H];             // unit origin: dome end forward, battery end aft, centred

Z_IN0 = -BELLY;  Z_IN1 = CAB_H - BELLY;          // inner section z range
echo(str("CABIN CONCEPT: inner ", CAB_W, " x ", CAB_H, " | bay x ", X_BULK + BULK_T, "..0 (", -X_BULK - BULK_T, " long) | unit x ",
         U_POS[0] - U_BAT[0], "..", U_POS[0] + U[0], " | unit top z ", U_POS[2] + U[2] + U_PED_H + U_DOME_D / 2));
assert(U_POS[0] - U_BAT[0] > X_BULK + BULK_T + 40, "unit battery end into the bulkhead");
assert(U_POS[0] + U[0] < -SEAT[2] * tan(SEAT_RAKE) - 40, "unit dome end into the raked seat backs");
assert(U[1] / 2 + 60 < CAB_W / 2, "unit wider than the bay");
assert(DOOR_X1 - DOOR[0] > X_BULK && DOOR_Z0 + DOOR[1] < Z_IN0 + CAB_H - CAB_R, "door outline off the flat wall zone");

// ---- 2D sections in the YZ plane (as [y, z]) ----------------------------------------
module rrect(w, h, r) offset(r = r) offset(delta = -r) square([w, h], center = true);
module sec_in()  translate([0, (Z_IN0 + Z_IN1) / 2]) rrect(CAB_W, CAB_H, CAB_R);
module sec_out() translate([0, (Z_IN0 + Z_IN1) / 2]) rrect(CAB_W + 2 * WALL, CAB_H + 2 * WALL, CAB_R + WALL);
module tail_in()  translate([0, (Z_IN0 + Z_IN1) / 2 + TAIL_RISE]) rrect(TAIL_W, TAIL_H, CAB_R * 0.6);
module tail_out() translate([0, (Z_IN0 + Z_IN1) / 2 + TAIL_RISE]) rrect(TAIL_W + 2 * WALL, TAIL_H + 2 * WALL, CAB_R * 0.6 + WALL);
// extrude a YZ section along X from x0 to x1
module along_x(x0, x1) translate([x0, 0, 0]) rotate([90, 0, 90]) linear_extrude(x1 - x0) children();
module slice_at(x) along_x(x, x + 0.01) children();

// ---- cabin shell + furniture ----------------------------------------------------------
module shell() difference() {
  along_x(X_BULK - 1, X_FWD) sec_out();
  along_x(X_BULK - 2, X_FWD + 1) sec_in();
  door_grooves();
}
module door2d() translate([DOOR_X1 - DOOR[0] / 2, DOOR_Z0 + DOOR[1] / 2]) difference() { rrect(DOOR[0], DOOR[1], DOOR_R); rrect(DOOR[0] - 2 * GROOVE[0], DOOR[1] - 2 * GROOVE[0], DOOR_R - GROOVE[0]); }
module door_grooves() for (y = [-CAB_W / 2 - WALL - 0.01, -CAB_W / 2 - GROOVE[1]])   // outer face and inner face of the RIGHT wall
  translate([0, y, 0]) rotate([90, 0, 0]) mirror([0, 0, 1]) linear_extrude(GROOVE[1] + 0.01) door2d();
module floor_slab() translate([X_BULK, -CAB_W / 2 + 6, -FLOOR_T]) cube([X_FWD - X_BULK, CAB_W - 12, FLOOR_T]);
module baggage_floor() translate([X_BULK, -CAB_W / 2 + 6, 0]) cube([-X_BULK, CAB_W - 12, SHELF_H]);
module bulkhead() along_x(X_BULK, X_BULK + BULK_T) sec_in();
module seat_back(side) translate([0, side * (SEAT_GAP / 2 + SEAT[1] / 2), 0])
  multmatrix([[1, 0, -tan(SEAT_RAKE), 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) translate([0, -SEAT[1] / 2, 0]) cube(SEAT);
module cushion(side) translate([SEAT[0], side * (SEAT_GAP / 2 + CUSH[1] / 2) - CUSH[1] / 2, 0]) cube(CUSH);
module cabin_raw() { shell(); floor_slab(); baggage_floor(); bulkhead(); for (s = [-1, 1]) { seat_back(s); cushion(s); } }

// ---- tailcone: tapers aft from the bulkhead station, cut by a leaning plane so it fades ----
module tail_raw() intersection() {
  difference() {
    hull() { slice_at(X_BULK - 1) sec_out(); slice_at(X_TAIL) tail_out(); }
    hull() { slice_at(X_BULK - 2) sec_in();  slice_at(X_TAIL - 1) tail_in(); }
  }
  // keep x >= X_TAIL + TAIL_SLANT * (z - Z_IN0): the cut leans aft with height
  translate([X_TAIL + TAIL_SLANT * -Z_IN0, 0, 0]) multmatrix([[1, 0, TAIL_SLANT, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    translate([0, -3000, -3000]) cube([6000, 6000, 6000]);
}

// ---- the unit: plain silhouette ---------------------------------------------------------
module unit_raw() translate(U_POS) {
  cube(U);                                                                        // frame + plates + deck as one block
  translate([-U_BAT[0], U[1] / 2 - U_BAT[1] / 2, U_BAT_Z0]) cube(U_BAT);         // battery block on the aft end
  translate([U_CASE_C[0] - U_CASE[0] / 2, U_CASE_C[1] - U_CASE[1] / 2, U[2]]) cube(U_CASE);   // compute case block
  translate([U_DOME_C[0], U_DOME_C[1], U[2]]) { cylinder(d = U_PED_D, h = U_PED_H, $fn = 48);
    translate([0, 0, U_PED_H]) intersection() { sphere(d = U_DOME_D, $fn = 64); translate([-U_DOME_D, -U_DOME_D, 0]) cube(2 * U_DOME_D); } }
}

// ---- ghost airframe: the "you are here" locator -----------------------------------------
// Side proportions traced from the site's generic high-wing side-profile art (viewBox 1200 x 430, nose at
// svg x 1118, tail post at 150): GH_S mm per svg unit, scene x = 0 sits at svg x GH_X0, the shell bottom at
// svg y GH_Y0.  Fuselage stations are [svg_x, top_y, bottom_y, width_mm]; the two cabin stations use the
// scene's own outer section so the cut-away sits exactly inside the hull (roof break moved aft to the
// bulkhead station for that reason).  Everything else: invented round numbers.
GH_S = 8.05;  GH_X0 = 775;  GH_Y0 = 322;  GH_Z0 = -(BELLY + WALL);
function gx(sx) = (sx - GH_X0) * GH_S;
function gz(sy) = GH_Z0 + (GH_Y0 - sy) * GH_S;
GH_STA = [[1118, 258, 266, 130], [1095, 247, 284, 520], [1072, 235, 298, 760], [1000, 221, 320, 950], [950, 211, 324, 1030],
          [894, 0, 0, 0], [660, 0, 0, 0],                                   // cabin stations: sec_out()
          [520, 215, 303, 720], [400, 230, 290, 460], [280, 243, 277, 300], [150, 252, 275, 150]];
GH_WLE = gx(958);  GH_WZ = 1150;  GH_SPAN2 = 5450;  GH_WBREAK = 2700;  GH_DIHED = 1.5;   // wing: LE x, root centre z, semi-span, taper break, dihedral deg
GH_CHORD = [1750, 1150];  GH_WT = [200, 140];                                            // root / tip chord and thickness
GH_STAB_SPAN2 = 1700;  GH_STAB_SWEEP = 250;  GH_FIN_T = 50;
GH_GEAR_Y = 1300;  GH_WHEEL_W = 150;
echo(str("GHOST: length ", gx(1118) - gx(150), " | span ", 2 * GH_SPAN2, " | cabin section inside hull x ", gx(660), "..", gx(894)));
assert(gx(660) <= X_BULK - 1 && gx(894) >= X_FWD, "cabin section outside the ghost's flat cabin stations");
assert(!ghost_fit || (gz(215) > (Z_IN0 + Z_IN1) / 2 + TAIL_RISE + TAIL_H / 2 + WALL && gz(303) < (Z_IN0 + Z_IN1) / 2 + TAIL_RISE - TAIL_H / 2 - WALL),
       "tailcone end section outside the ghost hull at the svg-520 station");

module gh_sec(s) { if (s[3] == 0) sec_out(); else { h = gz(s[1]) - gz(s[2]); translate([0, (gz(s[1]) + gz(s[2])) / 2]) rrect(s[3], h, min(s[3], h) * 0.42); } }
module gh_fuselage() for (i = [0 : len(GH_STA) - 2]) hull() { slice_at(gx(GH_STA[i][0])) gh_sec(GH_STA[i]); slice_at(gx(GH_STA[i + 1][0])) gh_sec(GH_STA[i + 1]); }
module gh_fin() rotate([90, 0, 0]) translate([0, 0, -GH_FIN_T / 2]) linear_extrude(GH_FIN_T)
  polygon([[gx(352), gz(240)], [gx(244), gz(92)], [gx(178), gz(88)], [gx(150), gz(252)], [gx(150), gz(262)], [gx(352), gz(262)]]);
module gh_stab() { xle = gx(318); xte = gx(128); tc = 0.6 * (xle - xte); sw = GH_STAB_SWEEP; hs = GH_STAB_SPAN2;
  translate([0, 0, gz(263) - 35]) linear_extrude(70)
    polygon([[xle - sw, -hs], [xle, -350], [xle, 350], [xle - sw, hs], [xle - sw - tc, hs], [xte, 350], [xte, -350], [xle - sw - tc, -hs]]); }
module slice_y(y) translate([0, y, 0]) rotate([90, 0, 0]) linear_extrude(0.01) children();
module gh_airfoil(chord, t) hull() { translate([GH_WLE - t / 2, 0]) circle(d = t, $fn = 32); translate([GH_WLE - chord, -1]) square([2, 2]); }
module gh_wing() for (s = [-1, 1]) {
  hull() { slice_y(0) translate([0, GH_WZ]) gh_airfoil(GH_CHORD[0], GH_WT[0]);
           slice_y(s * GH_WBREAK) translate([0, GH_WZ + GH_WBREAK * tan(GH_DIHED)]) gh_airfoil(GH_CHORD[0], GH_WT[0]); }
  hull() { slice_y(s * GH_WBREAK) translate([0, GH_WZ + GH_WBREAK * tan(GH_DIHED)]) gh_airfoil(GH_CHORD[0], GH_WT[0]);
           slice_y(s * GH_SPAN2) translate([0, GH_WZ + GH_SPAN2 * tan(GH_DIHED)]) gh_airfoil(GH_CHORD[1], GH_WT[1]); }
}
module gh_rod(a, b, d) hull() { translate(a) sphere(d = d, $fn = 16); translate(b) sphere(d = d, $fn = 16); }
module gh_strut(s) gh_rod([gx(888), s * 450, -120], [gx(858), s * 2650, GH_WZ + 2650 * tan(GH_DIHED) - 70], 45);
module gh_main_gear(s) { gh_rod([gx(862), s * 420, -140], [gx(826), s * GH_GEAR_Y, gz(380)], 50);
  translate([gx(818), s * GH_GEAR_Y, gz(390)]) rotate([90, 0, 0]) cylinder(r = 24 * GH_S, h = GH_WHEEL_W, center = true, $fn = 48); }
module gh_nose_gear() { translate([gx(1010), 0, gz(372)]) cylinder(d = 50, h = gz(372) * -1 - 150, $fn = 16);
  translate([gx(1010), 0, gz(392)]) rotate([90, 0, 0]) cylinder(r = 22 * GH_S, h = GH_WHEEL_W - 20, center = true, $fn = 48); }
module gh_prop() translate([gx(1104), 0, gz(262)]) rotate([0, 90, 0]) cylinder(r = 104 * GH_S, h = 12, center = true, $fn = 96);
module ghost_raw() { gh_fuselage(); gh_fin(); gh_stab(); for (s = [-1, 1]) { gh_strut(s); gh_main_gear(s); } gh_nose_gear(); gh_prop(); }
// the wing is its own group so its hidden-line pass does not hide the fuselage under it (plan / iso ghost)

// ---- cut-aways --------------------------------------------------------------------------
module keep_iso()     union() { translate([-4000, -4000, -4000]) cube([8000, 4000 + ISO_Y, 8000]); translate([-4000, -4000, -4000]) cube([8000, 8000, 4000 + ISO_SILL]); }
module keep_section() translate([-4000, -8000, -4000]) cube([8000, 8000, 8000]);           // y <= 0
module keep_plan()    translate([-4000, -4000, -8000]) cube([8000, 8000, 8000 + PLAN_Z]);  // z <= PLAN_Z
module cut_shell(apply_iso = true) {
  if (cut == "iso" && apply_iso) intersection() { children(); keep_iso(); }
  else if (cut == "section") intersection() { children(); keep_section(); }
  else if (cut == "plan") intersection() { children(); keep_plan(); }
  else children();
}

if (grp == "all" || grp == "cabin") color([0.93, 0.94, 0.96]) cut_shell() cabin_raw();
if (grp == "all" || grp == "tail")  color([0.96, 0.97, 0.98]) cut_shell(apply_iso = false) tail_raw();   // tail stays whole in the iso cut-away
if (grp == "all" || grp == "unit")  color([0.98, 0.98, 0.99]) unit_raw();                                // the unit is never sectioned
if (grp == "ghost") ghost_raw();                                                                          // never cut; rendered as its own faint layer
if (grp == "ghost_wing") gh_wing();
