from typing import Self

import ytreza_builder.command as cmd
import ytreza_builder.python.package_manager.type
from ytreza_builder.action_plan import ActionPlan


class PipenvBuiltIn:
    def __init__(self, action_plan: ActionPlan):
        self._action_plan = action_plan

    def with_pipenv(self) -> Self:
        self._action_plan = self._action_plan.prepare(
            cmd.CreateDirectory(cmd.ProjectPath()),
            cmd.ExecuteShell(command_line="python -m pip install --user pipenv", working_directory=cmd.ProjectPath()),
            cmd.UsePackageManager(ytreza_builder.python.package_manager.type.Pipenv()),
        )
        return self
