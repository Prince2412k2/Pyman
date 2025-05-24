from typing import List, Optional, Union
from pathlib import Path
from pydantic import BaseModel
from enum import Enum


class Kind(Enum):
    CONDA = "CONDA"
    VENV = "VENV"
    CUSTOM = "CUSTOM"
    PACKAGE = "PACKAGE"


class Package:
    def __init__(self, name, version) -> None:
        self.name: str = name
        self.version: str = version
        self.kind: Kind = Kind.PACKAGE

    def __repr__(self) -> str:
        return f"{self.name} : {self.version}\n"

    def get_name(self):
        return f"{self.name}={self.version}"


class Env:
    def __init__(self, path, kind: Kind) -> None:
        self.path: Path = path
        self.kind: Kind = kind
        self.packages: Optional[List[Package]] = None

    def __repr__(self) -> str:
        return f"{self.path}:{self.kind}\n"

    def get_name(self):
        return (
            str(self.path.name)
            if self.kind == Kind.CONDA
            else str(self.path.parent.name)
        )


class Envs:
    def __init__(
        self,
        conda_envs: List[Path],
        venvs: List[Path],
        custom_paths: List[str] = [""],
    ) -> None:
        self.conda_envs: List[Env] = [Env(i, Kind.CONDA) for i in conda_envs if i]
        self.venvs: List[Env] = [Env(i, Kind.VENV) for i in venvs if i]
        self.custom_paths: List[Env] = [
            Env(Path(i), Kind.CUSTOM) for i in custom_paths if i
        ]

    def get_all(self):
        return self.conda_envs + self.venvs + self.custom_paths

    def __repr__(self) -> str:
        return f"Envs(conda_envs=\n{self.conda_envs}\n\v,venvs=\n{self.venvs}\n\n,Cvenv=\n{self.custom_paths}"


class Config(BaseModel):
    conda_path: str
    custom_venvs: list[str]
    dirs_to_find: List[str] = [".venv", ".env"]
