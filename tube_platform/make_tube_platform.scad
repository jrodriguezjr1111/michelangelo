// ============================================================================
// CyberWing — SLIMRIG TUBE PLATFORM  (rev E — CHEESE PLATE)
// 94 (X) x 134 (Y) plate on two SlimRig tubes, on the PRINTED mirror rail
// clamps, with a 54 mm clear USB/Nano corridor underneath.
//
// *** rev E CHANGES ***
//  1. THE PLATE IS A CHEESE PLATE.  Every component-specific hole pattern on
//     the plate (RTK / relay / EG25 / deck legs / fence / lashing / lightening)
//     is DELETED and replaced by a UNIFORM 10.0 mm GRID of M3 heat-set bores.
//     The layout stops being a design dependency: to move a board you move a
//     screw, not a model.  The upper DECK carries the same grid, and so does
//     the plate UNDERSIDE (half-pitch-offset family — see below).
//  2. Plate back to 94 x 134 (y -67..+67) — the rev-D +30 mm is removed.
//     The rail band and its bolts are ABSOLUTE and did not move, so the
//     PRINTED CLAMPS AND CAPS STILL FIT (vertex-verified — see README).
//  3. Plate thickness 7 -> 8.  Two reasons, both hard:
//       (a) a 6.0 deep insert bore in a 7 plate leaves a 1.0 mm floor — a
//           heat-set WILL punch through some of 109 of them.  8 gives 2.0.
//       (b) perforating on a 10 grid costs 28% of bending stiffness; at 8 mm
//           the perforated plate is 1.08x the SOLID rev-D 7 mm plate.
//           => NO UNDERSIDE RIBS.  The Nano tunnel is untouched.
//
// *** WHY PITCH = 10.0 — the arithmetic (full table in README) ***
//   Real patterns:  RTK 37.60 sq · relay 40.77 x 19.77 (MEASURED) ·
//   EG25 70.80 x 24.21 · FlyCatcher 58 x 49 · ESP32 proto ~60 x 40 (UNMEASURED)
//   · family sled interface 64 x 40.  A Ø4.4 bore needs >= 2.5 mm ligament, so
//   the pitch floor is 6.9.  Brute force over 6.00..22.00 in 0.01 steps:
//     - NO pitch serves more than ONE whole pattern in both axes.  The spans
//       are mutually irrational (37.60 vs 40.77 vs 24.21 vs 58 vs 64).
//     - pitch 10 serves the MOST distinct spans: 6 of 10 within 1.0 mm
//       (19.77->20, 40, 40.77->40, 49->50, 60, 70.80->70), 3 of them to
//       <=0.23 mm.  It is also the prior art (pelican_frame platform_blank).
//     - pitch 8 is the ONLY pitch that lands the family's 64 x 40 sled
//       interface exactly — but it serves fewer real board spans, needs 56%
//       more bores and keeps only 0.95x the solid-7 stiffness.  REJECTED.
//     - pitch 12.5 uniquely nails the ZED-F9P (37.60 = 3 x 12.533, err 0.10)
//       and NOTHING else.  REJECTED.
//     - a DUAL-PITCH / half-offset (quincunx) grid buys NOTHING for a
//       rectangular 4-hole pattern: all four corners must lie in the SAME
//       coset, so reachable spans stay multiples of the base pitch.  A true
//       5 mm second family needs a 5 mm row pitch = 0.6 mm ligament =
//       impossible.  Slotting is impossible too — a heat-set needs a round
//       bore.  DEAD BY ARITHMETIC, not by opinion.
//   => 10.0 mm square grid.  Patterns that miss ride GRID SHOES (below):
//      two small bars per board, ~= the board's own footprint.
//
// *** THE 60-100 HEAT-SET PROBLEM ***
//   The grid is INSERT-READY, not insert-populated: every bore is printed with
//   a chamfered mouth, and a heat-set goes in ONLY where a screw lands.  The
//   reference loadout seats 33 of 220.
//
// part = "plate"|"deck"|"fence"|"shoes"|"clamps"|"caps_spacers"
//      | "spacers_extra"|"set"|"plan1"|"elevation"
// ============================================================================
$fn = 52;
part = "set";
eps = 0.01;

// ---- plate / tubes ----
PL_X = 94; PL_Y0 = -67; PL_Y1 = 67; PL_T = 8;      // 94 x 134 (rev E: -30 SOUTH)
PL_Y = PL_Y1 - PL_Y0;                              // 134
TUBE_D = 15.0; CLR = 0.4; BR = (TUBE_D+CLR)/2;     // 7.7
TUBE_X = 30;                                       // tube lines x = +/-30 (60 c-c)
CABLE_GAP = 54;                                    // clear tube-top -> plate underside
TZ = -(CABLE_GAP + BR);                            // tube centre z = -61.7

// ---- keep-out band + mirror rail clamps — ABSOLUTE, DO NOT TOUCH ----
// These numbers ARE the printed hardware.  The plate shrank 30 mm without
// moving any of them; that is why tp_clamps.stl and tp_caps_spacers.stl are
// not reprinted.  west_rail() below reads NONE of PL_T / PL_Y0 / PL_Y1.
CAP_T = 11; CAP_W = 20; PINCH = 1.0;
BOLT_DX = 12.5;
BAND_S = -40.4; BAND_N = 14.7;
KO_S = BAND_S - PL_Y0; KO_N = PL_Y1 - BAND_N;      // 26.6 / 52.3 (back to rev A5)
CAPY = [BAND_S+10, BAND_N-10];                     // -30.4 / 4.7
FT_D = 19;
RISY = [-33, 9];
RBX = 40; RBY = [-29, -19, -9];                    // rail-top bolts
PB = [for (sx=[-1,1], by=RBY) [sx*RBX, by]];
M3B = 3.4; CB_D = 6.2; CB_H = 3.5;
INS_D = 4.4; INS_DEP = 6.0; INS_CHAM = 0.6;        // the canon INS 4.4 family
SP_OD = 7; SP_H = 6;
NANO_OVER_TUBE = (12-BR) + 7 + 6 + 36;             // 53.3

