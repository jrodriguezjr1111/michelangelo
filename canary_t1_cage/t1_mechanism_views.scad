// ============================================================================
// CONCEPT D — "HOW IT WORKS" VIEWS of one peripheral bay and the Core tray.
// Wrapper: includes t1_concepts.scad (primitives: fbox, comp, thumb, plate_label,
// pigtail, extrusion, ext_z, canon parameters) WITHOUT editing it; the concept
// file's own scene is switched off by overriding `concept` below.
// Everything drawn here is CONCEPT geometry (no insert bores, no fits proven);
// the numbers come from t1_params.py / the fixed layout of 2026-09-21.
//
// view = "bay_cutaway" | "cartridge_alone" | "cartridge_back" | "sequence" | "core_tray"
// ============================================================================
include <t1_concepts.scad>
concept = "none";              // silence the concept file's scene
swap = "none"; pull = 0; lid = 0; panel = 0; labels = false; show_labels = true;
view = "bay_cutaway";
$fn = 40;

// ---- the Traffic bay, cartridge-local frame: x across (0..W), y depth (0 = faceplate
//      front, +y into the frame), z up (0 = tray underside = top of the bottom long)
W = 74; D = 70; H = CART_H;                 // 96 tall; D = 70 here (56 deep FlyCatcher + 8 + 6);
                                            // t1_concepts.scad draws 44 as a massing shortcut
WALL = 4; FLOOR = 3; CLR = 0.4;
NECK = SLT - CLR; HEADW = CAV - 0.6; HEADT = 2.0; LEAD = 1.0; KEY_Y = 9;   // key centred on the mullion axis
LUG_H = 22; LUG_Z = H - 26;
FLY_PAT = [58, 49]; FLY_STD = 6;            // MEAS pattern, standoff height DSN
LEADER = [0.9, 0.9, 0.9]; KEY_COL = [0.58, 0.58, 0.64];   // keys drawn lighter than the wall so they read

module key_chamfered(L) {                   // +X out of the wall face at x = 0, along +Z from z = 0
  color(KEY_COL) {
    hull() { translate([0, -NECK/2, LEAD]) cube([SLD + 0.4, NECK, L - 2*LEAD]);
             translate([0, -NECK/2 + LEAD, 0]) cube([SLD + 0.4, NECK - 2*LEAD, L]); }
    hull() { translate([SLD + 0.39, -HEADW/2, LEAD]) cube([HEADT, HEADW, L - 2*LEAD]);
             translate([SLD + 0.39, -HEADW/2 + LEAD, 0]) cube([HEADT - 0.6, HEADW - 2*LEAD, L]); }
  }
}
module mullion_cut(len) {                   // same section as t1_concepts extrusion(), drawn lighter and half-sectioned (y > centre removed)
  color([0.42, 0.43, 0.48]) difference() {
    rotate([0, -90, 0]) difference() {
      translate([0, -E/2, -E/2]) cube([len, E, E]);
      for (r = [0, 90, 180, 270]) rotate([r, 0, 0]) {
        translate([-1, -SLT/2, E/2 - SLD]) cube([len + 2, SLT, SLD + 1]);
        translate([-1, -CAV/2, E/2 - SLD - 2.5]) cube([len + 2, CAV, 2.5]);
      }
      rotate([0, 90, 0]) translate([0, 0, -1]) cylinder(d = 4.2, h = len + 2);
    }
    translate([-E, 0, -1]) cube([2*E, 2*E, len + 2]);
  }
}
module standoff() { color([0.85, 0.75, 0.3]) difference() { cylinder(d = 6, h = FLY_STD, $fn = 6); translate([0, 0, -1]) cylinder(d = 2.5, h = FLY_STD + 2); } }

module traffic_cartridge(screw = true) {
  color(BLK) fbox([W - 1, 5, H], 1.5);                                            // faceted faceplate
  color(BLK) for (x = [0, W - 1 - WALL]) translate([x, 5, 0]) cube([WALL, D - 5, H]);   // side walls
  color(BLK2) translate([WALL, 5, 0]) cube([W - 1 - 2*WALL, D - 5, FLOOR]);      // tray floor
  color(BLK2) translate([WALL, D - 3, 0]) cube([W - 1 - 2*WALL, 3, 30]);          // low back lip (pigtail exit above it)
  translate([0, KEY_Y, 4]) mirror([1, 0, 0]) key_chamfered(H - 8);               // T-keys, both side walls
  translate([W - 1, KEY_Y, 4]) key_chamfered(H - 8);
  color(BLK2) translate([WALL + 12, 24, -2]) cube([5, D - 30, 2]);                // KEYING RIB under the floor, behind the
                                                                                    // bottom long (bay-specific x); lands in the
                                                                                    // groove of the bay key plate, else sits 2 proud
  // FlyCatcher on four M3 standoffs on its MEASURED 58 x 49 pattern
  translate([(W - 1)/2, 5 + 4 + FLY[1]/2, FLOOR]) {
    for (sx = [-1, 1], sy = [-1, 1]) translate([sx * FLY_PAT[0]/2, sy * FLY_PAT[1]/2, 0]) standoff();
    translate([-FLY[0]/2, -FLY[1]/2, FLY_STD]) comp(FLY, PCB);
  }
  // faceplate RETURN LUG over the right mullion's front face; thumbscrew through it into the T-nut
  color(BLK) difference() {
    translate([W - 1, -1, LUG_Z]) cube([20, 6, LUG_H]);
    translate([W - 1 + 10, -3, LUG_Z + LUG_H/2]) rotate([-90, 0, 0]) cylinder(d = 5.4, h = 10);
  }
  if (screw) translate([W - 1 + 10, -1, LUG_Z + LUG_H/2]) rotate([90, 0, 0]) thumb(10, 6);
  color(YEL) translate([6, -7, H - 18]) fbox([10, 8, 7], 1);                      // pull tab
  translate([(W - 1)/2, -0.4, H/2]) rotate([90, 0, 0]) plate_label(lbl("TRAFFIC"), 50, 9);
  translate([(W - 1)/2 + 12, D, 36]) pigtail(22);                                 // pigtail out the back, locking connector
}

