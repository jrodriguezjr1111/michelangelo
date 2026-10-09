"""Verify cad_exchange/*.step are TRUE analytic B-rep (reuses the repo's
slimrig_mounts/verify_step.py reader).  PASS = exactly one closed valid solid,
millimetres, ZERO b-spline/tessellated faces.  (Plain boxes legitimately have
no cylinder faces, so the slimrig 'cylinder > 0' test is not applied here.)

Run:  ../.venv/bin/python verify_step.py        exit 0 = all pass
"""
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "slimrig_mounts"))
import verify_step as V                                   # noqa: E402
from OCP.BRep import BRep_Tool                            # noqa: E402
from OCP.BRepCheck import BRepCheck_Analyzer              # noqa: E402
from OCP.BRepGProp import BRepGProp                       # noqa: E402
from OCP.GProp import GProp_GProps                        # noqa: E402
from OCP.GeomAdaptor import GeomAdaptor_Surface           # noqa: E402
from OCP.IFSelect import IFSelect_ReturnStatus            # noqa: E402
from OCP.STEPControl import STEPControl_Reader            # noqa: E402
from OCP.TopAbs import TopAbs_FACE, TopAbs_SHELL, TopAbs_SOLID  # noqa: E402
from OCP.TopExp import TopExp_Explorer                    # noqa: E402
from OCP.TopoDS import TopoDS                             # noqa: E402

CAD = Path(__file__).parent / "cad_exchange"
bad = 0
print("%-26s %6s %6s %6s %5s  %-28s %12s  %s" % ("file", "solids", "closed", "valid", "unit", "faces plane/cyl/cone/other", "volume mm3", "verdict"))
for f in sorted(CAD.glob("*.step")):
    r = STEPControl_Reader()
    assert r.ReadFile(str(f)) == IFSelect_ReturnStatus.IFSelect_RetDone
    r.TransferRoots(); sh = r.OneShape()
    kinds = Counter()
    e = TopExp_Explorer(sh, TopAbs_FACE)
    while e.More():
        t = GeomAdaptor_Surface(BRep_Tool.Surface_s(TopoDS.Face_s(e.Current()))).GetType()
        kinds[V.SURF.get(t, str(t))] += 1; e.Next()
    closed = []
    e = TopExp_Explorer(sh, TopAbs_SHELL)
    while e.More():
        closed.append(BRep_Tool.IsClosed_s(e.Current())); e.Next()
    gp = GProp_GProps(); BRepGProp.VolumeProperties_s(sh, gp)
    ns = V.count(sh, TopAbs_SOLID); valid = BRepCheck_Analyzer(sh).IsValid()
    txt = f.read_text(errors="ignore").upper()      # whole file: the slimrig helper only scans 60 kB
    unit = "Milli" if "SI_UNIT(.MILLI.,.METRE.)" in txt.replace(" ", "") else "unstated"
    other = sum(v for k, v in kinds.items() if k not in ("plane", "cylinder", "cone"))
    ok = ns == 1 and all(closed) and closed and valid and other == 0 and unit == "Milli"
    bad += not ok
    print("%-26s %6d %6s %6s %5s  %3d / %3d / %3d / %3d %13s %12.1f  %s" % (
        f.name, ns, all(closed), valid, unit, kinds["plane"], kinds["cylinder"], kinds["cone"], other, "",
        gp.Mass(), "PASS" if ok else "FAIL"))
sys.exit(1 if bad else 0)
