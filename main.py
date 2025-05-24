import curses
import logging
import sys

from src.core.schema import Config, Envs, Env
from src.core.config_handler import get_config

from src.tui.main import main


def configure_logger(log_level=logging.DEBUG, log_file="app.log"):
    logger = logging.getLogger()  # Get the root logger
    logger.setLevel(log_level)

    # Formatter for logs
    formatter = logging.Formatter(
        "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    # configure_logger()
    logging.basicConfig(filename="curses.log", level=logging.INFO)
    curses.wrapper(main)
    # config = get_config()
    # assert config
    # envs = get_paths(config)
    # get_packages_for_all(envs)
    # for i in envs.get_all():
    #     print(i.packages)
