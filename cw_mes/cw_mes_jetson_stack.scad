/* ======================================================================
   CW-MES instance — JETSON NANO + ORIN STACK box
   Houses the jetson_stack frame (lower Nano deck + corner legs + upper
   Orin deck). Same modular 6-panel system; geometry from cw_mes_lib.scad.
   ----------------------------------------------------------------------
   Sized from jetson_stack.scad: deck 131 x 118.5, stack ~80 mm tall.
   inner = deck + ~8 clearance, height = stack + ~5.
   ⚠ If the Orin dims change in jetson_stack.scad, re-check inner here.
   ====================================================================== */

view = "assembled";   // assembled | plate | bottom top front back left right | fittest

/* ---------- 1 · Core dimensions ---------- */
inner = [139, 126, 85];   // fits the 131 x 118.5 deck + clearance; 85 = 2-board stack
t     = 3.0;
rim   = 2.5;
clr   = 0.10;             // PLA / Bambu PLA — coupon-verified
fit_tests = [0.10, 0.15, 0.20];

/* ---------- 2 · Fastener system (M3, DIN 562 square nuts) ---------- */
bolt_d  = 3.4;
bolt_l  = 12;
nut_w   = 5.8;
nut_t   = 2.1;
cbore_d = 6.4;
cbore_h = 0;

/* ---------- 3 · Joint pattern (taller box -> nz=3) ---------- */
nx = 3;
ny = 3;
nz = 3;

/* ---------- 4 · No bottom bosses — the stack frame sits on the floor ---------- */
mount_holes = [];
boss_d   = 8;
boss_h   = 14;
insert_d = 4.0;
insert_h = 5;

// GNSS-saddle mount: M4 36.14 x 36.1, centered on the bottom plate
saddle_d = 4.4;
scx = inner[0]/2;  scy = inner[1]/2;
saddle_holes = [[scx - 36.14/2, scy - 36.1/2], [scx + 36.14/2, scy - 36.1/2],
                [scx - 36.14/2, scy + 36.1/2], [scx + 36.14/2, scy + 36.1/2]];

/* ---------- 5 · Vents & cable glands ---------- */
vent_top   = [28, 28, 83, 70];   // big top grille over the Orin
vent_pitch = 8;
vent_slot  = 3;
cut_front  = [];
cut_back   = [];
cut_left   = [];
cut_right  = [];
// Ø12 clamshell-gland bores on the FRONT wall, Nano-I/O height (add more as needed)
cut_front_round = [[35, 20, 12], [70, 20, 12], [105, 20, 12]];

include <cw_mes_lib.scad>
