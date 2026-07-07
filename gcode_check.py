#!/usr/bin/env python3
"""
gcode_check.py — Inspect a sliced gcode file for sanity before printing.

Usage:
    python gcode_check.py path/to/file.gcode
    python gcode_check.py path/to/file.gcode --verbose
"""

import argparse
import re
import sys
from pathlib import Path


def parse_header(lines: list[str]) -> dict:
    """Extract slicer metadata from gcode comments at the top of the file."""
    meta = {}
    patterns = {
        "object_height": r";\s*object_height[:\s=]+([\d.]+)",
        "layer_height": r";\s*layer_height[:\s=]+([\d.]+)",
        "first_layer_height": r";\s*(?:first_layer_height|initial_layer_print_height)[:\s=]+([\d.]+)",
        "filament_used_mm": r";\s*filament\s*used\s*\[mm\][:\s=]+([\d.]+)",
        "filament_used_g": r";\s*(?:total\s*)?filament\s*used\s*\[g\][:\s=]+([\d.]+)",
        "estimated_time": r";\s*(?:estimated\s*printing\s*time|total\s*estimated\s*time)\b.*?([\d]+h?\s*[\d]+m?\s*[\d]+s|\d+)",
        "nozzle_temp": r";\s*(?:nozzle_temperature|first_layer_temperature)[:\s=]+(\d+)",
        "bed_temp": r";\s*(?:bed_temperature|first_layer_bed_temperature)[:\s=]+(\d+)",
        "filament_type": r";\s*filament_type[:\s=]+(\w+)",
        "slicer": r";\s*generated\s*by\s*([^\n]+)",
        "total_layer_number": r";\s*total\s*layer\s*number[:\s=]+(\d+)",
        "max_z_height": r";\s*max_z_height[:\s=]+([\d.]+)",
    }
    
    header_text = "\n".join(lines[:200])
    for key, pat in patterns.items():
        m = re.search(pat, header_text, re.IGNORECASE)
        if m:
            meta[key] = m.group(1).strip()
    return meta


def scan_gcode(lines: list[str]) -> dict:
    """Walk the actual gcode to find max Z height, layer count, extrusion total."""
    max_z = 0.0
    layer_count = 0
    total_e = 0.0
    last_e = 0.0
    abs_e_mode = True
    moves_with_extrusion = 0
    moves_no_extrusion = 0
    first_print_z = None
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith(";"):
            # Count layer markers from slicer comments
            if re.match(r";\s*LAYER[:\s]", line, re.I):
                layer_count += 1
            elif re.match(r";\s*layer_num\b", line, re.I):
                layer_count += 1
            continue
        
        # Track E mode
        if line.startswith("M82"):
            abs_e_mode = True
        elif line.startswith("M83"):
            abs_e_mode = False
        
        # Parse G0/G1 moves
        if line.startswith(("G0 ", "G1 ", "G0\t", "G1\t")):
            z_match = re.search(r"Z([-\d.]+)", line)
            e_match = re.search(r"E([-\d.]+)", line)
            
            if z_match:
                z = float(z_match.group(1))
                if z > max_z:
                    max_z = z
            
            if e_match:
                e = float(e_match.group(1))
                if abs_e_mode:
                    delta = e - last_e
                    last_e = e
                else:
                    delta = e
                if delta > 0:
                    total_e += delta
                    moves_with_extrusion += 1
                    if z_match and first_print_z is None:
                        first_print_z = float(z_match.group(1))
            else:
                if z_match or re.search(r"[XY]", line):
                    moves_no_extrusion += 1
    
    return {
        "max_z_observed": max_z,
        "layer_count_observed": layer_count,
        "total_extrusion_mm": round(total_e, 2),
        "moves_with_extrusion": moves_with_extrusion,
        "moves_no_extrusion": moves_no_extrusion,
        "first_extrusion_z": first_print_z,
    }


def check_sanity(meta: dict, scan: dict, expected_max_z: float = None) -> list[tuple[str, bool, str]]:
    """Run sanity checks and return (check_name, pass/fail, detail)."""
    checks = []
    
    # Meta vs scanned max Z should match
    meta_height = float(meta.get("object_height", 0)) if meta.get("object_height") else None
    scanned_max_z = scan["max_z_observed"]
    
    if meta_height:
        checks.append((
            "Metadata height matches scan",
            abs(meta_height - scanned_max_z) < 1.0,
            f"metadata object_height={meta_height}, scanned max Z={scanned_max_z}"
        ))
    
    # Expected height check
    if expected_max_z:
        checks.append((
            f"Max Z matches expected ({expected_max_z}mm)",
            abs(scanned_max_z - expected_max_z) < 0.5,
            f"Scanned max Z={scanned_max_z}mm (expected {expected_max_z}mm)"
        ))
    
    # First extrusion Z should be close to first layer height
    fl = float(meta.get("first_layer_height", 0.24)) if meta.get("first_layer_height") else 0.24
    fz = scan["first_extrusion_z"]
    if fz is not None:
        checks.append((
            "First extrusion at reasonable Z",
            0.1 <= fz <= 0.5,
            f"First extrusion Z={fz}mm (expected ~{fl}mm)"
        ))
    
    # Total extrusion sanity
    te = scan["total_extrusion_mm"]
    checks.append((
        "Total extrusion sensible",
        50 <= te <= 50000,
        f"Total E = {te}mm"
    ))
    
    # Layer count
    checks.append((
        "Layer count reasonable",
        scan["layer_count_observed"] > 0,
        f"Layers detected: {scan['layer_count_observed']}"
    ))
    
    return checks


def main():
    p = argparse.ArgumentParser()
    p.add_argument("gcode_file", type=Path)
    p.add_argument("--expected-z", type=float, default=None,
                   help="Expected max Z height in mm (e.g., 0.4 for a 0.4mm patch)")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()
    
    if not args.gcode_file.exists():
        print(f"File not found: {args.gcode_file}")
        sys.exit(1)
    
    print(f"Analyzing: {args.gcode_file}")
    print(f"Size: {args.gcode_file.stat().st_size:,} bytes\n")
    
    lines = args.gcode_file.read_text(errors="replace").splitlines()
    print(f"Total lines: {len(lines):,}\n")
    
    meta = parse_header(lines)
    scan = scan_gcode(lines)
    
    print("=" * 60)
    print("METADATA (from gcode header comments)")
    print("=" * 60)
    for k, v in meta.items():
        print(f"  {k:.<40} {v}")
    
    print()
    print("=" * 60)
    print("SCAN (from actual gcode moves)")
    print("=" * 60)
    for k, v in scan.items():
        print(f"  {k:.<40} {v}")
    
    print()
    print("=" * 60)
    print("SANITY CHECKS")
    print("=" * 60)
    checks = check_sanity(meta, scan, args.expected_z)
    all_passed = True
    for name, ok, detail in checks:
        status = "✓ PASS" if ok else "✗ FAIL"
        print(f"  [{status}] {name}")
        print(f"          {detail}")
        if not ok:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All checks passed. Safe to print.")
    else:
        print("⚠️  FAIL: Do NOT print this gcode. The scale or geometry is wrong.")
        sys.exit(2)


if __name__ == "__main__":
    main()
