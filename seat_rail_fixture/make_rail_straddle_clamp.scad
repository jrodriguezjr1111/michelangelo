/* ======================================================================
   RAIL STRADDLE CLAMP — candidate interface for the PROUD-HEAD seat rail
   (N417ER photo 2026-10-28; profile = rail_interface.scad "photo_2026_10_28")
   ----------------------------------------------------------------------
   The photo kills interface A (pads on a flat + 3 mm groove + bands): the
   head stands ~14 mm proud of a painted flange plate and nothing passes
   under the rail.  This is candidate (a): a three-piece T-rail clamp.

     DECK   a flat slab spanning the head on a bridge; a 1 mm crown PAD on
            its underside bears on the round crown (line contact along the
            rail).  Top face = the mounting deck: the rev E base bolts to
            it through its EXISTING interface-B holes (M4 at x 22 / 93 on
            the centreline), pads flat on the deck.  The Digiducer sidecar
            gets the same deck 48 long with two M4s where its band tunnels
            were.
     JAWS   four short bars (two per side), each with a 45 deg LIP that
            reaches under the head's lip into the undercut.  One vertical
            M4 per jaw, from the deck top (head outboard of the 45 mm node,
            reachable with the node installed), into a heat-set insert in
            the jaw.  Tightening pulls the jaw UP: its lip wedges into the
            undercut, the reaction presses the deck pad DOWN onto the crown.
            The rail head is in compression between pad and lips; the
            flange plate and the carpet are NOT in the load path (jaws
            float 1 mm above the plate).  The 45 deg wedges self-centre the
            deck laterally under preload; rigidity is preload-stiffness, as
            in a vise, not clearance.

   Install: set the deck on the crown, slide each jaw in from its side
   under the deck until the lip enters the undercut, run the four M4s down.
   No sliding on from the rail end, no seat removal; works with a one-
   sided undercut too (then only two jaws clamp, the other side is a
   locating wall) — but the photo shows the undercut on ONE side only, so
   CONFIRM the other before relying on symmetry.

   Candidate (b), not modelled: replace the rail's existing flange bolts
   (end pair / mid-span) with longer ones through a plate.  Those bolts are
   the seat rail's own floor attachment — removing them is maintenance on a
   primary occupant restraint (14 CFR 43, A&P + logbook); NOT assumed.

   Material: ASA for the bench/ground clamp (this print); flight article =
   the same geometry machined 6061 (structures call; lips in plastic creep
   under preload).  Print: deck top face DOWN (flat deck from the first
   layer, the pad and the channel walls rise off it, bridge underside is
   the only flat roof — spans 18, inside MAX_BRIDGE); jaws LIP UP, outer
   face down (the 45 deg lip face is self-supporting).  No support.

   part = "deck" | "jaw" | "all" | "print" | "assembly" | "none"
   deck_L = 100 (rev E) | 48 (sidecar)
   ====================================================================== */
part   = "all";
deck_L = 100;
$fn = 64; eps = 0.01;

include <../digiducer_mount/rail_interface.scad>
assert(rail_profile == "photo_2026_10_28", "the straddle clamp is cut for the photo profile");

/* ---------------- house tolerances ------------------------------------ */
m4_clr = 4.4; m4_ins_od = 6.0; m4_ins_l = 8.0; m4_bore_d = 5.6;  m4_head_d = 7.6; m4_head_h = 2.2;  // M4 x 8 long heat-set insert (OD 6.0) + BUTTON head ISO 7380 (VERIFY stock)
cb_h = m4_head_h + 0.3;   // heads fully recessed: they sit under the node's pads
clr_flank = 1.0;       // channel wall to the head flank
clr_crown = 1.0;       // bridge underside over the crown (the PAD closes it to 0)
clr_lip   = 0.3;       // lip face below the head lip underside before preload
clr_web   = 2.0;       // lip tip to the web (a 45 deg undercut leaves only ~2 mm of lip height at web + 1)
jaw_float = 1.0;       // jaw bottom above the flange plate (plate NOT in the load path)

