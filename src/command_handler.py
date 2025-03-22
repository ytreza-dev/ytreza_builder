import subprocess
from pathlib import Path
from typing import assert_never

from src.command_handler_port import CommandHandlerPort
from src.command import Command, CreateDirectory, ExecuteShell


class CommandHandler(CommandHandlerPort):
    def execute_all(self, commands: list[Command]):
        for command in commands:
            self._execute(command)


    def _execute(self, command: Command) -> None:
        match command:
            case CreateDirectory(path=path):
                self._create_directory(path)

            case ExecuteShell(command_line=command_line, working_directory=working_directory):
                self._execute_shell(command_line=command_line, working_directory=working_directory)

            case _:
                assert_never(command)

    @staticmethod
    def _create_directory(path: str) -> None:
        Path(path).mkdir()

    def _execute_shell(self, command_line: str, working_directory: str):
        subprocess.run(command_line.split(" "), cwd=working_directory)

