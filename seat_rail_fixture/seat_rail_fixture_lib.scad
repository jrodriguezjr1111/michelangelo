/* ======================================================================
   SEAT-RAIL FIXTURE — shared engine (seat_rail_fixture_lib.scad)
   ----------------------------------------------------------------------
   Bench replica of the N417ER (C172) seat rail so the rev E Feather-stack
   base and the Digiducer sidecar can be mounted to something rail-shaped
   before the next flight.  The rail PROFILE comes from
   `../digiducer_mount/rail_interface.scad` (the one file the node and the
   sidecar share) and its `rail_profile` switch:

     "photo_2026_10_28"  PROVISIONAL, from Javi's photo (reference/):
                         round-top head ~14 proud of a painted flange plate,
                         undercut lip over a web, hex flange bolts, no band
                         path, no seat-stop holes seen.  The fixture is the
                         flange plate + the rail section + the bolt heads.
                         Mounting = make_rail_straddle_clamp.scad (jaws in
                         the undercut), so there are NO band slots.
     "inferred_2026_08"  the falsified rev B..E rail (2 mm head on a flat,
                         bands under the body) — kept selectable so the two
                         bench replicas can be compared.

   Do NOT set parameters here.  Instance files (rail_seg*.scad) define the
   segment layout and then `include <seat_rail_fixture_lib.scad>`:
     part       "seg" | "gauge" | "assembly" | "none"
     seg_label  engraved id
     rail_L     rail length
     datums     [[x, "label"], ...] engraved ticks on the +Y lip
     fit_parts  [[stl, x_datum, [clamp-jaw x...], jaw_len, loop_h], ...]
                (photo profile: jaw footprints are checked against the
                flange bolt heads; inferred profile: band stations)
     stations   band centrelines (inferred profile only)
     hole_x0    first seat-stop hole (inferred profile only)
     bolt_x_mid optional: override the mid-span bolt x within its +/- 30

   Coordinates: x along the rail (0 = aft end, +x FWD), y across (0 = -Y
   plate edge), z up from the BED (plate bottom).  Print as modelled, plate
   on the bed; the head's 45 deg lip undersides are self-supporting, the
   round crown prints as a dome.  No support.
   ====================================================================== */
include <../digiducer_mount/rail_interface.scad>

$fn = 64;
eps = 0.01;
assert(!is_undef(part) && !is_undef(seg_label) && !is_undef(rail_L) && !is_undef(datums) && !is_undef(fit_parts),
       "instance file must define part, seg_label, rail_L, datums, fit_parts");
photo = (rail_profile == "photo_2026_10_28");
stations_i = is_undef(stations) ? [] : stations;
hole_x0_i  = is_undef(hole_x0)  ? 10.7 : hole_x0;
bolt_mid_x = is_undef(bolt_x_mid) ? ph_bolt_mid[0][0] : bolt_x_mid;

/* ---------------- base plate + feet (both profiles) ---------------------- */
plate_t    = 4.0;
plate_w    = 84.0;
tab        = 15.0;        // plate beyond each rail end (feet)
foot_d     = 6.5;         // 1/4 in or M6 bench bolt (M4 with a washer)
foot_y     = [8, plate_w - 8];
engrave_d  = 0.6;
yc         = plate_w/2;
plate_x0   = -tab;  plate_L = rail_L + 2*tab;

/* ================= PHOTO PROFILE (provisional) =========================== */
z_fl0   = plate_t;                         // flange plate bottom
z_fl1   = plate_t + ph_flange_t;           // flange plate top = profile z 0
z_crown = z_fl1 + ph_head_h;               // 20
z_lip   = z_fl1 + ph_lip_z;                // lip underside at the head edge
bolt_pos = concat([for (b = ph_bolt_end) [b[0], b[1]]], [[bolt_mid_x, ph_bolt_mid[0][1]]]);   // [x, y from CL]
bolt_hd  = ph_bolt_af/cos(30);             // hex corner diameter
/* a jaw footprint [x0, x1] at |y| 9..28 (both sides) must not land on a bolt head */
function jaw_hits(x0, x1) = [for (b = bolt_pos) if (b[0] + bolt_hd/2 > x0 && b[0] - bolt_hd/2 < x1 && abs(b[1]) + bolt_hd/2 > 9 && abs(b[1]) - bolt_hd/2 < 28) b];
jaw_checks = photo ? [for (p = fit_parts) for (jx = p[2]) [p[0], p[1] + jx - p[3]/2, p[1] + jx + p[3]/2, jaw_hits(p[1] + jx - p[3]/2, p[1] + jx + p[3]/2)]] : [];

