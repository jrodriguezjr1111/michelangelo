// ============================================================================
// CyberWing — RSD plate standing on its long edge over the SlimRig
// The RSD plate is VERTICAL (sits on its side). Its bottom long edge carries a
// 3-sided "staple" (⊓) that straddles the SlimRig running underneath: the bridge
// rests on the rig's top, two legs wrap the 15.02 thickness and bolt through the
// rig's side threads (2× 1/4"-20 per leg). The plate carries the RSD on the
// standard 120.18 × 51.83 / #8-32 pattern.
//   Modeled in PRINT = USE orientation: legs sit on the bed (Z=0), plate rises up.
//   X = SlimRig width / plate length (63.94 rig, 132 plate) ; Y = rig thickness
//   wrapped by the legs ; Z = up.
// show_rig=true overlays the SlimRig for a fit check.
// ============================================================================
$fn = 64;
show_rig = false;

// ---- SlimRig (measured) ----
RIG_W = 63.94;      // width along the plate length (X)
RIG_T = 15.02;      // thickness the legs wrap over  (Y)
WRAP_CLR = 0.4;     // clearance around the rig
GAP = RIG_T + WRAP_CLR;

// ---- staple ----
WALL = 5;           // leg wall thickness (holds the 1/4"-20)
LEG_H = 20;         // grip depth down the rig sides (Z)
BRIDGE_T = 5;       // bridge thickness over the rig top

// ---- side holes: 2× 1/4"-20 per leg (DEFAULTS — confirm against the rig) ----
Q_CLR   = 6.9;      // 1/4" (6.35) clearance
SIDE_SP = 36.25;    // spacing along the width (±18.125) — measured
SIDE_Z  = 5.10;     // hole centerline, up from the leg bottom — measured

// ---- RSD plate (vertical) ----
PLATE_X = 132;      // plate length (X)
PLATE_T = 5;        // plate thickness (Y)
RSD_PX = 120.18; RSD_PZ = 51.83; RSD_CLR = 4.5;   // #8-32 clearance
CB_D = 9; CB_H = 4;                                // head counterbore
BOT_CLR = 12;       // clearance: bridge top -> lower hole centerline
TOP_MARGIN = 8;     // material above the top hole

// ---- back-face gusset ribs (brace the tall wall) ----
GUSSET_W = 6; GUSSET_H = 40; GUSSET_X = [-50,-25,0,25,50];

LEGY  = GAP/2 + WALL/2;                 // leg centerline (Y)
OUTY  = GAP/2 + WALL;                   // staple outer half-width (Y)
BR_TOP = LEG_H + BRIDGE_T;              // bridge top (Z)
RSD_Zlo = BR_TOP + BOT_CLR;            // lower RSD hole centerline (Z)
RSD_Zc  = RSD_Zlo + RSD_PZ/2;          // RSD pattern center (Z)
PLATE_H = (RSD_Zlo + RSD_PZ + TOP_MARGIN) - LEG_H;  // plate height above the legs
WTOP    = LEG_H + PLATE_H;              // plate top (Z)

difference() {
  union() {
    // two clamp legs (full plate length so the wall is fully supported)
    for (sy = [-1,1])
      translate([-PLATE_X/2, sy*LEGY - WALL/2, 0]) cube([PLATE_X, WALL, LEG_H]);
    // bridge across the rig top
    translate([-PLATE_X/2, -OUTY, LEG_H]) cube([PLATE_X, 2*OUTY, BRIDGE_T]);
    // vertical RSD plate (centered on the bridge, rising up)
    translate([-PLATE_X/2, -PLATE_T/2, LEG_H]) cube([PLATE_X, PLATE_T, PLATE_H]);
  }

  // RSD mount holes + head counterbore (on the +Y face)
  for (sx = [-1,1], sz = [-1,1]) {
    translate([sx*RSD_PX/2, PLATE_T/2+0.1, RSD_Zc + sz*RSD_PZ/2])
      rotate([90,0,0]) cylinder(d=RSD_CLR, h=PLATE_T+0.2);
    translate([sx*RSD_PX/2, PLATE_T/2+0.1, RSD_Zc + sz*RSD_PZ/2])
      rotate([90,0,0]) cylinder(d=CB_D, h=CB_H);
  }

  // 1/4"-20 side holes through both legs into the rig's side threads
  for (sx = [-1,1])
    translate([sx*SIDE_SP/2, 0, SIDE_Z])
      rotate([90,0,0]) cylinder(d=Q_CLR, h=2*OUTY+2, center=true);
}

// ---- gusset ribs up the back (+Y) face, between the RSD holes ----
module gusset(xc)
  hull() {
    translate([xc-GUSSET_W/2, PLATE_T/2-0.1, BR_TOP-0.1])
      cube([GUSSET_W, OUTY-PLATE_T/2+0.1, 0.1]);                 // base: full depth to bridge edge
    translate([xc-GUSSET_W/2, PLATE_T/2-0.1, BR_TOP-0.1+GUSSET_H])
      cube([GUSSET_W, 0.1, 0.1]);                                // apex at the plate face
  }
for (gx = GUSSET_X) gusset(gx);

// ---- SlimRig overlay (fit check) ----
if (show_rig)
  color([0.55,0.42,0.62,0.4])
    translate([-RIG_W/2, -RIG_T/2, -6]) cube([RIG_W, RIG_T, LEG_H+6]);
