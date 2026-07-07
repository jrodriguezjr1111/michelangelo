/* ======================================================================
   CW-MES instance — JETSON NANO, STRONG bottom plate (STEP 1)
   Same box params as cw_mes_jetson_nano.scad, plus additive strengthening:
   underside rib lattice, RSD outboard side-mount flange, upright component
   posts. (STEP 2 will merge the GNSS dual-tube clamp.) Original files are
   untouched — this only adds parameters + includes the additive engine.
   ====================================================================== */

view = "strong";   // -> strong_bottom() from cw_mes_strong.scad

/* ---------- Nano box params (copied from cw_mes_jetson_nano.scad) ---------- */
front_gap = 57;
inner = [130, 80 + front_gap + 12, 45];
cable_d = 20; cable_y = 35; cable_z = 20;
t = 3.0; rim = 2.5; clr = 0.10; fit_tests = [0.10, 0.15, 0.20];

bolt_d = 3.4; bolt_l = 12; nut_w = 5.8; nut_t = 2.1; cbore_d = 6.4; cbore_h = 0;
nx = 3; ny = 3; nz = 2;

mh_f = front_gap + 10.88;
mh_r = mh_f + 58.25;
mount_holes = [[21.93, mh_f], [108.07, mh_f], [21.93, mh_r], [108.07, mh_r]];
boss_d = 8; boss_h = 8; insert_d = 4.0; insert_h = 5;

vent_top = [25, front_gap + 4, 80, 72]; vent_pitch = 7; vent_slot = 3;
cut_front = []; cut_back = []; cut_left = []; cut_right = [];
cut_right_round = [[cable_y, cable_z, cable_d]];

/* ---------- STRONG features (STEP 1) ---------- */
rib_h = 8; rib_w = 2.4; rib_pitch = 24;            // underside lattice

rsd_ledge = true;                                  // RSD outboard side-mount flange
rsd_PX = 51.83; rsd_PY = 120.18;                   // RSD pattern (PY long -> horizontal)
rsd_insert_d = 4.0; rsd_insert_h = 6; rsd_ledge_gap = 8;

post_h = 32; post_d = 9; post_insert_d = 4.0; post_insert_h = 6;
// upright posts along the -Y (front) short edge — PLACEHOLDER positions
// (BX=141, BY=160, o=5.5 for this box; awaiting the real plate's bolt pattern)
post_list = [[23.5, 8.5], [117.5, 8.5]];

include <cw_mes_lib.scad>      // computes BX, BY, o ...
include <cw_mes_strong.scad>   // additive modules + view dispatch
