// ============================================================================
// CyberWing — Jetson stack REDESIGN concept (placement / framework only)
//   Nano frame (bottom) + 40mm 8-32 standoffs + Orin frame (top)
//   + RSD flange on a LONG (±X) side spanning both frames
//   + component-plate frames on each SHORT (±Y) side (relay / ESP / FeatherWing)
//   Component hole patterns are placeholders — structure/placement only.
// ============================================================================
$fn = 40;

CX = 45;  CY = 75;          // frame corner pattern (X-arm tips)
HUB_H = 14;                 // each frame thickness
STANDOFF = 40;              // 8-32 standoff length
nano_z = 0;
orin_z = HUB_H + STANDOFF;  // 54 — Orin frame underside

// ---- the two real frames ----
color([0.30,0.45,0.70,0.95]) translate([0,0,nano_z]) import("nano_tubeclamp_xframe.stl");
color([0.85,0.42,0.36,0.95]) translate([0,0,orin_z]) import("orin_topframe.stl");

// ---- 4 corner 8-32 standoffs ----
color([0.55,0.55,0.6,0.95])
for (sx=[-1,1], sy=[-1,1])
  translate([sx*CX, sy*CY, HUB_H]) difference(){ cylinder(d=12,h=STANDOFF); cylinder(d=4.5,h=STANDOFF+0.1); }

// ---- RSD flange on the +X LONG side, spanning both frames ----
// RSD 4× #8-32 at 51.83 (vertical/Z) × 120.18 (horizontal/Y)
RSD_PZ = 51.83; RSD_PY = 120.18; RSD_D = 4.4;
flange_x = CX + 12;                          // X=57, just outboard of the +X corner bosses
mid_z = (HUB_H + orin_z + HUB_H) / 2;        // ~41, centered across the stack height
hub_x  = 36;                                 // +X hub face (HUB_X/2) where the M3 inserts live
ATT_Y  = 20; ATT_Z = HUB_H/2;                // existing +X-face M3 inserts (per frame): Y=±20, Z=7
ins_z  = [ATT_Z, orin_z + ATT_Z];            // 7 (Nano) and 61 (Orin)
module rsd_flange() {
  fz0 = min(ins_z[0], mid_z - RSD_PZ/2) - 6; // covers the lower insert + lower holes
  fz1 = max(ins_z[1], mid_z + RSD_PZ/2) + 6; // covers the upper insert + upper holes
  fw  = RSD_PY + 16;                         // Y width, centered on Y=0
  difference() {
    translate([flange_x, -fw/2, fz0]) cube([4, fw, fz1 - fz0]);
    // RSD #8-32 pattern on the outer face
    for (sy=[-1,1], sz=[-1,1])
      translate([flange_x-0.1, sy*RSD_PY/2, mid_z + sz*RSD_PZ/2]) rotate([0,90,0]) cylinder(d=RSD_D, h=6);
    // M3 clearance holes that land on the 4 EXISTING side inserts
    for (sy=[-1,1], zc=ins_z)
      translate([flange_x-0.1, sy*ATT_Y, zc]) rotate([0,90,0]) cylinder(d=3.4, h=6);
  }
  // mounting extrusions from the flange back to the 4 EXISTING M3 inserts (X=36)
  for (sy=[-1,1], zc=ins_z)
    translate([hub_x, sy*ATT_Y-5, zc-5]) cube([flange_x - hub_x + 4, 10, 10]);
}
color([0.20,0.55,0.55,0.95]) rsd_flange();

// ---- component-plate frames on each SHORT (±Y) side ----
// generic plate held by 4 M3 inserts; placeholder modules shown on it
SP_X = 20;          // ±Y-face M3 insert X positions (mirror of the long-side inserts)
hub_y = 50;         // ±Y hub face (HUB_Y/2)
module side_plate(sy) {
  py  = sy*(hub_y + 30);                       // plate stands ~30mm off the face (clears the arms)
  pz0 = HUB_H - 11; pz1 = orin_z + HUB_H + 4;  // same Z span as the RSD flange
  // plate (vertical X-Z) with M3 clearance holes landing on the ±Y inserts
  color([0.45,0.70,0.45,0.92])
  difference() {
    translate([-46, py-2, pz0]) cube([92, 4, pz1-pz0]);
    for (sx=[-1,1], zc=ins_z)
      translate([sx*SP_X, py, zc]) rotate([90,0,0]) cylinder(d=3.4, h=12, center=true);
  }
  // mounting extrusions from the 4 EXISTING ±Y inserts (Y=sy*hub_y) out to the plate
  color([0.55,0.55,0.6,0.95])
  for (sx=[-1,1], zc=ins_z)
    translate([sx*SP_X-5, min(sy*hub_y, py), zc-5]) cube([10, abs(py - sy*hub_y), 10]);
  // placeholder modules on the plate's outer face
  if (sy>0) {
    color([0.2,0.2,0.25,0.7]) translate([-40, py+2, 16]) cube([34,3,26]);   // relay
    color([0.2,0.2,0.25,0.7]) translate([6,  py+2, 18]) cube([32,3,18]);    // ESP
  } else {
    color([0.2,0.2,0.25,0.7]) translate([-23, py-5, 22]) cube([46,3,18]);   // FeatherWing
  }
}
side_plate(1);
side_plate(-1);
