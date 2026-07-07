// ============================================================================
// CyberWing — WAGO connector plate (side-mounted, vertical)
// Holds 4 WAGO splicing connectors in a vertical column. Mounts to a side
// frame's 4× M3 inserts (64 × 40 pattern) on 16 mm standoffs. Connectors
// retained by zip-ties through paired slots (universal). Print standoffs-up.
//   plate 71.94 (vertical / Y) × 47.87 (wide / X); connectors face the -Z front.
// ============================================================================
$fn = 40;

PW = 47.87; PH = 71.94; T = 4;                 // plate width(X), height(Y), thick(Z)
MNT_X = 40; MNT_Y = 64;                         // side-frame insert pattern (40 × 64)
SO_D = 7; SO_H = 16; SO_BORE = 3.4;             // 16 mm standoffs + M3 clearance
M3_CB_D = 6; M3_CB_H = 3;
CONN_Y = [-27, -9, 9, 27];                      // 4 connector centers up the column
ZT_X = 14; ZT_W = 3; ZT_L = 9;                  // zip-tie slot pair per connector

difference() {
  union() {
    translate([-PW/2, -PH/2, 0]) cube([PW, PH, T]);                       // plate
    for (sx=[-1,1], sy=[-1,1])                                            // 4 standoffs (back, +Z)
      translate([sx*MNT_X/2, sy*MNT_Y/2, T]) cylinder(d=SO_D, h=SO_H);
  }
  // M3 clearance through each standoff + plate, head counterbore on the front (z=0)
  for (sx=[-1,1], sy=[-1,1]) {
    translate([sx*MNT_X/2, sy*MNT_Y/2, -0.1]) cylinder(d=SO_BORE, h=T+SO_H+0.2);
    translate([sx*MNT_X/2, sy*MNT_Y/2, -0.1]) cylinder(d=M3_CB_D, h=M3_CB_H);
  }
  // zip-tie slot pairs (2 per connector, straddling it)
  for (cy=CONN_Y, sx=[-1,1])
    translate([sx*ZT_X - ZT_W/2, cy - ZT_L/2, -0.1]) cube([ZT_W, ZT_L, T+0.2]);
}