/* ================= INFERRED PROFILE (comparison) ========================= */
head_w_i = 18.0;  body_h_i = 14.0;  flange_w_i = 65.0;  flange_h_i = 2.0;  hole_d_i = 9.5;  hole_pitch_i = 25.4;
slot_w = 16.0;  slot_h = 6.0;  slot_spring = 0.9;  slot_crown = slot_w - 2*(slot_h - slot_spring);
z_body0_i = plate_t + flange_h_i;  z_bear_i = z_body0_i + body_h_i;  z_head_i = z_bear_i + rail_head_h;  z_slot1_i = z_body0_i + slot_h;
holes_x_i = photo ? [] : [for (x = [hole_x0_i : hole_pitch_i : rail_L - hole_d_i/2 - 2]) x];

/* ================= echoes ================================================== */
echo(str("=== SEAT-RAIL FIXTURE ", seg_label, " — profile ", rail_profile, ", rail ", rail_L, " long, plate ", plate_L, " x ", plate_w, " x ", plate_t, " ==="));
if (photo) {
  echo(str("Z: plate 0..", plate_t, " | flange plate ..", z_fl1, " (= profile z 0) | lip underside ", z_lip, " | crown ", z_crown,
           " | head ", ph_head_w, " wide, web ", ph_web_w, ", undercut ", ph_undercut, " @ ", ph_lip_angle, " deg | flange plate ", ph_flange_w, " wide"));
  echo(str("FLANGE BOLTS (hex ", ph_bolt_af, " AF x ", ph_bolt_hh, ") at [x, y from CL] ", bolt_pos, " (mid-span x ", bolt_mid_x, " of ", ph_bolt_mid[0][0], " +/- 30); head bar starts at x ", ph_head_setback, " (set-back, web only before it)"));
  echo(str("CLAMP STATIONS vs BOLT HEADS: ", [for (c = jaw_checks) str(c[0], " jaw x ", c[1], "..", c[2], len(c[3]) ? str(" *** HITS bolt ", c[3]) : " clear")]));
  echo(str("DATUMS: ", datums));
  echo("MAXSPAN=0");
  echo("UNSUPPORTED SPANS: none (lip undersides 45 deg, crown is a dome)");
} else {
  echo(str("Z: plate 0..", plate_t, " | flange ..", z_body0_i, " | body ..", z_bear_i, " = PAD PLANE | head ..", z_head_i,
           " | band slot z ", z_body0_i, "..", z_slot1_i, " (", slot_w, " wide, crown ", slot_crown, ")"));
  echo(str("SEAT-STOP HOLES: ", len(holes_x_i), " x Ø", hole_d_i, " at ", hole_pitch_i, " pitch, x = ", holes_x_i));
  echo(str("BAND STATIONS x = ", stations_i));
  echo(str("DATUMS: ", datums));
  echo(str("MAXSPAN=", slot_crown));
  echo(str("UNSUPPORTED SPANS: band-slot crown ", slot_crown, " mm x", len(stations_i), " (self-supporting <= 6)"));
}

/* ================= asserts ================================================== */
assert(plate_L <= 305 && plate_w <= 305, "exceeds bed");
assert(foot_d/2 + 3 <= tab/2 + eps, "foot hole breaks the plate end");
assert(plate_t - engrave_d >= 2.0, "engraving cuts the plate too thin");
if (photo) {
  assert(ph_flange_w <= plate_w - 2*8, "flange plate leaves no clamp lip on the base plate");
  for (b = bolt_pos) assert(b[0] - bolt_hd/2 >= 0 && b[0] + bolt_hd/2 <= rail_L && abs(b[1]) + bolt_hd/2 <= ph_flange_w/2, "flange bolt off the flange plate");
  for (b = bolt_pos) assert(b[0] + bolt_hd/2 <= ph_head_setback - 1 || abs(b[1]) - bolt_hd/2 >= ph_head_w/2 + 0.5, "flange bolt head under the rail head (and not in the head set-back)");
  for (p = fit_parts) assert(p[1] >= ph_head_setback, "fit part datum inside the head set-back — the clamp pad has no crown there");
  for (c = jaw_checks) assert(len(c[3]) == 0, str("clamp jaw of ", c[0], " at x ", c[1], "..", c[2], " lands on a flange bolt head ", c[3], " — move the datum"));
  for (p = fit_parts) assert(p[1] >= 0 && p[1] + max(p[2]) + p[3]/2 <= rail_L, "fit part runs off the rail");
} else {
  assert(slot_crown <= 6.0 && slot_crown > 0, "band-slot crown is a true bridge (> 6) or the gable closes");
  for (s = stations_i) assert(s - slot_w/2 >= 5 && s + slot_w/2 <= rail_L - 5, "band slot runs off the rail end");
}

