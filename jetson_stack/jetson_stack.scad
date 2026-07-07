// ============================================================================
// Jetson Nano + Orin STACK FRAME  (robust 2-deck bolted cage, fits in a CW-MES box)
// ----------------------------------------------------------------------------
// Lower deck carries the Nano; four heavy corner legs rise past it; the upper
// deck bolts onto the legs and carries the Orin above. Bolted = rigid. Both
// decks vented for airflow. Drops into a CW-MES box sized to the deck footprint.
//
//   part = "assembly" | "lower" | "upper"
//   ⚠ Orin board size + mount pattern are PLACEHOLDERS — confirm and update.
// ============================================================================

part = "assembly";
$fn  = 56;

// ---- boards (CONFIRM, esp. Orin) -------------------------------------------
nano_board = [100, 80];   nano_pat = [86.14, 58.25];   // Nano dev-kit (known)
orin_board = [103, 90.5]; orin_pat = [86.14, 58.25];   // Orin dev-kit  <-- CONFIRM pattern
heatsink_h = 26;          // tallest board+heatsink stack above the board face

// ---- frame -----------------------------------------------------------------
clr     = 3;                                   // board-edge to leg gap
post    = 11;                                  // square corner leg (robust)
dt      = 3;                                   // deck thickness
boss_od = 7;  boss_h = 6;  pilot = 2.6;        // M3 self-tap board standoffs
leg_bolt = 3.4;                                // upper-deck bolt clearance
deck_x  = max(nano_board[0], orin_board[0]) + 2*(post + clr);   // ~129
deck_y  = max(nano_board[1], orin_board[1]) + 2*(post + clr);   // ~117
post_h  = dt + boss_h + 1.6 + heatsink_h + 4;  // lower-deck-top -> upper-deck underside (~40)

// ---- vents -----------------------------------------------------------------
vent_d = 6;  vent_sp = 11;

pcx = deck_x/2 - post/2 - 1;   pcy = deck_y/2 - post/2 - 1;
posts = [[-pcx,-pcy],[pcx,-pcy],[-pcx,pcy],[pcx,pcy]];
function pat(p) = [for (sx=[-1,1], sy=[-1,1]) [sx*p[0]/2, sy*p[1]/2]];

module rrect(w,h,r=4) offset(r) offset(-r) translate([-w/2,-h/2]) square([w,h]);

module vents2d(avoid) {
  for (x = [-deck_x/2+9 : vent_sp : deck_x/2-9])
    for (y = [-deck_y/2+9 : vent_sp : deck_y/2-9])
      if (min([for (m=avoid) norm([x-m[0], y-m[1]])]) > 7.5)
        translate([x,y]) circle(d=vent_d);
}

module standoffs(pl)
  for (h = pat(pl)) translate([h[0],h[1],dt-0.01])
    difference() { cylinder(d=boss_od, h=boss_h); translate([0,0,-1]) cylinder(d=pilot, h=boss_h+2); }

module lower_deck() {
  linear_extrude(dt) difference() { rrect(deck_x, deck_y); vents2d(concat(pat(nano_pat), posts)); }
  standoffs(nano_pat);                                   // Nano mounts here
  for (p = posts) translate([p[0],p[1],dt-0.01])         // corner legs
    difference() {
      translate([-post/2,-post/2,0]) cube([post, post, post_h]);
      translate([0,0,post_h-9]) cylinder(d=pilot, h=10); // pilot for upper-deck bolt
    }
}

module upper_deck() {
  linear_extrude(dt) difference() {
    rrect(deck_x, deck_y);
    vents2d(concat(pat(orin_pat), posts));
    for (p = posts) translate(p) circle(d=leg_bolt);     // bolt down to the legs
  }
  standoffs(orin_pat);                                   // Orin mounts here
}

// ---- output ----------------------------------------------------------------
if (part=="lower")      lower_deck();
else if (part=="upper") upper_deck();
else {                                                   // assembly + board mocks
  lower_deck();
  translate([0,0,dt+post_h]) upper_deck();
  color([0.12,0.42,0.22,0.55]) translate([-nano_board[0]/2,-nano_board[1]/2, dt+boss_h]) cube([nano_board[0],nano_board[1],1.6]);
  color([0.12,0.30,0.55,0.55]) translate([-orin_board[0]/2,-orin_board[1]/2, 2*dt+post_h+boss_h]) cube([orin_board[0],orin_board[1],1.6]);
}
