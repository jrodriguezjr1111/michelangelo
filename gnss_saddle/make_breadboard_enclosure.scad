// ============================================================================
// CyberWing — breadboard enclosure with USB-C bay
// Board: 89 × 53, M3 holes 78.67 × 35.52, components ≤15 mm. Board sits on 4
// standoffs (Ø7 × 10, M3 through, head counterbore underneath). The cavity
// extends 40 mm past the +X short end for a USB-C plug overmold (40 × 14 × 14);
// the cable drops into a U-notch in that end wall (overmold stays inside).
// Snap-cap lid. part = "base" | "lid" | "both". Print base floor-down, lid
// plate-down (export part="lidprint").
// ============================================================================
$fn = 40;
part = "both";

// ---- board (measured) ----
BB_L = 89; BB_W = 53; COMP_H = 15;
HOLE_PX = 78.67; HOLE_PY = 35.52;
SO_OD = 7; SO_H = 10; M3 = 3.4; CB_D = 6; CB_H = 3;

// ---- box ----
CLR = 0.5;                       // per side around the board
BAY = 40;                        // USB-C bay past the +X board end
WALL = 2.5; BASE = 4;
IZ = SO_H + 1.6 + COMP_H + 2;    // floor -> lid underside (28.6)
NOTCH_W = 8;                     // cable U-notch in the +X wall

ix = BB_L + 2*CLR + BAY;         // 130
iy = BB_W + 2*CLR;               // 54
ox = ix + 2*WALL; oy = iy + 2*WALL;
oz = BASE + IZ;
xc = WALL + CLR + BB_L/2;        // board center
yc = oy/2;
notch_z = BASE + SO_H + 1.6;     // board top ~ cable sits just above

// ---- snap-cap lid ----
SK_T = 1.8; SK_CLR = 0.3; SK_H = 8;

module base() {
  difference() {
    union() {
      cube([ox, oy, oz]);
      }
    translate([WALL, WALL, BASE]) cube([ix, iy, IZ+0.1]);                 // cavity
    translate([ox-WALL-0.1, yc-NOTCH_W/2, notch_z-2])                     // cable U-notch, +X wall
      cube([WALL+0.2, NOTCH_W, oz]);
    for (sx=[-1,1], sy=[-1,1]) {                                          // standoff bores + bottom cb
      translate([xc+sx*HOLE_PX/2, yc+sy*HOLE_PY/2, -0.1]) cylinder(d=M3, h=BASE+SO_H+0.2);
      translate([xc+sx*HOLE_PX/2, yc+sy*HOLE_PY/2, -0.1]) cylinder(d=CB_D, h=CB_H);
    }
  }
  for (sx=[-1,1], sy=[-1,1])                                              // 4 standoffs
    difference() {
      translate([xc+sx*HOLE_PX/2, yc+sy*HOLE_PY/2, BASE]) cylinder(d=SO_OD, h=SO_H);
      translate([xc+sx*HOLE_PX/2, yc+sy*HOLE_PY/2, BASE-0.1]) cylinder(d=M3, h=SO_H+0.2);
    }
}

module lid() {
  LX = ox + 2*(SK_CLR+SK_T); LY = oy + 2*(SK_CLR+SK_T);
  translate([-(SK_CLR+SK_T), -(SK_CLR+SK_T), oz]) cube([LX, LY, 2]);      // top plate
  difference() {                                                           // skirt
    translate([-(SK_CLR+SK_T), -(SK_CLR+SK_T), oz-SK_H]) cube([LX, LY, SK_H]);
    translate([-SK_CLR, -SK_CLR, oz-SK_H-0.1]) cube([ox+2*SK_CLR, oy+2*SK_CLR, SK_H+0.2]);
  }
}

if (part=="base" || part=="both") color("SteelBlue") base();
if (part=="lid"  || part=="both") color("LightGreen") lid();
if (part=="lidprint") translate([0,0,oz+2]) rotate([180,0,0]) lid();
