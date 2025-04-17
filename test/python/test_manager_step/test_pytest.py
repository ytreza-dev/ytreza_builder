from typing import Any

import ytreza_builder.command as cmd
from test.base_test_any_step import BaseTestAnyStep
from ytreza_builder.action_plan import ActionPlan
from ytreza_builder.python.python_project_builder import PythonTestManagerChoice


class TestTestManagerChoice(BaseTestAnyStep):
    def from_step(self, action_plan: ActionPlan, configuration: dict[str, Any]) -> PythonTestManagerChoice:
        return PythonTestManagerChoice(action_plan=action_plan, configuration=configuration)

    def action(self, step: PythonTestManagerChoice) -> PythonTestManagerChoice:
        return step.with_pytest()

    def expected_command(self) -> list[cmd.Command]:
        return [cmd.InstallPackage(package_name="pytest")]
