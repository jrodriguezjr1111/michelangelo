// ============================================================================
// CW-Link — USB-C bulkhead cable gland  (OpenSCAD, self-contained)
// ----------------------------------------------------------------------------
// Panel-mount feedthrough for a PRE-TERMINATED USB-C cable. The body splits on
// its axis (clamshell) so the cable lays in — the molded plug never passes the
// bore. A knurled compression nut squeezes the halves and clamps the panel.
// Modern/robust language: hex flange, coarse threaded barrel, ribbed strain-
// relief snout, O-ring seal groove. Threads are made by twist-extrude (no libs).
//
//   Z = cable axis.  +Z = outside the box (snout, cable to device).
//   z=0 = wall outer face (hex flange seats here, O-ring groove underneath).
//   -Z  = into the box (threaded barrel through wall; nut + plug pocket).
//
// Render one part for STL:   openscad -D part=\"body\" -o cwlink_body.stl ...
//   part = "body" | "half" | "nut" | "all"
// ============================================================================

part = "all";
with_pin = true;            // set false for a clean split-face-down print (nut retains the halves)
$fn = 96;

// ---- cable / plug ----------------------------------------------------------
jacket_d  = 5.0;     // USB-C cable jacket Ø (channel grips just under this)
pocket_d  = 11.0;    // molded plug overmold Ø (seats inside, pull-out stop)
pocket_h  = 10.0;

// ---- barrel + coarse thread ------------------------------------------------
thread_major = 18.0;
pitch        = 3.2;
depth        = 1.2;
barrel_l     = 13.0;

// ---- hex flange (modern faceted, chamfered top) ----------------------------
flange_af = 28.0;                       // across flats
flange_r  = flange_af/2/cos(30);        // circumradius
flange_t  = 6.0;
flange_ch = 1.6;

// ---- ribbed strain-relief snout --------------------------------------------
snout_l  = 12.0;
snout_r0 = 6.6;
snout_r1 = 4.0;
snout_ribs = 3;

// ---- O-ring seal groove (flange underside, against the wall) ---------------
oring_mean = 21.0;
oring_w    = 1.8;

// ---- compression / panel nut -----------------------------------------------
nut_h     = 11.0;
nut_r     = 14.5;    // knurl outer radius
nut_lip   = 1.8;     // bears on the wall inner face
knurl_n   = 26;
knurl_d   = 1.9;

wall_hole = thread_major + 0.4;   // documentation

// ============================================================================
module torus(R, r) rotate_extrude(convexity=4) translate([R,0]) circle(r=r);

// Coarse external thread ridge (twist-extrude), unioned with its core.
module ext_thread(major, pitch, length, dep) {
    core_r = major/2 - dep;
    turns  = length/pitch;
    th     = pitch*0.62;            // tangential tooth width -> ~trapezoid flanks
    union() {
        cylinder(r=core_r+0.05, h=length);
        linear_extrude(height=length, twist=-360*turns,
                       slices=max(60, ceil(turns*48)), convexity=10)
            polygon([[core_r,      -th/2],
                     [core_r+dep,  -th/4],
                     [core_r+dep,   th/4],
                     [core_r,       th/2]]);
    }
}

module hex_flange() {
    h0 = flange_t - flange_ch;
    union() {
        linear_extrude(h0) circle(r=flange_r, $fn=6);
        translate([0,0,h0])
            linear_extrude(flange_ch, scale=(flange_af-2*flange_ch)/flange_af)
                circle(r=flange_r, $fn=6);
    }
}

module snout() {
    difference() {
        translate([0,0,flange_t]) cylinder(r1=snout_r0, r2=snout_r1, h=snout_l);
        for (i=[0:snout_ribs-1]) {
            zf = flange_t + snout_l*(i+0.7)/(snout_ribs+0.4);
            rr = snout_r0 + (snout_r1-snout_r0)*(zf-flange_t)/snout_l;
            translate([0,0,zf]) torus(rr, 0.8);
        }
    }
}

module body() {
    top = flange_t + snout_l;
    difference() {
        union() {
            hex_flange();
            mirror([0,0,1]) ext_thread(thread_major, pitch, barrel_l, depth);  // barrel z 0..-barrel_l
            snout();
            // grip ribs that bite the jacket (inside the channel)
            for (zf=[-2.0,-7.0]) translate([0,0,zf]) torus(jacket_d/2+0.3, 0.45);
        }
        // one straight jacket channel through everything
        translate([0,0,-barrel_l-1]) cylinder(r=jacket_d/2, h=barrel_l+top+2);
        // molded-plug pocket at the inside end
        translate([0,0,-barrel_l-0.01]) cylinder(r=pocket_d/2, h=pocket_h);
        // O-ring seal groove on the flange underside
        torus(oring_mean/2, oring_w/2);
    }
}

module body_half() {
    zc = flange_t/2;
    difference() {
        union() {
            intersection() {                                  // keep x >= 0
                body();
                translate([0,-200,-200]) cube([200,400,400]);
            }
            if (with_pin) translate([0,7.5,zc]) rotate([0,-90,0]) cylinder(r=1.2, h=2.2);  // pin (+Y)
        }
        if (with_pin) translate([0.01,-7.5,zc]) rotate([0,-90,0]) cylinder(r=1.45, h=2.4); // socket (-Y)
    }
}

module nut() {
    difference() {
        union() {
            cylinder(r=nut_r, h=nut_h);
            translate([0,0,nut_h]) cylinder(r=nut_r+nut_lip, h=nut_lip);     // wall-bearing lip
        }
        for (k=[0:knurl_n-1])                                                 // knurl flutes
            rotate([0,0,360*k/knurl_n]) translate([nut_r,0,-0.5])
                cylinder(r=knurl_d/2, h=nut_h+1);
        translate([0,0,-0.5]) cylinder(r=thread_major/2+0.2, h=nut_h+nut_lip+1);   // bore
        ext_thread(thread_major+0.45, pitch, nut_h+nut_lip+0.5, depth);            // female thread
        translate([0,0,nut_h+nut_lip-0.4]) cylinder(r1=thread_major/2-0.2, r2=thread_major/2+1.4, h=1.6); // lead-in
    }
}

// ---- output ----------------------------------------------------------------
if (part=="body")      body();
else if (part=="half") body_half();
else if (part=="halfprint") rotate([0,-90,0]) body_half();   // split-face on the bed
else if (part=="nut")  nut();
else {                                   // "all" — exploded, for the hero render
    body();
    color("silver") translate([0,0,-barrel_l-9]) nut();
    color("orange") translate([0,0,-barrel_l-4]) cylinder(r=jacket_d/2-0.2, h=barrel_l+flange_t+snout_l+18);
}