/* ---------------- geometry (y from the rail CL, z from the FLANGE PLATE top) */
hw  = ph_head_w/2;   ww = ph_web_w/2;
ch_hw   = hw + clr_flank;                        // channel half-width 9
z_br    = ph_head_h + clr_crown;                 // bridge underside 15
pad_h   = clr_crown;                             // crown pad reaches the crown
deck_t  = 8.0;                                   // bridge/deck thickness; jaw bolts pass through (counterbored), interface-B inserts seat in it
z_deck  = z_br + deck_t;                         // deck top 23 = the node's pad plane
deck_W  = 56.0;                                  // deck width: outboard bolt heads clear the 45 node
jaw_in  = ww + clr_web;                          // lip tip 5
jaw_out = deck_W/2;                              // jaw outer face 28
jaw_L   = deck_L == 100 ? 30.0 : 16.0;           // per jaw, along the rail
jaw_top = z_br - 0.5;                            // 0.5 under the bridge: the LIP must touch first
lip_z_tip = ph_lip_z - (hw - jaw_in)*tan(ph_lip_angle) - clr_lip;   // lip face z at the tip (y = jaw_in)
lip_z_out = ph_lip_z - clr_lip;                                     // lip face z at the head edge (y = hw)
bolt_y  = (ch_hw + jaw_out)/2 + 2;               // 20.5: under the node's pad edge (|y| <= 22.5) -> heads fully counterbored; clamp is torqued BEFORE the node goes on
jaw_x   = deck_L == 100 ? [15, 85] : [10, 38];   // rev E deck | sidecar deck (its old band stations)
ifB_x   = deck_L == 100 ? [22, 93] : [10, 38];   // rev E interface-B holes | sidecar's old band stations become M4s
ifB_ins = true;                                  // M4 heat-set inserts in the deck for the node's interface-B bolts
jaw_h   = jaw_top - jaw_float;                   // 13.5
jaw_bore_l = jaw_h - 1.5;                        // insert bore from the top, 1.5 floor
bolt_len = 18;                                   // M4 x 18 stock: through the deck 8, 0.5 gap, 8 insert, 1.5 spare
engage   = min(bolt_len - deck_t - 0.5, m4_ins_l);

/* ---------------- masses (solid, ASA 1.07 / 6061 2.70) --------------------- */
deck_vol = deck_L*(deck_W*deck_t + 6*pad_h);
jaw_vol  = jaw_L*((jaw_out-ch_hw)*jaw_h + (ch_hw-jaw_in)*(lip_z_out + lip_z_tip)/2);
mass = [deck_vol/1000*1.07, 4*jaw_vol/1000*1.07, deck_vol/1000*2.70, 4*jaw_vol/1000*2.70];
hw_mass = 4*1.6 + 4*0.6 + (ifB_ins ? 2*0.6 : 0);   // M4x16 button ~1.6 g, insert ~0.6

echo(str("=== RAIL STRADDLE CLAMP, deck ", deck_L, " long, profile photo_2026_10_28 (PROVISIONAL) ==="));
echo(str("CHANNEL: half-width ", ch_hw, " (head ", hw, " + ", clr_flank, "), bridge underside z ", z_br, " (crown ", ph_head_h, " + ", clr_crown,
         "), crown PAD ", pad_h, " proud -> bears on the crown; deck top z ", z_deck, " = node pad plane; deck ", deck_W, " wide"));
echo(str("JAWS: 4 x ", jaw_L, " long at x ", jaw_x, " (+/- ", jaw_L/2, "), y ", ch_hw, "..", jaw_out, " each side, height ", jaw_h,
         " (top ", jaw_top, " = ", z_br - jaw_top, " under the bridge, bottom ", jaw_float, " above the plate); lip tip at y ", jaw_in,
         " (web ", ww, " + ", clr_web, "), lip face z ", round(100*lip_z_tip)/100, " (tip) .. ", lip_z_out, " (head edge) = head lip underside - ", clr_lip));
