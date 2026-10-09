// ============================================================================
// CANARY T1 CAGE — TACTICAL FACE PLATE TEMPLATE            (t1_faceplate family)
// 2026-09-22 · concept D (80/20 20-2020 black frame) · a panel that fills a
// clear opening w x h between 20-series members, measured face-to-face.
//
//   faceplate(w, h, mount, sides, neighbour, vent, ...)
//
//   mount = "bolt"  FLIGHT variant.  Flange overlaps each member face by 10 mm
//                   (half the 20 mm member: the neighbouring plate owns the
//                   other half), bolt EARS reach 18.5 over the member on the
//                   slot centreline, counterbored flush for M5 BHCS into
//                   DROP-IN T-nuts -> the plate comes off without touching the
//                   frame (R1).  A 6 mm PLUG enters the opening so the members
//                   take shear in bearing and the bolts only clamp (R6.6).
//   mount = "slot"  FIT-CHECK variant.  5.6 mm tongues on two opposite edges
//                   slide into the 6.0 slots (Z-direction track, like the
//                   cartridges).  Not retained in +Z: bench use only.
//
// Every feature earns its place (owner's brief: "military tough and tactical"):
//   45 deg outer bezel      = bed-side chamfer, self-supporting, no supports
//   castellated flange      = the bolt ears + the notches that receive the
//                             neighbour's ears (two plates share one mullion)
//   perimeter rib + X rib   = stiffness on the back, 1.6 = 2 x 0.4 walls/side
//   hex / louver field      = airflow, open area echoed in cm2 (R4.2 >= 32)
//   label seat              = the coupon's dovetail pocket, yellow snap-in
//                             plate (R7.3 / R8), geometry = make_style_coupon
//   grip notch              = a real finger scallop on the open edge
//   Reticle Delta           = brand, inlaid 0.6 (never raised: face is on the bed)
//   NO fake bolts, NO cosmetic-only features.
//
// PRINT: flat, FACE DOWN (face = z 0 on the bed -> smooth bed finish outside).
// Every face-side recess (label seat, counterbores, mark) is therefore a short
// roof: MAXSPAN is echoed for the slice harness (R6.3).  Ears/notches/bezel/
// grip are chamfered at the bed edge = 45 deg overhangs.  No islands.
// Material: ASA for anything that flies (R6.1); PLA for the fit check only.
//
// Frame convention inside the module: VIEW coordinates (x right, y up as seen
// from OUTSIDE the box, z into the plate); the exported part is mirrored in x
// so the STL lands face-down in print orientation with the mark/label reading
// correctly from outside.
// ============================================================================
include <../t1_mark.scad>
use <../make_style_coupon.scad>          // plate(txt): the canonical yellow label plate
$fn = 48;

// ------------------------------------------------------------ instance params
part = "plate";              // "plate" | "label" | "set" (plate + label, coloured)
w = 84;                      // clear opening WIDTH, member face to member face
h = 100;                     // clear opening HEIGHT (concept D front bay: DZ - 2E = 100)
mount = "bolt";              // "bolt" (flight) | "slot" (fit check)
sides = [0, 1, 1, 1];        // member behind [top, right, bottom, left]  (D bays: top open)
neighbour = [0, 1, 0, 1];    // another plate shares that member -> notches interleave its ears
vent = "hex";                // "hex" | "louver" | "none"
vent_min_cm2 = 0;            // R4.2: set 32 where this face is the intake or the exhaust
grip = "top";                // "top" | "bottom" | "left" | "right" | "none"
label = true;                // dovetail seat for the snap-in label plate
label_txt = "SPARE";
mark = true;                 // Reticle Delta inlay (auto-off when it does not fit)
slot_edges = "lr";           // mount="slot": tongues on left/right ("lr") or top/bottom ("tb")

