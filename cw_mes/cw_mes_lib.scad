/* ======================================================================
   CW-MES — shared engine (cw_mes_lib.scad)
   Do NOT set parameters here. Instance files (cw_mes_<box>.scad) define
   all parameters, then `include <cw_mes_lib.scad>`. Identical joint
   geometry across every box in the family lives in this one file —
   panels with matching edge lengths and tab counts interchange.
   Extracted unmodified from cw_mes_enclosure.scad v1.0.
   ====================================================================== */
/* ====================== INTERNALS ===================== */
$fn = 40;
eps = 0.01;
o   = rim + t;                       // plate interior origin offset
W_fb = inner.x + 2*t;                // front/back wall width
W_lr = inner.y;                      // left/right wall width
H_w  = inner.z;                      // wall height
BX = inner.x + 2*t + 2*rim;          // plate footprint
BY = inner.y + 2*t + 2*rim;
nut_pos = bolt_l - t - nut_t - 1.0;  // edge -> nut near face

echo(str("Plate footprint: ", BX, " x ", BY, " mm  (bed 305x305)"));
echo(str("Bolt engagement: outer face -> nut far face = ",
         t + nut_pos + nut_t, " mm vs bolt_l = ", bolt_l));
assert(nut_pos > 1.5, "bolt_l too short for panel thickness — increase bolt_l");

// optional round wall cutouts (gland bores); instances may leave them undefined
rc_front = is_undef(cut_front_round) ? [] : cut_front_round;
rc_back  = is_undef(cut_back_round)  ? [] : cut_back_round;
rc_left  = is_undef(cut_left_round)  ? [] : cut_left_round;
rc_right = is_undef(cut_right_round) ? [] : cut_right_round;

// optional card-cage guides on the LEFT/RIGHT walls: list of shelf z-heights.
// Each shelf = a pair of ribs on the inner face; a plate slides in along Y.
cg_lr   = is_undef(card_guides)    ? [] : card_guides;     // guides on L/R (YZ) walls
cg_fb   = is_undef(card_guides_fb) ? [] : card_guides_fb;  // guides on F/B (XZ) walls
sad_holes = is_undef(saddle_holes) ? [] : saddle_holes;    // GNSS-saddle mount [x,y] (bottom plate)
sad_d     = is_undef(saddle_d)     ? 4.4 : saddle_d;       // M4 clearance
pb_list = is_undef(plate_bosses)    ? [] : plate_bosses;   // standoffs on a card plate [x,y from center]
pb_h    = is_undef(plate_boss_h)    ? 10  : plate_boss_h;
pb_d    = is_undef(plate_boss_d)    ? 7   : plate_boss_d;
pb_bore = is_undef(plate_boss_bore) ? 3.4 : plate_boss_bore;
plate_t = is_undef(card_plate_t) ? 2.0 : card_plate_t;   // slide-in plate thickness
cg_gap  = plate_t + 0.5;          // slot gap (plate + slide clearance)
cg_rw   = 1.8;                     // rib thickness (height direction)
cg_rh   = 4.0;                     // rib inward protrusion
cg_ch   = is_undef(card_chamfer) ? 1.2 : card_chamfer;  // funnel chamfer on the slot mouth (F/B)
cg_ch_lr = is_undef(rail_chamfer_lr) ? cg_ch : rail_chamfer_lr;  // L/R (green) chamfer (0 = square)
cg_frac_lr = is_undef(rail_frac_lr) ? 1.0 : rail_frac_lr;  // L/R (green) rail length fraction

// Card-rail pair at height h, chamfered so the slot mouth funnels (easy snap-in).
// x0/L = start/length along the wall; gside sets which face the ribs grow from.
module card_rails(x0, L, guides, gside, ch = cg_ch) {
  zb = gside > 0 ? t - eps : eps;            // base (overlaps the wall face)
  zt = gside > 0 ? t + cg_rh : -cg_rh;       // protruded tip
  for (h = guides) {
    hull() {                                  // bottom rib — chamfer (ch) its slot (upper) side
      translate([x0, h - cg_gap/2 - cg_rw, zb]) cube([L, cg_rw, 0.01]);
      translate([x0, h - cg_gap/2 - cg_rw, zt]) cube([L, cg_rw - ch, 0.01]);
    }
    hull() {                                  // top rib — chamfer its slot (lower) side
      translate([x0, h + cg_gap/2,    zb]) cube([L, cg_rw, 0.01]);
      translate([x0, h + cg_gap/2 + ch, zt]) cube([L, cg_rw - ch, 0.01]);
    }
  }
}

