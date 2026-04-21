# CyberWing Print Pipeline — Requirements Document

**Project:** Headless STL → Slice → Print workflow for QIDI Plus4
**Target user:** CyberWing engineering team (CanaryBox enclosure iteration)
**Status:** Draft v0.1

---

## 1. Overview

### 1.1 Goal

Build a scriptable, version-controlled Python pipeline that takes an STL file from CAD export through to a physical print on the QIDI Plus4, without opening the QIDI Studio GUI. The pipeline should be reproducible, testable, and suitable for iterative hardware development (CanaryBox Pelican insert, sensor mounts, cable management brackets, etc.).

### 1.2 Scope

**In scope:**
- Loading and overriding slicer profiles (machine, filament, process)
- Slicing STL/3MF files to G-code via OrcaSlicer CLI
- Uploading G-code to the Plus4 via the Moonraker HTTP API
- Starting, monitoring, and canceling prints programmatically
- Managing print queues, storing artifacts, logging results
- Parameter sweeps for calibration (temperature towers, retraction, flow)

**Out of scope (v1):**
- Bed mesh or Z-offset calibration automation
- Multi-material / QidiBox filament changes
- Slicer UI or visualization layer
- Cloud-based remote print orchestration

### 1.3 Success criteria

A new engineer can clone the repo, install dependencies, edit a YAML config, and run one Python command to slice a CAD export and start a print on the Plus4 in the CyberWing lab — with full reproducibility across machines.

---

## 2. System Requirements

### 2.1 Host environment

- **OS:** macOS 13+ (primary), Ubuntu 22.04+ (secondary). Windows support optional.
- **Python:** 3.11 or newer
- **Architecture:** arm64 and x86_64
- **Disk:** 500 MB minimum for OrcaSlicer, plus gcode/log storage
- **Network:** same LAN as the Plus4, or VPN with routable access to the printer's IP

### 2.2 External dependencies

| Dependency | Version | Purpose |
|---|---|---|
| OrcaSlicer | 2.1.0+ | CLI slicing engine |
| Python | 3.11+ | Pipeline runtime |
| QIDI Plus4 firmware | Stock or community (Moonraker enabled) | API endpoint |

### 2.3 Python package dependencies

- `requests` — HTTP calls to Moonraker
- `pydantic` — config schema validation
- `pyyaml` — human-editable config files
- `click` or `typer` — CLI entry points
- `rich` — terminal output formatting and progress bars
- `websockets` — real-time print status from Moonraker
- `pytest` — test suite
- `pathlib`, `subprocess`, `json`, `logging` — stdlib

---

## 3. Functional Requirements

### 3.1 Profile management (FR-1)

**FR-1.1** The system shall load machine, filament, and process profiles from JSON files matching the OrcaSlicer schema.

**FR-1.2** The system shall support profile inheritance — a user profile may `inherits` a system base profile and override specific fields.

**FR-1.3** The system shall validate profiles against a Pydantic schema before slicing, with clear error messages for malformed or missing required fields.

**FR-1.4** The system shall support runtime parameter overrides (e.g., nozzle_temperature, max_volumetric_speed) without requiring a new JSON file on disk — overrides are written to a temporary profile and cleaned up after slicing.

**FR-1.5** Profiles shall be stored in a directory structure suitable for git version control:
```
profiles/
  machines/{printer}.json
  filaments/{vendor}_{material}_{hardness}.json
  processes/{layer_height}_{quality_target}.json
```

### 3.2 Slicing (FR-2)

**FR-2.1** The system shall invoke the OrcaSlicer CLI with a specified STL/3MF input, a set of profile JSON files, and output G-code to a specified directory.

**FR-2.2** The system shall detect OrcaSlicer binary location automatically on macOS (`/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer`) and Linux (`which orcaslicer` or AppImage path), with an override env var `ORCASLICER_PATH`.

**FR-2.3** Slicer stdout/stderr shall be captured and logged. Non-zero exit codes shall raise a `SlicingError` exception with the captured error output.

**FR-2.4** The system shall verify the output .gcode file exists and is non-empty before considering a slice successful.

**FR-2.5** The system shall parse the gcode header to extract metadata (estimated print time, filament usage, layer count) and return it as a structured result.

