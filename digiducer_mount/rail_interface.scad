/* ======================================================================
   SEAT-RAIL INTERFACE — shared parameter block (VIB-01 rev D family)
   ----------------------------------------------------------------------
   Every value here is a COPY of make_vib01_revD.scad's underside block.
   Both parts must sit on the same N417ER seat rail with the same contact
   geometry, so these numbers may only change TOGETHER:

     build_digiducer_sidecar.py --check-rail   (runs on every build)

   greps make_vib01_revD.scad and fails if any value below differs from
   the node's.  When the N417ER rail is finally measured, edit the node
   first, then this file; the check tells you if you forgot one.  The
   cleaner end state is vib01 rev E doing `include <../digiducer_mount/
   rail_interface.scad>` — out of scope for the sidecar task (touches
   vib01_node/).

   INFERRED (vib01 rev D, 2026-08-20): rail head 16-19 wide, ~2 tall.
   Contact surfaces are the two 12.5 mm PADS (z = 0) and the GROOVE SIDE
   WALLS; the groove and tunnel ROOFS never touch anything, so their
   shape may differ by material: gabled (45 deg) for FDM bridging, flat
   for a milled block.
   ====================================================================== */
W           = 45;      // body width across the rail
slab        = 6.0;     // slab thickness; pads z=0 .. slab top z=6
groove_w    = 20.0;    // INFERRED — VERIFY on N417ER (rail head 16-19 wide)
groove_d    = 3.0;
rail_head_h = 2.0;     // INFERRED — rail head height inside the groove
tun_w       = 10.0;    // passes a 5/16 in (7.94) wide "mini" worm-drive band; pick the
                       // clamp DIAMETER from the measured block+rail loop (see sidecar echo)
tun_h       = 3.0;
tun_spring  = 0.9;     // vertical wall = band thickness envelope (band ~0.6)

groove_gable = groove_d - rail_head_h;        // 45 deg: run = rise
groove_crown = groove_w - 2*groove_gable;     // the printed bridge (18)
tun_crown    = tun_w - 2*(tun_h - tun_spring); // the printed bridge (5.8)
pad_w        = (W - groove_w)/2;              // 12.5 contact pads

/* 2-D profiles, verbatim from make_vib01_revD.scad; `gabled=false` gives
   the flat-roof machining variant with identical contact surfaces.
   tunnel_2d: local x = across the rail, local y = z.
   groove_2d: local x = z, local y = lateral.                            */
module tunnel_2d(gabled = true) {
  if (gabled)
    polygon([[-tun_w/2, -1], [tun_w/2, -1],
             [ tun_w/2, tun_spring], [ tun_crown/2, tun_h],
             [-tun_crown/2, tun_h], [-tun_w/2, tun_spring]]);
  else
    polygon([[-tun_w/2, -1], [tun_w/2, -1], [tun_w/2, tun_h], [-tun_w/2, tun_h]]);
}
module groove_2d(gabled = true) {
  if (gabled)
    polygon([[-1, -groove_w/2], [-1, groove_w/2],
             [groove_d-groove_gable, groove_w/2], [groove_d, groove_crown/2],
             [groove_d, -groove_crown/2], [groove_d-groove_gable, -groove_w/2]]);
  else
    polygon([[-1, -groove_w/2], [-1, groove_w/2],
             [groove_d, groove_w/2], [groove_d, -groove_w/2]]);
}


/* ======================================================================
   RAIL PROFILE SWITCH (2026-10-28)
   ----------------------------------------------------------------------
   rail_profile = "inferred_2026_08"  the numbers above: a 2 mm head proud of
                                      a 45-wide flat the pads sit on, banded
                                      (rev B..E, sidecar) — FALSIFIED by the
                                      2026-10-28 photo, kept for comparison
                = "photo_2026_10_28"  PROVISIONAL, from Javi's photo of the
                                      N417ER rail beside the rev D box
                                      (seat_rail_fixture/reference/
                                      N417ER_rail_and_node_2026-10-28.webp)

   What the photo shows (scale: 45 mm box width, ~10 mm hex bolt heads):
   a ROUND-TOP aluminium bar standing clearly proud of the floor on a wide
   flat painted flange plate; carpet cut around the plate; the plate
   fastened with hex-head bolts — a pair across the rail at its end and a
   single one mid-span on one side; a dark undercut band along one side of
   the head (lip over a narrower web); NO daylight under the rail (no band
   path); NO seat-stop holes on this stretch of head.  Every number below is
   a photo estimate with its +/- ; nothing is measured.  The old pad-on-flat
   + 3 mm groove + band interface cannot work on this rail: see
   seat_rail_fixture/make_rail_straddle_clamp.scad for the candidate.
   ====================================================================== */
rail_profile = "photo_2026_10_28";

