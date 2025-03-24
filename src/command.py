from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class ProjectPath:
    pass


@dataclass(frozen=True)
class CreateDirectory:
    path: ProjectPath


@dataclass(frozen=True)
class ExecuteShell:
    command_line: str
    working_directory: str


Command = CreateDirectory | ExecuteShell
