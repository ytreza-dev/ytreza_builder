from typing import Any

from test.base_test_any_step import BaseTestAnyStep
import src.command as cmd
from src.action_plan import ActionPlan
from src.python_project_builder import PythonTestManagerChoice, PythonSampleChoice


class TestTestManagerChoice(BaseTestAnyStep):
    def from_step(self, action_plan: ActionPlan, configuration: dict[str, Any]):
        return PythonSampleChoice(action_plan=action_plan, configuration=configuration)

    def action(self, step: PythonSampleChoice):
        return step.with_failing_test()

    def expected_command(self):
        return [cmd.CopySample(source="python/failing_test", destination=cmd.ProjectPath())]
