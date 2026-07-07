// =============================================================
//  CW-AEP-002c — WiFi Antenna Roll-Bar, Pelican 1400 (OUTWARD DEPLOY)
//  QIDI X-Plus 4 + PLA. Self-contained.
// -------------------------------------------------------------
//  Deploy geometry (fixes the swing-collision):
//   The whips fold OUTWARD toward opposite ends and swing up OVER
//   the ends. Because they fold to opposite ends they never overlap
//   and never cross the center, so:
//     - the CENTER SPLICE is fully solid (no whip channel) -> strong
//     - the whip swing sweeps only the OUTER top-rail zones, which are
//       removed; the top rail survives as a center segment + the pylons
//     - the bottom rail and shear web are never swept (whip is in front
//       of the web, and only swings UP) -> both stay full length
//   The stowed whips pass through a channel in each pylon and overhang
//   the case ends by ~35 mm (behind the stance plane, above the ground).
//
//  PRINT: PLA, 0.20, >=4 walls, ~35% infill, BED 60 C, 5 mm brim,
//         one half at a time, standing on the pylon face (no supports).
//  part = "frame"|"A"|"B"|"A_print"|"B_print"|"stowed"|"deployed"|"mid"
// =============================================================

$fn = $preview ? 40 : 72;
part = "deployed";

/* ================= PARAMETERS ================= */
// case interface (measured)
case_w      = 340;  case_h = 152;
hinge_clear = 22;   hinge_z = 42;         // knuckle 21.26 + margin ; parting line
rib_relief  = [128.6];  rib_w = 13;  rib_d = 8;   // outer ribs |x| from center

// frame envelope
frame_l  = 302;  frame_h = 84;
stand_h  = 46;   rail_t = 11;  rail_d = 20;  web_t = 4;
pylon_w  = 40;   corner_r = 6;

// antenna: cylindrical fold-over whip (measured)
whip_d = 13.10;  whip_l = 159;  knuckle = 20;  sma_hole = 6.5;
bay_z  = 26;                                   // both whips here (base half, no stagger)
bay_y  = (hinge_clear + stand_h)/2;            // whip depth = 34, in front of the web

// deploy positions (fold outward): pivots inboard, ~54 mm apart
pivA = 124;  pivB = frame_l - pivA;            // 124, 178
seg0 = pivA + 4;  seg1 = pivB - 4;             // center top-rail segment 128..174

// fastening
mnt_hole_d = 5.4;  csk_d = 10.4;
splice_t = 4;  m3 = 3.4;  drain_d = 4;
ch_h = whip_d + 4;                             // whip channel height in the pylons
/* ============================================== */

xc = frame_l/2;

module rrbox(size, r=4) {                       // rounded in X-Z, depth along Y
    translate([0,size[1],0]) rotate([90,0,0]) linear_extrude(size[1])
        hull() for (x=[r,size[0]-r], z=[r,size[2]-r]) translate([x,z]) circle(r=r);
}

module cradle(px) {                             // C-clip, whip snaps in, opens +Z
    difference() {
        union() {
            translate([px-5, hinge_clear, bay_z-whip_d/2-6]) cube([10, bay_y-hinge_clear, 6]);
            translate([px, bay_y, bay_z]) rotate([0,90,0]) cylinder(d=whip_d+7, h=10, center=true);
        }
        translate([px, bay_y, bay_z]) rotate([0,90,0]) cylinder(d=whip_d+0.6, h=10.4, center=true);
        translate([px-5.2, bay_y-whip_d/2, bay_z+0.8]) cube([10.4, whip_d, whip_d]);
    }
}

