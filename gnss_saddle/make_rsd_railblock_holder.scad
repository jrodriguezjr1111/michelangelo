// ============================================================================
// CyberWing — RSD holder, L-bracket for a SmallRig 15mm railblock
// Base bolts to the railblock's 4× 1/4"-20 grid (36.44 × 36.10 mm) for 4-point
// support. Vertical flange carries the RSD (4× #8-32 at 120.18 H × 51.83 V) so
// the RSD stands on its LONG side. Gussets brace the flange. Print base-down.
// ============================================================================
$fn = 56;

// RSD pattern on the vertical flange
RSD_PX = 120.18; RSD_PZ = 51.83; RSD_CLR = 4.5;
// railblock 4× 1/4"-20 grid + head counterbore
QTR_X = 36.44; QTR_Y = 36.10; QTR_CLR = 6.86; QTR_CB_D = 13.0; QTR_CB_H = 5.0;
// base / flange / gusset
BW = 130; BT = 7;                     // base width(X), thickness(Z)
B_FRONT = -27; FT = 5; FH = 63;       // base front Y, flange thick(Y), height(Z)
flange_y = 28;                        // flange front face Y (clears the back grid holes)
GT = 5; GH = 34; GD = 20;             // gusset thick(X), height(Z), reach(Y)
gx_list = [0, -40, 40, -62, 62];

mid_z = BT + FH/2;                    // RSD vertical center
B_BACK = flange_y + FT;               // base back Y

module gusset(x) {
  hull() {
    translate([x-GT/2, flange_y-0.01, BT]) cube([GT, 0.01, GH]);
    translate([x-GT/2, flange_y-GD,  BT]) cube([GT, GD,  0.01]);
  }
}

difference() {
  union() {
    translate([-BW/2, B_FRONT, 0]) cube([BW, B_BACK - B_FRONT, BT]);   // base
    translate([-BW/2, flange_y, 0]) cube([BW, FT, BT + FH]);           // flange
    for (gx = gx_list) gusset(gx);                                     // gussets
  }
  // 4× 1/4"-20 grid into the railblock + head counterbore on top
  for (sx = [-1, 1], sy = [-1, 1]) {
    translate([sx*QTR_X/2, sy*QTR_Y/2, -0.1]) cylinder(d=QTR_CLR, h=BT+0.2);
    translate([sx*QTR_X/2, sy*QTR_Y/2, BT-QTR_CB_H]) cylinder(d=QTR_CB_D, h=QTR_CB_H+0.1);
  }
  // RSD #8-32 through the flange (along Y)
  for (sx = [-1, 1], sz = [-1, 1])
    translate([sx*RSD_PX/2, flange_y-0.1, mid_z + sz*RSD_PZ/2]) rotate([-90,0,0]) cylinder(d=RSD_CLR, h=FT+0.3);
}
