#!/usr/bin/env python3
"""
plus4_doctor.py — QIDI Plus4 diagnostic tool

A standalone script that queries the Moonraker API on the Plus4 and reports
printer health, configuration, recent errors, and suggests fixes.

Usage:
    python plus4_doctor.py --host 192.168.1.XX
    python plus4_doctor.py --host plus4.local --verbose
    python plus4_doctor.py --host 192.168.1.XX --watch       # live monitor
    python plus4_doctor.py --host 192.168.1.XX --extrude-test # run extrude test

Requires: pip install requests rich
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from typing import Any

try:
    import requests
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.live import Live
except ImportError:
    print("Missing deps. Run: pip install requests rich")
    sys.exit(1)

console = Console()


# -----------------------------------------------------------------------------
# Moonraker client
# -----------------------------------------------------------------------------

@dataclass
class Moonraker:
    host: str
    port: int = 7125
    timeout: float = 5.0

    @property
    def base(self) -> str:
        return f"http://{self.host}:{self.port}"

    def get(self, path: str, **params: Any) -> dict:
        r = requests.get(f"{self.base}{path}", params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def post(self, path: str, **json_body: Any) -> dict:
        r = requests.post(f"{self.base}{path}", json=json_body or None,
                          timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    # --- Specific endpoints -------------------------------------------------

    def ping(self) -> bool:
        try:
            self.get("/server/info")
            return True
        except Exception:
            return False

    def server_info(self) -> dict:
        return self.get("/server/info")["result"]

    def printer_info(self) -> dict:
        return self.get("/printer/info")["result"]

    def objects_list(self) -> list[str]:
        return self.get("/printer/objects/list")["result"]["objects"]

    def query(self, objects: dict[str, list[str] | None]) -> dict:
        """Query specific Klipper objects.
        
        Example: query({"extruder": None, "toolhead": ["position", "homed_axes"]})
        """
        parts = []
        for obj, fields in objects.items():
            if fields is None:
                parts.append(obj)
            else:
                parts.append(f"{obj}={','.join(fields)}")
        return self.get("/printer/objects/query", **{"": "&".join(parts)})

    def query_raw(self, query_string: str) -> dict:
        url = f"{self.base}/printer/objects/query?{query_string}"
        r = requests.get(url, timeout=self.timeout)
        r.raise_for_status()
        return r.json()["result"]["status"]

    def gcode(self, script: str) -> dict:
        return self.post("/printer/gcode/script", script=script)

    def gcode_help(self) -> dict:
        return self.get("/printer/gcode/help")["result"]

    def logs(self) -> str:
        """Fetch the Klipper log (may be large)."""
        r = requests.get(f"{self.base}/server/files/klippy.log", timeout=30)
        r.raise_for_status()
        return r.text

    def history(self, limit: int = 10) -> list[dict]:
        try:
            return self.get("/server/history/list", limit=limit)["result"]["jobs"]
        except Exception:
            return []


# -----------------------------------------------------------------------------
# Diagnostic checks
# -----------------------------------------------------------------------------

@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str
    fix: str | None = None


def check_connectivity(m: Moonraker) -> CheckResult:
    if not m.ping():
        return CheckResult(
            "Connectivity", False,
            f"Cannot reach Moonraker at {m.base}",
            fix="Verify the printer is powered on and on the same network. "
                "Try pinging the IP. Check that port 7125 is open."
        )
    return CheckResult("Connectivity", True, f"Moonraker reachable at {m.base}")


def check_klipper_state(m: Moonraker) -> CheckResult:
    info = m.printer_info()
    state = info.get("state", "unknown")
    msg = info.get("state_message", "")
    ok = state == "ready"
    fix = None
    if state == "error":
        fix = "Klipper is in error state. Check klippy.log for details. "\
              "Often needs FIRMWARE_RESTART to clear."
    elif state == "shutdown":
        fix = "Klipper is shut down. Usually thermal runaway or MCU comm loss. "\
              "Power cycle the printer."
    elif state == "startup":
        fix = "Klipper is still starting up. Wait 30s and retry."
    return CheckResult("Klipper state", ok, f"{state}: {msg}", fix)


def check_temperatures(m: Moonraker) -> list[CheckResult]:
    data = m.query_raw("extruder&heater_bed&temperature_sensor%20chamber_sensor")
    results = []
    
    # Extruder
    ext = data.get("extruder", {})
    temp = ext.get("temperature", 0)
    target = ext.get("target", 0)
    if target > 0 and abs(temp - target) > 5:
        results.append(CheckResult(
            "Extruder temp", False,
            f"Actual {temp:.1f}°C, target {target:.1f}°C — not stable",
            fix="Wait for extruder to reach target. If oscillating, run PID_CALIBRATE HEATER=extruder"
        ))
    else:
        results.append(CheckResult(
            "Extruder temp", True, f"{temp:.1f}°C (target {target:.1f}°C)"
        ))
    
    # Bed
    bed = data.get("heater_bed", {})
    btemp = bed.get("temperature", 0)
    btarget = bed.get("target", 0)
    if btarget > 0 and abs(btemp - btarget) > 3:
        results.append(CheckResult(
            "Bed temp", False,
            f"Actual {btemp:.1f}°C, target {btarget:.1f}°C — not stable"
        ))
    else:
        results.append(CheckResult(
            "Bed temp", True, f"{btemp:.1f}°C (target {btarget:.1f}°C)"
        ))
    
    return results


def check_toolhead(m: Moonraker) -> list[CheckResult]:
    data = m.query_raw("toolhead&gcode_move")
    results = []
    
    th = data.get("toolhead", {})
    homed = th.get("homed_axes", "")
    if homed != "xyz":
        results.append(CheckResult(
            "Homing", False,
            f"Only '{homed}' axes homed (need xyz)",
            fix="Send G28 to home all axes before printing."
        ))
    else:
        results.append(CheckResult("Homing", True, "All axes homed (xyz)"))
    
    pos = th.get("position", [0, 0, 0, 0])
    results.append(CheckResult(
        "Position", True,
        f"X={pos[0]:.2f} Y={pos[1]:.2f} Z={pos[2]:.2f} E={pos[3]:.2f}"
    ))
    
    # Z offset from gcode_move
    gm = data.get("gcode_move", {})
    hp = gm.get("homing_origin", [0, 0, 0, 0])
    if len(hp) >= 3:
        results.append(CheckResult(
            "Z offset", True, f"Z offset applied: {hp[2]:.3f}mm"
        ))
    
    return results


def check_stepper_drivers(m: Moonraker) -> list[CheckResult]:
    """Check TMC driver temperatures — high temps indicate mechanical load or bad cooling."""
    # Try common TMC driver object names
    results = []
    drivers = ["tmc2209 stepper_x", "tmc2209 stepper_y", "tmc2209 stepper_z",
               "tmc5160 stepper_x", "tmc5160 stepper_y", "tmc5160 stepper_z",
               "temperature_sensor x_driver", "temperature_sensor y_driver"]
    
    try:
        available = m.objects_list()
        relevant = [d for d in drivers if d in available]
        if not relevant:
            return []
        
        query_str = "&".join(d.replace(" ", "%20") for d in relevant)
        data = m.query_raw(query_str)
        
        for obj_name in relevant:
            obj = data.get(obj_name, {})
            temp = obj.get("temperature")
            if temp is not None:
                if temp > 90:
                    results.append(CheckResult(
                        f"Driver {obj_name}", False,
                        f"{temp:.1f}°C — running hot",
                        fix="Check stepper cooling fan. Consider lowering motor current."
                    ))
                else:
                    results.append(CheckResult(
                        f"Driver {obj_name}", True, f"{temp:.1f}°C"
                    ))
    except Exception:
        pass
    
    return results


def check_recent_errors(m: Moonraker) -> CheckResult:
    """Scan the last ~200 lines of the Klipper log for errors."""
    try:
        log = m.logs()
    except Exception as e:
        return CheckResult("Log access", False, f"Cannot read log: {e}")
    
    lines = log.splitlines()[-500:]  # last 500 lines
    error_keywords = ["Error", "Shutdown", "Heater", "thermistor",
                      "MCU", "Timeout", "restart"]
    errors = []
    for line in lines:
        if any(kw in line for kw in error_keywords):
            errors.append(line.strip())
    
    # Deduplicate and take recent
    errors = list(dict.fromkeys(errors))[-5:]
    
    if not errors:
        return CheckResult("Recent log", True, "No errors in last 500 log lines")
    
    detail = "\n  ".join(errors)
    return CheckResult(
        "Recent log", False,
        f"Found {len(errors)} concerning lines:\n  {detail}",
        fix="Review full log at /server/files/klippy.log"
    )


def check_print_history(m: Moonraker) -> CheckResult:
    jobs = m.history(limit=5)
    if not jobs:
        return CheckResult("Print history", True, "No recent jobs")
    
    cancelled = sum(1 for j in jobs if j.get("status") == "cancelled")
    failed = sum(1 for j in jobs if j.get("status") == "error")
    completed = sum(1 for j in jobs if j.get("status") == "completed")
    
    detail = f"Last 5: {completed} completed, {cancelled} cancelled, {failed} failed"
    ok = failed == 0
    fix = None
    if failed > 0:
        fix = "Multiple failed prints. Check logs and verify calibration."
    elif cancelled > 2:
        fix = "Lots of cancellations — likely a setup issue. Run full diagnostic."
    
    return CheckResult("Print history", ok, detail, fix)


# -----------------------------------------------------------------------------
# Interactive actions
# -----------------------------------------------------------------------------

def run_extrude_test(m: Moonraker, target_temp: float = 220.0,
                     bed_temp: float = 60.0, amount: float = 20.0,
                     speed: float = 2.0) -> None:
    """Heat up, manually extrude, and report whether filament moved."""
    console.rule("[bold cyan]Extrude test")
    
    console.print(f"[yellow]Setting extruder to {target_temp}°C, bed to {bed_temp}°C...")
    m.gcode(f"M104 S{target_temp}")
    m.gcode(f"M140 S{bed_temp}")
    
    console.print("[yellow]Waiting for extruder to reach temperature...")
    while True:
        data = m.query_raw("extruder")
        t = data.get("extruder", {}).get("temperature", 0)
        console.print(f"  Extruder: {t:.1f}°C", end="\r")
        if t >= target_temp - 2:
            break
        time.sleep(2)
    
    console.print(f"\n[green]Reached temperature. Extruding {amount}mm at {speed}mm/s...")
    console.print("[bold red]>>> WATCH THE NOZZLE NOW <<<")
    
    # Get current E position
    before = m.query_raw("toolhead")["toolhead"]["position"][3]
    
    # Extrude with relative E
    m.gcode("M83")  # relative extrusion
    m.gcode(f"G1 E{amount} F{speed * 60}")  # F is mm/min
    
    # Wait for move to complete
    time.sleep(amount / speed + 2)
    
    after = m.query_raw("toolhead")["toolhead"]["position"][3]
    moved = after - before
    
    console.print(f"\nE-axis moved: {moved:.2f}mm (requested {amount}mm)")
    if abs(moved - amount) > 0.5:
        console.print("[red]⚠ E-axis did not move as expected. Extruder may be disabled or jammed.")
    else:
        console.print("[green]✓ Extruder stepped correctly. Did you see filament come out?")
        console.print("  If YES → feeding is good")
        console.print("  If NO  → clog, buckled filament, or filament not loaded")


def print_config_summary(m: Moonraker) -> None:
    """Show key config values from Klipper."""
    console.rule("[bold cyan]Configuration summary")
    
    try:
        data = m.get("/printer/objects/query?configfile=settings")
        settings = data["result"]["status"]["configfile"]["settings"]
        
        table = Table(show_header=True, header_style="bold")
        table.add_column("Section.Key")
        table.add_column("Value")
        
        interesting = [
            "extruder.max_temp",
            "extruder.min_temp",
            "extruder.pressure_advance",
            "extruder.rotation_distance",
            "heater_bed.max_temp",
            "stepper_z.position_max",
            "printer.max_velocity",
            "printer.max_accel",
        ]
        
        for path in interesting:
            section, key = path.split(".")
            val = settings.get(section, {}).get(key, "?")
            table.add_row(path, str(val))
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]Could not fetch config: {e}")


# -----------------------------------------------------------------------------
# Live monitor
# -----------------------------------------------------------------------------

def live_monitor(m: Moonraker) -> None:
    """Continuously display key printer state until Ctrl-C."""
    console.print("[cyan]Live monitor — Ctrl-C to exit[/]")
    
    def make_table() -> Table:
        try:
            data = m.query_raw(
                "extruder&heater_bed&toolhead&print_stats&display_status"
            )
        except Exception as e:
            t = Table()
            t.add_row(f"[red]Query failed: {e}")
            return t
        
        t = Table(title="QIDI Plus4 Status", show_header=True)
        t.add_column("Metric")
        t.add_column("Value")
        
        ext = data.get("extruder", {})
        bed = data.get("heater_bed", {})
        th = data.get("toolhead", {})
        ps = data.get("print_stats", {})
        ds = data.get("display_status", {})
        
        t.add_row("Extruder", f"{ext.get('temperature', 0):.1f}°C / "
                              f"{ext.get('target', 0):.0f}°C  "
                              f"({ext.get('power', 0)*100:.0f}% power)")
        t.add_row("Bed", f"{bed.get('temperature', 0):.1f}°C / "
                         f"{bed.get('target', 0):.0f}°C  "
                         f"({bed.get('power', 0)*100:.0f}% power)")
        pos = th.get("position", [0, 0, 0, 0])
        t.add_row("Position", f"X={pos[0]:.1f} Y={pos[1]:.1f} "
                              f"Z={pos[2]:.2f} E={pos[3]:.1f}")
        t.add_row("Homed", th.get("homed_axes", "-"))
        t.add_row("Print state", ps.get("state", "-"))
        t.add_row("Filename", ps.get("filename", "-") or "(none)")
        t.add_row("Progress", f"{ds.get('progress', 0)*100:.1f}%")
        t.add_row("Message", ds.get("message", "") or "-")
        
        return t
    
    try:
        with Live(make_table(), refresh_per_second=1, console=console) as live:
            while True:
                time.sleep(1)
                live.update(make_table())
    except KeyboardInterrupt:
        console.print("\n[cyan]Monitor stopped.")


# -----------------------------------------------------------------------------
# Main diagnostic run
# -----------------------------------------------------------------------------

def run_diagnostics(m: Moonraker) -> None:
    console.rule("[bold cyan]QIDI Plus4 Diagnostics")
    console.print(f"Host: [bold]{m.base}[/]\n")
    
    all_results: list[CheckResult] = []
    
    # Connectivity gate
    r = check_connectivity(m)
    all_results.append(r)
    if not r.ok:
        render_results(all_results)
        return
    
    # Server & Klipper info
    try:
        info = m.server_info()
        pinfo = m.printer_info()
        console.print(f"Moonraker: {info.get('moonraker_version', '?')}")
        console.print(f"Klipper: {info.get('klippy_state', '?')}")
        console.print(f"Host: {pinfo.get('hostname', '?')}")
        console.print(f"State: {pinfo.get('state', '?')} — {pinfo.get('state_message', '')}\n")
    except Exception as e:
        console.print(f"[red]Could not fetch info: {e}")
    
    all_results.append(check_klipper_state(m))
    all_results.extend(check_temperatures(m))
    all_results.extend(check_toolhead(m))
    all_results.extend(check_stepper_drivers(m))
    all_results.append(check_recent_errors(m))
    all_results.append(check_print_history(m))
    
    render_results(all_results)


def render_results(results: list[CheckResult]) -> None:
    table = Table(show_header=True, header_style="bold")
    table.add_column("Check", width=22)
    table.add_column("Status", width=8)
    table.add_column("Detail")
    
    for r in results:
        status = "[green]✓ OK" if r.ok else "[red]✗ FAIL"
        table.add_row(r.name, status, r.detail)
    
    console.print(table)
    
    # Fixes panel
    fixes = [r for r in results if not r.ok and r.fix]
    if fixes:
        console.rule("[bold yellow]Suggested fixes")
        for r in fixes:
            console.print(Panel(
                f"[bold]{r.name}[/]\n{r.fix}",
                border_style="yellow"
            ))


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description="QIDI Plus4 diagnostic tool")
    p.add_argument("--host", required=True,
                   help="Printer IP or hostname (e.g., 192.168.86.232 or plus4.local)")
    p.add_argument("--port", type=int, default=7125, help="Moonraker port")
    p.add_argument("--timeout", type=float, default=5.0)
    p.add_argument("--watch", action="store_true", help="Live status monitor")
    p.add_argument("--extrude-test", action="store_true",
                   help="Heat up and run a manual extrude test")
    p.add_argument("--config", action="store_true",
                   help="Print key configuration values")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()
    
    m = Moonraker(host=args.host, port=args.port, timeout=args.timeout)
    
    if args.watch:
        live_monitor(m)
    elif args.extrude_test:
        run_diagnostics(m)
        run_extrude_test(m)
    elif args.config:
        run_diagnostics(m)
        print_config_summary(m)
    else:
        run_diagnostics(m)


if __name__ == "__main__":
    main()
