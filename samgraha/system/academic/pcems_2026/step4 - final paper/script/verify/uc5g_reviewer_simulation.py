"""Verify script for reviewer-simulation usecase.

Checks that a reviewer-simulation semantic run exists for the paper
with 3 reviewer personas and a decision field.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _common import verify_main

if __name__ == "__main__":
    verify_main("reviewer-simulation")
