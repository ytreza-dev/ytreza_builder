from dataclasses import dataclass, field

import pytest

from src.python_project_builder import SystemFilePort, PythonProject, CommandHandlerPort
from src.command import Command


@dataclass(frozen=True)
class History:
    action: str
    param: dict = field(default_factory=dict)

    def __eq__(self, other):
        return self.action == other.action and self.param == other.param


class SystemFileForTest(SystemFilePort):
    def __init__(self):
        self._history = []

    def history(self) -> list[History]:
        return self._history

    def create_directory(self, path: str):
        self._history.append(History(action="create_directory", param={"path": path}))

    def execute(self, command_line: str, working_directory: str) -> None:
        self._history.append(
            History(action="execute", param={"command_line": command_line, "working_directory": working_directory}))


class CommandHandlerForTest(CommandHandlerPort):
    def __init__(self) -> None:
        self._history: list[Command] = []

    def history(self) -> list[Command]:
        return self._history

    def execute_all(self, commands: list[Command]):
        self._history.extend(commands)



@pytest.fixture
def system_file() -> SystemFileForTest:
    return SystemFileForTest()


@pytest.fixture
def python_project(system_file: SystemFileForTest) -> PythonProject:
    return PythonProject(system_file=system_file)


@pytest.fixture()
def command_handler() -> CommandHandlerForTest:
    return CommandHandlerForTest()
