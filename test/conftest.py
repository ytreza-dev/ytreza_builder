from typing import Any

import pytest

from ytreza_builder.action_plan import ActionPlan
from ytreza_builder.command import Command, CreateDirectory, ProjectPath
from ytreza_builder.command_handler_port import CommandHandlerPort
from test.system_file_for_test import SystemFileForTest


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


@pytest.fixture()
def command_handler() -> CommandHandlerForTest:
    return CommandHandlerForTest()


@pytest.fixture
def any_plan() -> ActionPlan:
    return ActionPlan().prepare(CreateDirectory(path=ProjectPath()))
