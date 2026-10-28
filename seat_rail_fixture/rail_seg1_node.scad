/* ======================================================================
   SEAT-RAIL FIXTURE — SEGMENT 1 "NODE": the rev E Feather-stack base
   ----------------------------------------------------------------------
   200 mm rail replica, the VIB-01 rev E base (100 long, three bands at
   x = 13.3 / 48.3 / 83.3 from its aft end) centred on it: aft end at the
   "E0" datum (x = 50).  Band slots at the node's three tunnel stations.
   Geometry + every number comes from seat_rail_fixture_lib.scad and
   ../digiducer_mount/rail_interface.scad — nothing is set here but the
   segment layout.  Render:  openscad -D 'part="seg"' -o rail_seg1_node.stl rail_seg1_node.scad
   ====================================================================== */
part      = "seg";            // seg | gauge | assembly | none
seg_label = "SEG 1 NODE";
rail_L    = 200;
E0        = 50;                                   // rev E base aft end on the rail
node_tun  = [13.3, 48.3, 83.3];                   // make_vib01_revE.scad tun_x (COPY — build script checks it)
stations  = [for (t = node_tun) E0 + t];          // 63.3 / 98.3 / 133.3
datums    = [[E0, "E0"], [E0 + 100, "E1"]];
hole_x0   = 10.7;                                 // first seat-stop hole; puts band 1 over a hole, band 2 between
fit_parts = [["../vib01_node/vib01e_base.stl", E0, node_tun, 36.4]];

include <seat_rail_fixture_lib.scad>