// ============================ THE CHEESE GRID ============================
// ONE insert family throughout (Ø4.4 x 6.0) — identical to the stock already
// in the printed caps and rail tops, so the box carries ONE heat-set SKU.
GRID_P   = 10.0;                                   // <-- the crux; see header
GRID_D   = INS_D;  GRID_DEP = INS_DEP;  GRID_CHAM = INS_CHAM;
DRV_R    = 4.0;                                    // Ø8 driver access at a rail bolt
GRID_CLR = 0.8;                                    // bore edge -> driver edge, extra web
GX = [for (i=[-4:4]) i*GRID_P];                    // 9 columns, x -40..40
GY = [for (j=[-6:6]) j*GRID_P];                    // 13 rows,   y -60..60

// Nodes sacrificed to Ø8 cable pass-throughs (plate top -> corridor).  They sit
// on the WEST edge column, where the photographed USB runs already exit, and
// clear of the under-side family (which occupies |x| <= 25).
PASS_NODES = [[-40,-40],[-40,-60]];  PASS_D = 8;

function _in(p, L) = len([for (q=L) if (q[0]==p[0] && q[1]==p[1]) 1]) > 0;
function _inn(v, L) = len([for (x=L) if (abs(x-v) < 1e-9) 1]) > 0;
function bolt_gap(p) = min([for (q=PB) norm([p[0]-q[0], p[1]-q[1]])]);
GRID_ALL = [for (gx=GX, gy=GY) [gx,gy]];
GRID = [for (g=GRID_ALL)
          if (bolt_gap(g) >= DRV_R + GRID_D/2 + GRID_CLR && !_in(g, PASS_NODES)) g];

// ---- UNDERSIDE grid: HALF-PITCH-OFFSET family ----------------------------
// A node cannot be bored from both faces (8 - 2x6 < 0), so the under-side
// family is offset (10i+5, 10j+5): 7.07 mm from every top-side node = 2.67 mm
// of web, and — the point — NO horizontal section line ever cuts both
// families, so the worst-case bending section is UNCHANGED (asserted).
// It lives only where hanging hardware is proven safe: south of the Nano's
// stop face and inboard of the rail blades.  This is the WAGO rail's home and
// it recovers, under the plate, some of the area the -30 mm took away.
UGX = [-25,-15,-5,5,15,25];                        // x, half-offset
UGY = [-55,-35,-15,5];                             // y, 20 pitch (a 40.77x19.77
UND = [for (ux=UGX, uy=UGY) [ux,uy]];              //     relay hangs on this)

// ---- upper deck: same grid, same story ----
DK_H = 29; DK_T = 6; DK = [-41.5, -66, 41.5, 66];  // 83 x 132, z 29..35 over the plate
DK_LEG = [[-30,60],[30,60],[-30,-60],[30,-60]];    // legs land on PLATE grid nodes
DGX = [for (i=[-3:3]) i*GRID_P];                   // 7 columns, x -30..30
DGY = [for (j=[-6:6]) j*GRID_P];                   // 13 rows,   y -60..60
DGRID = [for (gx=DGX, gy=DGY) if (!_in([gx,gy], DK_LEG)) [gx,gy]];

// ============================ GRID SHOES ============================
// The adapter for a pattern that misses the grid.  TWO small bars per board,
// 6.0 thick so they REPLACE the Ø7x6 spacers (board heights unchanged):
//   - two board holes: M3 clearance + a captive M3 nut pocket in the top face
//   - two grid holes:  M3 clearance, counterbored, M3x12 into a grid insert
// Sized so the pair's footprint is about the board's own footprint — a big
// square "tile" would have cost 60x60 for a 43.5 mm board and the loadout
// would not have nested.  [ name, board hx, board hy, grid hx, grid hy ]
SHOE_T = 6.0; NUT_AF = 5.8; NUT_T = 2.4; NUT_POCK = 3.0;
SH_BM = 5.0;                                       // margin round a Ø3.4 board hole
SH_GM = 6.0;                                       // margin round a Ø6.2 CB grid hole
SHOES = [
  ["RTK",    18.800, 18.800, 10, 10],              // 37.60 sq      -> grid 20 x 20
  ["RELAY",   9.885, 20.385, 10, 10],              // 19.77 x 40.77 -> grid 20 x 20 (rot 90)
  ["EG25",   35.400, 12.105, 20, 10],              // 70.80 x 24.21 -> grid 40 x 20
  ["FC",     29.000, 24.500, 20, 20]               // 58 x 49       -> grid 40 x 40
];
// ESP32-S3 protoboard 60 x 40 lands EXACTLY on the grid -> NO SHOE, plain
// Ø7x6 spacers.  UNMEASURED — this is the one pattern taken on trust.
// The RELAY is within 0.77/0.23 of a 40 x 20 grid rectangle; opening its own
// holes to Ø4.0 lets it mount DIRECT with no shoe at all (either is fine).
function sh_xa(s) = -max(s[1]+SH_BM, s[3]+SH_GM);
function sh_xb(s) = -min(s[1]-SH_BM, s[3]-SH_GM);
function sh_yh(s) =  max(s[2]+SH_BM, s[4]+SH_GM);

