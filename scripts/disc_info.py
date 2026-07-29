import argparse
import re
import shlex
import subprocess
from pathlib import Path

import yaml

STUB = True
def _is_existing_path(string):
    """Validates that a path exists and converts it to a pathlib.Path object."""
    path = Path(string)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"The path '{string}' does not exist.")
    return path

def get_disc_info():
    if STUB:
        return 'CINFO:2,0,"Avatar: The Last Airbender Book One: Water Disc 3"'
    info = subprocess.run(shlex.split("makemkvcon -r info disc:0"), check=True, capture_output=True, text=True)
    return info.stdout.splitlines()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("show_config", type=_is_existing_path, default="/config/shows.yaml")
    args = parser.parse_args()
    with args.show_config.open("r") as f:
        shows = yaml.safe_load(f)
    
    disc_info: str = ''
    show: str = ''
    for line in get_disc_info():
        if line.startswith("CINFO"):
            regex = re.compile(r"CINFO:([0-9]+),([0-9]+),(\".*\")")   
            m = regex.match(line)
            if m is not None:
                id, code, value = m.groups()
                id = int(id)
                code = int(code)
                if id == 2:
                    for show in shows.keys():
                        if value.startswith(show):
                            _, disc_info = value.split(show)
                            break
    if disc_info and show:
        manifest_dir = shows[show]["manifest_dir"]
        # send request to ripper
