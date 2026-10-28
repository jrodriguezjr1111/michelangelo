/* ======================================================================
   SEAT-RAIL FIXTURE — shared engine (seat_rail_fixture_lib.scad)
   ----------------------------------------------------------------------
   Bench replica of the C172 (N417ER) seat rail AS CURRENTLY MODELLED by
   the VIB-01 family, so the rev E Feather-stack base and the Digiducer
   sidecar can be banded to something rail-shaped on the bench and the
   mounting configuration worked out before the next flight.

   Do NOT set parameters here.  Instance files (rail_seg*.scad) define the
   segment (length, band stations, datum marks, labels) and then
   `include <seat_rail_fixture_lib.scad>`.  The rail PROFILE comes from
   `../digiducer_mount/rail_interface.scad` (the one file the node and the
   sidecar share), so the fixture, the node and the sidecar can never carry
   three different rails.

   WHAT IS MODELLED (every value tagged; see README caliper card):
     head      head_w x rail_head_h  ridge, centred     INFERRED (16-19 wide, 2 tall)
     bearing   W (45) wide flat the 12.5 mm pads sit on INFERRED (= node width; no ledge modelled)
     body      W wide x body_h tall solid under it      FIXTURE ONLY (scene module in the sidecar)
     flange    flange_w x flange_h step                 FIXTURE ONLY (sidecar scene module: 65 x 2)
     holes     Ø hole_d at hole_pitch along the head    INFERRED (seat-stop holes; literature ~3/8 in @ 1 in)
     band path a slot UNDER the bearing surface at each ASSUMPTION — how the band gets round the real
               band station (band loops body + part)   rail is unknown; photo it on N417ER

   Coordinates: x along the rail (0 = aft end of the rail body, +x FWD),
   y across (0 = -Y plate edge), z up from the BED (plate bottom).
   Print: as modelled, plate on the bed.  Only bridges = the band-slot
   crowns (gabled to 5.8, self-supporting).  No support anywhere.
   ====================================================================== */
include <../digiducer_mount/rail_interface.scad>   // W, groove_w, groove_d, rail_head_h, tun_w, tun_h, pad_w (+ asserts)

$fn = 64;
eps = 0.01;

/* ---------------- instance parameters (REQUIRED, set in the instance) --
     part       "seg" | "gauge" | "assembly" | "none"
     seg_label  engraved id
     rail_L     rail body length
     stations   band centrelines x (rail coords)
     datums     [[x, "label"], ...] engraved datum ticks
     hole_x0    first seat-stop hole centre
     fit_parts  [[stl, x_datum, [part band x...], loop_h], ...] for the assembly render
   ---------------------------------------------------------------------- */
assert(!is_undef(part) && !is_undef(seg_label) && !is_undef(rail_L) && !is_undef(stations) &&
       !is_undef(datums) && !is_undef(hole_x0) && !is_undef(fit_parts), "instance file must define part, seg_label, rail_L, stations, datums, hole_x0, fit_parts");

/* ---------------- rail profile (INFERRED, see README) ----------------- */
head_w     = 18.0;      // INFERRED 16-19 -> 18 (1.0 per side in the 20 groove)
head_h     = rail_head_h;                                // 2.0 — the number the node's groove was cut for
body_w     = W;                                          // 45 — the pad bearing surface IS the node width
body_h     = 14.0;      // fixture body above the flange step
flange_w   = 65.0;    // sidecar scene module
flange_h   = 2.0;
hole_d     = 9.5;      // INFERRED seat-stop hole Ø (3/8 in nominal; AD wear limit 0.42 in = 10.7)
hole_pitch = 25.4;  // INFERRED 1 in seat-adjust increment

/* ---------------- band slot under the bearing surface ---------------- */
slot_w     = 16.0;      // part tunnel 10 + +/-3 placement play
slot_h     = 6.0;      // band 0.6 thick, 7.94 wide on edge needs < 1; 6 = fingers
slot_spring = 0.9; // vertical wall before the 45 deg gable
slot_crown = slot_w - 2*(slot_h - slot_spring);          // 5.8 — the printed bridge

