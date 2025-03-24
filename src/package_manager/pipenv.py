from typing import Self

import src.command as cmd
from src.action_plan import ActionPlan


class PipenvBuiltIn:
    def __init__(self, action_plan: ActionPlan):
        self._action_plan = action_plan

    def with_pipenv(self) -> Self:
        self._action_plan = self._action_plan.prepare(
            cmd.ExecuteShell(command_line="python -m pip install --user pipenv", working_directory="."),
            cmd.UsePackageManager("pipenv")
        )
        return self
