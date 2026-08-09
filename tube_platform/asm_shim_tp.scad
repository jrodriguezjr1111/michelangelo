// ============================================================================
// CyberWing — SHIM: tube_platform rev B parts + parameters, namespaced.
//
// WHY: make_system_assembly.scad must instantiate the REAL part geometry and
// the REAL parameter values, but make_tube_platform.scad, make_nano_tube_plate
// .scad and make_orin_tube_plate.scad all define plate(), cap(), spacer(),
// PL_X, PL_T, TUBE_D ... with DIFFERENT values.  `include` them all into one
// file and they collide; `use` them all and the later cap() silently wins.
//
// This shim `include`s ONE part file (so its file-scope variables are live for
// its modules) and re-exports everything behind a unique tp_* prefix.  The
// assembly then `use`s the shim: `use` imports module/function DEFINITIONS
// only, so none of the raw names leak and nothing collides.
//
// NOTHING IS TRANSCRIBED HERE.  Every number the assembly draws comes back
// through these accessors from make_tube_platform.scad, which stays the sole
// authority.  If a dimension changes there, the assembly follows automatically.
//
// This file is NOT a part.  It renders nothing (part="none").
// ============================================================================
include <make_tube_platform.scad>
part = "none";                       // last assignment in scope wins -> silent

// ---------------------------------------------------------------- geometry --
module tp_plate()        plate();
module tp_fence()        fence();
module tp_tower()        tower();
module tp_carrier()      carrier();
module tp_retainer_bar() retainer_bar();
module tp_west_rail()    west_rail();
module tp_cap()          cap();
module tp_spacer()       spacer();

// -------------------------------------------------------------- parameters --
// plate / tubes / corridor
function tp_PL_X()   = PL_X;      function tp_PL_Y()  = PL_Y;
function tp_PL_T()   = PL_T;      function tp_TUBE_D()= TUBE_D;
function tp_TUBE_X() = TUBE_X;    function tp_BR()    = BR;
function tp_CABLE_GAP() = CABLE_GAP;
function tp_TZ()     = TZ;

// keep-out band / rail clamps / caps
function tp_KO_S()   = KO_S;      function tp_KO_N()  = KO_N;
function tp_BAND_S() = BAND_S;    function tp_BAND_N()= BAND_N;
function tp_CAPY()   = CAPY;      function tp_FT_D()  = FT_D;
function tp_RISY()   = RISY;      function tp_RBX()   = RBX;
function tp_RBY()    = RBY;       function tp_PB()    = PB;
function tp_CAP_T()  = CAP_T;     function tp_CAP_W() = CAP_W;
function tp_PINCH()  = PINCH;     function tp_BOLT_DX()= BOLT_DX;
function tp_NANO_OVER_TUBE() = NANO_OVER_TUBE;

// fasteners / inserts / spacers
function tp_M3B()    = M3B;       function tp_CB_D()  = CB_D;
function tp_CB_H()   = CB_H;      function tp_INS_D() = INS_D;
function tp_INS_DEP()= INS_DEP;   function tp_SP_OD() = SP_OD;
function tp_SP_H()   = SP_H;

// level-1 cargo
function tp_RTK_C()  = RTK_C;     function tp_RTK_P() = RTK_P;
function tp_RTK_BRD()= RTK_BRD;   function tp_RTK_H() = RTK_H;
function tp_EG_C()   = EG_C;      function tp_EG_P()  = EG_P;
function tp_EG_BRD() = EG_BRD;    function tp_EG_H()  = EG_H;
function tp_FC_C()   = FC_C;      function tp_FC_P()  = FC_P;
function tp_FC_BRD() = FC_BRD;    function tp_FC_H()  = FC_H;
function tp_EG_INS() = EG_INS;    function tp_FC_INS()= FC_INS;
function tp_RTK_INS()= pat(RTK_C,[RTK_P,RTK_P]);

// RTK tower
function tp_TWR_LEG()= TWR_LEG;   function tp_TWR_H() = TWR_H;
function tp_TWR_T()  = TWR_T;     function tp_TWR()   = TWR;

// fence / cable wall
function tp_WX0()    = WX0;       function tp_WX1()   = WX1;
function tp_WALL_H() = WALL_H;    function tp_SMA_D() = SMA_D;
function tp_SMA_Y()  = SMA_Y;     function tp_SMA_Z() = SMA_Z;
function tp_ZIP_Y()  = ZIP_Y;     function tp_FENCE_SCR() = FENCE_SCR;

// hanging ESP32 / breadboard carrier
function tp_BB()     = BB;        function tp_BB_T()  = BB_T;
function tp_ESP_DROP()= ESP_DROP; function tp_CAR()   = CAR;
function tp_CAR_W()  = CAR_W;     function tp_CAR_T() = CAR_T;
function tp_CAR_EW() = CAR_EW;    function tp_CARM()  = CARM;
function tp_CAR_DEPTH()= CAR_DEPTH;
function tp_BAR_W()  = BAR_W;     function tp_CAR_BAR_X() = CAR_BAR_X;
function tp_CAR_BAR_Y()= CAR_BAR_Y;
