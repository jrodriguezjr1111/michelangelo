/* ======================================================================
   SEAT-RAIL FIXTURE — SEGMENT 1 "NODE": the rev E Feather-stack base
   ----------------------------------------------------------------------
   200 mm replica of the N417ER rail (profile from rail_interface.scad —
   PROVISIONAL photo profile 2026-10-28), the rev E base on its 100 mm
   straddle-clamp deck with the aft end at datum "E0" x = 40: the clamp
   jaws (x 40..70 and 110..140) clear the end-pair bolt heads (x 6) and the
   mid-span bolt (x 150).  Geometry in seat_rail_fixture_lib.scad.
   Render:  openscad -D 'part="seg"' -o rail_seg1_node.stl rail_seg1_node.scad
   ====================================================================== */
part      = "seg";            // seg | gauge | assembly | none
seg_label = "SEG 1 NODE";
rail_L    = 200;
E0        = 40;                                   // rev E base / deck aft end on the rail
jaw_x     = [15, 85];  jaw_L = 30;                // make_rail_straddle_clamp.scad deck_L=100 (COPY — build script checks it)
node_tun  = [13.3, 48.3, 83.3];                   // make_vib01_revE.scad tun_x — inferred-profile bands only (COPY)
stations  = [for (t = node_tun) E0 + t];          // used only with rail_profile = "inferred_2026_08"
datums    = [[E0, "E0"], [E0 + 100, "E1"]];
hole_x0   = 10.7;                                 // inferred profile only
fit_parts = [["../vib01_node/vib01e_base.stl", E0, jaw_x, jaw_L, 36.4, "rail_clamp_all100.stl", 23]];

include <seat_rail_fixture_lib.scad>
