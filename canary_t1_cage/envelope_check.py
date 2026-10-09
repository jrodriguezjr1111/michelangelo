#!/usr/bin/env python3
"""
canary_t1_cage — ENVELOPE / LOAD / THERMAL FEASIBILITY  (concept study)

Methodology copied from im2050_system / skidframe / orin_tactical_case
envelope_check.py: total the real envelopes against the real constraints, tag
every number by provenance, and refuse to call anything feasible until the
arithmetic closes.   MEAS / PUB / EST / DSN — see t1_params.py.

This is an INPUT KIT for the owner + Andrew.  It scores three massing concepts
(A cartridge rack, B open book, C rod pods); it does not pick the design.

Usage:  python3 envelope_check.py        exit 0 = every hard check closes
"""
from __future__ import annotations
import math, sys
import t1_params as P

G = 9.81
fails: list[str] = []
warns: list[str] = []


def need(c, msg):
    if not c:
        fails.append(msg)


def warn(c, msg):
    if not c:
        warns.append(msg)


def rule(ch="-", n=86):
    print(ch * n)


def head(t):
    print(); rule("="); print("  " + t); rule("=")


# ===========================================================================
head("[1] INVENTORY — what flies in the T1 (bare Orin; alu case + Perch stack are OUT)")
print("  %-22s %22s %7s %6s  %s" % ("component", "L x W x H  mm", "g", "W", "tag"))
rule()
m_elec = p_tot = 0.0
for k, (L, W, H, g, w, tag, _n) in P.COMPONENTS.items():
    print("  %-22s %7.2f x %6.2f x %5.2f %7.0f %6.2f  %s" % (k, L, W, H, g, w, tag))
    m_elec += g; p_tot += w
m_elec += P.PDB[3] + P.HARNESS_G
print("  %-22s %22s %7.0f %6s  EST" % ("power dist + harness", "", P.PDB[3] + P.HARNESS_G, ""))
rule()
print("  electronics + harness  %6.0f g      dissipation %5.1f W sustained" % (m_elec, p_tot))
print("  rods 2 x %.0f mm O15x%.0f Al  %4.0f g  EST" % (P.ROD_L, P.TUBE_WALL, P.ROD_G))
hub_share = P.COMPONENTS["EST_uhr204_hub"][3] / m_elec
print("\n  >> The UHR204 hub is %.0f %% of the electronics mass (0.64 kg datasheet line," % (100 * hub_share))
print("     shared with the 7-port model -> EST-high) and the LARGEST footprint in the box")
print("     (139 x 87).  It is there for its 15 N high-retention ports.  See README item 1.")

# ===========================================================================
head("[2] SIZE CLASS  vs  printer bed, Pelican 1400, Cessna 172")
bed_use = P.BED[0] - 2 * P.BED_MARGIN
print("  QIDI Plus 4 bed %.0f x %.0f (PUB); usable with brim/arrange margin %.0f  (DSN %.0f/side)"
      % (P.BED[0], P.BED[1], bed_use, P.BED_MARGIN))
print("  Pelican 1400 exterior 339 x 295 x 152, ~1.8 kg empty (PUB) -> 15.2 L")
print()
print("  %-18s %18s %8s %22s %s" % ("concept", "body X x Y x Z", "litres", "overall incl. rods", "longest part / bed"))
rule()
for k, c in P.CONCEPTS.items():
    bx, by, bz = c["body"]
    fits = c["longest"] <= bed_use
    print("  %s %-15s %5.0f x %4.0f x %4.0f %8.1f %8.0f x %4.0f x %4.0f   %3.0f  %s"
          % (k, c["name"], bx, by, bz, bx * by * bz / 1e6, *c["overall"], c["longest"],
             "fits in one piece" if fits else "NEEDS A DESIGNED SEAM (> %.0f)" % bed_use))
    c["seam"] = not fits
print()
print("  C172 (POH-class figures — verify for the tail): baggage door ~387 x 559 mm,")
print("  baggage area 1 limit 120 lb (54 kg); rear bench ~1.0 m wide.  Every concept passes")
print("  through the door and is < 8 % of the baggage limit; NONE is size-critical in the")
print("  aircraft.  The binding size constraint is the PRINTER BED, not the Cessna.")

