// ============================================================================
// CyberWing — traffic-antenna SCABBARD (fold-down whip guard), print 3
// The whip hinges 90° at its SMA elbow. Folded, it lies in this fin-shaped
// channel: walls flank it, an end cap shields the tip, two spring-finger
// detents click it in/out, and horns protect the hinge. The top slot is open
// the full length so the whip unfolds freely to vertical — nothing to remove.
//   X = fold direction (hinge pivot at x=0, whip lies along +X)
//   Z = up. Bolts to the lid via 6× M3 feet.
// CONFIRM against the real antenna: WHIP_D, WHIP_L, PIVOT_H.
// ============================================================================
$fn = 40;
show_whip = false;

// ---- antenna (measured) ----
WHIP_D  = 13.10;    // whip diameter
WHIP_L  = 159;      // folded length beyond the pivot (7.75in total - pivot)
PIVOT_H = 38;       // pivot axis height (folded stack 1.75in = 44.5 top)

// ---- scabbard ----
CH_IW = WHIP_D + 4;                 // channel inner width
WALL = 3; LIP = 1.2;                // side walls + inward lips
H = PIVOT_H + WHIP_D/2 + 4;         // wall height (whip sits 4 below the rim)
X0 = 12; X1 = WHIP_L + 8;           // channel span (hinge side open)
HORN_H = H + 6;                     // hinge-guard horns
NUB_X = [0.38*WHIP_L, 0.85*WHIP_L]; // detent positions
M3 = 3.4;

module wall_profile(sy) {           // one side wall with lip, along X
  translate([X0, sy*CH_IW/2 + (sy>0?0:-WALL), 0]) cube([X1-X0, WALL, H]);
  translate([X0, sy>0 ? CH_IW/2-LIP : -CH_IW/2, H-2])
    cube([X1-X0, LIP, 2]);                                    // inward lip
}

module horn(sy) {                   // hinge-side guard, sloping into the wall
  translate([0, sy*CH_IW/2 + (sy>0?0:-WALL), 0])
    rotate([90,0,0]) mirror([0,0,sy>0?1:0]) linear_extrude(WALL)
      polygon([[-6,0],[X0+14,0],[X0+14,H],[2,HORN_H],[-6,HORN_H-8]]);
}

module detent(sy, nx) {             // flexure tab + click nub on one wall
  translate([nx, sy*(CH_IW/2+0.2), PIVOT_H+2.5])
    sphere(d=4.5);
}

difference() {
  union() {
    for (sy=[-1,1]) { wall_profile(sy); horn(sy); }
    translate([X0, -CH_IW/2-WALL, 0]) cube([X1-X0, CH_IW+2*WALL, 2.5]);  // floor
    translate([X1, -CH_IW/2-WALL, 0]) cube([4, CH_IW+2*WALL, H+3]);     // tip end cap
    for (fx=[X0+8, (X0+X1)/2, X1-6], sy=[-1,1])                          // M3 feet
      translate([fx-6, sy>0 ? CH_IW/2+WALL : -CH_IW/2-WALL-8, 0]) cube([12, 8, 3]);
  }
  // flexure slits around each detent (tab flexes outward on click)
  for (sy=[-1,1], nx=NUB_X) {
    translate([nx-9, sy*CH_IW/2 + (sy>0?-0.1:-WALL-0.1), PIVOT_H-18]) cube([2, WALL+LIP+0.2, H]);
    translate([nx+7, sy*CH_IW/2 + (sy>0?-0.1:-WALL-0.1), PIVOT_H-18]) cube([2, WALL+LIP+0.2, H]);
  }
  // side windows (weight + wire visibility), diagonal ovals
  for (sy=[-1,1], wx=[X0+16, (X0+X1)/2+12])
    translate([wx, sy*CH_IW/2 + (sy>0?-0.1:-WALL-0.1), 0]) hull() {
      translate([3,0,14]) rotate([-90,0,0]) cylinder(d=12, h=WALL+0.2);
      translate([26,0,PIVOT_H-8]) rotate([-90,0,0]) cylinder(d=12, h=WALL+0.2);
    }
  // floor drains
  for (dx=[X0+20, (X0+X1)/2, X1-20])
    translate([dx-2, -CH_IW/2+1, -0.1]) cube([4, CH_IW-2, 2.7]);
  // M3 feet holes
  for (fx=[X0+8, (X0+X1)/2, X1-6], sy=[-1,1])
    translate([fx, sy*(CH_IW/2+WALL+4), -0.1]) cylinder(d=M3, h=3.2);
}

// click nubs (added after cuts so the flexure slits don't eat them)
for (sy=[-1,1], nx=NUB_X) detent(sy, nx);

// ---- folded whip overlay ----
if (show_whip) color([0.3,0.5,0.75,0.5]) {
  translate([0, 0, PIVOT_H]) rotate([0,90,0]) cylinder(d=WHIP_D, h=WHIP_L);
  translate([0, 0, PIVOT_H]) sphere(d=12);                    // hinge knuckle
}
