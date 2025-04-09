from typing import Self

import ytreza_builder.command as cmd
import ytreza_builder.python.package_manager.type
from ytreza_builder.action_plan import ActionPlan


class PoetryBuiltIn:
    def __init__(self, action_plan: ActionPlan):
        self._action_plan = action_plan

    def with_poetry(self) -> Self:
        self._action_plan = self._action_plan.prepare(
            cmd.ExecuteShell(command_line="python -m pip install --user poetry", working_directory=cmd.ProjectParentPath()),
            cmd.ExecuteShell(command_line="poetry new {project_name}", working_directory=cmd.ProjectParentPath()),
            cmd.UsePackageManager(ytreza_builder.python.package_manager.type.Poetry()),
        )
        return self
