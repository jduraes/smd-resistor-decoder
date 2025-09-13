#!/usr/bin/env python3
"""
Development script for GUI testing.
Run this to quickly test GUI changes without building.
"""
import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set up X11 forwarding for WSL (if needed)
if 'DISPLAY' not in os.environ:
    os.environ['DISPLAY'] = ':0'

try:
    from smdresistor.gui import run
    print("Starting GUI development session...")
    print("Edit src/smdresistor/gui.py and rerun this script to see changes")
    run()
except KeyboardInterrupt:
    print("\nGUI development session ended")
except Exception as e:
    print(f"Error: {e}")
    print("\nMake sure you have X11 forwarding set up for WSL GUI apps")
    print("Try: export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0")
