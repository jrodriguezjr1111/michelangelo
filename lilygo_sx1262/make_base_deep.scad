// ============================================================================
// CyberWing — LilyGo DEEP BASE, redesigned around the existing top plate
// Replaces make_base.py (101 × 40 × 27 — too short, screws couldn't reach).
// Same footprint as the top plate (101 × 65) so the two mate flush all around,
// and the whole box sits on the IMU platform-saddle with matching Y edges.
//   - Interior deep enough for the 18650 + holder + wiring (INT_H, MEASURE)
//   - 4× Ø7 bosses at 70 × 32 rising to the RIM, M3 pilots — the top plate's
//     original screws engage immediately (the old failure, fixed structurally)
//   - Base bolts to the saddle itself: 4× M3 at 58 × 49 through the floor,
//     socket heads inside on counterbores (the top's 58×49 csk holes just
//     pass over the cavity — unused, no conflict)
//   - USB openings (12 × 7) on both ±X end walls, old 13.5 height kept
// Print floor-down, no supports. CONFIRM INT_H against the real cell stack.
// ============================================================================
$fn = 44;

// ---- footprint (cloned from the top plate) ----
L = 101; W = 65; WALL = 3; FLOOR = 4;
INT_H = 24;                      // interior depth (measured 20 below the plate + 4 slack)
H = FLOOR + INT_H;               // outer height (28)

// ---- interfaces ----
BOSS_PX = 70; BOSS_PY = 32;      // top plate screws -> rim bosses
BOSS_D = 7; PILOT = 2.7; PILOT_DEP = 12;
SAD_PX = 58; SAD_PY = 49;        // base -> saddle, through the floor
M3 = 3.4; CB_D = 6.5; CB_H = 3;
USB_W = 12; USB_H = 7; USB_Z = 13.5;   // end-wall openings (old height kept)

module rrect(l, w, r) hull() for (sx=[-1,1], sy=[-1,1])
  translate([sx*(l/2-r), sy*(w/2-r)]) circle(r=r);

difference() {
  linear_extrude(H) rrect(L, W, 4);                                     // shell
  // cavity
  translate([0,0,FLOOR]) linear_extrude(INT_H+0.1) rrect(L-2*WALL, W-2*WALL, 3);
  // saddle mount: M3 through the floor, head counterbore inside
  for (sx=[-1,1], sy=[-1,1]) {
    translate([sx*SAD_PX/2, sy*SAD_PY/2, -0.1]) cylinder(d=M3, h=FLOOR+0.2);
    translate([sx*SAD_PX/2, sy*SAD_PY/2, FLOOR-CB_H]) cylinder(d=CB_D, h=CB_H+0.2);
  }
  // USB openings, both ends
  for (sx=[-1,1])
    translate([sx*(L/2) - (WALL+0.2)/2 + (sx>0?0.1:-0.1), -USB_W/2, USB_Z-USB_H/2])
      cube([WALL+0.4, USB_W, USB_H]);
}

// rim bosses (added after the cavity cut so they stand inside it)
for (sx=[-1,1], sy=[-1,1])
  difference() {
    translate([sx*BOSS_PX/2, sy*BOSS_PY/2, 0]) cylinder(d=BOSS_D, h=H);
    translate([sx*BOSS_PX/2, sy*BOSS_PY/2, H-PILOT_DEP]) cylinder(d=PILOT, h=PILOT_DEP+0.1);
  }
