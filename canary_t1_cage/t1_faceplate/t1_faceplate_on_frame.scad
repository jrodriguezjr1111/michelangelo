// ============================================================================
// t1_faceplate — ASSEMBLED VIEW on the concept-D frame.  WRAPPER ONLY:
// the frame primitives (extrusion / ext_y / ext_z / bracket) come from
// ../t1_concepts.scad through `use`, unedited; the member layout below mirrors
// concept_D() (t1_concepts.scad, 2026-09-21) — 300 x 180 x 140, front mullions
// at x 104 / 208 (bays 74 / 84 / 62), rear mullions at 60 / 110 (30 / 30 / 160).
// Cartridges are NOT drawn: a bay holds either a cartridge or a face plate.
//   show = "all" | "front" | "rear"
// ============================================================================
use <../t1_concepts.scad>
use <make_t1_faceplate.scad>
use <../make_style_coupon.scad>

show = "all";
E = 20;  DX = 300;  DY = 180;  DZ = 140;  TOPY = DY/2 - E/2 - 30;       // = concept_D()
H = DZ - 2*E;                                                          // 100: the front opening height
BLK = [0.22, 0.22, 0.25];  YEL = [1.00, 0.80, 0.00];
FACE_Y = DY/2 + fp_t_fl();                                             // plate face 7 mm proud of the member face

// name, w, bay centre x, neighbour[top,right,bottom,left] (as seen from OUTSIDE), vent, label
FRONT = [["TRAFFIC", 74,  57, [0, 1, 0, 0], "hex",  "TRAFFIC"],
         ["LTE",     84, 156, [0, 1, 0, 1], "hex",  "LTE"],
         ["RTK",     62, 249, [0, 0, 0, 1], "none", "RTK"]];
REAR  = [["EXHAUST", 160, 200, [0, 1, 0, 0], "louver", "EXHAUST"]];   // seen from +Y, the mullion (x 100..120) is on the RIGHT

module frame_D() {                                                     // members + brackets, mirrors concept_D()
  for (y = [-1, 1]) translate([0, y * (DY - E)/2, E/2]) extrusion(DX);                       // bottom longs
  for (x = [E/2, DX - E/2]) translate([x, -(DY - E)/2 + E, E/2]) ext_y(DY - 2*E);              // bottom ends
  for (x = [E/2, DX - E/2], y = [-1, 1]) translate([x, y * (DY - E)/2, E]) ext_z(DZ - 2*E);   // corner posts
  for (x = [E/2, DX - E/2]) translate([x, -(DY - E)/2 + E, DZ - E/2]) ext_y(DY - 2*E);         // top end ties
  for (y = [-1, 1]) translate([E, y * TOPY, DZ - E/2]) extrusion(DX - 2*E);                    // top longs, set back 30
  translate([DX - 70, -TOPY + E/2, DZ - E/2]) ext_y(2*TOPY - E);                               // IMU cross member
  for (x = [104, 208]) translate([x, -(DY - E)/2, E]) ext_z(DZ - 2*E);                         // front mullions
  for (x = [60, 110]) translate([x, (DY - E)/2, E]) ext_z(DZ - 2*E);                           // rear mullions
  for (x = [E, DX - E], y = [-1, 1]) translate([x, y * (DY/2 - E), E])
    mirror([x > E ? 1 : 0, 0, 0]) mirror([0, y > 0 ? 1 : 0, 0]) bracket();
}

module plate_in_frame(p, front) {
  translate([p[2], front ? -FACE_Y : FACE_Y, E + H/2]) rotate(front ? [90, 0, 180] : [90, 0, 0]) {
    color(BLK) faceplate(w = p[1], h = H, mount = "bolt", sides = [0, 1, 1, 1], neighbour = p[3], vent = p[4],
                         vent_min_cm2 = p[4] == "louver" ? 32 : 0, grip = "top", label = true, mark = true, name = p[0]);
    color(YEL) mirror([1, 0, 0]) translate([0, fp_label_y(H), fp_lp_t() + 0.2]) mirror([0, 0, 1]) plate(p[5]);
  }
}

frame_D();
if (show != "rear") for (p = FRONT) plate_in_frame(p, true);
if (show != "front") for (p = REAR) plate_in_frame(p, false);