// ------------------------------------------------------------ house numbers
NOZ = 0.4;  LAY = 0.2;
E = 20;  SLT = 6.0;  SLD = 6.0;        // 20-2020 member, slot opening, slot depth (t1_tkey_detail.scad)
OV = 10;                               // flange overlap per member face = half the member
EAR_OV = 18.5;                         // bolt ear reaches 18.5 of the 20 (1.5 left for the neighbour's edge)
EAR_L = 16;  NOTCH_L = EAR_L + 2;      // ear along the member; notch = ear + 1.0 clearance per side
C_INS = 12;                            // first/last bolt slot inset from the opening corner
BOLT_PMAX = 60;                        // bolts per side = max(2, ceil(span / 60))
T_FACE = 4.0;                          // field skin, 20 layers
T_FL = 7.0;                            // flange = 3.0 counterbore + 4.0 under the head (R6.2)
T_BACK = 13.0;                         // back plane: flange + 6.0 plug / tongue at member mid-depth (10)
PLUG_D = T_BACK - T_FL;  PLUG_CLR = 0.25;   // plug into the opening, +0.5 total = slide-in house clearance
RIB_W = 1.6;                           // 4 lines: 2 x 0.4 walls each side, no infill
CHAM = 2.0;                            // outer bezel, 45 deg at the bed edge
M5B = 5.4;  CB_D = 10.0;  CB_H = 3.0;  // M5 clearance (house 3.4 / 4.4 / 5.4); BHCS head 9.5 x 2.75 -> flush
CB_FLAT = 8.0;                         // counterbore roof: 1.0 flat ring then a 45 deg cone to the bore
BOLT_L = 16;  NUT_T = 4.5;             // M5 x 16 BHCS; drop-in T-nut thread height (EST: verify on the nut)
TNG_T = SLT - 0.4;  TNG_D = SLD - 1.0;  TNG_LEAD = 1.0;   // slot tongue: 5.6 thick, 5.0 engaged, 1.0 lead
LP_W = 44;  LP_H = 11;  LP_T = 1.8;  LP_CLR = 0.15;  LIP = 0.6;   // == make_style_coupon.scad label plate
LP_PAD = 1.0;                          // back pad behind the seat -> 3.0 web, same as the coupon
FIELD_M = 4;                           // vent field inset from the opening edge (rib inner face is at 1.85)
HEX_AF = 5.0;  HEX_WEB = 1.6;          // hex across flats (no fingertip passes) / web (4 lines)
LV_H = 6.0;  LV_P = 12.0;              // louver slats: 6 tall on a 12 pitch (t1_concepts louver())
VENT_MARGIN = 0.6;                     // vent-to-rib clearance beyond the rib's own 0.8 half-width
GRIP_W = 24;  GRIP_D = 7;              // finger scallop
MARK_D = 12;  MARK_DEP = 0.6;

// ------------------------------------------------------------ exported for wrappers (use <> exports functions, not variables)
function fp_label_y(h) = -h/2 + FIELD_M + 1 + LP_H/2;   // label seat centre (view coords)
function fp_t_back() = T_BACK;
function fp_t_fl() = T_FL;
function fp_lp_t() = LP_T;

// ------------------------------------------------------------ small helpers
function ovs(sd, i) = sd[i] ? OV : 0;
function side_len(W, H, i) = (i == 0 || i == 2) ? W : H;
function srot(i) = i == 0 ? 90 : i == 1 ? 0 : i == 2 ? -90 : 180;          // +X -> outward
function sp(W, H, i, s, d) = i == 0 ? [s, H/2 + d] : i == 1 ? [W/2 + d, s]
                            : i == 2 ? [s, -H/2 - d] : [-W/2 - d, s];       // point on side i
function par(i) = (i == 0 || i == 1) ? 1 : 0;   // ear slot parity: top/right odd, bottom/left even
                                                // (180-deg symmetric: any plate meshes with any plate)
function nb(L) = max(2, ceil((L - 2*C_INS) / BOLT_PMAX));
function nslots(L, inter) = inter ? 2*nb(L) : nb(L);
function spitch(L, inter) = (L - 2*C_INS) / nslots(L, inter);
function spos(L, inter, k) = -L/2 + C_INS + (k + 0.5) * spitch(L, inter);
function ear_pos(L, i, inter) = [for (k = [0 : nslots(L, inter) - 1]) if (!inter || k % 2 == par(i)) spos(L, inter, k)];
function notch_pos(L, i) = [for (k = [0 : nslots(L, true) - 1]) if (k % 2 != par(i)) spos(L, true, k)];
function grip_i(g) = g == "top" ? 0 : g == "right" ? 1 : g == "bottom" ? 2 : g == "left" ? 3 : -1;
function dseg(p, a, b) =                                             // point-to-segment distance
  let (ab = b - a, t = max(0, min(1, ((p - a) * ab) / max(1e-9, ab * ab)))) norm(p - (a + t * ab));
