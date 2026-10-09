"""
Canary T1 cage — SHARED PARAMETERS (concept study, 2026-09-21).

One table, read by envelope_check.py (arithmetic) and make_t1_concept.py
(reference B-rep).  Nothing is dimensioned in two places.

PROVENANCE TAGS — every number carries one:
  MEAS = caliper-measured by the owner / in-repo record
  PUB  = published vendor datasheet or regulation
  EST  = estimated -> on the CONFIRM list, never to be cut into flight plastic
  DSN  = a design choice made in this concept (an OPTION, not a decision)

Frame:  X = along the rods (fore-aft in the aircraft), Y = lateral, Z = up.
        x = 0 at the seam between the CORE body (-X) and the PACK body (+X);
        y = 0 on the rod-pair centreline; z = 0 at the underside of the floor.
"""

# ---------------------------------------------------------------------------
# 1. COMPONENTS  (L along X, W along Y, H along Z as PLACED in this concept)
# ---------------------------------------------------------------------------
COMPONENTS = {
    # name: (L, W, H, mass_g, dissipation_W, tag, note)
    "orin_devkit": (100.0, 81.0, 36.0, 250.0, 15.0, "MEAS/EST",
        "BARE Jetson Orin dev kit. M3 pattern 91.86 x 58.37 MEAS (pelican_frame "
        "lineage, slimrig_mounts/make_orin_tube_plate.scad); board envelope "
        "~100 x 81 (repo record); height ~36 incl. heatsink + top-draw fan EST; "
        "mass EST. The aluminium-cased Orins were repurposed for T0 (owner, "
        "2026-09-21) and are NOT in the T1."),
    "EST_vmount_battery": (74.0, 107.0, 64.0, 640.0, 1.5, "EST",
        "ZGCINE V99 Pro 99 Wh 4S, 107x74x64 ~640 g per the canary memory bank "
        "(cybernode-power-monitoring, 2026-07-23) — vendor-class figure, not "
        "calipered. Placed 107 along Y so it loads through a SIDE door."),
    "EST_uhr204_hub": (139.0, 87.0, 35.0, 640.0, 2.0, "PUB/EST",
        "Advantech BB-UHR204: mech drawing 13.9 x 8.7 x 3.5 cm, 10-30 VDC, "
        "high-retention ports 15 N withdrawal, -40..80 C, metal IP30. "
        "Datasheet weight line reads 0.64 kg but is shared with the 7-port "
        "model -> mass is EST-high (the 2010 B&B sheet says 380 g — weigh it). "
        "Ports + host B on one 138 x 35 long face, DC on an end; end-face hole "
        "pattern and port positions: see UHR204 below and hub_mount/."),
    "flycatcher": (64.93, 56.03, 27.0, 48.0, 3.0, "MEAS/PUB",
        "Nooelec FlyCatcher dual 1090/978 tuner, Pi-HAT outline, holes 58 x 49 "
        "MEAS; datasheet 76 x 57 x 19 incl. SMAs, 48 g, 250 + 315 mA at 5 V (PUB). "
        "STILL IN T1: both tuners on UHR204 ports 1-2 (rf-node retired 2026-09-17). "
        "Two micro-USB leads (no latch) -> retention = printed clamp on the tray. "
        "2026-09-30: LEAVES THE CAGE -> stand-alone window unit on a suction cup "
        "(flycatcher_window/); SMA x +/-15.6, uUSB x +/-7.05 from the board centre (EST); "
        "cup screw M6 x 19 (owner), cup thread depth 12.34 MEAS -> 8.0 grip, 11.0 engaged, 1.34 to bottom; "
        "0.9 m bundled micro-USB run to hub "
        "p1/p2 (window-to-cage 2-3 ft); SMA exposed thread with antenna seated 6.16 MEAS 2026-09-30. "
        "MEAS 2026-10-01: SMA jacks 13.25 from each side edge (pitch 29.53), jack body 1.45 above the edge; "
        "uUSB 21.15 from each side edge (pitch 13.73), plug body 9.55 x 7.45 x 18.12, lead 5.61; "
        "LNA caps 16.93 tall, 4.46 down from the top edge; LED cluster 28.10 / 18.61; antennas 184 long; "
        "suction flange screws 39.85 c-c, 62.96 overall, plate 6.12, disc 1.0 high."),
    "co_stick": (20.92, 114.00, 15.12, 30.0, 0.2, "MEAS",
        "Canary Cabin CO: DGS stick + USB-UART, 114 along Y (side-loading "
        "cassette). Mass EST. Mount hole dia 4.216 per the T1 memo."),
    "zed_f9p": (43.5, 43.5, 12.0, 20.0, 0.7, "MEAS",
        "43.5 sq board, 37.6 sq hole pattern. Height EST (SMA + USB-C)."),
    # 2026-09-28 photos 40/41 (the actual board): MTi 1-s DEV Rev 2.6 is a TRIMMED Uno shield ~58.1 x 53.3,
    # not 68.6 long — see MTI_DEV below and canary_t1_cage/mti_mount/.  Tuple updated to the photo outline.
    "mti3_dk": (58.1, 53.3, 14.0, 25.0, 0.1, "EST/photo",
        "Xsens MTi-3 DEV BOARD as owned (photo 32, 2026-09-25): Arduino-Uno shield "
        "form factor 68.6 x 53.3, Uno hole pattern (CONFIRM by caliper), micro-USB "
        "on a short edge (the board's -X end), PSEL DIP, module at a corner with "
        "axes silkscreened: +X along the long axis away from the USB end, +Y across, "
        "+Z out. Mounts board flat, +X (arrow) to the nose. The 43.5 x 34 / M2.5 on "
        "23 x 28 figure from the MT0513P.C manual is the OLDER DK board — not this one. "
        "BNO085 REMOVED 2026-09-22. Height/mass EST."),
    "eg25g_lte": (90.0, 30.0, 14.0, 40.0, 2.0, "MEAS/photo",
        "EG25-G on a mini-PCIe->USB carrier (photo 22): outline ~90 x 30 scaled on "
        "the 30 mm mini-PCIe module width; 2+2 posts = the MEAS 70.80 x 24.21 pattern; "
        "USB receptacle at one short end (A/B CONFIRM), u.FL->SMA pigtail from the "
        "module's far end. Installed on the Orin (memory bank 2026-09-17)."),
    "ina219": (26.0, 21.0, 6.0, 5.0, 0.05, "EST", "STEMMA breakout class."),
}
# MTi 1-s DEV Rev 2.6 (MTi-3 module) — photos 40/41, 2026-09-28.  Used by mti_mount/make_mti_mount.scad.
MTI_DEV = dict(
    outline_uno=((11.2, 69.3), (0.0, 53.3)), outline_tag="EST",        # photo 41 at 14.2 px/mm (board plane)
    # MEAS 2026-09-28 (Javi, caliper): component side up, USB-C bottom-left, origin = upper-right hole:
    # UR (0, 0), LR (0, -47.75), UL (-47.95, -9.03).  Replaces the Uno-derived A/B/C (dx 52.1, dy 5.1).
    holes_j=((0.0, 0.0), (0.0, -47.75), (-47.95, -9.03)), holes_tag="MEAS 2026-09-28",
    hole_d=3.2, hole_d_tag="EST",
    # Uno frame (x_j = -x_uno, y_j = -y_uno): pair anchored where photo 41 put A/B — hole-to-edge offsets EST (CONFIRM)
    holes_uno=((14.65, 2.775), (14.65, 50.525), (62.6, 11.805)),
    hole_D_absent=(66.1, 35.5),                                          # Uno D falls on the MTi socket: not on this board (CONFIRM)
    pin_tail=10.5, pin_tail_tag="EST",                                   # stacking-header tails under the board (end-on in photo 40)
    socket_h=8.5, pcb_t=1.6, usb_c_uno=((69.3, 41.0), (69.3, 49.0)), usb_tag="EST",
    axes="X_s = -x_uno, Y_s = -y_uno, Z_s = +z (component side) — silkscreen, photo 41; = X right / Y up with USB-C bottom-left",
    note="Manual MT0513P fig. 9 (43.5 x 34, M2.5 on 23 x 28) is the OLDER DK board, not this one.")