// ============================ REFERENCE LOADOUT ============================
// NOT geometry — the plate and deck carry no board-specific feature.  This
// exists so the assembly view and the nesting check have something concrete.
// Every position is a grid node; move any of it freely.
RTK_P = 37.6/2; RTK_BRD = 43.5; RTK_H = 20;                 RTK_C = [-20, 30];
RLY_P = [40.77/2, 19.77/2]; RLY_BRD = [26, 50]; RLY_H = 20; RLY_C = [ 20, 20]; // rot 90
EG_P  = [70.80/2, 24.21/2]; EG_BRD = [80, 35];  EG_H = 24;  EG_C  = [  0,-30];
FC_P  = [58/2, 49/2]; FC_BRD = [73, 54]; FC_H = 27;         FC_C  = [  0, 30]; // deck
PB_P  = [60/2, 40/2]; PB_BRD = [70, 50]; PB_H = 25;         PB_C  = [  0,-30]; // deck
SP_OD2 = 7; SP_H2 = 6;
// footprint of a shoe-mounted board = the shoe pair's outline
function fp(s, c) = [c[0]+sh_xa(s), c[1]-sh_yh(s), c[0]-sh_xa(s), c[1]+sh_yh(s)];
L1_FP = [["RTK", fp(SHOES[0], RTK_C)], ["RELAY", fp(SHOES[1], RLY_C)],
         ["EG25", fp(SHOES[2], EG_C)]];
DK_FP = [["FC", fp(SHOES[3], FC_C)],
         ["ESP32", [PB_C[0]-PB_BRD[0]/2, PB_C[1]-PB_BRD[1]/2,
                    PB_C[0]+PB_BRD[0]/2, PB_C[1]+PB_BRD[1]/2]]];

// ---- fence / cable wall (re-cut for 134; SMA row still frozen) ----
WX0 = 44.5; WX1 = 47; WALL_H = 35;
SMA_D = 6.5; SMA_Y = [44, 16, -12]; SMA_Z = 17;    // *** DO NOT MOVE ***
RIB_Y = [60, 30, 0, -46]; RIB_W = 4; RIB_X = 4;    // outboard stiffening fins
RAIL_X0 = 43; RAIL_Z0 = 29;                        // inboard top rail
ZIP_Y = [60, 36, 24, 4, -4, -24, -40];             // 7 columns, pairs at z 21/27
CLAMP_Y = [-30]; CLAMP_PAD = [8, 22, 12];          // outboard cable-clamp pad
CLAMP_Z = 14; CLAMP_GR = 3;
FENCE_SCR = [[40,60],[40,40],[40,10],[40,-40],[40,-60]];   // ALL GRID NODES
FEED_WALL_Y = -57; FEED_WALL_Z = 12; FEED_D = 12;  // DC supply entry (RSD is outside)
WALL_PORT_D = 0; WALL_PORT_Y = -20; WALL_PORT_Z = 18;

// ---- stiffness bookkeeping (perforated section vs the solid rev-D plate) ----
function _lig() = (GRID_P - GRID_D)/GRID_P;
function _I(T, dep, f) =
  let (fl = T-dep, A1 = f*dep, c1 = fl+dep/2, A2 = fl, c2 = fl/2,
       yb = (A1*c1 + A2*c2)/(A1+A2))
  f*pow(dep,3)/12 + A1*pow(c1-yb,2) + pow(fl,3)/12 + A2*pow(c2-yb,2);
I_PERF  = _I(PL_T, GRID_DEP, _lig());
I_SOLID = pow(PL_T,3)/12;
I_REVD  = pow(7,3)/12;

// ---- registries ----
function pat(c,p) = [for (sx=[-1,1], sy=[-1,1]) [c[0]+sx*p[0], c[1]+sy*p[1]]];
PB_INS = pat(PB_C, PB_P);                          // the one DIRECT-mount board

// ---- echoes ----
echo(str("*** rev E CHEESE PLATE: ", PL_X, " x ", PL_Y, " (y ", PL_Y0, "..", PL_Y1,
         "), ", PL_T, " thick.  GRID PITCH ", GRID_P, ", Ø", GRID_D, " x ", GRID_DEP,
         " heat-set bores.  RAIL BAND AND BOLTS DID NOT MOVE (band y ", BAND_S, "..",
         BAND_N, ", bolts x +/-", RBX, " y ", RBY, ") -> PRINTED CLAMPS AND CAPS ",
         "STILL FIT.  Cantilever off the band: S ", KO_S, " / N ", KO_N, ". ***"));
echo(str("BORES: plate TOP ", len(GRID), " insert-ready + plate UNDER ", len(UND),
         " (half-offset family) + ", len(PASS_NODES), " Ø", PASS_D,
         " pass-throughs; ", len(GRID_ALL)-len(GRID)-len(PASS_NODES),
         " nodes suppressed for rail-bolt driver access.  DECK ", len(DGRID),
         " insert-ready (+", len(DK_LEG), " leg through-bolts).  TOTAL INSERT-READY ",
         len(GRID)+len(UND)+len(DGRID),
         " — the reference loadout SEATS 33 of them.  Seat nothing else."));
echo(str("GRID REACH: plate X spans ", GRID_P, "..", max(GX)-min(GX),
         " | plate Y spans ", GRID_P, "..", max(GY)-min(GY),
         " | deck X ", max(DGX)-min(DGX), ", deck Y ", max(DGY)-min(DGY),
         " | under-side X ", max(UGX)-min(UGX), " (10 pitch), Y ",
         max(UGY)-min(UGY), " (20 pitch).  Ligament ", _lig()*GRID_P,
         " mm same-family, ", GRID_P/sqrt(2)-GRID_D, " mm top-to-under."));
echo(str("STIFFNESS: perforated I ", I_PERF, " vs solid ", PL_T, " mm ", I_SOLID,
         " (", I_PERF/I_SOLID, "x) — and vs the SOLID rev-D 7 mm plate ",
         I_PERF/I_REVD, "x.  Going 7 -> 8 mm buys back everything the grid ",
         "costs, so NO UNDERSIDE RIBS: the ", CABLE_GAP,
         " mm Nano corridor and the ", KO_N, " north insertion are untouched."));