/* ================= geometry ================================================ */
module arrow2d(len=10) { polygon([[0,-0.9],[len-3,-0.9],[len-3,-2],[len,0],[len-3,2],[len-3,0.9],[0,0.9]]); }
module hexprism(af, h) { cylinder(d = af/cos(30), h = h, $fn = 6); }
module labels_2d() {
  translate([2, 1.8]) text(str("CANARY RAIL FIXTURE  ", seg_label), size=3.2, font="Liberation Sans:style=Bold");
  translate([rail_L - 28, 1.6]) text("FWD", size=3.2, font="Liberation Sans:style=Bold");
  translate([rail_L - 14, 3.2]) arrow2d(12);
  for (d = datums) {
    translate([d[0] - 0.5, plate_w - 7.5]) square([1.0, 7.5]);
    translate([d[0] + 1.5, plate_w - 6.2]) text(d[1], size=3.0, font="Liberation Sans:style=Bold");
  }
  translate([2, plate_w - 6.2]) text(photo ? "PROVISIONAL PROFILE (PHOTO 2026-10-28) - MEASURE N417ER" : "INFERRED PROFILE 2026-08 - FALSIFIED 2026-10-28",
                                     size=2.6, font="Liberation Sans:style=Bold");
}
module plate_and_feet() {
  difference() {
    translate([plate_x0, 0, 0]) cube([plate_L, plate_w, plate_t]);
    for (x = [plate_x0 + tab/2, rail_L + tab/2], y = foot_y) translate([x, y, -1]) cylinder(d=foot_d, h=plate_t + 2);
    translate([0, 0, plate_t - engrave_d]) linear_extrude(engrave_d + eps) labels_2d();
  }
}
module rail_photo() {
  translate([0, yc - ph_flange_w/2, z_fl0 - eps]) cube([rail_L, ph_flange_w, ph_flange_t + eps]);          // painted flange plate
  translate([ph_head_setback, yc, z_fl1 - eps]) rotate([90, 0, 90]) linear_extrude(rail_L - ph_head_setback) rail_section_2d();   // head + web
  translate([0, yc - ph_web_w/2, z_fl1 - eps]) cube([ph_head_setback + eps, ph_web_w, ph_lip_z + eps]);                      // web only in the set-back
  for (b = bolt_pos) translate([b[0], yc + b[1], z_fl1 - eps]) hexprism(ph_bolt_af, ph_bolt_hh + eps);       // flange bolt heads
}
module slot_2d() {
  polygon([[-slot_w/2, -eps], [slot_w/2, -eps], [slot_w/2, slot_spring], [slot_crown/2, slot_h], [-slot_crown/2, slot_h], [-slot_w/2, slot_spring]]);
}
module rail_inferred() {
  difference() {
    union() {
      translate([0, yc - flange_w_i/2, plate_t - eps]) cube([rail_L, flange_w_i, flange_h_i + eps]);
      translate([0, yc - W/2, z_body0_i - eps]) cube([rail_L, W, body_h_i + eps]);
      translate([0, yc - head_w_i/2, z_bear_i - eps]) cube([rail_L, head_w_i, rail_head_h + eps]);
    }
    for (s = stations_i) translate([s, plate_w + 1, z_body0_i]) rotate([90, 0, 0]) linear_extrude(plate_w + 2) slot_2d();
    for (x = holes_x_i) translate([x, yc, z_body0_i]) cylinder(d=hole_d_i, h=body_h_i + rail_head_h + 1);
  }
}
module segment() { plate_and_feet(); if (photo) rail_photo(); else rail_inferred(); }

/* ---------------- gauge: the caliper card as a part ---------------------------
   Photo profile: head WIDTH notches (13 / 16 / 19, 12 deep so they drop over the
   crown), HEIGHT ladder (steps 10 / 14 / 18 above the card edge: stand the card
   on the flange plate beside the head, read which step the crown reaches),
   UNDERCUT feelers (tabs 2 / 4 / 6 wide x 2 thick to slide under the lip), bolt
   head notches (9.5 / 11.1 AF), and the hole pins kept (Ø9.5 go / 10.7 no-go)
   for seat-stop holes found elsewhere.                                          */
