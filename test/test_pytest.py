from base_test_any_step import BaseTestAnyStep
from src import command
from src.action_plan import ActionPlan
from src.python_project_builder import PythonTestManagerChoice


class TestTestManagerChoice(BaseTestAnyStep):
    def from_step(self, action_plan: ActionPlan):
        return PythonTestManagerChoice(action_plan=action_plan, configuration={})

    def action(self, step: PythonTestManagerChoice):
        return step.with_pytest()

    def expected_command(self):
        return [command.InstallPackage(package_name="pytest")]
