// ============================================================================
// CONCEPT D — T-SLOT CARTRIDGE DETAIL (massing-level, 80/20 20-series)
// The load-bearing element of the extrusion-frame concept: a printed ASA T-key
// on each side wall of the cartridge rides the facing slot of a 20-2020 mullion
// (Z-direction track; the cartridge drops in from the top).  Shown: one mullion,
// the cartridge side wall + faceplate return, its key in the slot, the captive
// M5 thumbscrew through the faceplate return into a slide-in T-nut in the
// mullion's front slot, the pull tab, the locking pigtail.
// Concept numbers only; the 20-series slot cavity (11.0) is to be read from the
// 80/20 CAD model (20-2020) before any key is cut.
// view = "plan" (horizontal section through the thumbscrew axis, from above)
//      | "iso"
// ============================================================================
view = "plan";
$fn = 40;
BLK = [0.19,0.19,0.21]; BLK2 = [0.29,0.29,0.32]; YEL = [1,0.8,0]; ANO = [0.15,0.15,0.17]; MET = [0.55,0.56,0.6];
E = 20; SLT = 6.0; SLD = 6.0; CAV = 11.0; CLR = 0.4;      // 20-2020 (cavity: verify in vendor CAD)
KEY_L = 88; NECK = SLT - CLR; HEAD = CAV - 0.6; HEAD_T = 2.0; LEAD = 1.0;
WALL = 4; H = 96; MX = E/2 + CLR/2;                         // mullion centre x; its -X face at x = CLR/2

module slab() { translate([-60, -100, H - 17]) cube([200, 200, 3]); }   // cut plane = thumbscrew axis (z = H-14)
module C(col) { if (view == "plan") color(col) render() intersection() { children(); slab(); } else color(col) children(); }

module extrusion(len) {                                     // along +Z, centred; slot on every face
  C(ANO) difference() {
    translate([-E/2, -E/2, 0]) cube([E, E, len]);
    for (r = [0, 90, 180, 270]) rotate([0, 0, r]) {
      translate([E/2 - SLD, -SLT/2, -1]) cube([SLD + 1, SLT, len + 2]);
      translate([E/2 - SLD - 2.5, -CAV/2, -1]) cube([2.5, CAV, len + 2]);
    }
    translate([0, 0, -1]) cylinder(d = 4.2, h = len + 2);
  }
}
module tkey() {                                              // grows +X from the wall face at x = 0
  C(BLK2) {
    hull() { translate([0, -NECK/2, LEAD]) cube([SLD + 0.4, NECK, KEY_L - 2*LEAD]);
             translate([0, -NECK/2 + LEAD, 0]) cube([SLD + 0.4, NECK - 2*LEAD, KEY_L]); }
    hull() { translate([SLD + 0.39, -HEAD/2, LEAD]) cube([HEAD_T, HEAD, KEY_L - 2*LEAD]);
             translate([SLD + 0.39, -HEAD/2 + LEAD, 0]) cube([HEAD_T - 0.6, HEAD - 2*LEAD, KEY_L]); }
  }
}
module tnut() {                                              // slide-in economy T-nut in the mullion's -Y slot (14122 class)
  C(MET) translate([MX - (CAV - 0.6)/2, -E/2 + 0.2, H - 20]) difference() {
    cube([CAV - 0.6, SLD + 2.3, 12]);
    translate([(CAV - 0.6)/2, -1, 6]) rotate([-90, 0, 0]) cylinder(d = 4.2, h = 12);
  }
}
module thumb() {                                             // captive M5 thumbscrew, shank along +Y
  C(YEL) rotate([-90, 0, 0]) { cylinder(d = 11, h = 7, $fn = 12); cylinder(d = 5, h = 7 + 6 + 2 + SLD + 4, $fn = 24);
                                   translate([0, 0, 7]) cylinder(d = 10, h = 1.2); }            // washer face
}
module scene() {
  translate([MX, 0, 0]) extrusion(H + 20);                                          // mullion
  C(BLK) translate([-WALL, -80, 0]) cube([WALL, 92, H]);                            // cartridge side wall
  translate([0, 0, 4]) tkey();                                                      // key: neck in the slot, head in the cavity
  C(BLK) difference() { translate([-WALL - 10, -E/2 - 6 - 1.5, H - 26]) cube([E + WALL + 10, 6, 22]);   // faceplate return (lug)
                        translate([MX, -E/2 - 20, H - 14]) rotate([-90, 0, 0]) cylinder(d = 5.4, h = 30); }   // M5 clearance bore
  tnut();
  translate([MX, -E/2 - 6 - 1.5 - 7, H - 14]) thumb();
  C(YEL) translate([-WALL - 10, -E/2 - 6 - 1.5 - 8, H - 22]) cube([10, 8, 7]);   // pull tab
  C([0.3,0.3,0.32]) translate([-WALL - 16, -30, 30]) rotate([90, 0, 0]) cylinder(d = 5, h = 38);   // pigtail
  C(MET) translate([-WALL - 16, -68, 30]) rotate([90, 0, 0]) cylinder(d = 10, h = 12, $fn = 6);     // locking connector
  C(YEL) translate([-WALL - 16, -71, 30]) rotate([90, 0, 0]) cylinder(d = 11.5, h = 3);
}
scene();
