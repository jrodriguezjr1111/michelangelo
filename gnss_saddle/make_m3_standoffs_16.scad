// ============================================================================
// CyberWing — M3 standoff columns, 16 mm (×4)
// Spacers between the side frame's 4× M3 inserts (64×40 pattern) and the WAGO
// snap plate. M3 bolt passes clear through each column. Print upright.
// ============================================================================
$fn = 48;

SO_OD = 7;        // column outer diameter
SO_H  = 16;       // length
M3_CLR = 3.4;     // M3 clearance bore
N = 4;            // how many
PITCH = 12;       // spacing on the bed

for (i = [0:N-1])
  translate([i*PITCH, 0, 0])
    difference() {
      cylinder(d=SO_OD, h=SO_H);
      translate([0,0,-0.1]) cylinder(d=M3_CLR, h=SO_H+0.2);
    }
