// ============================================================================
// CyberWing — TUBE PLATFORM SYSTEM ASSEMBLY (rev B)
//
// A SCENE, not a part.  Nothing here is printed and nothing here re-derives a
// dimension: every solid is the real part module and every number is read back
// out of the part file through the asm_shim_*.scad accessors.  The authorities
// stay:
//     tube_platform/make_tube_platform.scad          (platform rev B)
//     slimrig_mounts/make_nano_tube_plate.scad       (Nano plate)
//     slimrig_mounts/make_orin_tube_plate.scad       (Orin plate)
//
// WHAT IS SHOWN
//   - the SlimRig tube pair (Ø15.0, 60 c-c) on the platform datum
//   - the two mirror rail clamps + their 4 canon caps, correctly mated
//   - the 94x134x7 plate, the RTK tower, the cable-wall fence, the hanging
//     ESP32 carrier + its 2 retainer bars, and every printed Ø7x6 spacer
//   - ghosted board envelopes (EG25-G, FlyCatcher, ZED-F9P, breadboard, ESP32)
//   - THE JETSON NANO on its own nano_tube_plate, inserted from the NORTH into
//     the 54 mm under-plate corridor up to its stop on the rail faces
//   - (part="orin_option") the Jetson Orin on its orin_tube_plate at its
//     earliest non-interfering station on the SAME tube pair — NOT in the
//     default scene; see the ORIN note below.
//
// *** CAP MATING — this scene does NOT reproduce the part file's view bug. ***
//   make_tube_platform.scad's own assembly() places the 4 rail caps with
//   `rotate([0,0,90]) rotate([90,0,0]) rotate([0,90,0])`, which resolves to
//   (x,y,z) -> (-x,z,y): the cap's trough ends up running ACROSS the tube
//   instead of along it, and the cap lies flat, 11 mm north of its bolt line.
//   Display-only (part="clamps" / "caps_spacers" are unaffected and the
//   PRINTED parts are correct), but it hides the cap's real intrusion into the
//   Nano corridor, so this scene mates them properly with `rotate([-90,0,90])`
//   at x = TUBE_X - PINCH.  Checked: the cap heat-set axes land exactly on the
//   rail bolt axes at z = TZ +/- BOLT_DX, and the 1.0 mm pinch gap is present.
//
// *** ORIN — not co-mounted in the default scene, and why (quantified). ***
//   The Orin plate is 102 long on the tube axis.  Everything from y = +14.7
//   (rail north face) to y = -91 (carrier south edge) is taken: the rails own
//   the keep-out band, and south of it the hanging carrier drops 30 mm into
//   the 54 mm corridor, leaving 24 — less than the Orin's own 17.3 seat stack
//   plus any board.  The first free station is therefore north edge at y = -91,
//   centre y = -142, which needs ~285 mm of tube between the Orin's south edge
//   and the Nano's north edge before any end margin.  No repo file states the
//   tube length, so part="orin_option" draws that case with the tubes extended
//   and the default scene leaves the Orin out.
//
// part = "assembled" | "exploded" | "elevation" | "plan" | "orin_option"
// ============================================================================
use <asm_shim_tp.scad>
use <asm_shim_nano.scad>
use <asm_shim_orin.scad>

$fn = 52;
part = "assembled";
SHOW_DIMS = true;                            // corridor / margin witness bars

// ---------------------------------------------------------------------------
// DATUM (platform frame): plate underside z = 0, plate top z = PL_T,
// tubes run along Y at x = +/- TUBE_X, tube axis z = TZ.
// ---------------------------------------------------------------------------
PL_X = tp_PL_X();  PL_Y = tp_PL_Y();  PL_T = tp_PL_T();
TZ   = tp_TZ();    BR   = tp_BR();    TUBE_X = tp_TUBE_X();
GAP  = tp_CABLE_GAP();
TUBE_TOP = TZ + BR;                          // -54, the corridor floor

