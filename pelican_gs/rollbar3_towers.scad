// ============================================================================
// CW-AEP-002d — END TOWERS only (2× identical, x-symmetric — same part fits
// both ends). Twin full-height fins flank the whip's swing band (y 22..38
// open), joined by the bottom shelf with a shallow V whip-rest; 2× M5
// countersunk in the ground fin. Geometry lives in make_rollbar_3pc.scad.
// Shown in print pose (shelf down). Set count = 1 for a single tower.
// ============================================================================
use <make_rollbar_3pc.scad>

count = 2;
spacing = 60;

for (i = [0 : count-1])
    translate([i*spacing, 0, 0]) tower();