echo(str("PATTERN SERVICE at pitch ", GRID_P,
         ": ESP32 60x40 DIRECT (spacers) | relay 40.77x19.77 -> 40x20, err ",
         "0.77/0.23 — DIRECT if you open its own holes to Ø4.0, else a shoe | ",
         "RTK 37.60 sq, EG25 70.80x24.21, FC 58x49 -> GRID SHOES.  No pitch in ",
         "6..22 serves more than one whole pattern; see the README table."));
echo(str("SHOE FOOTPRINTS (pair): ",
         [for (s=SHOES) str(s[0], " ", -2*sh_xa(s), "x", 2*sh_yh(s))],
         "  vs board envelopes RTK ", RTK_BRD, "sq, RELAY ", RLY_BRD,
         ", EG25 ", EG_BRD, ", FC ", FC_BRD, " — the shoes tuck under."));
echo(str("VERTICAL (above plate top): RTK/relay/EG25 top ", SP_H+RTK_H,
         " | deck underside ", DK_H, " -> clear ", DK_H-(SP_H+RTK_H),
         " | deck top ", DK_H+DK_T, " | FC top ", DK_H+DK_T+SP_H+FC_H,
         " | proto top ", DK_H+DK_T+SP_H+PB_H));
echo(str("RAIL BOLTS: plate is now ", PL_T, " thick, so an M3x12 through the ",
         CB_H, " counterbore engages ", 12-PL_T,
         " mm of brass in the rail-top insert.  The joint is plastic-limited ",
         "(~300 N insert pull-out), not thread-limited, so M3x12 stands; ",
         "M3x14 gives the full ", INS_DEP, " mm if you want belt and braces."));

// ============================ asserts ============================
// -- grid vs the PRINTED rail clamps: bores must clear the bolt AND its Ø8
//    driver column, or the caps stop being serviceable with the plate on.
for (g=GRID) assert(bolt_gap(g) - DRV_R - GRID_D/2 >= 0.5,
  str("GRID node ", g, " fouls a rail-bolt driver column"));
for (g=GRID) assert(bolt_gap(g) - CB_D/2 - GRID_D/2 >= 2.0,
  str("GRID node ", g, " crowds a rail-bolt counterbore"));
// -- grid web / edge
assert(GRID_P - GRID_D >= 2.5, "grid ligament below the 2.5 mm web minimum");
for (g=GRID) assert(min(PL_X/2-abs(g[0]), g[1]>0 ? PL_Y1-g[1] : g[1]-PL_Y0)
                    - GRID_D/2 >= 2.5, str("GRID node ", g, " too near the plate edge"));
for (u=UND) assert(min(PL_X/2-abs(u[0]), u[1]>0 ? PL_Y1-u[1] : u[1]-PL_Y0)
                   - GRID_D/2 >= 2.5, str("UNDER node ", u, " too near the plate edge"));
// -- insert web to the plate underside (this is what killed PL_T = 7)
assert(PL_T - GRID_DEP >= 1.5,
  str("insert bore floor only ", PL_T-GRID_DEP, " mm — a heat-set will punch through"));
// -- top-side and under-side families must never share a node, and must keep web
for (u=UND) assert(!_in(u, GRID), "a node is bored from BOTH faces");
for (u=UND, g=GRID) assert(norm([u[0]-g[0],u[1]-g[1]]) - GRID_D >= 2.0,
  str("under-side node ", u, " has no web to top-side node ", g));
// -- the half-offset family must not cut the same section line as the top family
for (u=UND) assert(!_inn(u[0], GX) && !_inn(u[1], GY),
  str("under-side node ", u, " shares a row or column with the top family — the ",
      "worst-case bending section would then cut BOTH families"));
// -- pass-throughs
for (p=PASS_NODES) assert(!_in(p, GRID), "pass-through node still carries an insert");
for (p=PASS_NODES, g=GRID) assert(norm([p[0]-g[0],p[1]-g[1]]) - PASS_D/2 - GRID_D/2 >= 2.0,
  "Ø8 pass-through eats a grid bore's web");
for (p=PASS_NODES, u=UND) assert(norm([p[0]-u[0],p[1]-u[1]]) - PASS_D/2 - GRID_D/2 >= 2.0,
  "Ø8 pass-through eats an under-side bore's web");
for (p=PASS_NODES) assert(min(PL_X/2-abs(p[0]), p[1]>0 ? PL_Y1-p[1] : p[1]-PL_Y0)
                          - PASS_D/2 >= 2.5, "Ø8 pass-through too near the plate edge");
for (p=PASS_NODES) assert(!_in(p, FENCE_SCR), "a pass-through took a fence screw node");
// -- grid vs the tube trough / Nano corridor
assert(CABLE_GAP - NANO_OVER_TUBE >= 0.5,
  str("Nano tunnel gone: ", CABLE_GAP-NANO_OVER_TUBE));
assert(abs(TZ + BR + CABLE_GAP) < 1e-9, "tube trough datum drifted");
for (g=GRID) assert(PL_T - GRID_DEP > 0, "top grid bore opens into the tube corridor");
for (u=UND)  assert(PL_T - GRID_DEP > 0, "under grid bore opens through the plate top");
for (u=UND)  assert(u[1] <= BAND_N - 8,
  str("under-side node ", u, " is in the Nano's north insertion sweep"));
for (u=UND)  assert(abs(u[0]) <= TUBE_X - 3,
  str("under-side node ", u, " sits over a tube trough / rail blade"));
// -- deck
for (d=DGRID) assert(min(DK[2]-abs(d[0]), d[1]>0 ? DK[3]-d[1] : d[1]-DK[1])
                     - GRID_D/2 >= 2.5, str("deck node ", d, " too near the deck edge"));
for (d=DGRID, l=DK_LEG) assert(norm([d[0]-l[0],d[1]-l[1]]) - GRID_D/2 - CB_D/2 >= 2.0,
  "deck node crowds a leg bolt");
