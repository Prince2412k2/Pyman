from pathlib import Path
import json
from typing import Optional, Dict
import logging

logger = logging.getLogger()


def get_conda_path(path: str) -> Optional[Path]:
    if path:
        path_temp = Path(path)
        if (path_temp / "envs").exists():
            return path_temp
        raise ValueError(
            f"{path} not a valid conda path,\n it should have 'envs' directory"
        )

    anaconda_path = Path.home() / "anaconda3"
    miniconda_path = Path.home() / "miniconda3"
    if anaconda_path.exists():
        return anaconda_path
    if miniconda_path.exists():
        return miniconda_path
    raise ValueError("Path to conda not found, please provide it in config.json")


def load_config() -> Dict[str, str]:
    path = Path("~/.config/pyman/config.json").expanduser()
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