# Advantech B+B BB-UHR204 (ULI-414I) — 2026-09-29, canary_t1_cage/hub_mount/.  Datasheets: B&B UHRx04_3210ds
# (2010, dimensioned drawing) + Advantech BB-UHRx04 & BB-UHRx07_1819ds (2018 mechanical diagram, scaled for EST).
UHR204 = dict(
    case=(138.24, 86.92, 35.0), case_tag="PUB 2010 (2018: 86.34 +/-0.51, 35 +/-0.51; length scales 138.7)",
    port_face="138 x 35 long face: host USB-B + 4 x USB-A (high retention, 15 N) + LEDs",
    port_x_from_tb_end=dict(host_b=15.6, leds=(44.0, 60.4), p1=71.1, p2=88.5, p3=105.7, p4=122.9), port_tag="EST (2018 drawing scaled)",
    end_holes_from_back=(8.4, 17.5, 68.83, 77.93), end_holes_tag="inner pair 51.33 c-c PUB (2018); outer EST; mid-thickness; "
        "4 per END face (the 'side' holes); thread NOT published (M3 / #4-40, CONFIRM)",
    ear_holes=(153.61, 25.40), ear_tag="PUB 2018: factory panel-bracket ear holes c-c (with brackets 168.19 overall)",
    dc_end="3-pole 5.08 terminal block + locking 5.5 mm barrel jack on the host-B end face", mass_g=640,
    port_map="p1 FlyCatcher ADS-B, p2 FlyCatcher UAT, p3 CO CP2102, p4 XIAO vib (sysfs 2026-09-23)")

