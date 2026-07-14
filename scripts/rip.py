#!/usr/bin/env python3

import sys
import subprocess
import argparse
from pathlib import Path

RAW = Path("/data/rips/raw")

parser = argparse.ArgumentParser()


if len(sys.argv) != 3:
    print("Usage: rip.py <show> <disc>")
    sys.exit(1)

    show = sys.argv[1]
    disc = sys.argv[2]

    output = RAW / show / disc
    output.mkdir(parents=True, exist_ok=True)

    print(f"Ripping {show} - {disc}")
    print(f"Output: {output}")

    subprocess.run(["makemkvcon", "mkv", "disc:0", "all", str(output)], check=True)

    print("Rip complete")
