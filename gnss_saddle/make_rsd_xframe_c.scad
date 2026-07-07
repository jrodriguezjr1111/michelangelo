// ============================================================================
// CyberWing — RSD X-FRAME, tube-clamping version
// Top: 2 standoffs to the Orin +X inserts (Ø7.8). Bottom: 2 C-clip legs that
// WRAP the GNSS tubes (Ø15.39) for the lower anchor. Open truss carries the RSD
// (4× #8-32, 120.18 × 51.83), shifted up 10 mm.
//   model X = stack Y (across); model Y = stack Z (up); model Z = mount-out / tube axis
// show_tubes=true overlays the tubes.
// ============================================================================
$fn = 56;
show_tubes = false;

SHIFT = 10;
GX = 40.54/2;                                   // Orin standoff X = ±20.27
Sul = [-GX, 53.64/2]; Sur = [GX, 53.64/2];      // upper (Orin) standoffs
Tl  = [-30.085, -34]; Tr = [30.085, -34];       // tube centers (= lower C-clips)
Rx = 120.18/2; Rt = SHIFT + 51.83/2; Rb = SHIFT - 51.83/2;
Rul = [-Rx, Rt]; Rur = [Rx, Rt]; Rll = [-Rx, Rb]; Rlr = [Rx, Rb];

T = 5; BW = 6; BW_LO = 6.5;
SO_UP = 7.8; SO_H = 14; SO_BORE = 3.4; M3_CB_D = 6; M3_CB_H = 3;
RSD_CLR = 4.5; BOSS_D = 10;
TUBE_D = 15.39; TUBE_CLR = 0.5; CLIP_OD = 22; CLIP_H = 16; OPEN_DEG = 95;  // C-clip

module beam(a, b, w=BW) { hull() { translate(a) circle(d=w); translate(b) circle(d=w); } }

module frame2d() {
  beam(Sul, Sur);                               // top rail between standoffs
  beam(Sul, Rul); beam(Sur, Rur); beam(Rul, Rur);   // upper arms + RSD top rail
  beam(Sul, Tl); beam(Sur, Tr);                 // side rails to the tube clips
  beam(Sul, Tr); beam(Sur, Tl);                 // central X-brace
  beam(Tl, Rll, BW_LO); beam(Tr, Rlr, BW_LO);   // lower arms tube -> RSD boss
  beam(Tl, Tr, BW_LO);                          // bottom rail between the clips
  beam(Rll, Rlr);                               // RSD bottom rail
  for (p=[Rul,Rur,Rll,Rlr]) translate(p) circle(d=BOSS_D);   // RSD bosses
  for (p=[Sul,Sur]) translate(p) circle(d=9);                // standoff pads
}

// C-clip wrapping a tube (opening faces +Y, toward the frame)
module cclip(p) {
  translate([p[0], p[1], 0]) linear_extrude(CLIP_H)
    difference() {
      circle(d=CLIP_OD);
      circle(d=TUBE_D + TUBE_CLR);
      polygon([[0,0],
               [CLIP_OD*cos(90+OPEN_DEG/2), CLIP_OD*sin(90+OPEN_DEG/2)],
               [CLIP_OD*cos(90-OPEN_DEG/2), CLIP_OD*sin(90-OPEN_DEG/2)]]);
    }
}

module part() {
  difference() {
    union() {
      linear_extrude(T) frame2d();
      for (p=[Sul,Sur]) translate([p[0],p[1],T]) cylinder(d=SO_UP, h=SO_H);
      cclip(Tl); cclip(Tr);
    }
    for (p=[Sul,Sur]) {
      translate([p[0],p[1],-0.1]) cylinder(d=SO_BORE, h=T+SO_H+0.2);
      translate([p[0],p[1],-0.1]) cylinder(d=M3_CB_D, h=M3_CB_H);
    }
    for (p=[Rul,Rur,Rll,Rlr]) translate([p[0],p[1],-0.1]) cylinder(d=RSD_CLR, h=T+0.2);
  }
}

part();

if (show_tubes)
  color([0.55,0.42,0.62,0.4])
  for (sx=[-1,1]) translate([sx*30.085, -34, -30]) cylinder(d=TUBE_D, h=90);