function dline(p, dir) = abs(p[0]*dir[1] - p[1]*dir[0]) / norm(dir);   // point-to-line through origin
function flat(l) = [for (a = l) each a];
function cut1(s, e) = (e[0] >= s[1] || e[1] <= s[0]) ? [s]
                      : concat(s[0] < e[0] ? [[s[0], e[0]]] : [], e[1] < s[1] ? [[e[1], s[1]]] : []);
function cutall(segs, ex) = len(ex) == 0 ? segs : cutall(flat([for (s = segs) cut1(s, ex[0])]), [for (j = [1 : 1 : len(ex) - 1]) ex[j]]);

module cham_prism(zt, ch = CHAM) {           // convex 2D child -> prism with a 45 deg bed-edge chamfer
  hull() { linear_extrude(0.01) offset(delta = -ch) children();
           translate([0, 0, ch]) linear_extrude(zt - ch) children(); }
}
module rcham_cutter(zt, ch = CHAM) {         // convex 2D child -> cutter that is WIDER at the bed: 45 deg over ch, then vertical
  hull() { translate([0, 0, -1]) linear_extrude(0.01) offset(delta = ch + 1) children();      // (hulling the whole prism would
           translate([0, 0, ch]) linear_extrude(0.01) children(); }                          //  taper it end to end)
  translate([0, 0, ch - 0.01]) linear_extrude(zt - ch + 1.01) children();
}
module dovetail(w, h, t, lip) {              // wider at z=0: the coupon's seat / plate profile
  hull() { linear_extrude(0.01) square([w + 2*lip, h + 2*lip], center = true);
           translate([0, 0, lip]) linear_extrude(t - lip) square([w, h], center = true); }
}

