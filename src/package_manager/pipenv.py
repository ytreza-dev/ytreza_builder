from typing import Self

from src.action_plan import ActionPlan
from src.command import ExecuteShell


class PipenvBuiltIn:
    def __init__(self, action_plan: ActionPlan):
        self._action_plan = action_plan

    def with_pipenv(self) -> Self:
        self._action_plan = self._action_plan.prepare(
            ExecuteShell(command_line="python -m pip install --user pipenv", working_directory="."))
        return self
