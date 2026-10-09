// ============================================================================
// canary_unit_cutout.scad — the web massing (canary_unit_web.scad) with ONE long-side plate
// re-cut as the CANARY stencil + a thin diffuser panel behind it (2026-10-09 render variant B).
//
// Same disclosure posture as the base: exterior only.  Behind the letters there is ONLY the
// diffuser panel (rendered as a flat dark panel when the LED is off, emissive amber when on);
// the interior stays the opaque mask block — no internals exist in the model.
//
// grp = "all" | "body" | "dome" | "diffuser"   (render_cutout.py exports the three colour groups;
//                                               the deck LED bar is folded into "body", unlit)
// Letterforms: the house wordmark vector (../t1_panels/brand/canary-wordmark.svg), the same geometry
// as the etched deck wordmark, resized to CO_WM_W.  The house glyphs are single closed outlines —
// the A and R are open forms with NO enclosed counters — so no stencil ties are needed; none are added.
// ============================================================================
include <canary_unit_web.scad>
part = "none";            // silence the base file's top-level output; this file selects by grp
grp = "all";

CO_FACE = 0;  CO_ROW = 2;                         // the -Y (hero-facing) long face, upper vented row
CO_WM_W = 254;  CO_BORDER = 12;                   // letter span across the plate (plate is PLATE_W wide)
CO_SKIN = 0.8;  CO_REB_M = 6;                     // rebate from the BACK around the letter band leaves this skin at the letters (the real
                                                  // cut-out plate does the same: 5 mm front, 3.2 rebate = 1.8 skin) — a 5 mm-deep stencil
                                                  // wall hides ~70 % of a 5 mm stroke at the hero angle (57 deg off-normal); 0.8 mm ~25 %.
                                                  // RENDER value: a printed skin would be 1.2-1.8 (3-4 layers) — see README
DIFF_T = 2;                                       // diffuser panel seated in the rebate, flush behind the skin
// Imported house vector, measured after resize([254, 0]): bbox x -127..127, y 18.198..45.656 (2026-10-09, openscad 2026.06.10).
// import(center = true) centres the SVG viewBox ("0 -32 256 40"), NOT the glyphs, so the glyph band sits +0.1257 x width above
// the origin and is 0.1081 x width tall.  Everything below anchors to the measured glyph bbox, not to the origin.
WM_ASPECT = 254 / 27.457;                         // width / glyph height
WM_CY = 31.927 / 254;                             // glyph-band centre offset (fraction of width) left by center = true

CO_CAP = CO_WM_W / WM_ASPECT;
CO_BAY = [RZ[CO_ROW - 1] + E, RZ[CO_ROW]];
CO_REB = [CO_WM_W + 2 * CO_REB_M, CO_CAP + 2 * CO_REB_M];
CO_C = [PLATE_W / 2, (CO_BAY[0] + CO_BAY[1]) / 2];      // letter band centre: u, absolute z
echo(str("CUTOUT PLATE: plate ", PLATE_W, " wide x ", RZ[CO_ROW] + E / 2 + 6 - (RZ[CO_ROW - 1] + E / 2 - 6), " tall | letters ", CO_WM_W,
         " x ~", CO_CAP, " cap, one line, centred in the ", CO_BAY[1] - CO_BAY[0], " bay | rebate ", CO_REB[0], " x ", CO_REB[1], " x ",
         PLATE_T - CO_SKIN, " deep, skin ", CO_SKIN, " | diffuser ", CO_REB[0] - 0.6, " x ", CO_REB[1] - 0.6, " x ", DIFF_T, " in the rebate"));
assert(CO_WM_W + 2 * CO_BORDER <= PLATE_W, "letters run into the plate border");
assert(CO_REB[1] + 2 * 8 <= CO_BAY[1] - CO_BAY[0], "rebate reaches the rails (letters must sit between them)");
assert(DIFF_T + 0.3 <= PLATE_T - CO_SKIN, "diffuser thicker than the rebate");

module co_wordmark2d() translate([0, -WM_CY * CO_WM_W]) resize([CO_WM_W, 0], auto = true) import("../t1_panels/brand/canary-wordmark.svg", center = true);   // glyph bbox centred on the origin
module cutout_plate(row) difference() {           // same frame as side_plate(row): u along the face, v = absolute z, local +z outward
  z0 = RZ[row - 1] + E / 2 - 6; z1 = RZ[row] + E / 2 + 6;
  linear_extrude(PLATE_T) translate([0, z0]) difference() {
    plate2d(PLATE_W, z1 - z0);
    translate([PLATE_W / 2, CO_C[1] - z0]) co_wordmark2d();
  }
  translate([CO_C[0] - CO_REB[0] / 2, CO_C[1] - CO_REB[1] / 2, -1]) cube([CO_REB[0], CO_REB[1], PLATE_T - CO_SKIN + 1]);   // rebate from the back
}
module diffuser_local() translate([CO_C[0] - CO_REB[0] / 2 + 0.3, CO_C[1] - CO_REB[1] / 2 + 0.3, PLATE_T - CO_SKIN - DIFF_T])
  cube([CO_REB[0] - 0.6, CO_REB[1] - 0.6, DIFF_T]);
module place_face(face) translate(face == 0 ? [(FL - PLATE_W) / 2, 0, 0] : [(FL + PLATE_W) / 2, DP, 0]) rotate([90, 0, face == 0 ? 0 : 180]) children();
module side_plates_co() for (face = [0, 1], row = [1, 2]) place_face(face) { if (face == CO_FACE && row == CO_ROW) cutout_plate(row); else side_plate(row); }
module diffuser() place_face(CO_FACE) diffuser_local();
module body_co() { frame(); gussets(); side_plates_co(); interior_mask(); deck(); compute_case(); pedestal(); battery(); ledbar(); }

if (grp == "all" || grp == "body") color(grp == "all" ? C_DARK : C_LIGHT) body_co();
if (grp == "all" || grp == "dome") color(C_WHITE) dome();
if (grp == "all" || grp == "diffuser") color([1.0, 0.76, 0.28]) diffuser();
