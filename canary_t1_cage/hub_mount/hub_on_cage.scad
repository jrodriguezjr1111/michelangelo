// UHR204 hub mount (variant "dual", SPAN 125.5) on the as-built cage BACK face (photo 39), ports UP.
// Hub centred at frame x XC_HUB, terminal-block end toward the battery / V-mount (+x); the backplate on the
// inner faces of the back deck rail + back mid rail; plugs + comb rise between the back mid rail (y 259)
// and the antenna plate's back edge (y 220 EST) to the antenna level.  The MTi bridge (being printed)
// slides left along the same two rails to XC_MTI so the two share the face (> 100 mm hub-to-board).
// Numbers from ../t1_panels/asbuilt_cage.scad (face 444.5, rails z 0 / 125.5 / 211.5) and the
// ../mti_mount/mti_on_cage.scad section.  Read-only use of both mount files.
use <make_hub_mount.scad>
use <../mti_mount/make_mti_mount.scad>
FL = 444.5; DP = 279; EE = 20; RZ = [0, 125.5, 211.5];
XC_HUB = 295;          // hub centre: case x 225.9..364.1, plate 204.5..385.5, TB + plug to ~389 (battery at 392)
XC_MTI = 83;           // MTi plate x 26.5..134.1 (was 222) — board x 54..112
ANT = [[30, 414], [60, 220], 145.5, 5];   // antenna plate x, y, z, t (EST)
color([0.15, 0.15, 0.17]) {
  for (z = RZ) translate([0, DP - EE, z]) cube([FL, EE, EE]);                                   // back long rails
  for (x = [0, FL - EE]) translate([x, DP - EE, 0]) cube([EE, EE, RZ[2] + EE]);                  // back posts
  for (z = RZ) for (x = [0, FL - EE]) translate([x, 150, z]) cube([EE, DP - 150 - EE, EE]);      // end rails (stubs)
}
color([0.2, 0.2, 0.22]) for (m = [0, 1]) translate([m * FL, DP + 3.2, 0]) mirror([m, 0, 0]) rotate([90, 0, 0]) linear_extrude(3.2) {
  polygon([[0, 0], [62, 0], [62, 20], [22, 60], [0, 60]]);
  polygon([[0, 105.5], [20, 105.5], [62, 125.5], [62, 145.5], [20, 165.5], [0, 165.5]]);
}
color([0.1, 0.1, 0.11]) { translate([54, 110, 30]) cube([132, 66, 47]); translate([258, 110, 30]) cube([132, 66, 41]); }   // case back ends (y to 176)
color([0.2, 0.2, 0.22]) translate([392, 150, 22]) cube([30, 70, 120]);                                                       // battery (right end)
color([0.1, 0.1, 0.11]) translate([ANT[0][0], ANT[1][1] - 45, ANT[2]]) cube([ANT[0][1] - ANT[0][0], 45, ANT[3]]);           // antenna plate, back strip
translate([XC_MTI, DP - EE, (10 + 135.5) / 2]) rotate([90, 0, 0]) assembly();
translate([XC_HUB, DP - EE, 0]) rotate([0, 0, 180]) hub_assembly();
// clearance read-out (mirrors make_hub_mount.scad: plate 6.4, hub 35, ports centred, overmold half 8, comb bar to mount y 36.4)
YP_ABS = DP - EE - (6.4 + 17.5);
echo(str("ON CAGE: plug column abs y ", YP_ABS - 8, "..", YP_ABS + 8, " | back mid rail inner face ", DP - EE, " (", DP - EE - YP_ABS - 8, " clear)",
         " | antenna plate edge ", ANT[1][1], " (", YP_ABS - 8 - ANT[1][1], " clear; comb bar ", DP - EE - 36.4 - ANT[1][1], " clear)",
         " | TB end x ", XC_HUB + 69.12, " -> plug ~", XC_HUB + 69.12 + 20, " vs battery 392 | MTi board x ", XC_MTI - 29.05, "..", XC_MTI + 29.05,
         " -> hub case at ", XC_HUB - 69.12, " (", XC_HUB - 69.12 - XC_MTI - 29.05, " mm)"));
