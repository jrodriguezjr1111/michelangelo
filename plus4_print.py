#!/usr/bin/env python3
"""
plus4_print.py — Headless STL → gcode → print pipeline for QIDI Plus4.

Subcommands:
    slice <stl> --material pla     Slice an STL using OrcaSlicer
    check <gcode>                  Inspect a gcode file for sanity
    send <gcode>                   Upload and print an existing gcode
    status                          Show printer status
    stop                            Cancel current print
    estop                           Emergency stop

Examples:
    python3 plus4_print.py slice saddle_lower_v2.stl --material pla --check
    python3 plus4_print.py send saddle_lower_v2.gcode

Requires: pip install requests rich

NOTES:
- The QIDI Plus4 OrcaSlicer machine profile has a bug where the PRINT_START
  macro receives wrong temperature values due to template variable name
  mismatch. We post-process the gcode to rewrite the PRINT_START line.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import requests
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
except ImportError:
    print("Missing deps. Run: pip install requests rich")
    sys.exit(1)

console = Console()

# =============================================================================
# Configuration
# =============================================================================

DEFAULT_HOST = os.environ.get("PLUS4_HOST", "192.168.86.232")
ORCA_PATH_DEFAULT = "/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer"
ORCA_CONFIG_DIR = Path.home() / "Library/Application Support/OrcaSlicer/system/QIDI"

PROFILES = {
    "machine": "Qidi X-Plus 4 0.4 nozzle.json",
    "filaments": {
        "pla": "Bambu PLA @Qidi X-Plus 4 0.4 nozzle.json",
        "pla_hatchbox": "HATCHBOX PLA @Qidi X-Plus 4 0.4 nozzle.json",
    },
    "processes": {
        "standard": "0.20mm Standard @Qidi XPlus4.json",
    },
}

# Correct temperatures per material — these override the broken PRINT_START
# values that come out of the slicer due to a profile variable mismatch.
# Tuple: (bed_temp_first_layer_C, hotend_temp_first_layer_C, chamber_temp_C)
MATERIAL_TEMPS = {
    "pla":          (70, 215, 0),
    "pla_hatchbox": (70, 215, 0),
    "petg":         (75, 240, 0),
    "abs":          (95, 250, 50),
    "asa":          (95, 255, 50),
    "tpu":          (60, 220, 0),
}


def find_orca() -> Path:
    env = os.environ.get("ORCA_PATH")
    if env and Path(env).exists():
        return Path(env)
    if Path(ORCA_PATH_DEFAULT).exists():
        return Path(ORCA_PATH_DEFAULT)
    raise FileNotFoundError(
        "OrcaSlicer not found. Install with: brew install --cask orcaslicer"
    )


def resolve_profile(category: str, name: str) -> Path:
    p = ORCA_CONFIG_DIR / category / name
    if not p.exists():
        cat_dir = ORCA_CONFIG_DIR / category
        available = sorted(
            f.name for f in cat_dir.iterdir() if f.suffix == ".json"
        ) if cat_dir.exists() else []
        match_terms = name.lower().split()
        relevant = [a for a in available if all(t in a.lower() for t in match_terms[:2])][:10]
        raise FileNotFoundError(
            f"Profile not found: {p}\n\nClosest matches in {category}:\n"
            + "\n".join(f"  {a}" for a in relevant)
        )
    return p


# =============================================================================
# Gcode post-processor — fix bad temperatures in PRINT_START line
# =============================================================================

def postprocess_gcode(gcode_path: Path, material: str,
                     z_offset: float = 0.0) -> dict:
    """Replace the broken PRINT_START macro call with an explicit, known-good
    preamble (homing + heat + wait), matching the hand-rolled bezel gcode.

    The QIDI Plus4's PRINT_START macro on this machine fails to home the
    axes reliably (and also has a temperature template-variable mismatch).
    Symptom: nozzle prints in midair / no first-layer adhesion. The fix is
    to bypass the macro entirely and emit explicit gcode.

    Also rewrites the M140/M104/M141 lines that follow.
    """
    if material not in MATERIAL_TEMPS:
        console.print(f"[yellow]No temperature override defined for material '{material}'")
        return {"changed": False}

    bed_t, hotend_t, chamber_t = MATERIAL_TEMPS[material]

    text = gcode_path.read_text()
    original_print_start = None
    new_print_start = None
    changes = []

    # Replace PRINT_START call with explicit preamble (bezel-style).
    # Order matters: heat both → home → wait both → small lift before purge.
    # Preamble order:
    #   bed heat -> home -> wait bed -> mesh (cold nozzle, no ooze)
    #   -> hotend heat -> wait hotend -> lift.
    # NOTE: avoid M140/M104 lines here that the regex below would clobber;
    # use M190/M109 (wait variants) which the regex doesn't touch, so the
    # bed/hotend targets we set survive post-processing intact.
    replacement_preamble = (
        "; --- explicit preamble (mirrors QIDI PRINT_START) ---\n"
        "G90                      ; absolute XYZ\n"
        "M83                      ; relative E\n"
        "SET_ZOFFSET              ; apply saved z_offset\n"
        "SET_HEATER_TEMPERATURE HEATER=extruder TARGET=0  ; hotend off during leveling\n"
        f"SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET={bed_t} ; start bed heating\n"
        "G28                      ; home all\n"
        f"M190 S{bed_t}                ; wait for bed temp\n"
        "SET_HEATER_TEMPERATURE HEATER=extruder TARGET=140 ; preheat (no ooze)\n"
        "Z_TILT_ADJUST            ; level gantry (dual Z)\n"
        "BED_MESH_CLEAR           ; drop stale mesh\n"
        "BED_MESH_CALIBRATE       ; fresh mesh on hot+level bed\n"
        "G0 Z50 F600              ; lift\n"
        f"M109 S{hotend_t}              ; heat & wait for hotend\n"
        f"M141 S{chamber_t}                ; chamber temp\n"
        "ENABLE_ALL_SENSOR        ; filament sensors on\n"
        "; --- end explicit preamble ---"
    )

    print_start_pattern = re.compile(
        r'^PRINT_START\s+BED=(\S+)\s+HOTEND=(\S+)\s+CHAMBER=(\S+)\s+EXTRUDER=(\S+)',
        re.MULTILINE
    )

    def replace_print_start(m: re.Match) -> str:
        nonlocal original_print_start, new_print_start
        original_print_start = m.group(0)
        new_print_start = replacement_preamble
        return replacement_preamble

    new_text, n_print_start = print_start_pattern.subn(replace_print_start, text, count=1)
    if n_print_start:
        changes.append(f"PRINT_START → explicit preamble (G28 + heat + wait, bed={bed_t}, hot={hotend_t})")
    
    start_end = new_text.find("SET_PRINT_STATS_INFO CURRENT_LAYER=1")
    if start_end == -1:
        start_end = new_text.find(";LAYER_CHANGE")
    if start_end == -1:
        start_end = min(len(new_text), 12000)
    startup_text = new_text[:start_end]
    body_text = new_text[start_end:]

    temp_rewrites = (
        (r'^M140\s+S\d+', f"M140 S{bed_t}", "M140 (startup bed)"),
        (r'^M104\s+S\d+', f"M104 S{hotend_t}", "M104 (startup hotend)"),
        (r'^M141\s+S\d+', f"M141 S{chamber_t}", "M141 (startup chamber)"),
    )
    for pattern, replacement, label in temp_rewrites:
        startup_text, count = re.subn(pattern, replacement, startup_text,
                                      flags=re.MULTILINE)
        if count:
            changes.append(f"{label} → {replacement.split()[-1]}")

    # Mid-print temp rewrites: the slicer drops the bed (e.g. "Cool Plate"
    # M140 S35) and tweaks the nozzle after layer 1, which kills adhesion on
    # large/thin parts. Rewrite every NON-ZERO M140/M104/M141 in the body to
    # the material target, while leaving the end-of-print S0 shutdown lines
    # untouched (negative lookahead on S0).
    body_rewrites = (
        (r'^M140\s+S(?!0\b)\d+', f"M140 S{bed_t}", "M140 (mid-print bed)"),
        (r'^M104\s+S(?!0\b)\d+', f"M104 S{hotend_t}", "M104 (mid-print hotend)"),
        (r'^M141\s+S(?!0\b)\d+', f"M141 S{chamber_t}", "M141 (mid-print chamber)"),
    )
    for pattern, replacement, label in body_rewrites:
        body_text, count = re.subn(pattern, replacement, body_text,
                                   flags=re.MULTILINE)
        if count:
            changes.append(f"{label} → {replacement.split()[-1]} ×{count}")
    new_text = startup_text + body_text

    # Inject Z-offset right before first ;LAYER_CHANGE (after all startup,
    # purge, and T0 commands that might reset gcode offsets)
    if z_offset != 0.0:
        anchor = ";LAYER_CHANGE"
        idx = new_text.find(anchor)
        if idx != -1:
            offset_line = f"SET_GCODE_OFFSET Z_ADJUST={z_offset:+.3f} MOVE=1 ; first-layer Z tweak (additive)\n"
            if offset_line.strip() not in new_text:
                new_text = new_text[:idx] + offset_line + new_text[idx:]
            changes.append(f"Z-offset → {z_offset:+.3f} mm (before layer 1)")

    if changes:
        gcode_path.write_text(new_text)
        return {
            "changed": True,
            "changes": changes,
            "original_print_start": original_print_start,
            "new_print_start": new_print_start,
        }
    
    return {"changed": False, "warning": "PRINT_START line not found"}


# =============================================================================
# Moonraker client
# =============================================================================

@dataclass
class Moonraker:
    host: str
    port: int = 7125

    @property
    def base(self) -> str:
        return f"http://{self.host}:{self.port}"

    def get(self, path: str) -> dict:
        r = requests.get(f"{self.base}{path}", timeout=10)
        r.raise_for_status()
        return r.json()

    def post(self, path: str, json_body: dict | None = None) -> dict:
        r = requests.post(f"{self.base}{path}", json=json_body, timeout=30)
        r.raise_for_status()
        return r.json()

    def upload(self, file_path: Path) -> dict:
        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "application/octet-stream")}
            data = {"root": "gcodes"}
            r = requests.post(f"{self.base}/server/files/upload",
                              files=files, data=data, timeout=120)
            r.raise_for_status()
            return r.json()

    def gcode(self, script: str) -> dict:
        return self.post("/printer/gcode/script", {"script": script})

    def start_print(self, filename: str) -> dict:
        return self.post("/printer/print/start", {"filename": filename})

    def cancel_print(self) -> dict:
        return self.post("/printer/print/cancel", {})

    def emergency_stop(self) -> dict:
        return self.post("/printer/emergency_stop", {})

    def query(self, objects: str) -> dict:
        r = requests.get(f"{self.base}/printer/objects/query?{objects}", timeout=10)
        r.raise_for_status()
        return r.json()["result"]["status"]

    def state(self) -> str:
        # Prefer the webhooks object — /printer/info hangs on some Moonraker
        # builds (e.g. v0.8.0-dirty on the Qidi X-Plus 4).
        try:
            wh = self.query("webhooks")["webhooks"]
            return wh.get("state", "unknown")
        except Exception:
            try:
                return self.get("/printer/info")["result"].get("state", "unknown")
            except Exception:
                return "unknown"

    def is_ready(self) -> bool:
        return self.state() == "ready"


# =============================================================================
# Gcode inspection
# =============================================================================

def parse_header(lines: list[str]) -> dict:
    meta = {}
    patterns = {
        "object_height": r";\s*(?:object_height|max_z_height)[:\s=]+([\d.]+)",
        "filament_mm": r";\s*(?:total\s*)?filament\s*(?:used\s*)?(?:length\s*)?\[mm\][:\s=]+([\d.]+)",
        "filament_g": r";\s*(?:total\s*)?filament\s*(?:used\s*)?(?:weight\s*)?\[g\][:\s=]+([\d.]+)",
        "nozzle_temp": r";\s*(?:nozzle_temperature|first_layer_temperature)[:\s=]+(\d+)",
        "bed_temp": r";\s*(?:bed_temperature|first_layer_bed_temperature)[:\s=]+(\d+)",
        "filament_type": r";\s*filament_type[:\s=]+(\w+)",
        "slicer": r";\s*generated\s*by\s*([A-Za-z]+Slicer[^\n;]*)",
        "estimated_time": r";\s*(?:total estimated|estimated printing)\s*time[^:]*:\s*([^\n;]+)",
    }
    header_text = "\n".join(lines[:300])
    for key, pat in patterns.items():
        m = re.search(pat, header_text, re.IGNORECASE)
        if m:
            meta[key] = m.group(1).strip()
    return meta


def scan_gcode_print_only(lines: list[str]) -> dict:
    """Scan only the actual printing portion of the gcode (skip start/end macros)."""
    max_z = 0.0
    min_x = min_y = float("inf")
    max_x = max_y = 0.0
    total_e = 0.0
    last_e = 0.0
    abs_e = True

    in_print_section = False
    layer_count = 0

    for line in lines:
        line = line.strip()
        # Detect when actual printing starts (LAYER_CHANGE comment or first real layer)
        if not in_print_section:
            if "LAYER_CHANGE" in line or "CURRENT_LAYER=1" in line:
                in_print_section = True
            continue

        # Stop scanning at end-of-print parking moves
        if line.startswith("PRINT_END") or "; END" in line:
            break

        if not line or line.startswith(";"):
            if "LAYER_CHANGE" in line:
                layer_count += 1
            continue

        if line.startswith("M82"):
            abs_e = True; continue
        if line.startswith("M83"):
            abs_e = False; continue

        if line.startswith(("G0 ", "G1 ")):
            x_m = re.search(r"X(-?[\d.]+)", line)
            y_m = re.search(r"Y(-?[\d.]+)", line)
            z_m = re.search(r"Z(-?[\d.]+)", line)
            e_m = re.search(r"E(-?[\d.]+)", line)
            if x_m:
                x = float(x_m.group(1))
                min_x = min(min_x, x); max_x = max(max_x, x)
            if y_m:
                y = float(y_m.group(1))
                min_y = min(min_y, y); max_y = max(max_y, y)
            if z_m:
                max_z = max(max_z, float(z_m.group(1)))
            if e_m:
                e = float(e_m.group(1))
                delta = (e - last_e) if abs_e else e
                if abs_e:
                    last_e = e
                if delta > 0:
                    total_e += delta

    return {
        "max_z": round(max_z, 3),
        "x_range": (round(min_x, 2) if min_x != float("inf") else 0, round(max_x, 2)),
        "y_range": (round(min_y, 2) if min_y != float("inf") else 0, round(max_y, 2)),
        "xy_footprint": (
            round(max_x - min_x, 2) if max_x > 0 else 0,
            round(max_y - min_y, 2) if max_y > 0 else 0,
        ),
        "total_e_mm": round(total_e, 1),
        "layer_count": layer_count,
    }


def find_print_start(lines: list[str]) -> dict:
    """Find and parse the PRINT_START line so we can verify temps."""
    for line in lines[:200]:
        if line.strip().startswith("PRINT_START"):
            m = re.search(
                r'PRINT_START\s+BED=(\S+)\s+HOTEND=(\S+)\s+CHAMBER=(\S+)',
                line
            )
            if m:
                return {
                    "bed": m.group(1),
                    "hotend": m.group(2),
                    "chamber": m.group(3),
                }
    return {}


def check_gcode(path: Path, expected_z: float | None = None,
                expected_xy: tuple[float, float] | None = None,
                material: str | None = None) -> bool:
    console.rule(f"[cyan]Checking {path.name}")
    if not path.exists():
        console.print(f"[red]File not found: {path}")
        return False

    lines = path.read_text(errors="replace").splitlines()
    console.print(f"Size: {path.stat().st_size:,} bytes, {len(lines):,} lines")

    meta = parse_header(lines)
    scan = scan_gcode_print_only(lines)
    ps = find_print_start(lines)

    t = Table(show_header=True, header_style="bold")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Slicer", meta.get("slicer", "?"))
    t.add_row("Filament type", meta.get("filament_type", "?"))
    t.add_row("Est. print time", meta.get("estimated_time", "?"))
    t.add_row("Object height (header)", meta.get("object_height", "?") + " mm")
    t.add_row("Max Z (printing only)", f"{scan['max_z']} mm")
    t.add_row("Layer count", str(scan["layer_count"]))
    t.add_row("Filament", f"{scan['total_e_mm']} mm")
    t.add_row("XY footprint",
              f"{scan['xy_footprint'][0]} × {scan['xy_footprint'][1]} mm")
    t.add_row("X range", f"{scan['x_range'][0]} → {scan['x_range'][1]}")
    t.add_row("Y range", f"{scan['y_range'][0]} → {scan['y_range'][1]}")
    if ps:
        t.add_row("PRINT_START BED", f"{ps.get('bed', '?')}°C")
        t.add_row("PRINT_START HOTEND", f"{ps.get('hotend', '?')}°C")
        t.add_row("PRINT_START CHAMBER", f"{ps.get('chamber', '?')}°C")
    console.print(t)

    ok = True
    issues = []
    if expected_z is not None and abs(scan["max_z"] - expected_z) > 1.0:
        issues.append(f"Expected max Z ~{expected_z}mm, got {scan['max_z']}mm")
        ok = False
    if expected_xy is not None:
        ex, ey = expected_xy
        ax, ay = scan["xy_footprint"]
        if abs(ax - ex) > 2 or abs(ay - ey) > 2:
            issues.append(f"Expected XY ~{ex}×{ey}mm, got {ax}×{ay}mm")
            ok = False
    # Bed bounds check on actual printing only
    if scan["x_range"][1] > 280:
        issues.append(f"Print exceeds X bed (max X={scan['x_range'][1]})")
        ok = False
    if scan["y_range"][1] > 280:
        issues.append(f"Print exceeds Y bed (max Y={scan['y_range'][1]})")
        ok = False
    if scan["x_range"][0] < 0 or scan["y_range"][0] < 0:
        issues.append(f"Print has negative coordinates")
        ok = False
    
    # Temperature sanity check
    if material and material in MATERIAL_TEMPS:
        expected_bed, expected_hotend, _ = MATERIAL_TEMPS[material]
        if ps:
            try:
                bed_actual = int(ps.get("bed", "0"))
                hotend_actual = int(ps.get("hotend", "0"))
                if bed_actual != expected_bed:
                    issues.append(
                        f"Bed temp {bed_actual}°C, expected {expected_bed}°C for {material}"
                    )
                    ok = False
                if hotend_actual != expected_hotend:
                    issues.append(
                        f"Hotend temp {hotend_actual}°C, expected {expected_hotend}°C for {material}"
                    )
                    ok = False
            except ValueError:
                pass

    if issues:
        console.print(Panel("\n".join(issues), title="[red]Issues",
                            border_style="red"))
    else:
        console.print("[green]✓ Gcode looks sane")
    return ok


# =============================================================================
# Slicer
# =============================================================================

def slice_stl(stl_path: Path, out_gcode: Path,
              material: str = "pla", process: str = "standard",
              brim_width: float = 0.0, z_offset: float = 0.0,
              process_overrides: dict | None = None,
              filament_overrides: dict | None = None) -> Path:
    orca = find_orca()
    out_gcode.parent.mkdir(parents=True, exist_ok=True)

    machine_p = resolve_profile("machine", PROFILES["machine"])
    filament_p = resolve_profile("filament", PROFILES["filaments"][material])
    process_p = resolve_profile("process", PROFILES["processes"][process])

    console.print(f"[cyan]Slicing {stl_path.name}")
    console.print(f"  Machine:  {machine_p.name}")
    console.print(f"  Filament: {filament_p.name}")
    console.print(f"  Process:  {process_p.name}")

    work_dir = out_gcode.parent

    # Collect all process overrides into a single patched JSON
    _tmp_files: list[Path] = []
    overrides: dict = {}
    if brim_width > 0:
        overrides.update({"brim_type": "outer_only", "brim_width": str(brim_width),
                          "brim_object_gap": "0.1", "skirt_loops": "0"})
        console.print(f"  [yellow]Brim:     {brim_width} mm (outer_only)")
    if process_overrides:
        overrides.update({k: str(v) for k, v in process_overrides.items()})
        for k, v in process_overrides.items():
            console.print(f"  [yellow]{k}: {v}")
    effective_process = process_p
    if overrides:
        base = json.loads(process_p.read_text())
        base.update(overrides)
        patched = Path(tempfile.mktemp(suffix=".json", prefix="proc_"))
        patched.write_text(json.dumps(base))
        effective_process = patched
        _tmp_files.append(patched)
    settings_chain = f"{machine_p};{effective_process}"

    # Filament overrides (fan speeds etc.) live in the filament profile, whose
    # values are single-element arrays. Wrap scalars accordingly.
    effective_filament = filament_p
    if filament_overrides:
        fbase = json.loads(filament_p.read_text())
        for k, v in filament_overrides.items():
            fbase[k] = v if isinstance(v, list) else [str(v)]
            console.print(f"  [yellow]{k}: {v}")
        fpatched = Path(tempfile.mktemp(suffix=".json", prefix="filament_"))
        fpatched.write_text(json.dumps(fbase))
        effective_filament = fpatched
        _tmp_files.append(fpatched)

    cmd = [
        str(orca),
        "--load-settings", settings_chain,
        "--load-filaments", str(effective_filament),
        "--orient", "0",       # respect STL orientation (we designed for flat-down)
        "--arrange", "1",      # but center on the bed
        "--slice", "0",
        "--outputdir", str(work_dir),
        str(stl_path),
    ]

    console.print(f"\n[dim]$ {' '.join(str(c) for c in cmd)}\n")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    for f in _tmp_files:
        f.unlink(missing_ok=True)

    if result.returncode != 0:
        console.print("[red]Slicer failed:")
        console.print(result.stderr[:3000])
        if not result.stderr:
            # OrcaSlicer prints errors to stdout sometimes
            console.print(result.stdout[-3000:])
        raise RuntimeError(f"OrcaSlicer exited {result.returncode}")

    # Find the produced gcode (OrcaSlicer may name it after the STL or plate_N)
    expected = work_dir / (stl_path.stem + ".gcode")
    pre_mtime = expected.stat().st_mtime if expected.exists() else 0
    # Pick the freshest gcode newer than anything before slicing
    candidates = sorted(
        (g for g in work_dir.glob("*.gcode") if g.stat().st_mtime > pre_mtime),
        key=lambda p: p.stat().st_mtime, reverse=True,
    )
    if not candidates and expected.exists():
        candidates = [expected]  # slicer overwrote in-place
    if candidates:
        chosen = candidates[0]
        if chosen != out_gcode:
            shutil.move(str(chosen), str(out_gcode))
    else:
        raise FileNotFoundError(
            f"No gcode produced. Slicer output:\n{result.stdout[:2000]}"
        )

    console.print(f"[green]✓ Sliced: {out_gcode.name}")

    # Post-process to fix temperatures (workaround for QIDI profile bug)
    pp = postprocess_gcode(out_gcode, material, z_offset=z_offset)
    if pp.get("changed"):
        console.print(f"[cyan]Post-processed gcode for material '{material}':")
        for change in pp["changes"]:
            console.print(f"  ✓ {change}")
    elif "warning" in pp:
        console.print(f"[yellow]Post-process warning: {pp['warning']}")

    return out_gcode


# =============================================================================
# Print
# =============================================================================

def send_and_print(m: Moonraker, gcode_path: Path) -> None:
    if not m.is_ready():
        console.print(f"[red]Printer not ready (state: {m.state()})")
        sys.exit(1)
    console.print(f"[cyan]Uploading {gcode_path.name}...")
    m.upload(gcode_path)
    console.print("[green]✓ Uploaded")
    console.print(f"[cyan]Starting print...")
    m.start_print(gcode_path.name)
    console.print("[green]✓ Print started")


def print_status(m: Moonraker) -> None:
    try:
        data = m.query("extruder&heater_bed&toolhead&print_stats&display_status")
    except Exception as e:
        console.print(f"[red]Cannot query: {e}")
        return

    t = Table(title=f"Plus4 Status @ {m.host}")
    t.add_column("Metric"); t.add_column("Value")

    ext = data.get("extruder", {}); bed = data.get("heater_bed", {})
    th = data.get("toolhead", {}); ps = data.get("print_stats", {})
    ds = data.get("display_status", {})

    t.add_row("Extruder",
              f"{ext.get('temperature', 0):.1f}°C / {ext.get('target', 0):.0f}°C")
    t.add_row("Bed",
              f"{bed.get('temperature', 0):.1f}°C / {bed.get('target', 0):.0f}°C")
    pos = th.get("position", [0, 0, 0, 0])
    t.add_row("Position", f"X={pos[0]:.1f} Y={pos[1]:.1f} Z={pos[2]:.2f}")
    t.add_row("Homed", th.get("homed_axes", "-"))
    t.add_row("Print state", ps.get("state", "-"))
    t.add_row("Filename", ps.get("filename") or "(none)")
    t.add_row("Progress", f"{ds.get('progress', 0) * 100:.1f}%")
    console.print(t)


# =============================================================================
# Commands
# =============================================================================

def cmd_slice(args):
    stl = Path(args.stl).resolve()
    if not stl.exists():
        console.print(f"[red]STL not found: {stl}"); sys.exit(1)
    out = Path(args.out).resolve() if args.out else stl.with_suffix(".gcode")
    overrides: dict = {}
    if args.fast:
        overrides.update({
            "sparse_infill_density": "10%",
            "sparse_infill_pattern": "lightning",
            "layer_height": "0.28",
            "top_shell_layers": "2",
            "bottom_shell_layers": "2",
        })
    for kv in args.overrides:
        if "=" not in kv:
            console.print(f"[red]Bad --set '{kv}', expected KEY=VALUE"); sys.exit(1)
        k, v = kv.split("=", 1)
        overrides[k.strip()] = v.strip()
    fil_overrides: dict = {}
    for kv in args.filament_overrides:
        if "=" not in kv:
            console.print(f"[red]Bad --set-filament '{kv}', expected KEY=VALUE"); sys.exit(1)
        k, v = kv.split("=", 1)
        fil_overrides[k.strip()] = v.strip()
    slice_stl(stl, out, material=args.material, process=args.process,
              brim_width=args.brim, z_offset=args.z_offset,
              process_overrides=overrides or None,
              filament_overrides=fil_overrides or None)
    if args.check:
        check_gcode(out, material=args.material)


def cmd_check(args):
    ok = check_gcode(Path(args.gcode),
                     expected_z=args.expected_z,
                     expected_xy=(args.expected_x, args.expected_y) if args.expected_x else None,
                     material=args.material)
    sys.exit(0 if ok else 2)


def cmd_send(args):
    send_and_print(Moonraker(args.host), Path(args.gcode))


def cmd_status(args):
    print_status(Moonraker(args.host))


def cmd_stop(args):
    Moonraker(args.host).cancel_print()
    console.print("[yellow]Print cancelled")


def cmd_estop(args):
    Moonraker(args.host).emergency_stop()
    console.print("[red]EMERGENCY STOP sent")


def main():
    p = argparse.ArgumentParser(description="Plus4 headless print pipeline")
    p.add_argument("--host", default=DEFAULT_HOST, help="Printer IP")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("slice", help="Slice STL via OrcaSlicer CLI")
    c.add_argument("stl")
    c.add_argument("--out")
    c.add_argument("--material", default="pla",
                   choices=list(MATERIAL_TEMPS.keys()))
    c.add_argument("--process", default="standard",
                   choices=list(PROFILES["processes"].keys()))
    c.add_argument("--brim", type=float, default=0.0,
                   help="Brim width in mm (0 = none, 5-10 recommended for large flat parts)")
    c.add_argument("--z-offset", type=float, default=0.0,
                   help="First-layer Z tweak in mm (negative = closer to bed, e.g. -0.10)")
    c.add_argument("--fast", action="store_true",
                   help="Aggressive speed: lightning infill 10%%, 0.28mm layers, 2 top/bottom")
    c.add_argument("--set", action="append", default=[], dest="overrides",
                   metavar="KEY=VALUE",
                   help="Override any process setting, repeatable "
                        "(e.g. --set raft_layers=4 --set initial_layer_speed=20)")
    c.add_argument("--set-filament", action="append", default=[], dest="filament_overrides",
                   metavar="KEY=VALUE",
                   help="Override any filament setting, repeatable "
                        "(e.g. --set-filament fan_max_speed=40 --set-filament close_fan_the_first_x_layers=3)")
    c.add_argument("--check", action="store_true",
                   help="Sanity check after slicing")
    c.set_defaults(func=cmd_slice)

    c = sub.add_parser("check", help="Inspect gcode")
    c.add_argument("gcode")
    c.add_argument("--expected-z", type=float)
    c.add_argument("--expected-x", type=float)
    c.add_argument("--expected-y", type=float)
    c.add_argument("--material",
                   help="Verify temperatures match expected for material")
    c.set_defaults(func=cmd_check)

    c = sub.add_parser("send", help="Upload and print")
    c.add_argument("gcode")
    c.set_defaults(func=cmd_send)

    c = sub.add_parser("status", help="Show status")
    c.set_defaults(func=cmd_status)

    c = sub.add_parser("stop", help="Cancel print")
    c.set_defaults(func=cmd_stop)

    c = sub.add_parser("estop", help="Emergency stop")
    c.set_defaults(func=cmd_estop)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
