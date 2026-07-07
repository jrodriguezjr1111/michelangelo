// ============================================================================
// Vibration-isolating foot — RSD/Jetson box -> Pelican floor  (print 4, PLA)
// ----------------------------------------------------------------------------
// Bolts to a box bottom corner (M4 heat-set insert, top). A Ø16 rubber bumper
// presses into the bottom recess; the box rests on the four rubber feet on the
// Pelican floor and the case lid/foam retains it — so vibration is damped by
// the rubber, not transmitted through a rigid bolt.
// ============================================================================

$fn = 80;
BASE_D = 28;      // wide base for stability
TOP_D  = 18;      // tapers up to the box
H      = 16;      // standoff height
INS_D  = 5.6;     // M4 heat-set insert bore (top, to box)
INS_H  = 6;
RUB_D  = 16.4;    // stick-on rubber bumper recess (bottom)
RUB_H  = 4;

module iso_foot() {
  difference() {
    hull() {                                         // tapered body
      cylinder(d = BASE_D, h = 0.1);
      translate([0, 0, H]) cylinder(d = TOP_D, h = 0.1);
    }
    translate([0, 0, H - INS_H]) cylinder(d = INS_D, h = INS_H + 0.1);   // box M4 insert
    translate([0, 0, -0.05])     cylinder(d = RUB_D, h = RUB_H);          // rubber bumper recess
  }
}

iso_foot();
