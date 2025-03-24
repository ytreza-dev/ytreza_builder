from typing import Self

from src import command
from src.action_plan import ActionPlan


class PytestBuiltIn:
    def __init__(self, action_plan: ActionPlan):
        self._action_plan = action_plan

    def with_pytest(self) -> Self:
        self._action_plan = self._action_plan.prepare(
            command.InstallPackage(package_name="pytest"))
        return self