for (l=DK_LEG) assert(_in(l, GRID), str("deck leg ", l, " does not land on a plate node"));
for (l=DK_LEG) assert(min(DK[2]-abs(l[0]), l[1]>0 ? DK[3]-l[1] : l[1]-DK[1]) >= 4.5+1.5,
  "deck leg boss runs off the deck");
assert(DK[2] <= WX0 - 2, "deck hits the cable wall");
assert(RAIL_X0 - DK[2] >= 1.0, "deck collides with the wall top rail");
assert(DK_H - (SP_H+RTK_H) >= 3, "deck crushes the reference level-1 stack");
assert(DK[1] >= PL_Y0 && DK[3] <= PL_Y1, "deck overhangs the plate");
// -- fence
for (q=FENCE_SCR) assert(_in(q, GRID), str("fence screw ", q, " is not a grid node"));
assert(RBX + CB_D/2 <= WX0 - 0.4, "east plate-bolt CB under the cable-wall base");
assert(WALL_H > SMA_Z + SMA_D/2 + 3, "cable wall too short for the SMA row");
assert(RAIL_Z0 >= SMA_Z + SMA_D/2 + 3, "top rail cuts into the SMA row");
for (jy=SMA_Y) assert(abs(jy) <= PL_Y/2 - SMA_D/2 - 3, "an SMA ran off the 134 wall");
for (zy=ZIP_Y) assert(abs(zy) <= PL_Y/2 - M3B/2 - 2, "a zip column ran off the 134 wall");
for (ry=RIB_Y) assert(abs(ry) <= PL_Y/2 - RIB_W/2, "a rib ran off the 134 wall");
for (cy=CLAMP_Y) assert(abs(cy) + CLAMP_PAD[1]/2 <= PL_Y/2, "clamp pad ran off the wall");
for (ry=RIB_Y, jy=SMA_Y) assert(abs(ry-jy) - RIB_W/2 >= 8, "outboard rib blocks an SMA nut");
for (zy=ZIP_Y, jy=SMA_Y) assert(abs(zy-jy) >= 6, "zip column crowds an SMA bulkhead");
for (cy=CLAMP_Y, jy=SMA_Y) assert(abs(cy-jy) - CLAMP_PAD[1]/2 >= 4, "clamp pad blocks an SMA");
for (cy=CLAMP_Y, ry=RIB_Y)
  assert(abs(cy-ry) - CLAMP_PAD[1]/2 - RIB_W/2 >= 2, "clamp pad collides with a rib");
assert(FEED_WALL_Y - FEED_D/2 >= PL_Y0 + 3, "DC feed-through off the wall south end");
for (jy=SMA_Y) assert(abs(FEED_WALL_Y-jy) - FEED_D/2 - SMA_D/2 >= 4, "DC feed crowds an SMA");
for (ry=RIB_Y) assert(abs(FEED_WALL_Y-ry) - FEED_D/2 - RIB_W/2 >= 2, "DC feed hits a rib");
for (cy=CLAMP_Y) assert(abs(FEED_WALL_Y-cy) - FEED_D/2 - CLAMP_PAD[1]/2 >= 2,
  "DC feed overlaps the clamp pad");
for (zy=ZIP_Y) assert(abs(FEED_WALL_Y-zy) - FEED_D/2 >= 2, "DC feed hits a zip column");
// -- shoes
for (s=SHOES) {
  assert(abs(2*s[3]/GRID_P - round(2*s[3]/GRID_P)) < 1e-6 &&
         abs(2*s[4]/GRID_P - round(2*s[4]/GRID_P)) < 1e-6,
         str("shoe ", s[0], ": grid span is not a multiple of the pitch"));
  assert(norm([s[1]-s[3], s[2]-s[4]]) >= M3B + 3.0,
         str("shoe ", s[0], ": grid hole and board hole overlap"));
  assert(sh_xb(s) - sh_xa(s) >= 8, str("shoe ", s[0], " bar too narrow"));
  assert(SHOE_T - NUT_POCK >= 2.0, "shoe too thin under the nut pocket");
  assert(NUT_POCK >= NUT_T + 0.5, "nut pocket shallower than the nut");
  assert(SHOE_T - CB_H >= 2.0, "shoe too thin under the grid counterbore");
}
// -- reference loadout: on-plate, clear of the deck-leg bosses, no overlaps
for (f=L1_FP) assert(f[1][0] >= -PL_X/2 && f[1][2] <= PL_X/2 &&
                     f[1][1] >= PL_Y0 && f[1][3] <= PL_Y1,
                     str("reference item ", f[0], " runs off the plate"));
for (f=L1_FP, l=DK_LEG)
  assert(!(l[0] > f[1][0]-5.0 && l[0] < f[1][2]+5.0 &&
           l[1] > f[1][1]-5.0 && l[1] < f[1][3]+5.0),
         str("reference item ", f[0], " lands on a deck-leg boss"));
for (i=[0:len(L1_FP)-2], j=[i+1:len(L1_FP)-1])
  assert(L1_FP[i][1][2] <= L1_FP[j][1][0] || L1_FP[j][1][2] <= L1_FP[i][1][0] ||
         L1_FP[i][1][3] <= L1_FP[j][1][1] || L1_FP[j][1][3] <= L1_FP[i][1][1],
         str("reference items ", L1_FP[i][0], " and ", L1_FP[j][0], " overlap"));
for (f=DK_FP) assert(f[1][0] >= DK[0] && f[1][2] <= DK[2] &&
                     f[1][1] >= DK[1] && f[1][3] <= DK[3],
                     str("reference deck item ", f[0], " runs off the deck"));
assert(DK_FP[0][1][1] >= DK_FP[1][1][3] || DK_FP[1][1][1] >= DK_FP[0][1][3],
       "reference deck items overlap");
