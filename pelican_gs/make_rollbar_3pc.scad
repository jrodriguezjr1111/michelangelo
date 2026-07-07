// =============================================================
//  CW-AEP-002d — WiFi Antenna Kit, Pelican 1400 — THREE PIECES
//  1x CENTER BLOCK + 2x IDENTICAL END TOWERS (QIDI + PLA)
// -------------------------------------------------------------
//  CENTER BLOCK (1x): both antennas SCREW IN here. Jack axes are
//   tilted 67 deg up-outward, so:
//     EXTENDED (straight) = DEPLOYED: near-vertical V (+/-23 deg)
//     FOLDED 90 deg       = STOWED : diagonal down-outboard (-23),
//   whips descend across the face, tips land inside the end towers.
//   C-cradles near the roots retain the stowed whips. Bolts on the
//   base half only; pocket clears the hinge knuckles (21.26 mm).
//  END TOWER (2x, one STL, x-symmetric -> same part both ends):
//   two full-height fins flank the whip's swing plane (y 22..38
//   stays open), joined by a bottom shelf. The whip sweeps BETWEEN
//   the fins; the fins take the vertical stance (outer faces
//   coplanar with the center block's) and shield the stowed tips.
//  NOTE: stowed whips cross the lid zone — fold antennas up (or
//   unscrew) before opening the case.
//  PRINT: PLA 0.20, >=4 walls, BED 60 C, 5 mm brim, no supports.
//  part = "center"|"tower"|"stowed"|"deployed"|"mid"
//       | "center_print"|"tower_print"
// =============================================================

$fn = $preview ? 40 : 72;
part = "deployed";

/* ============ measured case / antennas ============ */
case_w  = 340;  case_h = 152;  hinge_z = 42;
knuckle_clear = 22;        // hinge knuckles 21.26 + margin
knuckle_band  = [32, 52];  // z band the knuckles occupy
rib_relief = [69.94, 106.36, 128.6]; rib_w = 13; rib_d = 8;
whip_d = 13.10;  whip_l = 159;  knuckle = 20;   // jack face -> pivot (CONFIRM)
sma_hole = 6.5;

/* ============ geometry ============ */
stand   = 46;              // ground plane distance (all outer faces coplanar)
ax_deg  = 67;              // jack axis elevation -> stow at -(90-ax_deg) = -23
jdx     = 9;               // jack faces at x = +/-9
jz      = 62;              // jack face height
bay_y   = 30;              // whip centreline depth (clears knuckles: 22+6.6+1)
stow    = 90 - ax_deg;     // 23 deg below horizontal
pivx    = jdx + knuckle*cos(ax_deg);   // 16.8
pivz    = jz  + knuckle*sin(ax_deg);   // 80.4
tipx    = pivx + whip_l*cos(stow);     // 163.2
tipz    = pivz - whip_l*sin(stow);     // 18.3

// center block
cb_w = 84;  cb_side_h = 58;  cb_top_h = 70;  cb_top_w = 40;
// end towers
tw_cx = 156;               // tower centre |x|
tw_w  = 22;  tw_h = 48;  fin_t = 8;  shelf_h = 7;
slot_y = [22, 38];         // open band the whip lives/swings in
m5 = 5.4;  csk = 10.4;  m3 = 3.4;

echo(str("stowed tip at (", tipx, ", ", tipz, ") — inside tower x ",
         tw_cx-tw_w/2, "..", tw_cx+tw_w/2));

/* ================= CENTER BLOCK ================= */
module cradle_at(px, pz) {   // robust U-saddle: 4.5 mm cheeks, mouth faces the
    U_W = whip_d + 0.8;      // whip's swing-approach direction (67 deg up-out)
    difference() {
        union() {
            translate([px, bay_y, pz]) rotate([0, stow, 0])          // saddle body
                translate([-7, -U_W/2-4.5, -12]) cube([14, U_W+9, 20]);
            translate([px-7, bay_y-U_W/2-4.5, pz-24]) cube([14, U_W+9, 16]); // root into the block
        }
        translate([px, bay_y, pz]) rotate([0, stow, 0]) {
            rotate([0, 90, 0]) translate([0,0,-7.2]) cylinder(d=U_W, h=14.4); // rounded seat
            translate([-7.2, -U_W/2, 0]) cube([14.4, U_W, 14]);              // U mouth, open up-out
        }
    }
}

