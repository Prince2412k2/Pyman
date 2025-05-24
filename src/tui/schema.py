from dataclasses import dataclass
from abc import ABC, abstractmethod
import curses
from enum import Enum
from pathlib import Path
from src.core.schema import Env, Kind, Package


@dataclass(frozen=True)
class TypeElement(ABC):
    icon: str
    color: int

    @abstractmethod
    def get_name(self, path: Path) -> str:
        raise NotImplementedError()


@dataclass(frozen=True)
class TypeOther(TypeElement):
    icon: str = " "
    color: int = 1

    def get_name(self, path: Path) -> str:
        return str(path.parent.name)


@dataclass(frozen=True)
class TypeConda(TypeElement):
    icon: str = " "
    color: int = 2

    def get_name(self, path: Path) -> str:
        return str(path.name)


@dataclass(frozen=True)
class TypePackage(TypeElement):
    icon: str = ""
    color: int = 4

    def get_name(self, path: Path) -> str:
        return str(path.name)


@dataclass(frozen=True)
class Mapper:
    conda: TypeConda = TypeConda()
    other_envs: TypeOther = TypeOther()
    package: TypePackage = TypePackage()

    def get(self, element: Env | Package) -> TypeElement:
        if element.kind == Kind.CONDA:
            return self.conda
        elif element.kind == Kind.PACKAGE:
            return self.package
        else:
            return self.other_envs


class WindowTypes(Enum):
    ENV = "ENV"
    PACKAGE = "PACKAGE"
    DATA = "DATA"


@dataclass
class State:
    focus: WindowTypes = WindowTypes.ENV
