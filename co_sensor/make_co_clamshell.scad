// ============================================================================
// CyberWing — CO sensor CLAMSHELL CARD CAGE (SPEC 3-board stick)
// The stick is 3 detachable boards on header plugs (CP2102 USB / D-ULPSM AFE /
// SPEC PSCB cell). Vertical-split clamshell: each half-shell carries 3 groove
// tiers; the assembled stack LAYS IN sideways (no sliding stress on the header
// joints), the second half closes over, 2× M3 screws through end lugs.
// Crack it open to swap any single layer (the cell board is the consumable).
//   X = length (cell end x=0, USB +X) ; Y = split at 0 ; Z = up.
// Cell module + membrane face UP through an open ceiling window. Vented cell
// end + floor. Print halves seam-face down (no supports).
// part = "A" (screw-head half) | "B" (pilot half) | "both" (assembled view)
// ============================================================================
$fn = 40;
part = "both";

// ---- measured stack ----
PCB_W = 20.92; PCB_T = 1.6;
GAP1 = 5.80;                // USB board -> AFE (measured)
GAP2 = 4.52;                // AFE -> cell board (derived from 15.12; CONFIRM)
CELL_X = 19.80;             // cell module center from the cell end
MOD_SQ = 15.58;             // black cell module side
PLUG_PROT = 12;             // USB-A metal beyond the board end (std; CONFIRM)
STICK_L = 114.00;           // overall incl. plug

// ---- cage ----
ENG = 1.6; WALL = 2.0; FLOOR = 2.0; TOP = 2.0; END = 2.5;
FLR_GAP = 1.5; SLOT_H = PCB_T + 0.4; CEIL_CLR = 0.6;
WIN = 16.6;                 // ceiling window over the module
USB_W = 15; USB_H = 6;      // end aperture (plug passes, boards can't)
EAR_X = [30, 80]; M3 = 3.4;

// ---- derived ----
b1 = FLR_GAP;                       // USB board bottom
b2 = b1 + PCB_T + GAP1;             // AFE bottom
b3 = b2 + PCB_T + GAP2;             // cell board bottom
IH = b3 + PCB_T + CEIL_CLR;
OH = FLOOR + IH + TOP;
RIBY = PCB_W/2 - ENG;               // rib inner face
GFLR = PCB_W/2 + 0.25;              // groove floor
OW = 2*(GFLR + WALL);
CAV_L = STICK_L - PLUG_PROT + 0.5;  // boards only; plug exits the end wall
OL = END + CAV_L + END;
x_cell = END + 0.25 + CELL_X;
lugs = [[-3.5, OH-6], [OL+3.5, OH-6]];   // [x, z] screw centers, both ends up top

module shell() {
  difference() {
    union() {
      translate([0, -OW/2, 0]) cube([OL, OW, OH]);                      // body
      translate([-7, -6, OH-10]) cube([7, 12, 8]);                      // -X lug
      translate([OL, -6, OH-10]) cube([7, 12, 8]);                      // +X lug
      for (x = EAR_X, sy = [-1,1])                                      // 4 ears
        translate([x-6, sy>0 ? OW/2 : -OW/2-8, 0]) cube([12, 8, 3]);
    }
    translate([END, -RIBY, FLOOR]) cube([CAV_L, 2*RIBY, IH]);           // cavity between ribs
    for (tb = [b1, b2, b3])                                             // 3 groove tiers
      translate([END, -GFLR, FLOOR+tb]) cube([CAV_L, 2*GFLR, SLOT_H]);
    translate([x_cell-WIN/2, -WIN/2, FLOOR+IH-0.1])                     // open cell window
      cube([WIN, WIN, TOP+0.2]);
    translate([OL-END-0.1, -USB_W/2, FLOOR+b1+PCB_T-0.6])               // USB aperture
      cube([END+0.2, USB_W, USB_H]);
    for (vy = [-7, 7])                                                  // outer cell-end vents (full height, beside the lug)
      translate([-0.1, vy-1.25, FLOOR+1]) cube([END+0.2, 2.5, IH-3]);
    for (vy = [-3.5, 3.5])                                              // inner vents stop below the lug — solid wall behind the screw boss
      translate([-0.1, vy-1.25, FLOOR+1]) cube([END+0.2, 2.5, (OH-11)-(FLOOR+1)]);
    for (vx = [14, 20, 26, 32])                                         // floor vents under the cell
      translate([vx, -8, -0.1]) cube([3, 16, FLOOR+0.2]);
    for (x = EAR_X, sy = [-1,1])                                        // ear M3
      translate([x, sy*(OW/2+4), -0.1]) cylinder(d=M3, h=3.2);
    for (p = lugs)                                                      // lug pilots (M3 self-tap in B)
      translate([p[0], -6.1, p[1]]) rotate([-90,0,0]) cylinder(d=2.8, h=12.2);
  }
}

module halfA() {                       // y<0, screw heads
  difference() {
    intersection() { shell(); translate([-60,-60,-5]) cube([OL+120, 60, OH+20]); }
    for (p = lugs) {
      translate([p[0], -6.1, p[1]]) rotate([-90,0,0]) cylinder(d=M3, h=6.2);      // clearance
      translate([p[0], -6.1, p[1]]) rotate([-90,0,0]) cylinder(d=6, h=2.6);       // head cb
    }
  }
}
module halfB() intersection() { shell(); translate([-60,0,-5]) cube([OL+120, 60, OH+20]); }

if (part=="both") { color("SteelBlue") halfA(); color("LightGreen") halfB(); }
if (part=="A") rotate([-90,0,0]) halfA();     // seam-face down for printing
if (part=="B") rotate([90,0,0])  halfB();
