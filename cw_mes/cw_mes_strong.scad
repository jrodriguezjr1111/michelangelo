/* ======================================================================
   cw_mes_strong.scad — ADDITIVE strengthening + mounts for the Nano plate.
   Include AFTER cw_mes_lib.scad; uses its globals (BX, BY, o, t, rim, eps).
   Renders via view="strong" -> strong_bottom().  STEP 1 (no saddle yet).
   Nothing here edits the existing library or instance files.
   ====================================================================== */

// ---- params (override in the instance; safe is_undef defaults) ----
rib_h2     = is_undef(rib_h)      ? 8    : rib_h;      // rib depth below the plate
rib_w2     = is_undef(rib_w)      ? 2.4  : rib_w;      // rib thickness
rib_pitch2 = is_undef(rib_pitch)  ? 24   : rib_pitch;  // lattice spacing

rsd_on     = is_undef(rsd_ledge)    ? false  : rsd_ledge;
rsd_px2    = is_undef(rsd_PX)       ? 51.83  : rsd_PX;        // short span -> vertical (Z)
rsd_py2    = is_undef(rsd_PY)       ? 120.18 : rsd_PY;        // long span  -> horizontal (X) ∥ ground
rsd_insd   = is_undef(rsd_insert_d) ? 4.0    : rsd_insert_d;  // M3 heat-set pilot
rsd_insh   = is_undef(rsd_insert_h) ? 6      : rsd_insert_h;
rsd_gap    = is_undef(rsd_ledge_gap)? 8      : rsd_ledge_gap; // outboard standoff

posts2     = is_undef(post_list)     ? []  : post_list;       // [[x,y],...] in plate frame
post_h2    = is_undef(post_h)        ? 30  : post_h;
post_d2    = is_undef(post_d)        ? 9   : post_d;
post_insd  = is_undef(post_insert_d) ? 4.0 : post_insert_d;
post_insh  = is_undef(post_insert_h) ? 6   : post_insert_h;

// ---- underside rib lattice (prints ribs-down, no support) ----
module rib_lattice() {
  ins = o + 1;
  for (yy = [ins : rib_pitch2 : BY - ins])
    translate([ins, yy - rib_w2/2, -rib_h2]) cube([BX - 2*ins, rib_w2, rib_h2 + eps]);
  for (xx = [ins : rib_pitch2 : BX - ins])
    translate([xx - rib_w2/2, ins, -rib_h2]) cube([rib_w2, BY - 2*ins, rib_h2 + eps]);
}

// ---- RSD outboard vertical flange (RSD on its side: 120.18 horizontal) ----
module rsd_ledge() {
  fw = rsd_py2 + 22;          // flange width  (X)
  ft = rsd_insh + 4;         // flange thickness (Y) — hosts the inserts
  fh = rsd_px2 + 28;         // flange height (Z)
  cx = BX/2;
  fy = BY + rsd_gap;         // flange inner face
  difference() {
    union() {
      translate([cx - fw/2, BY - eps, 0]) cube([fw, rsd_gap + ft, t + 5]);  // web from edge -> flange
      translate([cx - fw/2, fy, 0])       cube([fw, ft, fh]);               // vertical flange
      // corner gussets bracing flange to web
      for (sx = [-1, 1])
        translate([cx + sx*(fw/2 - eps), fy, 0]) rotate([0, sx*90, 0])
          linear_extrude(2.4, center = true) polygon([[0,0],[ft + rsd_gap, 0],[0, fh*0.6]]);
    }
    // 4 M3 insert bores from the outer (+Y) face inward
    for (sx = [-1, 1], sz = [-1, 1])
      translate([cx + sx*rsd_py2/2, fy + ft + eps, fh/2 + sz*rsd_px2/2])
        rotate([90, 0, 0]) cylinder(d = rsd_insd, h = rsd_insh + 2*eps);
  }
}

// ---- upright component-plate posts (M3 insert in the top) ----
module component_posts() {
  difference() {
    for (p = posts2) translate([p[0], p[1], t - eps]) cylinder(d = post_d2, h = post_h2 + eps);
    for (p = posts2) translate([p[0], p[1], t + post_h2 - post_insh]) cylinder(d = post_insd, h = post_insh + 2*eps);
  }
}

module strong_bottom() {
  union() {
    plate(true);
    rib_lattice();
    if (rsd_on) rsd_ledge();
    component_posts();
  }
}

if (view == "strong") strong_bottom();
