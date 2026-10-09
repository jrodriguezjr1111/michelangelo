// ============================================================================
// canary_unit_web.scad — EXTERIOR-ONLY massing of the as-built Canary flight unit
// for the public website renders (2026-10-08).  NOT a part, NOT printable intent.
//
// Disclosure posture (hard rule): exterior form only.  No wiring, boards,
// connectors, sensor placement, aircraft mounting, battery brand, part numbers,
// dimensions or text other than the optional etched CANARY wordmark on the deck.
// The interior between the levels is an opaque mask block (`interior_mask`), so
// nothing inside the frame exists in the model at all.
//
// Geometry basis: Javi's photos 2026-10-08 (nine views, described) + the
// project-fledge "AS BUILT 2026-09-27" / "CAGE RE-ARRANGED 2026-10-07" blocks:
// two-level black 2020 frame ~406 x 279 footprint, ~270 tall; printed corner
// gussets + hex-vented side plates on the long faces (t1_sideplates family look);
// flat top deck with the fan-cooled compute case and the white GNSS dome on a
// short pedestal near one end; V-mount style battery block hanging on the far end.
//
// part = "all" | "body" | "dome" | "ledbar"   (render_web.py exports the three colour groups)
// wordmark = true | false                      (etched CANARY on the deck, the only text)
// ============================================================================
part = "all";
wordmark = true;

// ---- frame (2020 extrusion, two levels) ------------------------------------
FL = 406;  DP = 279;  E = 20;                 // footprint, rail section
RZ = [0, 120, 250];                           // deck / mid / top rail bottoms
H  = RZ[2] + E;                               // 270 overall frame height
PLATE_T = 5;  GUS_T = 3.2;  GUS = 56;         // printed plates / gussets
DECK_T = 4;   DECK_IN = 2;  DECK_CH = 8;      // top deck plate
// hex vent cell (stylised; the real t1_sideplates cell is 5.0 AF / 1.6 web)
HEX_AF = 8.0; HEX_WEB = 2.5; HEX_R = HEX_AF / sqrt(3);   // coarsened from the house 5.0/1.6 cell so the vents read as line art at web size
// top-deck payload
CASE = [160, 120, 56]; CASE_C = [130, DP / 2]; CASE_CH = 3;     // compute case (plain box + fan grille)
GRILLE = 70; GRILLE_D = 62; HUB_D = 22;
DOME_D = 110; DOME_C = [FL - 76, DP / 2]; PED_D = 50; PED_H = 18; PED_BASE = 90;
// battery block on the -X end face
BAT = [45, 95, 150]; BAT_Z0 = 70; VPLATE = [6, 100, 150];
// LED bar: a strip let into the deck's front long edge (amber only in the variant)
LED = [FL - 40, 5, 3];
// etched wordmark
WM_W = 130; WM_DEPTH = 0.8; WM_C = [CASE_C[0], 40];

ZT = H + DECK_T;                              // deck top
PLATE_W = FL - 2 * (GUS + 6);                 // plates sit between the gussets
echo(str("WEB RENDER ENVELOPE: frame ", FL, " x ", DP, " x ", H, " | deck top z ", ZT,
         " | dome top z ", ZT + PED_H + 4 + DOME_D / 2, " | battery x ", -VPLATE[0] - BAT[0], "..0",
         " | overall ", FL + VPLATE[0] + BAT[0], " x ", DP, " x ", ZT + PED_H + 4 + DOME_D / 2));
assert(PLATE_W >= 240, "side plates too narrow between the gussets");
assert(DOME_C[0] + DOME_D / 2 <= FL - DECK_IN && DOME_C[0] - DOME_D / 2 >= CASE_C[0] + CASE[0] / 2 + 10, "dome overlaps the deck edge or the case");
assert(CASE_C[1] - CASE[1] / 2 >= WM_C[1] + 12, "wordmark under the case");
assert(BAT_Z0 >= 0 && BAT_Z0 + BAT[2] <= ZT, "battery outside the end face");
assert(LED[0] <= FL - 2 * DECK_CH - 4, "LED bar runs into the deck chamfers");

C_DARK = [0.16, 0.16, 0.18]; C_LIGHT = [0.93, 0.94, 0.96]; C_WHITE = [0.98, 0.98, 0.97]; C_AMBER = [0.886, 0.604, 0.122];

module rail_x(z, y) translate([0, y, z]) cube([FL, E, E]);
module rail_y(z, x) translate([x, E, z]) cube([E, DP - 2 * E, E]);
module post(x, y) translate([x, y, 0]) cube([E, E, H]);
module frame() {
  for (z = RZ) { rail_x(z, 0); rail_x(z, DP - E); rail_y(z, 0); rail_y(z, FL - E); }
  for (x = [0, FL - E], y = [0, DP - E]) post(x, y);
}
// flat corner / T gussets on both long faces (y = -t face and y = DP face)
module gussets_face(y) for (m = [0, 1]) translate([m * FL, y, 0]) mirror([m, 0, 0]) rotate([90, 0, 0])   // extrudes toward -Y: proud of the face at y
  linear_extrude(GUS_T) {
    polygon([[0, 0], [GUS, 0], [GUS, E], [E + 2, GUS + 4], [0, GUS + 4]]);
    polygon([[0, RZ[1] - 36], [E, RZ[1] - 36], [GUS, RZ[1]], [GUS, RZ[1] + E], [E, RZ[1] + E + 36], [0, RZ[1] + E + 36]]);
    polygon([[0, H], [GUS, H], [GUS, H - E], [E + 2, H - GUS - 4], [0, H - GUS - 4]]);
  }
