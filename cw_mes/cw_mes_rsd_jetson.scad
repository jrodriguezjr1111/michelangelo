/* ======================================================================
   CW-MES instance — JETSON STACK + RSD box
   Houses the jetson_stack frame; RSD DC converter bolts to the OUTSIDE of
   the back wall via 4× #8-32. Front cable bay + grommet exit on a side wall.
   Pelican mount: 3D-printed isolating feet (4 corner holes on the bottom).
   ====================================================================== */

view = "assembled";   // assembled | plate | bottom top front back left right | fittest

/* ---------- 1 · Core ---------- */
inner = [200, 132, 90];   // X: Jetson 131 + ~70 cable bay; Y: 120.18 RSD pattern + margin; Z
t     = 3.0;
rim   = 2.5;
clr   = 0.10;
fit_tests = [0.10, 0.15, 0.20];

/* ---------- 2 · Fasteners (M3 square nuts) ---------- */
bolt_d  = 3.4;  bolt_l = 12;  nut_w = 5.8;  nut_t = 2.1;  cbore_d = 6.4;  cbore_h = 0;

/* ---------- 3 · Joints (big box) ---------- */
nx = 4;  ny = 3;  nz = 3;

/* ---------- 4 · Bottom: no bosses; 4 corner foot-mount holes ---------- */
mount_holes = [];
boss_d = 8;  boss_h = 14;  insert_d = 4.0;  insert_h = 5;
// isolating-foot bolts (M4) at the 4 corners
saddle_d = 4.4;
saddle_holes = [[14, 14], [inner[0]-14, 14], [14, inner[1]-14], [inner[0]-14, inner[1]-14]];

/* ---------- 5 · Vents + RSD mount + grommet ---------- */
vent_top   = [80, 22, 100, 88];   // grille over the Jetson (X +end)
vent_pitch = 8;  vent_slot = 3;
cut_front = [];  cut_back = [];  cut_left = [];  cut_right = [];

// RSD converter: 4× #8-32 (Ø4.4) at 51.83 × 120.18, BACK (+X end / right) wall, centered.
// External mount — clearance through-holes only.
RSD_PX = 51.83;  RSD_PY = 120.18;  RSD_D = 4.4;
rcy = inner[1]/2;  rcz = inner[2]/2;
cut_right_round = [[rcy - RSD_PY/2, rcz - RSD_PX/2, RSD_D], [rcy - RSD_PY/2, rcz + RSD_PX/2, RSD_D],
                   [rcy + RSD_PY/2, rcz - RSD_PX/2, RSD_D], [rcy + RSD_PY/2, rcz + RSD_PX/2, RSD_D]];

// Cable exit: Ø20 open grommet pass-through on the front side wall, cable-bay end.
cut_front_round = [[35, 32, 20]];

include <cw_mes_lib.scad>
