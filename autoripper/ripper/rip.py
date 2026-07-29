#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path

RAW = Path("/data/rips/raw")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("show", type=str)
    parser.add_argument("disc", type=str)

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

if __name__ == "__main__":
    main()
