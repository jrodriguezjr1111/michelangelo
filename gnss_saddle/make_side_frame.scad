// ============================================================================
// CyberWing — side component frame  (print 2: ±Y short sides)
// Bolts flush to the stack's ±Y short-side M3 inserts (X=±20 / 40, Z=7 & 61 / 54)
// and presents 4× M3 heat-set inserts (on raised bosses) for the user's
// relay/ESP/FeatherWing plate. Framework only — component holes added later.
// Printed flat; mounts in the X-Z plane on the stack.
// ============================================================================
$fn = 56;
SU = 92; SV = 62; T = 4;                // plate (SU=X, SV=Z)
MNT_PU = 40; MNT_PV = 54;              // frame-mount M3 (to the ±Y inserts)
PLATE_PU = 64; PLATE_PV = 40;          // M3 inserts for the component plate
M3_CLR = 3.4; M3_CB_D = 6.0; M3_CB_H = 3.0;
INS_D = 4.0; INS_H = 6.0; BOSS_D = 8; BOSS_H = 5;

difference() {
  union() {
    translate([-SU/2, -SV/2, 0]) cube([SU, SV, T]);
    // raised bosses to host the M3 inserts (4mm plate alone is too thin)
    for (su=[-1,1], sv=[-1,1])
      translate([su*PLATE_PU/2, sv*PLATE_PV/2, T]) cylinder(d=BOSS_D, h=BOSS_H);
  }
  // frame-mount M3 through-holes + head counterbore on the outer face
  for (su=[-1,1], sv=[-1,1]) {
    translate([su*MNT_PU/2, sv*MNT_PV/2, -0.1]) cylinder(d=M3_CLR, h=T+0.2);
    translate([su*MNT_PU/2, sv*MNT_PV/2, T-M3_CB_H]) cylinder(d=M3_CB_D, h=M3_CB_H+0.1);
  }
  // M3 heat-set inserts (open on the boss tops, toward the component plate)
  for (su=[-1,1], sv=[-1,1])
    translate([su*PLATE_PU/2, sv*PLATE_PV/2, T+BOSS_H-INS_H]) cylinder(d=INS_D, h=INS_H+0.1);
}