# NOT IN THE T1 — a different product, kept only as a named reference solid:
PERCH_STACK = dict(L=122.55, W=92.44, H=60.38, PAT_DX=93.86, PAT_A=50.31,
                   PAT_B=43.56, tag="MEAS",
                   note="CANARY PERCH (ground-side postflight handoff unit). "
                        "Does not fly. Housed by orin_tactical_case/.")

# hole patterns (MEAS) for the envelope solids
PAT_FLYCATCHER = (58.0, 49.0)
PAT_ZED = (37.6, 37.6)
PAT_BNO = (19.95, 17.81)
PAT_EG25 = (70.80, 24.21)

HARNESS_G = 300.0       # EST  wiring, 6 SMA + USB + DC bulkheads, fuses, pigtails
FAN_D = 70.0            # EST  compute top-fan grille keep-out diameter
PLUG_KEEPOUT = 55.0     # EST  USB-A plug + boot + bend radius off the conn face

# ---------------------------------------------------------------------------
# 2. FIXED INTERFACES
# ---------------------------------------------------------------------------
TUBE_D, TUBE_CLR, TUBE_CC = 15.0, 0.4, 60.0       # MEAS print-validated SlimRig
BR = (TUBE_D + TUBE_CLR) / 2                      # 7.7
TUBE_WALL = 2.0                                   # EST  rod is an Al tube, M12 ends
CAP_T, CAP_W, PINCH, BOLT_DY = 11.0, 20.0, 1.0, 12.5   # CANON rev B — do not touch
ST_W, ST_DEP, PL_T = 34.0, 12.0, 7.0                   # CANON
M3B, CB_D, CB_H = 3.4, 6.2, 3.5                        # CANON
INS_D, INS_DEP, INS_CHAM = 4.4, 6.0, 0.6               # CANON
M4B = 4.4                                              # house
BED = (305.0, 305.0, 280.0)                            # PUB QIDI Plus 4
BED_MARGIN = 12.0       # DSN  brim + skirt + arrange margin per side