echo(str("BOLTS: 4 x M4 x ", bolt_len, " button head in a Ø", m4_head_d + 0.6, " x ", cb_h, " counterbore (flush: the heads sit under the node pads, |y| ", bolt_y - m4_head_d/2, "..", bolt_y + m4_head_d/2, " vs pad edge 22.5 -> torque the clamp BEFORE the node goes on), into M4 inserts in the jaws (bore Ø", m4_bore_d, " x ", jaw_bore_l,
         "), engagement ", engage, " = ", engage/4, " x D; node interface-B M4s at x ", ifB_x, " on the CL into deck inserts (deck ", deck_t, " thick)"));
echo(str("LOAD PATH: bolt tension -> jaw lip UP into the undercut (45 deg wedge, self-centring) -> head -> crown pad DOWN -> deck. ",
         "Flange plate + carpet OUT of the path (jaws float ", jaw_float, "). Lateral stiffness = wedge preload, not clearance."));
echo(str("MASS (solid): deck ", round(mass[0]), " g ASA / ", round(mass[2]), " g 6061; 4 jaws ", round(mass[1]), " g ASA / ", round(mass[3]),
         " g 6061; hardware ~", round(hw_mass), " g -> clamp ~", round(mass[0]+mass[1]+hw_mass), " g ASA on top of the 65 g rev E enclosure (W&B; the 70 g gate is the enclosure only)"));
echo(str("UNCERTAINTY DRIVERS: head_h +/-4 moves z_deck; head_w +/-3 moves the channel and lip reach; lip angle (45 assumed, flat likely) RE-CUTS the lip; ",
         "web +/-3 moves the lip tip. None of this is final until the caliper card is filled."));
MAX_BRIDGE = 20.0;
echo(str("MAXSPAN=", 2*ch_hw));
echo(str("UNSUPPORTED SPANS: bridge underside over the channel ", 2*ch_hw, " mm (deck printed top-face DOWN: that roof is a TRUE BRIDGE, <= ", MAX_BRIDGE, ")"));

/* ---------------- asserts ------------------------------------------------- */
assert(2*ch_hw <= MAX_BRIDGE, "channel roof exceeds MAX_BRIDGE");
assert(lip_z_tip >= jaw_float + 1.0, "lip tip would reach below the jaw float — no undercut to engage (head_t vs lip angle)");
assert(lip_z_out > lip_z_tip, "lip face is not a rising wedge");
assert(jaw_top < z_br, "jaw top touches the bridge before the lip engages");
assert(jaw_bore_l >= m4_ins_l + 0.5, "jaw too short for the M4 insert + floor");
assert(engage >= 1.5*4, "M4 engagement under 1.5 D");
assert(bolt_y - m4_head_d/2 >= ch_hw + 0.5 && bolt_y + m4_head_d/2 <= jaw_out - 0.5, "bolt head off the jaw");
assert(deck_t - cb_h >= 4.0, "counterbore leaves < 4 mm of deck under the jaw-bolt heads");
assert(deck_W <= ph_flange_w - 2*2, "deck wider than the flange plate (jaws would hang over carpet)");
ifB_ins_l = 5.7;   // the deck takes the SHORT M4 insert (5.7) for interface B: 8 deck - 5.7 - 0.3 floor
assert(deck_t - ifB_ins_l - 0.3 >= 1.5, "deck too thin for the interface-B inserts");
assert(jaw_bore_l - m4_ins_l >= 0.5 && bolt_len - deck_t - 0.5 <= jaw_bore_l - 0.5, "jaw bolt bottoms out in the bore");
for (x = jaw_x) assert(x - jaw_L/2 >= 0 && x + jaw_L/2 <= deck_L, "jaw off the deck end");
for (x = ifB_x) for (j = jaw_x) assert(true);   // CL vs |y|>9: no geometric conflict by construction