/* ---------------- base plate + feet ------------------------------------ */
plate_t    = 4.0;
plate_w    = 84.0;
tab        = 15.0;         // plate beyond each rail end (feet)
foot_d     = 6.5;      // 1/4 in or M6 bench bolt (M4 with a washer)
foot_y     = [8, plate_w - 8];
engrave_d  = 0.6;

/* ---------------- derived ---------------------------------------------- */
yc         = plate_w/2;                                  // rail centreline
z_flange   = plate_t;                                    // flange step top = plate_t + flange_h
z_body0    = plate_t + flange_h;                         // body starts, slot floor
z_bear     = z_body0 + body_h;                           // pad bearing surface (node z = 0 sits here)
z_head     = z_bear + head_h;                            // head top
z_slot1    = z_body0 + slot_h;                           // slot roof crown
above_slot = z_bear - z_slot1;                           // solid body over the band slot
plate_x0   = -tab;  plate_L = rail_L + 2*tab;
holes_x    = [for (x = [hole_x0 : hole_pitch : rail_L - hole_d/2 - 2]) x];
n_holes    = len(holes_x);
loop_node  = 36.4 + above_slot + head_h;                 // rev E closed box (Hb 34 + lid 2.4) + rail section in the loop
loop_perim = 2*(loop_node + body_w);                     // band loop perimeter around node + rail (rectangle, no corner radii)
loop_dia   = loop_perim/PI;
loop_dg    = 2*((18 + above_slot + head_h) + body_w)/PI; // sidecar block seat plane z=18
function nearest_hole(x) = min([for (h = holes_x) abs(h - x)]);
function hole_rel(x) = let(d = nearest_hole(x)) d <= hole_d/2 ? "OVER a hole" : (d >= (hole_d + tun_w)/2 ? "between holes" : "hole edge under the band");
slot_free_x = [for (i = [0:len(stations)-2]) stations[i+1] - stations[i] - slot_w];   // body between slots

echo(str("=== SEAT-RAIL FIXTURE ", seg_label, " — rail ", rail_L, " long, plate ", plate_L, " x ", plate_w, " x ", plate_t, " ==="));
echo(str("PROFILE (from rail_interface.scad): head ", head_w, " x ", head_h, " (groove ", groove_w, " x ", groove_d,
         " -> ", (groove_w - head_w)/2, " per side, ", groove_d - head_h, " over the head); bearing ", body_w,
         " wide (pads 2 x ", pad_w, "); body ", body_w, " x ", body_h, "; flange ", flange_w, " x ", flange_h));
echo(str("Z: plate 0..", plate_t, " | flange ..", z_body0, " | body ..", z_bear, " = PAD PLANE | head ..", z_head,
         " | band slot z ", z_body0, "..", z_slot1, " (", slot_w, " wide, crown ", slot_crown, ") -> ", above_slot, " mm of body in the band loop"));
echo(str("SEAT-STOP HOLES: ", n_holes, " x Ø", hole_d, " at ", hole_pitch, " pitch, x = ", holes_x, " (blind from the head top to the flange step; open into a band slot where one crosses)"));
echo(str("BAND STATIONS x = ", stations, " -> ", [for (s = stations) str(s, ": ", hole_rel(s), " (", round(10*nearest_hole(s))/10, " mm)")]));
echo(str("BAND LOOP around the rev E box + rail: ~", round(loop_node), " x ", body_w, " -> perimeter ", round(loop_perim),
         " -> Ø", round(loop_dia), " mm (SAE #32 1-9/16..2-1/2 in = 40..64 mm; #36 to 70); Digiducer block: Ø", round(loop_dg)));
echo(str("DATUMS: ", datums));
echo(str("MAXSPAN=", slot_crown));
echo(str("UNSUPPORTED SPANS: band-slot crown ", slot_crown, " mm x", len(stations), " (self-supporting <= 6)"));

