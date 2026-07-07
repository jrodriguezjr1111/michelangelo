// Tube-clearance check for the shifted RSD plate (concept, not for print)
// Stack coords: X = out from the +X face; Y = across; Z = up.
$fn = 40;

GY = 20.27;  ZN = 7;  ZO = 61;        // +X inserts: Y=±20.27, Z=7 (Nano) & 61 (Orin)
SO_D = 7.8;  SO_L = 14;               // standoffs Ø7.8 × 14
RSD_Y = 120.18; RSD_Z = 51.83; RSD_CLR = 4.5;
PT = 5; SHIFT = 10;
PZc = (ZN + ZO)/2 + SHIFT;            // plate center Z = 44
PZ0 = PZc - 28; PZ1 = PZc + 28;       // plate Z 16..72
PX  = SO_L;                           // plate inner face at X=14

// --- GNSS tubes (run along +X at Y=±30.085, Z=0) ---
color([0.55,0.42,0.62,0.5])
for (sy=[-1,1]) translate([-25, sy*30.085, 0]) rotate([0,90,0]) cylinder(d=15.39, h=95);

// --- proposed part ---
color([0.30,0.50,0.72,0.95]) {
  // 4 standoffs to the grid
  for (sy=[-1,1], z=[ZN,ZO]) translate([0, sy*GY, z]) rotate([0,90,0]) cylinder(d=SO_D, h=SO_L);
  // RSD plate (shifted up)
  translate([PX, -66, PZ0]) cube([PT, 132, PZ1-PZ0]);
  // lower arms from plate down to the lower standoffs
  for (sy=[-1,1]) translate([PX, sy*GY-5, ZN]) cube([PT, 10, PZ0-ZN]);
}
