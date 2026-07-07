// ============================================================================
// CyberWing — LilyGo SX1262 Pelican side-mount box (board only, no battery)
// Full box + snap lid for the LilyGo (100 × 33 board, M2 mounts 95.33 × 28.55).
// Mounts LONG AXIS VERTICAL on the outside of a Pelican case wall via 4× M4
// through-bolts in flanges on the LONG sides (2 per side; nut + washer inside
// the case). Mounted width capped at 56 mm (40.5 box + 7.75/side flange).
// USB-C opening on the BOTTOM end wall (cable hangs down), wide rectangular
// antenna slot on the TOP end wall (alignment TBD).
// Lid = snap cap secured by 2× M3 self-tap screws through the skirt mid-sides.
//   Modeled back-plate down (X = board length = vertical in use).
// part = "base" | "lid" | "both" | "lidprint"
// ============================================================================
$fn = 44;
part = "both";

// ---- board (proven: lilygo_sx1262 generators) ----
BRD_L = 100; BRD_W = 33;
M2_PX = 95.33; M2_PY = 28.55;
BOSS_D = 5; BOSS_H = 5; M2_PILOT = 1.8;   // M2 self-tap into bosses
COMP_H = 11;                              // headroom above the board

// ---- box ----
WALL = 3; FLOOR = 4; CLR = 1.0;
ix = BRD_L + 2*CLR; iy = BRD_W + 1.5;     // 102 × 34.5 cavity
iz = BOSS_H + 1.6 + COMP_H + 0.9;         // 18.5 deep
ox = ix + 2*WALL; oy = iy + 2*WALL; oz = FLOOR + iz;
xc = ox/2; yc = oy/2;

// ---- ports ----
USB_W = 12; USB_H = 7;                    // bottom end wall (x=0)
PORT_Z = FLOOR + BOSS_H + 1.6 + 1.7;      // USB-C centerline ~12.3
ANT_W = 26; ANT_H = 8;                    // antenna slot, top end wall (x=ox) — wide, alignment TBD

// ---- Pelican mount flanges on the LONG sides (through-bolt M4) ----
// Total mounted width capped at 56 mm: oy (40.5) + 2 × FL_W (7.75) = 56.0
FL_W = 7.75; FL_T = 4; FL_L = 90; M4 = 4.4; FL_HX = 35;   // holes at xc±35

// ---- lid ----
SK_T = 1.8; SK_CLR = 0.3; SK_H = 8; LID_T = 2.5;
M3_CLR = 3.4; PILOT = 2.7;                // skirt screw -> wall pilot
lockz = oz - 4;                           // lid-screw height

module base() {
  difference() {
    union() {
      cube([ox, oy, oz]);
      for (sy = [-1, 1])                                       // M4 flanges, long sides
        translate([xc-FL_L/2, sy>0 ? oy : -FL_W, 0]) cube([FL_L, FL_W, FL_T]);
    }
    translate([WALL, WALL, FLOOR]) cube([ix, iy, iz+0.1]);     // cavity
    translate([-0.1, yc-USB_W/2, PORT_Z-USB_H/2])              // USB-C, bottom end
      cube([WALL+0.2, USB_W, USB_H]);
    translate([ox-WALL-0.1, yc-ANT_W/2, PORT_Z-ANT_H/2])       // antenna slot, top end
      cube([WALL+0.2, ANT_W, ANT_H]);
    for (sx = [-1, 1], sy = [-1, 1])                           // M4 through flanges
      translate([xc+sx*FL_HX, sy>0 ? oy+FL_W/2 : -FL_W/2, -0.1]) cylinder(d=M4, h=FL_T+0.2);
    for (sy = [0, 1])                                          // lid-screw pilots, mid long walls
      translate([xc, sy==0 ? -0.1 : oy-3.1, lockz]) rotate([-90,0,0]) cylinder(d=PILOT, h=3.2);
  }
  for (sx = [-1, 1], sy = [-1, 1])                             // M2 board bosses
    difference() {
      translate([xc+sx*M2_PX/2, yc+sy*M2_PY/2, FLOOR]) cylinder(d=BOSS_D, h=BOSS_H);
      translate([xc+sx*M2_PX/2, yc+sy*M2_PY/2, FLOOR+BOSS_H-5]) cylinder(d=M2_PILOT, h=5.1);
    }
}

module lid() {
  LX = ox + 2*(SK_CLR+SK_T); LY = oy + 2*(SK_CLR+SK_T);
  difference() {
    union() {
      translate([-(SK_CLR+SK_T), -(SK_CLR+SK_T), oz]) cube([LX, LY, LID_T]);
      difference() {
        translate([-(SK_CLR+SK_T), -(SK_CLR+SK_T), oz-SK_H]) cube([LX, LY, SK_H]);
        translate([-SK_CLR, -SK_CLR, oz-SK_H-0.1]) cube([ox+2*SK_CLR, oy+2*SK_CLR, SK_H+0.2]);
      }
    }
    for (sy = [-1, 1])                                         // M3 through skirt mid-sides
      translate([xc, yc+sy*(oy/2+SK_CLR+SK_T+0.1), lockz]) rotate([sy>0?-90:90,0,0]) cylinder(d=M3_CLR, h=SK_T+SK_CLR+0.3);
  }
}

if (part=="base" || part=="both") color("SteelBlue") base();
if (part=="lid"  || part=="both") color("LightGreen") lid();
if (part=="lidprint") translate([0,0,oz+LID_T]) rotate([180,0,0]) lid();
