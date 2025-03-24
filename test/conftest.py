from dataclasses import dataclass, field
from typing import Any

import pytest

from src.action_plan import ActionPlan
from src.command import Command, CreateDirectory, ProjectPath
from src.command_handler_port import CommandHandlerPort
from src.python_project_builder import SystemFilePort, PythonProject


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
        self._configuration : dict[str, Any]= {}
        self._history: list[Command] = []

    def history(self) -> list[Command]:
        return self._history

    def configuration(self) -> dict[str, Any]:
        return self._configuration

    def execute_all(self, configuration: dict[str, Any], action_plan: ActionPlan):
        self._configuration = configuration
        self._history.extend(action_plan.commands)



@pytest.fixture
def system_file() -> SystemFileForTest:
    return SystemFileForTest()


@pytest.fixture
def python_project(system_file: SystemFileForTest) -> PythonProject:
    return PythonProject()


@pytest.fixture()
def command_handler() -> CommandHandlerForTest:
    return CommandHandlerForTest()


@pytest.fixture
def any_plan() -> ActionPlan:
    return ActionPlan().prepare(CreateDirectory(path=ProjectPath()))
