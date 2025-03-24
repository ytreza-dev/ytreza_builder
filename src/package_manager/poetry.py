from typing import Self

from src.action_plan import ActionPlan
from src.command import Command, ExecuteShell
from src.command_handler_port import CommandHandlerPort


class PoetryBuiltIn:
    def __init__(self, action_plan: ActionPlan):
        self._action_plan = action_plan

    def with_poetry(self) -> Self:
        self._action_plan = self._action_plan.prepare(
            ExecuteShell(command_line="python -m pip install --user poetry", working_directory=".")
        )
        return self
