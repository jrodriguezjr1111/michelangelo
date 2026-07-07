// ============================================================================
// CO clamshell — HALF B (pilot half, boards lay in here first). Geometry lives
// in make_co_clamshell.scad; this file just poses it. orient = "print"
// (seam-face down, as sliced) or "assembled" (in-place, y>0 half).
// ============================================================================
use <make_co_clamshell.scad>
orient = "print";

if (orient == "print") rotate([90,0,0]) halfB();
else halfB();
