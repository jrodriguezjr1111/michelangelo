// ============================================================================
// T1 PANELS on the cage — rev B lower (CO) panel replacing rev A's lower panel on
// the BACK long face; upper panel (rev A) unchanged on the front.  Same scene as
// panels_on_cage.scad (photo 38 arrangement); every included file is read-only.
// ============================================================================
include <../t1_concept_E.scad>
use <make_t1_panels.scad>
use <make_t1_panels_revB.scad>
use <../t1_stack/make_t1_stack.scad>
view = "none";
rev = "C";
MID_Z0 = 110;
PT = 5.6 + 6.4;                 // rev A upper panel: face to rail plane
PX0 = (406 - 400.05) / 2;
BX0 = (406 - 304.8) / 2;        // rev B: sits flat on the rail faces between the gussets
module mid_rails() {
  for (y = [E / 2, DYE - E / 2]) translate([0, y, MID_Z0 + E / 2]) extrusion(DXE);
  for (x = [E / 2, DXE - E / 2]) translate([x, E, MID_Z0 + E / 2]) ext_y(DYE - 2 * E);
}
module front_gussets(yface, s) color([0.45, 0.46, 0.5]) for (m = [0, 1]) translate([m * 406, 0, 0]) mirror([m, 0, 0])
  translate([0, yface, 0]) rotate([90, 0, 0]) linear_extrude(3.2) {
    polygon([[0, 0], [70, 0], [70, 20], [20, 70], [0, 70]]);
    polygon([[0, 60], [20, 60], [70, 110], [70, 130], [20, 180], [0, 180]]); }
deck_frame(); posts_and_rods(); mid_rails();
translate([70, 70, 30]) rotate([0, 0, 180]) translate([0, -106, 0]) case_solid(47, true);
translate([220, 70, 30]) rotate([0, 0, 180]) translate([0, -106, 0]) case_solid(41, false);
color([0.2, 0.2, 0.22]) translate([318, 120, 24]) cube([86, 100, 120]);
front_gussets(0, 1); translate([0, DYE + 3.2, 0]) front_gussets(0, 1);
translate([PX0, -PT, 0]) rotate([90, 0, 0]) panel_assembled("upper");
translate([406 - BX0, DYE + 5.6, 0]) rotate([0, 0, 180]) rotate([90, 0, 0]) panel_revB();   // face 5.6 off the rail plane
