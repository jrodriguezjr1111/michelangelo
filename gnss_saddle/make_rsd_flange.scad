// ============================================================================
// CyberWing — RSD flange  (bolts flush to the stack's +X long-side M3 inserts,
// spans both frames; carries the RSD converter on 4× #8-32).
// Frame-mount M3 pattern = the existing side inserts: Y=±20 (40), Z=7 & 61 (54).
// RSD pattern = 4× #8-32 at 120.18 (horizontal) × 51.83 (vertical).
// Printed flat; mounts in the Y-Z plane on the stack.
// ============================================================================
$fn = 56;
U = 132; V = 62; T = 4;                 // plate (U=horizontal/Y, V=vertical/Z)
RSD_PU = 120.18; RSD_PV = 51.83; RSD_CLR = 4.5;   // #8-32 clearance
MNT_PU = 40; MNT_PV = 54;               // frame-mount M3 (Y=±20, Z=±27)
M3_CLR = 3.4; M3_CB_D = 6.0; M3_CB_H = 3.0;

difference() {
  translate([-U/2, -V/2, 0]) cube([U, V, T]);
  // RSD #8-32 clearance holes
  for (su=[-1,1], sv=[-1,1])
    translate([su*RSD_PU/2, sv*RSD_PV/2, -0.1]) cylinder(d=RSD_CLR, h=T+0.2);
  // frame-mount M3 through-holes + head counterbore on the front (RSD) face
  for (su=[-1,1], sv=[-1,1]) {
    translate([su*MNT_PU/2, sv*MNT_PV/2, -0.1]) cylinder(d=M3_CLR, h=T+0.2);
    translate([su*MNT_PU/2, sv*MNT_PV/2, T-M3_CB_H]) cylinder(d=M3_CB_D, h=M3_CB_H+0.1);
  }
}