# ===========================================================================
head("[3] PRINTED MASS / PRINT-EFFORT CLASS  (class estimate, +/-30 %; nothing sliced)")
print("  model: exterior area x skin t x solidity + extras;  sliced = CAD x %.2f;" % P.FILL)
print("  hours = sliced cm3 x %.3f h/cm3 (orin_tactical_case ASA, 359 cm3 = 37.85 h)" % P.H_PER_CM3)
print()
print("  %-18s %9s %9s %9s %8s %7s %9s" % ("concept", "skin cm3", "extra cm3", "sliced", "ASA g", "hours", "plates@10h"))
rule()
for k, c in P.CONCEPTS.items():
    bx, by, bz = c["body"]
    if k in ("D", "E"):   # structure is extrusion: no skin; frame mass added below
        area = 0.0
    elif k == "C":      # eight pods, not one shell: sum the pod shells
        pods = [(112, 120, 50), (82, 120, 74), (64, 120, 40), (148, 120, 46),
                (52, 120, 26), (44, 120, 26), (30, 120, 26)]
        area = sum(2 * (a * b + a * h + b * h) for a, b, h in pods) + 8 * 2 * 96 * 60
    else:
        area = 2 * (bx * by + bx * bz + by * bz)
    skin = area * c["skin_t"] * c["open"] / 1000
    sl = (skin + c["extras_cm3"]) * P.FILL
    c["print_g"] = sl * P.RHO["ASA"]
    c["hours"] = sl * P.H_PER_CM3
    print("  %s %-15s %9.0f %9.0f %9.0f %8.0f %7.0f %9.0f"
          % (k, c["name"], skin, c["extras_cm3"], sl, c["print_g"], c["hours"], math.ceil(c["hours"] / 10)))
print()
print("  %-18s %8s %8s %8s %8s   vs Pelican build ~3.1 kg (canary BOM)" % ("GROSS (g)", "elec", "rods", "print", "TOTAL"))
rule()
for k, c in P.CONCEPTS.items():
    c["frame_g"] = 0.0
    if k == "D":
        S = P.SERIES[20]; cl = P.d_cutlist(20)
        mm = sum(n * L for _, n, L in cl)
        c["frame_g"] = mm * S["g_per_mm"] + 24 * S["bracket_g"] + 40 * S["tnut_g"] + 64 * 2.5   # + M5 screws
        c["frame_mm"] = mm
    if k == "E":
        S = P.SERIES[20]; cl = P.e_cutlist(20)
        mm = sum(n * L for _, n, L in cl)
        # owner's 4 corner L-gussets (43 g class) + 2 T-gussets (42) + 8 post brackets + ~40 T-nuts + screws
        c["frame_g"] = mm * S["g_per_mm"] + 4 * 43 + 2 * 42 + 8 * S["bracket_g"] + 40 * S["tnut_g"] + 60 * 2.5
        c["frame_mm"] = mm
        c["vplate_g"] = 150.0   # EST_ COTS V-mount female plate with D-Tap
    c["gross"] = m_elec + P.ROD_G + c["print_g"] + c["frame_g"] + c.get("vplate_g", 0) + 120      # +120 g hardware
    print("  %s %-15s %8.0f %8.0f %8.0f %8.0f   %s" % (k, c["name"], m_elec, P.ROD_G, c["print_g"], c["gross"],
          ("frame %.0f g (%.2f m of 20-2020 + 24 brackets + 40 T-nuts + screws)" % (c["frame_g"], c["frame_mm"]/1000)) if k == "D" else
          ("frame %.0f g (%.2f m incl. 4 posts, gussets, T-nuts) + V-plate %.0f g" % (c["frame_g"], c["frame_mm"]/1000, c["vplate_g"])) if k == "E" else ""))
    need(c["gross"] < 5000, "%s gross over 5 kg" % k)
    warn(c["gross"] <= 3700, "%s gross %.0f g exceeds R7.2 (3.7 kg)" % (k, c["gross"]))

# ---- concept D: the frame (DECIDED 2026-09-21: 80/20 20-series, black anodized)
head("[3b] CONCEPT D — 80/20 20-series frame: cut list, mass, cost class")
D = P.CONCEPTS["D"]; S = P.SERIES[20]; cl = P.d_cutlist(20); mm = sum(n * L for _, n, L in cl)
print("  profile %s  %s  %.4f g/mm  A=%.0f mm2  I=%.0f mm4  slot %.1f x %.1f deep  bolt %s"
      % (S["part"], S["alloy"], S["g_per_mm"], S["area_mm2"], S["I_mm4"], S["slot"], S["slot_depth"], S["bolt"]))
print("  cut list %.2f m: " % (mm/1000) + ", ".join("%dx%.0f %s" % (n, L, nm) for nm, n, L in cl))
fg = D["frame_g"]
print("  frame mass: extrusion %.0f g + 24 brackets %.0f g + 40 T-nuts %.0f g + ~64 M5 screws %.0f g = %.0f g"
      % (mm * S["g_per_mm"], 24 * S["bracket_g"], 40 * S["tnut_g"], 64 * 2.5, fg))
print("  extrusion cost class: %.2f m x $%.4f/mm = $%.0f (Black-FB, extended anodizing lead time; plain 20-2020 for the fit frame)"
      % (mm/1000, S["usd_per_mm"], mm * S["usd_per_mm"]))
hub = P.COMPONENTS["EST_uhr204_hub"][3]
print("\n  >> gross %.0f g vs R7.2 3700 g: %s.  Dropping the UHR204 hub (-%.0f g) -> %.0f g %s R7.2."
      % (D["gross"], "OVER" if D["gross"] > 3700 else "ok", hub, D["gross"] - hub, "meets" if D["gross"] - hub <= 3700 else "still over"))