// ============================================================ the face plate
module faceplate(w = w, h = h, mount = mount, sides = sides, neighbour = neighbour, vent = vent,
                 vent_min_cm2 = vent_min_cm2, grip = grip, label = label, mark = mark,
                 slot_edges = slot_edges, name = "") {
  bolt = mount == "bolt";
  sd = bolt ? sides : [0, 0, 0, 0];
  nbr = bolt ? neighbour : [0, 0, 0, 0];
  gi = grip_i(grip);
  // ---- plug (view coords, centred on the opening); slot variant: the plate IS the plug
  pc = [for (i = [0 : 3]) (bolt ? (sd[i] ? PLUG_CLR : 0) : PLUG_CLR)];
  px0 = -w/2 + pc[3];  px1 = w/2 - pc[1];  py0 = -h/2 + pc[2];  py1 = h/2 - pc[0];
  // ---- outline: flange over the members (bolt) or the plug itself (slot)
  x0 = bolt ? -w/2 - ovs(sd, 3) : px0;  x1 = bolt ? w/2 + ovs(sd, 1) : px1;
  y0 = bolt ? -h/2 - ovs(sd, 2) : py0;  y1 = bolt ? h/2 + ovs(sd, 0) : py1;
  OW = x1 - x0;  OH = y1 - y0;
  // ---- features
  lab = [0, fp_label_y(h)];                                      // label seat centre
  lab_fw = LP_W + 2*LP_CLR + 2*LIP;  lab_fh = LP_H + 2*LP_CLR + 2*LIP;   // seat footprint at the deep end
  mk = [w/2 - FIELD_M - MARK_D/2 - 1, h/2 - FIELD_M - MARK_D/2 - 1];
  mark_ok = mark && (gi != 0 || mk[0] - MARK_D/2 >= GRIP_W/2 + 1) && (w >= LP_W + 2*FIELD_M + 4);
  gA = gi < 0 ? [0, 0] : sp(w, h, gi, -(GRIP_W/2 - GRIP_D), 0);   // grip stadium end centres, on the outline edge
  gB = gi < 0 ? [0, 0] : sp(w, h, gi, +(GRIP_W/2 - GRIP_D), 0);
  gA2 = gi < 0 ? gA : gA + [ovs(sd, gi) * cos(srot(gi)), ovs(sd, gi) * sin(srot(gi))];   // (bolt: on the flange edge)
  gB2 = gi < 0 ? gB : gB + [ovs(sd, gi) * cos(srot(gi)), ovs(sd, gi) * sin(srot(gi))];
  // ---- vent zone: inside the field, above the label band, minus the grip band
  vz = [-w/2 + FIELD_M, w/2 - FIELD_M,
        -h/2 + FIELD_M + (label ? 1 + LP_H + 2 : 0), h/2 - FIELD_M];
  function excl(p, r) =                                          // true when a vent element (centre p, radius r) must go
       dline(p, [w, h]) < r + RIB_W/2 + VENT_MARGIN
    || dline(p, [w, -h]) < r + RIB_W/2 + VENT_MARGIN
    || (label && abs(p[0] - lab[0]) < lab_fw/2 + r + 1.5 && abs(p[1] - lab[1]) < lab_fh/2 + r + 1.5)
    || (mark_ok && norm(p - mk) < MARK_D/2 + r + 1.5)
    || (gi >= 0 && dseg(p, gA2, gB2) < GRIP_D + r + 1.5);
  // hex cells
  hr = HEX_AF / sqrt(3);  hpx = HEX_AF + HEX_WEB;  hpy = hpx * sqrt(3) / 2;
  hex_c = vent == "hex" ? [for (j = [-40 : 40], i = [-40 : 40])
            let (c = [(vz[0] + vz[1])/2 + i*hpx + (abs(j) % 2) * hpx/2, (vz[2] + vz[3])/2 + j*hpy])
            if (c[0] >= vz[0] + hr && c[0] <= vz[1] - hr && c[1] >= vz[2] + hr && c[1] <= vz[3] - hr && !excl(c, hr)) c] : [];
  hex_cm2 = len(hex_c) * (HEX_AF * HEX_AF * sqrt(3) / 2) / 100;
  // louver rows -> segments (x intervals) outside every exclusion
  phi = atan2(h, w);
  le = (RIB_W/2 + VENT_MARGIN + LV_H/2 * cos(phi)) / sin(phi);   // half-exclusion along x where a slat meets a diagonal
  nrow = vent == "louver" ? max(0, floor((vz[3] - vz[2] - LV_H) / LV_P) + 1) : 0;
  function row_y(j) = (vz[2] + vz[3])/2 - (nrow - 1) * LV_P/2 + j * LV_P;
  function row_ex(y) = concat(
    [[-y*w/h - le, -y*w/h + le], [y*w/h - le, y*w/h + le]],
    (label && abs(y - lab[1]) < lab_fh/2 + LV_H/2 + 1.5) ? [[lab[0] - lab_fw/2 - 1.5, lab[0] + lab_fw/2 + 1.5]] : [],
    (mark_ok && abs(y - mk[1]) < MARK_D/2 + LV_H/2 + 1.5) ? [[mk[0] - MARK_D/2 - 1.5, mk[0] + MARK_D/2 + 1.5]] : [],
    (gi == 0 || gi == 2) && abs(y - (gi == 0 ? h/2 : -h/2)) < GRIP_D + LV_H/2 + 1.5 ? [[-GRIP_W/2 - 1.5, GRIP_W/2 + 1.5]] : [],
    (gi == 1 && abs(y) < GRIP_W/2 + LV_H/2 + 1.5) ? [[w/2 - GRIP_D - 1.5, w]] : [],
    (gi == 3 && abs(y) < GRIP_W/2 + LV_H/2 + 1.5) ? [[-w, -w/2 + GRIP_D + 1.5]] : []);
  lv = nrow == 0 ? [] : [for (j = [0 : nrow - 1]) let (y = row_y(j))
          for (s = cutall([[vz[0], vz[1]]], row_ex(y))) if (s[1] - s[0] >= LV_H + 2) [s[0], s[1], y]];
  lv_cm2 = len(lv) == 0 ? 0 : (sum_len(lv) - len(lv) * LV_H) * LV_H / 100 + len(lv) * PI * (LV_H/2) * (LV_H/2) / 100;
  function sum_len(l, i = 0) = i >= len(l) ? 0 : (l[i][1] - l[i][0]) + sum_len(l, i + 1);
  open_cm2 = vent == "hex" ? hex_cm2 : vent == "louver" ? lv_cm2 : 0;
  // ---- bolts
  ears = bolt ? [for (i = [0 : 3]) if (sd[i]) for (s = ear_pos(side_len(w, h, i), i, nbr[i])) [i, s]] : [];
  notches = bolt ? [for (i = [0 : 3]) if (sd[i] && nbr[i]) for (s = notch_pos(side_len(w, h, i), i)) [i, s]] : [];
  shank_past_face = BOLT_L - (T_FL - CB_H);          // shank beyond the member face (head sits on the cb floor)
  engage = min(NUT_T, shank_past_face - SLD);          // thread in the T-nut (nut face at the slot floor)
  maxspan = max(label ? lab_fh : 0, bolt ? CB_D : 0, mark_ok ? MARK_D * 0.5 : 0);
  tag = name == "" ? str(w, "x", h) : name;
  // ---- design checks
  echo(str("FACEPLATE ", tag, " mount=", mount, " outline ", OW, "x", OH, "x", T_BACK,
           " bolts=", len(ears), " (M5x", BOLT_L, " BHCS, T-nut engage ", engage, " mm)",
           " vent=", vent, " OPEN_CM2=", open_cm2, " hex=", len(hex_c), " slats=", len(lv), " mark=", mark_ok));
  echo(str("MAXSPAN=", maxspan));
  assert(OW <= 281 && OH <= 281, "plate exceeds the 281 mm bed rule (R6.4)");
  assert(T_FL - CB_H >= 4.0, "less than 4 mm under the bolt head (R6.2)");
  assert(!bolt || engage >= 0.8 * 5, "M5 engagement in the T-nut < 0.8 d: lengthen BOLT_L");
  assert(!bolt || shank_past_face <= E/2 + 2, "bolt tip past the member centre bore: shorten BOLT_L");
  assert(EAR_OV - OV - CB_D/2 >= 2.5, "ear wall round the counterbore < 2.5");
  assert(EAR_OV + 1.0 <= E, "ear + neighbour clearance exceeds the 20 mm member");
  for (i = [0 : 3]) if (bolt && sd[i] && nbr[i])
    assert(spitch(side_len(w, h, i), true) >= NOTCH_L, str("side ", i, " too short to interleave ears+notches: set neighbour=0 there"));
  assert(open_cm2 >= vent_min_cm2, str("open area ", open_cm2, " cm2 < required ", vent_min_cm2, " (R4.2)"));
  assert(!label || (w >= LP_W + 2*FIELD_M + 2), "opening too narrow for the 44 mm label seat");
  assert(T_FACE + LP_PAD - (LP_T + 0.2) >= 3.0, "label seat leaves < 3 mm web");
  assert(abs(RIB_W / NOZ - round(RIB_W / NOZ)) < 1e-6, "rib width not a multiple of 0.4");
  assert(mount == "bolt" || mount == "slot", "mount must be bolt|slot");

  // ---- 2D regions
  module rect2d() translate([x0, y0]) square([OW, OH]);
  module ear2d(i, s) translate(sp(w, h, i, s, 0)) rotate(srot(i)) translate([OV - 4, -EAR_L/2]) square([EAR_OV - OV + 4, EAR_L]);
  module notch2d(i, s) translate(sp(w, h, i, s, 0)) rotate(srot(i)) translate([-0.01, -NOTCH_L/2]) square([OV + 1.5, NOTCH_L]);
  module grip2d(rr = GRIP_D) if (gi >= 0) hull() { translate(gA2) circle(r = rr); translate(gB2) circle(r = rr); }
  // plug outline shrunk by d, with the grip scallop (0.2 clear of the cut) grown by d.  Built explicitly rather
  // than with offset(): the scallop's arc meets the plug edge exactly on a polygon vertex and offset() of that
  // difference left slivers in the mesh.
  module plugring(d) difference() { translate([px0 + d, py0 + d]) square([px1 - px0 - 2*d, py1 - py0 - 2*d]); grip2d(GRIP_D + 0.2 + d); }
  module plug2d() plugring(0);
  module inner2d() plugring(RIB_W);                         // inside the perimeter rib
  module midwall2d() plugring(RIB_W/2);                     // ribs end INSIDE the perimeter wall: no coincident faces
  module xribs2d() intersection() { midwall2d(); for (s = [-1, 1]) rotate(s * phi) square([2*(w + h), RIB_W], center = true); }

  // ---- solid.  One hollow cut through one union makes the skin + perimeter rib: two bodies sharing a
  //      curved face (the rib round the grip) would leave T-junctions in the mesh.
  mirror([1, 0, 0]) difference() {                            // view coords -> print coords (face down, reads right)
    union() {
      difference() {
        union() {
          cham_prism(T_FL) rect2d();                          // face + flange block (or the slot plate body)
          for (e = ears) cham_prism(T_FL) ear2d(e[0], e[1]);  // bolt ears
          translate([0, 0, T_FL - 0.01]) linear_extrude(T_BACK - T_FL + 0.01) plug2d();   // plug, solid
        }
        translate([0, 0, T_FACE]) linear_extrude(T_BACK) inner2d();   // hollow behind the 4 mm skin -> perimeter rib / plug wall
      }
      translate([0, 0, T_FACE - 0.01]) linear_extrude(T_BACK - T_FACE + 0.01) xribs2d();                          // X rib
      if (label) translate([lab[0], lab[1], T_FACE - 0.01]) linear_extrude(LP_PAD + 0.01)                          // label back pad
        intersection() { square([lab_fw + 6, lab_fh + 6], center = true); translate(-lab) midwall2d(); }
      if (!bolt) tongues();                                    // slot variant
    }
    // ---- cutters
    for (n = notches) rcham_cutter(T_BACK) notch2d(n[0], n[1]);
    if (gi >= 0) rcham_cutter(T_BACK) grip2d();
    for (e = ears) translate(sp(w, h, e[0], e[1], OV)) {
      translate([0, 0, -1]) cylinder(d = M5B, h = T_BACK + 2);
      translate([0, 0, -1]) cylinder(d = CB_D, h = CB_H + 1);                        // BHCS head, flush
      translate([0, 0, CB_H - 0.01]) cylinder(d1 = CB_FLAT, d2 = M5B, h = (CB_FLAT - M5B)/2 + 0.01);   // 45 deg roof
    }
    for (c = hex_c) translate([c[0], c[1], -1]) rotate(30) cylinder(r = hr, h = T_BACK + 2, $fn = 6);
    for (s = lv) hull() for (x = [s[0] + LV_H/2, s[1] - LV_H/2]) translate([x, s[2], -1]) cylinder(d = LV_H, h = T_BACK + 2);
    if (label) translate([lab[0], lab[1], LP_T + 0.2]) mirror([0, 0, 1]) {
      dovetail(LP_W + 2*LP_CLR, LP_H + 2*LP_CLR, LP_T + 0.2, LIP);
      translate([0, 0, LP_T + 0.19]) linear_extrude(1) square([LP_W + 2*LP_CLR, LP_H + 2*LP_CLR], center = true);   // clean exit
    }
    if (mark_ok) translate([mk[0], mk[1], -1]) linear_extrude(MARK_DEP + 1) scale(MARK_D / 170) mark2d();
  }

  module tongues() {                                            // slot variant: 5.6 tongues, 45 deg underside, 1.0 lead
    zt = T_BACK - 0.2;  z0 = zt - TNG_T;                        // centred on the member mid-depth (10.0)
    for (i = (slot_edges == "lr" ? [1, 3] : [0, 2])) {
      L = side_len(w, h, i) - 2*PLUG_CLR;
      translate(sp(w, h, i, 0, -pc[i])) rotate(srot(i)) intersection() {
        rotate([90, 0, 0]) linear_extrude(L, center = true)
          polygon([[-0.5, z0], [0, z0], [TNG_D, z0 + TNG_D], [TNG_D, zt], [-0.5, zt]]);
        translate([0, 0, z0 - 1]) linear_extrude(TNG_T + 2)
          polygon([[-1, -L/2], [TNG_D, -L/2 + TNG_LEAD], [TNG_D, L/2 - TNG_LEAD], [-1, L/2]]);
      }
    }
  }
}

// ============================================================ top level
if (part == "plate") faceplate();
if (part == "label") plate(label_txt);
if (part == "set") {
  color([0.19, 0.19, 0.21]) faceplate();
  color([1, 0.8, 0]) mirror([1, 0, 0]) translate([0, fp_label_y(h), LP_T + 0.2]) mirror([0, 0, 1]) plate(label_txt);
}
