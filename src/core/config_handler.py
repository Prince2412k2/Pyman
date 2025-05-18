import os
from typing import Dict, List, Optional

from pydantic_core import ValidationError
import json
from pathlib import Path
import logging

from src.core.path_handler import get_conda_path, get_venv_paths
from src.core.schema import Config, Env

logger = logging.getLogger(__name__)
with open("./src/core/.path_to_config", "r") as file:
    temp = file.read()
    temp_json = json.loads(temp)
    CONFIG_PATH = Path(temp_json["path"]).expanduser()


def read_conf() -> Optional[Dict[str, str]]:
    path = CONFIG_PATH
    with open(path, "r") as file:
        data = file.read()
    try:
        config = json.loads(data)
    except json.JSONDecodeError as e:
        logger.error(f"[load_config] : {e}")
        raise
    except FileNotFoundError:
        logger.error(f"[load_config] Config file not found at {path}")
        raise
    return config


def create_conf():
    """create config.json if not exist"""
    path = CONFIG_PATH
    if not path.exists():
        logger.info(f"making config at {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path = path / "config.json" if not path.name == "config.json" else path
        path.touch()

        config = Config(
            conda_path="",
            custom_venvs=[""],
        )

        config = reload_conda_path(config)
        with open(path, "+w") as conf:
            conf.write(config.model_dump_json())
        logger.info(f"[create_conf] Created config at {path}")
        return config
    else:
        logger.info(f"[create_conf] found config at {path}")


def load_conf() -> Optional[Config]:
    """read config.json"""
    create_conf()
    config_json = read_conf()
    if not config_json:
        return
    try:
        return Config.model_validate(config_json)

    except ValidationError:
        logger.error("[read_conf] : failed to validate json cofig")
        raise


def reload_conda_path(config: Config, path: str = ""):
    new_conda_path = get_conda_path(path)
    config.conda_path = str(new_conda_path)
    return config


def add_to_dirs_to_find(config: Config, name: str):
    """add dir to dirs_to_find in config"""
    if name in config.dirs_to_find:
        return
    config.dirs_to_find.append(name)


def remove_to_dirs_to_find(config: Config, name: str):
    """remove dir to dirs_to_find in config"""
    if name not in config.dirs_to_find:
        return
    config.dirs_to_find.remove(name)


def get_config() -> Optional[Config]:
    return load_conf()