print("  >> vs concept A's printed shell (%.0f g): the frame + D's printed parts (%.0f g) cost +%.0f g for a native metal restraint path."
      % (P.CONCEPTS["A"]["print_g"], fg + D["print_g"], fg + D["print_g"] - P.CONCEPTS["A"]["print_g"]))
print("  >> 15-series (Misumi HFS3-1515, 0.34 kg/m, I=2800, slot 3.4, M3) was considered: it saves only ~%.0f g of frame,"
      % (mm * (S["g_per_mm"] - 0.34) + 24*5 + 40*3))
print("     gives 41 % of the stiffness, a 3.0 mm printed key neck, and M3 sheet brackets rated 160 N.  20-series won.")

print("\n  T-KEY IN THE SLOT — the load-bearing detail (printed ASA key on the cartridge side, riding the mullion slot)")
neck = S["slot"] - 0.4; headw = S["cavity"] - 0.6; L = 88.0; F = 0.74 * G * 18 / 2
print("    key: neck %.1f wide (%.0f lines of 0.4) x %.0f engaged, head %.1f wide x 2.0 thick in the %.1f cavity, 1.0 lead chamfer"
      % (neck, neck / 0.4, L, headw, S["cavity"]))
print("    worst load (battery-class 131 N at 18 g, 2 keys): neck shear %.2f MPa, slot-lip bearing %.2f MPa  (ASA allow 5 / 10)"
      % (F / (neck * L), F / (S["slot_depth"] * L)))
print("    print: key printed WITH the cartridge, neck vertical = layer lines ALONG the neck (shear across layers is never loaded)")
print("    why 6 mm matters: a 5.6 mm neck (14 lines) carries a 1.0 mm lead chamfer and survives a dropped cartridge;")
print("    a 3.0 mm neck (15-series) is 7 lines, chips on insertion, and its 5.1 x 2 head is thinner than two walls.")
print("    vs mini ball-bearing slides (Accuride/Sugatsune 100-150 mm): +40-80 g and +4 screws per bay, a 10-13 mm side")
print("    gap, steel in a hot cabin, and RATTLE unless detented; they earn their place only for a full-extension drawer")
print("    heavier than ~1 kg.  Nothing here is.  The T-slot is already the rail: zero added parts, zero gap.")

print("\n  HOT PRELOAD IN PLASTIC — what remains in concept D")
print("    rods -> frame: canon caps still printed, but the rods are handle + antenna rail only; the belt goes round")
print("                   the frame's bottom long members (metal, native).  R2.2 / R2.3 satisfied by the extrusion.")
print("    cartridge:     M5 captive thumbscrew -> steel T-nut in the mullion = metal-to-metal preload; the ASA")
print("                   faceplate is only CLAMPED (washer under the head, 0.2 MPa).  Keys carry bearing, not preload.")
print("    IMU seat:      the one place plastic would sit under M5 preload -> machined Al seat (or PA12-CF + washers).")
print("    battery:       latch = M5 thumbscrew into a T-nut (metal); strap round a frame member (metal).")
print("    => nothing structural depends on printed preload.  Print creep can only loosen a label plate.")

print("\n  BOLTED T-SLOT JOINTS UNDER VIBRATION")
print("    20-series M5 (8.8, steel T-nut): 4.5 N.m + Loctite 243 + torque-stripe; ~2 kN/joint. 24 brackets x 2 = 48 joints.")
print("    a corner sees up to %.0f N at 18 g -> one M5 joint carries it with >10x; the T-nut thread is steel, not Al." % (646/4))
print("    rule: every bracket screw torque-striped after Loctite; re-check at the first 10 h and every 50 h (vibration).")
print("    Mullion cantilever 100 mm under 65 N: delta = FL^3/3EI = %.3f mm — the extrusion does not notice." % (65*100**3/(3*70000*6826)))


# ===========================================================================
head("[4] LOAD CASES — secured carry-on, NOT an installation")
LC = {
    "flight +3.8 g x1.5 (down)": (0, 0, -5.70),
    "flight -1.52 g x1.5 (up)": (0, 0, 2.28),
    "emergency fwd 9 g  (CAR 3.386 / 23.561 classic, ultimate)": (9.0, 0, 0),
    "emergency up 3 g": (0, 0, 3.0),
    "emergency side 1.5 g": (0, 1.5, 0),
    "fwd 18 g (23.561(b)(3) later amdt, items of mass in cabin) — margin case": (18.0, 0, 0),
    "handling: carried by the rods, 3 g swing": (0, 0, -3.0),
}
M = max(c["gross"] for c in P.CONCEPTS.values()) / 1000
print("  design gross (heaviest concept) M = %.2f kg" % M)
for n, (gx, gy, gz) in LC.items():
    print("    %-74s F = %6.0f N" % (n, M * G * max(abs(gx), abs(gy), abs(gz))))

F9, F18, Fup, Fcarry = M * G * 9, M * G * 18, M * G * 3, M * G * 3

