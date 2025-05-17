from pathlib import Path
from src.conda import load_config
import logging

logger = logging.getLogger()


def create_conf():
    path = Path("~/.config/pyman/config.json")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        logger.info(f"[create_conf] Created config at {path}")
    else:
        logger.info(f"[create_conf] found config at {path}")


def dump_conf():
    create_conf()
    load_config()
