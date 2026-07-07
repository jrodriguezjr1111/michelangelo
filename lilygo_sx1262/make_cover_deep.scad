// ============================================================================
// CyberWing — LilyGo TOP COVER (mates the deep base, sandwiches the plate)
// Completes the stack: deep base (make_base_deep) + existing 101×65 top plate
// (T-Beam on 5 mm bosses, 18650 holder hanging through the cutout) + THIS.
// The cover's skirt wraps the base's outer wall and self-taps into it with 4
// side M3s, clamping the plate between cover and base rim — no shared axes.
// Openings: OLED window, USB-C cable slot (bottom -X end, open downward so the
// cover drops on with the cable attached), antenna notch (top +X end for the
// SMA elbow, whip outside).
//   Model: z=0 at the PLATE TOP, cover rises +z; skirt hangs -z over the base.
// CONFIRM: CAV_H (tallest point above the plate), window/slot positions.
// part = "cover" | "coverprint" (flipped for the bed)
// ============================================================================
$fn = 44;
part = "cover";

// ---- stack interfaces ----
L = 101; W = 65;                 // plate/base footprint
PLATE_T = 4;                     // existing plate
CAV_H = 18;                      // interior above the plate top (MEASURE: acrylic top + clr)
WALL = 3; ROOF = 3;
SK_T = 2.4; SK_CLR = 0.3;        // skirt over the base wall
SK_ENG = 10;                     // skirt engagement below the plate underside
M3 = 3.4; PILOT = 2.7;
SCREW_X = [-30, 30];             // skirt screws, both long sides

// ---- openings (positions from the photos — CONFIRM) ----
OLED_W = 42; OLED_H = 17; OLED_X = 22;    // window centered at x=+22 (upper board)
USB_W = 16;                                // bottom (-X) cable slot, open downward
ANT_W = 18; ANT_X0 = 8;                    // top (+X) antenna notch in roof+wall

HTOT = CAV_H + ROOF;             // above plate
SK_DEP = PLATE_T + SK_ENG;       // skirt drop below z=0

module cover() {
  difference() {
    union() {
      // shell above the plate
      translate([-L/2-SK_CLR-SK_T, -W/2-SK_CLR-SK_T, 0])
        cube([L+2*(SK_CLR+SK_T), W+2*(SK_CLR+SK_T), HTOT]);
      // skirt hanging over plate edge + base wall
      difference() {
        translate([-L/2-SK_CLR-SK_T, -W/2-SK_CLR-SK_T, -SK_DEP])
          cube([L+2*(SK_CLR+SK_T), W+2*(SK_CLR+SK_T), SK_DEP]);
        translate([-L/2-SK_CLR, -W/2-SK_CLR, -SK_DEP-0.1])
          cube([L+2*SK_CLR, W+2*SK_CLR, SK_DEP+0.2]);
      }
    }
    // interior cavity (walls inset WALL from the plate edge)
    translate([-L/2+WALL, -W/2+WALL, -0.1]) cube([L-2*WALL, W-2*WALL, CAV_H+0.1]);
    // OLED window
    translate([OLED_X-OLED_W/2, -OLED_H/2, CAV_H-0.1]) cube([OLED_W, OLED_H, ROOF+0.2]);
    // USB-C slot: bottom (-X) end, open down through the skirt
    translate([-L/2-SK_CLR-SK_T-0.1, -USB_W/2, -SK_DEP-0.1])
      cube([WALL+SK_CLR+SK_T+0.2, USB_W, SK_DEP+CAV_H*0.55+0.1]);
    // antenna notch: top (+X) end wall + roof strip (SMA elbow + whip out)
    translate([L/2-WALL-SK_CLR-0.1, -ANT_W/2, -0.1]) cube([WALL+SK_CLR+SK_T+0.2, ANT_W, HTOT+0.2]);
    // skirt screw holes (self-tap into the base wall)
    for (fx=SCREW_X, sy=[-1,1])
      translate([fx, sy*(W/2+SK_CLR+SK_T/2), -PLATE_T-SK_ENG/2])
        rotate([sy>0?-90:90,0,0]) cylinder(d=M3, h=SK_T+0.4, center=true);
  }
}

if (part=="cover") cover();
if (part=="coverprint") translate([0,0,HTOT]) rotate([180,0,0]) cover();
