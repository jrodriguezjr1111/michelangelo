// ============================================================================
// CyberWing — WAGO snap plate (side-mounted, vertical)
// 4 WAGO connectors (18.03 L × 18.53 W × 8.03 H) press into a central snap
// channel and click under two flexible side rails (C-lips). Locating ridges
// between them, end stops top/bottom. Mount holes sit in the side margins,
// clear of the connectors. Mounts to a side frame's 4× M3 inserts (64×40) via
// 16 mm standoffs (separate). Print flat, snap rack UP.
// ============================================================================
$fn = 40;

PW = 47.87; PH = 71.94; T = 4;                  // plate W(X) × H(Y) × thick(Z)
MNT_X = 40; MNT_Y = 64; M3_CLR = 3.4; M3_CB_D = 6; M3_CB_H = 3;

// ---- connector (measured) ----
NC = 4;
CONN_W = 18.53;     // connector width across the rails (X)
CONN_L = 18.03;     // connector length along the column (Y), per slot
CONN_H = 8.03;      // connector depth out of the plate (snap height)
CLR = 0.3;          // press-fit clearance
LIP = 1.6; WALL_T = 2.4; LIP_T = 1.6; RIDGE_H = 1.0;
WIN_L = 14;                                       // wire-exit window length per bay (in the right rail)

CHAN = CONN_W + CLR;            // channel width between rails
railx = CHAN/2;                // inner face of each rail

// ---- plate + mount holes (in the side margins, counterbored on the front) ----
difference() {
  translate([-PW/2, -PH/2, 0]) cube([PW, PH, T]);
  for (sx=[-1,1], sy=[-1,1]) {
    translate([sx*MNT_X/2, sy*MNT_Y/2, -0.1]) cylinder(d=M3_CLR, h=T+0.2);
    translate([sx*MNT_X/2, sy*MNT_Y/2, -0.1]) cylinder(d=M3_CB_D, h=M3_CB_H);   // head counterbore on the BACK face
  }
}

// ---- two flexible side rails with inward snap lips ----
module rail(sx) {
  translate([sx*railx, -PH/2+1, T]) {
    translate([sx>0?0:-WALL_T, 0, 0]) cube([WALL_T, PH-2, CONN_H]);                 // wall
    translate([sx>0?-LIP:-WALL_T, 0, CONN_H-LIP_T]) cube([WALL_T+LIP, PH-2, LIP_T]); // top lip inward
  }
}
rail(-1);                                         // left rail (solid)
difference() {                                    // right rail with wire-exit windows (lip kept on posts)
  rail(1);
  for (by=[-27,-9,9,27])
    translate([railx-LIP-0.1, by-WIN_L/2, T-0.1]) cube([WALL_T+LIP+0.2, WIN_L, CONN_H-LIP_T+0.1]);
}

// ---- end stops (cap the column) ----
for (sy=[-1,1])
  translate([-railx, sy*(PH/2-1) - (sy>0?WALL_T:0), T]) cube([CHAN, WALL_T, CONN_H]);

// ---- locating ridges between the 4 connectors ----
for (i=[1:NC-1])
  translate([-railx, -2*CONN_L + i*CONN_L - 1, T]) cube([CHAN, 2, RIDGE_H]);
