// ============================================================================
// CyberWing — Jetson drone-frame STACK  (CONCEPT / visualization only)
//   base X-frame (clamps tubes)  ->  Nano deck  ->  Orin deck
//   shared 172 x 104 corner columns, M3 inserts join each level.
//   Orin pattern/heights are PLACEHOLDERS — confirm before building real parts.
// ============================================================================
$fn = 48;

// ---- shared geometry ----
CX = 86;  CY = 52;                 // corner column pattern (172 x 104)
TUBE_X = 30.085;  TUBE_OD = 15.39; // tubes run along Y at X = +/-30

nano_pat = [86.14, 58.25];  nano_board = [100, 80,  1.6];   // Nano (known)
orin_pat = [86.14, 58.25];  orin_board = [103, 90.5, 1.6];  // Orin (PLACEHOLDER)

base_top_z = 14;     // base insert face height
col_nano   = 22;     // base top  -> Nano deck underside
col_orin   = 42;     // Nano deck -> Orin deck (heatsink clearance)
deck_t  = 4;         // deck plate thickness
post_od = 13;        // corner column OD
boss_od = 7;  boss_h = 6;          // board standoffs
nano_hs = 26; orin_hs = 28;        // heatsink mock heights

nano_z = base_top_z + col_nano;
orin_z = nano_z + deck_t + col_orin;

// ---- the real base X-frame, flipped to in-use pose (scoops down, inserts up) ----
module base() {
  color([0.25,0.45,0.72,0.9])
    translate([0,0,base_top_z]) rotate([180,0,0])
      import("jetson_tube_xframe.stl");
}

// ---- 2 GNSS tubes for context ----
module tubes() {
  color([0.42,0.32,0.6,0.45])
    for (sx=[-1,1]) translate([sx*TUBE_X,-75,0]) rotate([-90,0,0]) cylinder(d=TUBE_OD,h=150);
}

// ---- corner columns between two levels (M3 bore through) ----
module columns(z0,h,col) {
  color(col)
  for (sx=[-1,1], sy=[-1,1])
    translate([sx*CX, sy*CY, z0]) difference() {
      cylinder(d=post_od, h=h);
      translate([0,0,-0.1]) cylinder(d=3.4, h=h+0.2);
    }
}

// ---- a drone deck: hub + 4 arms to corners + board standoffs + board/heatsink mock ----
module deck(z, pat, board, hs, col) {
  translate([0,0,z]) {
    color(col) linear_extrude(deck_t) {
      offset(r=6) square([pat[0]+8, pat[1]+8], center=true);     // hub
      for (sx=[-1,1], sy=[-1,1])                                  // arms
        hull() {
          translate([sx*pat[0]/2, sy*pat[1]/2]) circle(d=10);
          translate([sx*CX, sy*CY]) circle(d=post_od);
        }
    }
    color(col) for (sx=[-1,1], sy=[-1,1])                          // board standoffs
      translate([sx*pat[0]/2, sy*pat[1]/2, deck_t]) cylinder(d=boss_od, h=boss_h);
    color([0.18,0.5,0.3,0.55])                                     // board mock
      translate([-board[0]/2,-board[1]/2, deck_t+boss_h]) cube(board);
    color([0.55,0.55,0.6,0.5])                                     // heatsink mock
      translate([-board[0]*0.35,-board[1]*0.35, deck_t+boss_h+board[2]])
        cube([board[0]*0.7, board[1]*0.7, hs]);
  }
}

// ---- assembly ----
tubes();
base();
columns(base_top_z, col_nano, [0.25,0.45,0.72,0.9]);
deck(nano_z, nano_pat, nano_board, nano_hs, [0.18,0.55,0.55,0.9]);
columns(nano_z+deck_t, col_orin, [0.18,0.55,0.55,0.9]);
deck(orin_z, orin_pat, orin_board, orin_hs, [0.88,0.42,0.36,0.9]);
