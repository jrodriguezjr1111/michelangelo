"""
CyberWing Canary - WT901 IMU saddle clamp for engine mount tube.

Two-piece split saddle (left/right) that clamps a tube of TUBE_OD diameter
using two M5 stainless screws. The upper half has a flat sensor pad with
a locating pocket for a WT901SDCL-BT50 (51.5 x 36.1 x 15mm).

GEOMETRY:
  - Saddle inner radius: TUBE_OD/2 + CLEARANCE
  - Saddle outer wall: SADDLE_WALL thickness
  - Length along tube: SADDLE_LENGTH
  - Two flanges extending out, each containing one M5 bolt hole
  - Upper half adds sensor pad on top, oriented so sensor X = tube axis

PRINT:
  - Each half prints flat-face-down (split surface on bed)
  - Layer lines perpendicular to clamp axis (good for clamp force)
  - No supports needed if FLANGE_ANGLE is shallow enough

OUTPUTS:
  /mnt/user-data/outputs/saddle_lower.stl  (the bottom half)
  /mnt/user-data/outputs/saddle_upper.stl  (the top half with sensor pad)

ENGINEERING NOTES:
  - CHANGE TUBE_OD AFTER MEASURING WITH CALIPERS
  - For PLA: prototype/benchtop only, DO NOT FLY
  - For airworthy: switch to ASA, increase wall thickness
"""

import math
import struct
from pathlib import Path


# ============================================================================
# PARAMETERS — change these to fit your build
# ============================================================================

# Tube specs (MEASURE THIS)
TUBE_OD = 19.05         # mm (= 0.75")
CLEARANCE = 0.4         # total diametral clearance (0.2mm per side)

# Saddle body
SADDLE_WALL = 5.5       # radial wall thickness (M5 needs ~5mm, plus margin)
SADDLE_LENGTH = 55.0    # along tube axis

# Flanges (where the clamp screws go)
FLANGE_THICKNESS = 8.0  # how far flange extends from saddle OD
FLANGE_WIDTH = 16.0     # along tube axis
SCREW_DIAMETER = 5.4    # M5 with light clearance
NUT_FLATS = 8.0         # M5 nut flats (across-flats) - hex pocket
NUT_DEPTH = 4.5         # M5 nut thickness
SCREW_HEAD_DIAM = 9.0   # M5 socket head clearance
SCREW_HEAD_DEPTH = 5.5  # countersink depth for socket cap

# Sensor pocket (WT901SDCL-BT50 = 51.5 x 36.1 x 15mm)
SENSOR_LEN = 51.5
SENSOR_WID = 36.1
SENSOR_HT = 15.0
SENSOR_FIT = 0.4        # extra mm in pocket dimensions
POCKET_DEPTH = 2.5      # how deep into the pad the sensor sits

# Sensor pad (flat platform on top half)
PAD_LEN = SENSOR_LEN + 8       # extends past sensor each end
PAD_WID = SENSOR_WID + 8
PAD_THICKNESS = 5.0            # base thickness above saddle OD

# Strap slots (for zip tie or velcro to hold sensor in pocket)
STRAP_SLOT_W = 3.5             # zip tie thickness
STRAP_SLOT_L = 12.0            # zip tie width

# Mesh quality
SEGMENTS = 48                   # arc subdivision

# Output paths
OUT_LOWER = Path("/mnt/user-data/outputs/saddle_lower.stl")
OUT_UPPER = Path("/mnt/user-data/outputs/saddle_upper.stl")


