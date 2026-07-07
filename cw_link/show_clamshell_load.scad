// M18 gland — ONE clamshell half (open), with a USB-C cable laid into the channel.
// Shows that the plug never feeds through a bore: you open the halves, lay the
// pre-terminated cable in (plug seats in the inner pocket), then close + nut.
$fn = 72;
color([0.80,0.81,0.85]) import("cwlink_body_half.stl");          // open half
// USB-C cable laid in:
color([0.78,0.79,0.83]) translate([0,0,-16.5]) cube([8.4,3,4.4], center=true); // USB-C tip -> board (into box)
color([0.13,0.13,0.16]) translate([0,0,-8])    cylinder(d=10.5, h=10, center=true); // overmold in Ø11 pocket
color([0.86,0.5,0.24])  translate([0,0,-3])    cylinder(d=4.5, h=34);               // jacket out the snout
