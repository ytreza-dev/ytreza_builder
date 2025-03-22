from typing import Self

from conftest import CommandHandlerForTest
from src.command import ExecuteShell, Command
from src.command_handler import CommandHandler
from src.python_project_builder import CommandHandlerPort


class PipenvBuiltIn:
    def __init__(self, commands: list[Command]):
        self._commands: list[Command] = commands

    def with_pipenv(self) -> Self:
        self._commands.append(ExecuteShell(command_line="python -m pip install --user pipenv", working_directory="."))
        return self

    def execute(self, command_handler: CommandHandlerPort) -> None:
        command_handler.execute_all(self._commands)


def test_create_project_with_pipenv(command_handler: CommandHandlerForTest):
    project = PipenvBuiltIn(commands=[])
    (project
     .with_pipenv()
     .execute(command_handler))

    assert ExecuteShell(command_line="python -m pip install --user pipenv",
                        working_directory=".") in command_handler.history()
