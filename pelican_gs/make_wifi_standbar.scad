// ============================================================================
// CyberWing — WiFi TWIN-LANE STAND POD, Pelican 1400 back (hinge side)
// The 2 WiFi antennas are fold-over whips (Ø13.1, pivot 38 off the wall,
// 159 beyond the pivot — same as the traffic whips). They stow HORIZONTALLY,
// nose-to-tail in opposite directions in two lanes offset across the bar, and
// swing up through a full-length slot on the case-top side to deploy vertical
// (bases ±105 → 210 mm MIMO spacing). DEPLOY ORDER: slot-side lane first.
// The pod face stands 52 proud (> 21.26 hinges) and is the case's foot when
// stood on this end — print 2 HEEL blocks (part="heel") for the lid half so
// the stance is level. Rim is notched for the case's vertical ribs.
//   Model: z=0 outer/ground face, z=H at the case wall (bay opens there).
//   +Y = toward the case TOP edge (swing slot side). Print face-down.
// part = "pod" | "heel"
// ============================================================================
$fn = 48;
part = "pod";
show_whips = false;

// ---- antennas (measured — same as traffic whips) ----
WHIP_D = 13.10; WHIP_L = 159; PIVOT = 38; BASE_D = 18; BASE_H = 44.5;
BASE_X = 105;                       // base centers at ±105 (deployed = 210 apart)
LANE_Y = 14;                        // lanes at y ±14 (whips pass each other)

// ---- pod ----
BAR_L = 250; BAR_W = 66; H = 52;
WALL = 3; FACE_T = 3; CHAM = 10;
RIB_X = [-106.36, -69.94, 69.94, 106.36]; RIB_W = 12; RIB_D = 8;
M4 = 4.4;
wz = H - PIVOT;                     // whip centerline above the outer face (14)

module rrect(l, w, r) hull() for (sx=[-1,1], sy=[-1,1])
  translate([sx*(l/2-r), sy*(w/2-r)]) circle(r=r);

module pod() {
  difference() {
    union() {
      hull() {                                                    // chamfered slab
        linear_extrude(1) rrect(BAR_L-2*CHAM, BAR_W-2*CHAM, 8);
        translate([0,0,CHAM]) linear_extrude(H-CHAM) rrect(BAR_L, BAR_W, 8);
      }
      for (sx=[-1,1], sy=[-1,1])                                  // M4 lugs, hulled into the wall
        hull() {
          translate([sx*(BAR_L/2-38), sy*(BAR_W/2+5), H-8]) cylinder(d=13, h=8);
          translate([sx*(BAR_L/2-38) - 10, sy>0 ? BAR_W/2-2 : -BAR_W/2, H-8]) cube([20, 2, 8]);
        }
    }
    hull() {                                                      // bay (opens at wall)
      translate([0,0,FACE_T]) linear_extrude(1) rrect(BAR_L-2*CHAM-2*WALL, BAR_W-2*CHAM-2*WALL, 6);
      translate([0,0,CHAM+2]) linear_extrude(H-CHAM-2+0.1) rrect(BAR_L-2*WALL, BAR_W-2*WALL, 6);
    }
    translate([-BAR_L/2+16, BAR_W/2-CHAM-WALL-0.1, wz-WHIP_D/2-3])  // swing slot (+Y face)
      cube([BAR_L-32, CHAM+WALL+7.2, WHIP_D+6]);
    for (rx = RIB_X)                                              // rib relief in the rim
      translate([rx-RIB_W/2, -BAR_W/2-8, H-RIB_D]) cube([RIB_W, BAR_W+16, RIB_D+0.1]);
    for (sx=[-1,1], sy=[-1,1])                                    // M4 through lugs
      translate([sx*(BAR_L/2-38), sy*(BAR_W/2+5), H-8.1]) cylinder(d=M4, h=8.3);
    for (dx=[-80, 0, 80])                                         // face drains
      translate([dx-2, -BAR_W/2+10, -0.1]) cube([4, BAR_W-20, FACE_T+0.2]);
  }
  // lane cradles: 2 snap fingers per lane, C opens toward +Y (the swing side)
  for (lane = [[-1, -LANE_Y, 1], [1, LANE_Y, -1]]) {              // [whipdir, laneY, side]
    for (fx = [lane[0]*-25, lane[0]*-75])
      translate([lane[0]*BASE_X + fx, lane[1], 0]) cradle();
  }
}

