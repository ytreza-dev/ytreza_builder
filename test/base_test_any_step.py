from abc import ABC, abstractmethod
from typing import Any

from test.conftest import CommandHandlerForTest
from src.action_plan import ActionPlan
from src.command import DummyCommand


class BaseTestAnyStep(ABC):
    def test_plan_action(self, command_handler: CommandHandlerForTest):
        (self.action(step=self.from_step(ActionPlan(), configuration={})).execute(command_handler))
        assert self.expected_command() == command_handler.history()

    def test_plan_previous_action(self, command_handler: CommandHandlerForTest):
        initial_plan = ActionPlan().prepare(DummyCommand(value="first"))

        (self.action(step=self.from_step(
            initial_plan, configuration={}))
         .execute(command_handler))

        assert list(initial_plan.prepare(*self.expected_command()).commands) == command_handler.history()

    def test_keep_configuration(self, command_handler: CommandHandlerForTest):
        initial_plan = ActionPlan().prepare(DummyCommand(value="first"))

        configuration = {"key": "value"}
        (self.action(step=self.from_step(
            initial_plan, configuration=configuration))
         .execute(command_handler))

        assert configuration == command_handler.configuration()



    @abstractmethod
    def action(self, step):
        pass

    @abstractmethod
    def expected_command(self):
        pass

    @abstractmethod
    def from_step(self, action_plan: ActionPlan, configuration: dict[str, Any]):
        pass