module frame() {
    color("#FFC60A")
    difference() {
        union() {
            for (x0=[0, frame_l-pylon_w])                       // end pylons
                translate([x0,0,0]) rrbox([pylon_w, stand_h, frame_h], corner_r);
            translate([0, stand_h-rail_d, 0])                   // bottom rail (full)
                rrbox([frame_l, rail_d, rail_t], 4);
            translate([seg0, stand_h-rail_d, frame_h-rail_t])   // top rail: CENTER SEGMENT only
                rrbox([seg1-seg0, rail_d, rail_t], 4);
            translate([0, hinge_clear, 0])                      // shear web (full)
                rrbox([frame_l, web_t, frame_h], corner_r);
            for (px=[pivA, pivB])                               // jack blocks at the pivots
                translate([px-6, hinge_clear, bay_z-14]) cube([12, stand_h-hinge_clear, 28]);
            cradle(pivA-40); cradle(pivA-84);                   // stow cradles (fold -X)
            cradle(pivB+40); cradle(pivB+84);                   //             (fold +X)
        }
        // whip pass-through channels through the pylons (folded whips exit the ends)
        for (x0=[-1, frame_l-pylon_w-1])
            translate([x0, hinge_clear-1, bay_z-ch_h/2]) cube([pylon_w+2, stand_h-hinge_clear+1, ch_h]);
        // SMA jack holes (inboard face of each jack block)
        translate([pivA-8, bay_y, bay_z]) rotate([0,90,0]) cylinder(d=sma_hole, h=16);
        translate([pivB+8, bay_y, bay_z]) rotate([0,-90,0]) cylinder(d=sma_hole, h=16);
        // coax bores toward the case face
        for (px=[pivA, pivB]) translate([px,-1,bay_z]) rotate([-90,0,0]) cylinder(d=8, h=hinge_clear+6);
        // pylon mounts: 2x M5 per pylon, side-by-side, LOW on the base half (clear of channel)
        for (x0=[pylon_w/2-10, pylon_w/2+10, frame_l-pylon_w/2-10, frame_l-pylon_w/2+10])
            translate([x0,-1,12]) rotate([-90,0,0]) {
                cylinder(d=mnt_hole_d, h=stand_h+2);
                translate([0,0,stand_h-2.3]) cylinder(d1=mnt_hole_d, d2=csk_d, h=2.31);
                translate([0,0,stand_h+0.9]) cylinder(d=csk_d, h=1.2);
            }
        // rib relief in the pylon case-faces
        for (s=[-1,1], rx=rib_relief) {
            gx = xc + s*rx;
            if (gx < pylon_w+2 || gx > frame_l-pylon_w-2)
                translate([gx-rib_w/2,-0.1,-1]) cube([rib_w, rib_d, frame_h+2]);
        }
        for (dx=[0.15,0.35,0.65,0.85])                          // drains in the bottom rail
            translate([frame_l*dx, stand_h-rail_d/2,-1]) cylinder(d=drain_d, h=rail_t+2);
    }
}

// solid center splice (no whip channel — whips never reach center)
module splice(side) {
    x0 = side>0 ? xc : xc-splice_t;
    difference() {
        translate([x0, hinge_clear, 0]) cube([splice_t, stand_h-hinge_clear, frame_h]);
        for (z=[6, hinge_z, frame_h-6])                         // 3x M3 through solid bands
            translate([x0-0.1, bay_y, z]) rotate([0,90,0]) cylinder(d=m3, h=splice_t+0.2);
    }
}
module halfA() {
    intersection() { frame(); translate([-60,-5,-5]) cube([60+xc, stand_h+10, frame_h+10]); }
    color("#FFC60A") splice(-1);
    color("#FFC60A") translate([xc-splice_t, bay_y-8, hinge_z-8]) cube([splice_t+3,16,16]);   // tab
}
module halfB() {
    difference() {
        union() {
            intersection() { frame(); translate([xc,-5,-5]) cube([frame_l-xc+60, stand_h+10, frame_h+10]); }
            color("#FFC60A") splice(1);
        }
        translate([xc-splice_t-0.2, bay_y-8.2, hinge_z-8.2]) cube([splice_t+3.4,16.4,16.4]);  // pocket
    }
}

// whip: dir -1 folds -X, +1 folds +X ; deploy 0 stowed, 90 vertical
module whip(deploy, dir) {
    ang = -dir*(90-deploy);
    color("#26262A") {
        rotate([0, dir>0?-90:90, 0]) cylinder(d=whip_d+3, h=knuckle-4);
        translate([-dir*(knuckle-4),0,0]) sphere(d=whip_d+3.5);
        translate([-dir*(knuckle-2),0,0]) rotate([0,ang,0]) cylinder(d=whip_d, h=whip_l);
    }
}
module whips(deploy) {
    translate([pivA, bay_y, bay_z]) whip(deploy, -1);
    translate([pivB, bay_y, bay_z]) whip(deploy,  1);
}

module pelican() {
    color("#C9CCCF") {
        translate([-(case_w-frame_l)/2,-22,-(case_h-frame_h)/2]) cube([case_w,22,case_h]);
        for (i=[0:6]) translate([-(case_w-frame_l)/2+30+i*45,-2,hinge_z-9]) cube([26,11,18]);
    }
}

if (part=="frame")    frame();
if (part=="A")        halfA();
if (part=="B")        halfB();
if (part=="stowed")   { pelican(); frame(); whips(0); }
if (part=="deployed") { pelican(); frame(); whips(90); }
if (part=="mid")      { frame(); whips(35); }
if (part=="A_print")  rotate([0,-90,0]) halfA();
if (part=="B_print")  translate([frame_l,0,0]) rotate([0,90,0]) halfB();