**FR-2.6** The system shall support batch slicing — given a list of (STL, profile) pairs, produce a corresponding list of gcode files, with parallelism controlled by a concurrency parameter.

### 3.3 Parameter sweeps (FR-3)

**FR-3.1** The system shall support generating parameter sweeps — e.g., slice the same STL at nozzle temperatures from 210°C to 240°C in 5°C increments — producing one gcode file per parameter value.

**FR-3.2** Sweep outputs shall be named predictably (e.g., `vase_test_nozzle_220.gcode`) and placed in a sweep-specific directory.

**FR-3.3** The system shall produce a manifest file (JSON or CSV) mapping gcode filenames to the parameter values used.

### 3.4 Printer communication (FR-4)

**FR-4.1** The system shall communicate with the Plus4 via the Moonraker HTTP API on port 7125 (or configurable).

**FR-4.2** The printer IP or hostname shall be configurable via env var (`PLUS4_HOST`) or config file.

**FR-4.3** The system shall authenticate with Moonraker where authentication is enabled, supporting either API key or one-shot tokens.

**FR-4.4** The system shall support the following Moonraker operations:
- `upload_gcode(path) → file_id` — upload a gcode file to the printer
- `list_files() → [files]` — list gcode files on the printer SD card
- `delete_file(filename)` — remove a gcode file
- `start_print(filename)` — begin printing an uploaded file
- `pause_print()`, `resume_print()`, `cancel_print()` — print control
- `get_status() → PrinterStatus` — current state (idle, printing, error), temperatures, progress
- `emergency_stop()` — immediate halt

**FR-4.5** The system shall handle network errors gracefully with configurable retry (default: 3 retries with exponential backoff).

**FR-4.6** The system shall verify printer state is `ready` before starting a print and raise an error otherwise.

### 3.5 Print monitoring (FR-5)

**FR-5.1** The system shall optionally subscribe to Moonraker websocket events for real-time status updates during a print.

**FR-5.2** The system shall display a progress bar showing layer, time elapsed, time remaining, and current temperatures.

**FR-5.3** The system shall detect abnormal conditions (thermal runaway, filament runout, cancelled state) and surface them as exceptions or logged warnings.

**FR-5.4** The system shall support a `--wait` flag that blocks the Python process until the print completes, with optional timeout.

### 3.6 Pre-flight checks (FR-6)

**FR-6.1** Before uploading a gcode file, the system shall verify:
- Printer is online and reachable
- Printer is in `ready` or `standby` state (not currently printing)
- Sufficient disk space on the printer SD card (min 10 MB free)
- Gcode file passes a sanity check (has valid start/end markers, references the correct printer model in its header)

**FR-6.2** Pre-flight checks shall be skippable with a `--force` flag for advanced users.

### 3.7 Logging and artifacts (FR-7)

**FR-7.1** Every run shall produce a timestamped log file containing: input files, profile used, overrides applied, slicer output, printer API calls, final print status.

**FR-7.2** Sliced gcode shall be archived per-run in a configurable artifact directory, not overwritten.

**FR-7.3** Log format shall be structured (JSON lines) to enable later analysis.

### 3.8 CLI interface (FR-8)

**FR-8.1** The system shall expose a `cwprint` command-line tool with subcommands:
```
cwprint slice <stl> --profile <name> [--override key=value]...
cwprint upload <gcode> [--host <ip>]
cwprint print <filename>
cwprint status
cwprint cancel
cwprint sweep <stl> --param <key> --range <start>,<end>,<step>
cwprint run <stl> --profile <name>           # slice + upload + print in one
```

**FR-8.2** The CLI shall support `--dry-run` mode that runs slicing but skips printer operations.

**FR-8.3** Each subcommand shall support `--help` with examples.

### 3.9 Configuration (FR-9)

**FR-9.1** A user config file shall live at `~/.cwprint/config.yaml` with defaults for printer host, OrcaSlicer path, default profiles, and output directories.

**FR-9.2** Config values shall be overridable by env vars (prefix `CWPRINT_`) and then by CLI flags, in that order of precedence.

**FR-9.3** A project-local config file (`.cwprint.yaml` in the working directory) shall override user config for project-specific profiles.

