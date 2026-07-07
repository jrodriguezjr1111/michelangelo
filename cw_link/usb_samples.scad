// ============================================================================
// CW-Link — USB connector SAMPLES  (USB-A / USB-C / micro-USB)
// ----------------------------------------------------------------------------
// Dimensionally-representative plug mock-ups for (a) checking that a cable end
// clears a box cable port / gland, and (b) printing as a physical go/no-go gauge
// you push through the printed hole. Plug axis = +Y (insertion tip), cable = -Y.
//
//   kind = "A" | "C" | "micro" | "all"
//   Each spec: name, shell[w, l, h], overmold[w, l, h], cable_d
//   (shell = metal connector; overmold = molded grip; the overmold is the widest
//    part, so its diagonal is what must clear a round port.)
// ============================================================================

kind = "all";
$fn  = 56;

specs = [
  ["USB-A",     [12.0, 12.0, 4.50], [17.0, 22, 10.0], 4.5],
  ["USB-C",     [ 8.34, 6.5, 2.56], [11.0, 20,  6.8], 4.0],
  ["micro-USB", [ 6.85, 7.5, 1.80], [10.0, 17,  7.0], 3.5],
];

// reference ports in this project (for the echo'd fit check)
port_jetson = 20.0;     // Jetson right-wall round cable port Ø
gland_chan  = 5.0;      // CW-Link gland cable channel Ø (jacket only)

module rbox(d, r=1.6)                       // rounded box, total size = d
  minkowski() { cube([d[0]-2*r, d[1]-2*r, d[2]-2*r], center=true); sphere(r); }

module plug(s) {
  shell = s[1]; mold = s[2]; cd = s[3];
  color([0.14,0.14,0.17]) rbox(mold);                                   // overmold grip
  color([0.78,0.79,0.83])                                               // metal shell tip
    translate([0, mold[1]/2 + shell[1]/2 - 0.8, 0])
      cube([shell[0], shell[1], shell[2]], center=true);
  color([0.20,0.32,0.55])                                               // insert tongue
    translate([0, mold[1]/2 + shell[1]/2 - 0.8, 0])
      cube([shell[0]-2.4, shell[1]+0.6, max(shell[2]-2.2,0.8)], center=true);
  color([0.17,0.17,0.20])                                               // cable stub
    translate([0, -mold[1]/2, 0]) rotate([90,0,0]) cylinder(d=cd, h=20);
}

// ---- output ----------------------------------------------------------------
for (s = specs) {
  diag = sqrt(s[2][0]*s[2][0] + s[2][2]*s[2][2]);
  echo(str(s[0], ": overmold ", s[2][0], "x", s[2][2],
           "  diag=", diag, " mm  -> Jetson Ø", port_jetson,
           diag < port_jetson ? "  PASS" : "  TOO BIG",
           "  | jacket Ø", s[3], " vs gland Ø", gland_chan,
           s[3] <= gland_chan ? " OK" : " (gland too small)"));
}

if      (kind == "A")     plug(specs[0]);
else if (kind == "C")     plug(specs[1]);
else if (kind == "micro") plug(specs[2]);
else                                            // "all" — laid out along X
  for (i = [0:len(specs)-1])
    translate([(i-1)*26, 0, specs[i][2][2]/2]) plug(specs[i]);
