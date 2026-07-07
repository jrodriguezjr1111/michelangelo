// ============================================================================
// CyberWing — CO sensor enclosure, 3-TIER CARD CAGE (SPEC USB stick)
// The rigid 3-board stack (USB-UART / AFE / SPEC cell) slides in axially; each
// board edge rides a groove on the long walls. The CO cell is internal (faces
// up into the 5.80 mm gap, fed by the 5.09 mm port in the middle board), so the
// cell (-X) end stays OPEN for airflow — nothing is ever put through the port.
//   X = length (cell -X open, USB +X stop) ; Y = width ; Z = up (tiers).
// part = base | both. Print floor-down (grooves bridge ~ENG, no supports).
// ============================================================================
$fn = 32;
part = "both";

// ---- measured ----
PCB_L = 114.00; PCB_W = 20.92; PCB_T = 1.6;
GAP1 = 5.80;                 // cell board -> middle board (measured)
GAP2 = 4.52;                 // middle -> top (derived from 15.12 total; CONFIRM)
CLR  = 0.4;                  // slot clearance

// ---- cage ----
ENG = 1.6; BACK = 1.5; FLOOR = 2.0; END_WALL = 2.5; FLR_GAP = 1.5;
USB_W = 14;                  // top notch in the +X stop wall for the USB plug
VENT_W = 3; VENT_PITCH = 6;  // floor slots under the cell
EAR_X = [35, 92]; M3 = 3.4;

// ---- derived tiers (board bottoms, from floor top) ----
b1 = FLR_GAP;
b2 = b1 + PCB_T + GAP1;
b3 = b2 + PCB_T + GAP2;
tiers = [b1, b2, b3];
stack_top = b3 + PCB_T;

RIBY = PCB_W/2 - ENG;        // rib inner face (Y)
GFLR = PCB_W/2 + CLR/2;      // groove floor (Y)
ox = 2*(GFLR + BACK);        // outer width
cavlen = PCB_L + 0.5;        // cavity length (-X open)
Llen = cavlen + END_WALL;
oz = FLOOR + stack_top + 0.5;
SLOT_H = PCB_T + CLR;

module wall(sy) {
  difference() {
    translate([0, sy>0 ? RIBY : -(GFLR+BACK), FLOOR]) cube([Llen, GFLR+BACK-RIBY, oz-FLOOR]);
    for (tb = tiers)                                            // 3 grooves, open at -X
      translate([-0.1, sy>0 ? RIBY-0.1 : -(GFLR+0.1), FLOOR+tb])
        cube([cavlen+0.1, GFLR-RIBY+0.2, SLOT_H]);
  }
}

module base() {
  // floor with cell vents
  difference() {
    translate([0, -ox/2, 0]) cube([Llen, ox, FLOOR]);
    for (x = [10 : VENT_PITCH : 34])
      translate([x, -(PCB_W/2-3), -0.1]) cube([VENT_W, PCB_W-6, FLOOR+0.2]);
  }
  // two grooved side walls
  wall(1); wall(-1);
  // +X stop wall with a top notch for the USB plug
  difference() {
    translate([cavlen, -ox/2, 0]) cube([END_WALL, ox, oz]);
    translate([cavlen-0.1, -USB_W/2, FLOOR+b3-1.5]) cube([END_WALL+0.2, USB_W, oz]);
  }
  // mounting ears (both long sides, 2 per side)
  for (x = EAR_X, sy = [-1, 1])
    difference() {
      translate([x-6, sy>0 ? ox/2 : -ox/2-8, 0]) cube([12, 8, 3]);
      translate([x, sy*(ox/2+4), -0.1]) cylinder(d=M3, h=4);
    }
}

base();