// ---- Nano placement -------------------------------------------------------
// Nano plate frame: tube axes along X at y = +/- TUBE_Y, z = -ST_DEP.  Rotate
// 90 about Z to put its tube axis on the platform's Y, drop it so the tube
// axes coincide, then slide it north until its south edge lands on the rail
// north faces (BAND_N) — the physical insertion stop.
NN_DZ  = TZ + nn_ST_DEP();                             // -49.7
NN_TY  = tp_BAND_N() + nn_PL_X()/2;                    //  52.7 fully inserted
NN_SEAT       = nn_ST_DEP() - nn_BR();                 //   4.3 crown -> underside
NN_STACK_BASE = NN_SEAT + nn_PL_T() + nn_SP_H();       //  17.3 seat+plate+spacer
NANO_ENV_H    = tp_NANO_OVER_TUBE() - NN_STACK_BASE;   //  36   board+SoM+heatsink
NANO_MARGIN   = GAP - tp_NANO_OVER_TUBE();             //   0.7

// ---- Orin placement (option view only) ------------------------------------
OO_DZ = TZ + oo_ST_DEP();
OO_TY = tp_CAR()[1] - oo_PL_X()/2;                     // north edge on carrier S

// ---- cross-file interface asserts (the whole point of an assembly) --------
assert(nn_TUBE_D() == tp_TUBE_D() && oo_TUBE_D() == tp_TUBE_D(),
       "tube diameter disagrees between the platform and a tube plate");
assert(nn_BR() == tp_BR() && oo_BR() == tp_BR(), "trough radius disagrees");
assert(nn_TUBE_Y() == tp_TUBE_X() && oo_TUBE_Y() == tp_TUBE_X(),
       "tube centre-to-centre disagrees between the platform and a tube plate");
assert(nn_CAP_T() == tp_CAP_T() && nn_PINCH() == tp_PINCH(),
       "canon cap is no longer interchangeable across the family");
assert(nn_BOLT_DY() == tp_BOLT_DX(), "cap bolt spacing diverged");
assert(NANO_ENV_H > 0, "Nano seat stack already exceeds NANO_OVER_TUBE");
assert(NANO_MARGIN >= 0.5, "Nano stack does not clear the corridor");

echo(str("ASSEMBLY datum: plate underside z0, plate top z", PL_T,
         ", tube axis z", TZ, ", corridor floor z", TUBE_TOP, " (", GAP, " clear)"));
echo(str("NANO: frame dz ", NN_DZ, ", inserted centre y ", NN_TY,
         "; seat ", NN_SEAT, " + plate ", nn_PL_T(), " + spacer ", nn_SP_H(),
         " = ", NN_STACK_BASE, " -> board/heatsink envelope ", NANO_ENV_H,
         "; total ", tp_NANO_OVER_TUBE(), " vs corridor ", GAP,
         " -> margin ", NANO_MARGIN));
echo(str("NANO board ", nn_BRD_W(), " (tube axis) x ", nn_BRD_L(),
         " (across) is CENTRED on its plate -> spans y ", NN_TY-nn_BRD_W()/2,
         "..", NN_TY+nn_BRD_W()/2, ".  It therefore overhangs the plate SOUTH by ",
         nn_BRD_W()/2 - nn_PL_X()/2, ", i.e. ",
         tp_BAND_N()-(NN_TY-nn_BRD_W()/2), " PAST the rail stop face; it clears ",
         "because the board underside sits ",
         (NN_DZ + nn_PL_T() + nn_SP_H()) - (TZ + 17),
         " above the rail top.  (make_tube_platform.scad's own ghost draws this ",
         "board 2 mm NORTH of the plate edge instead of centred.)"));
echo(str("ORIN co-mount option: centre y ", OO_TY, ", spans y ",
         OO_TY-oo_PL_X()/2, "..", OO_TY+oo_PL_X()/2,
         "; tube run needed Orin-south -> Nano-north = ",
         (NN_TY + nn_PL_X()/2) - (OO_TY - oo_PL_X()/2), " mm"));

// ===========================================================================
// PALETTE
// ===========================================================================
C_PLATE  = "DarkKhaki";      C_FENCE   = "SteelBlue";
C_TOWER  = "MediumPurple";   C_CARRIER = "IndianRed";
C_BAR    = "Firebrick";      C_RAIL    = "Goldenrod";
C_CAP    = "LimeGreen";      C_SPACER  = "Sienna";
C_NPLATE = "DarkTurquoise";  C_NCAP    = "MediumSpringGreen";
C_OPLATE = "SlateBlue";
C_TUBE   = [0.45, 0.55, 0.62, 0.55];