print("\n  (a) RESTRAINT PATH — belt / straps go round the RODS (metal), never a printed lug")
A_t = math.pi * ((P.TUBE_D / 2) ** 2 - (P.TUBE_D / 2 - P.TUBE_WALL) ** 2)
I_t = math.pi / 64 * (P.TUBE_D ** 4 - (P.TUBE_D - 2 * P.TUBE_WALL) ** 4)
span = 230.0
Mb = (F18 / 2) * span / 4
sig = Mb * (P.TUBE_D / 2) / I_t
print("      rod O15x%.0f 6061 (EST wall): A=%.0f mm2  I=%.0f mm4" % (P.TUBE_WALL, A_t, I_t))
print("      worst case 18 g taken as a mid-span transverse load, %0.f mm between yokes, 2 rods:" % span)
print("      M = %.0f N.mm/rod  ->  sigma = %.0f MPa  vs 6061-T6 yield ~240  -> MS = %.1f"
      % (Mb, sig, 240 / sig - 1))
need(sig < 240 / 1.5, "rod bending over allowable")
print("      seat belt webbing rated >= 6.7 kN (TSO-C22 class) vs %.0f N: not the limit." % F18)

print("\n  (b) ROD -> PRINT TRANSFER at the canon troughs")
n_st = 4
brg = n_st * 20 * P.TUBE_D          # projected trough bearing, 4 stations x 20 mm cap width
print("      transverse: %d stations x 20 x %.0f projected = %d mm2 -> %.2f MPa at 18 g"
      % (n_st, P.TUBE_D, brg, F18 / brg))
print("      AXIAL (along the rods, = the 9 g direction): canon clamp is FRICTION ONLY.")
pre = 0.6 / (0.2 * 0.003)
print("        fresh: 8 x M3 @0.6 N.m -> ~%.0f N each, mu 0.25 -> %.0f N slip  vs %.0f N (9 g): OK cold"
      % (pre, 8 * pre * 0.25, F9))
print("        hot + 6 months: ASA/PA creep relaxes clamp preload -> CANNOT be counted on.")
print("        => REQUIREMENT: positive axial stop in metal — O15 split shaft collars each side")
print("           of one yoke, or M12 end-screws + washers in the rod ends (SmallRig rods are")
print("           M12-threaded — CONFIRM).  Collar face on a yoke: %.2f MPa at 18 g."
      % (F18 / (2 * math.pi * (14 ** 2 - 7.7 ** 2))))

print("\n  (c) CARRY LOAD (concept A, rods on top): rod pulls UP on the canon caps")
per = Fcarry / (4 * 2)
print("      %.0f N / (4 caps x 2 M3) = %.1f N per heat-set insert in tension" % (Fcarry, per))
print("      M3 brass heat-set pull-out in ASA ~ 400 N cold, take 150 N hot/aged -> MS = %.0f" % (150 / per - 1))
need(per < 150 / 3, "cap insert pull-out margin < 3")

bat = P.COMPONENTS["EST_vmount_battery"][3] / 1000 + 0.10      # + cartridge/carrier
print("\n  (d) HEAVIEST SWAPPABLE ITEM — battery + carrier = %.2f kg" % bat)
print("      9 g -> %.0f N     18 g -> %.0f N     3 g up -> %.0f N     1.5 g side -> %.0f N"
      % (bat * G * 9, bat * G * 18, bat * G * 3, bat * G * 1.5))
print("      A  cartridge slides ALONG Y: the 9 g fore-aft load goes into the bay walls in")
print("         bearing (107 x 64 face -> %.3f MPa); the single thumbscrew sees only the side case"
      % (bat * G * 18 / (107 * 64)))
print("         ... IF the unit is belted rods-fore-aft.  A CFI will turn it 90 deg one day, so:")
print("      => REQUIREMENT: latch AND secondary strap EACH hold 18 g x %.2f kg = %.0f N in ANY axis."
      % (bat, bat * G * 18))
print("         one M4 captive thumbscrew into a heat-set: ~600 N cold / ~250 N hot -> MS = %.1f"
      % (250 / (bat * G * 18) - 1))
arm, base = 36.0, 110.0
print("      B  carrier on the grid, 2 x M3 thumbscrews: shear %.0f N each at 18 g; bearing on a 4 mm"
      % (bat * G * 18 / 2))
print("         carrier %.1f MPa; overturning (CG %.0f above, %.0f screw spread) -> %.0f N pull-out each"
      % (bat * G * 18 / 2 / (3 * 4), arm, base, bat * G * 18 * arm / base))
print("      C  pod on the rods: same axial-friction problem as (b), per pod -> every pod needs a")
print("         positive axial key (collar or a pin through a rod hole) or pods stack end-to-end")
print("         against one collared datum so the 9 g load is carried in COMPRESSION pod-to-pod.")

print("\n  (e) PRINT ALLOWABLES used above (conservative, hot + aged + FDM knock-down)")
print("      ASA      XY 40 MPa, interlayer ~20 -> allowable 5 MPa interlayer tension, 10 MPa bearing")
print("      PA12-CF  XY ~85 MPa, interlayer ~30, HDT >150 C, but hygroscopic (dry + recondition)")
print("      Every number in (a)-(d) is 1-2 orders under these.  STRENGTH IS NOT THE PROBLEM;")
print("      creep of clamped/threaded joints at cabin-soak temperature is.  Design for that.")

