import curses
import logging
import sys

from src.core.schema import Config, Envs, Env
from src.core.config_handler import get_config
from src.core.env_handler import get_packages, get_packages_for_all, get_paths


def configure_logger(log_level=logging.DEBUG, log_file="app.log"):
    logger = logging.getLogger()  # Get the root logger
    logger.setLevel(log_level)

    # Formatter for logs
    formatter = logging.Formatter(
        "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Avoid adding handlers multiple times (when using reload in FastAPI dev mode)
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    # curses.wrapper(main)
    configure_logger()
    config = get_config()
    assert config
    envs = get_paths(config)
    get_packages_for_all(envs)
    for i in envs.get_all():
        print(i.packages)
