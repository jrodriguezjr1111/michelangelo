// ============================================================================
// CW-Link — single-cable CLAMSHELL gland  (OpenSCAD, self-contained)
// ----------------------------------------------------------------------------
// Passes ONE pre-terminated cable through a round box port without feeding the
// plug through. Two IDENTICAL halves (print x2): lay the cable in, close them,
// and the circumferential GROOVE drops into the wall port — the panel rim sits
// in the groove, capturing the wall between the outer flange and inner lip. A
// pin/socket on the split keeps the halves together. No nut, no thread.
//
//   Z = cable axis (through the wall).  z=0 = wall OUTER face, +Z = outside.
//   part = "half" (printable, x2) | "body" (both halves merged) | "demo" (in a wall)
// ============================================================================

part = "demo";
$fn  = 80;

// ---- fit these to your box + cable ----------------------------------------
port_d   = 20.0;     // round wall port Ø (Jetson right-wall port; 18.4 = gland bore)
wall_t   = 3.0;      // box wall thickness (CW-MES = 3)
cable_d  = 5.0;      // single cable jacket Ø (grips ~0.5 under)

// ---- styling (derived) -----------------------------------------------------
neck_d   = port_d - 0.4;        // sits in the port hole
oflange_d = port_d + 9;         // outer stop flange
iflange_d = port_d + 5;         // inner retaining lip
flange_t = 3.0;
snout_l  = 9.0;                 // outside strain-relief snout
snout_r1 = cable_d/2 + 2.0;     // snout tip radius
groove_w = wall_t + 0.4;        // wall seats here (slip fit)
eps = 0.02;

module torus(R, r) rotate_extrude(convexity=4) translate([R,0]) circle(r=r);

// full (both halves merged), cable channel + grips, captures the wall in a groove
module body() {
  difference() {
    union() {
      translate([0,0,-wall_t])        cylinder(d=neck_d, h=wall_t);          // neck (in port)
      translate([0,0,0])              cylinder(d=oflange_d, h=flange_t);      // outer flange
      translate([0,0,-wall_t-flange_t]) cylinder(d=iflange_d, h=flange_t);   // inner lip
      translate([0,0,flange_t-eps])                                          // ribbed snout
        cylinder(d1=oflange_d*0.62, d2=2*snout_r1, h=snout_l);
    }
    // cable channel through everything
    translate([0,0,-wall_t-flange_t-2]) cylinder(d=cable_d, h=wall_t+2*flange_t+snout_l+6);
    // boot grooves on the snout
    for (z=[flange_t+3, flange_t+6]) translate([0,0,z]) torus(snout_r1+1.2, 0.7);
  }
  // grip ribs that bite the jacket
  for (z=[-wall_t/2, -wall_t-flange_t+1.2]) translate([0,0,z]) torus(cable_d/2, 0.5);
}

// one printable half: split on x=0 + identical-mating pin(+Y)/socket(-Y)
module half() {
  zc = -wall_t/2;
  difference() {
    union() {
      intersection() { body(); translate([0,-60,-60]) cube([60,120,120]); }   // keep x>=0
      translate([0, oflange_d/2-3, zc]) rotate([0,-90,0]) cylinder(d=2.4, h=2.4); // pin +Y
    }
    translate([eps, -(oflange_d/2-3), zc]) rotate([0,-90,0]) cylinder(d=2.7, h=2.7); // socket -Y
  }
}

// ---- output ----------------------------------------------------------------
if (part == "half") half();
else if (part == "body") body();
else {                                            // demo: gland + wall + cable
  color([0.55,0.6,0.7,0.35])                                                 // box wall slab
    translate([-30,-30,-wall_t]) difference() {
      cube([60,60,wall_t]);
      translate([30,30,-1]) cylinder(d=port_d, h=wall_t+2);
    }
  color([0.82,0.45,0.2]) cylinder(d=cable_d-0.3, h=80, center=true);          // cable
  color([0.20,0.55,0.85]) body();                                            // gland (closed)
}
