#!/home/prince/projects/pyman/.venv/bin/python3

from src.core.path_handler import get_conda_path
from src.core.config_handler import get_config
from src.core.schema import Config, Kind
from src.core.env_handler import get_paths
import json
import time

mapper = {Kind.CONDA: " ", Kind.CUSTOM: " ", Kind.VENV: " "}


def return_list():
    config = Config(conda_path=str(get_conda_path()))
    assert config

    paths = get_paths(config)
    lis = []

    for i in paths.get_all():
        name = i.get_name()
        icon = mapper[i.kind]
        lis.append({f"{icon} {name}": str(i.path)})
    json_list = json.dumps(lis)
    return json_list
