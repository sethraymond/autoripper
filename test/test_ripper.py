import tempfile
from pathlib import Path

import pytest
import yaml

from autoripper.ripper.rip import Ripper


@pytest.fixture
def temp_config():
    d = tempfile.TemporaryDirectory()
    config = Path(d.name) / "shows.yaml"
    config_data = {
        "Avatar: The Last Airbender": {
            "type": "tv",
            "naming": "tvdb",
            "manifest_dir": "atla",
        }
    }
    with config.open("w") as f:
        yaml.safe_dump(config_data, f)

    manifest_dir = Path(d.name) / "manifests/atla"
    manifest_dir.mkdir(parents=True)
    test_manifest_file = manifest_dir / "book1-disk3.yaml"
    test_manifest = {
        "disc": "Book One: Water Disc 3",
        "episodes": [
            {
                "track": "0",
                "episode": "S01E17",
                "title": "The Northern Air Temple",
            },
              {
                "track": "1",
                "episode": "S01E18",
                "title": "The Waterbending Master",
              },
              {
                "track": "2",
                "episode": "S01E19",
                "title": "The Seige of the North (1)",
              },
              {
                "track": "3",
                "episode": "S01E20",
                "title": "The Seige of the North (2)",
              },
        ]
    }

    with test_manifest_file.open("w") as f:
        yaml.safe_dump(test_manifest, f)

    yield config 

def test_get_disc_info(temp_config):
    ripper = Ripper(temp_config)
    ripper.STUB = True
    show, manifest = ripper._get_disc_info()
    assert show
    assert len(manifest["episodes"]) > 1
