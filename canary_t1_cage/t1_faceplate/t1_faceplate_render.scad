// ============================================================================
// t1_faceplate — RENDER WRAPPER.  Presents one plate in VIEW orientation
// (face toward +z, reads as seen from outside the box) with its yellow label
// plate seated, for the front / back / iso PNGs.  Pure presentation: every
// number comes from make_t1_faceplate.scad through the module arguments.
// ============================================================================
use <make_t1_faceplate.scad>
use <../make_style_coupon.scad>

w = 84;  h = 100;  mount = "bolt";  sides = [0, 1, 1, 1];  neighbour = [0, 1, 0, 1];
vent = "hex";  vent_min_cm2 = 0;  grip = "top";  label = true;  mark = true;  slot_edges = "lr";
label_txt = "SPARE";  name = "";
BLK = [0.22, 0.22, 0.25];  YEL = [1.00, 0.80, 0.00];

rotate([0, 180, 0]) {                                 // print coords -> view coords (face up, reads right)
  color(BLK) faceplate(w = w, h = h, mount = mount, sides = sides, neighbour = neighbour, vent = vent,
                       vent_min_cm2 = vent_min_cm2, grip = grip, label = label, mark = mark,
                       slot_edges = slot_edges, name = name);
  if (label) color(YEL) mirror([1, 0, 0]) translate([0, fp_label_y(h), fp_lp_t() + 0.2]) mirror([0, 0, 1]) plate(label_txt);
}