# ---------------------------------------------------------------------------
# 3. THE THREE MASSING CONCEPTS  (every value DSN — mirrors t1_concepts.scad)
# ---------------------------------------------------------------------------
PDB = (60.0, 40.0, 20.0, 80.0)          # EST fuse/power-distribution block + mass
ROD_L = 400.0           # EST  *** CONFIRM which rod lengths are owned ***
ROD_G = 2 * ROD_L * 3.14159 * ((TUBE_D/2)**2 - (TUBE_D/2 - TUBE_WALL)**2) * 2.70e-3

CONCEPTS = {
  # body envelope (X, Y, Z) excluding rods; overall incl. rods/caps; shell model:
  #   skin = exterior area x t x open-factor ; extras = cartridges/carriers/pods cm3
  "A": dict(name="CARTRIDGE RACK", body=(285, 175, 100), overall=(400, 187, 143),
            skin_t=4.0, open=0.80, extras_cm3=6*38 + 2*45 + 60, rods="top",
            parts=1+1+6+2+4+8, longest=285),
  "B": dict(name="OPEN BOOK", body=(300, 262, 86), overall=(400, 262, 110),
            skin_t=4.0, open=0.85, extras_cm3=8*22 + 300*262*4*0.75/1000 + 2*40,
            rods="bottom", parts=2+2+8+1+4+6, longest=300),
  "C": dict(name="ROD PODS", body=(316, 154, 150), overall=(400, 154, 150),
            skin_t=3.0, open=0.85, extras_cm3=8*30 + 60, rods="middle",
            parts=8+8+16+1+8, longest=148),
  # D: structure is extrusion, so skin_t=0; printed parts = 5 cartridges + battery
  #    carrier + 2 louver inserts + core tray + 2 yoke plates + IMU seat + bezels
  # E: the owner's flat 406 x 279 2020 deck + centre member, two printed full-bay
  #    trays, four 100 mm posts + two yoke bridges (antenna level).  Printed parts =
  #    2 trays + 2 yokes + IMU plate is Al (not printed) + combs/labels/bulkhead plate
  "E": dict(name="FLAT DECK 406x279", body=(406, 279, 24), overall=(406, 279, 190),
            skin_t=0.0, open=0.0, extras_cm3=2*(173*239*4*0.7/1000 + 60) + 2*35 + 40,
            rods="top", parts=2+2+6+4, longest=239),
  "D": dict(name="EXTRUSION FRAME", body=(300, 180, 140), overall=(400, 180, 174),   # 14 members, fixed layout
            skin_t=0.0, open=0.0, extras_cm3=5*34 + 60 + 2*45 + 50 + 2*20 + 12 + 40,
            rods="top", parts=5+1+2+1+2+1+6, longest=134),
}

# ---------------------------------------------------------------------------
# 3b. EXTRUSION for concept D — DECIDED 2026-09-21: 80/20 20-series black.
#     (PUB: FPE/AHP 80/20 spec sheets.  Slot cavity width: verify in the 80/20 CAD.)
#     15-series (Misumi HFS3-1515: 0.34 kg/m, I 2800 mm4, slot 3.4, M3) considered and rejected.
# ---------------------------------------------------------------------------
SERIES = {
  20: dict(part="80/20 20-2020 / 20-2020-Black-FB", alloy="6063-T6 per 8020.net (distributor sheets say 6105-T5)", yield_mpa=172,
           g_per_mm=0.4411, area_mm2=159.1, I_mm4=6826, slot=6.0, slot_depth=6.0,
           cavity=11.0, bolt="M5", usd_per_mm=0.0328,        # 8020.net 2026-09-21; plain 20-2020 $0.0131/mm; $3.00 per cut bracket="20-4119-Black 2-hole inside corner ($7.55, 8020.net)",
           tnut="14122 M5 slide-in economy T-nut block ($0.37, 8020.net)", bracket_g=9.0, tnut_g=4.0),
}
# concept D cut list (mm) — FIXED LAYOUT 2026-09-21 (Core top/end removal path):
#   the two set-back top longs and the IMU cross are DELETED; the top plane is the
#   two full-width end ties only, so the Core lifts straight out between them
#   (200 x 140 opening) or slides out the -X end on the bottom longs' inner slots.
#   IMU datum moved onto the rear Al yoke plate (bolted to the rear top tie).
def e_cutlist(E):                 # the frame the owner HAS (cut from stock) + the added posts
    DX, DY = 406, 279
    return [("E01-E02 long (belt/strap members)", 2, DX), ("E03-E04 end", 2, DY - 2*E),
            ("E05 centre member", 1, DY - 2*E), ("E06-E09 antenna posts (ADD)", 4, 100)]