/* ---------------- failure-mode asserts ---------------------------------- */
assert(plate_L <= 305 && plate_w <= 305, "exceeds bed");
assert(head_w + 2*0.5 <= groove_w, "head will not drop into the node's groove with the house +0.5");
assert(head_h <= groove_d - 0.5, "head taller than the groove — pads would float");
assert(head_w >= 16 && head_w <= 19, "head width outside the 16-19 inferred range the groove was sized for");
assert(slot_crown <= 6.0 && slot_crown > 0, "band-slot crown is a true bridge (> 6) or the gable closes");
assert(slot_w >= tun_w + 2, "band slot narrower than the part tunnel + 2");
assert(slot_h >= 2.0, "band slot will not pass a 0.6 band with fingers");
assert(above_slot >= 6.0, "less than 6 mm of body above the band slot");
assert(flange_w <= plate_w - 2*8, "flange step leaves no clamp lip on the plate");
assert(foot_d/2 + 3 <= tab/2 + eps, "foot hole breaks the plate end");
for (f = slot_free_x) assert(f >= 10, "band slots closer than 10 mm of body between them");
for (s = stations) assert(s - slot_w/2 >= 5 && s + slot_w/2 <= rail_L - 5, "band slot runs off the rail end");
assert(hole_d < body_w - 2*6, "seat-stop hole leaves < 6 mm of body wall each side");
assert(hole_pitch - hole_d >= 8, "seat-stop holes too close");
assert(loop_dia <= 70, "band loop over the node exceeds an SAE #36 band");
assert(plate_t - engrave_d >= 2.0, "engraving cuts the plate too thin");

/* ======================================================================
   geometry
   ====================================================================== */
module slot_2d() {    // local x across the rail -> extruded along y; local y = z above the slot floor
  polygon([[-slot_w/2, -eps], [slot_w/2, -eps], [slot_w/2, slot_spring],
           [slot_crown/2, slot_h], [-slot_crown/2, slot_h], [-slot_w/2, slot_spring]]);
}
module arrow2d(len=10) { polygon([[0,-0.9],[len-3,-0.9],[len-3,-2],[len,0],[len-3,2],[len-3,0.9],[0,0.9]]); }
module labels_2d() {
  /* -Y lip strip (y 0..~7): segment id, FWD arrow, datum ticks + labels */
  translate([2, 1.8]) text(str("CANARY RAIL FIXTURE  ", seg_label), size=3.2, font="Liberation Sans:style=Bold");
  translate([rail_L - 28, 1.6]) text("FWD", size=3.2, font="Liberation Sans:style=Bold");
  translate([rail_L - 14, 3.2]) arrow2d(12);
  for (d = datums) {
    translate([d[0] - 0.5, plate_w - 7.5]) square([1.0, 7.5]);               // tick on the +Y lip, up to the flange step
    translate([d[0] + 1.5, plate_w - 6.2]) text(d[1], size=3.0, font="Liberation Sans:style=Bold");
  }
  /* +Y lip: the honesty line */
  translate([2, plate_w - 6.2]) text("INFERRED PROFILE 2026-10-28 - MEASURE N417ER", size=2.6, font="Liberation Sans:style=Bold");
}

module segment() {
  difference() {
    union() {
      translate([plate_x0, 0, 0]) cube([plate_L, plate_w, plate_t]);                                   // plate
      translate([0, yc - flange_w/2, plate_t - eps]) cube([rail_L, flange_w, flange_h + eps]);         // flange step
      translate([0, yc - body_w/2, z_body0 - eps]) cube([rail_L, body_w, body_h + eps]);               // body (pad bearing on top)
      translate([0, yc - head_w/2, z_bear - eps]) cube([rail_L, head_w, head_h + eps]);                // head ridge
    }
    /* band slots: across the full width, floor on the flange step */
    for (s = stations) translate([s, plate_w + 1, z_body0]) rotate([90, 0, 0]) linear_extrude(plate_w + 2) slot_2d();
    /* seat-stop holes: blind from the head top down to the flange step */
    for (x = holes_x) translate([x, yc, z_body0]) cylinder(d=hole_d, h=body_h + head_h + 1);
    /* feet */
    for (x = [plate_x0 + tab/2, rail_L + tab/2], y = foot_y) translate([x, y, -1]) cylinder(d=foot_d, h=plate_t + 2);
    /* engraving on the plate top (lips) */
    translate([0, 0, plate_t - engrave_d]) linear_extrude(engrave_d + eps) labels_2d();
  }
}