// ===========================================================================
// SUB-ASSEMBLIES
// ===========================================================================
module tubes(y0, y1) {
  color(C_TUBE) for (sx = [-1, 1])
    translate([sx*TUBE_X, y0, TZ]) rotate([-90, 0, 0])
      cylinder(d = tp_TUBE_D(), h = y1 - y0);
}

// west rail drawn at its true place; east is the mirror.  ex = explode, outboard
module rails(ex = 0) {
  color(C_RAIL) {
    translate([-ex, 0, 0]) tp_west_rail();
    translate([ ex, 0, 0]) mirror([1, 0, 0]) tp_west_rail();
  }
}

// the 4 canon caps, correctly mated (see header note); ex pulls them outboard
module rail_caps(ex = 0) {
  color(C_CAP) for (sx = [-1, 1], cy = tp_CAPY())
    translate([sx*(TUBE_X - tp_PINCH() + ex), cy, TZ])
      rotate([-90, 0, 90]) tp_cap();
}

module spacers_lvl1() {
  color(C_SPACER) for (p = concat(tp_EG_INS(), tp_FC_INS()))
    translate([p[0], p[1], PL_T]) tp_spacer();
}
module spacers_rtk() {
  color(C_SPACER) for (p = tp_RTK_INS())
    translate([p[0], p[1], PL_T + tp_TWR_H() + tp_TWR_T()]) tp_spacer();
}

module hanging_carrier() { color(C_CARRIER) mirror([0, 0, 1]) tp_carrier(); }
module retainer_bars() {
  color(C_BAR) for (by = tp_CAR_BAR_Y())
    translate([0, by, -(tp_CAR_T() + tp_BB_T())]) mirror([0, 0, 1]) tp_retainer_bar();
}

// -- ghosted component envelopes (all numbers via the shim) ----------------
module ghost_eg25() {
  EG = tp_EG_C(); EB = tp_EG_BRD();
  color([0.20, 0.60, 1.00, 0.35])
    translate([EG[0]-EB[0]/2, EG[1]-EB[1]/2, PL_T + tp_SP_H()])
      cube([EB[0], EB[1], tp_EG_H()]);
}
module ghost_fc() {
  FC = tp_FC_C(); FB = tp_FC_BRD();
  color([1.00, 0.45, 0.20, 0.35])
    translate([FC[0]-FB[0]/2, FC[1]-FB[1]/2, PL_T + tp_SP_H()])
      cube([FB[0], FB[1], tp_FC_H()]);
}
module ghost_rtk() {
  RC = tp_RTK_C(); RB = tp_RTK_BRD();
  color([0.20, 0.90, 0.40, 0.40])
    translate([RC[0]-RB/2, RC[1]-RB/2, PL_T + tp_TWR_H() + tp_TWR_T() + tp_SP_H()])
      cube([RB, RB, tp_RTK_H()]);
}
module ghost_breadboard() {
  CAR = tp_CAR();
  color([0.90, 0.90, 0.20, 0.45])
    translate([CAR[0]+tp_CAR_W(), CAR[1]+tp_CAR_EW(), -tp_CAR_T()-tp_BB_T()])
      cube([CAR[2]-CAR[0]-2*tp_CAR_W(), CAR[3]-CAR[1]-2*tp_CAR_EW(), tp_BB_T()]);
}
module ghost_esp32() {
  CAR = tp_CAR();
  color([0.90, 0.50, 0.10, 0.45])
    translate([-18, CAR[1]+20, -tp_CAR_DEPTH()]) cube([36, 60, tp_ESP_DROP()]);
}