/* --- photo profile, z from the FLANGE PLATE TOP, y from the rail centreline --- */
ph_head_w    = 16.0;   // +/- 3   head width (the round bar)
ph_head_h    = 14.0;   // +/- 4   flange-plate top -> crown
ph_head_t    = 9.0;    // +/- 3   head thickness: lip underside -> crown
ph_head_r    = 8.0;    // +/- 3   crown radius (looks fully round-topped: r = w/2)
ph_web_w     = 8.0;    // +/- 3   web under the head
ph_lip_angle = 45;     // +/- 45  lip underside: 45 deg assumed (printable); flat is likely — MEASURE
ph_flange_w  = 63.0;   // +/- 8   painted flange plate, carpet cut around it
ph_flange_t  = 2.0;    // +/- 1   not visible edge-on; thin sheet assumed
ph_bolt_af   = 9.5;    // +/- 1.5 hex head across flats (AN3-class 3/8 in; AN4 = 11.1)
ph_bolt_hh   = 4.0;    // +/- 1   head height
ph_bolt_end  = [[6, -12], [6, 12]];   // +/- 3 / +/- 3   end pair: x from the plate end, y from the rail CL
ph_bolt_mid  = [[150, 15]];           // +/- 30 / +/- 4  single mid-span bolt, +Y side only (as photographed)
ph_head_setback = 18.0;  // +/- 6   the round head bar ENDS this far before the flange-plate end; the end-pair bolts sit in that clear stretch (web only)
ph_lip_z     = ph_head_h - ph_head_t;                 // 5: flange top -> lip underside
ph_undercut  = (ph_head_w - ph_web_w)/2;              // 4 per side (seen on one side; CONFIRM the other)

/* 2-D cross-section of the photo profile (x = y across the rail, y = z above the flange top).
   Round crown, straight flanks, lip underside at ph_lip_angle from horizontal down to the web. */
module rail_section_2d() {
  hw = ph_head_w/2; ww = ph_web_w/2;
  r  = min(ph_head_r, hw);
  zc = ph_head_h - r;                                 // crown circle centre
  lip_drop = ph_undercut * tan(ph_lip_angle);         // lip underside falls this much toward the web
  union() {
    intersection() {                                  // round crown, CLIPPED at the lip underside (never below the lips)
      translate([0, zc]) circle(r = r, $fn = 64);
      translate([-hw - 1, ph_lip_z]) square([2*hw + 2, 2*r + 1]);
    }
    polygon([[-hw, ph_lip_z], [hw, ph_lip_z], [hw, max(zc, ph_lip_z)], [-hw, max(zc, ph_lip_z)]]);   // straight flanks
    polygon([[-hw, ph_lip_z], [hw, ph_lip_z], [ww, max(ph_lip_z - lip_drop, 0)], [-ww, max(ph_lip_z - lip_drop, 0)]]);   // lips (undercut)
    polygon([[-ww, -0.01], [ww, -0.01], [ww, ph_lip_z + 0.01], [-ww, ph_lip_z + 0.01]]);                                 // web
  }
}
if (rail_profile == "photo_2026_10_28") {
  echo(str("RAIL PROFILE = photo_2026_10_28 (PROVISIONAL): head ", ph_head_w, " wide x ", ph_head_h, " above the flange plate, crown r ",
           ph_head_r, ", head ", ph_head_t, " thick -> lip underside at z ", ph_lip_z, ", web ", ph_web_w, " -> undercut ", ph_undercut,
           " per side at ", ph_lip_angle, " deg; flange plate ", ph_flange_w, " x ", ph_flange_t, "; bolts hex ", ph_bolt_af, " AF x ", ph_bolt_hh,
           " at ", ph_bolt_end, " (end pair) + ", ph_bolt_mid, " (mid-span); head bar set back ", ph_head_setback, " from the plate end. NO band path, NO seat-stop holes seen."));
  echo("*** INTERFACE A (pads + 3 mm groove + band tunnels) IS INVALID on this profile: the head stands ~14 mm proud and nothing passes under the rail ***");
  assert(ph_head_h - ph_head_t >= 2.0, "photo profile: lip underside too close to the flange for any hook/jaw");
  assert(ph_undercut >= 0, "photo profile: web wider than the head");
} else {
  echo("RAIL PROFILE = inferred_2026_08 (FALSIFIED 2026-10-28 — comparison only)");
}

/* rail-interface sanity (same gates as the node) */
assert(slab - tun_h >= 3.0, "tunnel roof web < 3 mm");
assert(slab - groove_d >= 2.5, "slab web above rail groove too thin");
assert(groove_w <= 25 && pad_w >= 12, "pad/groove geometry out of spec");
assert(groove_gable >= 0, "groove gable would cut into the rail head clearance");
assert(groove_d - groove_gable >= rail_head_h, "groove gable starts below the rail head");
assert(tun_w >= 9.0, "tunnel too narrow to pass a 5/16 in (7.94 mm) clamp band");
assert(tun_crown > 0 && tun_spring < tun_h, "tunnel has no gable");
