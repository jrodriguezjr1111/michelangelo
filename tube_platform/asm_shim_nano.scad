// ============================================================================
// CyberWing — SHIM: slimrig_mounts/make_nano_tube_plate.scad, namespaced nn_*.
// See asm_shim_tp.scad for why the shims exist.  Renders nothing.
// ============================================================================
include <../slimrig_mounts/make_nano_tube_plate.scad>
part = "none";

module nn_plate()  plate();
module nn_cap()    cap();
module nn_spacer() spacer();

function nn_PL_X()   = PL_X;      // along the tube axis
function nn_PL_W()   = PL_W;      // across the tubes
function nn_PL_T()   = PL_T;
function nn_ST_L()   = ST_L;      function nn_ST_DEP() = ST_DEP;
function nn_TUBE_Y() = TUBE_Y;    function nn_TUBE_D() = TUBE_D;
function nn_BR()     = BR;        function nn_PINCH()  = PINCH;
function nn_CAP_T()  = CAP_T;     function nn_CAP_W()  = CAP_W;
function nn_BOLT_DY()= BOLT_DY;
function nn_NANO_X() = NANO_X;    function nn_NANO_Y() = NANO_Y;
function nn_BRD_L()  = BRD_L;     // 100, across the tubes
function nn_BRD_W()  = BRD_W;     // 80, along the tube axis
function nn_SP_H()   = SP_H;      function nn_SP_OD()  = SP_OD;
function nn_INS_D()  = INS_D;     function nn_M3B()    = M3B;