// -- the Nano group, in ITS OWN frame; the caller places it ----------------
module nano_group(ghosts = true) {
  color(C_NPLATE) nn_plate();
  color(C_NCAP) for (sy = [-1, 1])
    translate([0, sy*nn_TUBE_Y(), -nn_ST_DEP() - nn_PINCH()]) nn_cap();
  color(C_SPACER) for (sx = [-1, 1], sy = [-1, 1])
    translate([sx*nn_NANO_X(), sy*nn_NANO_Y(), nn_PL_T()]) nn_spacer();
  if (ghosts)
    color([0.30, 0.90, 0.50, 0.32])                 // board + SoM + heatsink env
      translate([-nn_BRD_W()/2, -nn_BRD_L()/2, nn_PL_T() + nn_SP_H()])
        cube([nn_BRD_W(), nn_BRD_L(), NANO_ENV_H]);
}
module nano_placed(slide = 0, ghosts = true) {
  translate([0, NN_TY + slide, NN_DZ]) rotate([0, 0, 90]) nano_group(ghosts);
}

module orin_group(ghosts = true) {
  color(C_OPLATE) oo_plate();
  color(C_NCAP) for (sy = [-1, 1])
    translate([0, sy*oo_TUBE_Y(), -oo_ST_DEP() - oo_PINCH()]) oo_cap();
  color(C_SPACER) for (sx = [-1, 1], sy = [-1, 1])
    translate([sx*oo_ORIN_X(), sy*oo_ORIN_Y(), oo_PL_T()]) oo_spacer();
  if (ghosts)
    color([0.55, 0.45, 0.95, 0.32])
      translate([-oo_BRD_L()/2, -oo_BRD_W()/2, oo_PL_T() + oo_SP_H()])
        cube([oo_BRD_L(), oo_BRD_W(), 1.6]);
}
module orin_placed(ghosts = true) {
  translate([0, OO_TY, OO_DZ]) rotate([0, 0, 90]) orin_group(ghosts);
}

// -- witness bars: the corridor and the margins that define it -------------
// RED    = 54.0  clear corridor, tube top -> plate underside   (at y =  12)
// CYAN   = 53.3  Nano stack over the tube top -> 0.7 margin    (at y =  40)
// YELLOW = 24.0  corridor left under the hanging carrier       (at y = -60)
module dim_bars() {
  wx = -PL_X/2 - 9;
  color([1, 0.15, 0.15, 0.95])
    translate([wx,  12, TUBE_TOP]) cube([3, 3, GAP]);
  color([0.05, 0.7, 1, 0.95])
    translate([wx,  40, TUBE_TOP]) cube([3, 3, tp_NANO_OVER_TUBE()]);
  color([1, 0.85, 0.1, 0.95])
    translate([wx, -60, TUBE_TOP]) cube([3, 3, GAP - tp_CAR_DEPTH()]);
}

// ===========================================================================
// SCENE
// ===========================================================================
module scene(ex = 0, nano_slide = 0, with_orin = false, ghosts = true,
             dims = true) {
  ty0 = with_orin ? OO_TY - oo_PL_X()/2 - 25 : min(-PL_Y/2, tp_CAR()[1]) - 25;
  ty1 = NN_TY + nn_PL_X()/2 + nano_slide + 25;
  tubes(ty0, ty1);

  rails(ex * 45);
  rail_caps(ex * 25);

  color(C_PLATE) tp_plate();
  translate([0, 0, PL_T + ex*34])                       color(C_FENCE) tp_fence();
  translate([0, 0, PL_T + tp_TWR_H() + ex*54])          color(C_TOWER) tp_tower();
  translate([0, 0, ex*26]) spacers_lvl1();
  translate([0, 0, ex*64]) spacers_rtk();
  translate([0, 0, -ex*42]) hanging_carrier();
  translate([0, 0, -ex*62]) retainer_bars();

  if (ghosts) {
    translate([0, 0, ex*26]) { ghost_eg25(); ghost_fc(); }
    translate([0, 0, ex*64]) ghost_rtk();
    translate([0, 0, -ex*42]) ghost_breadboard();
    translate([0, 0, -ex*52]) ghost_esp32();
  }

  nano_placed(nano_slide, ghosts);
  if (with_orin) orin_placed(ghosts);
  if (dims && SHOW_DIMS) dim_bars();
}

// ===========================================================================
if (part == "assembled")   scene(dims = false);
if (part == "exploded")    scene(ex = 1, nano_slide = 96, dims = false);
if (part == "elevation")   scene(dims = true);
if (part == "plan")        scene(dims = false);
if (part == "orin_option") scene(with_orin = true, dims = false);