for (q=PB_INS) assert(_in(q, DGRID), "ESP32 direct-mount hole is not a free deck node");
echo(str("REFERENCE NESTING (level 1): ",
         [for (f=L1_FP) str(f[0], " x ", f[1][0], "..", f[1][2],
                            " y ", f[1][1], "..", f[1][3])],
         " | deck: ", [for (f=DK_FP) str(f[0], " y ", f[1][1], "..", f[1][3])],
         "  — RTK/RELAY abut with a 0.2 mm gap in X; that is the 10 mm grid ",
         "quantisation, not a fit problem.  It is layout, not geometry: slide ",
         "either one a node."));

// ============================ helpers ============================
module flushins(x, y, zt) {                        // blind insert, opens UP
  translate([x, y, zt-INS_DEP]) cylinder(d=INS_D, h=INS_DEP+0.1);
  translate([x, y, zt-INS_CHAM]) cylinder(d1=INS_D, d2=INS_D+2*INS_CHAM, h=INS_CHAM+0.05);
}
module flushins_dn(x, y, zb) {                     // blind insert, opens DOWN
  translate([x, y, zb-0.1]) cylinder(d=INS_D, h=INS_DEP+0.1);
  translate([x, y, zb-0.05]) cylinder(d1=INS_D+2*INS_CHAM, d2=INS_D, h=INS_CHAM+0.05);
}
module thruins(x, y, t) {                          // through insert (deck)
  translate([x, y, -0.1]) cylinder(d=INS_D, h=t+0.2);
  translate([x, y, t-INS_CHAM]) cylinder(d1=INS_D, d2=INS_D+2*INS_CHAM, h=INS_CHAM+0.05);
  translate([x, y, -0.05]) cylinder(d1=INS_D+2*INS_CHAM, d2=INS_D, h=INS_CHAM+0.05);
}
module rrect(x0,y0,x1,y1,r=4) hull() for (px=[x0+r,x1-r], py=[y0+r,y1-r])
  translate([px,py]) circle(r=r);

// ============================ LEVEL-1 CHEESE PLATE ============================
// No component features.  Grid, rail bolts, under-side grid, pass-throughs.
module plate() {
  difference() {
    translate([-PL_X/2, PL_Y0, 0]) cube([PL_X, PL_Y, PL_T]);
    for (q=PB) {                                   // plate -> rail bolts (UNCHANGED)
      translate([q[0], q[1], -0.1]) cylinder(d=M3B, h=PL_T+0.2);
      translate([q[0], q[1], PL_T-CB_H]) cylinder(d=CB_D, h=CB_H+0.1);
    }
    for (g=GRID)       flushins(g[0], g[1], PL_T);   // THE CHEESE GRID
    for (u=UND)        flushins_dn(u[0], u[1], 0);   // half-offset under-side family
    for (p=PASS_NODES) translate([p[0], p[1], -0.1]) cylinder(d=PASS_D, h=PL_T+0.2);
  }
}

// ============================ UPPER CHEESE DECK ============================
// Same grid, 6 mm so a Ø4.4 heat-set sits flush through.  Prints deck-face
// DOWN, legs up — zero support.
module deck() {
  difference() {
    union() {
      linear_extrude(DK_T) rrect(DK[0], DK[1], DK[2], DK[3], 5);
      for (l=DK_LEG) translate([l[0], l[1], -DK_H]) cylinder(d=9, h=DK_H+eps);
    }
    for (l=DK_LEG) {                               // M3x35 from the deck top
      translate([l[0], l[1], -DK_H-1]) cylinder(d=M3B, h=DK_H+DK_T+1.2);
      translate([l[0], l[1], DK_T-CB_H]) cylinder(d=CB_D, h=CB_H+0.1);
    }
    for (d=DGRID) thruins(d[0], d[1], DK_T);       // THE CHEESE GRID
  }
}

// ============================ GRID SHOE ============================
module shoe(s) {                                   // the -x bar of the pair
  xa = sh_xa(s); xb = sh_xb(s); yh = sh_yh(s);
  difference() {
    linear_extrude(SHOE_T) rrect(xa, -yh, xb, yh, 3);
    for (sy=[-1,1]) {
      translate([-s[1], sy*s[2], -0.1]) cylinder(d=M3B, h=SHOE_T+0.2);
      translate([-s[1], sy*s[2], SHOE_T-NUT_POCK])
        cylinder(d=NUT_AF/cos(30), h=NUT_POCK+0.1, $fn=6);
      translate([-s[3], sy*s[4], -0.1]) cylinder(d=M3B, h=SHOE_T+0.2);
      translate([-s[3], sy*s[4], SHOE_T-CB_H]) cylinder(d=CB_D, h=CB_H+0.1);
    }
  }
}
module shoe_pair(s) { shoe(s); mirror([1,0,0]) shoe(s); }