# ===========================================================================
head("[4E] CONCEPT E — flat 406 x 279 deck: restraint, rods, trays")
CE = P.CONCEPTS["E"]; ME = CE["gross"] / 1000
print("  gross %.2f kg  (electronics %.0f g, deck+posts %.0f g, trays/yokes %.0f g, rods %.0f g, V-plate %.0f g, hw 120)"
      % (ME, m_elec, CE["frame_g"], CE["print_g"], P.ROD_G, CE["vplate_g"]))
F18e, F9e, F3e = ME * G * 18, ME * G * 9, ME * G * 3
print("  18 g fwd %.0f N   9 g fwd %.0f N   3 g carry %.0f N" % (F18e, F9e, F3e))
print("  (a) LAP BELT over the battery in the y100-172 band + two cargo straps looped round BOTH long members (E01/E02)")
print("      at x = 100 / 306: 18 g fwd = %.0f N shared by two 2020 members in bending over a 30 mm strap width -" % F18e)
print("      the strap bears on the member face: %.2f MPa on 6063 (172 yield). The trays' strap slots keep the strap off plastic." % (F18e / (2 * 30 * 20)))
print("      Belt/strap load never enters a printed part: R2.2 native.  No printed clamp in the axial path: R2.3 native.")
print("  (b) 3 g SWING carried by the rods: %.0f N -> 4 canon caps x 2 M3 = %.1f N per insert in the printed yoke bridge" % (F3e, F3e / 8))
print("      (MS %.0f vs 150 N hot) — but the bridge itself hangs on 2 x M5 into each 2020 post: %.0f N per post pair, fine." % (150 / (F3e / 8) - 1, F3e / 2))
print("      The rods are handle + antenna rail + lid carrier only; they are NOT in the restraint path.")
print("  (c) HEAVIEST ITEM = battery %.2f kg on its V-plate: V-lock latch (COTS, ~2 kN class) + the lap belt directly over it" % (P.COMPONENTS["EST_vmount_battery"][3] / 1000))
print("      + a secondary strap round the pack: 18 g = %.0f N in any axis, R2.4 met three ways." % (P.COMPONENTS["EST_vmount_battery"][3] / 1000 * G * 18))
print("  (d) TRAYS as stressed skin: a bare 2020 picture frame racks about its bracket joints (torsion J ~ 2I = %.0f mm4 per member)." % (2 * 6826))
print("      Two 4 mm ASA skins over 173 x 239 add in-plane shear stiffness G.t = 0.7 GPa x 4 = 2.8 kN/mm per mm width each;")
print("      the deck goes from 'four brackets in bending' to a shear panel: racking stiffness up by an order of magnitude class,")
print("      which is why the trays are full-bay-width and bolted on all four sides (M5 + T-nuts, thumbscrews on bay R).")
print("      Centre member: KEEP — it halves the tray span (173 not 366), gives a mid-line bolt row, two prints under 281 mm.")
print("  (e) Tray PRINT: 4 mm skin + 9 mm ribs, ASA (PLA never flies; a 60 C cabin sags a 173 mm PLA span under a 640 g hub).")
print("      Each tray ~%.0f cm3 sliced class, ~%.0f h; nothing longer than 239 mm." % (173*239*4*0.7/1000*0.85 + 60, (173*239*4*0.7/1000*0.85 + 60) * P.H_PER_CM3))

# ===========================================================================
head("[4E-C] CONCEPT E REV C — full-height cage (posts to a top 406 x 279 rectangle)")
S = P.SERIES[20]; RL = P.ROD_LEVEL_C; DM = P.DOME; MA = P.MA963
E_ = 20.0; DXE, DYE = 406.0, 279.0
dome_top = P.ROD_Z + 7.7 + DM["puck_h"] + DM["H"]
post_c = math.ceil(dome_top + RL["top_clr"] - E_ - (E_ + 3))          # shortest whole-mm post (mirrors the scad)
top_z0 = E_ + 3 + post_c; top_top = top_z0 + E_; overall = top_top + 3
pc_z = P.ROD_Z + 7.7 + DM["puck_h"] + DM["PC"]
ma_clamp = P.ROD_Z + MA["st_dep"] + MA["plate"][2] + MA["clamp_top"]
ma_ref = P.ROD_Z + MA["st_dep"] + MA["plate"][2] + MA["H"] / 2
whip_top = RL["whip_base"] + RL["whip_h"]
print("  post %d mm (shortest whole mm with the dome top %.0f under the rail top), top-rail top z %.0f, overall %.0f incl. top gussets"
      % (post_c, RL["top_clr"], top_top, overall))
