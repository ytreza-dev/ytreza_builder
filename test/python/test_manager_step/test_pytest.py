from typing import Any

from test.base_test_any_step import BaseTestAnyStep
from ytreza_builder import command
from ytreza_builder.action_plan import ActionPlan
from ytreza_builder.python.python_project_builder import PythonTestManagerChoice


class TestTestManagerChoice(BaseTestAnyStep):
    def from_step(self, action_plan: ActionPlan, configuration: dict[str, Any]):
        return PythonTestManagerChoice(action_plan=action_plan, configuration=configuration)

    def action(self, step: PythonTestManagerChoice):
        return step.with_pytest()

    def expected_command(self):
        return [command.InstallPackage(package_name="pytest")]
