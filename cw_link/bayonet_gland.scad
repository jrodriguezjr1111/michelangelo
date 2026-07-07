// ============================================================================
// CW-Link — BAYONET cable gland  (no printed threads, no extra hardware)
// ----------------------------------------------------------------------------
// Clamshell body (2 halves) with 2 radial LUGS near the inner end. A knurled
// COLLAR slides on from inside (lugs enter its axial slots) and quarter-turns:
// the lugs seat in the circumferential lock, clamping the wall between the
// outer flange and the collar — and the collar holds the two halves together.
// Robust, reusable, all-coarse features that print cleanly.
//
//   Z = cable axis.  z=0 = wall OUTER face, +Z out, -Z into the box.
//   part = "demo" | "half" (printable x2) | "collar" | "body"
// ============================================================================

part = "demo";
$fn  = 80;

// fit to box + cable
port_d  = 20.0;        // round wall port Ø (18.4 / 12 etc.)
wall_t  = 3.0;
cable_d = 5.0;

// derived / styling
neck_d   = port_d - 0.4;
flange_d = port_d + 9;
flange_t = 3.0;
snout_l  = 9.0;
snout_r1 = cable_d/2 + 2.0;
barrel_l = wall_t + 10;              // through wall + collar zone (13)
lug_d    = 3.6;  lug_h = 2.4;        // bayonet pins
collar_len = 9.0;  axial_len = 4.5;  twist = 55;
lug_z    = -wall_t - collar_len + axial_len;   // -7.5 : seats at the lock when collar is home
collar_id = neck_d + 0.8;
collar_od = port_d + 8;
with_pin = false;                    // light align pin (off = clean split-face print)
eps = 0.02;

module torus(R, r) rotate_extrude(convexity=4) translate([R,0]) circle(r=r);

module lugs()
  for (a = [0, 180]) rotate([0,0,a])
    translate([neck_d/2 - 0.4, 0, lug_z]) rotate([0,90,0]) cylinder(d=lug_d, h=lug_h+0.4);

module body() {
  difference() {
    union() {
      translate([0,0,-barrel_l]) cylinder(d=neck_d, h=barrel_l);                    // barrel
      cylinder(d=flange_d, h=flange_t);                                             // outer flange
      translate([0,0,flange_t-eps]) cylinder(d1=flange_d*0.6, d2=2*snout_r1, h=snout_l); // snout
      lugs();
    }
    translate([0,0,-barrel_l-2]) cylinder(d=cable_d, h=barrel_l+flange_t+snout_l+6);// cable channel
    for (z=[flange_t+3, flange_t+6]) translate([0,0,z]) torus(snout_r1+1.2, 0.7);   // boot grooves
  }
  for (z=[-3,-9]) translate([0,0,z]) torus(cable_d/2, 0.5);                          // grip ribs
}

module half() {
  difference() {
    union() {
      intersection() { body(); translate([0,-60,-60]) cube([60,120,120]); }         // keep x>=0
      if (with_pin) translate([0, flange_d/2-3, -wall_t/2]) rotate([0,-90,0]) cylinder(d=2.2, h=2.2);
    }
    if (with_pin) translate([eps, -(flange_d/2-3), -wall_t/2]) rotate([0,-90,0]) cylinder(d=2.5, h=2.4);
  }
}

module collar() {
  difference() {
    cylinder(d=collar_od, h=collar_len);
    translate([0,0,-eps]) cylinder(d=collar_id, h=collar_len+2*eps);                 // bore
    for (a = [0, 180]) rotate([0,0,a]) {
      translate([collar_id/2-0.4, -(lug_d+0.8)/2, -eps]) cube([collar_od, lug_d+0.8, axial_len+eps]); // axial entry
      rotate_extrude(angle=twist) translate([collar_id/2-0.4, axial_len-(lug_d+0.8)/2])
        square([collar_od/2, lug_d+0.8]);                                            // circumferential lock
    }
    for (k = [0:23]) rotate([0,0,360*k/24]) translate([collar_od/2,0,-0.5]) cylinder(d=1.6, h=collar_len+1); // knurl
  }
}

module wall()
  color([0.55,0.6,0.7,0.35]) translate([-30,-30,-wall_t])
    difference() { cube([60,60,wall_t]); translate([30,30,-1]) cylinder(d=port_d, h=wall_t+2); }

// ---- output ----------------------------------------------------------------
if (part=="half")        rotate([0,-90,0]) half();        // split-face on the bed
else if (part=="collar") collar();
else if (part=="body")   body();
else {                                                    // demo: locked in a wall, cable through
  wall();
  color([0.82,0.46,0.22]) cylinder(d=cable_d-0.3, h=82, center=true);
  color([0.20,0.55,0.85]) body();
  color([0.62,0.64,0.68]) translate([0,0,-wall_t-collar_len]) collar();
}
