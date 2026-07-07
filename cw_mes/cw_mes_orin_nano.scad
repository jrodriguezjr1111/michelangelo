/* CW-MES instance — ORIN NANO dev-kit box (original v1.0 defaults).
   mount_holes are PLACEHOLDERS — measure before printing. */

view = "assembled";

/* ---------- 1 · Core dimensions ---------- */
inner = [130, 110, 60];  // interior cavity X·Y·Z — sized for Orin Nano DK + cable room
t     = 3.0;             // panel thickness (>= 3 recommended for nut pockets)
rim   = 2.5;             // top/bottom plate overhang (keeps tab slots closed)
clr   = 0.18;            // mating clearance per face — PETG sweet spot 0.15–0.22

/* ---------- 2 · Fastener system (defaults: M3, DIN 562 square nuts) --- */
bolt_d  = 3.4;   // bolt clearance hole          (M4: 4.5)
bolt_l  = 12;    // bolt length, mm              (M4: 12–16)
nut_w   = 5.8;   // square nut width, 5.5 + play (M4: 7.2)
nut_t   = 2.1;   // square nut thickness, 1.8 +  (M4: 2.4)
cbore_d = 6.4;   // socket head clearance dia    (M4: 7.6)
cbore_h = 0;     // > 0 recesses heads (e.g. 1.5); 0 = heads sit proud

/* ---------- 3 · Joint pattern ---------- */
nx = 3;          // tabs per X edge  (front/back <-> top/bottom)
ny = 3;          // tabs per Y edge  (left/right <-> top/bottom)
nz = 2;          // tabs per vertical corner edge (nz=2 -> 1 bolt per corner)

/* ---------- 4 · Component mounting (bosses on bottom plate) ----------- */
// !! PLACEHOLDER pattern — MEASURE your Orin Nano carrier board hole
// !! centers before printing and update mount_holes (interior XY coords).
mount_holes = [[22, 26], [108, 26], [22, 84], [108, 84]];
boss_d      = 8;     // standoff boss diameter
boss_h      = 6;     // standoff height above floor
insert_d    = 3.2;   // pilot for M2.5 heat-set insert (M3 insert: 4.0)
insert_h    = 5;     // insert pilot depth

/* ---------- 5 · Vents & port cutouts (interior coordinates) ----------- */
vent_top   = [30, 25, 70, 60];   // [x, y, w, h] slot-vent region on top; [] = none
vent_pitch = 7;                  // vent row spacing
vent_slot  = 3;                  // vent slot width
// Per-wall rectangular cutouts: [x, z, w, h] from interior corner; r=2 corners
cut_front = [[40, 10, 50, 16]];  // example: Jetson I/O bay — edit/clear as needed
cut_back  = [];
cut_left  = [];
cut_right = [];

include <cw_mes_lib.scad>
