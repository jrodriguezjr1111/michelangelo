// ============================================================================
// CyberWing — Nano->Orin spacer column  (print 4, PLA)
// Fastens to the Nano deck's M3 insert with an M3 x 30 screw dropped through
// from the top (head recessed in the counterbore). 26 mm tall -> with the Nano
// deck's 8 mm insert boss it gives a ~34 mm gap, clearing the 29 mm Nano+heatsink.
// The Orin deck sits on the column tops.
// ============================================================================
$fn = 72;

H      = 26;     // column height
OD     = 11;     // outer diameter (sits on the Nano deck's 10 mm boss)
HOLE   = 3.4;    // M3 screw clearance through-hole
CB_D   = 6.2;    // counterbore for the M3 x 30 head (5.35 mm + clearance)
CB_H   = 4.0;    // counterbore depth (recesses the head flush)
CHAM   = 1.0;    // top/bottom edge chamfer

module column() {
  difference() {
    // body with chamfered top + bottom edges
    hull() {
      translate([0,0,CHAM])      cylinder(d=OD, h=H-2*CHAM);
      cylinder(d1=OD-2*CHAM, d2=OD, h=CHAM);
      translate([0,0,H-CHAM])    cylinder(d1=OD, d2=OD-2*CHAM, h=CHAM);
    }
    translate([0,0,-0.1]) cylinder(d=HOLE, h=H+0.2);          // screw through-hole
    translate([0,0,H-CB_H]) cylinder(d=CB_D, h=CB_H+0.1);     // top counterbore (M3x30 head)
  }
}

column();
