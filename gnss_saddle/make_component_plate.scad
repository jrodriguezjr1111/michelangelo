// ============================================================================
// CyberWing — side-frame component plate, board CENTERED on standoffs
// Mounts to a side frame's 4× M3 inserts (64 × 40). A board sits centered on 4
// standoffs. Drive it for either board with -D:
//   FeatherWing : PAT_X=45.72 PAT_Y=17.78 SO_OD=6 SO_BORE=2.8   (1.8"×0.7", M2.5)
//   IMU         : PAT_X=19.94 PAT_Y=17.78 SO_OD=5 SO_BORE=2.2
// Recovered from the original feather_imu_plate.stl. Print flat, standoffs up.
// ============================================================================
$fn = 48;

// ---- plate + frame mount (64 × 40 to the side frame) ----
PLATE_X = 72; PLATE_Y = 48; T = 4;
MNT_PU = 64; MNT_PV = 40;
M3_CLR = 3.4; M3_CB_D = 6; M3_CB_H = 2.5;

// ---- board standoffs (override per board) ----
PAT_X  = 45.72;     // hole pattern, X
PAT_Y  = 17.78;     // hole pattern, Y
SO_OD  = 6;         // standoff outer dia
SO_BORE = 2.8;      // standoff bore
SO_H   = 10;        // standoff height above the plate

difference() {
  union() {
    translate([-PLATE_X/2, -PLATE_Y/2, 0]) cube([PLATE_X, PLATE_Y, T]);       // plate
    for (sx=[-1,1], sy=[-1,1])                                                 // 4 centered standoffs
      translate([sx*PAT_X/2, sy*PAT_Y/2, T]) cylinder(d=SO_OD, h=SO_H);
  }
  // board screw bores through the standoffs + plate
  for (sx=[-1,1], sy=[-1,1])
    translate([sx*PAT_X/2, sy*PAT_Y/2, -0.1]) cylinder(d=SO_BORE, h=T+SO_H+0.2);
  // frame-mount M3 clearance + head counterbore on top
  for (sx=[-1,1], sy=[-1,1]) {
    translate([sx*MNT_PU/2, sy*MNT_PV/2, -0.1]) cylinder(d=M3_CLR, h=T+0.2);
    translate([sx*MNT_PU/2, sy*MNT_PV/2, T-M3_CB_H]) cylinder(d=M3_CB_D, h=M3_CB_H+0.1);
  }
}
