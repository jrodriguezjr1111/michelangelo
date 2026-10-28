/* ======================================================================
   SEAT-RAIL FIXTURE — SEGMENT 2 "DG-B": the Digiducer sidecar (concept B)
   ----------------------------------------------------------------------
   200 mm rail replica laid out as the concept-B PAIR: the rev E base at
   "E0" (x = 22, bands 35.3 / 70.3 / 105.3) and the Digiducer sidecar
   block (48 long, bands at 10 / 38 from its aft end) 8 mm forward of it
   at "DG0" (x = 130, bands 140 / 168) — the node_gap the sidecar was
   designed with.  The sidecar fits alone on its two slots; with the node
   also on, the wrench ring / gap / stud-to-IMU-row distance can be
   checked for real.  Layout only; geometry in seat_rail_fixture_lib.scad.
   ====================================================================== */
part      = "seg";
seg_label = "SEG 2 DG-B";
rail_L    = 200;
E0        = 22;                                   // rev E base aft end
node_gap  = 8;                                    // make_digiducer_sidecar.scad node_gap (REQ-4.3 >= 5)
DG0       = E0 + 100 + node_gap;                  // 130: sidecar block aft end
node_tun  = [13.3, 48.3, 83.3];                   // make_vib01_revE.scad tun_x (COPY — build script checks it)
dg_tun    = [10, 38];                             // make_digiducer_sidecar.scad tun_x (COPY — build script checks it)
stations  = concat([for (t = node_tun) E0 + t], [for (t = dg_tun) DG0 + t]);   // 35.3 70.3 105.3 140 168
datums    = [[E0, "E0"], [DG0, "DG0"], [DG0 + 48, "DG1"]];
hole_x0   = 10.7;
fit_parts = [["../vib01_node/vib01e_base.stl", E0, node_tun, 36.4],
             ["../digiducer_mount/digiducer_sidecar_pla.stl", DG0, dg_tun, 18]];

include <seat_rail_fixture_lib.scad>