for nm, z in (("dome (EST)", dome_top), ("MA963 corner clamps", ma_clamp), ("1090/978 stubbies", whip_top)):
    print("    %-20s top z %6.1f  -> %5.1f under the top-rail top" % (nm, z, top_top - z))
    need(top_top - z >= RL["top_clr"], "rev C: %s within %.0f mm of the top rails" % (nm, RL["top_clr"]))
print("  C172 baggage door 387 x 559: cage %.0f x %.0f x %.0f -> passes long axis first, %.0f / %.0f mm spare"
      % (DXE, DYE, overall, 387 - max(DYE, overall), 559 - min(DYE, overall)))
need(max(DYE, overall) < 387 and DXE < 1000, "rev C does not pass the baggage door")

print("\n  (a) GNSS MASK = atan(rail-top height above the reference / horizontal distance to the rail's inner face)")
def d_in(i, cx):
    return (DYE / 2 - E_) if i < 2 else ((cx - E_) if i == 2 else (DXE - E_ - cx))
rails = ["y=0 long", "y=279 long", "x=0 end", "x=406 end"]
for nm, cx, zr in (("dome L1 PC (EST)", RL["dome_cx"], pc_z), ("MA963 mid-housing", RL["ma963_cx"], ma_ref)):
    h = top_top - zr
    a = [math.degrees(math.atan(h / d_in(i, cx))) for i in range(4)]
    lo = [math.degrees(math.atan((top_z0 - zr) / (d_in(i, cx) + E_))) for i in range(4)]
    print("      %-18s z %5.1f x %3.0f, rail top +%4.1f:  " % (nm, zr, cx, h)
          + "  ".join("%s %4.1f (band from %4.1f)" % (rails[i], a[i], lo[i]) for i in range(4)))
print("      vs a 10-15 deg RTK elevation mask: the dome's shadow bands top out at 18.8 / 18.8 / 9.0 / 20.4 deg -> the cage")
print("      shadows sky ABOVE a 15 deg mask in three of four directions.  h cannot drop below dome (H-PC) + 15 = %.0f mm, and" % (DM["H"] - DM["PC"] + RL["top_clr"]))
print("      d is capped at %.1f by the 279 deck, so no rev C geometry reaches <= 15 deg fore/aft (needs d >= %.0f)."
      % (DYE / 2 - E_, (DM["H"] - DM["PC"] + RL["top_clr"]) / math.tan(math.radians(15))))
print("      MA963 has NO GNSS element (LTE/Wi-Fi, towers at or below the horizon from altitude): its 17-44 deg numbers do not bite.")

print("\n  (b) MASS — what rev C adds to rev B (antennas are NOT in either gross; listed separately)")
cl = P.e_cutlist_C(20, post_c)
mm_c = sum(n * L for _, n, L in cl); mm_b = sum(n * L for _, n, L in P.e_cutlist(20))
n_brk, n_gus, n_gus_bolt = 8, 4, 5 * 4
add = dict(extrusion=(mm_c - mm_b) * S["g_per_mm"], gussets=n_gus * 43.0, brackets=n_brk * S["bracket_g"],
           fasteners=(2 * n_brk + n_gus_bolt) * (S["tnut_g"] + 2.5))
d_mass = sum(add.values())
CE = P.CONCEPTS["E"]; gross_c = CE["gross"] + d_mass
print("      +%.0f mm of 20-2020 (%s)" % (mm_c - mm_b, ", ".join("%dx%.0f" % (n, L) for nm, n, L in cl[3:])))
print("      " + "  ".join("%s +%.0f g" % kv for kv in add.items()) + "   =  +%.0f g" % d_mass)
print("      gross rev B %.0f g -> rev C %.0f g   (rod-level payload on both, not in gross: MA963 %.0f + plate %.0f + dome %.0f EST + puck %.0f"
      " + CO tray %.0f + whips %.0f = %.0f g)" % (CE["gross"], gross_c, MA["mass_g"], MA["hw_g"], DM["mass_g"], DM["puck_g"], RL["co_g"], RL["whips_g"],
         MA["mass_g"] + MA["hw_g"] + DM["mass_g"] + DM["puck_g"] + RL["co_g"] + RL["whips_g"]))
warn(gross_c <= 5000, "E rev C gross %.0f g is OVER the 5 kg bound the concept table is held to (R7.2 ceiling still to be restated by the owner)" % gross_c)

print("\n  (c) RESTRAINT — PICK: lap belt + 2 cargo straps round the BOTTOM long members (unchanged from rev B), never the top rails")
F18c = gross_c / 1000 * G * 18
print("      18 g fwd at rev C gross = %.0f N; strap bearing on the 6063 long members %.2f MPa (172 yield)." % (F18c, F18c / (2 * 30 * 20)))
z_cg = 70.0   # EST gross CG height: battery / hub / Orin low, rod level + top ring high
arm = top_top - 10 - z_cg
print("      Why not the top rails: a strap there sits ~%.0f mm above the CG (z ~%.0f EST); 18 g x that arm = %.0f N.m, reacted by the"
      % (arm, z_cg, F18c * arm / 1000))
