// ============================================================================
// CyberWing — Nano->Orin spacer column, 8-32 version  (print 4, PLA)
// 27.4 mm tall, through-hole sized for a #8-32 screw, head counterbored at top.
// ============================================================================
$fn = 72;

H      = 27.4;   // column height
OD     = 12;     // outer diameter
HOLE   = 4.5;    // #8-32 clearance through-hole (major Ø 4.17)
CB_D   = 7.2;    // counterbore for the #8-32 head (socket cap ~6.4)
CB_H   = 4.0;    // counterbore depth
CHAM   = 1.0;    // top/bottom edge chamfer

module column() {
  difference() {
    hull() {
      translate([0,0,CHAM])      cylinder(d=OD, h=H-2*CHAM);
      cylinder(d1=OD-2*CHAM, d2=OD, h=CHAM);
      translate([0,0,H-CHAM])    cylinder(d1=OD, d2=OD-2*CHAM, h=CHAM);
    }
    translate([0,0,-0.1]) cylinder(d=HOLE, h=H+0.2);          // #8-32 through-hole
    translate([0,0,H-CB_H]) cylinder(d=CB_D, h=CB_H+0.1);     // top counterbore (head)
  }
}

column();