// ---- mullions + bottom long around the bay (frame parts), same local frame
module bay_frame(cut_left = false) {
  // bottom long M01 runs along X under the front 20 mm of the cartridge (y -1..19)
  translate([-30, KEY_Y, -E/2]) extrusion(W + 60);
  // right mullion (slot faces -X, into the cartridge)
  translate([W - 1 + E/2 + CLR/2, KEY_Y, 0]) ext_z(H + 10);
  // left mullion, optionally cut at its centre plane so the slot cavity shows
  if (cut_left) translate([-E/2 - CLR/2, KEY_Y, 0]) mullion_cut(H + 10);   // lengthwise half-section, lighter so the cut face reads
  else translate([-E/2 - CLR/2, KEY_Y, 0]) ext_z(H + 10);
  // bay KEY PLATE: printed, bolted into the bottom long's top slot behind the mullion line (1 x M5 + 14122);
  // one groove at this bay's rib position - a wrong cartridge sits 2 mm proud and the thumbscrew cannot reach its nut
  color(BLK) translate([WALL, KEY_Y + E/2 + 1, -2]) difference() { cube([W - 1 - 2*WALL, 30, 2]); translate([12 - 0.3, -1, -1]) cube([5.6, 32, 4]); }
  // T-nut in the right mullion's front slot, behind the lug
  color([0.55, 0.56, 0.6]) translate([W - 1 + E/2 + CLR/2 - 5.2, KEY_Y - E/2 + 0.2, LUG_Z + LUG_H/2 - 6]) cube([10.4, SLD + 2.3, 12]);
}

module marker(n, at, from) {                // numbered marker: yellow ball + n white beads stacked above it; leader to the feature
  color(YEL) translate(at) sphere(4, $fn = 24);
  color([1, 1, 1]) for (i = [1 : n]) translate([at[0], at[1], at[2] + 4 + i * 4.2]) sphere(1.7, $fn = 16);
  color(LEADER) hull() { translate(from) sphere(0.6, $fn = 8); translate(at) sphere(0.6, $fn = 8); }
}

