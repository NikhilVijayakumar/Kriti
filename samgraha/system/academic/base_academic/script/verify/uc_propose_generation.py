"""Verify script for propose-generation — checks that an approved
generation proposal exists at the current commit."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import verify_main

if __name__ == "__main__":
    verify_main("propose-generation")
