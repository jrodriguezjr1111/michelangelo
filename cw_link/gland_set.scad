// CW-Link gland SET — the two single-cable options, visualized together.
// Imports the part meshes so both render in one scene (no param coupling).
//   left  : threaded gland (M18, Ø18.4 hole)  — body + compression nut
//   right : clamshell gland (Ø12 hole)         — split grommet, no hardware
$fn = 64;

module cable(h=78, d=4.0) color([0.82,0.46,0.22]) translate([0,0,-h/2]) cylinder(d=d, h=h);

// --- threaded gland (M18) : body + nut (exploded below) -------------------
translate([-34, 0, 0]) {
  color([0.80, 0.81, 0.85]) import("cwlink_body.stl");
  color([0.55, 0.57, 0.62]) translate([0, 0, -24]) import("cwlink_nut.stl");
  cable();
}

// --- clamshell gland (Ø12) : closed split grommet -------------------------
translate([34, 0, 0]) {
  color([0.20, 0.55, 0.85]) import("clamshell_body12.stl");
  cable();
}

// --- labels (flat on z=0) -------------------------------------------------
color([0.15, 0.15, 0.15]) linear_extrude(0.8) {
  translate([-58, -26]) text("threaded  M18 / O18.4", size=4.2);
  translate([ 18, -26]) text("clamshell  O12", size=4.2);
}
