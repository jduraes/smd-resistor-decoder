# SMD Resistor Decoder

A Python package and small GUI app to convert SMD resistor digit codes (e.g., 103, 4R7, 01C, 1002) into real resistance values with units.

Features:
- Supports common SMD code schemes: 3-digit, 4-digit, EIA-96 (two digits + letter), and R-as-decimal notation (e.g., 4R7)
- CLI and Tkinter-based GUI
- Library API with tests
- GUI extras: live decode, copy-to-clipboard, theme toggle (light/dark), and saved window size

Requirements:
- Python 3.8+
- Tkinter (usually included; on Linux install python3-tk)

Install (editable):
- python -m pip install -e .

Quick start:
- CLI: `python -m smdresistor 103` or `smdresistor 103`
- GUI: `python -m smdresistor.gui` or `smdresistor-gui`

Examples:
- 103 -> 10kΩ (3-digit)
- 4R7 -> 4.7Ω (R)
- 01C -> 100Ω (EIA-96)

Development:
- Run tests: `python -m pip install pytest && PYTHONPATH=src python -m pytest -q`
- Lint/format: optional (add your preferred tools)

Build standalone executables locally (PyInstaller):
- python -m pip install pyinstaller
- PYTHONPATH=src pyinstaller -n smdresistor-gui --onefile -w -F smdresistor/gui.py
  - Output in `dist/`

CI builds (GitHub Actions):
- A workflow at `.github/workflows/ci.yml` builds on Windows, macOS, and Linux, runs tests, and uploads artifacts.

License: MIT