/* ---------------- geometry --------------------------------------------------- */
module deck() {           // modelled in place (deck top at z_deck); print = top face down
  difference() {
    union() {
      translate([0, -deck_W/2, z_br]) cube([deck_L, deck_W, deck_t]);
      translate([0, -3, z_br - pad_h]) cube([deck_L, 6, pad_h + eps]);                     // crown pad: 6 wide strip on the CL
    }
    for (x = jaw_x, s = [-1, 1]) {                                                          // jaw bolts: through the deck, counterbored 1 mm
      translate([x, s*bolt_y, z_br - 1]) cylinder(d = m4_clr, h = deck_t + 2);
      translate([x, s*bolt_y, z_deck - cb_h]) cylinder(d = m4_head_d + 0.6, h = cb_h + 1);
    }
    for (x = ifB_x) translate([x, 0, z_br - 1]) cylinder(d = ifB_ins ? m4_bore_d : m4_clr, h = deck_t + 2);   // node interface-B
    translate([deck_L - 14, -deck_W/2 + 1.5, z_deck - 0.6]) linear_extrude(1) text("FWD", size = 3, font = "Liberation Sans:style=Bold");
  }
}
module jaw(len = jaw_L) {   // +Y jaw, modelled in place; -Y = mirror
  difference() {
    union() {
      translate([-len/2, ch_hw, jaw_float]) cube([len, jaw_out - ch_hw, jaw_h]);            // body outboard of the channel wall
      /* lip: from the channel wall inward to the tip, 45 deg top face under the head lip */
      translate([-len/2, 0, 0]) rotate([90, 0, 90]) linear_extrude(len)
        polygon([[jaw_in, jaw_float], [ch_hw + eps, jaw_float], [ch_hw + eps, lip_z_out + (ch_hw - hw)*tan(ph_lip_angle)],
                 [hw, lip_z_out], [jaw_in, lip_z_tip]]);
    }
    translate([0, bolt_y, jaw_top - jaw_bore_l]) cylinder(d = m4_bore_d, h = jaw_bore_l + 1);   // M4 insert bore from the top
  }
}
module jaws() { for (x = jaw_x, s = [-1, 1]) translate([x, 0, 0]) mirror([0, s < 0 ? 1 : 0, 0]) jaw(); }

module rail_scene(L = deck_L + 40, x0 = -20) {
  color("#b8bcc2") translate([x0, 0, 0]) rotate([90, 0, 90]) linear_extrude(L) rail_section_2d();
  color("#d9cfae") translate([x0, -ph_flange_w/2, -ph_flange_t]) cube([L, ph_flange_w, ph_flange_t]);
}
module bolts() { color("#555") for (x = jaw_x, s = [-1, 1]) translate([x, s*bolt_y, z_deck - cb_h]) { cylinder(d = m4_head_d, h = m4_head_h); translate([0,0,-bolt_len]) cylinder(d = 4, h = bolt_len); } }

if (part == "deck") deck();
if (part == "jaw")  jaw();
if (part == "all")  { deck(); jaws(); }
module jaw_print_pose() {   // outer face (y = jaw_out) on the bed, lip up: rotate -90 about x maps y -> -z
  translate([0, 0, jaw_out]) rotate([-90, 0, 0]) jaw();
}
if (part == "print") {                                        // deck top-face down; jaws on their outer faces
  translate([0, 0, z_deck]) mirror([0, 0, 1]) deck();
  for (i = [0:3]) translate([jaw_L/2 + i*(jaw_L + 6), deck_W/2 + 8, 0]) jaw_print_pose();
}
if (part == "assembly") { rail_scene(); color("#a9b4c2") deck(); color("#8fa3b8") jaws(); bolts();
  color("#d9d4c2", 0.85) translate([0, -22.5, z_deck]) import("../vib01_node/vib01e_base.stl"); }