// =========================================================================== views
if (view == "bay_cutaway") {
  bay_frame(cut_left = true);
  traffic_cartridge();
  marker(1, [-40, 30, H - 6],  [-6, KEY_Y + 2, H - 40]);       // 1 T-key in the slot cavity (sectioned mullion)
  marker(2, [W/2 + 10, D + 30, -14], [W/2 + 10, D - 6, FLOOR]); // 2 tray floor
  marker(3, [W + 36, 20, H + 14], [W - 1 + 10, -6, LUG_Z + LUG_H/2]);   // 3 thumbscrew -> T-nut in the mullion's front slot
  marker(4, [-30, -14, H - 30], [8, -7, H - 14]);               // 4 pull tab
  marker(5, [W + 30, D + 36, 34], [(W - 1)/2 + 12, D + 22, 36]); // 5 pigtail + locking connector
  marker(6, [W/2 - 20, D + 30, H + 24], [W/2 - 20, 40, FLOOR + FLY_STD + 10]);   // 6 FlyCatcher on 4 standoffs, 58 x 49
  marker(7, [-30, 60, -16], [WALL + 14, 50, -2]);               // 7 keying rib under the floor / bay key plate
}
if (view == "cartridge_alone") traffic_cartridge();
if (view == "cartridge_back")  traffic_cartridge();
if (view == "sequence") {
  for (i = [0 : 2]) translate([i * (W + 70), 0, 0]) {
    bay_frame(cut_left = false);
    translate([0, 0, [0, 40, H + 24][i]]) traffic_cartridge(screw = i == 0);
    if (i > 0) translate([W - 1 + 10, -40, LUG_Z + LUG_H/2 + [0, 40, H + 24][i]]) rotate([90, 0, 0]) thumb(10, 6);   // screw out
    color(YEL) translate([(W - 1)/2, -14, -30]) rotate([90, 0, 0]) linear_extrude(0.6)
      text(["1  SEATED", "2  SCREW OUT, LIFT 40", "3  CLEAR - THE SLOT IS THE RAIL"][i], size = 5, font = "DIN Condensed:style=Bold", halign = "center");
  }
}
if (view == "core_tray") {
  // frame corner: bottom longs M01/M02 (inner slots = the track), -X end member M03 = 130 (5 mm gaps so the
  // tray walls can pass), posts M05/M07, top end tie M09
  for (y = [-1, 1]) translate([0, y * (DY - E)/2, E/2]) extrusion(200);
  translate([E/2, -65, E/2]) ext_y(130);
  for (y = [-1, 1]) translate([E/2, y * (DY - E)/2, E]) ext_z(DZ - 2*E);
  translate([E/2, -(DY - E)/2 + E, DZ - E/2]) ext_y(DY - 2*E);
  TL = HUB[0] + 16; TW = DY - 2*E - 2*CLR; PULL = 90;                              // tray 155 x 139.2
  translate([E + 2 - PULL, -TW/2, E]) {
    color(BLK2) cube([TL, TW, FLOOR]);                                             // floor at z 20..23 (clears M03)
    color([0.45, 0.45, 0.5]) for (i = [1 : 14], j = [1 : 8]) translate([6 + i * 10, 4 + j * 10, FLOOR - 0.2]) cylinder(d = 3.2, h = 0.6, $fn = 8);  // cheese-grid field under the hub (ear pattern unknown)
    color(BLK) for (y = [0, TW - WALL]) translate([0, y, -13]) cube([TL, WALL, 53]); // side walls, hanging 13 below the floor to the key line
    color(BLK2) for (sy = [0, 1]) translate([4, sy ? TW : 0, -10]) mirror([0, sy ? 0 : 1, 0])   // T-keys along X, into the longs' inner slots
      rotate([0, 90, 0]) rotate([0, 0, 90]) key_chamfered(TL - 8);
    translate([8, (TW - HUB[1])/2, FLOOR]) color(MET) cube(HUB);                   // hub on the floor
    translate([TL/2, TW/2, FLOOR + HUB[2] + 6]) {                                   // Orin deck over the hub, 4 posts, MEASURED pattern
      color(BLK2) translate([-55, -42, -4]) difference() { cube([110, 84, 4]); translate([12, 12, -1]) cube([86, 60, 6]); }
      color(BLK2) for (sx = [-1, 1], sy = [-1, 1]) translate([sx * 48 - 4, sy * 36 - 4, -HUB[2] - 6 - FLOOR + FLOOR]) cube([8, 8, HUB[2] + 6 - 4]);
      for (sx = [-1, 1], sy = [-1, 1]) translate([sx * 91.86/2, sy * 58.37/2, 0]) standoff();
      translate([-ORIN[0]/2, -ORIN[1]/2, FLY_STD]) comp(ORIN, PCB);
    }
    color(BLK) translate([-6, -6, -2]) difference() { fbox([6, TW + 12, H + 4], 1.5); for (i = [1 : 7]) translate([-1, 10, 8 + i * 12]) cube([8, TW - 8, 6]); }   // end bezel = intake louver
    translate([-6, TW + 2, H - 14]) rotate([0, -90, 0]) thumb(11, 6);
    color(YEL) translate([-6, TW/2 - 5, H - 30]) rotate([0, -90, 0]) fbox([7, 10, 8], 1);
    translate([-6.2, TW/2, 24]) rotate([90, 0, -90]) plate_label(lbl("CORE"), 60, 9);
  }
  PX = E + 2 - PULL;
  marker(1, [PX + 40, -DY/2 - 26, -18], [PX + 40, -TW/2 - 4, E - 10]);             // 1 T-keys in M01/M02 inner slots
  marker(2, [PX - 36, -DY/2 - 16, DZ - 10], [PX - 6, -TW/2 + 30, E + 60]);         // 2 end bezel = intake louver
  marker(3, [PX + TL/2 + 30, -DY/2 - 30, DZ + 10], [PX + TL/2 - 30, -24, E + FLOOR + HUB[2] + 14]);   // 3 Orin on its pattern, deck over the hub
  marker(4, [E/2 + 40, -DY/2 - 30, -30], [E/2, -66, E - 4]);                        // 4 M03 cut 130: gap lets the wall pass
  marker(5, [PX - 30, DY/2 + 6, DZ + 4], [PX - 8, TW/2 + 2, E + H - 14]);          // 5 thumbscrew -> T-nut in the post
  marker(6, [PX + 60, -DY/2 - 26, E + 4], [PX + 60, -TW/2 + 20, E + FLOOR]);        // 6 cheese-grid field under the hub (ear pattern unknown)
}