function seg(L, n)     = L / (2*n + 1);
function tabs0(L, n)   = [for (i = [0:n-1]) (2*i + 1) * seg(L, n)];
function boltsAt(L, n) = n < 2 ? [] :
                         [for (i = [1:n-1]) (2*i) * seg(L, n) + seg(L, n)/2];

module rsq(size, r = 2)              // rounded-corner square
  offset(r) offset(-r) square(size);

module rrect(w, h, r = 2)            // rounded cutout rect
  offset(r) offset(-r) square([w, h]);

module tabrects(L, n, d)             // tab row along +x, protruding -y
  for (x = tabs0(L, n))
    translate([x, -d - eps]) square([seg(L, n), d + 2*eps]);

module tslot() {                     // T-slot: edge at y=0, opens into +y body
  translate([-bolt_d/2, -eps]) square([bolt_d, nut_pos + nut_t + eps]);
  translate([-nut_w/2, nut_pos]) square([nut_w, nut_t]);
}

module vents(region) {
  if (len(region) == 4)
    intersection() {
      translate([region[0], region[1]]) rrect(region[2], region[3], 3);
      for (y = [region[1] : vent_pitch : region[1] + region[3]])
        translate([region[0] - 5, y])
          rrect(region[2] + 10, vent_slot, vent_slot/2 - eps);
    }
}

/* ---------------- FRONT / BACK WALL ---------------- */
module wall_fb(cuts = [], rcuts = [], guides = [], gside = 1) {
  card_rails(t, inner.x, guides, gside);                // funneled card rails (run along X)
  difference() {
    linear_extrude(t) difference() {
      union() {
        square([W_fb, H_w]);
        translate([t, 0])                  tabrects(inner.x, nx, t);  // bottom tabs
        translate([t, H_w]) mirror([0,1])  tabrects(inner.x, nx, t);  // top tabs
      }
      // vertical corner slots (receive left/right wall tabs)
      for (ys = tabs0(inner.z, nz)) {
        translate([-eps,            ys - clr]) square([t + clr + eps, seg(inner.z, nz) + 2*clr]);
        translate([W_fb - t - clr,  ys - clr]) square([t + clr + eps, seg(inner.z, nz) + 2*clr]);
      }
      // T-slots, bottom & top edges
      for (b = boltsAt(inner.x, nx)) {
        translate([t + b, 0])                  tslot();
        translate([t + b, H_w]) mirror([0,1])  tslot();
      }
      // corner bolt holes (vertical joints)
      for (gz = boltsAt(inner.z, nz)) {
        translate([t/2,        gz]) circle(d = bolt_d);
        translate([W_fb - t/2, gz]) circle(d = bolt_d);
      }
      // user port cutouts
      for (c = cuts) translate([t + c[0], c[1]]) rrect(c[2], c[3]);
      // round cutouts (e.g. cable-gland bores): [x, z, Ø]
      for (rc = rcuts) translate([t + rc[0], rc[1]]) circle(d = rc[2]);
    }
    // optional counterbores on outer face (local z = 0)
    if (cbore_h > 0)
      for (gz = boltsAt(inner.z, nz), x = [t/2, W_fb - t/2])
        translate([x, gz, -eps]) cylinder(d = cbore_d, h = cbore_h + eps);
  }
}

