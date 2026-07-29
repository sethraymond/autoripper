import re
import shlex
import subprocess
from pathlib import Path

import yaml


class Ripper:
    STUB = True

    def __init__(self, config_path: Path = Path("/config/shows.yaml")):
        if not config_path.exists():
            raise RuntimeError("[Ripper] Cannot read configuration!")
        self._manifests_path = config_path.parent / "manifests/"
        if not self._manifests_path.exists():
            raise RuntimeError("[Ripper] Cannot find manifests")
        with config_path.open("r") as f:
            self._config = yaml.safe_load(f)

    def rip(self):
        show, manifest = self._get_disc_info()
        output: str = (
            f"/data/{'series' if show[type] == 'tv' else 'movies'}/{show['naming']}/"
        )
        subprocess.run(["makemkvcon", "mkv", "disc:0", "all", output], check=True)
        # TODO: Rename files based on manifest

    def _get_disc_info(self) -> tuple[dict, dict]:
        if self.STUB:
            info = ['CINFO:2,0,"Avatar: The Last Airbender Book One: Water Disc 3"']
        else:
            info = subprocess.run(
                shlex.split("makemkvcon -r info disc:0"),
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
        disc_info: str = ""
        show: str = ""
        for line in info:
            if line.startswith("CINFO"):
                regex = re.compile(r"CINFO:([0-9]+),([0-9]+),\"(.*)\"")
                m = regex.match(line)
                if m is not None:
                    id, code, value = m.groups()
                    id = int(id)
                    code = int(code)
                    if id == 2:
                        for show in self._config.keys():
                            if value.startswith(show):
                                disc_info = value.split(show)[1].lstrip()
                                break
                        if not disc_info:
                            # TODO: this is an issue, fallback to default ripping?
                            pass
        if disc_info and show:
            manifest_dir_name = self._config[show]["manifest_dir"]
            for manifest_file in (self._manifests_path / manifest_dir_name).glob(
                "*.yaml"
            ):
                with manifest_file.open("r") as f:
                    manifest = yaml.safe_load(f)
                if manifest["disc"] == disc_info:
                    return self._config[show], manifest
        # TODO: if we get to this point, we didn't find the show or we didn't find a suitable manifest, fall back to default ripping
        return {}, {}
