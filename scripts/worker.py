#!/usr/bin/env python3

import time
import yaml
import subprocess
from pathlib import Path


CONFIG = Path("/config")
QUEUE = Path("/data/rips/queue")


with open(CONFIG / "shows.yaml") as f:
    shows = yaml.safe_load(f)


def process_job(job):

    show, manifest_name = job.name.split("__", 1)
    if show not in shows:
        print(f"Unknown show {show}")
        return

    show_cfg = shows[show]
    manifest_dir = show_cfg["manifest_dir"]
    manifest = CONFIG / "manifests" / manifest_dir / f"{manifest_name}.yaml"
    if not manifest.exists():
        print(f"Missing manifest {manifest}")
        return

    subprocess.run(["/opt/rip-stack/process.py", show, str(manifest)], check=True)

    while True:
        for job in QUEUE.iterdir():
            if job.is_file():
                print(f"Processing {job}")
                process_job(job)
                job.unlink()

        time.sleep(30)