/* ---------------- LEFT / RIGHT WALL ---------------- */
// gside = +1 puts the card ribs on the +Z (local) face, -1 on the -Z face — set
// per wall so the ribs always protrude INTO the cavity.
module wall_lr(cuts = [], rcuts = [], guides = [], gside = 1) {
  card_rails(W_lr*(1-cg_frac_lr)/2, W_lr*cg_frac_lr, guides, gside, cg_ch_lr);  // centered, cg_frac_lr length, own chamfer
  linear_extrude(t) difference() {
    union() {
      square([W_lr, H_w]);
      tabrects(inner.y, ny, t);                            // bottom tabs
      translate([0, H_w]) mirror([0,1])
        tabrects(inner.y, ny, t);                          // top tabs
      for (ys = tabs0(inner.z, nz)) {                      // vertical tabs
        translate([-t,   ys]) square([t, seg(inner.z, nz)]);
        translate([W_lr, ys]) square([t, seg(inner.z, nz)]);
      }
    }
    for (b = boltsAt(inner.y, ny)) {                       // T-slots top/bottom
      translate([b, 0])                 tslot();
      translate([b, H_w]) mirror([0,1]) tslot();
    }
    for (gz = boltsAt(inner.z, nz)) {                      // T-slots vertical
      translate([0,    gz]) rotate(-90) tslot();
      translate([W_lr, gz]) rotate( 90) tslot();
    }
    for (c = cuts) translate([c[0], c[1]]) rrect(c[2], c[3]);
    // round cutouts (e.g. cable-gland bores): [y, z, Ø]
    for (rc = rcuts) translate([rc[0], rc[1]]) circle(d = rc[2]);
  }
}

/* ---------------- TOP / BOTTOM PLATE ---------------- */
function plate_holes() = concat(
  [for (b = boltsAt(inner.x, nx)) [o + b, rim + t/2]],
  [for (b = boltsAt(inner.x, nx)) [o + b, BY - rim - t/2]],
  [for (b = boltsAt(inner.y, ny)) [rim + t/2,      o + b]],
  [for (b = boltsAt(inner.y, ny)) [BX - rim - t/2, o + b]]);

module plate(is_bottom = true) {
  difference() {
    union() {
      linear_extrude(t) difference() {
        rsq([BX, BY], rim + 1);
        // wall tab slots (closed — protected by the rim)
        for (xs = tabs0(inner.x, nx)) {
          translate([o + xs - clr, rim - clr])
            square([seg(inner.x, nx) + 2*clr, t + 2*clr]);
          translate([o + xs - clr, BY - rim - t - clr])
            square([seg(inner.x, nx) + 2*clr, t + 2*clr]);
        }
        for (ys = tabs0(inner.y, ny)) {
          translate([rim - clr, o + ys - clr])
            square([t + 2*clr, seg(inner.y, ny) + 2*clr]);
          translate([BX - rim - t - clr, o + ys - clr])
            square([t + 2*clr, seg(inner.y, ny) + 2*clr]);
        }
        for (p = plate_holes()) translate(p) circle(d = bolt_d);
        if (!is_bottom) translate([o, o]) vents(vent_top);
      }
      if (is_bottom)                                       // standoff bosses
        for (h = mount_holes)
          translate([o + h.x, o + h.y, t - eps])
            cylinder(d = boss_d, h = boss_h + eps);
    }
    if (is_bottom)                                         // insert pilots
      for (h = mount_holes)
        translate([o + h.x, o + h.y, t + boss_h - insert_h])
          cylinder(d = insert_d, h = insert_h + eps);
    if (is_bottom)                                         // GNSS-saddle mount holes (through)
      for (h = sad_holes)
        translate([o + h.x, o + h.y, -eps]) cylinder(d = sad_d, h = t + 2*eps);
    if (cbore_h > 0)                                       // counterbores, outer face
      for (p = plate_holes())
        translate([p.x, p.y, -eps]) cylinder(d = cbore_d, h = cbore_h + eps);
  }
}

/* ---------------- FIT-TEST COUPONS ---------------- */
module fittest() {
  // Instance files may set `fit_tests` to tune the coupon range per material
  // (PETG ~[0.12, 0.18, 0.24]; PLA ~[0.10, 0.15, 0.20]).
  tests = is_undef(fit_tests) ? [0.12, 0.18, 0.24] : fit_tests;
  difference() {
    linear_extrude(t) rsq([78, 26], 2);
    for (i = [0 : len(tests) - 1]) {
      c = tests[i];
      translate([10 + i*24 - c, 14, -eps])
        cube([10 + 2*c, t + 2*c, t + 2*eps]);
      translate([10 + i*24, 4, t - 0.6])
        linear_extrude(1) text(str(c), size = 4);
    }
  }
  translate([0, 32]) linear_extrude(t) union() {        // tab coupon, 10 mm tab
    square([20, 12]);
    translate([5, 12]) square([10, t]);
  }
}