print("      eight post-end bracket joints in bending (~%.1f kN bolt tension per foot, 20 mm heel lever) instead of the straps bearing"
      % (F18c * arm / 1000 / 4 / 0.020 / 1000))
print("      on metal at the deck; and the belt would ride over the dome's sky.  The top rails are the CARRY HANDLE (3 g) only.")
up_g = (2 * DXE + 2 * (DYE - 2 * E_)) * S["g_per_mm"] + add["gussets"] + add["brackets"] + add["fasteners"] \
    + 4 * post_c / 2 * S["g_per_mm"] + P.ROD_G + RL["yokes_g"] + MA["mass_g"] + MA["hw_g"] + DM["mass_g"] + DM["puck_g"] + RL["co_g"] + RL["whips_g"]
V = up_g / 1000 * G * 18 / 4
M_cant = V * post_c / 1000
T_bolt = M_cant / 0.020
print("      Mass carried BY the posts (top ring + half posts + rod level incl. antennas) %.0f g -> 18 g: %.0f N per post;" % (up_g, V))
print("      post-foot moment %.1f N.m cantilever (upper bound) / %.1f portal -> bracket bolt %.2f / %.2f kN vs ~2 kN class:"
      % (M_cant, M_cant / 2, T_bolt / 1000, T_bolt / 2000))
print("      MS %.1f / %.1f at 18 g; at the 9 g classic case MS %.1f / %.1f.  Torque-stripe + 10 h re-check (R6.6) now matters here."
      % (2000 / T_bolt - 1, 4000 / T_bolt - 1, 4000 / T_bolt - 1, 8000 / T_bolt - 1))
need(2000 / T_bolt - 1 > 0, "rev C post-foot joints over the 2 kN class at 18 g")
k1 = 3 * 70000 * S["I_mm4"] / post_c ** 3; k2 = 4 * k1
f_c = math.sqrt(4 * k1 * 1000 / (up_g / 1000)) / (2 * math.pi); f_p = math.sqrt(4 * k2 * 1000 / (up_g / 1000)) / (2 * math.pi)
print("      sway mode of the upper mass on 4 posts: ~%.0f Hz (cantilever) to ~%.0f Hz (portal), before joint compliance - it brackets the"
      % (f_c, f_p))
print("      C172 2-blade prop / 4-cyl firing ~80 Hz at 2400 rpm (rev B's 100 mm posts: ~%.0f Hz).  The seat/belt mount isolates well below this,"
      % (math.sqrt(4 * 3 * 70000 * S["I_mm4"] / 100 ** 3 * 1000 / ((P.ROD_G + RL["yokes_g"] + MA["mass_g"] + MA["hw_g"] + DM["mass_g"] + DM["puck_g"] + RL["co_g"] + RL["whips_g"]) / 1000)) / (2 * math.pi)))
print("      but it is a structures-engineer check before flight: add the vib node on the top rail for one ground run.")

print("\n  (d) TRAY / COMPONENT EXIT — through the SIDE windows, not the top")
print("      top opening inside the top rails %.0f x %.0f; a tray with its 10 mm member flanges is %.0f x %.0f -> it cannot go straight up"
      % (DXE - 2 * E_, DYE - 2 * E_, 173 + 20, DYE - 2 * E_ + 20))
print("      (and in rev B the rod pair already spans both bays at z %.0f with 44.6 mm between the rods, so 'lift out the top' was never true"
      % (P.ROD_Z - 7.5))
print("      with the rods fitted).  Real path, both revs: undo the tray bolts, lift %d mm, slide out a long-face window between the posts:"
      % 12)
win_h = top_z0 - E_
bat_top = E_ + 4 + 10 + 64
print("      window %.0f wide x %.0f tall; bay-L tray + battery tops at z %.0f vs the lowest rod-level part over it z %.1f (MA963 caps);"
      % (DXE - 2 * E_, win_h, bat_top + 12, P.ROD_Z - 10))
print("      bay-R tray tallest item (Orin) at z %.0f vs the CO tray underside z %.1f.  Side rails at z ~%.0f do not cross this path."
      % (E_ + 4 + 6 + 36 + 12, P.ROD_Z - 44.62, P.ROD_Z + 50))
need(bat_top + 12 <= P.ROD_Z - 10 - 10 and E_ + 4 + 6 + 36 + 12 <= P.ROD_Z - 44.62 - 10, "rev C side-exit path blocked")
print("      Carry: by the top rails, all metal -> posts in tension -> deck: %.0f N at 3 g, no printed part in the carry path (rev B: canon caps)."
      % (gross_c / 1000 * G * 3))
CE["gross_C"] = gross_c; CE["d_mass_C"] = d_mass; CE["post_C"] = post_c

# ===========================================================================
head("[5] THERMAL — sealed is impossible here too; design the airflow")
U = 2.3            # W/m2K overall, natural convection + radiation through a printed wall
print("  sustained dissipation %.1f W (EST);  U = %.1f W/m2K (orin_tactical_case method)" % (p_tot, U))
print("  %-18s %9s %12s %14s" % ("concept, SEALED", "area m2", "dT K", "interior @35 C"))
rule()
for k, c in P.CONCEPTS.items():
    bx, by, bz = c["body"]
    a = 2 * (bx * by + bx * bz + by * bz) / 1e6
    dT = p_tot / (U * a)
    print("  %s %-15s %9.3f %12.0f %12.0f C" % (k, c["name"], a, dT, 35 + dT))
    need(True, "")
