// ============================================================================
// CyberWing — Pelican 1400 ground station, antenna placement mockup (NOT a print)
// Case exterior 340 × 295 × 152 (13.37 × 11.62 × 6.00 in), lid ~45 top.
//   X = length (340, short ends ±170) ; Y = width (front latches -Y, hinge +Y)
//   Z = up. Case sits flat, lid on top.
// Antennas per the placement plan:
//   BLUE   3× traffic 978/1090 verticals, lid top, diagonal, Ø110 ground discs
//   ORANGE 2× cellular LTE paddles, short ends (right one tilted 45°)
//   GREEN  2× wifi paddles, back (hinge) wall, 180 mm apart
// show_lilygo=true adds the LilyGo box silhouette (final spot TBD).
// ============================================================================
$fn = 48;
show_lilygo = false;

CL = 340; CW = 295; BASE_H = 107; LID_H = 45; R = 12;

module rbox(l, w, h, r)                        // rounded-corner box
  hull() for (sx=[-1,1], sy=[-1,1])
    translate([sx*(l/2-r), sy*(w/2-r), 0]) cylinder(r=r, h=h);

// ---------------- case ----------------
color([0.25,0.27,0.29]) {
  rbox(CL, CW, BASE_H, R);                                     // base
  translate([0,0,BASE_H+1]) rbox(CL, CW, LID_H, R);            // lid
  for (sx=[-1,1]) translate([sx*80-20, -CW/2-4, 88]) cube([40, 8, 40]);   // latches
  translate([-60, -CW/2-6, 30]) cube([120, 8, 26]);            // handle
  for (sx=[-1,1]) translate([sx*100-18, CW/2-2, 96]) cube([36, 10, 30]);  // hinges
}

// ---------------- traffic (lid top, diagonal) ----------------
LID_TOP = BASE_H + 1 + LID_H;
for (p = [[-105, 75], [0, 0], [105, -75]])
  translate([p[0], p[1], LID_TOP]) color("SteelBlue") {
    cylinder(d=110, h=3);                                      // ground-plane disc
    cylinder(d=14, h=10);                                      // SMA base
    cylinder(d=8, h=110);                                      // whip
    translate([0,0,110]) sphere(d=9);
  }

// ---------------- cellular (short ends; right tilted 45°) ----------------
module paddle(h=100) {                                         // origin at hinge puck
  cylinder(d=16, h=8);
  translate([-6, -3, 0]) cube([12, 6, h]);
  translate([-6, -3, h]) cube([12, 6, 6]);
}
color("Orange") {
  translate([-CL/2-3, 0, 92]) rotate([0,0,90]) paddle();                    // c1 vertical
  translate([ CL/2+3, 0, 92]) rotate([45,0,0]) rotate([0,0,90]) paddle();   // c2 45° tilt
}

// ---------------- wifi (back wall, 180 apart) ----------------
color("MediumSeaGreen")
for (sx=[-1,1])
  translate([sx*90, CW/2+3, 80]) paddle(90);

// ---------------- LilyGo box silhouette (spot TBD) ----------------
if (show_lilygo)
  color([0.6,0.6,0.65,0.6]) translate([-54, -CW/2-24, 20]) cube([108, 24, 56]);
