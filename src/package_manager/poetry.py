from typing import Self

import src.command as cmd
import src.python_package_manager as package_manager
from src.action_plan import ActionPlan


class PoetryBuiltIn:
    def __init__(self, action_plan: ActionPlan):
        self._action_plan = action_plan

    def with_poetry(self) -> Self:
        self._action_plan = self._action_plan.prepare(
            cmd.ExecuteShell(command_line="python -m pip install --user poetry", working_directory="."),
            cmd.UsePackageManager(package_manager.Poetry()),
            cmd.CreateDirectory(path=cmd.ProjectPath()),
            cmd.ExecuteShell(command_line="poetry init", working_directory="."),
        )
        return self
