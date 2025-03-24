from typing import Self

from src.command import Command, ExecuteShell
from src.command_handler_port import CommandHandlerPort


class PipenvBuiltIn:
    def __init__(self, commands: list[Command]):
        self._commands: list[Command] = commands

    def with_pipenv(self) -> Self:
        self._commands.append(ExecuteShell(command_line="python -m pip install --user pipenv", working_directory="."))
        return self
