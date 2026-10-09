// ============================================================================
// T1 PANELS on the cage — photo 38's as-built arrangement, drawn from the E
// model read-only (t1_concept_E.scad rev C deck + posts + top ring + rod level)
// plus the as-built MID-RAIL rectangle, the two aluminium cases side by side in
// the lower bay (as on the desk, I/O faces toward the front long face), and the
// two panels on the long faces of the lower bay:
//   front (y = 0, the I/O side)   : UPPER panel (CANARY badge, hex 44.8 cm2)
//   back  (y = 279)               : LOWER panel (bird + CO cassette; the cassette
//                                   reaches 19 mm into the bay — kept off the I/O cable side)
// None of the included files is edited.
// ============================================================================
include <../t1_concept_E.scad>
use <make_t1_panels.scad>
use <../t1_stack/make_t1_stack.scad>
view = "none";
rev = "C";
MID_Z0 = 110;            // as-built mid rail bottom (slot centreline z 120, EST photo 38 — same numbers as make_t1_panels)
PT = 5.6 + 6.4;          // panel face to rail plane (T + STANDOFF)
PX0 = (406 - 400.05) / 2;

module mid_rails() {                                                     // as-built mid rectangle
  for (y = [E / 2, DYE - E / 2]) translate([0, y, MID_Z0 + E / 2]) extrusion(DXE);
  for (x = [E / 2, DXE - E / 2]) translate([x, E, MID_Z0 + E / 2]) ext_y(DYE - 2 * E);
}
module front_panel(p) translate([PX0, -PT, 0]) rotate([90, 0, 0]) panel_assembled(p);
module back_panel(p)  translate([406 - PX0, DYE + PT, 0]) rotate([0, 0, 180]) rotate([90, 0, 0]) panel_assembled(p);

deck_frame();
posts_and_rods();
mid_rails();
// the two cases side by side, I/O faces toward the front (photo 38), on a rod pair
translate([70, 70, 30]) rotate([0, 0, 180]) translate([0, -106, 0]) case_solid(47, true);
translate([220, 70, 30]) rotate([0, 0, 180]) translate([0, -106, 0]) case_solid(41, false);
color([0.2, 0.2, 0.22]) translate([318, 120, 24]) cube([86, 100, 120]);           // V99 on its plate at the stack end (photo 38)
front_panel("upper");
back_panel("lower");