/* ---------------- go/no-go gauge for N417ER ----------------------------
   Flat card, notches on one long edge for the HEAD (width 16 / 18 / 20,
   depth = groove_d) and pins on the other for the SEAT-STOP HOLE
   (Ø 9.0 / 9.5 / 10.0 go, 10.7 = AD wear limit no-go) plus a pitch pair.
   ---------------------------------------------------------------------- */
g_L = 110; g_W = 30; g_T = 5;
g_notch = [16, 18, 20];
g_pins  = [9.0, 9.5, 10.0, 10.7];
g_pin_h = 8;
module gauge() {
  difference() {
    union() {
      cube([g_L, g_W, g_T]);
      for (i = [0:len(g_pins)-1]) translate([10 + i*16, g_W - 6.5, g_T - eps]) cylinder(d=g_pins[i], h=g_pin_h + eps);
      for (k = [0, 1]) translate([g_L - 11 - (1-k)*hole_pitch, g_W - 6.5, g_T - eps]) cylinder(d=8.0, h=g_pin_h + eps);   // pitch pair, 25.4 c-c
    }
    for (i = [0:len(g_notch)-1]) translate([8 + i*30 - g_notch[i]/2, -1, -1]) cube([g_notch[i], groove_d + 1, g_T + 2]);
    translate([0, 0, g_T - engrave_d]) linear_extrude(engrave_d + eps) {
      for (i = [0:len(g_notch)-1]) translate([8 + i*30 - 4, groove_d + 1.5]) text(str(g_notch[i]), size=2.8, font="Liberation Sans:style=Bold");
      for (i = [0:len(g_pins)-1]) translate([10 + i*16 - 4, g_W - 14.5]) text(str(g_pins[i]), size=2.4, font="Liberation Sans:style=Bold");
      translate([g_L - 42, g_W - 14.5]) text(str("PITCH ", hole_pitch), size=2.4, font="Liberation Sans:style=Bold");
      translate([3, 10.5]) text(str("NOTCH ", groove_d, " DEEP = GROOVE"), size=2.4, font="Liberation Sans:style=Bold");
      translate([58, 10.5]) text("N417ER RAIL GAUGE", size=2.6, font="Liberation Sans:style=Bold");
    }
  }
}
echo(str("GAUGE: notches ", g_notch, " x ", groove_d, " deep (head width/height), pins Ø", g_pins,
         " (seat-stop hole go / AD no-go), pitch pair Ø8 at ", hole_pitch, " c-c"));

/* ---------------- scene (render only) ----------------------------------- */
module band(x, screw_side = 1, hgt = loop_node) {   // cosmetic: a 0.6 x 8 ring, floor on the flange step, over the part
  zt = z_bear + hgt;
  color("#c9cbd0") translate([x - 4, 0, 0]) difference() {
    translate([0, yc - body_w/2 - 0.6, z_body0]) cube([8, body_w + 1.2, zt - z_body0 + 0.6]);
    translate([-eps, yc - body_w/2, z_body0 + 0.6]) cube([8 + 2*eps, body_w, zt - z_body0 - 0.6]);
  }
  color("#c9cbd0") translate([x - 6, screw_side > 0 ? yc + body_w/2 + 0.6 : yc - body_w/2 - 8.6, z_bear + 6]) cube([12, 8, 7]);
}

/* ---------------- fit parts for the assembly render -----------------------
   fit_parts = [[stl_path (relative to this dir), x_datum, y_tunnels_from_part_x0...], ...]
   Each entry: the part STL (print orientation = pad plane z 0) placed with its
   aft end at x_datum on the rail; its band centrelines (part coords) for the
   bands drawn around it.  Instances define it; empty = bare rail.          */

/* ================= part selection ================= */
if (part == "seg")   segment();
if (part == "gauge") gauge();
if (part == "assembly") {
  color("#9aa3ad") segment();
  for (p = fit_parts) {
    color("#d9d4c2", 0.9) translate([p[1], yc - body_w/2, z_bear]) import(p[0]);
    for (i = [0:len(p[2])-1]) band(p[1] + p[2][i], i % 2 == 0 ? 1 : -1, p[3]);
  }
}
