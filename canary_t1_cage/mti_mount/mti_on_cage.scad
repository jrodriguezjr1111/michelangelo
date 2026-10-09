// MTi bridge mount, placement (a): VERTICAL on the inner faces of the BACK deck rail + mid rail (SPAN 125.5,
// photo 39), centred at frame x 222, board facing into the lower bay behind the cases.  Clean section of the
// as-built back face (numbers from ../t1_panels/asbuilt_cage.scad: face 444.5, rails z 0 / 125.5 / 211.5,
// front-face gussets L 62 x 60, T 62 x +/-30) + the case back ends for context.  Read-only use of the mount file.
use <make_mti_mount.scad>
FL = 444.5; DP = 279; EE = 20; RZ = [0, 125.5, 211.5];
color([0.15, 0.15, 0.17]) {
  for (z = RZ) translate([0, DP - EE, z]) cube([FL, EE, EE]);                                   // back long rails
  for (x = [0, FL - EE]) translate([x, DP - EE, 0]) cube([EE, EE, RZ[2] + EE]);                  // back posts
  for (z = RZ) for (x = [0, FL - EE]) translate([x, 20, z]) cube([EE, DP - 40, EE]);             // end rails (stubs)
}
color([0.2, 0.2, 0.22]) for (m = [0, 1]) translate([m * FL, DP + 3.2, 0]) mirror([m, 0, 0]) rotate([90, 0, 0]) linear_extrude(3.2) {
  polygon([[0, 0], [62, 0], [62, 20], [22, 60], [0, 60]]);
  polygon([[0, 105.5], [20, 105.5], [62, 125.5], [62, 145.5], [20, 165.5], [0, 165.5]]);
}
color([0.1, 0.1, 0.11]) { translate([54, 70, 30]) cube([132, 106, 47]); translate([258, 70, 30]) cube([132, 106, 41]); }   // cases (backs at y 176)
color([0.2, 0.2, 0.22]) translate([392, 120, 22]) cube([30, 100, 120]);                                                      // battery at the right end
translate([FL / 2, DP - EE, (10 + 135.5) / 2]) rotate([90, 0, 0]) assembly();
