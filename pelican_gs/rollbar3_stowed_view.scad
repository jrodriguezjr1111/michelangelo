// ============================================================================
// CW-AEP-002d — STOWED view: 3-piece antenna kit on the Pelican 1400 back.
// Both whips folded 90° onto their -23° diagonals, tips resting inside the
// end towers. Geometry lives in make_rollbar_3pc.scad; this file just poses it.
// Set deploy 0..90 below to animate the swing (0 = stowed, 90 = deployed V).
// ============================================================================
use <make_rollbar_3pc.scad>

deploy = 0;

pelican();
kit();
whip( 1, deploy);
whip(-1, deploy);
