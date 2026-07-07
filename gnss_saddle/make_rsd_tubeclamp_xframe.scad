// ============================================================================
// CyberWing — RSD mount with a Nano-style tube clamp (length-wise)
// Bottom: a tube-clamp block (half-pipe scoops + 4× M4) that grips both GNSS
// tubes along their length and mates the existing nano_tubeclamp_lower half.
// Up top: the RSD flange (4× #8-32, 120.18 × 51.83) rises from the clamp,
// shifted above the tubes. Gussets brace it.
//   Stack coords: X = tube axis (clamp juts out +X); Y = across; Z = up.
// ============================================================================
$fn = 56;
show_tubes = false;

// ---- tubes / Nano clamp (leveraged) ----
TUBE_OD = 15.39; CLR = 0.4; R_IN = TUBE_OD/2 + CLR/2; TUBE_Y = 60.17/2;  // 30.085
M4_P = 18; M4_CLR = 4.4; M4_CB_D = 8.5; M4_CB_H = 4.5;
CLAMP_LEN = 50; CLAMP_W = 72; CLAMP_H = 14;         // X len, Y width, Z height

// ---- RSD flange ----
RSD_PY = 120.18; RSD_PZ = 51.83; RSD_CLR = 4.5;
FLANGE_T = 5; FLANGE_W = 132; RSD_Zc = 42;          // flange thick, width, RSD center Z
FL_TOP = RSD_Zc + RSD_PZ/2 + 6;                     // ~74

clamp_x0 = FLANGE_T;                                 // clamp starts behind the flange
cxc = clamp_x0 + CLAMP_LEN/2;                        // clamp center X

module clamp() {
  difference() {
    translate([clamp_x0, -CLAMP_W/2, 0]) cube([CLAMP_LEN, CLAMP_W, CLAMP_H]);
    for (sy=[-1,1]) translate([-0.2, sy*TUBE_Y, 0]) rotate([0,90,0]) cylinder(r=R_IN, h=clamp_x0+CLAMP_LEN+0.4);  // scoops
    for (sx=[-1,1], sy=[-1,1]) {                      // 4× M4 + nut counterbore (top)
      translate([cxc+sx*M4_P, sy*M4_P, -0.1]) cylinder(d=M4_CLR, h=CLAMP_H+0.2);
      translate([cxc+sx*M4_P, sy*M4_P, CLAMP_H-M4_CB_H]) cylinder(d=M4_CB_D, h=M4_CB_H+0.1);
    }
  }
}

module flange() {
  difference() {
    translate([0, -FLANGE_W/2, CLAMP_H]) cube([FLANGE_T, FLANGE_W, FL_TOP-CLAMP_H]);
    for (sy=[-1,1], sz=[-1,1])
      translate([-0.1, sy*RSD_PY/2, RSD_Zc+sz*RSD_PZ/2]) rotate([0,90,0]) cylinder(d=RSD_CLR, h=FLANGE_T+0.2);
  }
}

// gussets: flange back -> clamp top (a few along Y)
module gussets() {
  for (gy=[-50,-25,0,25,50])
    translate([FLANGE_T, gy-2, CLAMP_H]) hull() {
      cube([0.1, 4, 30]);                 // tall edge at flange
      translate([28, 0, 0]) cube([0.1, 4, 0.1]);  // reach back over the clamp
    }
}

clamp(); flange(); gussets();

if (show_tubes)
  color([0.55,0.42,0.62,0.4])
  for (sy=[-1,1]) translate([-25, sy*TUBE_Y, 0]) rotate([0,90,0]) cylinder(d=TUBE_OD, h=110);
