// ============================================================================
// CyberWing — component plate, 53.68 × 40.22 M3 standoffs + dual mount patterns
// Board sits on 4 standoffs (53.68 × 40.22, M3 clearance through). The plate
// itself mounts via two centered M3 hole patterns: 78.67 × 35.52 (outer) and
// 45 × 20 (inner). Print flat.
// ============================================================================
$fn = 48;

PLATE_X = 90; PLATE_Y = 48; T = 4;
SO_PX = 53.68; SO_PY = 40.22;          // standoff pattern
SO_OD = 6; SO_H = 10; M3 = 3.4;        // Ø6 standoffs, M3 clearance
MNT_A = [78.67, 35.52];                // outer mount pattern
MNT_C = [45, 20];                      // inner mount pattern

difference() {
  union() {
    translate([-PLATE_X/2, -PLATE_Y/2, 0]) cube([PLATE_X, PLATE_Y, T]);   // plate
    for (sx=[-1,1], sy=[-1,1])                                            // 4 standoffs
      translate([sx*SO_PX/2, sy*SO_PY/2, T]) cylinder(d=SO_OD, h=SO_H);
  }
  for (sx=[-1,1], sy=[-1,1]) {
    translate([sx*SO_PX/2, sy*SO_PY/2, -0.1]) cylinder(d=M3, h=T+SO_H+0.2);  // standoff bores
    for (p=[MNT_A, MNT_C])                                                   // mount holes
      translate([sx*p[0]/2, sy*p[1]/2, -0.1]) cylinder(d=M3, h=T+0.2);
  }
}