module cradle() {                    // post + C-clip at whip height, opening +Y
  difference() {
    union() {
      translate([-3, -WHIP_D/2-3, 0]) cube([6, WHIP_D+6, wz]);
      translate([0, 0, wz]) rotate([0,90,0]) cylinder(d=WHIP_D+6, h=6, center=true);
    }
    translate([0, 0, wz]) rotate([0,90,0]) cylinder(d=WHIP_D+0.6, h=6.2, center=true);
    translate([-3.1, 0.6, wz]) cube([6.2, WHIP_D, WHIP_D]);       // C opening toward +Y, past center
  }
}

module heel() {                      // lid-half stand block (print 2)
  difference() {
    hull() {
      linear_extrude(1) rrect(40-2*8, 30-2*8, 5);
      translate([0,0,8]) linear_extrude(H-8) rrect(40, 30, 5);
    }
    for (sx=[-1,1]) {
      translate([sx*12, 0, -0.1]) cylinder(d=M4, h=H+0.2);
      translate([sx*12, 0, 4]) cylinder(d=9, h=H);                // socket-head pocket
    }
  }
}

// ---- split version: two halves bolted at a mid splice (smaller prints) ----
// Each half ends at x=0 with a 4 mm internal web. The webs bolt face-to-face
// (3× M3 + nuts, reached through the open wall side). A full-width channel at
// whip height (z 4.5..23.5) stays open across both webs — the whips cross the
// seam stowed AND sweep through it deploying. A tab in half A's outer face
// fills a notch in B's, keeping the ground face coplanar.
WEB_T = 4; CH_Z = [4.5, 23.5];
BOLTS = [[-15, 38], [15, 38], [-26, 12]];   // [y, z] on the seam webs

module web(dir) {                            // dir -1 = half A (x<0), +1 = B
  difference() {
    translate([dir>0 ? 0 : -WEB_T, -29, 3]) cube([WEB_T, 58, 47]);
    translate([dir>0 ? -0.1 : -WEB_T-0.1, -23.2, CH_Z[0]])          // whip channel
      cube([WEB_T+0.2, 52.4, CH_Z[1]-CH_Z[0]]);
    for (b = BOLTS)                                                  // M3 through
      translate([-WEB_T-0.1, b[0], b[1]]) rotate([0,90,0]) cylinder(d=3.4, h=2*WEB_T+0.2);
  }
}

module halfA() {
  intersection() { pod(); translate([-200, -100, -20]) cube([200, 200, 100]); }
  web(-1);
  translate([0, -15, 0]) cube([8, 30, 3]);                           // face tab
}
module halfB() {
  difference() {
    union() {
      intersection() { pod(); translate([0, -100, -20]) cube([200, 200, 100]); }
      web(1);
    }
    translate([-0.1, -15.2, -0.1]) cube([8.3, 30.4, 3.2]);           // tab notch
  }
}

if (part=="pod") pod();
if (part=="A") halfA();
if (part=="B") halfB();
if (part=="heel") heel();

if (show_whips && part=="pod") color([0.2,0.65,0.45,0.5])
  for (lane = [[-1,-LANE_Y],[1,LANE_Y]]) {
    translate([lane[0]*BASE_X, lane[1], H-BASE_H]) cylinder(d=BASE_D, h=BASE_H);   // base stack
    translate([lane[0]*BASE_X, lane[1], wz]) rotate([0, -lane[0]*90, 0]) cylinder(d=WHIP_D, h=WHIP_L);
  }