/* ---------------- SLIDE-IN CARD PLATE ---------------- */
// Sized so its X edges ride the left/right wall guides; slides in along Y.
// M3 component-mount grid; edit the spacing per board.
module card_plate() {
  both = len(cg_fb) > 0 && len(cg_lr) > 0;   // 4-sided -> full plate, drops in from the top
  fb   = len(cg_fb) > 0;                      // F/B only -> edges ride front/back, slide along X
  pw = both ? inner.x - 0.8 : (fb ? inner.x - 3   : inner.x - 0.6);   // X
  pd = both ? inner.y - 0.8 : (fb ? inner.y - 0.6 : inner.y - 3);     // Y
  difference() {
    translate([-pw/2, -pd/2, 0]) cube([pw, pd, plate_t]);
    for (gx = [-pw/2 + 12 : 22 : pw/2 - 10])
      for (gy = [-pd/2 + 9 : 18 : pd/2 - 8])
        translate([gx, gy, -1]) cylinder(d = 3.2, h = plate_t + 2);
  }
}

// Same footprint, but with standoff bosses (no grid) — component mount plate.
module card_plate_boss() {
  both = len(cg_fb) > 0 && len(cg_lr) > 0;
  fb   = len(cg_fb) > 0;
  pw = both ? inner.x - 0.8 : (fb ? inner.x - 3   : inner.x - 0.6);
  pd = both ? inner.y - 0.8 : (fb ? inner.y - 0.6 : inner.y - 3);
  difference() {
    union() {
      translate([-pw/2, -pd/2, 0]) cube([pw, pd, plate_t]);
      // boss entry: [x, y] or [x, y, od, bore] for mixed patterns on one plate
      for (b = pb_list) translate([b[0], b[1], plate_t - eps]) cylinder(d = len(b) >= 3 ? b[2] : pb_d, h = pb_h + eps);
    }
    for (b = pb_list) translate([b[0], b[1], -1]) cylinder(d = len(b) >= 4 ? b[3] : pb_bore, h = plate_t + pb_h + 2);
  }
}

/* ---------------- VIEWS ---------------- */
module assembled() {
  color("SteelBlue")  translate([-o, -o, -t]) plate(true);
  color("SteelBlue")  translate([-o, -o, inner.z + t]) mirror([0,0,1]) plate(false);
  color("Orange")     translate([-t, 0, 0])           rotate([90,0,0])  wall_fb(cut_front, rc_front, cg_fb, -1);
  color("Orange")     translate([-t, inner.y + t, 0]) rotate([90,0,0])  wall_fb(cut_back,  rc_back,  cg_fb,  1);
  color("LightGreen") translate([-t, 0, 0])           rotate([90,0,90]) wall_lr(cut_left,  rc_left,  cg_lr,  1);
  color("LightGreen") translate([inner.x, 0, 0])      rotate([90,0,90]) wall_lr(cut_right, rc_right, cg_lr, -1);
}

module plate_layout() {
  g = 10;
  plate(true);
  translate([BX + g, 0]) plate(false);
  translate([t, BY + g + t])                    wall_fb(cut_front, rc_front, cg_fb);
  translate([t, BY + g + 2*t + H_w + g + t])    wall_fb(cut_back,  rc_back,  cg_fb);
  translate([2*BX + 2*g + t, t])                rotate(90) wall_lr(cut_left,  rc_left,  cg_lr);
  translate([2*BX + 2*g + H_w + 3*t + g, t])    rotate(90) wall_lr(cut_right, rc_right, cg_lr);
}

if      (view == "assembled") assembled();
else if (view == "plate")     plate_layout();
else if (view == "bottom")    plate(true);
else if (view == "top")       plate(false);
else if (view == "front")     wall_fb(cut_front, rc_front, cg_fb);
else if (view == "back")      wall_fb(cut_back,  rc_back,  cg_fb);
else if (view == "left")      wall_lr(cut_left,  rc_left,  cg_lr);
else if (view == "right")     wall_lr(cut_right, rc_right, cg_lr);
else if (view == "card")      card_plate();
else if (view == "cardboss")  card_plate_boss();
else if (view == "fittest")   fittest();
