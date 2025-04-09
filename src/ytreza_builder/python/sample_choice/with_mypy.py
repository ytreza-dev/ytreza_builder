from typing import Self

from ytreza_builder import command
from ytreza_builder.action_plan import ActionPlan


class WithMypy:
    def __init__(self, action_plan: ActionPlan):
        self._action_plan = action_plan

    def with_mypy(self) -> Self:
        self._action_plan=self._action_plan.prepare(command.CopySample(source="python/mypy", destination=command.ProjectPath()))
        return self