// ============================ CABLE WALL (fence) ============================
// Re-cut for the 134 plate.  SMA row FROZEN (y 44/16/-12, z 17) so bulkheads
// already installed still fit and align; DC feed and clamp pad re-sited into
// the clear windows the shorter wall leaves; screw column moved onto GRID
// NODES at x = 40, so the wall needs no dedicated bores in the plate.
module fence() {
  difference() {
    union() {
      translate([WX0, PL_Y0, 0]) cube([WX1-WX0, PL_Y, WALL_H]);      // 2.5 core
      translate([RAIL_X0, PL_Y0, RAIL_Z0])                           // inboard top rail
        cube([WX1-RAIL_X0, PL_Y, WALL_H-RAIL_Z0]);
      for (ry=RIB_Y) {                                               // outboard fins
        translate([WX1-eps, ry-RIB_W/2, 0]) cube([RIB_X, RIB_W, 30]);
        translate([WX1-eps, ry-RIB_W/2, 30]) rotate([0,45,0])
          cube([RIB_X*1.42, RIB_W, RIB_X*1.42]);
      }
      for (cy=CLAMP_Y) {                                             // clamp pad + gusset
        translate([WX1-eps, cy-CLAMP_PAD[1]/2, CLAMP_Z-CLAMP_PAD[2]/2])
          cube([CLAMP_PAD[0], CLAMP_PAD[1], CLAMP_PAD[2]]);
        hull() {
          translate([WX1-eps, cy-CLAMP_PAD[1]/2, CLAMP_Z-CLAMP_PAD[2]/2])
            cube([0.1, CLAMP_PAD[1], 0.1]);
          translate([WX1-eps, cy-CLAMP_PAD[1]/2, CLAMP_Z-CLAMP_PAD[2]/2-CLAMP_PAD[0]])
            cube([0.1, CLAMP_PAD[1], 0.1]);
        }
      }
      for (q=FENCE_SCR) translate([q[0], q[1]]) cylinder(d=9, h=3);
      for (q=FENCE_SCR) translate([q[0], q[1]-4.5, 0]) cube([WX0-q[0]+0.1, 9, 3]);
    }
    for (jy=SMA_Y) translate([WX0-0.1, jy, SMA_Z]) rotate([0,90,0])
      cylinder(d=SMA_D, h=WX1+RIB_X-WX0+0.4);                        // SMA (FROZEN)
    translate([WX0-0.1, FEED_WALL_Y, FEED_WALL_Z]) rotate([0,90,0])   // DC supply entry
      cylinder(d=FEED_D, h=WX1+RIB_X-WX0+0.4);
    for (zy=ZIP_Y, zz=[21,27]) translate([WX0-0.1, zy, zz]) rotate([0,90,0])
      cylinder(d=M3B, h=WX1-WX0+0.2);
    for (cy=CLAMP_Y) {
      translate([WX1+CLAMP_PAD[0]-CLAMP_GR, cy, CLAMP_Z-CLAMP_PAD[2]/2-1])
        cylinder(r=CLAMP_GR, h=CLAMP_PAD[2]+2);
      for (sy=[-1,1]) translate([WX1+CLAMP_PAD[0]+0.1, cy+sy*6.5, CLAMP_Z])
        rotate([0,-90,0]) { cylinder(d=INS_D, h=INS_DEP+0.1);
          cylinder(d1=INS_D+2*INS_CHAM, d2=INS_D, h=INS_CHAM+0.05); }
    }
    if (WALL_PORT_D > 0) translate([WX0-0.1, WALL_PORT_Y, WALL_PORT_Z])
      rotate([0,90,0]) cylinder(d=WALL_PORT_D, h=WX1-WX0+0.2);
    for (q=FENCE_SCR) {
      translate([q[0], q[1], -0.1]) cylinder(d=M3B, h=3.2);
      translate([q[0], q[1], 3-CB_H]) cylinder(d=CB_D, h=CB_H+2);
    }
  }
}
module clamp_bar() difference() {
  translate([0, -CLAMP_PAD[1]/2, 0]) cube([4, CLAMP_PAD[1], 9]);
  translate([4+CLAMP_GR-1.2, 0, -1]) cylinder(r=CLAMP_GR, h=11);
  for (sy=[-1,1]) translate([-0.1, sy*6.5, 4.5]) rotate([0,90,0]) {
    cylinder(d=M3B, h=5); translate([0,0,4-CB_H]) cylinder(d=CB_D, h=CB_H+1.2); }
}
module anchor_clip() difference() {
  hull() { cylinder(d=9, h=2.5); translate([15,0,0]) cylinder(d=8, h=2.5); }
  translate([0,0,-0.1]) cylinder(d=M3B, h=3);
  translate([12,-1.4,-0.1]) cube([6, 2.8, 3]);
}

// ============================ RAIL CLAMP (BIT-FROZEN) ============================
// Nothing below this line may change: tp_clamps.stl and tp_caps_spacers.stl
// are PRINTED and in the user's hands.
module west_rail() {
  difference() {
    union() {
      translate([-TUBE_X-FT_D, BAND_S, TZ-17]) cube([FT_D, BAND_N-BAND_S, 34]);
      translate([-TUBE_X-FT_D, RISY[0], TZ+17-eps])
        cube([16, RISY[1]-RISY[0], CABLE_GAP+BR-17+eps]);
      hull() {
        translate([-TUBE_X-FT_D, BAND_S, TZ+13]) cube([FT_D, BAND_N-BAND_S, 4]);
        translate([-TUBE_X-FT_D, RISY[0], TZ+17]) cube([16, RISY[1]-RISY[0], 4]);
      }
    }
    translate([-TUBE_X, BAND_S-1, TZ]) rotate([-90,0,0])
      cylinder(r=BR, h=BAND_N-BAND_S+2);
    for (sz=[-1,1]) translate([-TUBE_X, (BAND_S+BAND_N)/2, TZ+sz*BR])
      rotate([0,45,0]) cube([1.7, BAND_N-BAND_S+2.4, 1.7], center=true);
    for (cy=CAPY, sb=[-1,1]) {
      translate([-TUBE_X-FT_D-1, cy, TZ+sb*BOLT_DX]) rotate([0,90,0]) cylinder(d=M3B, h=FT_D+2);
      translate([-TUBE_X-FT_D-0.1, cy, TZ+sb*BOLT_DX]) rotate([0,90,0]) cylinder(d=CB_D, h=CB_H+0.1);
    }
    for (by=RBY) {
      translate([-RBX, by, -INS_DEP]) cylinder(d=INS_D, h=INS_DEP+0.1);
      translate([-RBX, by, -INS_CHAM]) cylinder(d1=INS_D, d2=INS_D+2*INS_CHAM, h=INS_CHAM+0.05);
    }
  }
}
module cap() {
  difference() {
    translate([-CAP_W/2, -17, -CAP_T]) cube([CAP_W, 34, CAP_T]);
    translate([-CAP_W/2-0.1, 0, PINCH]) rotate([0,90,0]) cylinder(r=BR, h=CAP_W+0.2);
    for (sb=[-1,1]) {
      translate([0, sb*BOLT_DX, -INS_DEP]) cylinder(d=INS_D, h=INS_DEP+0.1);
      translate([0, sb*BOLT_DX, -INS_CHAM]) cylinder(d1=INS_D, d2=INS_D+2*INS_CHAM, h=INS_CHAM+0.05);
    }
  }
}
module spacer() difference() {
  cylinder(d=SP_OD, h=SP_H);
  translate([0,0,-0.1]) cylinder(d=M3B, h=SP_H+0.2);
}