module center() {
    color("#FFC60A") {
        difference() {
            // chevron block, profile in X-Z, depth 0..stand
            translate([0, stand, 0]) rotate([90,0,0]) linear_extrude(stand)
                polygon([[-cb_w/2,0],[cb_w/2,0],[cb_w/2,cb_side_h],
                         [cb_top_w/2,cb_top_h],[-cb_top_w/2,cb_top_h],
                         [-cb_w/2,cb_side_h]]);
            // hinge-knuckle pocket (nothing below y=knuckle_clear in the band)
            translate([-cb_w/2-1, -0.1, knuckle_band[0]])
                cube([cb_w+2, knuckle_clear+0.1, knuckle_band[1]-knuckle_band[0]]);
            // jack bores along the 67-deg axes
            for (s=[-1,1]) translate([s*jdx, bay_y, jz]) rotate([0, s*(90-ax_deg), 0]) {
                cylinder(d=sma_hole, h=30, center=true);
                translate([0,0,6]) cylinder(d=11, h=14);      // jack body seat
            }
            // coax bores to the case face
            for (s=[-1,1]) translate([s*jdx, -1, jz-14]) rotate([-90,0,0])
                cylinder(d=8, h=knuckle_clear+8);
            // 4x M5 low on the base half, countersunk in the ground face
            for (sx=[-1,1], zz=[10, 24])
                translate([sx*(cb_w/2-12), -1, zz]) rotate([-90,0,0]) {
                    cylinder(d=m5, h=stand+2);
                    translate([0,0,stand-2.3]) cylinder(d1=m5, d2=csk, h=2.31);
                    translate([0,0,stand+0.9]) cylinder(d=csk, h=1.2);
                }
            // rib relief (inner rib pair crosses the block at +/-69.94? outside cb_w/2=42 -> skipped)
            for (s=[-1,1], rx=rib_relief) if (rx < cb_w/2-2)
                translate([s*rx-rib_w/2, -0.1, -1]) cube([rib_w, rib_d, cb_top_h+2]);
        }
        // stow U-saddles near the roots (whips rest in at -23 deg)
        for (s=[-1,1]) mirror([s<0?1:0,0,0])
            cradle_at(pivx+24*cos(stow), pivz-24*sin(stow));
    }
}

/* ================= END TOWER (identical, x-symmetric) ================= */
module tower() {
    color("#FFC60A")
    difference() {
        union() {
            translate([-tw_w/2, 0, 0]) cube([tw_w, stand, shelf_h]);          // shelf
            translate([-tw_w/2, slot_y[0]-fin_t, 0]) cube([tw_w, fin_t, tw_h]); // case-side fin
            translate([-tw_w/2, slot_y[1], 0]) cube([tw_w, stand-slot_y[1], tw_h]); // ground fin
            for (sx=[-1,1])                                                    // low tie-walls, both ends
                translate([sx*tw_w/2 - (sx>0?4:0), 0, 0]) cube([4, stand, 10]); // (below the whip's path)
        }
        // 2x M5 through everything, countersunk in the ground face
        for (sx=[-1,1]) translate([sx*7, -1, 4+shelf_h+14]) rotate([-90,0,0]) {
            cylinder(d=m5, h=stand+2);
            translate([0,0,stand-2.3]) cylinder(d1=m5, d2=csk, h=2.31);
            translate([0,0,stand+0.9]) cylinder(d=csk, h=1.2);
        }
        // shallow V rest for the whip on the shelf top
        translate([-tw_w/2-1, bay_y, shelf_h+2]) rotate([0,90,0])
            cylinder(d=whip_d+8, h=tw_w+2);
    }
}

/* ================= whips / context ================= */
module whip_r(deploy) {    // right-side whip; deploy 0 stowed .. 90 vertical-ish
    ang = 90 + stow - deploy;          // 113 (stowed, down-out) .. 23 (deployed, along axis)
    color("#26262A") translate([jdx, bay_y, jz]) {
        rotate([0, 90-ax_deg, 0]) cylinder(d=whip_d+3, h=knuckle);      // barrel+hinge
        translate([knuckle*cos(ax_deg), 0, knuckle*sin(ax_deg)])
            rotate([0, ang, 0]) cylinder(d=whip_d, h=whip_l);
    }
}
module whip(s, deploy) { if (s>0) whip_r(deploy); else mirror([1,0,0]) whip_r(deploy); }
module pelican() {
    color("#C9CCCF") {
        translate([-case_w/2, -22, 0]) cube([case_w, 22, case_h]);
        for (i=[0:6]) translate([-case_w/2+30+i*45, -2, hinge_z-9]) cube([26,11,18]);
    }
}
module kit() { center(); for (s=[-1,1]) translate([s*tw_cx, 0, 0]) tower(); }

if (part=="center")   center();
if (part=="tower")    tower();
if (part=="stowed")   { pelican(); kit(); whip(1,0);  whip(-1,0);  }
if (part=="deployed") { pelican(); kit(); whip(1,90); whip(-1,90); }
if (part=="mid")      { kit(); whip(1,45); whip(-1,45); }
if (part=="center_print") rotate([-90,0,0]) center();   // case face down
if (part=="tower_print")  tower();                       // shelf down as modeled
