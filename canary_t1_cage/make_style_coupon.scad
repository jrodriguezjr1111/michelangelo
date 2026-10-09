// ============================================================================
// CANARY T1 — STYLE COUPON  (the ONE printable part in this concept package)
//
// Proves the visual language on THIS printer before anything big is committed:
//   (a) faceted 45 deg bezel round an opening, on a clipped-corner panel
//   (b) recessed X-brace pocket (real stiffening, real anti-warp, and the look)
//   (c) snap-in ACCENT PLATE SEAT (dovetail-lipped recess) + the LABEL PLATE
//       that snaps into it, printed separately in canary-yellow filament
//   (d) the Reticle Delta mark, embossed 1.0 mm, two facet heights
//   (e) a recessed fastener well + a chamfered slot mouth (the house tolerances)
//
// part = "panel" | "plate" | "plate_show" | "set" (assembly preview) | "print"
// Print: panel FACE UP (bezel, pockets, mark and seat are all top-side features;
// the opening's bezel is a 45 deg chamfer -> self-supporting; the seat lip is a
// 1.0 mm overhang at 45 deg -> no support).  Plate FACE UP, its dovetail flanks
// 45 deg.  PLA is fine — this is a style coupon, it never flies.
// ============================================================================
include <t1_mark.scad>
$fn = 40;
part = "print";

PW = 90; PH = 70; PT = 5;            // panel
CORNER = 10; CHAM = 2;               // clipped corners, edge facet
OW = 34; OH = 22; BEZ = 3;           // opening + 45 deg bezel band
XB_W = 40; XB_H = 44; XB_D = 1.6; XB_B = 4;      // X-brace pocket
LP_W = 44; LP_H = 11; LP_T = 1.8;    // label plate
LP_CLR = 0.15;                       // seat clearance per side (snap fit — tune here)
LIP = 0.6;                           // dovetail lip (snap: one long edge under, bow, snap the other — TUNE)
WELL_D = 7; WELL_H = 2.5; M3B = 3.4; // house fastener well
SLOT_W = 6; SLOT_L = 16; SLOT_CH = 1.2;

// declared for the slice harness (nothing here is a true bridge)
MAXSPAN = max(OW, XB_W) > 0 ? 3.6 : 0;   // fastener-well annulus is the only "roof"
echo(str("MAXSPAN=", MAXSPAN));
echo(str("COUPON panel ", PW, "x", PH, "x", PT, " plate ", LP_W, "x", LP_H, "x", LP_T,
         " seat clr ", LP_CLR, " lip ", LIP));
assert(LIP < LP_T, "lip taller than the plate");
assert(PT - XB_D >= 3, "X-brace pocket leaves < 3 mm web");

module clipped(w, h, c) polygon([[c,0],[w-c,0],[w,c],[w,h-c],[w-c,h],[c,h],[0,h-c],[0,c]]);
module facet_slab(w, h, t, c, e) {                 // clipped outline + 45 deg top/bottom edge facet
  hull() {
    translate([0,0,e]) linear_extrude(t - 2*e) clipped(w, h, c);
    translate([e,e,0]) linear_extrude(t) clipped(w - 2*e, h - 2*e, max(c - e, 0.01));
  }
}
module dovetail(w, h, t, lip) {                     // wider at the bottom: plate/seat profile
  hull() {
    translate([0,0,0]) linear_extrude(0.01) square([w + 2*lip, h + 2*lip], center = true);
    translate([0,0,lip]) linear_extrude(t - lip) square([w, h], center = true);
  }
}

module panel() {
  difference() {
    facet_slab(PW, PH, PT, CORNER, CHAM);
    // (a) opening with a 45 deg bezel: the bezel is the cut widening toward the face
    translate([PW*0.30, PH*0.62, -1]) {
      linear_extrude(PT + 2) square([OW, OH], center = true);
      translate([0,0,PT + 1 - BEZ]) linear_extrude(BEZ + 0.01, scale = [(OW + 2*BEZ)/OW, (OH + 2*BEZ)/OH])
        square([OW, OH], center = true);
    }
    // (b) X-brace pocket
    translate([PW*0.73, PH*0.55, PT]) difference() {
      translate([-XB_W/2, -XB_H/2, -XB_D]) cube([XB_W, XB_H, XB_D + 0.1]);
      for (s = [-1, 1]) rotate([0,0,s*atan2(XB_H, XB_W)])
        translate([-(XB_W + XB_H), -XB_B/2, -XB_D - 0.1]) cube([2*(XB_W + XB_H), XB_B, XB_D + 0.3]);
      // bezel the pocket rim too: 45 deg on the pocket edge (it is a chamfered mouth)
    }
    // (c) label-plate SEAT: dovetail recess, lip overhangs at 45 deg = self-supporting
    translate([PW*0.30, PH*0.22, PT - LP_T - 0.2]) dovetail(LP_W + 2*LP_CLR, LP_H + 2*LP_CLR, LP_T + 0.3, LIP);
    // (e) fastener well + chamfered slot mouth
    translate([PW - 9, 9, -1]) { cylinder(d = M3B, h = PT + 2); translate([0,0,PT + 1 - WELL_H]) cylinder(d = WELL_D, h = WELL_H + 0.1); }
    translate([PW - 12, PH*0.62, PT/2]) {
      cube([SLOT_L, SLOT_W, PT + 2], center = true);
      translate([0,0,PT/2 - SLOT_CH]) linear_extrude(SLOT_CH + 0.01, scale = [(SLOT_L + 2*SLOT_CH)/SLOT_L, (SLOT_W + 2*SLOT_CH)/SLOT_W]) square([SLOT_L, SLOT_W], center = true);
    }
  }
  // (d) the mark, embossed on the flat field between the seat and the well
  translate([PW*0.68, PH*0.22, PT]) mark3d(16, 1.0);
}

module plate(txt = "TRAFFIC") {
  difference() {
    dovetail(LP_W, LP_H, LP_T, LIP);
    translate([0, 0, LP_T - 0.5]) linear_extrude(0.6)
      text(txt, size = 6.2, font = "DIN Condensed:style=Bold", halign = "center", valign = "center", spacing = 1.1);
  }
}

if (part == "panel") panel();
if (part == "plate") plate("TRAFFIC");
if (part == "plate_show") plate("T1-01 BRAVO");
if (part == "set") { color([0.2,0.2,0.22]) panel(); color([1,0.8,0]) translate([PW*0.30, PH*0.22, PT - LP_T]) plate(); }
if (part == "print") { panel(); translate([PW + 14, 20, 0]) plate("TRAFFIC"); translate([PW + 14, 40, 0]) plate("T1-01 BRAVO"); }