// ============================ views ============================
module ghosts() {
  color([0.4,0.6,0.8,0.4]) for (sx=[-1,1])                          // tubes
    translate([sx*TUBE_X, PL_Y0-15, TZ]) rotate([-90,0,0]) cylinder(d=TUBE_D, h=PL_Y+30);
  color([0.2,0.6,1,0.35])                                            // EG25 assembly
    translate([EG_C[0]-EG_BRD[0]/2, EG_C[1]-EG_BRD[1]/2, PL_T+SP_H])
      cube([EG_BRD[0], EG_BRD[1], EG_H]);
  color([0.9,0.2,0.2,0.4])                                           // RTK
    translate([RTK_C[0]-RTK_BRD/2, RTK_C[1]-RTK_BRD/2, PL_T+SP_H])
      cube([RTK_BRD, RTK_BRD, RTK_H]);
  color([0.2,0.3,0.9,0.35])                                          // relay (rot 90)
    translate([RLY_C[0]-RLY_BRD[0]/2, RLY_C[1]-RLY_BRD[1]/2, PL_T+SP_H])
      cube([RLY_BRD[0], RLY_BRD[1], RLY_H]);
  color([0.2,0.5,1,0.4])                                             // FlyCatcher, on deck
    translate([FC_C[0]-FC_BRD[0]/2, FC_C[1]-FC_BRD[1]/2, PL_T+DK_H+DK_T+SP_H])
      cube([FC_BRD[0], FC_BRD[1], FC_H]);
  color([0.3,0.8,0.3,0.4])                                           // ESP32-S3 protoboard
    translate([PB_C[0]-PB_BRD[0]/2, PB_C[1]-PB_BRD[1]/2, PL_T+DK_H+DK_T+SP_H])
      cube([PB_BRD[0], PB_BRD[1], PB_H]);
  color([0.3,0.9,0.5,0.35]) {                                        // Nano, from the north
    translate([-48, BAND_N, TZ+BR+4.3]) cube([96, 76, 7]);
    translate([-50, BAND_N+2, TZ+BR+4.3+7+6]) cube([100, 80, 36]);
  }
}
module assembly() {
  color("Khaki") plate();
  color("LightSteelBlue") translate([0,0,PL_T]) fence();
  color("Thistle") translate([0,0,PL_T+DK_H]) deck();
  color("Gold") { west_rail(); mirror([1,0,0]) west_rail(); }
  color("LightGreen") for (cy=CAPY) {
    translate([-TUBE_X+2, cy, TZ]) rotate([0,0,90]) rotate([90,0,0]) rotate([0,90,0]) cap();
    mirror([1,0,0]) translate([-TUBE_X+2, cy, TZ]) rotate([0,0,90]) rotate([90,0,0])
      rotate([0,90,0]) cap();
  }
  color("Coral") {                                  // grid shoes, in place
    translate([RTK_C[0], RTK_C[1], PL_T]) shoe_pair(SHOES[0]);
    translate([RLY_C[0], RLY_C[1], PL_T]) shoe_pair(SHOES[1]);
    translate([EG_C[0],  EG_C[1],  PL_T]) shoe_pair(SHOES[2]);
    translate([FC_C[0],  FC_C[1],  PL_T+DK_H+DK_T]) shoe_pair(SHOES[3]);
  }
  color("Khaki") for (q=PB_INS) translate([q[0],q[1],PL_T+DK_H+DK_T]) spacer();
  ghosts();
}

if (part=="plate")   translate([0,0,PL_T]) rotate([180,0,0]) plate();   // cargo face down
if (part=="fence")   { fence(); translate([-20,-40,0]) clamp_bar();
                       translate([-20,-20,0]) clamp_bar();
                       for (i=[0:5]) translate([-38+i*12, 20, 0]) anchor_clip(); }
if (part=="deck")    translate([0,0,DK_T]) rotate([180,0,0]) deck();    // deck face down
if (part=="shoes") {
  translate([-30,  46, 0]) shoe_pair(SHOES[0]);     // RTK
  translate([ 30,  46, 0]) shoe_pair(SHOES[1]);     // RELAY
  translate([  0,  -2, 0]) shoe_pair(SHOES[2]);     // EG25
  translate([  0, -50, 0]) shoe_pair(SHOES[3]);     // FC
}
if (part=="spacers_extra") for (i=[0:7]) translate([i%4*12-18, floor(i/4)*12, 0]) spacer();
if (part=="clamps") {
  translate([-15, 30, FT_D]) rotate([0,-90,0]) translate([TUBE_X, 0, -TZ]) west_rail();
  translate([ 15, -30, FT_D]) rotate([0,90,0]) translate([-TUBE_X, 0, -TZ])
    mirror([1,0,0]) west_rail();
}
if (part=="caps_spacers") {
  for (i=[0:3]) translate([i*28-42, 0, CAP_T]) cap();
  for (i=[0:11]) translate([i%6*12-30, (i<6? 28 : 38), 0]) spacer();
}
if (part=="set") assembly();
if (part=="plan1") { plate(); translate([0,0,PL_T]) fence(); }
if (part=="elevation") assembly();