def e_cutlist_C(E, post_h):       # concept E rev C (full-height cage): longer posts + a top rectangle
    DX, DY = 406, 279
    return [("E01-E02 long (belt/strap members)", 2, DX), ("E03-E04 end", 2, DY - 2*E),
            ("E05 centre member", 1, DY - 2*E), ("E06-E09 cage posts (ADD, rev C)", 4, post_h),
            ("E10-E11 top long rail (ADD, rev C)", 2, DX), ("E12-E13 top end rail (ADD, rev C)", 2, DY - 2*E)]

# ---------------------------------------------------------------------------
# 3c. ROD LEVEL (antenna level) — concept E.  Mirrored in t1_concept_E.scad.
#     z = 0 deck underside; x along the 406 deck, y across (279), deck coords.
# ---------------------------------------------------------------------------
DOME = dict(D=150.0, H=60.0, PC=35.0, mass_g=400.0, puck_h=30.0, puck_g=40.0, tag="EST",
            note="white L1/L2 GNSS survey dome on the rod level (photos 27/30): O150 x 60 read "
                 "from photos, L1 phase centre 35 above its base, mass 400 g — ALL EST, no "
                 "datasheet in hand.  5/8-11 puck rod-mount is to design (30 tall DSN).")
MA963 = dict(L=146.37, W=133.95, H=20.04, mass_g=730.0, tag="MEAS/DS",
             plate=(173.0, 180.0, 7.0), clamp_top=23.24, st_dep=12.0, st_cx=52.0, st_l=46.0,
             hw_g=250.0,
             note="Taoglas MA963 Guardian: 146.37 (ALONG the rods) x 133.95 x 20.04 MEAS, 730 g DS, "
                  "4 x 5G/4G MIMO 600 MHz-6 GHz, NO GNSS element. On the CW-ANT-005 rev C canon "
                  "plate (taoglas_ma963/): plate 173 along x 180 across x 7, underside 12 above the "
                  "rod axis, corner clamps 23.24 above the plate top. Plate + clamps + caps ~250 g EST.")
ROD_Z = 151.7            # DSN rod axis, concept E (E + 3 + 100 + 10 + 11 + 7.7) — same in rev B and C
ROD_LEVEL_C = dict(      # rev C x positions (DSN) — see LAYOUT_E.md rev C
    ma963_cx=107.0, dome_cx=277.0, co_cap_x=225.0, whips=((374.0, 50.0), (374.0, 229.0)),
    whip_h=40.0, whip_base=141.0, top_clr=15.0,
    co_g=120.0, whips_g=60.0, yokes_g=55.0)

def d_cutlist(E):
    DX, DY, DZ = 300, 180, 140
    return [
        ("M01-M02 bottom long", 2, DX), ("M03-M04 bottom end (5 mm gaps)", 2, DY - 2*E - 10),
        ("M05-M08 corner post", 4, DZ - 2*E), ("M09-M10 top end tie", 2, DY - 2*E),
        ("M11-M12 front mullion", 2, DZ - 2*E), ("M13-M14 rear mullion", 2, DZ - 2*E)]
# ---------------------------------------------------------------------------
# 4. MATERIAL / PRINT RATIOS  (from this repo's own sliced evidence)
# ---------------------------------------------------------------------------
RHO = {"ASA": 1.07, "PA12-CF": 1.06, "PLA": 1.24}
FILL = 0.85             # sliced volume / CAD volume at 4 walls, 30 % gyroid, 4-5 mm skins
H_PER_CM3 = 37.85 / 359.39   # orin_tactical_case ASA: 0.105 h per sliced cm3
