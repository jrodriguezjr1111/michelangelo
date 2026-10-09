// ============================================================================
// AS-BUILT CAGE (photo 39, 2026-09-29) — the owner's two-bay 2020 frame, measured
// straight-on (keystone-corrected, 20 mm gusset bolt pitch + 20 mm rails as rulers):
//   long face ~444.5 (17.5 in, EST 442 +/- 5), depth 279 (E deck, CONFIRM)
//   deck rail z 0-20, mid rail 125.5-145.5 (slot pitch 125.5), top rail 211.5-231.5 (pitch 86)
//   front/back-face gussets: L 62 x 60 at deck + top corners, T 62 x +/-30 at the mid rail
// Contents as photographed: two aluminium cases SIDE BY SIDE in the lower bay, I/O faces
// to the front; CO node between them; V-mount + battery at the right end; antenna plate
// (MA963) + GNSS dome on the mid rail.  Panels: the rev B family (make_t1_panels_revB.scad).
//   bay = "lowerbay" : UPPER (badge) rev B on the FRONT of the lower bay (captive thumbscrews,
//                      cable notch) + the rev B CO panel on the BACK of the lower bay
//   bay = "upperbay" : UPPER (badge) rev B as the brow on the FRONT of the upper bay
//   bay = "pair"     : THE DECIDED PLACEMENT (owner 2026-09-28): both on the FRONT face — CO rev B (vented,
//                      plain louver over the node, fix per make_t1_panels_revB `fix`) on the lower bay, badge brow on the upper bay
// Read-only use of every other file.
// ============================================================================
use <../t1_concepts.scad>
use <make_t1_panels_revB.scad>
use <../t1_stack/make_t1_stack.scad>
bay = "lowerbay";
FL = 444.5; DP = 279; RZ = [0, 125.5, 211.5]; EE = 20;
X0P = (FL - 304.8) / 2;
C_EXT = [0.15, 0.15, 0.17]; C_GUS = [0.2, 0.2, 0.22];
module rail_x(z, y) color(C_EXT) translate([0, y, z]) cube([FL, EE, EE]);
module rail_y(z, x) color(C_EXT) translate([x, EE, z]) cube([EE, DP - 2 * EE, EE]);
module gussets_face(y, t = 3.2) color(C_GUS) for (m = [0, 1]) translate([m * FL, y, 0]) mirror([m, 0, 0]) rotate([90, 0, 0])
  linear_extrude(t) {
    polygon([[0, 0], [62, 0], [62, 20], [22, 60], [0, 60]]);
    polygon([[0, 105.5], [20, 105.5], [62, 125.5], [62, 145.5], [20, 165.5], [0, 165.5]]);
    polygon([[0, 231.5], [62, 231.5], [62, 211.5], [22, 171.5], [0, 171.5]]);
  }
// frame
for (z = RZ) { rail_x(z, 0); rail_x(z, DP - EE); rail_y(z, 0); rail_y(z, FL - EE); }
color(C_EXT) for (x = [0, FL - EE], y = [0, DP - EE]) translate([x, y, 0]) cube([EE, EE, RZ[2] + EE]);
gussets_face(0); gussets_face(DP + 3.2);
// contents (photo 39)
translate([120, 70, 30]) rotate([0, 0, 180]) translate([0, -106, 0]) case_solid(47, true);     // Orin, I/O to the front
translate([324, 70, 30]) rotate([0, 0, 180]) translate([0, -106, 0]) case_solid(41, false);    // RTK + LTE
color([0.12, 0.12, 0.13]) translate([FL / 2 - 5 - 24, 50, 38]) cube([48, 40, 70]);              // CO node between them: x = centre - 5 (photo 39), front ~50 behind the rail plane (EST)
color([0.2, 0.2, 0.22]) translate([392, 120, 22]) cube([30, 100, 120]);                        // V-mount + battery at the right end
color([0.1, 0.1, 0.11]) translate([30, 60, RZ[1] + EE]) cube([FL - 60, 160, 5]);               // antenna plate on the mid rail
color([0.08, 0.08, 0.09]) translate([70, 80, RZ[1] + EE + 5]) cube([146, 134, 20]);            // MA963
color([0.95, 0.95, 0.93]) translate([300, 140, RZ[1] + EE + 12]) scale([1, 1, 0.3]) sphere(d = 140, $fn = 64);   // GNSS dome
// panels
if (bay == "lowerbay") {
  translate([X0P, -5.6, 0]) rotate([90, 0, 0]) upper_revB("lowerbay");
  translate([FL - X0P, DP + 5.6, 0]) rotate([0, 0, 180]) rotate([90, 0, 0]) panel_revB();
}
if (bay == "upperbay" || bay == "pair") translate([X0P, -5.6, RZ[1]]) rotate([90, 0, 0]) upper_revB("upperbay");
if (bay == "pair") translate([X0P, -5.6, 0]) rotate([90, 0, 0]) panel_revB();