module gussets() { gussets_face(0); translate([0, DP + GUS_T, 0]) gussets_face(0); }

// hex-vented side plate: u along the face, v up; field inside a border, over the bay only
module hex_field(w, v0, v1, border = 7) {
  px = HEX_AF + HEX_WEB; py = px * sqrt(3) / 2; m = HEX_R + HEX_WEB / 2;
  nu = floor((w - 2 * border - 2 * m) / px); nv = floor((v1 - v0 - 2 * border - 2 * m) / py);
  u0 = (w - nu * px) / 2; vv0 = (v0 + v1) / 2 - nv * py / 2;
  for (j = [0 : nv], i = [0 : nu - 1 - (j % 2)]) translate([u0 + (i + (j % 2) / 2) * px + px / 2, vv0 + j * py]) rotate(30) circle(r = HEX_R, $fn = 6);
}
module plate2d(w, h, ch = 6) polygon([[ch, 0], [w - ch, 0], [w, ch], [w, h - ch], [w - ch, h], [ch, h], [0, h - ch], [0, ch]]);
module side_plate(row) {                        // row 1: deck->mid, row 2: mid->top ; plate covers half of each shared rail
  z0 = RZ[row - 1] + E / 2 - 6; z1 = RZ[row] + E / 2 + 6;
  bay0 = RZ[row - 1] + E; bay1 = RZ[row];
  linear_extrude(PLATE_T) translate([0, z0]) difference() {           // plate sits ON the rail faces, proud by PLATE_T
    plate2d(PLATE_W, z1 - z0);
    translate([0, -z0]) hex_field(PLATE_W, bay0, bay1);
  }
}
module side_plates() for (face = [0, 1], row = [1, 2])
  translate(face == 0 ? [(FL - PLATE_W) / 2, 0, 0] : [(FL + PLATE_W) / 2, DP, 0]) rotate([90, 0, face == 0 ? 0 : 180]) side_plate(row);   // extrusion runs outward (-Y front, +Y back)

// opaque mask: the interior is a closed grey volume, nothing inside is modelled
module interior_mask() translate([E + 2, E + 2, E]) cube([FL - 2 * E - 4, DP - 2 * E - 4, RZ[2] - E]);

module wordmark2d() resize([WM_W, 0], auto = true) import("../t1_panels/brand/canary-wordmark.svg", center = true);
module deck() difference() {
  translate([DECK_IN, DECK_IN, H]) linear_extrude(DECK_T) plate2d(FL - 2 * DECK_IN, DP - 2 * DECK_IN, DECK_CH);
  translate([FL / 2 - LED[0] / 2, DECK_IN - 0.01, ZT - LED[2]]) cube([LED[0], LED[1] + 0.01, LED[2] + 0.01]);          // LED bar groove
  if (wordmark) translate([WM_C[0], WM_C[1], ZT - WM_DEPTH]) linear_extrude(WM_DEPTH + 0.01) wordmark2d();
}
module ledbar() translate([FL / 2 - LED[0] / 2, DECK_IN, ZT - LED[2]]) cube([LED[0], LED[1], LED[2]]);

module chamfered_box(s, ch) hull() for (dz = [ch, s[2] - ch]) translate([ch, ch, dz]) linear_extrude(0.01) offset(delta = ch, chamfer = true) square([s[0] - 2 * ch, s[1] - 2 * ch]);
module compute_case() translate([CASE_C[0] - CASE[0] / 2, CASE_C[1] - CASE[1] / 2, ZT]) difference() {
  chamfered_box(CASE, CASE_CH);
  gx = CASE[0] / 2; gy = CASE[1] / 2; zt = CASE[2];
  translate([gx - GRILLE / 2, gy - GRILLE / 2, zt - 1.5]) cube([GRILLE, GRILLE, 2]);                 // square grille recess
  translate([gx, gy, zt - 7]) difference() { cylinder(d = GRILLE_D, h = 8, $fn = 72); translate([0, 0, 0]) cylinder(d = HUB_D, h = 2, $fn = 48); }  // fan opening, hub boss stays
  translate([0, 0, zt - 12]) difference() { translate([-1, -1, 0]) cube([CASE[0] + 2, CASE[1] + 2, 1]); translate([0.8, 0.8, -1]) cube([CASE[0] - 1.6, CASE[1] - 1.6, 3]); }   // lid parting line
}
module pedestal() translate([DOME_C[0], DOME_C[1], ZT]) {
  translate([-PED_BASE / 2, -PED_BASE / 2, 0]) chamfered_box([PED_BASE, PED_BASE, 4], 1.5);
  translate([0, 0, 4]) cylinder(d = PED_D, h = PED_H, $fn = 64);
}
module dome() translate([DOME_C[0], DOME_C[1], ZT + 4 + PED_H]) intersection() { sphere(d = DOME_D, $fn = 96); translate([-DOME_D, -DOME_D, 0]) cube(2 * DOME_D); }

module battery() {
  translate([-VPLATE[0], DP / 2 - VPLATE[1] / 2, BAT_Z0]) chamfered_box(VPLATE, 1.5);
  translate([-VPLATE[0] - BAT[0], DP / 2 - BAT[1] / 2, BAT_Z0]) chamfered_box(BAT, 3);
}

module body() { frame(); gussets(); side_plates(); interior_mask(); deck(); compute_case(); pedestal(); battery(); }

if (part == "all" || part == "body") color(part == "all" ? C_DARK : C_LIGHT) body();
if (part == "all" || part == "dome") color(C_WHITE) dome();
if (part == "all" || part == "ledbar") color(C_AMBER) ledbar();
