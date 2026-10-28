/* ======================================================================
   SEAT-RAIL FIXTURE — SEGMENT 2 "DG-B": the Digiducer sidecar (concept B)
   ----------------------------------------------------------------------
   200 mm replica (PROVISIONAL photo profile) laid out as the concept-B
   PAIR on straddle-clamp decks: the Digiducer sidecar on its 48 mm deck
   at "DG0" x = 44 (jaws 46..62 / 74..90) and the rev E base on its 100 mm
   deck at "E0" x = 100 (jaws 100..130 / 170..200), node_gap 8.  The
   mid-span flange bolt (x 150) sits in the gap between the node's jaws;
   the end-pair bolts (x 6) are clear of everything.  The pair is aft/fwd
   mirrored vs the sidecar's own scene (block forward of the node) — the
   bolt pattern forced it; on the aircraft the bolt pattern decides.
   The sidecar fits alone on its deck.
   ====================================================================== */
part      = "seg";
seg_label = "SEG 2 DG-B";
rail_L    = 200;
node_gap  = 8;                                    // make_digiducer_sidecar.scad node_gap (REQ-4.3 >= 5)
DG0       = 44;                                   // sidecar deck aft end
E0        = DG0 + 48 + node_gap;                  // 100: rev E deck aft end
jaw_x     = [15, 85];  jaw_L = 30;                // clamp deck_L=100 (COPY — build script checks it)
dg_jaw_x  = [10, 38];  dg_jaw_L = 16;             // clamp deck_L=48  (COPY — build script checks it)
node_tun  = [13.3, 48.3, 83.3];                   // inferred-profile bands only (COPY)
dg_tun    = [10, 38];
stations  = concat([for (t = node_tun) E0 + t], [for (t = dg_tun) DG0 + t]);   // inferred profile only
datums    = [[DG0, "DG0"], [DG0 + 48, "DG1"], [E0, "E0"]];
hole_x0   = 10.7;
fit_parts = [["../vib01_node/vib01e_base.stl", E0, jaw_x, jaw_L, 36.4, "rail_clamp_all100.stl", 23],
             ["../digiducer_mount/digiducer_sidecar_pla.stl", DG0, dg_jaw_x, dg_jaw_L, 18, "rail_clamp_all48.stl", 23]];

include <seat_rail_fixture_lib.scad>
