// ============================================================================
// T1 STACK on the concept-E deck — placement + interference study (read-only use
// of t1_concept_E.scad; that file is NOT edited).  RED = where the E antenna
// level (rods, yokes, MA963, dome, CO tray) passes through the stack's envelope.
//   openscad -D 'rev="C"' ...   (rev = "B" | "C"; set here AFTER the include so it overrides the E default)
// Placement: bay R, stack slide axis along deck +X (I/O face toward the x = 406
// end face), stack -X -> deck +Y (nose); cheese plate spans the centre member
// (x 203) and the x = 406 end member (x 396) on 8 mm risers (belt tunnel).
// ============================================================================
include <../t1_concept_E.scad>
use <make_t1_stack.scad>
view = "none";
rev = "C";
X_OFF = 232;          // deck x of the case back ends (stack y = 0)
Y_CTR = DYE / 2;      // deck y of the stack centreline
RISER = 8;            // Al risers on the member tops: cheese underside at z 28 (belt / strap tunnel over the tray skin z 24)
Z_OFF = E + RISER + 10;   // cheese-plate top (plate 10 EST)
S_ENV = [[-126, -95, 0], [174, 95, 171.5]];   // stack y 174 -> deck x 406: the cable bar stops at the end-face plane   // stack envelope in stack coords (from make_t1_stack echo)

module on_deck() translate([X_OFF, Y_CTR, Z_OFF]) rotate([0, 0, -90]) mirror([0, 0, 0]) children();
module env_box() on_deck() translate(S_ENV[0]) cube(S_ENV[1] - S_ENV[0]);

deck_frame();
posts_and_rods();
color([0.55, 0.56, 0.6]) for (x = [203, 396], y = [Y_CTR - 70, Y_CTR + 70]) translate([x - 8, y - 8, E]) cube([16, 16, RISER]);   // risers
on_deck() stack();
color([0.95, 0.1, 0.1]) intersection() { posts_and_rods(); env_box(); }                             // the conflict
// belt band + tunnel marker (lap belt at deck level, under the cheese plate and the hanging battery)
color([1, 0.8, 0], 0.5) for (y = BELT) translate([0, y - 1, E + 5]) cube([DXE, 2, 1]);
