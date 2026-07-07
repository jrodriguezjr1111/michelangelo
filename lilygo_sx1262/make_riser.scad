// ============================================================================
// CyberWing — LilyGo housing RISER (intermediate plate)
// The top plate (101 × 65 × 4, make_top.py) floats >15 mm above the base
// (101 × 40 × 27, make_base.py) — its M3 screws can't reach the base's Ø6
// bosses (70 × 32). This riser fills the gap:
//   - 101 × 65 × 4 plate, same footprint/cutout as make_top (saddle-compatible:
//     58 × 49 pass-throughs kept, battery cutout kept)
//   - perimeter wall down GAP mm, sitting wall-on-wall on the base rim
//   - 4 columns at 70 × 32 that LAND on the base bosses, with M3 self-tap
//     pilots on top — the top plate's original screws bite into these
//   - 4 skirt fingers over the base's ±Y walls, M3 self-taps hold the riser
//     to the base (no axis shared with the column screws)
// Print upside-down (plate on the bed, walls/columns up) — no supports.
// CONFIRM: GAP = measured float between top-plate underside and base rim.
// ============================================================================
$fn = 44;

GAP = 16;                       // riser height (MEASURE the real float)

// ---- cloned make_top footprint ----
TOP_L = 101; TOP_W = 65; T = 4;
CUT_L = 86; CUT_W = 23; CUT_EXT_PX = 4.7;      // battery cutout, +X extended
SADDLE_PX = 58; SADDLE_PY = 49; M3_CLR = 3.4;  // saddle pass-through pattern
X_SHIFT = 10.5;                                 // plate is +10.5 vs base/saddle center

// ---- base interface (make_base.py) ----
BASE_L = 101; BASE_W = 40; WALL = 2.5;
BOSS_PX = 70; BOSS_PY = 32;                     // base boss pattern
COL_D = 9; PILOT = 2.7; PILOT_DEP = 12;
FING_W = 14; FING_DEP = 10; FING_T = 3; FING_CLR = 0.3;
FING_X = [-30, 30];                             // finger centers along the base

// modeled in ASSEMBLY orientation: z=0 at the base rim, plate on top of GAP
difference() {
  union() {
    translate([X_SHIFT - TOP_L/2, -TOP_W/2, GAP]) cube([TOP_L, TOP_W, T]);   // plate
    difference() {                                                            // riser ring on the base rim
      translate([-BASE_L/2, -BASE_W/2, 0]) cube([BASE_L, BASE_W, GAP]);
      translate([-BASE_L/2+WALL, -BASE_W/2+WALL, -0.1]) cube([BASE_L-2*WALL, BASE_W-2*WALL, GAP+0.2]);
    }
    for (sx=[-1,1], sy=[-1,1])                                                // columns onto the bosses
      translate([sx*BOSS_PX/2, sy*BOSS_PY/2, 0]) cylinder(d=COL_D, h=GAP+T);
    for (fx=FING_X, sy=[-1,1])                                                // skirt fingers over base walls
      translate([fx-FING_W/2, sy>0 ? BASE_W/2+FING_CLR : -BASE_W/2-FING_CLR-FING_T, -FING_DEP])
        cube([FING_W, FING_T, FING_DEP+GAP]);
  }
  // battery cutout through the plate (asymmetric +X, as make_top)
  translate([X_SHIFT + CUT_EXT_PX/2 - (CUT_L+CUT_EXT_PX)/2, -CUT_W/2, GAP-0.1])
    cube([CUT_L+CUT_EXT_PX, CUT_W, T+0.2]);
  // saddle pass-throughs (58 × 49, centered on the base/saddle origin)
  for (sx=[-1,1], sy=[-1,1])
    translate([sx*SADDLE_PX/2, sy*SADDLE_PY/2, GAP-0.1]) cylinder(d=M3_CLR, h=T+0.2);
  // M3 pilots in the column tops (top plate's screws bite here)
  for (sx=[-1,1], sy=[-1,1])
    translate([sx*BOSS_PX/2, sy*BOSS_PY/2, GAP+T-PILOT_DEP]) cylinder(d=PILOT, h=PILOT_DEP+0.1);
  // finger screw holes (M3 self-tap into the base wall)
  for (fx=FING_X, sy=[-1,1])
    translate([fx, sy*(BASE_W/2+FING_CLR+FING_T/2) + (sy>0?0.01:-0.01), -FING_DEP/2])
      rotate([sy>0?-90:90,0,0]) cylinder(d=3.4, h=FING_T+0.2, center=true);
}
