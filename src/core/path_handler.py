from typing import Optional, List, Union
from pathlib import Path
import subprocess
import logging

logger = logging.getLogger(__name__)


def get_conda_path(path: str = "") -> Optional[Path]:
    """checks if given conda path is valid,
    else finds most likely conda path"""
    if path:
        path_temp = Path(path)
        if (path_temp / "envs").exists():
            return path_temp
        raise ValueError(
            f"{path} not a valid conda path,\n it should have 'envs' directory"
        )

    anaconda_path = Path.home() / "anaconda3"
    miniconda_path = Path.home() / "miniconda3"
    if (anaconda_path / "envs").exists():
        return anaconda_path
    if (miniconda_path / "envs").exists():
        return miniconda_path
    raise ValueError("Path to conda not found, please provide it in config.json")


def get_venv_paths(
    start: str = "", dirs_to_find: List[str] = [".venv", ".env"]
) -> List[Path]:
    """gets all instance of path where path matches dirs_to_find/bin format"""
    path = Path.home() if not start else Path(start).expanduser()
    name_expr = []
    for i, name in enumerate(dirs_to_find):
        if i > 0:
            name_expr.append("-o")
        name_expr.extend(["-name", name])

    cmd = (
        ["find", path, "("]
        + name_expr
        + [")", "-type", "d", "-exec", "test", "-d", "{}/bin", ";", "-print"]
    )
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
    )
    return [
        Path(i)
        for i in result.stdout.splitlines()
        if (Path(i) / "bin" / "python").exists()
    ]


def load_paths(conda_path, venv_start, dirs_to_find):
    conda_path = get_conda_path(conda_path)
    venv_paths = get_venv_paths(start=venv_start, dirs_to_find=dirs_to_find)
