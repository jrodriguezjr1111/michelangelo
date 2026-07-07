// ============================================================================
// CyberWing — RSD X-FRAME on the stack's +X long-side M3 inserts (tube-clearing)
// Open truss: 4 mount standoffs (40.54 × 53.64 grid; upper Ø7.8, lower Ø4.2),
// cross-braced and armed out to the 4 RSD corners (120.18 × 51.83). Shifted up
// 10 mm so the body clears the GNSS tubes that pass just below.
//   model X = stack Y (across); model Y = stack Z (up); model Z = mount-out
// show_tubes=true overlays the tubes for a clearance check.
// ============================================================================
$fn = 48;
show_tubes = false;

SHIFT = 10;                                   // plate shift up (model +Y)
GX = 40.54/2; GYn = -53.64/2; GYo = 53.64/2;  // standoff grid: X=±20.27, Nano Y, Orin Y (about grid center)
// joints in model coords (grid centered at model Y=0; RSD shifted +SHIFT)
Sul = [-GX, GYo]; Sur = [GX, GYo];            // upper (Orin) standoffs
Sll = [-GX, GYn]; Slr = [GX, GYn];            // lower (Nano) standoffs
Rx = 120.18/2; Rt = SHIFT + 51.83/2; Rb = SHIFT - 51.83/2;
Rul = [-Rx, Rt]; Rur = [Rx, Rt]; Rll = [-Rx, Rb]; Rlr = [Rx, Rb];  // RSD corners

T = 5; BW = 6; BW_LO = 4;                     // extrude thick, beam width (lower beams thinner)
SO_UP = 7.8; SO_LO = 4.2; SO_H = 14; SO_BORE = 3.4;
RSD_CLR = 4.5; M3_CB_D = 6; M3_CB_H = 3; BOSS_D = 10;

module beam(a, b, w=BW) { hull() { translate(a) circle(d=w); translate(b) circle(d=w); } }

module frame2d() {
  beam(Sul, Sur);                              // top standoff rail
  beam(Sul, Sll); beam(Sur, Slr);              // side rails
  beam(Sul, Slr); beam(Sur, Sll);             // central X-brace
  beam(Sul, Rul); beam(Sur, Rur);             // upper arms to RSD
  beam(Sll, Rll, BW_LO); beam(Slr, Rlr, BW_LO);  // lower arms (thinner, near tubes)
  beam(Rul, Rur); beam(Rll, Rlr);             // RSD top + bottom rails
  for (p=[Rul,Rur,Rll,Rlr]) translate(p) circle(d=BOSS_D);   // RSD bosses
  for (p=[Sul,Sur]) translate(p) circle(d=9);                // upper standoff pads
  for (p=[Sll,Slr]) translate(p) circle(d=5.5);              // lower standoff pads (small)
}

module part() {
  difference() {
    union() {
      linear_extrude(T) frame2d();
      for (p=[Sul,Sur]) translate([p[0],p[1],T]) cylinder(d=SO_UP, h=SO_H);
      for (p=[Sll,Slr]) translate([p[0],p[1],T]) cylinder(d=SO_LO, h=SO_H);
    }
    for (p=[Sul,Sur,Sll,Slr]) {
      translate([p[0],p[1],-0.1]) cylinder(d=SO_BORE, h=T+SO_H+0.2);
      translate([p[0],p[1],-0.1]) cylinder(d=M3_CB_D, h=M3_CB_H);
    }
    for (p=[Rul,Rur,Rll,Rlr]) translate([p[0],p[1],-0.1]) cylinder(d=RSD_CLR, h=T+0.2);
  }
}

part();

if (show_tubes)
  color([0.55,0.42,0.62,0.45])
  for (sx=[-1,1]) translate([sx*30.085, -34, -40]) cylinder(d=15.39, h=120);
