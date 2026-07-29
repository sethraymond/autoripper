#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

import yaml

RAW = Path("/data/rips/raw")
MEDIA = Path("/data/media/tv")


show = sys.argv[1]
manifest_file = Path(sys.argv[2])


with open(manifest_file) as f:
    manifest = yaml.safe_load(f)
    disc = manifest["disc"]
    source_dir = RAW / show / disc

    destination = MEDIA / show / "Season 01"
    destination.mkdir(parents=True, exist_ok=True)

    files = sorted(source_dir.glob("*_t*.mkv"))
    for episode in manifest["episodes"]:
        track = episode["track"]
        src = files[track]
        filename = f"{show} - " f"{episode['episode']} - " f"{episode['title']}.mkv"
        intermediate = destination / filename
        print(f"Processing {src.name} -> {intermediate.name}")

        subprocess.run(
            [
                "HandBrakeCLI",
                "-i",
                str(src),
                "-o",
                str(intermediate),
                "--encoder",
                "qsv_h265",
                "--quality",
                "28",
                "--all-audio",
                "--all-subtitles",
            ],
            check=True,
        )

        print("Done")
