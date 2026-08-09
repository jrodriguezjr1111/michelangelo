// ============================================================================
// CyberWing — SHIM: slimrig_mounts/make_orin_tube_plate.scad, namespaced oo_*.
// See asm_shim_tp.scad for why the shims exist.  Renders nothing.
// ============================================================================
include <../slimrig_mounts/make_orin_tube_plate.scad>
part = "none";

module oo_plate()  plate();
module oo_cap()    cap();
module oo_spacer() spacer();

function oo_PL_X()   = PL_X;      // along the tube axis
function oo_PL_W()   = PL_W;      // across the tubes
function oo_PL_T()   = PL_T;
function oo_ST_L()   = ST_L;      function oo_ST_DEP() = ST_DEP;
function oo_TUBE_Y() = TUBE_Y;    function oo_TUBE_D() = TUBE_D;
function oo_BR()     = BR;        function oo_PINCH()  = PINCH;
function oo_CAP_T()  = CAP_T;
function oo_ORIN_X() = ORIN_X;    function oo_ORIN_Y() = ORIN_Y;
function oo_BRD_L()  = BRD_L;     // 100, along the tube axis
function oo_BRD_W()  = BRD_W;     //  81, across the tubes
function oo_SP_H()   = SP_H;
