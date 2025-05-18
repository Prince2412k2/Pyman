from os import name
from typing import List, Optional, Dict, Union
from pathlib import Path
import subprocess
import logging
from enum import Enum
import json

from src.core.schema import Config, Env, Envs, Kind, Package
from src.core.path_handler import get_venv_paths

logger = logging.getLogger(__name__)


def get_conda_envs(config: Config) -> List[Path]:
    path_to_envs = Path(config.conda_path) / "envs"
    logger.info(path_to_envs)
    cmd = ["ls", str(path_to_envs)]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )

    logger.info(result.stdout)
    logger.info(result.stderr)
    return [
        path_to_envs / i
        for i in result.stdout.strip().splitlines()
        if (path_to_envs / i / "bin" / "python").exists()
    ]


def get_packages(env: Env):
    """uv pip list --verbose --directory ./pyman --format=json"""
    # venv_cmd = [
    #     "uv",
    #     "pip",
    #     "list",
    #     f"--directory={str(env.path)}",
    #     "--format=json",
    # ]
    cmd = [
        "uv",
        "pip",
        "list",
        "-p",
        str(env.path / "bin" / "python"),
        "--format=json",
    ]
    # cmd = conda_cmd if env.kind == Kind.CONDA else venv_cmd
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if result.returncode == 0:
        packages = json.loads(result.stdout)
        if packages:
            env.packages = [
                Package(name=i["name"], version=i["version"]) for i in packages
            ]
            return env
        logger.info(f"No packages found for env:{env.path}")

    logger.warning(f"subprocess failed for env : {env.path}")


def get_packages_for_all(envs: Envs):
    for i in envs.get_all():
        env = get_packages(i)
        if env:
            print(env.path)
            print(env.packages)
            print()


def get_paths(config: Config):
    conda_paths: List[Path] = get_conda_envs(config)
    venv_paths: List[Path] = get_venv_paths()
    custom_venvs: List[str] = list(config.custom_venvs)
    return Envs(conda_envs=conda_paths, venvs=venv_paths, custom_paths=custom_venvs)
