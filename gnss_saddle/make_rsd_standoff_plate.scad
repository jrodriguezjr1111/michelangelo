// ============================================================================
// CyberWing — RSD plate on the stack's +X long-side M3 inserts (tube-clearing)
// Mounts to the Nano + Orin +X-face M3 inserts (40.54 × 53.64 grid). The RSD
// plate is shifted UP 10 mm to clear the GNSS tubes, the UPPER (Orin) standoffs
// are Ø7.8 × 14, and the LOWER (Nano) standoffs are thinned to Ø4.2 × 14 (with
// thin tabs down to them) so they clear the tubes that pass just below.
//   model X = stack Y (across) ;  model Y = stack Z (up) ;  model Z = mount-out
// Set show_tubes=true to overlay the GNSS tubes for a clearance check.
// ============================================================================
$fn = 48;
show_tubes = false;

INS_X = 40.54; INS_Y = 53.64; GX = INS_X/2; GY = INS_Y/2;   // grid ±20.27, ±26.82
SO_UP = 7.8; SO_LO = 4.2; SO_H = 14; SO_BORE = 3.4;          // upper/lower standoffs
RSD_X = 120.18; RSD_Y = 51.83; RSD_CLR = 4.5;
PW = 132; PT = 5; SHIFT = 10;                                // plate, shifted up
PYc = SHIFT; PV = 56; PY0 = PYc - PV/2; PY1 = PYc + PV/2;    // plate Y = -18..38
M3_CB_D = 6; M3_CB_H = 3; TAB_W = 5;

module part() {
  difference() {
    union() {
      translate([-PW/2, PY0, 0]) cube([PW, PY1-PY0, PT]);                 // main plate (shifted up)
      for (sx=[-1,1]) translate([sx*GX-TAB_W/2, -GY, 0]) cube([TAB_W, PY0+GY, PT]); // tabs to lower standoffs
      for (sx=[-1,1]) translate([sx*GX,  GY, PT]) cylinder(d=SO_UP, h=SO_H);        // upper standoffs Ø7.8
      for (sx=[-1,1]) translate([sx*GX, -GY, PT]) cylinder(d=SO_LO, h=SO_H);        // lower standoffs Ø4.2
    }
    for (sx=[-1,1], sy=[-1,1]) {                                          // M3 clearance + counterbore
      translate([sx*GX, sy*GY, -0.1]) cylinder(d=SO_BORE, h=PT+SO_H+0.2);
      translate([sx*GX, sy*GY, -0.1]) cylinder(d=M3_CB_D, h=M3_CB_H);
    }
    for (sx=[-1,1], sy=[-1,1])                                            // RSD #8-32 (shifted up)
      translate([sx*RSD_X/2, PYc + sy*RSD_Y/2, -0.1]) cylinder(d=RSD_CLR, h=PT+0.2);
  }
}

part();

if (show_tubes)                                                          // GNSS tubes: stack Z=0 -> model Y=-34
  color([0.55,0.42,0.62,0.45])
  for (sx=[-1,1]) translate([sx*30.085, -34, -40]) cylinder(d=15.39, h=120);