print("  limits: Li-ion 45 C charge / 60 C discharge, Orin ~50 C ambient, PLA Tg 60, ASA Tg ~100")
print("  -> a sealed shell exceeds the battery limit in EVERY concept.  C has no shell (free).")
fan_cm2 = math.pi * (20 ** 2 - 8 ** 2) / 100
flow = 2.4e-3      # m3/s ~ 5 CFM, EST for a 40 mm dev-kit fan in a ducted box
dTair = p_tot / (1.2 * 1005 * flow)
print("\n  vented: dev-kit fan throat ~%.1f cm2 (EST O40) -> house rule >= 3x = %.0f cm2 EACH of" % (fan_cm2, 3 * fan_cm2))
print("  intake and exhaust.  At ~5 CFM (EST) bulk air rise = %.1f K  -> interior ~%.0f C at 35 C."
      % (dTair, 35 + dTair))
print("  RULES: fan intake ducted to an exterior grille (no recirculation); exhaust on a")
print("  DIFFERENT face; the battery sits UPSTREAM of or outside the Orin's exhaust, behind a")
print("  partition; nothing printed within the fan keep-out.  Parked-cabin soak (60-70 C) is an")
print("  unpowered SURVIVAL case for the material, not an operating case.")

# ===========================================================================
head("[6] SWAP ARITHMETIC — steps and tools to get one failed peripheral out")
SW = [  # concept, item, steps, tools, note
    ("A", "peripheral cartridge", 3, 0, "thumbscrew - pull - unlock pigtail at the patch point"),
    ("A", "battery cartridge", 3, 0, "release strap - thumbscrew - pull (blind-mate or short lead)"),
    ("A", "Core (Orin/hub)", 8, 0, "4 lid thumbscrews - slide lid out under the rods - unplug - 4 M3"),
    ("A", "IMU", 3, 0, "2 captive screws + 1 locking connector; RE-CAL REQUIRED"),
    ("B", "any carrier", 4, 0, "2 lid screws - 2 carrier thumbscrews - unlock pigtail - lift"),
    ("B", "IMU", 5, 0, "lid + 2 captive screws + connector; RE-CAL REQUIRED"),
    ("C", "any pod", 6, 1, "unlock trunk connector - 4 cap screws (hex key unless knurled) - lift"),
    ("C", "IMU", 3, 0, "2 captive screws + connector; RE-CAL REQUIRED"),
    ("D", "peripheral cartridge", 3, 0, "thumbscrew - lift out of the mullion slots - unlock pigtail"),
    ("D", "battery cartridge", 3, 0, "strap - thumbscrew - slide out along X"),
    ("D", "Core (Orin/hub)", 3, 0, "thumbscrew - slide the tray out the -X end on the bottom longs' slots - unplug (fixed layout)"),
    ("D", "IMU", 3, 0, "2 captive M5 into the rear Al yoke plate pocket + connector; dowel = key; RE-CAL REQUIRED"),
    ("E", "any board on a tray", 4, 0, "unlock pigtail - 4 thumbscrews (or M3 on standoffs) - lift; tray itself: 6 thumbscrews"),
    ("E", "battery", 1, 0, "V-lock release (+ strap) - the whole point of the V-mount insert"),
    ("E", "Core (Orin/hub)", 3, 0, "everything is on the open top level: unplug - 4 standoff screws - lift; nothing above it but rods"),
    ("E", "IMU", 3, 0, "4 x M2.5 on the corner Al plate + micro-USB clamp; RE-CAL REQUIRED"),
]
print("  %-3s %-22s %6s %6s   %s" % ("", "item", "steps", "tools", "sequence"))
rule()
for c, i, s, t, n in SW:
    print("  %-3s %-22s %6d %6d   %s" % (c, i, s, t, n))
print("\n  T0 removal history (owner): IMU, companion computer, ADS-B receiver, a sensor cable,")
print("  a power monitor.  3 of 5 are PERIPHERALS, 1 is the Core, 1 is a CABLE — so the harness")
print("  must be as swappable as the boxes: every pigtail a separate, labelled, locking part.")

# ===========================================================================
head("VERDICT")
for w_ in warns:
    print("  WARN  " + w_)
fails = [f for f in fails if f]
if fails:
    for f in fails:
        print("  FAIL  " + f)
    sys.exit(1)
print("  Every hard check closes for all five concepts (D/E carry a mass WARN against the old R7.2).")
print("  Strength, size in the aircraft and")
print("  mass are NOT discriminators.  The discriminators are: swap steps, IMU datum rigidity,")
print("  airflow discipline, bed seams, print hours — and the things only T0 experience knows.")
sys.exit(0)
