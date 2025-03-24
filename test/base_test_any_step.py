from abc import ABC, abstractmethod

from test.conftest import CommandHandlerForTest
from src.action_plan import ActionPlan
from src.command import DummyCommand


class BaseTestAnyStep(ABC):
    def test_plan_action(self, command_handler: CommandHandlerForTest):
        (self.action(step=self.from_step(ActionPlan())).execute(command_handler))
        assert self.expected_command() == command_handler.history()

    def test_plan_previous_action(self, command_handler: CommandHandlerForTest):
        initial_plan = ActionPlan().prepare(DummyCommand(value="first"))

        (self.action(step=self.from_step(
            initial_plan))
         .execute(command_handler))

        assert list(initial_plan.prepare(*self.expected_command()).commands) == command_handler.history()



    @abstractmethod
    def action(self, step):
        pass

    @abstractmethod
    def expected_command(self):
        pass

    @abstractmethod
    def from_step(self, action_plan: ActionPlan):
        pass