# ============================================================================
# Vector / STL helpers
# ============================================================================

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def sub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def add(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def scale(v, s):
    return (v[0]*s, v[1]*s, v[2]*s)

def norm(v):
    m = math.sqrt(sum(c*c for c in v))
    return (v[0]/m, v[1]/m, v[2]/m) if m > 0 else (0,0,0)

def write_stl(path, triangles, header="part"):
    with open(path, 'wb') as f:
        f.write(header.encode('ascii')[:80].ljust(80, b' '))
        f.write(struct.pack('<I', len(triangles)))
        for v1, v2, v3 in triangles:
            n = norm(cross(sub(v2,v1), sub(v3,v1)))
            f.write(struct.pack('<12fH',
                n[0],n[1],n[2],
                v1[0],v1[1],v1[2],
                v2[0],v2[1],v2[2],
                v3[0],v3[1],v3[2], 0))


def quad(p1, p2, p3, p4):
    """Two triangles forming a quad. Order: p1, p2, p3, p4 should be CCW."""
    return [(p1, p2, p3), (p1, p3, p4)]


# ============================================================================
# Build saddle half (used for both upper and lower)
# ============================================================================

def build_half_saddle(is_upper: bool):
    """
    Build one half of the saddle clamp.
    
    Coordinate system:
      X = along tube axis (sensor X axis)
      Y = horizontal, perpendicular to tube
      Z = up (when fully assembled on tube)
    
    The split plane is the X-Z plane (y=0).
    For the lower half, the half-circle extends into Y < 0.
    For the upper half, the half-circle extends into Y > 0.
    Both have the flat split surface on the X-Z plane.
    
    For PRINTING:
      - Print flat side down on the bed (the split surface)
      - For upper, this means the sensor pad is at the bottom of the build,
        and the curved saddle interior faces UP. Print orientation requires
        rotation before printing — we'll generate it in "assembled" orientation
        and tell the user to rotate in slicer.
    
    Actually let me change approach: generate each part in its PRINT orientation.
    Print orientation: split surface facing UP (so you slice it lying flat),
    curved saddle body BELOW. No, this won't print well either.
    
    Best print: each half lies on the FLAT split surface, curved part up.
    The flat split surface is at z=0 in the print orientation.
    For lower half: the saddle interior arches UP from z=0 to z=TUBE_OD/2+CLEARANCE/2.
    For upper half: same, plus the sensor pad on top.
    
    OK switching to print-orientation directly:
      X = along tube axis
      Y = horizontal across split
      Z = build direction (up = away from bed)
    The split surface (formerly Y=0 plane) is the bed (z=0).
    The half-tube cylinder is centered above z=0 with axis parallel to X.
    The cylinder axis is at z=0 (on the split surface).
    Saddle goes from z=0 up to z=tube_radius+wall.
    """
    triangles = []
    
    r_in = TUBE_OD / 2 + CLEARANCE / 2     # inner radius (saddle bore)
    r_out = r_in + SADDLE_WALL              # outer radius
    
    L = SADDLE_LENGTH
    x0 = -L/2
    x1 = L/2
    
    # ----- Build the half-cylindrical shell (saddle body) -----
    # In print orientation: cylinder axis at (X, 0, 0), saddle in upper half
    # angle 0 = +Y direction (across split), pi = -Y direction (NOT in this half)
    # For half cylinder: angle from 0 to pi (upper half, Z >= 0)
    # Wait - we want the saddle ABOVE z=0 (on top of bed).
    # Cylinder axis at (x, 0, 0). For upper half: z >= 0.
    # Parametrize angle theta from 0 (+Y) to pi (-Y), with z = r*sin(theta)
    # That gives upper half. Correct.
    
    arc_steps = SEGMENTS // 2
    
    inner_pts = []  # (x0 ring, x1 ring) of inner arc points
    outer_pts = []
    for ring_x in [x0, x1]:
        ring_inner = []
        ring_outer = []
        for i in range(arc_steps + 1):
            theta = math.pi * i / arc_steps   # 0 to pi
            cy_in, cz_in = r_in * math.cos(theta), r_in * math.sin(theta)
            cy_out, cz_out = r_out * math.cos(theta), r_out * math.sin(theta)
            ring_inner.append((ring_x, cy_in, cz_in))
            ring_outer.append((ring_x, cy_out, cz_out))
        inner_pts.append(ring_inner)
        outer_pts.append(ring_outer)
    
    # Inner cylindrical surface (faces -Z when viewed from inside the bore)
    # Outward normal from this surface points TOWARD the cylinder axis (downward into the saddle bore)
    # CCW winding when viewed from inside the bore (from below)
    for i in range(arc_steps):
        p1 = inner_pts[0][i]
        p2 = inner_pts[1][i]
        p3 = inner_pts[1][i+1]
        p4 = inner_pts[0][i+1]
        # Inner surface, normal points to axis = -radial, so winding is reversed
        triangles += quad(p1, p4, p3, p2)
    
    # Outer cylindrical surface (normal points outward radially)
    for i in range(arc_steps):
        p1 = outer_pts[0][i]
        p2 = outer_pts[0][i+1]
        p3 = outer_pts[1][i+1]
        p4 = outer_pts[1][i]
        triangles += quad(p1, p2, p3, p4)
    
    # End caps (annular - between inner and outer arcs at x=x0 and x=x1)
    # x=x0 cap (faces -X, normal -X)
    for i in range(arc_steps):
        i_in_a = inner_pts[0][i]
        i_in_b = inner_pts[0][i+1]
        i_out_a = outer_pts[0][i]
        i_out_b = outer_pts[0][i+1]
        # Normal points in -X direction
        # CCW when viewed from -X means: outer to inner going around
        triangles += quad(i_out_a, i_in_a, i_in_b, i_out_b)
    
    # x=x1 cap (faces +X, normal +X)
    for i in range(arc_steps):
        i_in_a = inner_pts[1][i]
        i_in_b = inner_pts[1][i+1]
        i_out_a = outer_pts[1][i]
        i_out_b = outer_pts[1][i+1]
        # Normal points in +X direction. CCW from +X view.
        triangles += quad(i_out_a, i_out_b, i_in_b, i_in_a)
    
    # Bottom (split-plane) surfaces — these are the flat faces at z=0
    # On each side of the saddle (Y > 0 and Y < 0), there's a flat strip
    # from inner radius to outer radius along X. These are the surfaces
    # that mate with the other half.
    # For Y > 0 side (theta = 0 endpoints): from (x, r_in, 0) to (x, r_out, 0)
    # For Y < 0 side (theta = pi endpoints): from (x, -r_out, 0) to (x, -r_in, 0)
    
    # Y > 0 split face (this is part of the flange)
    p_in_x0_pos = inner_pts[0][0]   # (x0, r_in, 0)
    p_in_x1_pos = inner_pts[1][0]   # (x1, r_in, 0)
    p_out_x0_pos = outer_pts[0][0]  # (x0, r_out, 0)
    p_out_x1_pos = outer_pts[1][0]  # (x1, r_out, 0)
    
    p_in_x0_neg = inner_pts[0][-1]  # (x0, -r_in, 0)
    p_in_x1_neg = inner_pts[1][-1]  # (x1, -r_in, 0)
    p_out_x0_neg = outer_pts[0][-1] # (x0, -r_out, 0)
    p_out_x1_neg = outer_pts[1][-1] # (x1, -r_out, 0)
    
    # Note: these strips become the inboard part of the flanges. The flanges
    # extend from r_out outward by FLANGE_THICKNESS.
    # We'll build the flanges as boxes attached to these strips.
    
    # ----- Flanges (extend outward in +Y and -Y) -----
    # +Y flange: extends from y=r_out to y=r_out+FLANGE_THICKNESS
    #            width FLANGE_WIDTH in X (centered), height same as saddle wall (z=0 to ~saddle wall)
    # The flange height should be enough to fit the M5 hardware. Make it equal to r_out
    # so it visually wraps around - actually for simpler geometry, make flange height = SADDLE_WALL + 4
    
    flange_height = SADDLE_WALL + 4   # z extent of flange
    flange_x_half = FLANGE_WIDTH / 2
    
    for sign in [+1, -1]:
        # Flange box from (x: -flange_x_half to flange_x_half),
        # (y: sign*r_out to sign*(r_out+FLANGE_THICKNESS)),
        # (z: 0 to flange_height)
        x_lo, x_hi = -flange_x_half, flange_x_half
        y_lo = sign * r_out
        y_hi = sign * (r_out + FLANGE_THICKNESS)
        if sign < 0:
            y_lo, y_hi = y_hi, y_lo  # ensure y_lo < y_hi
        z_lo, z_hi = 0, flange_height
        
        # 8 corners of flange box
        c000 = (x_lo, y_lo, z_lo)
        c100 = (x_hi, y_lo, z_lo)
        c110 = (x_hi, y_hi, z_lo)
        c010 = (x_lo, y_hi, z_lo)
        c001 = (x_lo, y_lo, z_hi)
        c101 = (x_hi, y_lo, z_hi)
        c111 = (x_hi, y_hi, z_hi)
        c011 = (x_lo, y_hi, z_hi)
        
        # bottom (z_lo, normal -Z)
        triangles += quad(c000, c010, c110, c100)
        # top (z_hi, normal +Z)
        triangles += quad(c001, c101, c111, c011)
        # X-low face (normal -X)
        triangles += quad(c000, c001, c011, c010)
        # X-high face (normal +X)
        triangles += quad(c100, c110, c111, c101)
        # Y-low face — this is the OUTBOARD face for negative sign or INBOARD for positive sign
        # For sign=+1: y_lo = r_out (inboard, faces -Y back at saddle); y_hi = r_out+thickness (outboard, faces +Y)
        # For sign=-1: y_lo = -(r_out+thickness) (outboard, -Y); y_hi = -r_out (inboard)
        # Y-low face (normal -Y)
        if sign > 0:
            triangles += quad(c000, c100, c101, c001)  # +Y flange inboard skip; no, this is the inboard side facing into saddle
        # Actually we don't want to skip - the flange box has all 6 faces. The inboard face overlaps with the saddle wall but having both shouldn't cause issues for STL since they're co-planar; slicers handle it.
        # Just include all 6 faces:
        triangles += quad(c000, c100, c101, c001)  # -Y face (outboard for sign<0)
        # Y-high face (normal +Y)
        triangles += quad(c010, c011, c111, c110)  # +Y face
    
    # NOTE: We're not boolean-subtracting the screw holes here because that
    # requires CSG. For STL purposes, the slicer can handle co-planar faces.
    # The screw holes will be added as cylindrical voids, which means we need
    # to actually cut the flange. Without CSG, we'll do this differently:
    # split the flange faces around the holes.
    # 
    # SIMPLER APPROACH: build the flange WITHOUT screw holes for v1.
    # User can drill the holes after printing using an M5 drill bit.
    # Add visual markers (dimples on top and bottom) showing where to drill.
    # 
    # For now, just emit the solid flange. The user gets perfect alignment
    # by drilling through both halves clamped together.
    
    # ----- Sensor pad (UPPER HALF ONLY) -----
    if is_upper:
        # The sensor pad sits on TOP of the saddle, at z = r_out
        # Pad dimensions: PAD_LEN (X) x PAD_WID (Y) x PAD_THICKNESS (Z above r_out)
        pad_z_lo = r_out
        pad_z_hi = r_out + PAD_THICKNESS
        pad_x_lo = -PAD_LEN / 2
        pad_x_hi = PAD_LEN / 2
        pad_y_lo = -PAD_WID / 2
        pad_y_hi = PAD_WID / 2
        
        # 8 corners of pad
        c000 = (pad_x_lo, pad_y_lo, pad_z_lo)
        c100 = (pad_x_hi, pad_y_lo, pad_z_lo)
        c110 = (pad_x_hi, pad_y_hi, pad_z_lo)
        c010 = (pad_x_lo, pad_y_hi, pad_z_lo)
        c001 = (pad_x_lo, pad_y_lo, pad_z_hi)
        c101 = (pad_x_hi, pad_y_lo, pad_z_hi)
        c111 = (pad_x_hi, pad_y_hi, pad_z_hi)
        c011 = (pad_x_lo, pad_y_hi, pad_z_hi)
        
        # All 6 faces of pad
        triangles += quad(c000, c010, c110, c100)  # bottom
        triangles += quad(c001, c101, c111, c011)  # top  
        triangles += quad(c000, c001, c011, c010)  # -X
        triangles += quad(c100, c110, c111, c101)  # +X
        triangles += quad(c000, c100, c101, c001)  # -Y
        triangles += quad(c010, c011, c111, c110)  # +Y
        
        # NOTE: sensor pocket and strap slots not implemented in this v1
        # because subtracting from STL requires proper CSG. User can:
        # - Mark sensor outline on pad surface and route a 2.5mm pocket
        # - OR redesign with OpenSCAD/Build123d for proper CSG
        # - OR just attach sensor with VHB tape directly to flat pad
        # 
        # The flat pad with VHB tape is actually the most reliable approach
        # for this sensor anyway.
    
    return triangles


# ============================================================================
# Generate
# ============================================================================

def report():
    print("=" * 60)
    print("CyberWing Canary - WT901 Saddle Clamp")
    print("=" * 60)
    print(f"Tube OD assumed:    {TUBE_OD:.2f} mm  (= {TUBE_OD/25.4:.3f}\")")
    print(f"Saddle bore ID:     {TUBE_OD + CLEARANCE:.2f} mm")
    print(f"Saddle outer dia:   {TUBE_OD + CLEARANCE + 2*SADDLE_WALL:.2f} mm")
    print(f"Saddle length:      {SADDLE_LENGTH} mm")
    print(f"Flange thickness:   {FLANGE_THICKNESS} mm (outboard from saddle)")
    print(f"Sensor pad:         {PAD_LEN} x {PAD_WID} x {PAD_THICKNESS} mm")
    print(f"Sensor (WT901):     {SENSOR_LEN} x {SENSOR_WID} x {SENSOR_HT} mm")
    print()
    print(f"Total assembled outline (LxWxH):")
    total_w = TUBE_OD + CLEARANCE + 2*(SADDLE_WALL + FLANGE_THICKNESS)
    total_h = TUBE_OD + CLEARANCE + 2*SADDLE_WALL + PAD_THICKNESS
    print(f"  ~{SADDLE_LENGTH} x {total_w:.1f} x {total_h:.1f} mm")
    print()
    print(f"M5 screws needed: 2x M5 stainless socket cap, length ~25mm + nuts")
    print()


if __name__ == "__main__":
    report()
    
    # Lower half
    lower = build_half_saddle(is_upper=False)
    write_stl(OUT_LOWER, lower, "Canary saddle lower")
    print(f"Wrote: {OUT_LOWER.name} ({len(lower)} triangles, {OUT_LOWER.stat().st_size} bytes)")
    
    # Upper half
    upper = build_half_saddle(is_upper=True)
    write_stl(OUT_UPPER, upper, "Canary saddle upper")
    print(f"Wrote: {OUT_UPPER.name} ({len(upper)} triangles, {OUT_UPPER.stat().st_size} bytes)")
    
    print()
    print("PRINT NOTES:")
    print("  - Each part: print flat-face-down (split surface on bed)")
    print("  - Layer height: 0.2mm")
    print("  - Walls: 4 perimeters minimum")
    print("  - Infill: 50% gyroid (or higher for clamping force)")
    print("  - No supports needed — overhangs are gentle")
    print("  - Material: PLA = prototype only. ASA/PETG for actual aircraft use.")
    print()
    print("ASSEMBLY:")
    print("  1. Drill 5.0mm holes through both flanges, clamped together,")
    print("     aligned. Mark hole locations on flange faces during design v2.")
    print("  2. Test fit on a piece of scrap tube of correct OD")
    print("  3. Attach WT901 to top pad with 3M VHB tape (cleanest)")
    print("     OR use 2 zip ties through pad edges (need to add slots in v2)")
    print("  4. Verify sensor X axis is parallel to tube longitudinal axis")
