from typing import Self

from src.command import Command, ExecuteShell
from src.command_handler_port import CommandHandlerPort


class PoetryBuiltIn:
    def __init__(self, commands: list[Command]):
        self._commands: list[Command] = commands

    def with_poetry(self) -> Self:
        self._commands.append(ExecuteShell(command_line="python -m pip install --user poetry", working_directory="."))
        return self

    def execute(self, command_handler: CommandHandlerPort) -> None:
        command_handler.execute_all(self._commands, {})