---

## 4. Non-Functional Requirements

### 4.1 Reliability (NFR-1)

- Slicer invocation failures, network timeouts, and API errors shall not crash the Python process — all exceptions shall be caught and reported with actionable messages.
- The system shall be idempotent where possible — re-running a slice with identical inputs produces identical gcode (modulo slicer nondeterminism).

### 4.2 Performance (NFR-2)

- Slicing a 50×50×50mm part at 0.2mm layer height shall complete in under 30 seconds on an M-series Mac.
- Parameter sweeps shall run slices in parallel, with concurrency defaulting to `min(cpu_count, 4)`.
- Gcode upload to the Plus4 shall achieve at least 5 MB/s on gigabit LAN.

### 4.3 Security (NFR-3)

- API keys shall not be logged or committed to version control.
- The config file shall be readable only by the current user (0600 permissions).
- The system shall warn if the printer is reachable over untrusted networks.

### 4.4 Observability (NFR-4)

- All Moonraker API calls shall be logged with request/response pairs at DEBUG level.
- Slicer CLI invocations shall be logged with the exact command line for reproducibility.
- Print completion shall emit a structured event suitable for downstream ingestion (e.g., into a build log for the CanaryBox iteration history).

### 4.5 Testability (NFR-5)

- Unit tests shall cover profile loading, override application, gcode parsing, and Moonraker API wrappers (mocked).
- Integration tests shall cover end-to-end slicing with a fixture STL (no printer required).
- A `--mock-printer` mode shall simulate Moonraker responses for CI.

### 4.6 Maintainability (NFR-6)

- Code shall follow PEP 8, type-hinted throughout, with `mypy --strict` clean.
- Public APIs shall have docstrings in Google style.
- Profile JSON schema shall be documented with a schema file (JSON Schema or Pydantic model export).

---

## 5. Repository Structure

```
cyberwing-print-pipeline/
├── README.md
├── pyproject.toml
├── .cwprint.yaml.example
├── profiles/
│   ├── machines/
│   │   └── qidi_plus4_0.4mm.json
│   ├── filaments/
│   │   ├── sunlu_tpu_95a.json
│   │   ├── qidi_pla.json
│   │   └── polymaker_pa12cf.json
│   └── processes/
│       ├── 0.20mm_standard.json
│       └── 0.20mm_tpu_slow.json
├── src/cwprint/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── profiles.py
│   ├── slicer.py
│   ├── moonraker.py
│   ├── monitor.py
│   ├── sweeps.py
│   └── errors.py
├── tests/
│   ├── fixtures/
│   │   └── cube_20mm.stl
│   ├── test_profiles.py
│   ├── test_slicer.py
│   ├── test_moonraker.py
│   └── test_cli.py
├── docs/
│   ├── getting_started.md
│   ├── profile_authoring.md
│   └── calibration_workflows.md
└── scripts/
    ├── dump_existing_profiles.sh
    └── calibration_temp_tower.py
```

---

## 6. Open Questions / Future Work

- **Multi-printer support:** when CyberWing acquires a second printer, should the tool target specific machines by name, or always the default?
- **Firmware version compatibility:** which Moonraker API versions are validated? Document the minimum firmware.
- **CanaryBox-specific:** should the pipeline emit a print-card artifact (QR code, RFID tag) with the build metadata for each CanaryBox enclosure printed?
- **Material tracking:** integrate with a filament inventory to deduct estimated filament usage per print?
- **Failure classification:** when a print fails mid-run, can we automatically categorize the failure (adhesion, clog, thermal) from Moonraker telemetry for later analysis?

---

## 7. Acceptance Criteria

The v1 release is complete when:

1. A new clone + `pip install -e .` results in a working `cwprint` command within 5 minutes on a clean Mac.
2. `cwprint run vase_test.stl --profile tpu_95a_plus4` successfully slices, uploads, and starts a print on the CyberWing lab Plus4.
3. A parameter sweep of 10 variants runs in under 5 minutes of slicer time.
4. CI passes on macOS and Ubuntu with `pytest` and `mypy --strict`.
5. Documentation covers: installation, first print, authoring a new filament profile, running a calibration sweep.
