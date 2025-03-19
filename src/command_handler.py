from pathlib import Path
from typing import assert_never

from src.python_project_builder import CommandHandlerPort
from src.command import Command, CreateDirectory, ExecuteShell


class CommandHandler(CommandHandlerPort):
    def execute_all(self, commands: list[Command]):
        for command in commands:
            self._execute(command)


    def _execute(self, command: Command) -> None:
        match command:
            case CreateDirectory(path=path):
                self._create_directory(path)

            case _:
                assert_never(command)

    @staticmethod
    def _create_directory(path: str) -> None:
        Path(path).mkdir()

