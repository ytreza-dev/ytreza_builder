from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class CreateDirectory:
    path: str


@dataclass(frozen=True)
class ExecuteShell:
    command_line: str


Command = Union[CreateDirectory, ExecuteShell]