g_L = 130; g_W = 40; g_T = 5;
g_notch = [13, 16, 19];  g_notch_d = 12;
g_steps = [10, 14, 18];
g_feel  = [2, 4, 6];
g_bolt  = [9.5, 11.1];
g_pins  = [9.5, 10.7];  g_pin_h = 8;
module gauge() {
  difference() {
    union() {
      cube([g_L, g_W, g_T]);
      for (i = [0:len(g_steps)-1]) translate([g_L - 36 + i*11, g_W - eps, 0]) cube([10, g_steps[i], g_T]);          // height ladder off the +Y edge
      for (i = [0:len(g_feel)-1]) translate([g_L - eps, 6 + i*10, 0]) cube([10, g_feel[i], 2.0]);                   // undercut feelers off the +X end
      for (i = [0:len(g_pins)-1]) translate([g_L - 60 + i*16, g_W - 8, g_T - eps]) cylinder(d=g_pins[i], h=g_pin_h + eps);
    }
    for (i = [0:len(g_notch)-1]) translate([12 + i*28 - g_notch[i]/2, -1, -1]) cube([g_notch[i], g_notch_d + 1, g_T + 2]);   // head-width notches
    for (i = [0:len(g_bolt)-1]) translate([-1, 14 + i*12, -1]) cube([6, g_bolt[i], g_T + 2]);                                // bolt AF notches off the -X end
    translate([0, 0, g_T - engrave_d]) linear_extrude(engrave_d + eps) {
      for (i = [0:len(g_notch)-1]) translate([12 + i*28 - 4, g_notch_d + 1.5]) text(str(g_notch[i]), size=2.8, font="Liberation Sans:style=Bold");
      for (i = [0:len(g_steps)-1]) translate([g_L - 36 + i*11, g_W - 4.5]) text(str(g_steps[i]), size=2.4, font="Liberation Sans:style=Bold");
      for (i = [0:len(g_feel)-1]) translate([g_L - 8, 6 + i*10]) text(str(g_feel[i]), size=2.2, font="Liberation Sans:style=Bold");
      for (i = [0:len(g_bolt)-1]) translate([7, 14 + i*12 + 1]) text(str(g_bolt[i]), size=2.2, font="Liberation Sans:style=Bold");
      for (i = [0:len(g_pins)-1]) translate([g_L - 60 + i*16 - 4, g_W - 15]) text(str(g_pins[i]), size=2.2, font="Liberation Sans:style=Bold");
      translate([16, 20]) text("v HEAD WIDTH notches", size=2.4, font="Liberation Sans:style=Bold");
      translate([16, 26]) text("UNDERCUT feelers ->", size=2.4, font="Liberation Sans:style=Bold");
      translate([16, 32]) text("HEIGHT ladder ^  BOLT AF <-", size=2.4, font="Liberation Sans:style=Bold");
      translate([82, 5]) text("N417ER RAIL GAUGE v2", size=3.0, font="Liberation Sans:style=Bold");
    }
  }
}
echo(str("GAUGE v2: width notches ", g_notch, " x ", g_notch_d, " deep; height ladder ", g_steps, "; undercut feelers ", g_feel,
         " x 2 thick; bolt AF ", g_bolt, "; hole pins Ø", g_pins));

/* ---------------- scene (render only) ----------------------------------------- */
module band(x, screw_side = 1, hgt) {   // inferred profile only
  zt = z_bear_i + hgt;
  color("#c9cbd0") translate([x - 4, 0, 0]) difference() {
    translate([0, yc - W/2 - 0.6, z_body0_i]) cube([8, W + 1.2, zt - z_body0_i + 0.6]);
    translate([-eps, yc - W/2, z_body0_i + 0.6]) cube([8 + 2*eps, W, zt - z_body0_i - 0.6]);
  }
}

/* ================= part selection ================================================ */
if (part == "seg")   segment();
if (part == "gauge") gauge();
if (part == "assembly") {
  color("#9aa3ad") segment();
  for (p = fit_parts) {
    if (photo) {
      /* the straddle clamp under the part: deck + jaws from make_rail_straddle_clamp.scad, rendered via its print STLs */
      color("#a9b4c2") translate([p[1], yc, z_fl1]) import(p[5]);                       // clamp "all" STL (deck + jaws, modelled in place)
      color("#d9d4c2", 0.9) translate([p[1], yc - W/2, z_fl1 + p[6]]) import(p[0]);  // part on the deck
    } else {
      color("#d9d4c2", 0.9) translate([p[1], yc - W/2, z_bear_i]) import(p[0]);
      for (i = [0:len(p[2])-1]) band(p[1] + p[2][i], i % 2 == 0 ? 1 : -1, p[4]);
    }
  }
}
