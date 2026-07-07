/* ======================================================================
   CW-MES instance — JETSON NANO dev-kit box
   Parameters only; all geometry comes from cw_mes_lib.scad.
   ----------------------------------------------------------------------
   Board facts (measured earlier in this project, NOT placeholders):
     board 100 x 80 mm, mount pattern 86.14 (long) x 58.25 (short), M3.
   Layout: board centered in X (spans 15..115), I/O edge toward the FRONT
   wall with an 8 mm gap (board Y 8..88, 12 mm rear cable room).
   Board seat: boss_h = 8 (NOT 6) so the front I/O bay floor (z=9) clears
   the bottom-edge T-slot pockets, which reach z = bolt_l - t - 1 = 8.
   Stack top = 8 + 34 (board+heatsink, measured) = 42 < inner.z = 45.
   ====================================================================== */

view = "assembled";   // assembled | plate | bottom top front back left right | fittest

/* ---------- 1 · Core dimensions ---------- */
// front_gap = clear depth in front of the board's I/O edge; encloses the USB
// connectors + a cable chamber. 57 -> footprint Y = 160 mm. The front wall is now
// CLOSED (no I/O bay); cables turn and exit a round port in the RIGHT wall.
front_gap = 57;                          // footprint Y (BY) = inner.y + 11 = 160
inner = [130, 80 + front_gap + 12, 45];  // X: 100 board + 15/side; Y: front + 80 + 12 rear

// circular cable exit in the RIGHT wall (YZ face, x = inner.x)
cable_d = 20;                            // 18.4 for a CW-Link gland; larger for a bundle
cable_y = 35;                            // along the wall (in the front chamber)
cable_z = 20;                            // height (clears the z0..8 / z37..45 joint zones)
t     = 3.0;
rim   = 2.5;
clr   = 0.10;            // PLA / Bambu PLA profile — COUPON-VERIFIED 2026-06-12
fit_tests = [0.10, 0.15, 0.20];   // PLA coupon range (PETG was 0.12/0.18/0.24)

/* ---------- 2 · Fastener system (M3, DIN 562 square nuts) ---------- */
bolt_d  = 3.4;
bolt_l  = 12;
nut_w   = 5.8;
nut_t   = 2.1;
cbore_d = 6.4;
cbore_h = 0;

/* ---------- 3 · Joint pattern ---------- */
nx = 3;
ny = 3;
nz = 2;

/* ---------- 4 · Component mounting (bosses on bottom plate) ---------- */
// Jetson Nano: pattern 86.14 x 58.25, centered in X (65); board front edge sits
// at y = front_gap, so the Y holes track the front_gap (front inset 10.88).
mh_f = front_gap + 10.88;             // front row
mh_r = mh_f + 58.25;                  // rear row
mount_holes = [[21.93, mh_f], [108.07, mh_f],
               [21.93, mh_r], [108.07, mh_r]];
boss_d   = 8;
boss_h   = 8;      // raised from 6: clears bottom T-slots for the I/O bay
insert_d = 4.0;    // M3 heat-set insert (Nano holes are M3, not M2.5)
insert_h = 5;

/* ---------- 5 · Vents & port cutouts (interior coordinates) ---------- */
vent_top   = [25, front_gap + 4, 80, 72];   // vents track the board (now shifted back)
vent_pitch = 7;
vent_slot  = 3;
// Front wall CLOSED — connectors fully enclosed; no open I/O bay.
cut_front = [];
cut_back  = [];
cut_left  = [];
cut_right = [];
// round cable exit on the RIGHT wall (YZ face): [y_along_wall, z, Ø]
cut_right_round = [[cable_y, cable_z, cable_d]];

include <cw_mes_lib.scad>

/* ---- preview only (NOT exported): board + USB plugs show the enclosure ---- */
// USB-A plugs span y = front_gap-20 .. front_gap (18..38) — fully inside the
// case (front face at y=0), recessed behind the I/O bay so cables exit but the
// connectors are enclosed.
if (view == "assembled") {
  color([0.13, 0.45, 0.28]) translate([15, front_gap, t + boss_h]) cube([100, 80, 1.6]);
  for (ux = [33, 50, 67, 84])
    color([0.82, 0.82, 0.86]) translate([ux, front_gap - 20, t + boss_h + 2]) cube([13, 20, 6]);
}
